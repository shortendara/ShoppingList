#Import libraries
from bs4 import BeautifulSoup
from bs4 import element
import urllib
import re
import recipe
import smtplib
import unicodedata
from details import password, email_address

#Function to retieve recipe
def get_recipe(recipe_url):
    #Variabales
    ingredients = []
    cooking_method =[]

    #Open URL using urllib
    url = "https://www.bbc.co.uk/"+recipe_url
    print url

    recipe_page = urllib.urlopen(url)

    #Use BeautifulSoup to get html text
    soup = BeautifulSoup(recipe_page, 'lxml')

    #Retrieve each list of recipe ingredients
    for ingredient in soup.find_all('ul', {'class': 'recipe-ingredients__list'}):
        #Convert text from unicode to python str
        ingredients.append(ingredient.text.encode('utf-8'))

    #Retrieve method for cooking the dish
    for method in soup.find_all('p', {'class': 'recipe-method__list-item-text'}):
        #Convert text from unicode to python str
        cooking_method.append(method.text.encode('utf-8'))

    save_recipe(ingredients, cooking_method)

#Function to send recipe to email address
def save_recipe(ingredients, cooking_method):
    email_address = "dara.shorten@gmail.com"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, 'poiuytr987')

    #Create message including ingredients and cooking method
    msg = ""
    for ingredient in ingredients:
        msg += ingredient
    for method in cooking_method:
        msg += method+"\n"
    
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
                daily_picks.append(link['href'])
    
#get_daily_picks()
get_recipe("food/recipes/herbycouscouswithbut_92552")