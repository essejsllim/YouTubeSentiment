import nltk
import textblob
import re
import csv
inFile = open('comments-qsLCCp2AD6I.csv', 'r' , encoding='utf-8')
inFileReader = csv.reader(inFile, delimiter=',', quotechar='"', quoting = csv.QUOTE_ALL, skipinitialspace = True)
outFile = open("cleanedComments.csv", 'w+')
outFileWriter = csv.writer(outFile, delimiter=',', quotechar='"', quoting = csv.QUOTE_ALL, skipinitialspace = True)

def clean(string):
     string = re.sub(r"[^\x00-\xFFFF]", "", string) #remove non-utf-8 characters
     string = re.sub(r"\+\w*", "USERNAME", string) #cover usernames. Doesn't catch multi-word names
     string = re.sub(r"\d\d?:\d\d", "TIMESTAMP", string) #replace timestamps
     string = re.sub(r'http\S+', 'URL', string) #replace urls
     string = re.sub(r'www\.\S+', 'URL', string) #replace urls
     return(string)

for line in inFileReader:
    cleanLine = []
    for field in line:  
        if field != '':
            cleanField = clean(field)
            cleanLine.append(cleanField)
    outFileWriter.writerow(cleanLine)
    #print("usr:", cleanLine[1], "       ", cleanLine[4])
    
inFile.close()
outFile.close()
