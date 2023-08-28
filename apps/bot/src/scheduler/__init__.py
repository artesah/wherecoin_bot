import importlib

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .created_operations_sender import job as created_operations_sender_job
from ...config import SCHEDULER_CONFIG


def _get_job_func(module_name):
    monitoring_module = importlib.import_module(
        f"apps.bot.src.scheduler.{module_name}"
    )

    return getattr(monitoring_module, "job")


def init_scheduler(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.start()
    for module_name, config in SCHEDULER_CONFIG.items():
        scheduler.add_job(
            func=_get_job_func(module_name),
            args=(bot,),
            **config
        )
