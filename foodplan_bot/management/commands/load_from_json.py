import json
from django.core.management.base import BaseCommand

from foodplan_bot.models import DishRecipe, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        recipes_filepath = 'recipe.json'

        def read_from_json(filepath):
            with open(filepath, encoding='UTF-8', mode='r') as f:
                return json.loads(f.read())

        def update_recipes(filepath):
            dish_recipes = read_from_json(filepath)
            for dish in dish_recipes:
                if dish['diet'] == 'vegetarian':
                    menu_type = 'Вегетарианское'
                if dish['diet'] == 'low_carb':
                    menu_type = 'Низкоуглеводное'
                dish_recipe = DishRecipe.objects.get_or_create(
                    name = dish['name'],
                    defaults={
                        'name': dish['name'],
                        'image': dish['recipe_image'],
                        'ingredients': dish['recipe_ingredients'],
                        'instructions': dish['recipe_instructions'],
                        'description': dish['recipe_description'],
                        'timing': dish['time_to_prepare'],
                        # 'categories': dish['categories'],
                        'menu_type': menu_type
                    }
                )
                dish_recipe[0].name = dish['name']
                dish_recipe[0].image = dish['recipe_image']
                dish_recipe[0].ingredients = dish['recipe_ingredients']
                dish_recipe[0].instructions = dish['recipe_instructions']
                dish_recipe[0].description = dish['recipe_description']
                dish_recipe[0].timing = dish['time_to_prepare']
                dish_recipe[0].menu_type = menu_type
                dish_recipe[0].save()

                for category in dish['categories']:
                    dish_category = Category.objects.get_or_create(
                        name = category,
                        defaults={'name': category}
                    )
                    dish_recipe[0].categories.add(dish_category[0])

        update_recipes(recipes_filepath)
