from datetime import datetime, timezone

from telegram import KeyboardButton, ReplyKeyboardMarkup

from foodplan_bot.models import Subscription, DishRecipe


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


def create_subscriptions_keyboard(chat_id):
    subscriptions = Subscription.objects.filter(
        user__tg_chat_id=chat_id
    ).filter(is_paid=True)
    keyboard = list()
    for subscription in subscriptions:
        keyboard.append(
            [
                KeyboardButton(
                    text=(
                        f'Подписка c id {subscription.id} на '
                        f'{subscription.menu_type.lower()} меню до '
                        f'{subscription.expiration_date.strftime("%d-%m-%Y")}'
                    )
                )
            ]
        )
    return make_reply_markup(keyboard)


def create_day_menu_keyboard(subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    keyboard = list()
    menu_date = datetime.now(timezone.utc).strftime("%d-%m-%Y")
    for dish_id in subscription.menu[menu_date].values():
        dish = DishRecipe.objects.get(id=dish_id)
        keyboard.append(
            [
                KeyboardButton(
                    text=(
                        f'{dish.name}'
                    )
                )
            ]
        )
    return make_reply_markup(keyboard)
