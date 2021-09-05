from vk_api.keyboard import VkKeyboard, VkKeyboardColor

colors = {
    "BLUE": VkKeyboardColor.PRIMARY,
    "GREEN": VkKeyboardColor.POSITIVE,
    "RED": VkKeyboardColor.NEGATIVE,
    "WHITE": VkKeyboardColor.SECONDARY
}
keyboards_list = {
    "EMPTY": VkKeyboard.get_empty_keyboard()
}


class Keyboard:
    def __init__(self, keyboard_id, inline=False, callback_msg=None):
        self.id = keyboard_id
        self.one_time = False
        self.inline = inline
        self.buttons_amount = 0
        self.buttons = []
        self.keyboard = None
        self.callback_msg = callback_msg

    def add_rows(self, rows_amount=1):
        for _ in range(min(max(abs(rows_amount), 1), 10)):
            self.buttons.append([])

    def add_button(self, text, color="WHITE", row=1, callback=False):
        try:
            if (self.inline and self.buttons_amount < 10) or (not self.inline and self.buttons_amount < 30):
                self.buttons[row-1].append([text, color, callback])
                self.buttons_amount += 1

            else:
                print("[!!] Достигнуто максимальное количество кнопок.")

        except IndexError:
            print("[!!] Неправильно указан ряд кнопки. Кнопка будет добавлена в существующий/новый ряд.")

            if len(self.buttons) == 0:
                self.add_rows()
                self.add_button(text, color, row)
                print("[!!] Нет рядов. Кнопка будет добавлена в новый ряд.")

            else:
                self.add_button(text, color)
                print("[!!] Неправильно указан ряд кнопки. Кнопка будет добавлена в первый ряд.")

    def get_keyboard(self):
        if not self.inline:
            keyboard = VkKeyboard(one_time=self.one_time)

        else:
            keyboard = VkKeyboard(inline=True)

        for row in self.buttons:
            for button in row:
                if button[2]:
                    if self.inline:
                        keyboard.add_callback_button(
                            label=button[0],
                            color=colors[button[1].upper()],
                            payload=button[2]
                        )

                    else:
                        print("[!!] Указан параметр callback, однако параметр inline = False.")

                else:
                    keyboard.add_button(
                        label=button[0],
                        color=colors[button[1].upper()]
                    )

            if self.buttons[-1] != row:
                keyboard.add_line()

        vk_keyboard = keyboard.get_keyboard()
        return vk_keyboard

    def bake(self):
        global keyboards_list

        self.keyboard = self.get_keyboard()
        keyboards_list[self.id] = self


def get_by_id(keyboard_id):
    try:
        result = keyboards_list[keyboard_id]

    except KeyError:
        result = None

    return result.keyboard


def get_msg(keyboard_id):
    try:
        result = keyboards_list[keyboard_id]

    except KeyError:
        result = None

    return result.callback_msg


# Создание клавиатур
_ = Keyboard("EXAMPLE", True, "Первое меню")
_.add_rows(2)
_.add_button("Уведомление", "BLUE", 1, {
    "type": "show_snackbar",
    "text": "Уведомление. Исчезнет автоматически, или свайпом."
})
_.add_button("Другая клавиатура", "RED", 2, {
    "type": "zb_EXAMPLE_2"
})
_.bake()

_ = Keyboard("EXAMPLE_2", True, "Второе меню")
_.add_rows(2)
_.add_button("Обычная кнопка", "WHITE")
_.add_button("Обратно", "RED", 2, {
    "type": "zb_EXAMPLE"
})
_.bake()
