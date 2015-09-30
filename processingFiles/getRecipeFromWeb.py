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
filename="../filenames.csv"#the recipe id stored in this file
recipeIds=pandas.read_csv(filename,encoding='ISO-8859-1')['filenames'].values#load the file

f_out2 = open('../data/titles.csv','w')
f_out2.write('recipeId,title\n')#save to file

for recipeId in recipeIds:
    url='http://allrecipes.com/recipe/'+str(recipeId)+'/'
    print url#create the url
    r = requests.get(url)#get html
    ingredients=find_betweenMulti( r.content, 'itemprop="ingredients">', '</span>')
    f_out = open('../data/ingredients/ingredients'+str(recipeId)+'.csv','w')
    f_out.write('ingredients\n')#save to file
    for ingredient in ingredients:
        f_out.write('"'+ingredient+'"\n')
    f_out.close()

    title=find_betweenMulti(r.content,'<h1 class="recipe-summary__h1" itemprop="name">','</h1>')
    f_out2.write(str(recipeId)+',"'+title[0]+'"\n')

f_out2.close()
