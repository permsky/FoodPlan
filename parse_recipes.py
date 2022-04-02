from bs4 import BeautifulSoup
from time import sleep
import requests
import json


def get_pages_count(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    pages_count = soup.find('div', class_='navigation').find_all('a')[-1].get_text()
    return int(pages_count)


def parse_categories(raw_string: str):
    categories = []
    raw_categories = raw_string.replace('Категории: ', '').split(',')
    for category in raw_categories[:-1]:
        categories.append(category.strip())
    return categories


def parse_ingredients(raw_string: str):
    ingredients = []
    raw_ingredients = raw_string.replace('...', '').split(',')
    for ingredient in raw_ingredients:
        ingredients.append(ingredient.strip())
    return ingredients


def get_recipe_in_html(url: str):
    response = requests.get(url)
    response.raise_for_status()
    markdown = BeautifulSoup(response.text, 'html.parser')
    return markdown


def fetch_url_recipes(diet_type: dict) -> dict:
    recipes_url = []
    for diet, base_url in diet_type.items():
        page = 1
        pages_count = get_pages_count(base_url)
        if pages_count > 8:
            pages_count = 8
        while page <= pages_count:
            url = f'{base_url}page/{page}/'
            markdown = get_recipe_in_html(url)
            recipes_blok = markdown.find_all('div', class_= 'shortstory')
            for blok in recipes_blok:
                recipe_views = blok.find('div', class_='recepiesimg').get_text()
                if recipe_views:
                    raw_ingredients = blok.find('span', class_='shortingr').get_text()
                    raw_categories = blok.find('div', class_='short_category').get_text()
                    recipe_info = {
                        'name': blok.find('h3').get_text(),
                        'url': blok.a.get('href'),
                        'ingredients': parse_ingredients(raw_ingredients),
                        'diet': diet,
                        'categories': parse_categories(raw_categories),
                    }
                    if '(кетодиета)' in recipe_info['name']:
                        recipe_info['diet'] = 'keto'
                    recipes_url.append(recipe_info)
            page += 1
    return recipes_url


def parse_recipes(diet_type: dict):
    recipes = fetch_url_recipes(diet_type)
    for index, recipe in enumerate(recipes):
        if index % 150 == 0:
            sleep(360)
        markdown = get_recipe_in_html(recipe['url'])
        recipes[index]['recipe_image'] = markdown.find('div', class_='centr').img.get('src')
        recipes[index]['recipe_description'] = markdown.find('p', { 'itemprop': 'description'}).get_text()
        recipes[index]['recipe_instructions'] = [text.get_text() for text in markdown.find_all('li', {'itemprop': 'recipeInstructions'})]
        recipes[index]['recipe_ingredients'] = [text.get_text() for text in markdown.find_all('li', {'itemprop': 'recipeIngredient'})]
        recipes[index]['time_to_prepare'] = markdown.find('span', class_='duration').get_text()

    with open('recipe.json', 'w', encoding='utf-8') as file:
        json.dump(recipes, file, ensure_ascii=False)


def main():
    diet_type = {
        'classic': 'https://grandkulinar.ru/recepies/osnovnye-blyuda/',
        'low_carb': 'https://grandkulinar.ru/recepies/zdorovoe-pitanie/nizkouglevodnye-blyuda/',
        'vegetarian': 'https://grandkulinar.ru/recepies/zdorovoe-pitanie/vegetarianskie-blyuda/',
    }
    try:
        parse_recipes(diet_type)
    except requests.exceptions.HTTPError:
        print('Произошла ошибка')


if __name__ == '__main__':
    main()
