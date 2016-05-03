import io
import subprocess
import sys
import os
import json
import csv
import html
import re
import nltk

#Takes a directory of files from the SenTube Corpus,
#extracts the relevant information, places it in a
#tab-separated values file, runs the Ark Tweet tagger
#on the comments, formats the words/tags from the tagger
#and then rejoins the tagged comments with the other
#necessary data extracted from the Corpus

def construct(directory):
    #Construct stage 1 files
    outputFile1 = 'firstStageData.txt'
    outputFile2 = 'firstStageComments.txt'
    #call parseAll
    parseAll(directory, outputFile1, outputFile2)
    #Construct stage 2 files
    inputFile = outputFile2
    outputFile3 = 'secondStageComments.txt'
    #call the tagger
    tagger(inputFile, outputFile3)
    #Construct the stage 3 files
    inputFile = outputFile3
    outputFile4 = 'thirdStageComments.txt'
    #call joinTags to properly format the tokens
    joinTags(inputFile, outputFile4)
    #Construct the stage 4 files
    inputFile = outputFile4
    outputFile5 = 'finalData.txt'
    #call rejoinTags to rejoin the tagged comments with
    #the other data fields
    rejoinTaggedComments(outputFile1, inputFile, outputFile5)
    

def parse3(inputFile, outputFile, writer, outputFile2, writer2):
    print(inputFile)
    #print(outputFile)
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
            if annotation.get('vrating'):
                vrating = annotation['vrating']
                if vrating == '1' or vrating == '2' or vrating == '3':
                    for key in annotation:
                        #if the annotation is marked for negative sentiment, decrement the sentiment value
                        if(key == 'negative-video' or key == 'negative-product'):
                            if(sentiment == 1):
                                sentiment = 0
                            else:
                                sentiment = -1
                        #if the annotation is marked for positive sentiment, increment the sentiment value
                        if(key == 'positive-video' or key == 'positive-product'):
                            if(sentiment == -1):
                                sentiment = 0
                            else:
                                sentiment = 1
                    #reformat the tagged words for easier access later
                    #they'll be in the form word_tag
                    #get the other information we need to output
                    user = comment['author']
                    user = clean(user)
                    time = comment['published']
                    #store it in a list
                    data = [sentiment, user, time, commentText]
                    commentText = commentText.replace('"','')
                    commentText = [commentText]
                    #and write it to the output file
                    #print(data)
                    writer.writerow(data)
                    writer2.writerow(commentText)
    #close the read/write files
    readFile.close()
    #writeFile.close()


def parseAll(directory, outputFile, outputFile2):
    #open the output file
    writeFile = open(outputFile, 'w+')
    writeFile2 = open(outputFile2, 'w+')
    #and start a csv writer for it
    writer = csv.writer(writeFile, delimiter='\t', quotechar ='"', quoting=csv.QUOTE_ALL, escapechar = ' ', skipinitialspace=True)
    writer2 = csv.writer(writeFile2, delimiter='\t', quotechar ='"', quoting=csv.QUOTE_ALL, escapechar = ' ',  skipinitialspace=True)
    for filename in os.listdir(directory):
        if filename.endswith("Agata.json"):
            parse3(directory+filename, writeFile, writer, writeFile2, writer2)
    writeFile.close()
    writeFile2.close()

def tagger(filename, outputFile):
    #stringy = 'ark-tweet-nlp-0.3.2/runTagger.sh --model ark-tweet-nlp-0.3.2/model.ritter_ptb_alldata_fixed.20130723 ' + filename + ' > tempOutput.txt'
    stringy = 'ark-tweet-nlp-0.3.2/runTagger.sh --model ark-tweet-nlp-0.3.2/model.ritter_ptb_alldata_fixed.20130723 ' + filename
    output = subprocess.getoutput(stringy)
    #subprocess(stringy)
    #output = output[27:]
    outFile = open(outputFile, 'w+')
    outFile.write(output)
    outFile.close()
    return outFile

def joinTags(inFileName, outFileName):
    inFile = open(inFileName, 'r')
    outFile = open(outFileName, 'w+')
    fileList = list(inFile)
    fileList = fileList[1:len(fileList)-1]
    for line in fileList:
        line = ''.join(line)
        splitLine = line.split('\t')
        comment = splitLine[0]
        tags = splitLine[1]
        commentSplit = comment.split(' ')
        tagsSplit = tags.split(' ')
        taggedWords = []
        i = 0
        for word in commentSplit:
            taggedWords.append(word + '_' + tagsSplit[i])
            i = i+1
        taggedStr = ' '.join(taggedWords)
        outFile.write(taggedStr + '\n')
    outFile.close()

def rejoinTaggedComments(infoFile, taggedFile, outputFile):
    info = open(infoFile, 'r+')
    tagsFile = open(taggedFile, 'r+')
    tagsList = list(tagsFile)
    #print(tagsList)
    outFile = open(outputFile, 'w+', newline='')
    writer = csv.writer(outFile, delimiter='\t', quotechar ='"', quoting=csv.QUOTE_NONE, doublequote = False, escapechar = ' ', lineterminator='\n')
    i = 0
    for line in info:
        splitLine = line.split('\t')
        sent = splitLine[0]
        #user = splitLine[1]
        #time = splitLine[2]
        #print(splitLine[2])
        #print(tagsList[i])
        tags = tagsList[i].replace('\n','')
        data = [sent, tags]
        i = i + 1
        #print(data)
        writer.writerow(data)
    info.close()
    tagsFile.close()
    outFile.close()

def clean(string):
     string = re.sub(r"[^\x00-\xFFFF]", "", string) #remove non-utf-8 characters
     string = re.sub(r"\+\w*", "USERNAME", string) #cover usernames. Doesn't catch multi-word names
     string = re.sub(r"\d\d?:\d\d", "TIMESTAMP", string) #replace timestamps
     string = re.sub(r'http\S+', 'URL', string) #replace urls
     string = re.sub(r'www\.\S+', 'URL', string) #replace urls
     string = string.replace('\n', '')
     return(string)
