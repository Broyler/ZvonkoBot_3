import vk_api.vk_api
from files import vk_settings
from vk_api.bot_longpoll import VkBotLongPoll
from random import randint
from keyboards import get_by_id


class ZvonkoBot:
    def __init__(self):
        self.vk = vk_api.VkApi(token=vk_settings.token)
        self.vk_long_poll = VkBotLongPoll(self.vk, abs(vk_settings.group_id))
        self.vk_api = self.vk.get_api()

    def msg_send(self, uid, msg, keyboard=None):
        message_id = self.vk_api.messages.send(
            peer_id=uid,
            message=msg,
            random_id=randint(-10000000000, 10000000000),
            keyboard=None if not get_by_id(keyboard) else get_by_id(keyboard).keyboard
        )
        return message_id
