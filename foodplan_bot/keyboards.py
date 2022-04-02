from telegram import KeyboardButton, ReplyKeyboardMarkup


def make_reply_markup(keyboard):
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )    


def create_start_keyboard():
    keyboard = [
        [KeyboardButton(text='Старт')],
    ]
    return make_reply_markup(keyboard)


def create_registration_keyboard():
    keyboard = [
        [KeyboardButton(text='Регистрация')],
        [KeyboardButton(text='Отмена')],
    ]
    return make_reply_markup(keyboard)


def create_initial_keyboard():
    keyboard = [
        [KeyboardButton(text='Сформировать подписку')],
        [KeyboardButton(text='Мои подписки')],
        [KeyboardButton(text='Отмена')],
    ]
    return make_reply_markup(keyboard)


def create_menu_type_keyboard():
    keyboard = [
        [KeyboardButton(text='Классическое')],
        [KeyboardButton(text='Вегетарианское')],
        [KeyboardButton(text='Низкоуглеводное')],
        [KeyboardButton(text='Кето')],
        [KeyboardButton(text='Отмена')],
    ]
    return make_reply_markup(keyboard)


def create_allergy_keyboard():
    keyboard = [
        [KeyboardButton(text='Рыба и морепродукты')],
        [KeyboardButton(text='Мясо')],
        [KeyboardButton(text='Зерновые')],
        [KeyboardButton(text='Продукты пчеловодства')],
        [KeyboardButton(text='Орехи и бобовые')],
        [KeyboardButton(text='Молочные продукты')],
        [KeyboardButton(text='Далее')],
        [KeyboardButton(text='Отмена')],
    ]
    return make_reply_markup(keyboard)


def create_subscription_period_keyboard():
    keyboard = [
        [KeyboardButton(text='1 месяц')],
        [KeyboardButton(text='3 месяца')],
        [KeyboardButton(text='6 месяцев')],
        [KeyboardButton(text='12 месяцев')],
        [KeyboardButton(text='Отмена')],
    ]
    return make_reply_markup(keyboard)


def create_payment_keyboard():
    keyboard = [
        [KeyboardButton(text='Оплатить')],
        [KeyboardButton(text='Отмена')],
    ]
    return make_reply_markup(keyboard)