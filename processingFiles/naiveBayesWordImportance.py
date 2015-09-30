import pandas
import pandasql
from nltk import sent_tokenize  
from nltk import word_tokenize 
import numpy as np
from nltk.corpus import wordnet as wn
from nltk.corpus import movie_reviews
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


movWords=[]
movTarget=[]
for sentence in movie_reviews.sents():
    for word in sentence:
        types=[b.lexname() for b in wn.synsets(word)]
        if 'adj.all' in types and word!='i' and 'noun.quantity' not in types and all(['verb' not in type1 for type1 in types]) and 'noun.food' not in types:
            movWords.append(word)
            movTarget.append('mov')
#load the move reviews data, not verbs and not foods

filename="filenames.csv"#the recipe id stored in this file
recipeIds=pandas.read_csv(filename,encoding='ISO-8859-1')['filenames'].values#load the file
dictInfo={}#create a dic for the word info
for recipeId in recipeIds:#go through each recipe
    print recipeId
    filename="reviews/reviews"+str(recipeId)+".csv"#this is our keywords
    reviews=pandas.read_csv(filename,encoding='ISO-8859-1')#load the file
    #get the reviews
    recRev = sent_tokenize(' '.join([review.lower().replace('c.','cup').replace('tspn.','teaspoon').replace(
                'tbsp.','tablespoon').replace('tbs.','tablespoon').replace('tsp.','teaspoon').replace('tbl.','tablespoon').replace(
                ' T.',' tablespoon').replace(' t.',' teaspoon') for review in reviews['reviewText']]).encode('ascii','ignore'))
    #format reviews
    
    recWords=[]
    recTarget=[]
    for sentence in recRev:
        words = word_tokenize(sentence)
        for word in words:
            word=''.join([i for i in word if not i.isdigit()])
            types=[b.lexname() for b in wn.synsets(word)]
            if 'adj.all' in types and word!='i' and 'noun.quantity' not in types and all(['verb' not in type1 for type1 in types]) and 'noun.food' not in types:
                recWords.append(word)
                recTarget.append('rec')
    #load the recipe data

    #apply tfidf and naive bayes to movie and recipe data
    #http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(np.array(recWords+movWords))

    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    X_train_tf.shape

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = MultinomialNB().fit(X_train_tfidf, np.array(recTarget+movTarget))

    docs_new=np.array(list(set(recWords)))

    X_new_counts = count_vect.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    arrayTot=[]
    predicted = clf.predict_proba(X_new_tfidf)
    for word,pred in zip(docs_new,predicted):
        arrayTot.append([word,pred[0],pred[1]])


    #get some sentences for examples, one from negative review and one from positive reviews
    #different from above without the lower
    posRev2 = sent_tokenize(' '.join([review for review,rating in zip(reviews['reviewText'],reviews['ratings']) if rating>3]).encode(
                'ascii','ignore').replace('c.','cup').replace('tspn.','teaspoon').replace(
                'tbsp.','tablespoon').replace('tbs.','tablespoon').replace('tsp.','teaspoon').replace('tbl.','tablespoon').replace(
                ' T.',' tablespoon').replace(' t.',' teaspoon'))
    negRev2 = sent_tokenize(' '.join([review for review,rating in zip(reviews['reviewText'],reviews['ratings']) if rating<3]).encode(
                'ascii','ignore').replace('c.','cup').replace('tspn.','teaspoon').replace(
                'tbsp.','tablespoon').replace('tbs.','tablespoon').replace('tsp.','teaspoon').replace('tbl.','tablespoon').replace(
                ' T.',' tablespoon').replace(' t.',' teaspoon'))


    arrayInfo=[]
    for a in sorted(arrayTot, key=lambda student: student[1]):
    #sorted by most associated with recipes
        if float((recWords).count(a[0]))/float(len(recWords))>0.002 and a[2]>.75: 
        #has a reasonable number of mentions and not too far from the most probable
            posEx=" "
            negEx=" "
            for rev in posRev2:#get sample sentences but not too long
                if a[0] in rev and len(rev.split(' '))<20:
                    posEx=rev
                    break;
            for rev in negRev2:
                if a[0] in rev and len(rev.split(' '))<20:
                    negEx=rev
                    break;
            arrayInfo.append([a[0],posEx,negEx])
    dictInfo[recipeId]=arrayInfo
    #put it into the dictionary for later

#store the important words
f_out = open('importantWords/importantWords.csv','w')
f_out.write('foodword,posEx,negEx\n')

for recipeId in recipeIds:
    for x in dictInfo[recipeId]:
        f_out.write(str(recipeId)+',"'+x[0]+'","'+x[1]+'","'+x[2]+'"\n')
f_out.close()
