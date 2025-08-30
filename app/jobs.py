import asyncio
import os
from app.drive import get_gdrive_service, list_files, download_file
from app.telegram import send_document
from app.config import Settings, SOURCES
from app.models import File
from app.db import AsyncSessionLocal
from app.utils import extract_metadata, match_filters, render_caption
from sqlalchemy.future import select

async def scan_sources():
    async with AsyncSessionLocal() as db:
        for src in SOURCES:
            srv = get_gdrive_service(src['credentials_path'])
            for folder_id in src['drive_folders']:
                files = await asyncio.get_event_loop().run_in_executor(
                    None, list_files, srv, folder_id, src.get('filters', {}).get('include_mime')
                )
                for gfile in files:
                    if not match_filters(gfile, src.get('filters', {})):
                        continue
                    existing = await db.execute(select(File).where(File.file_id == gfile['id']))
                    if existing.scalars().first():
                        continue
                    meta = extract_metadata(gfile)
                    caption = render_caption(
                        Settings.CAPTION_TEMPLATE,
                        src['author_tag'],
                        meta['type_tag'],
                        meta['created_ymd'],
                        meta['original_name']
                    )
                    new_file = File(
                        file_id=gfile['id'],
                        source_id=src['source_id'],
                        original_name=gfile['name'],
                        size=gfile.get('size'),
                        status="new",
                        caption=caption,
                        meta=meta,
                    )
                    db.add(new_file)
                await db.commit()

async def worker():
    async with AsyncSessionLocal() as db:
        q = await db.execute(select(File).where(File.status == "new").limit(5))
        for file in q.scalars().all():
            src = next(s for s in SOURCES if s["source_id"] == file.source_id)
            srv = get_gdrive_service(src['credentials_path'])
            try:
                tmp_path = await asyncio.get_event_loop().run_in_executor(
                    None, download_file, srv, file.file_id, file.original_name
                )
                msg_id = await send_document(Settings.TELEGRAM_CHANNEL_ID, tmp_path, file.caption)
                srv.files().delete(fileId=file.file_id).execute()
                file.status = "deleted"
                file.telegram_message_id = str(msg_id)
                await db.commit()
                os.remove(tmp_path)
            except Exception as e:
                file.status = "error"
                file.try_count += 1
                await db.commit()

async def scheduler_loop():
    while True:
        await scan_sources()
        await worker()
        await asyncio.sleep(Settings.SCAN_INTERVAL)
