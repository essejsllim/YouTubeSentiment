import io
import sys
import os
import json
import csv
import html
import re
import nltk
import textblob
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
import itertools

ap_tagger = PerceptronTagger()

def parse(inputFile, outputFile):
    readFile = open(inputFile, 'r', encoding='utf-8-sig')
    jsonFile = json.load(readFile)
    writeFile = open(outputFile, 'w+')
        #print(key)
    comments = jsonFile['comments']
    #print(comments)

    for comment in comments:
        for key in comment:
            if(key == 'text'):
                commentText = TextBlob(comment[key], pos_tagger=ap_tagger)
                taggedComment = commentText.tags
                print('Key: {}, Comment: {}'.format(key, taggedComment))
            else:
                print('Key: {}, Comment: {}'.format(key, comment[key]))
        print('\n')
    #print(jsonFile)


def parse2(inputFile, outputFile):
    readFile = open(inputFile, 'r', encoding='utf-8')
    jsonFile = json.load(readFile)
    writeFile = open(outputFile, 'w+')
    writer = csv.writer(writeFile, delimiter=',', quotechar ='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        #print(key)
    comments = jsonFile['comments']
    #print(comments)
    for comment in comments:
        for key in comment:
            if(key == 'text'):
                commentText = TextBlob(comment[key], pos_tagger=ap_tagger)
                taggedComment = commentText.tags
                tags = []
                for pair in taggedComment:
                    word = pair[0].replace("\ufeff", "")
                    tag = pair[1]
                    tags.append(word+'_'+tag)
                #comment[key] = taggedComment
        user = str(comment['author'])
        time = str(comment['published'])
        data = [user, time, tags]
        writer.writerow(data)
    readFile.close()
    writeFile.close()
    #print(jsonFile)

def parse3(inputFile, outputFile, writer):
    print(inputFile)
    print(outputFile)
    #read in the input file
    readFile = open(inputFile, 'r', encoding='utf-8')
    #and open it with the json module
    jsonFile = json.load(readFile)
    #open the output file
    ##writeFile = open(outputFile, 'w+')
    #and start a csv writer for it
    ##writer = csv.writer(writeFile, delimiter=',', quotechar ='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    #get the comments from the json file
    comments = jsonFile['comments']
    #loop through all the comments
    for comment in comments:
        if comment.get('annotation'):
            #grabbing the annotation and comment text from each one
            annotation = comment['annotation']
            commentText = comment['text']
            commentText = clean(commentText)
            #and setting an initial sentiment score
            sentiment = 0
            for key in annotation:
                #if the annotation is marked for negative sentiment, decrement the sentiment value
                if(key == 'negative-video' or key == 'negative-product'):
                    sentiment = sentiment - 1
                #if the annotation is marked for positive sentiment, increment the sentiment value
                if(key == 'positive-video' or key == 'positive-product'):
                    sentiment = sentiment + 1
            #tag all the comment text using the textblob tagger
            commentText = TextBlob(commentText, pos_tagger=ap_tagger)
            #and extract the tagged text
            taggedComment = commentText.tags
            tags = []
            #reformat the tagged words for easier access later
            #they'll be in the form word_tag
            for pair in taggedComment:
                word = pair[0]
                tag = pair[1]
                tags.append(word+'_'+tag)
            #get the other information we need to output
            user = comment['author']
            user = clean(user)
            time = comment['published']
            #store it in a list
            data = [sentiment, user, time, tags]
            #and write it to the output file
            #print(data)
            writer.writerow(data)
    #close the read/write files
    readFile.close()
    #writeFile.close()

def parseAll(directory, outputFile):
    #open the output file
    writeFile = open(outputFile, 'w+')
    #and start a csv writer for it
    writer = csv.writer(writeFile, delimiter=',', quotechar ='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    for filename in os.listdir(directory):
        if filename.endswith("Agata.json"):
            parse3(filename, writeFile, writer)
    writeFile.close()

def clean(string):
     string = re.sub(r"[^\x00-\xFFFF]", "", string) #remove non-utf-8 characters
     string = re.sub(r"\+\w*", "USERNAME", string) #cover usernames. Doesn't catch multi-word names
     string = re.sub(r"\d\d?:\d\d", "TIMESTAMP", string) #replace timestamps
     string = re.sub(r'http\S+', 'URL', string) #replace urls
     string = re.sub(r'www\.\S+', 'URL', string) #replace urls
     return(string)
