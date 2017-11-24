#Import libraries
from bs4 import BeautifulSoup
from bs4 import element
import urllib
import re
from recipe import Recipe
import smtplib
import unicodedata
from details import Details

#Function to retieve recipe
def get_recipe(recipe_url):
    #Variabales
    name =""
    ingredients = []
    cooking_method =[]

    #Open URL using urllib
    url = "https://www.bbc.co.uk"+recipe_url
    print url

    recipe_page = urllib.urlopen(url)

    #Use BeautifulSoup to get html text
    soup = BeautifulSoup(recipe_page, 'lxml')

    #Retrieve recipe name
    name = soup.find("h1", {'class': 'content-title__text'}).text.encode('utf-8')
    print name
    #Retrieve each list of recipe ingredients
    for ingredient in soup.find_all('ul', {'class': 'recipe-ingredients__list'}):
        #Convert text from unicode to python str
        ingredients.append(ingredient.text.encode('utf-8'))

    #Retrieve method for cooking the dish
    for method in soup.find_all('p', {'class': 'recipe-method__list-item-text'}):
        #Convert text from unicode to python str
        cooking_method.append(method.text.encode('utf-8'))

    recipe_item = Recipe(name, ingredients, url)
    return recipe_item

#Function to send recipe to email address
def email_recipes(recipe_list):
    email_address = Details.email
    password = Details.password
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, password)

    #Create message including ingredients and cooking method
    msg = ""
    #Loop through each recipe in list and append to msg
    for recipe in recipe_list:
        msg += recipe.name+'\n'
        msg += recipe.url+'\n'
        for ingredient in recipe.ingredients:
            msg += ingredient
    
    server.sendmail(email_address, email_address, msg)
    server.quit()

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
                #TODO Verify url is /food/recipes
                if link['href'][:13] == "/food/recipes":
                    daily_picks.append(link['href'])
    
    return daily_picks

def main():
    recipe_list = []
    picks = get_daily_picks()
    for pick in picks:
        recipe_list.append(get_recipe(pick))
    
    email_recipes(recipe_list)
    print "Done"
main()
