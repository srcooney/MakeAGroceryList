

import webapp2

from bs4 import BeautifulSoup
from bs4 import NavigableString
import urllib2
import os
import jinja2
import json
from google.appengine.ext import ndb

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
#         url = "http://www.cookingclassy.com/2013/05/churro-bites/"
class LoginPage(webapp2.RequestHandler):         
    def get(self):
        user = users.get_current_user()

        if user:
            self.redirect("/")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class MakeAGroceryList(webapp2.RequestHandler):         
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/LoginPage")
            return
        url = self.request.get('url')
        ingredientsList = []
        if url != "":
#           fixed forbidden error  http://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

            req = urllib2.Request(url, headers=hdr)

            r = urllib2.urlopen(req)
            data = r.read()
            
            soup = BeautifulSoup(data)
            ingredients = soup.findAll('li', {'class': "ingredient"})
            for ingredient in ingredients:
                if isinstance(ingredient.next_element, NavigableString):
                    text = ingredient.text
                    if not text.isspace():
                        ingredientsList.append(text)
                        
        template_values = {
            'url': url,
            'ingredientsList': ingredientsList,
        }

        template = JINJA_ENVIRONMENT.get_template('grocery_list_webpage.html')
        self.response.write(template.render(template_values))
        
class GetIngredients(webapp2.RequestHandler):         
    def get(self):
        url = self.request.get('url')
#         url = "http://www.cookingclassy.com/2013/05/churro-bites/"
        ingredientsList = []
        if url != "":
#           fixed forbidden error  http://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

            req = urllib2.Request(url, headers=hdr)

            r = urllib2.urlopen(req)
            data = r.read()
            
            soup = BeautifulSoup(data)
            ingredients = soup.findAll('li', {'class': "ingredient"})
            for ingredient in ingredients:
                if isinstance(ingredient.next_element, NavigableString):
                    text = ingredient.text
                    if not text.isspace():
                        ingredientsList.append(text)
                        
            jsonObj = json.dumps({"ingredientsList":ingredientsList})  
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.out.write(jsonObj)
            
ALL_RECIPES_NAME = 'all_recipes'
def recipe_key(recipeName=ALL_RECIPES_NAME):
    return ndb.Key('Recipe', recipeName)

class Recipe(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    owner = ndb.StringProperty()
    title = ndb.StringProperty()
    ingredients = ndb.StringProperty(repeated=True)

            
class SaveRecipe(webapp2.RequestHandler):         
    def get(self):
        ingredientsJson = self.request.get('ingredients')
        ingredients= json.loads(ingredientsJson)
        recipeTitle = self.request.get('recipeTitle')
        
        recipe = Recipe(parent=recipe_key(ALL_RECIPES_NAME))
        recipe.owner = users.get_current_user().email()
        recipe.title = recipeTitle
        print "-------------------------- ingredients type=" + ingredients[0]
        
        for ingredient in ingredients:
            recipe.ingredients.append(ingredient)
        recipe.put()
        
        
        
        
def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return obj
#     elif isinstance(obj, ...):
#         return ...
#     else:
#         raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))        
        
class GetSavedRecipes(webapp2.RequestHandler):         
    def get(self):        
        recipes_query = Recipe.query(ancestor=recipe_key(ALL_RECIPES_NAME)).order(-Recipe.date)
        recipes = recipes_query.fetch(1000)
        recipeList = []
        for recipe in recipes:
            if recipe.owner == users.get_current_user().email():
                recipeList.append(recipe.to_dict())
        
        jsonObj = json.dumps({"recipeList":recipeList}, default=handler)  
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(jsonObj)
    

application = webapp2.WSGIApplication([
    ('/', MakeAGroceryList),
    ('/LoginPage', LoginPage),
    ('/GetSavedRecipes', GetSavedRecipes),
    ('/SaveRecipe', SaveRecipe),
    ('/GetIngredients', GetIngredients),
    
], debug=True)