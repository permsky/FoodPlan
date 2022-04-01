from datetime import datetime, timedelta, timezone
from django.db import models
import math
import random


class User(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Имя и фамилия пользователя'
    )
    tg_chat_id = models.PositiveIntegerField(
        verbose_name='Чат id пользователя в Telegram',
        unique=True
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона пользователя',
        max_length=12,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('1', 'Блюда из картофеля'),
        ('2', 'Овощи и грибы'),
        ('3', 'Рыба и морепродукты'),
        ('4', 'Мясо'),
        ('5', 'Крупы, бобовые'),
        ('6', 'Яйца и молочные продукты'),
    ]

    name = models.CharField(
        verbose_name='Категория блюда',
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория блюд'
        verbose_name_plural = 'Категории блюд'


class Allergy(models.Model):
    ALLERGY_CHOICES = [
        ('1', 'Рыба и морепродукты'),
        ('2', 'Мясо'),
        ('3', 'Зерновые'),
        ('4', 'Продукты пчеловодства'),
        ('5', 'Орехи и бобовые'),
        ('6', 'Молочные продукты'),
    ]

    type = models.CharField(
        verbose_name='Аллерген',
        max_length=21,
        choices=ALLERGY_CHOICES,
        unique=True
    )
    categories = models.ManyToManyField(
        Category,
        related_name='categories_for_allergy',
        verbose_name='Категории',
        blank=True
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Аллергия'
        verbose_name_plural = 'Аллергии'


class Subscription(models.Model):
    TYPE_CHOICES = [
        ('Классическое', 'Классическое'),
        ('Низкоуглеводное', 'Низкоуглеводное'),
        ('Вегетарианское', 'Вегетарианское'),
        ('Кето', 'Кето'),
    ]

    PERSON_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False
    )
    menu_type = models.CharField(
        verbose_name='Тип меню',
        max_length=15,
        choices=TYPE_CHOICES
    )
    menu = models.JSONField(
        verbose_name='Меню по подписке',
        default=dict,
        blank=True
    )
    person_count = models.PositiveSmallIntegerField(
        verbose_name='Количество персон',
        choices=PERSON_CHOICES
    )
    eating_count = models.PositiveSmallIntegerField(
        verbose_name='Количество приемов пищи',
        choices=PERSON_CHOICES
    )
    allergy = models.ManyToManyField(
        Allergy,
        related_name='allergy',
        verbose_name='Аллергии',
        blank=True
    )
    expiration_date = models.DateTimeField(
        verbose_name='Срок действия подписки'
    )

    def __str__(self):
        return (
            f'Подписка пользователя {self.user} на {self.menu_type.lower()} '
            f'меню до {self.expiration_date}'
        )

    def create_menu(self):
        dishes = DishRecipe.objects.filter(menu_type=self.menu_type)
        if self.allergy.all():
            for allergy in self.allergy.all():
                for category in allergy.categories.all():
                    dishes = dishes.exclude(categories=category)
        menu = dict()
        dates = list()
        dish_ids = list()
        start_date = datetime.now(timezone.utc)
        for days in range(int((self.expiration_date - start_date).days) + 2):
            dates.append(start_date + timedelta(days))
        for dish in dishes:
            dish_ids.append(dish.id)
        menu_dishes = list()
        for index in range(
            math.ceil(len(dates)*self.eating_count/len(dish_ids))
        ):
            random.shuffle(dish_ids)
            dishes_temp = dish_ids.copy()
            random.shuffle(dishes_temp)
            menu_dishes.extend(dishes_temp)
        for day in dates:
            menu[day.strftime("%d-%m-%Y")] = dict()
            for eating_number in range(self.eating_count):
                menu[day.strftime("%d-%m-%Y")][eating_number + 1] = \
                    menu_dishes.pop()
        self.menu = menu
        self.save()

    class Meta:
        ordering = ['-expiration_date']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class DishRecipe(models.Model):
    TYPE_CHOICES = [
        ('Классическое', 'Классическое'),
        ('Низкоуглеводное', 'Низкоуглеводное'),
        ('Вегетарианское', 'Вегетарианское'),
        ('Кето', 'Кето'),
    ]

    name = models.CharField(
        verbose_name='Название блюда',
        max_length=256
    )
    image = models.ImageField(
        upload_to='dishes',
        verbose_name='Фото блюда',
        blank=True
    )
    ingredients = models.JSONField(verbose_name='Ингридиенты')
    description = models.TextField(verbose_name='Описание блюда')
    calorific_value = models.PositiveIntegerField(
        verbose_name='Калорийность'
    )
    recipe = models.TextField(verbose_name='Рецепт')
    categories = models.ManyToManyField(
        Category,
        related_name='categories_for_dishes',
        verbose_name='Категории',
        blank=True
    )
    menu_type = models.CharField(
        verbose_name='Тип меню',
        max_length=15,
        choices=TYPE_CHOICES,
        default='Классическое'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
