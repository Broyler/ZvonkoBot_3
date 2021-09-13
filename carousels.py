from vk_api.keyboard import VkKeyboardColor

colors = {
    "BLUE": VkKeyboardColor.PRIMARY,
    "GREEN": VkKeyboardColor.POSITIVE,
    "RED": VkKeyboardColor.NEGATIVE,
    "WHITE": VkKeyboardColor.SECONDARY
}
carousels_list = {}


class Carousel:
    def __init__(self, carousel_id):
        self.carousel_id = str(carousel_id)
        self.object = {
            "type": "carousel",
            "elements": []
        }

    def add_card(self, title=None, description=None, photo_id=None):
        if len(self.object["elements"]) < 10:
            self.object["elements"].append({
                "buttons": []
            })

            if title and description:
                self.object["elements"][-1]["title"] = str(title)
                self.object["elements"][-1]["description"] = str(description)

            if photo_id:
                self.object["elements"][-1]["photo_id"] = str(photo_id)
                self.object["elements"][-1]["action"] = {
                    "type": "open_photo"
                }

            else:
                self.object["elements"][-1]["action"] = {
                    "type": "open_link",
                    "link": "https://vk.com"
                }

        else:
            print("[!!] Достигнуто максимальное количество карточек в клавиатуре.")

    def add_button(self, label, card_id=1):
        self.object["elements"][int(card_id)-1]["buttons"].append({
            "action": {
                "type": "text",
                "label": str(label),
                "payload": {}
            }
        })

    def bake(self):
        global carousels_list
        carousels_list[str(self.carousel_id)] = self


def cget_by_id(carousel_id):
    try:
        result = carousels_list[str(carousel_id)].object

    except KeyError:
        result = None

    return result


_ = Carousel("EXAMPLE")
_.add_card(
    title="Пример карточки в карусели.",
    description="Описание карточки. Обязательно если задан title.",
    photo_id="-156104648_457240158"
)
_.add_button("Кнопка 1")
_.add_button("Кнопка 2")
_.add_button("Закрыть")
_.bake()
