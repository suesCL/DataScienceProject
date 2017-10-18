import sys
import json
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



def findLocationSentiment(response, scoreMap):
    stateScores = {}
    for line in response:
        #filter by language
        if  line.has_key("text") and line.has_key("lang"):
            if line.get("lang") == "en":
                # method 1 : use user object's location field
                if line.has_key("user"):
                    if line["user"]["location"] is not None:
                        stateFound = False
                        for state in states.keys():
                            if line["user"]["location"].find(state) != -1:
                                stateFound = True
                                stateScores = addState(stateScores, state, line, scoreMap)
                        if not stateFound:
                            checkRetweetUser(line, stateScores, scoreMap)

                    else:
                        checkRetweetUser(line, stateScores, scoreMap)
                else:
                    checkRetweetUser(line, stateScores, scoreMap)
    return stateScores

def checkRetweetUser(line, stateScores, scoreMap):
    if line.has_key("retweeted_status"):
        if line["retweeted_status"].has_key("user"):
            if line["retweeted_status"]["user"]["location"] is not None:
                stateFound = False
                for state in states.keys():
                    if line["retweeted_status"]["user"]["location"].find(state) != -1:
                        stateFound = True
                        stateScores = addState(stateScores, state, line, scoreMap)
                if not stateFound:
                    checkPlace(line, stateScores, scoreMap)
            else:
                checkPlace(line, stateScores, scoreMap)
        else:
            checkPlace(line, stateScores, scoreMap)
    else:
        checkPlace(line, stateScores, scoreMap)


def checkPlace(line, stateScores, scoreMap):
    # method 2: use place object's full name field
    if line.has_key("place"):
        if line["place"] is not None:
            if line["place"].has_key("country_code"):
                if line["place"]["country_code"] == "US":
                    if line["place"].has_key("full_name"):
                        for state in states:
                            if line["place"]["full_name"].find(state) != -1:
                                stateScores = addState(stateScores, state, line, scoreMap)





def addState(stateScores, state, line, scoreMap):

    if state in stateScores:
        stateScores[state] += calculateScore(line,scoreMap)
        stateScores[state] = stateScores[state]/2
    else:
        stateScores[state] = calculateScore(line,scoreMap)
    return stateScores


def calculateScore(line, scores):
    #check duplicates
    tweetCopy = ""
    scoreCopy = 0
    tweet_score = 0

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
        scoreCopy = tweet_score
    else:
        tweet_score = scoreCopy
    return tweet_score




def removeNonAscii(s):
    return filter(lambda x: x in ascii, s)

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}



def main():
    score_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = storeSentimentScores(score_file)
    data = jsonConvert(tweet_file)
    locationScores = findLocationSentiment(data,scores)

    happyState = ""
    maxScore = 0
    for key, value in locationScores.iteritems():
        if value > maxScore :
            happyState = key
            maxScore = value
    print happyState





if __name__ == '__main__':
    main()
