#------------------------------------------------------------------------------------#
# This program is designed to be a Naive Bayes Classifier to categorize
# tweets pulled from a MySQL Database. The tweets will be categorized based
# on whether or not they pertain to the subject of social unrest.
#
#    Author: Timothy Grant Clark
#    References:https://pythonprogramming.net/naive-bayes-classifier-nltk-tutorial/
#         https://www.youtube.com/playlist?list=PLQVvvaa0QuDf2JswnfiGkliBInZnIC4HL
#    Date Created: 5/18/2018
#    Python Version: 3.6
#-------------------------------------------------------------------------------------#
import mysql.connector
import nltk
from nltk.corpus import stopwords
import re
import random
import pandas as pd
import preprocessor as p
from pandas import DataFrame
connection = mysql.connector.connect(host='localhost',
                            user='root',
                            passwd='pass123',
                            db='twitter_research',
                            charset='ascii',
                            use_unicode= True)



# DataFrame of tweets hand picked to use for Naive Bayes Classifier
df = pd.read_sql("SELECT * from TWEETS WHERE Important=1 OR Important=0;", con=connection)
#print(df)
# list of words selected tweets currently marked by 1 or 0 in field Important
scrapedTweets = []
#list of all words
words = []
#List of Regular Expressions used in selected vocabulary
regex = ["(.*)strik(.*)" ,
	"(.*)unrest(.*)",
     "(.*)mass(.*)",
     "(.*)protest(.*)",
     "(.*)demonstrat(.*)",
     "(.*)compan(.*)",
     "(.*)union(.*)",
     "(.*)caste(.*)",
     "(.*)religi(.*)",
     "(.*)ethnic(.*)",
     "(.*)reform(.*)",
     "(.*)rebel(.*)",
     "(.*)defen(.*)",
     "(.*)violen(.*)",
     "(.*)war (.*)",
     "(.*)arm (.*)",
     "(.*)fight(.*)",
     "(.*)right(.*)",
     "(.*)free(.*)",
     "(.*)libert(.*)",
     "(.*)justice(.*)",
     "(.*)fair(.*)",
     "(.*)equal(.*)",
     "(.*)terror(.*)",
     "(.*)extrem(.*)",
     "(.*)bomb(.*)",
     "(.*)IED (.*)",
     "(.*)weapon(.*)",
     "(.*)gun(.*)",
     "(.*)wmd(.*)",
     "(.*)threat(.*)",
     "(.*)suicid(.*)",
     "(.*)murder(.*)",
     "(.*)kill(.*)",
     "(.*)death(.*)",
     "(.*)explo(.*)",
     "(.*)militar(.*)",
     "(.*)police(.*)",
     "(.*)elit(.*)",
     "(.*)govern(.*)",
     "(.*)pressi(.*)",
     "(.*)power(.*)",
     "(.*)regime(.*)",
     "(.*)fraud(.*)",
     "(.*)corrupt(.*)",
     "(.*)coup(.*)",
     "(.*)safe(.*)",
     "(.*)secur(.*)",
     "(.*)protect(.*)",
     "(.*)enem(.*)",
     "(.*)resist(.*)",
     "(.*)hostage(.*)",
     "(.*)truce(.*)",
     "(.*)fire(.*)",
     "(.*)greed(.*)",
     "(.*)panic(.*)",
     "(.*)inflat(.*)",
     "(.*)price(.*)",
     "(.*)water(.*)
]
combined =
#list of common words to remove before running classifier
s = set(stopwords.words('english'))
# remove url append from tweets into training set
for (index, row) in df.iterrows():
    tweet = df.at[index,'Text']
    pyboolean = df.at[index,'PyBoolean']
    p.set_options(p.OPT.URL, p.OPT.EMOJI)
    cleanTweet = p.clean(tweet).lower()
    scrapedTweets.append((list(cleanTweet.split(" ")), pyboolean) )
    all_words = cleanTweet.split(" ")
    # create list of unique words
    for word in all_words:
        if len(word) > 2:
            if word not in s:
                words.append(word)

random.shuffle(scrapedTweets)
word_dist =list(nltk.FreqDist(words))

#featureSet of words to train and test, Could we possibly use our vocabulary?

def find_features(tweets):
    wrd = set(tweets)
    features = {}
    for w in word_dist:
        features[w] = (w in wrd )
    return features

featureSets = [(find_features(tweetText), category) for(tweetText, category) in scrapedTweets]
#print(featureSets)

trainSet = featureSets[:80]
testSet = featureSets[80:]

classifier = nltk.NaiveBayesClassifier.train(trainSet)
print("accuracy:", (nltk.classify.accuracy(classifier,testSet))*100, "percent")
classifier.show_most_informative_features(20)
