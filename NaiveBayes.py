import io
import subprocess
import sys
import os
import json
import csv
import html
import re
import nltk

trainingSet = open('C:\\Users\\essej\\OneDrive\\Documents\\VASSAR\\Senior_Year\\Spring\\CMPU366\\Final Project\\SenTube\\Testing Corpus\\Training Data\\finalTrainingComments.txt', 'r')
testingSet = open('C:\\Users\\essej\\OneDrive\\Documents\\VASSAR\\Senior_Year\\Spring\\CMPU366\\Final Project\\SenTube\\Testing Corpus\\Testing Data\\finalTestingComments.txt', 'r')

trainReader = csv.reader(trainingSet)
testReader = csv.reader(testingSet)

trainData = list(trainReader)
#testData = list(testReader)

print(trainData)
'''
def loadCsv(file):
    lines = csv.reader(file)
    dataset = list(lines)
    return lines
'''
