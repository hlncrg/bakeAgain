import requests
from bs4 import BeautifulSoup
import pandas
import pandasql
import urllib2
import HTMLParser
import re

#find string between two other strings
def find_betweenMulti( s, first, last ):
    stringBetween=[]
    end=0
    while (1):
        try:
            start = s.index( first,end ) + len( first )
            end = s.index( last, start )
            stringBetween.append(s[start:end])
        except ValueError:
            return stringBetween

#get these recipes
recipeIds=["17165","10497"]
recipeNames=["big-soft-ginger-cookies","beths-spicy-oatmeal-raisin-cookies"]


for recipeId,recipeName in zip(recipeIds,recipeNames):
    url='http://allrecipes.com/recipe/'+recipeId+'/'+recipeName+'/'
    print url#create the url
    r = requests.get(url)#get html
    ingredients=find_betweenMulti( r.content, 'itemprop="ingredients">', '</span>')
    f_out = open('ingredients/ingredients'+recipeId+'.csv','w')
    f_out.write('ingredients\n')#save to file
    for ingredient in ingredients:
        f_out.write('"'+ingredient+'"\n')
    f_out.close()
