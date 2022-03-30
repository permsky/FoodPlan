from django.db import models


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


class Subscription(models.Model):
    TYPE_CHOICES = [
        ('Классическое', 'Классическое'),
        ('Низкоуглеводное', 'Низкоуглеводное'),
        ('Вегетарианское', 'Вегетарианское'),
        ('Кето', 'Кето'),
    ]
    ALLERGY_CHOICES = [
        ('1', 'Рыба и морепродукты'),
        ('2', 'Мясо'),
        ('3', 'Зерновые'),
        ('4', 'Продукты пчеловодства'),
        ('5', 'Орехи и бобовые'),
        ('6', 'Молочные продукты'),
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
    person_count = models.PositiveSmallIntegerField(
        verbose_name='Количество персон',
        choices=PERSON_CHOICES
    )
    eating_count = models.PositiveSmallIntegerField(
        verbose_name='Количество приемов пищи',
        choices=PERSON_CHOICES
    )
    allergy = models.CharField(
        verbose_name='Аллергия',
        max_length=21,
        choices=ALLERGY_CHOICES,
        blank=True
    )
    expiration_date = models.DateTimeField(
        verbose_name='Срок действия подписки'
    )

    def __str__(self):
        return (
            f'Подписка пользователя {self.user} на {self.menu_type.lower()} меню'
            f' до {self.expiration_date}'
        )
    
    class Meta:
        ordering = ['-expiration_date']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class DishRecipe(models.Model):
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
    subscriptions = models.ManyToManyField(
        Subscription,
        related_name='subscriptions',
        verbose_name='Подписки',
        blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
