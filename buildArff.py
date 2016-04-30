import os
import string
from collections import OrderedDict
import sys

#####################################################################################
##     Method buildArff() reads a file with tagged tweets and outputs an arff file
##     for use with Weka. Input and output filenames are currently hard-coded;
##     this can be modified to pass the filenames as parameters (program must be run
##     the command line to pass paramters). It is assumed that the input file is in the
##     same directory as the buildArff() method.
##
##     Input format:
##
##           <digit> , <tagged_words>
##
##     where <digit> is either 0 or 4, indicating the sentiment of the tweet as given
##     in the training data; a comma follows <digit>, and <tagged_words> is a series
##     of <word_PoS> comprising the tagged tokens in the tweet, where "word" and "PoS"
##     are connected with the character "_", and sequential <word_PoS> items are separated
##     with blanks. Each tweet ends with a carriage return.
##
##     Output is written to a file in the same directory as the buildArff() method;
##     again the filename is currently hard-coded.
#####################################################################################


def is_punct_string(s):
    # check if string consists only of punctuation 
    for char in s:
       if not char in string.punctuation:
           return False
    return True

def is_digit_string(s):
    # check if string consists only of digits 
    for char in s:
       if not char.isdigit():
           return False
    return True

def is_all_upper(s):
    # check if string contins all upper case characters
    for char in s:
       if not char.isupper():
           return False
    return True

# A filter to aid in feature selection, currently unused.
# Modify this to do more sophisticated feature selection.
def featurePassesFilter(feature):

    if feature.isdigit():
        return False
    return True

# Build a dicitonary whose keys are possible values for tokens and tags,
# each of which is associated with the feature it represents.
# This is where you can add specific tokens and tags that increment
# their associated feature counts.
def buildFeatureDictionary():
    dictionary = {
        "i":"First_person_pronouns",
        "me":"First_person_pronouns",
        "my":"First_person_pronouns",
        "mine":"First_person_pronouns",
        "we":"First_person_pronouns",
        "us":"First_person_pronouns",
        "our":"First_person_pronouns",
        "ours":"First_person_pronouns",
        "you":"Second_person_pronouns",
        "your":"Second_person_pronouns",
        "yours":"Second_person_pronouns",
        "u":"Second_person_pronouns",
        "ur":"Second_person_pronouns",
        "urs":"Second_person_pronouns",
        "he":"Third_person_pronouns",
        "him":"Third_person_pronouns",
        "his":"Third_person_pronouns",
        "she":"Third_person_pronouns",
        "her":"Third_person_pronouns",
        "hers":"Third_person_pronouns",
        "it":"Third_person_pronouns",
        "its":"Third_person_pronouns",
        "they":"Third_person_pronouns",
        "them":"Third_person_pronouns",
        "their":"Third_person_pronouns",
        "theirs":"Third_person_pronouns",
        "CC": "Coordinating conjunctions",
        "VBD":"Past_tense_verbs",
        "VBN":"Past_tense_verbs",
        "’ll":"Future_tense_verbs",
        "will":"Future_tense_verbs",
        "gonna":"Future_tense_verbs",
        "won’t":"Future_tense_verbs",
        ",":"Commas",
        ":":"Colon_semi-colon_ellipsis",
        "-":"Dashes",
        "(":"Parentheses",
        ")":"Parentheses",
        "NN":"Common_nouns",
        "NNS":"Common_nouns",
        "NNP":"Proper_nouns",
        "NNPS":"Proper_nouns",
        "RB":"Adverbs", 
        "RBR":"Adverbs",  
        "RBS":"Adverbs", 
        "WDT":"Wh_words",
        "WP":"Wh_words",
        "WP$":"Wh_words",
        "WRB":"Wh_words",
        "smh":"Modern_slang_acronyms",
        "fwb":"Modern_slang_acronyms",
        "lmfao":"Modern_slang_acronyms",
        "lmao":"Modern_slang_acronyms",
        "lms":"Modern_slang_acronyms",
        "tbh":"Modern_slang_acronyms",
        "rofl":"Modern_slang_acronyms",
        "wtf":"Modern_slang_acronyms",
        "bff":"Modern_slang_acronyms",
        "wyd":"Modern_slang_acronyms",
        "lylc":"Modern_slang_acronyms",
        "brb":"Modern_slang_acronyms",
        "atm":"Modern_slang_acronyms",
        "imao":"Modern_slang_acronyms",
        "sml":"Modern_slang_acronyms",
        "btw":"Modern_slang_acronyms",
        "bw":"Modern_slang_acronyms",
        "imho":"Modern_slang_acronyms",
        "fyi":"Modern_slang_acronyms",
        "ppl":"Modern_slang_acronyms",
        "sob":"Modern_slang_acronyms",
        "ttyl":"Modern_slang_acronyms",
        "imo":"Modern_slang_acronyms",
        "ltr":"Modern_slang_acronyms",
        "thx":"Modern_slang_acronyms",
        "kk":"Modern_slang_acronyms",
        "omg":"Modern_slang_acronyms",
        "ttys":"Modern_slang_acronyms",
        "afn":"Modern_slang_acronyms",
        "bbs":"Modern_slang_acronyms",
        "cya":"Modern_slang_acronyms",
        "ez":"Modern_slang_acronyms",
        "f2f":"Modern_slang_acronyms",
        "gtr":"Modern_slang_acronyms",
        "ic":"Modern_slang_acronyms",
        "jk":"Modern_slang_acronyms",
        "k":"Modern_slang_acronyms",
        "ly":"Modern_slang_acronyms",
        "ya":"Modern_slang_acronyms",
        "nm":"Modern_slang_acronyms",
        "np":"Modern_slang_acronyms",
        "plz":"Modern_slang_acronyms",
        "ru":"Modern_slang_acronyms",
        "so":"Modern_slang_acronyms",
        "tc":"Modern_slang_acronyms",
        "tmi":"Modern_slang_acronyms",
        "ym":"Modern_slang_acronyms",
        "sol":"Modern_slang_acronyms",
        "lol":"Modern_slang_acronyms",
        "omg":"Modern_slang_acronyms",
        }
    
    return OrderedDict(sorted(dictionary.items(), key = lambda t:t[0]))

# Build a list of features that will be included in the arff file.
# This is where to add feature names if desired. Additional feature
# names shoud be added BEFORE "Average_token_length" and "Sentiment",
# which must be the last two features in the list
def buildFeatureList():

    feature_list = [
        "First_person_pronouns",
        "Second_person_pronouns",
        "Third_person_pronouns",
        "Coordinating conjunctions",
        "Past_tense_verbs",
        "Future_tense_verbs",
        "Commas",
        "Colon_semi-colon_ellipsis",
        "Dashes",
        "Parentheses",
        "Common_nouns",
        "Proper_nouns",
        "Adverbs",
        "Wh_words",
        "Modern_slang_acronyms",
        "Upper_case",
        "Average_token_length",
        "Sentiment"]
    return feature_list

# Write the arff header to the output file 
def writeArffHeader(outfile,relation_name,feature_list):

    # Write out the first line with the Relation name
    outfile.write("@RELATION " + relation_name + "\n\n")

    # Write out the feature names and their types
    for feature_name in feature_list:
        
        outfile.write("@ATTRIBUTE\t\"" + feature_name + "\"\tNUMERIC\n")

    # Write out the data header
    outfile.write("\n@DATA\n\n")
    
# Writes the feature vector for a tweet to the @DATA section of the arff file
def writeInstance(outfile,feature_list,feature_vector):

    for feature in feature_list[:-2]:
        outfile.write(str(feature_vector[feature]) + ",")
    outfile.write(str(feature_vector["Average_token_length"]) + ",")
    outfile.write(str(feature_vector["Sentiment"]) + "\n")

# Creates and initializes a new feature vector for a tweet
def createFeatureVector(feature_list):
    feature_vector = {}
    
    for feature in feature_list:
        feature_vector[feature] = 0
    return feature_vector

# Iterates through the token/tag pairs in a tweet and increments feature
# counts. 
def buildFeatureVector(data,feature_list,feature_dict):

    # Separate the sentiment indicator from the tweet's token_tag pairs
    
    sentiment = data.split('\t')[0]
    comment = data.split('\t')[1]
    
    # Get a new initialized feature vector for this tweet
    feature_vector = createFeatureVector(feature_list)
    average_token_length = 0
    number_of_words = 0
    
    # Set up a variable to enable finding the sequence "going to VB"
    going_to_VB = 0

    # Iterate over the tag_token pairs and split each pair into "tok" and "tag"
    for item in data.split():
        tok = item.split('_')[0]
        tag = item.split('_')[1]

        # Do not add punctuation to the computation of average word length
        # TODO: check that this is working as assumed
        if not (is_punct_string(tok) or tag == "CD"):
            average_token_length = average_token_length + len(tok)
            number_of_words += 1

        # An inelegant chunk of code to deal with the "going to VB" sequence.
        # Could be abstracted out into a separate function
        if (tok.lower == "going" and going_to_VB == 0) or (tok.lower == "to" and going_to_VB == 1):
            going_to_VB += 1
        elif (going_to_VB == 2 and tag == "VB"):
            feature_vector[feature_dict["Future_tense_verbs"]] += 1
            going_to_VB = 0

        # If the token or tag is in the dictionary of feature values, increment
        # the corresponding feature value in the feature vector for this tweet.
        if tok.lower() in list(feature_dict.keys()):
            feature_vector[feature_dict[tok.lower()]] += 1
        elif tag in list(feature_dict.keys()):
            feature_vector[feature_dict[tag]] += 1

        # Increment the Upper_case feature if appropriate. 
        if len(tok) > 1 and is_all_upper(tok):
            feature_vector["Upper_case"] += 1

    #fix for divide by zero error
    if number_of_words == 0:
        number_of_words = 1
            
    # Fill in the feature value for Average_token_length, rounded to the nearest integer            
    feature_vector["Average_token_length"] = round(average_token_length / number_of_words)
    # Fill in the feature value for Sentiment
    feature_vector["Sentiment"] = sentiment

    return feature_vector

# To execute this file, run the file and then enter the command buildArff() on the Python shell command line
def buildArff(inFileName):
    # Retrieve the path of the current directory (the one continaing this code)
    curdir = os.getcwd()
    # Create the path name to the input file, assumed to be in the current directory.
    # Change this to get the filename from input parameters 
    infile_name = os.path.join(curdir,"test_file.txt")
    # Output written to a file in the current directory (by default).
    # Change this to get the filename from input parameters 
    outfile_name = "comments.arff"

    # Create the dictionary of "string", "feature type" pairs, and the list of features
    feature_dict= buildFeatureDictionary()
    feature_list = buildFeatureList()

    # Open the output file and write the arff header
    outfile = open(outfile_name,"w")

    writeArffHeader(outfile,"tweets-sentiment",feature_list)

    # Read each line of the input file (assumed each is one tweet) and build
    # a vector of feature counts for the tweet, then append to the arff file
    infile = open(inFileName)
    for tweet in infile:
        feature_vector = buildFeatureVector(tweet,feature_list,feature_dict)
        writeInstance(outfile,feature_list,feature_vector)

#allow program to run from command line        
if __name__ =="__main__":
    buildArffMax(sys.argv)


