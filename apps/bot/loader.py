import logging

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # TODO RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from playhouse.pool import PooledPostgresqlExtDatabase
from apps.bot.config import (
    LOG_CONFIG,
    BOT_TOKEN,
    POSTGRES_CONFIG,
    CONTENT_FILENAME,
)
from apps.bot.src.content import load_content
from apps.bot.src.scheduler import init_scheduler
from libs.models import database
from libs.services.services import init_services

logging.basicConfig(**LOG_CONFIG)

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
content = load_content(filename=CONTENT_FILENAME)

database.initialize(PooledPostgresqlExtDatabase(**POSTGRES_CONFIG))

init_services()
init_scheduler(scheduler, bot)
