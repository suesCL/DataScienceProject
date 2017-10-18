# Twitter Sentiment Analysis 

## Overview 
Millions people use twitter to communicate and express their opininons on topics. The project will analyze tweets from Twitter APIs to score 
tweets' sentiment, generate sentiment score for new terms, predict happiest state in US and find the most frequently used hashtags. 

## Content 
* Stream twitter data 
* Derive sentiment of each tweet
* Derive sentiment of new terms 
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
4. Extract tweet text from each line of tweet information and give sentiment score for each tweet text. 
    * Narrow the search to calculate scores for only English tweets. Give zero to the rest of tweets. 
    * Clean each tweet text by removing symbols, urls, hashtags using regex expressions.
    * Find the sentiment carrying words in each text. Total the scores of the words and assign the total score to the text.

5. The final output is tthe scores for all tweets. There is one score for the corresponding tweet per line. 

## Derive sentiment of new terms 
This part intends to derive the score for non-sentiment-carrying terms in each tweet based on the scores of sentiment-carrying words.

**Procedures:**
1. Split each long string of tweet text into smaller strings based on white spaces. Each string corresponds to a word or phrase. Create a list containing all of the words for each tweet. 
```
for line in response:
        list = line.split(' ')
        list = [word.strip() for word in list]
        list = [x for x in list if x]
```
2. Find the sentiment-carrying terms in the list and count the number of positive terms and the number of negative terms respectively. Substracting the number of negative terms from the number of postive terms gives the score for all non-sentiment-carrying words in the tweet text. Add them to a dictionary of new terms from all tweets.
```
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
            nonSentScore = countPos-countNeg
        # assign scores to each non-sentiment-carrying words 
        for i in list:
            if i not in nonSentTerms:
                nonSentTerms[i] = nonSentScore
```


## Compute term frequency 
## Predict the happiest state 
## Find top ten hashtags

## Installation
The project is written in Python 2.7. 
