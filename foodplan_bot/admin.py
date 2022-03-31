from django.contrib import admin

from .models import User, Subscription, DishRecipe, Allergy


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tg_chat_id', 'phone_number')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'menu_type',
        'person_count',
        'eating_count',
        'expiration_date',
    )


@admin.register(DishRecipe)
class DishRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image',
        'name',
        'ingredients',
        'description',
        'calorific_value',
        'recipe',
    )


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
