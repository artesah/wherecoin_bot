from aiogram import Dispatcher
from aiogram.dispatcher.filters import (
    ChatTypeFilter,
    CommandStart,
    CommandHelp,
    Command,
)

from apps.bot.src.filters.filters import (
    BotAdminFilter,
    ChatExistsFiler,
    UserFilter,
)


def setup(dp: Dispatcher):
    dp.filters_factory.bind(ChatTypeFilter),
    dp.filters_factory.bind(CommandStart),
    dp.filters_factory.bind(CommandHelp),
    dp.filters_factory.bind(Command),
    dp.filters_factory.bind(BotAdminFilter)
    dp.filters_factory.bind(ChatExistsFiler)
    dp.filters_factory.bind(UserFilter)
