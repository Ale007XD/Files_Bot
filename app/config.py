import os
import yaml

class Settings:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    DATABASE_URL = (
        os.getenv('DATABASE_URL') or
        f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
    )
    SOURCES_CONFIG_PATH = os.getenv('SOURCES_CONFIG_PATH', "/app/sources.yaml")
    CAPTION_TEMPLATE = os.getenv('CAPTION_TEMPLATE', '{author_tag} {type_tag} {created_ymd}\n{original_name}')
    SCAN_INTERVAL = int(os.getenv('SCAN_INTERVAL', 300))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

def load_sources():
    with open(Settings.SOURCES_CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    return config['sources']

SOURCES = load_sources()
