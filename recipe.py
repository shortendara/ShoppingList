class Recipe(object):
    ingredients =[]
    method = []

    def __init__(self, ingredients, method):
        self.ingredients = ingredients
        self.method = method