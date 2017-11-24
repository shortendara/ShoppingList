#Import libraries
from bs4 import BeautifulSoup
from bs4 import element
import urllib
import re
import recipe

#Function to retieve recipe
def get_recipe(url):
    #Variabales
    ingredients = []
    cooking_method =[]

    #Open URL using urllib
    url = "https://www.bbc.co.uk/"+url
    recipe_page = urllib.urlopen(url)

    #Use BeautifulSoup to get html text
    soup = BeautifulSoup(recipe_page, 'lxml')

    #Retrieve each list of recipe ingredients
    for ingredient in soup.find_all('ul', {'class': 'recipe-ingredients__list'}):
        ingredients.append(ingredient.text)

    #Retrieve method for cooking the dish
    for method in soup.find_all('p', {'class': 'recipe-method__list-item-text'}):
        cooking_method.append(method.text)

    save_recipe(ingredients, cooking_method)

#Function to save recipe to database
def save_recipe(ingredients, cooking_method):
    save = recipe.Recipe(ingredients, cooking_method)

#Function to retrieve recipes at declared time
def get_daily_picks():
    #Open BBC Food index page
    url = "https://www.bbc.co.uk/food"
    index_page = urllib.urlopen(url)

    #Store recipes in list
    daily_picks = []

    #Use BeautifulSoup to parse page
    soup = BeautifulSoup(index_page, "lxml")
    for links in soup.find_all('dd', {'class': 'picks-list'}):
        for link in links.find_all('a', href=True):
            if link.get_text(strip = True):
                
                daily_picks.append(link['href'])

get_daily_picks()