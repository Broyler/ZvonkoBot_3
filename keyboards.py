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
    def __init__(self, keyboard_id, inline=False):
        self.id = keyboard_id
        self.one_time = False
        self.inline = inline
        self.buttons_amount = 0
        self.buttons = []
        self.keyboard = None

    def add_rows(self, rows_amount=1):
        for i in range(min(max(abs(rows_amount), 1), 10)):
            self.buttons.append([])

    def add_button(self, text, color="WHITE", row=1):
        try:
            if (self.inline and self.buttons_amount < 10) or (not self.inline and self.buttons_amount < 30):
                self.buttons[row-1].append([text, color])
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
        keyboards_list[self.id] = self.keyboard


def get_by_id(keyboard_id):
    try:
        result = keyboards_list[keyboard_id]

    except KeyError:
        result = None

    return result


# Создание клавиатур
_ = Keyboard("EXAMPLE", True)
_.add_rows(3)
_.add_button("Да", "GREEN")
_.add_button("Нет", "RED", 1)
_.add_button("Белый", "WHITE", 2)
_.add_button("Синий", "BLUE", 2)
_.add_button("Зелёный", "GREEN", 2)
_.add_button("Красный", "RED", 2)
_.add_button("3й ряд", "WHITE", 3)
_.add_button("2я кнопка в 3м ряду", "WHITE", 3)
_.bake()
