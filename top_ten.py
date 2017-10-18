import sys
import json
import codecs
import string
import re
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
ascii = set(string.printable)

totalHash = 0

def findHashTags(response):
    hashtagCount = {}
    global totalHash
    for line in response:
        if  line.has_key("text") and line.has_key("lang"):
            if line.get("lang") == "en":
                for i in line.keys():
                    if i == "entities":
                        for item in line["entities"]["hashtags"]:
                            hashtag = item["text"]
                            totalHash += 1
                            if hashtagCount.has_key(hashtag):
                                hashtagCount[hashtag] += 1
                            else:
                                hashtagCount[hashtag] = 1
    return hashtagCount


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


def removeNonAscii(s):
    return filter(lambda x: x in ascii, s)


def main():
    tweet_file = open(sys.argv[1])
    response = jsonConvert(tweet_file)
    hashTags = findHashTags(response)
    count = 0
    for key, value in sorted(hashTags.iteritems(), reverse = True, key=lambda (k,v): (v,k)):
        if count < 10:
            key = removeNonAscii(key)
            print "%s %s" % (key, value)
        count += 1


if __name__ == '__main__':
    main()
