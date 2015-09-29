import string
import pandas
import pandasql
from nltk import pos_tag 
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize
import re
from collections import Counter


def findnoun(sentence):#custom function for finding food related nouns
    foundword=[]
    foundOne=0
    for word2 in sentence:#loop through the sentence
        if (word2[1]=='NN' or word2[1]=='NNS' or word2[1]=='JJ' or (#find a word that is an adjective or noun
            'noun.food' in [b.lexname() for b in wn.synsets(word2[0])] and word2[0] not in measurementwords['measurementwords'].values)) and (
            word2[0] not in exceptionWords):#or if it is food-related but not a measurement or non-ingredient
                        foundOne=1#success
                        foundword.append(word2)
        elif foundOne==1:#as soon as there is no more in a row
                        break;#exit the loop
    return foundword



def customPOS(sentence):#part of speech tagger
    text = word_tokenize(sentence.lower())#lower everything
    sentenceNew = list(pos_tag(text))#use nltk to tagg
    sentenceNew = [[p[0], p[1]] for p in sentenceNew]#reformat into easier form
    for indexword,word in enumerate(sentenceNew):#tag words a measurements (cup, tsp, ...)
        if word[0] in measurementwords['measurementwords'].values:
            sentenceNew[indexword][1]='measure'
    return sentenceNew

def getKeyWords(reviewTextSentences):
#here we find food words, action words, and example sentences
        foodwords=[]
        actions=[]
        foodActionSentences=[]
        for reviewTextSentence in reviewTextSentences:#loop through the sentences
            sentence=customPOS(reviewTextSentence)#tag each sentence with part of speech
            for indexword,word in enumerate(sentence):#go through each word in the sentence
                wordletters=word[0]#the actual word
                wordpos=word[1]# the part of speech
                if wordletters in keywordsDict.keys():#if we find a keyword (increase, decrease, add,...)
                        foundwords=findnoun(sentence[indexword+1:])#find the noun after the action word
                        if ' '.join([foundword[0] for foundword in foundwords]) not in exceptionWholeWords:
                            for foundword in foundwords:#if this at least one of the words in the noun phrase is food related
                                if 'noun.food' in [b.lexname() for b in wn.synsets(foundword[0])]:
                                    foodwords.append([i[0] for i in foundwords])#save the word and 
                                    actions.append(keywordsDict[wordletters])#associated action
                                    foodActionSentences.append(reviewTextSentence)
                                    break;
                if indexword+1<len(sentence):#look at two word keywords
                    if " ".join([wordletters,sentence[indexword+1][0]]) in keywordsDict.keys():
                        foundwords=findnoun(sentence[indexword+2:])#check for problem words
                        if ' '.join([foundword[0] for foundword in foundwords]) not in exceptionWholeWords:
                            for foundword in foundwords:#if this at least one of the words in the noun phrase is food related
                                if 'noun.food' in [b.lexname() for b in wn.synsets(foundword[0])]:
                                    foodwords.append([i[0] for i in foundwords])#save the word and 
                                    actions.append(keywordsDict[" ".join([wordletters,sentence[indexword+1][0]])])
                                    foodActionSentences.append(reviewTextSentence)#associated action
                                    break;
        return foodwords,actions,foodActionSentences


filename="filenames.csv"#the recipe id stored in this file
filenames=pandas.read_csv(filename,encoding='ISO-8859-1')['filenames'].values#load the file
filename="exceptionWords.csv"#exception words that are food-related but not ingredients
exceptionWords=pandas.read_csv(filename,encoding='ISO-8859-1')['exceptionWords'].values#load the file
filename="exceptionWholeWords.csv"
exceptionWholeWords=pandas.read_csv(filename,encoding='ISO-8859-1')['exceptionWholeWords'].values#load the file


filename="measurement.csv"#the common measurement words
measurementwords=pandas.read_csv(filename,encoding='ISO-8859-1')#load the file
filename="keywordsStartSingle.csv"#the action words
keywordsStart=pandas.read_csv(filename,encoding='ISO-8859-1')#load the file
keywordsDict=keywordsStart.set_index('keywords')['catagory'].to_dict()

uniqueActions=['mod','inc_add','inc','dec','sub']
#the catagories of action words
for recipeId in filenames:#loop through each recipe
    filename="reviews/reviews"+str(recipeId)+".csv"#file to store to
    reviewText=pandas.read_csv(filename,encoding='ISO-8859-1')#load the file
    
    reviewTextSentences = sent_tokenize(' '.join(reviewText['reviewText']).replace('c.','cup').replace('tspn.','teaspoon').replace(
                'tbsp.','tablespoon').replace('tbs.','tablespoon').replace('tsp.','teaspoon').replace('tbl.','tablespoon').replace(
                ' T.',' tablespoon').replace(' t.',' teaspoon'))#reformate some commonly used abbriviations
    foodwords,actions,foodActionSentences=getKeyWords(reviewTextSentences)#find the action and food words
    counts = Counter()
    #########################
    numTot=0
    for foodword in foodwords:
        counts.update([' '.join(foodword)])
    for foodwordUnique in counts.most_common(70):
        for uniqueAction in uniqueActions:
            num=len([[' '.join(foodword),action] for foodword,action in zip(foodwords,actions) if foodwordUnique[0]==' '.join(foodword) and action==uniqueAction])
            numTot=numTot+num#total number of ingredients considered
    #########################
    f_out = open('foodwords/foodwords'+str(recipeId)+'.csv','w')
    f_out.write('foodword,modWord,modWordEx,inc_addWord,inc_addWordEx,incWord,incWordEx,decWord,decWordEx,subWord,subWordEx,numTot\n')
    for foodwordUnique in counts.most_common(70):
        numActions=''#a string to store what will be saved to file
        numTotfoodUnique=0#the total number of a give ingredient
        for uniqueAction in uniqueActions:#loop through the unique actions
                    num=len([[' '.join(foodword),action] for foodword,action in zip(foodwords,actions) if foodwordUnique[0]==' '.join(foodword) and action==uniqueAction])
                    numTotfoodUnique=numTotfoodUnique+num#to find the total number of a give ingredient
        if float(numTotfoodUnique)/float(numTot)>.0:#if the food existed in the 'most common'
            for uniqueAction in uniqueActions:#now look at each unique action -->'mod','inc_add','inc','dec','sub'
                num=len([[' '.join(foodword),action] for foodword,action in zip(foodwords,actions) if foodwordUnique[0]==' '.join(foodword) and action==uniqueAction])
                numActions=numActions+str(round(float(num)/float(numTotfoodUnique),3))+','#the fraction of times a given unique action is used
                addSentence=''#an example sentence
                for sentence2,action2,foodword2 in zip(foodActionSentences,actions,foodwords):
                    if ' '.join(foodword2)==foodwordUnique[0] and uniqueAction==action2 and len(sentence2.split(' '))<20:
                        addSentence=filter(lambda x: x in string.printable, sentence2)
                        break;#grab the first sentence that is under 20 words long
                if addSentence=='':
                    addSentence=' '#sometimes there is no sentence un 20 words long
                numActions=numActions+'"'+addSentence+'",'#add the sentence to the end
            f_out.write('"'+foodwordUnique[0]+'",'+numActions[:-1]+","+str(numTotfoodUnique)+'\n')
    f_out.close()#close the file
    
