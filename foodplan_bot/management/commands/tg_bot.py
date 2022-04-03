from datetime import datetime, timezone, timedelta
from enum import Enum
from textwrap import dedent

import logging
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)
from telegram.ext import (
    CallbackContext,
    MessageHandler,
    Filters,
    ConversationHandler,
    CommandHandler,
    Updater
)

from foodplan_bot import keyboards
from foodplan_bot.models import Allergy, DishRecipe, Subscription, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            main()
        except Exception as exc:
            raise CommandError(exc)


class States(Enum):
    START = 1
    REGISTRATION = 2
    CREATE_SUBSCRIPTION = 3
    INPUT_NAME = 4
    INPUT_PHONE = 5
    MENU_TYPE = 6
    EATING_COUNT = 7
    ALLERGY = 8
    INPUT_PERIOD = 9
    PAYMENT = 10
    CHOOSE_DISH = 11
    SHOW_DISH = 12
    # INPUT_EMAIL = 13
    # INPUT_WISHLIST = 14
    # INPUT_LETTER = 15
    # CHANGE_GAME_PARAMS = 16
    # CHANGE_GAME_NAME = 17
    # CHOOSE_NEW_COST_RANGE = 18
    # CHOOSE_NEW_TOSS_DATE = 19


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    chat_id = int(update.message.chat_id)
    try:
        user = User.objects.get(tg_chat_id=chat_id)
        update.message.reply_text(
            dedent(
                f'''\
                    Сформируйте подписку
                '''
            ),
            reply_markup=keyboards.create_initial_keyboard()
        )
    except ObjectDoesNotExist:
        update.message.reply_text(
            dedent(
                f'''\
                    Вы не зарегистрированы.
                    \nЗарегистрируйтесь, пожалуйста, следуя инструкциям.
                '''
            ),
            reply_markup=keyboards.create_registration_keyboard()
        )
        return States.REGISTRATION
    return States.CREATE_SUBSCRIPTION


def registrate(update, context):
    update.message.reply_text(
        dedent(f'''\
            Введите ваше имя и фамилию
        '''),
    )
    return States.INPUT_NAME


def handle_input_name(update, context):
    User.objects.create(
        name=update.message.text,
        tg_chat_id=int(update.message.chat_id)
    )
    update.message.reply_text(
        dedent(f'''\
        Введите номер телефона
        '''),
    )
    return States.INPUT_PHONE


def handle_input_phone(update, context):
    user = User.objects.get(tg_chat_id=int(update.message.chat_id))
    user.phone_number = update.message.text
    user.save()
    update.message.reply_text(
        dedent(f'''\
        Сервис для составления меню по вашим запросам
        '''),
        reply_markup=keyboards.create_start_keyboard()
    )
    return States.START


def create_subscription(update, context):
    update.message.reply_text(
        dedent(f'''\
            Выберите тип меню
        '''),
        reply_markup=keyboards.create_menu_type_keyboard()
    )
    return States.MENU_TYPE


def set_menu_type(update, context):
    try:
        Subscription.objects.get(
            user__tg_chat_id=update.message.chat_id,
            is_paid=False
        ).delete()
    except ObjectDoesNotExist as exc:
        print(exc)
    user = User.objects.get(tg_chat_id=update.message.chat_id)
    Subscription.objects.create(
        user=user,
        menu_type=update.message.text
    )
    update.message.reply_text(
        dedent(f'''\
            Введите количество приемов пищи (от 1 до 6)
        ''')
    )
    return States.EATING_COUNT


def set_eating_count(update, context):
    subscription = Subscription.objects.get(
        user__tg_chat_id=update.message.chat_id,
        is_paid=False
    )
    subscription.eating_count = update.message.text
    subscription.save()

    update.message.reply_text(
        dedent(f'''\
            Исключите аллергены из меню или нажмите "Далее"
        '''),
        reply_markup=keyboards.create_allergy_keyboard()
    )
    return States.ALLERGY


def set_allergy(update, context):
    subscription = Subscription.objects.get(
        user__tg_chat_id=update.message.chat_id,
        is_paid=False
    )
    if update.message.text == 'Рыба и морепродукты':
        allergy_type = '1'
    if update.message.text == 'Мясо':
        allergy_type = '2'
    if update.message.text == 'Зерновые':
        allergy_type = '3'
    if update.message.text == 'Продукты пчеловодства':
        allergy_type = '4'
    if update.message.text == 'Орехи и бобовые':
        allergy_type = '5'
    if update.message.text == 'Молочные продукты':
        allergy_type = '6'
    allergy = Allergy.objects.get(type=allergy_type)
    subscription.allergy.add(allergy)

    update.message.reply_text(
        dedent(f'''\
            Исключите аллергены из меню или нажмите "Далее"
        '''),
        reply_markup=keyboards.create_allergy_keyboard()
    )
    return States.ALLERGY


def go_to_period_input(update, context):
    update.message.reply_text(
        dedent(f'''\
            Выберите срок подписки
        '''),
        reply_markup=keyboards.create_subscription_period_keyboard()
    )
    return States.INPUT_PERIOD


def set_expiration_date(update, context):
    subscription = Subscription.objects.get(
        user__tg_chat_id=update.message.chat_id,
        is_paid=False
    )
    if update.message.text == '1 месяц':
        subscription.expiration_date = datetime.now(timezone.utc) \
            + timedelta(30)
    if update.message.text == '3 месяца':
        subscription.expiration_date = datetime.now(timezone.utc) \
            + timedelta(30*3)
    if update.message.text == '6 месяцев':
        subscription.expiration_date = datetime.now(timezone.utc) \
            + timedelta(30*6)
    if update.message.text == '12 месяцев':
        subscription.expiration_date = datetime.now(timezone.utc) \
            + timedelta(30*12)
    subscription.save()
    update.message.reply_text(
        dedent(f'''\
            Оплатите подписку
        '''),
        reply_markup=keyboards.create_payment_keyboard()
    )
    return States.PAYMENT


# FIXME
def do_payment(update, context):
    subscription = Subscription.objects.get(
        user__tg_chat_id=update.message.chat_id,
        is_paid=False
    )
    subscription.is_paid = True
    subscription.create_menu()
    subscription.save()
    update.message.reply_text(
        dedent(
            f'''\
                Оплата произведена
            '''
        )
    )
    return States.START


def show_subscriptions(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(
        dedent(f'''\
            Список ваших подписок:
        '''),
        reply_markup=keyboards.create_subscriptions_keyboard(chat_id)
    )
    return States.CHOOSE_DISH


def choose_dish(update, context):
    subscription_id = update.message.text.split(' ')[3]
    subscription = Subscription.objects.get(id=subscription_id)
    update.message.reply_text(
        dedent(f'''\
            Список блюд на сегодня:
        '''),
        reply_markup=keyboards.create_day_menu_keyboard(subscription_id)
    )
    return States.SHOW_DISH


def show_dish(update, context):
    name = update.message.text
    dish = DishRecipe.objects.get(name=name)
    context.bot.send_photo(update.message.chat_id, str(dish.image))
    ingredients = '\n'.join(dish.ingredients)
    instructions = '\n'.join(dish.instructions)
    update.message.reply_text(
        dedent(f'''\
            \n{name}
            \n{dish.description}
            \nИнгредиенты: \n{ingredients}
            \nРецепт: \n{instructions}
            \nВремя приготовления: {dish.timing}
        ''')
    )
    return States.START


def cancel(update, context):
    update.message.reply_text(
        dedent(f'''\
        Сервис для составления меню по вашим запросам
        '''),
        reply_markup=keyboards.create_start_keyboard()
    )
    return States.START


def main():
    updater = Updater(token=settings.TOKEN)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.START:[
                MessageHandler(
                    Filters.regex('Старт$'),
                    start
                )
            ],
            States.REGISTRATION:[
                MessageHandler(
                    Filters.regex('Регистрация$'),
                    registrate
                )
            ],
            States.INPUT_NAME:[
                MessageHandler(
                    Filters.text & ~Filters.command,
                    handle_input_name
                )
            ],
            States.INPUT_PHONE:[
                MessageHandler(
                    Filters.text & ~Filters.command,
                    handle_input_phone
                )
            ],
            States.CREATE_SUBSCRIPTION:[
                MessageHandler(
                    Filters.regex('Сформировать подписку$'),
                    create_subscription
                ),
                MessageHandler(
                    Filters.regex('Мои подписки$'),
                    show_subscriptions
                )
            ],
            States.MENU_TYPE:[
                MessageHandler(
                    Filters.regex('Классическое$'),
                    set_menu_type
                ),
                MessageHandler(
                    Filters.regex('Вегетарианское$'),
                    set_menu_type
                ),
                MessageHandler(
                    Filters.regex('Низкоуглеводное$'),
                    set_menu_type
                ),
                MessageHandler(
                    Filters.regex('Кето$'),
                    set_menu_type
                )
            ],
            States.EATING_COUNT:[
                MessageHandler(
                    Filters.regex('[1-6]'),
                    set_eating_count
                )
            ],
            States.ALLERGY:[
                MessageHandler(
                    Filters.regex('Рыба и морепродукты$'),
                    set_allergy
                ),
                MessageHandler(
                    Filters.regex('Мясо$'),
                    set_allergy
                ),
                MessageHandler(
                    Filters.regex('Зерновые$'),
                    set_allergy
                ),
                MessageHandler(
                    Filters.regex('Продукты пчеловодства$'),
                    set_allergy
                ),
                MessageHandler(
                    Filters.regex('Орехи и бобовые$'),
                    set_allergy
                ),
                MessageHandler(
                    Filters.regex('Молочные продукты$'),
                    set_allergy
                ),
                MessageHandler(
                    Filters.regex('Далее$'),
                    go_to_period_input
                )
            ],
            States.INPUT_PERIOD:[
                MessageHandler(
                    Filters.regex('1 месяц$'),
                    set_expiration_date
                ),
                MessageHandler(
                    Filters.regex('3 месяца$'),
                    set_expiration_date
                ),
                MessageHandler(
                    Filters.regex('6 месяцев$'),
                    set_expiration_date
                ),
                MessageHandler(
                    Filters.regex('12 месяцев$'),
                    set_expiration_date
                )
            ],
            States.PAYMENT:[
                MessageHandler(
                    Filters.regex('Оплатить$'),
                    do_payment
                )
            ],
            States.CHOOSE_DISH: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    choose_dish
                ),
            ],
            States.SHOW_DISH: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    show_dish
                ),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(Filters.regex('^Отмена$'), cancel)
        ],
    )

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()
