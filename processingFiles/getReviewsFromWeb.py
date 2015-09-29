import requests
from bs4 import BeautifulSoup
import pandas
import pandasql
import urllib2
import HTMLParser
import re

#find the string between two other strings, once
def find_between( s, first, last ):
    stringBetween=[]
    end=0
    try:
        start = s.index( first,end ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
            return stringBetween

#find the string between two other strings, all
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


recipeIds=["13477"]
recipeNames=["double-layer-pumpkin-cheesecake"]


for recipeId,recipeName in zip(recipeIds,recipeNames):
    f_out = open('reviews/reviews'+recipeId+'.csv','w')#open a file to save reviews in
    f_out.write('helpfulCounts,ratings,reviewText\n')#header of the file
    reviewIds=[]#store review ids
    for pagenumber in xrange(1,20):#go through a resonable range ~20
        url='http://allrecipes.com/recipe/getreviews/?recipeid='+recipeId+'&pagenumber='+str(pagenumber)+'&pagesize=2000&recipeType=Recipe'
        print url
        r = requests.get(url)#get the page html
        reviewIds=find_betweenMulti( r.content, '<a class="review-detail__link" href="reviews/', '/">')
        for reviewId in reviewIds:#get the ids and look up the individual pages
            url="http://allrecipes.com/recipe/"+recipeId+"/"+recipeName+"/reviews/"+str(reviewId)
            print url
            r = requests.get(url)
            try:#the comments have ascii and other messy stuff that we need to deal with
                reviewText=re.sub(' +',' ',
                    HTMLParser.HTMLParser().unescape(
                        urllib2.unquote(
                            find_between( r.content, '<p itemprop="reviewBody">', '</p>')
                        ).decode('utf8','mixed')
                    ) 
                ).replace('\n', ' ').replace('\r', '').lstrip().rstrip().encode('utf-8')
            except LookupError:
                reviewText=re.sub(' +',' ',
                    HTMLParser.HTMLParser().unescape(
                        urllib2.unquote(
                            find_between( r.content, '<p itemprop="reviewBody">', '</p>')
                        ).decode('latin-1')
                    ) 
                ).replace('\n', ' ').replace('\r', '').lstrip().rstrip().encode('utf-8')
                
            ratingStars=HTMLParser.HTMLParser().unescape(find_between( r.content, 'data-ratingstars=','>')).lstrip().rstrip()
            helpfulCount=HTMLParser.HTMLParser().unescape(find_between( r.content, '<div class="button helpful-count" itemprop="interactionCount"><format-large-number number="','"></format-large-number></div>' ))
            # get the star rating and helpful rating
            f_out.write('"'+str(helpfulCount)+'","'+str(ratingStars)+'","'+reviewText.replace('"',"'")+'"\n')
    f_out.close()
    
