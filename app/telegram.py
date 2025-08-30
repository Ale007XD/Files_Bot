from aiogram.client.bot import Bot
from aiogram.types import FSInputFile
from app.config import Settings

bot = Bot(token=Settings.BOT_TOKEN)

async def send_document(channel, file_path, caption):
    input_file = FSInputFile(file_path, filename=file_path.split('/')[-1])
    msg = await bot.send_document(
        chat_id=channel,
        document=input_file,
        caption=caption,
        disable_notification=True,
    )
    return msg.message_id
