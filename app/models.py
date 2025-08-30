from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'
    file_id = mapped_column(String, primary_key=True)
    source_id = mapped_column(String, nullable=False)
    status = mapped_column(String, default="new")
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    original_name = mapped_column(String)
    size = mapped_column(Integer)
    caption = mapped_column(Text)
    telegram_message_id = mapped_column(String, nullable=True)
    published_at = mapped_column(DateTime, nullable=True)
    deleted_at = mapped_column(DateTime, nullable=True)
    try_count = mapped_column(Integer, default=0)
    meta = mapped_column(JSONB, default={})
