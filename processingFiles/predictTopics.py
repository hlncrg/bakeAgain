import pandas
import pandasql
import nltk
import numpy as np
from nltk.corpus import wordnet as wn

filename="importantWords/importantWords.csv"#important words
impWords=pandas.read_csv(filename,encoding='ISO-8859-1')#load the file
filename="exceptionWords.csv"#important words
exceptions=pandas.read_csv(filename,encoding='ISO-8859-1')['words'].values#load the file

f_out = open('importantWords/importantWordsRanked.csv','w')
f_out.write('recipeId,words,rank,posEx,negEx\n')

maxCount=max([list(impWords['foodword'].values).count(word) for word in impWords['foodword']])
for recipeId,word,posEx,negEx in zip(impWords['recipeId'],impWords['foodword'],impWords['posEx'],impWords['negEx']):
    if float(list(impWords['foodword'].values).count(word))/float(maxCount)<.3 and word not in exceptions:
        f_out.write(str(recipeId)+',"'+word+'",'+str(float(list(impWords['foodword'].values).count(word))/float(maxCount))+',"'+posEx+'","'+negEx+'"\n')
f_out.close()
