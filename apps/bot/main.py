from aiogram import executor

from apps.bot.src import filters, middlewares
from apps.bot.src.utils import send_message_to_admins


async def _on_startup(dp):
    filters.setup(dp)
    middlewares.setup(dp)

    await send_message_to_admins(dp, "Hello World!")


def run():
    from apps.bot.src.handlers import dp

    executor.start_polling(dp, on_startup=_on_startup)


if __name__ == "__main__":
    run()
