import sys
import json
import sys
import codecs
import string
import re

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
ascii = set(string.printable)

def jsonConvert(fp):
    response = []
    for line in fp:
        if isinstance(line, bytes): #check if it's in byte
            line = line.decode('utf-8')
        else:
            print("Object not of byte type")
        decoded = json.loads(line)
        response.append(decoded)
    return response


def storeSentimentScores(fp):
    scores = {}
    for line in fp:
        term, score = line.strip().split("\t")
        scores[term] = int(score)
    return scores


def scoreSentiment(response, scores):
    tweets_score = []
    #check duplicates
    tweetCopy = ""
    scoreCopy = 0
    for line in response:
        tweet_score = 0

        if  line.has_key("text") and line.has_key("lang"):
            if line.get("lang") == "en":

                #get each tweet
                tweet = line.get("text")
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


                    #check if any sentiment terms exist in tweet
                    for key, value in scores.iteritems():
                        if tweet.find(key) != -1:
                            tweet_score += value
                    tweets_score.append(tweet_score)
                    scoreCopy = tweet_score
                else:
                    tweets_score.append(scoreCopy)
            else: tweets_score.append(tweet_score)
        else:
            tweets_score.append(tweet_score)
    return tweets_score



def removeNonAscii(s):
    return filter(lambda x: x in ascii, s)



def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = storeSentimentScores(sent_file)
    data = jsonConvert(tweet_file)
    tweetScores = scoreSentiment(data,scores)
    for i in tweetScores:
        print i

if __name__ == '__main__':
    main()
