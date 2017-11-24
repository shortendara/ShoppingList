class Recipe(object):
    name =""
    ingredients =[]
    url = ""

    def __init__(self, name, ingredients, url):
        self.name = name
        self.ingredients = ingredients
        self.url = url