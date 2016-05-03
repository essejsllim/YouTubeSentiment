import io
import subprocess
import sys
import os
import json
import csv
import html
import re
import nltk


def run():
    posWords = popularAdj('finalTrainingComments.txt', 'p')
    negWords = popularAdj('finalTrainingComments.txt', 'n')
    print(posWords)
    print(len(posWords))
    print(len(negWords))
    overlap = {x for x in posWords if x in negWords}
    posWords = posWords - overlap
    negWords = negWords - overlap
    print(len(posWords))
    print(len(negWords))
    posWords = addToSeedSets(posWords, negWords, 'cleanTaggedComments.txt', 'p')
    negWords = addToSeedSets(posWords, negWords, 'cleanTaggedComments.txt', 'n')
    print(len(posWords))
    print(len(negWords))
    overlap = {x for x in posWords if x in negWords}
    posWords = posWords - overlap
    negWords = negWords - overlap
    print(len(posWords))
    print(len(negWords))
    '''
    print(len(posWords))
    print(len(negWords))
    posWords = seedSetAdder(posWords, 'cleanTaggedComments.txt')
    negWords = seedSetAdder(negWords, 'cleanTaggedComments.txt')
    print(len(posWords))
    print(len(negWords))
    overlap = {x for x in posWords if x in negWords}
    posWords = posWords - overlap
    negWords = negWords - overlap
    print(len(posWords))
    print(len(negWords))
    #posWords = addToSeedSet(posWords, negWords, 'cleanTaggedComments.txt', 'and')
    #negWords = addToSeedSet(negWords, posWords, 'cleanTaggedComments.txt', 'and')
    '''

def popularAdj(filename, choice):
    #open the input file
    file = open(filename, 'r')
    #initialize the sets for positive and negative words
    posWords = set()
    negWords = set()
    #iterate through the file
    for line in file:
        #split the lines into sentiment and commentText
        sent = line.split('\t')[0]
        comment = line.split('\t')[1]
        #split the commentText from each line into a list of tokens
        tokList = comment.split(' ')
        #split the tokens into word/tag
        #due to the formatting of the ArkTagger, each tokList will
        #start with a ' ', so we have to catch that
        for tok in tokList:
            try:
                word = tok.split('_')[0]
                tag = tok.split('_')[1]
            except IndexError as e:
                word = ''
                tag = ''
            #if the tag is some form of adjective or adverb, we add it to one of our sets
            if tag == 'JJ' or tag == 'JJR' or tag == 'JJS' or tag == 'RB' or tag == 'RBR' or tag == 'RBS':
                #if the comment had negative sentiment, we add it to negWords
                if sent == ' "-1 "':
                    negWords.add(word.lower())
                #if the comment had positive sentiment, we add it to posWords
                if sent == ' "1 "':
                    posWords.add(word.lower())
    #return either the set of positive or negative words
    if choice == 'p':
        return posWords
    if choice == 'n':
        return negWords

def addToSeedSets(posSet, negSet, filename, choice):
    file = open(filename, 'r')
    posWords = posSet
    negWords = negSet
    for line in file:
        tokenList = line.split(' ')
        prevprevword = ''
        prevword = ''
        for token in tokenList:
            word = token.split('_')[0]
            tag = token.split('_')[1]
            if (tag == 'JJ' or tag == 'RB') and prevword == 'and' and (prevprevword in posSet):
                posSet.add(word.lower())
            if (tag == 'JJ' or tag == 'RB') and prevword == 'but' and (prevprevword in posSet):
                negSet.add(word.lower())
            if (tag == 'JJ' or tag == 'RB') and prevword == 'and' and (prevprevword in negSet):
                negSet.add(word.lower())
            if (tag == 'JJ' or tag == 'RB') and prevword == 'but' and (prevprevword in negSet):
                posSet.add(word.lower())
            prevprevword = prevword
            prevword = word
    if choice == 'p':
        return posWords
    if choice == 'n':
        return negWords
                

pos_words = set(['great', 'good', 'decent', 'stoked', 'nice', 'better', 'striking',
                'neat', 'coolest', 'awesome', 'versatile', 'outstanding', 'best',
                'love', 'amazing', 'like', 'helpful', 'quick', ':)', 'fast',
                'beautiful', 'handsome', ':-)', 'honest', 'happy', 'fantastic',
                'wonderful', 'classy', 'clever', 'intelligent', 'amazed',
                'excellent', 'balanced', 'ballin\'', 'brilliant', 'informative',
                'direct', 'comprehensive', 'perfect', 'awesom', 'cool', 'nice',
                ':D', 'gr8', 'interesting', ';)', ';D', 'detailed', 'rocks', 'loving',
                'fastest', 'clear', 'happy', 'happier', 'enjoyed', 'legit', 'sweet',
                'flawless', 'flawlessly', 'fast', 'adore', 'dope', 'concise', 'fair',
                'responsive', 'sexy', '<3', 'convenient', 'smooth', 'simple', 'impressive',
                'decent', 'stable', 'satisfied'])

neg_words = set(['bad', 'poor', 'shit', 'twat', 'ass', 'suck', 'fucking', 'pompous'
                'dumbass', 'frickin', 'pointless', 'douchebag', 'shitty',
                'useless', 'ugly', 'ripoff', 'boring', 'fag', 'worst', 'hate',
                'douche', 'ridiculous', 'dumb', 'racist', 'idiot', 'stupid',
                'whiny', 'waste', 'idiot', 'ignorant', 'primitive', 'fail', 'wtf',
                'outdated', 'trash'])


def addToSeedSet(seedSet1, seedSet2, comments, choice):
    #open the file of comments
    comments = open(comments, 'r')
    #initialize the seed sets, so we don't actually alter the input sets
    newSeeds = seedSet1
    newOppSeeds = seedSet2
    #iterate through the file
    for line in comments:
        #split the comment into its tokens
        comment = line.split(' ')
        #initialize the values of the 2 previous words (used later)
        prevword = ''
        prevprevword = ''
        #split the tokens into word/tag pairs
        for pair in comment:
            word = pair.split('_')[0]
            tag = pair.split('_')[1]
            #and get rid of any newline characters that have made it this far
            word = word.replace("\n","")
            tag = tag.replace("\n","")
            #if the tag is an adjective or adverb, and is linked to one of the words in newSeeds with
            #the word 'and', we add it to newSeeds
            if tag == 'JJ' or tag == 'JJR' or tag == 'JJS' or tag == 'RB' or tag == 'RBR' or tag == 'RBS' and prevword == 'and' and prevprevword in newSeeds:
                newSeeds.add(word.lower())
            #if the tag is an adjective or adverb, and is linked to one of the words in newSeeds with
            #the word 'but', we add it to newOppSeeds
            if tag == 'JJ' or tag == 'JJR' or tag == 'JJS' or tag == 'RB' or tag == 'RBR' or tag == 'RBS' and prevword == 'but' and prevprevword in newSeeds:
                newOppSeeds.add(word.lower())
            #update the values of the previous words accordingly
            prevprevword = prevword
            prevword = word
    if choice == 'and':
        return newSeeds
    if choice == 'but':
        return newOppSeeds
    else:
        return 'Invalid choice. Please enter either "and" or "but"'

def seedSetAdder(seedSet, comments):
    #open the file of comments
    comments = open(comments, 'r')
    #initialize the seed sets, so we don't actually alter the input sets
    newSeeds = seedSet
    #iterate through the file
    for line in comments:
        #split the comment into its tokens
        comment = line.split(' ')
        #initialize the values of the 2 previous words (used later)
        prevword = ''
        prevprevword = ''
        #split the tokens into word/tag pairs
        for pair in comment:
            word = pair.split('_')[0]
            tag = pair.split('_')[1]
            #and get rid of any newline characters that have made it this far
            word = word.replace("\n","")
            tag = tag.replace("\n","")
            #if the tag is an adjective or adverb, and is linked to one of the words in newSeeds with
            #the word 'and', we add it to newSeeds
            if tag == 'JJ' or tag == 'RB' and prevword == 'and' and prevprevword in newSeeds:
                newSeeds.add(word.lower())
            #update the values of the previous words accordingly
            prevprevword = prevword
            prevword = word
    return newSeeds
