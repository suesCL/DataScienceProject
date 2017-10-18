import sys
import json
import codecs
from sets import Set
import string
import re

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
ascii = set(string.printable)

def cleanTweets(fp):
    response = []
    for line in fp:
        if isinstance(line, bytes): #check if it's in byte
            line = line.decode('utf-8')
        else:
            print("Object not of byte type")
        decoded = json.loads(line)

        #check duplicates
        tweetCopy = ""
        if  decoded.has_key("text") and decoded.has_key("lang"):
            if decoded.get("lang") == "en":
                #get each tweet
                tweet = decoded.get("text")
                if tweetCopy != tweet:
                    tweetCopy = tweet
                    tweet = removeNonAscii(tweet)
                    #remove tag like "RT @xxxx: "
                    tweet = re.sub(r'RT\s@([\w\.-]+):\s',"",tweet)
                    #remove tag "@xxxx"
                    tweet = re.sub(r'@([\w\.-]+)',"",tweet)
                    #remove tag "https:\\xxx"
                    tweet = re.sub(r'(http([\w/:\.-]+))+',"",tweet)
                    #remove tag "http"
                    tweet = re.sub(r'(ht[\w])+',"",tweet)
                    #remove tag "htt" and "ht"
                    tweet = re.sub(r'(htt)+',"",tweet)
                    tweet = re.sub(r'(ht)+',"",tweet)
                    #remove hashtag "#..."
                    tweet = re.sub(r'(#([#\w\.-]+))+',"",tweet)
                    #remove special symbols
                    tweet = re.sub('[^a-zA-Z\s]+', "", tweet)
                    tweet = re.sub('\n+', " ", tweet)

                    tweet = tweet.encode("utf-8")
                    tweet = tweet.lower()
                    tweet = tweet.strip()
                    response.append(tweet)

    return response



def storeSentimentScores(fp):
    scores = {}
    for line in fp:
        term, score = line.strip().split("\t")
        scores[term] = int(score)
    return scores

def scoreSentiment(response,scores):

    nonTerm_scores = {}
    for line in response:
        list = line.split(' ')
        list = [word.strip() for word in list]
        list = [x for x in list if x]

        countPos = 0
        countNeg = 0

        # check if senetiment-carrying terms exist in the list
        for key, value in scores.iteritems():
            if key in list:
                list = filter(lambda a: a != key, list)
                if scores[key] > 0:
                    countPos += 1
                else:
                    countNeg += 1
            scores_nonTerm = float(countPos-countNeg)

        for i in list:
            if i not in nonTerm_scores:
                nonTerm_scores[i] = scores_nonTerm
    return nonTerm_scores

def removeNonAscii(s):
    return filter(lambda x: x in ascii, s)


def main():
    scores = open(sys.argv[1])
    output = open(sys.argv[2])
    scores = storeSentimentScores(scores)
    cleaned_tweets = cleanTweets(output)
    nonTerm_scores = scoreSentiment(cleaned_tweets,scores)
    for key, value in nonTerm_scores.iteritems():
        print key + " " + str(value)





if __name__ == '__main__':
    main()
