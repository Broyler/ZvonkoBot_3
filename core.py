import vk_api.vk_api
from files import vk_settings
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint
from keyboards import get_by_id, get_msg
from carousels import cget_by_id
from json import dumps, loads


class ZvonkoBot:
    def __init__(self):
        self.vk = vk_api.VkApi(token=vk_settings.token)
        self.vk_long_poll = VkBotLongPoll(self.vk, abs(vk_settings.group_id))
        self.vk_api = self.vk.get_api()

    def msg_send(self, uid, msg, keyboard=None, carousel=None):
        try:
            message_id = self.vk_api.messages.send(
                peer_id=uid,
                message=msg,
                random_id=randint(-10000000000, 10000000000),
                keyboard=None if not keyboard or not get_by_id(keyboard) else get_by_id(keyboard),
                template=None if not carousel or not cget_by_id(carousel) else dumps(cget_by_id(carousel))
            )
            return message_id

        except vk_api.exceptions.ApiError as error:
            print("[!] Сообщение не дошло, id: {}. Ошибка ApiError {}".format(str(uid), error))
            return 1

    def long_poll(self):
        for event in self.vk_long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_EVENT:
                if event.object.payload.get('type') == "show_snackbar":
                    if len(str(event.object.payload.get('text'))) <= 50:
                        self.vk_api.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=dumps(event.object.payload))

                    else:
                        print("[!!] Длина сообщения уведомления более чем 50 символов. Уведомление не будет отправлено")

                elif event.object.payload.get('type')[0:2].lower() == 'zb':
                    if get_by_id(event.object.payload.get('type')[3:]):
                        self.vk_api.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=get_msg(event.object.payload.get('type')[3:]),
                            conversation_message_id=event.obj.conversation_message_id,
                            keyboard=get_by_id(event.object.payload.get('type')[3:])
                        )

                    else:
                        print("[!!] Callback кнопка пытается вызвать не существующую клавиатуру. Проверьте синтаксис")
