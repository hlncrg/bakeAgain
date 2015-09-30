import pymysql as mdb
import pandas
import pandasql
import string
con = mdb.connect('localhost', 'root', '', 'recipesDB') #host, user, password, #database

filename="../data/titles.csv"#the recipe id stored in this file
recipeIds=pandas.read_csv(filename,encoding='ISO-8859-1')['recipeId'].values#load the file
titles=pandas.read_csv(filename,encoding='ISO-8859-1')['title'].values#load the file



with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Recipes")
    cur.execute("CREATE TABLE Recipes(Id INT PRIMARY KEY AUTO_INCREMENT,recipeid int,recipeName varchar(255))")
    for recipeId,title in zip(recipeIds,titles):
        cur.execute('INSERT INTO Recipes(recipeId,recipeName) VALUES('+str(recipeId)+',"'+title+'")')

    filename="../data/importantWords/importantWordsRanked.csv"#this is our keywords
    words=pandas.read_csv(filename,encoding='ISO-8859-1')['words'].values#load the file
    negEx=pandas.read_csv(filename,encoding='ISO-8859-1')['negEx'].values#load the file
    posEx=pandas.read_csv(filename,encoding='ISO-8859-1')['posEx'].values#load the file
    recipeIds=pandas.read_csv(filename,encoding='ISO-8859-1')['recipeId'].values
    cur.execute("DROP TABLE IF EXISTS ImpWords")
    cur.execute("CREATE TABLE ImpWords(Id INT PRIMARY KEY AUTO_INCREMENT, recipeId int, words varchar(255), negEx varchar(2000),posEx varchar(2000))")
    for recipeId,word,nEx,pEx in zip(recipeIds,words,negEx,posEx):
        cur.execute('INSERT INTO ImpWords(recipeId,words,negEx,posEx) VALUES('+str(recipeId)+',"'+word+'","'+str(nEx)+'","'+str(pEx)+'")')


    for recipeId in recipeIds:
        recipeId=str(recipeId)

        cur.execute("DROP TABLE IF EXISTS ImpWords"+recipeId)

        filename="../data/ingredients/ingredients"+str(recipeId)+".csv"
        ingredients=pandas.read_csv(filename,encoding='ISO-8859-1')['ingredients'].values#load the file
        cur.execute("DROP TABLE IF EXISTS Ingredients"+recipeId)
        cur.execute("CREATE TABLE Ingredients"+recipeId+"(Id INT PRIMARY KEY AUTO_INCREMENT,ingredients varchar(255))")
        for ingredient in ingredients:
            cur.execute('INSERT INTO Ingredients'+recipeId+'(ingredients) VALUES("'+ingredient+'")')
       
        filename="../data/foodwords/foodwords"+recipeId+".csv"
        words=pandas.read_csv(filename,encoding='ISO-8859-1')#load the file
        cur.execute("DROP TABLE IF EXISTS RecipesCount"+recipeId)
        line="CREATE TABLE RecipesCount"+recipeId+"(Id INT PRIMARY KEY AUTO_INCREMENT,foodword varchar(255), modFood float, modFoodEx varchar(2000),inc_addFood float, inc_addFoodEx varchar(2000), incFood float,incFoodEx varchar(2000) ,decFood float, decFoodEx varchar(2000),subFood float, subFoodEx varchar(2000),numTot int)"
        cur.execute(line)
        for foodword,modFood,modFoodEx,inc_addFood,inc_addFoodEx,incFood,incFoodEx,decFood,decFoodEx,subFood,subFoodEx,numTot in zip(words['foodword'],words['modWord'],words['modWordEx'],words['inc_addWord'],words['inc_addWordEx'],words['incWord'],words['incWordEx'],words['decWord'],words['decWordEx'],words['subWord'],words['subWordEx'],words['numTot']):
            line="INSERT INTO RecipesCount"+recipeId+'(foodword,modFood,modFoodEx,inc_addFood,inc_addFoodEx,incFood,incFoodEx,decFood,decFoodEx,subFood,subFoodEx,numTot) VALUES("'+foodword+'",'+str(modFood)+',"'+filter(lambda x: x in string.printable,modFoodEx)+'",'+str(inc_addFood)+',"'+filter(lambda x: x in string.printable,inc_addFoodEx)+'",'+str(incFood)
            line=line+',"'+filter(lambda x: x in string.printable,incFoodEx)+'",'
            line=line+str(decFood)+',"'+filter(lambda x: x in string.printable,decFoodEx)+'",'
            line=line+str(subFood)+',"'+filter(lambda x: x in string.printable,subFoodEx)+'",'+str(numTot)+')'
            cur.execute(line)


        filename="../data/predictions/predictions"+recipeId+".csv"#this is our keywords
        words=pandas.read_csv(filename,encoding='ISO-8859-1')['foodword'].values#load the file
        mix=pandas.read_csv(filename,encoding='ISO-8859-1')['mixWord'].values#load the file
        inc=pandas.read_csv(filename,encoding='ISO-8859-1')['incWord'].values#load the file
        dec=pandas.read_csv(filename,encoding='ISO-8859-1')['decWord'].values#load the file
        add=pandas.read_csv(filename,encoding='ISO-8859-1')['addWord'].values#load the file
        numTots=pandas.read_csv(filename,encoding='ISO-8859-1')['numTot'].values#load the file
        cur.execute("DROP TABLE IF EXISTS ModWords"+recipeId)
        cur.execute("CREATE TABLE ModWords"+recipeId+"(Id INT PRIMARY KEY AUTO_INCREMENT,words varchar(255), mixWord float,incWord float,decWord float,addWord float, numTot int)")
        for word,m,i,d,a,numTot in zip(words,mix,inc,dec,add,numTots):
            cur.execute('INSERT INTO ModWords'+recipeId+'(words,mixWord,incWord,decWord,addWord,numTot) VALUES("'+word+'",'+str(m)+','+str(i)+','+str(d)+','+str(a)+','+str(numTot)+')')
            
