# Twitter Sentiment Analysis 

## Overview 
Millions people use twitter to communicate and express their opininons on topics. The project will analyze tweets from Twitter APIs to score 
tweets' sentiment, generate sentiment score for new terms, predict happiest state in US and find the most frequently used hashtags. 

* Stream twitter data 
* Derive sentiment of each tweet
* Derive sentient of new terms 
* Compute term frequency 
* Predict the happiest state 
* Find top ten hashtags 

## Stream twitter data 
The project collected live stream data from Twitter lasting for 3 minutes. 


## Derive sentiment of each tweet
**Procedures:**
1. Read AFINN-111 file which contains pre-computed sentiment scores. Each line contains a word followed by a sentiment 
score. 
2. Save each word with its score as a key-value pair in a dictionary. The function shown below：
```
    def storeSentimentScores(fp):
      scores = {}
      for line in fp:
          term, score = line.strip().split("\t")
          scores[term] = int(score)
      return scores
```
3. Read the output file, decode each tweet and and convert it to python object. Create a list of dictionaries where each list item is a tweet.
```
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
```








## Derive sentient of new terms 
## Compute term frequency 
## Predict the happiest state 
## Find top ten hashtags

## Installation
The project is written in Python 2.7. 
