import pandas
import pandasql
from sklearn.naive_bayes import GaussianNB
import numpy

recipeIds=["10141","10813","15004","24445","25037"]#the pretagged files
filename="filenames.csv"#the recipe id stored in this file
recipeId2s=pandas.read_csv(filename,encoding='ISO-8859-1')['filenames'].values#load the file
#the files to be tagged

wordToNum={'dec':0,'add':1,'inc':2,'mix':3}
#the meaning catagories
data=[]
target=[]
for recipeId in recipeIds:
    filename='taggedFiles/taggedFiles'+str(recipeId)+".csv"#this is our keywords
    impWords=pandas.read_csv(filename,encoding='ISO-8859-1')#load the file
    for label,modWord,inc_addWord,incWord,decWord,subWord,numTot in zip(impWords['label'],impWords['modWord'],impWords['inc_addWord'],impWords['incWord'],impWords['decWord'],impWords['subWord'],impWords['numTot']):
        data.append([modWord,inc_addWord,incWord,decWord,subWord,numTot])#set up the pretagged data
        target.append(wordToNum[label])#and associated target labels

feature_names=['modWord','inc_addWord','incWord','decWord','subWord','numTot']
#name of the feature space
target_names=wordToNum.keys()

clf = GaussianNB().fit(numpy.array(data),numpy.array(target)) #use the naive bayes model

for recipeId2 in recipeId2s:#loop through each recipe

    filename='foodwords/foodwords'+str(recipeId2)+".csv"#load processed ingredient files
    impWords=pandas.read_csv(filename,encoding='ISO-8859-1')#load the file
    testCase=[]
    foodwords=[]
    for food,modWord,inc_addWord,incWord,decWord,subWord,numTot in zip(impWords['foodword'],impWords['modWord'],impWords['inc_addWord'],impWords['incWord'],impWords['decWord'],impWords['subWord'],impWords['numTot']):
        testCase.append([modWord,inc_addWord,incWord,decWord,subWord,numTot])
        foodwords.append(food)#getting data from file and putting it in the correct format
    predictions = clf.predict_proba(numpy.array(testCase))#returns the probability of each label
    print recipeId2#save the output
    f_out = open('predictions/predictions'+str(recipeId2)+'.csv','w')
    f_out.write('foodword,decWord,addWord,incWord,mixWord,numTot\n')

    for foodword,prediction,numTot in zip(foodwords,predictions,impWords['numTot']):
        f_out.write('"'+foodword+'",'+str(prediction[0])+','+str(prediction[1])+','+str(prediction[2])+','+str(prediction[3])+','+str(numTot)+'\n')
    f_out.close()
