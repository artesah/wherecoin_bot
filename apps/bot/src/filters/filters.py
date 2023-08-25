from aiogram import types
from aiogram.dispatcher.filters import BoundFilter, Filter

from apps.bot.config import BOT_ADMINS
from libs.models import Chat, User


class BotAdminFilter(BoundFilter):
    async def check(self, update: types.Message):
        return str(update.from_user.id) in BOT_ADMINS


class ChatExistsFiler(Filter):
    async def check(self, update: types.Message):
        return Chat.select(Chat.id).where(Chat.id == update.from_user.id).exists()


class UserFilter(Filter):
    async def check(self, update: types.Message or types.CallbackQuery):
        if isinstance(update, types.Message):
            # tg_bot = update.bot
            # tg_chat = update.chat
            tg_user = update.from_user
        elif isinstance(update, types.CallbackQuery):
            # tg_bot = update.bot
            # tg_chat = update.message.chat
            tg_user = update.from_user
        else:
            raise NotImplementedError

        current_user = User.ServiceClass.get_by_chat_id(tg_user.id)
        if current_user is None:
            return False

        if current_user.is_blocked:
            return False

        return {"current_user": current_user}
