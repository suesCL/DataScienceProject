import sys
import json
import codecs
from sets import Set
import string
import re

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
ascii = set(string.printable)


def removeNonAscii(s):
    return filter(lambda x: x in ascii, s)


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
                    list = tweet.split(' ')
                    list = [word.strip() for word in list]
                    list = [x for x in list if x]
                    response.append(list)

    return response

def calculateFrequency(tweetsList):

    Occurrances = {}
    totalOccur = 0
    for list in tweetsList:
        for term in list:
            totalOccur += 1
            if term in Occurrances:
                Occurrances[term] += 1
            else:
                Occurrances[term] = 1
    for key, value in Occurrances.iteritems():
        frequency = float(value) / totalOccur
        print key + " " + str(frequency)


def main():
    output = open(sys.argv[1])
    tweetsList = cleanTweets(output)
    frequencies = calculateFrequency(tweetsList)


if __name__ == '__main__':
    main()
