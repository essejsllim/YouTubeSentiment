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

# Building the seed sets from which we will construct a dictionary
def run(choice):
    posWords = popularAdj('finalTrainingComments.txt', 'p')
    negWords = popularAdj('finalTrainingComments.txt', 'n')
    posWords = addToSeedSets(posWords, negWords, 'cleanTaggedComments.txt', 'p')
    negWords = addToSeedSets(posWords, negWords, 'cleanTaggedComments.txt', 'n')
    overlap = {x for x in posWords if x in negWords}
    posWords = posWords - overlap
    negWords = negWords - overlap
    if choice == 'p':
        return posWords
    else:
        
        return negWords

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
            if tag == 'JJ' or tag == 'RB':
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
            try:
                word = token.split('_')[0].lower()
                tag = token.split('_')[1].lower()
            except IndexError as e:
                word = ''
                tag = ''
            if (tag == 'JJ' or tag == 'RB') and prevword == 'and' and (prevprevword in posSet):
                print(word)
                posSet.add(word.lower())
            if (tag == 'JJ' or tag == 'RB') and prevword == 'but' and (prevprevword in posSet):
                print(word)
                negSet.add(word.lower())
            if (tag == 'JJ' or tag == 'RB') and prevword == 'and' and (prevprevword in negSet):
                print(word)
                negSet.add(word.lower())
            if (tag == 'JJ' or tag == 'RB') and prevword == 'but' and (prevprevword in negSet):
                print(word)

                posSet.add(word.lower())
            prevprevword = prevword
            prevword = word
    if choice == 'p':
        return posWords
    if choice == 'n':
        return negWords

# Build a dicitonary whose keys are possible values for tokens and tags,
# each of which is associated with the feature it represents.
# This is where you can add specific tokens and tags that increment
# their associated feature counts.
posWords = {'snappy', 'favorable', 'helpfull', 'gritty', 'big', 'soothing',
            'distinctive', 'fond', 'favourite', 'bright', 'wisely', 'epicc',
            'interactive', 'kind', 'particularly', 'fancy', 'pleasurable',
            'breathtaking', 'beautiful', 'gentle',
            'excellent', 'clean', 'badass', 'dynamic', 'tough', 'finest',
            'winning-est', 'imaginative', 'knowledgable', 'enhanced', 'discreet',
            'duly', 'sound', 'freakin\'', 'stylish', 'grand', 'timeless',
            'correct', 'reasonable', 'genuinly', 'convincingly', 'thrilling',
            'concise', 'honestly', 'fricken\'', 'exponentially', 'not-douchey',
            'mindblowing', 'original', 'effective', 'overwhelming', 'respectful',
            'exotic', 'schweeet', 'durable', 'buttery', 'sturdy', 'elegant',
            'real', 'interested', 'scrumptious',
            'vivid',
            'able', 'highly', 'unreal', 'clearly', 'discrete', 'fresh',
            'competent', 'friggn\'', 'wise', 'compatible', 'cexy', 'loveable',
            'minimalistic', 'useful', 'eveeerrr', 'witty', 'comedic',
            'informative', 'incomparable', 'good', 'classy', 'speechless',
            'greatly', 'goooood', 'friendly', 'portable', 'functional',
            'appropriately', 'detailed', 'clever', 'creative', 'ultimate',
            'impressive', 'beefy', 'anti-boredom', 'effing', 'fing',
            'beautifull', 'dopeu', 'heavenly', 'precise',
            'open', 'charming', 'genuinely', 'wondefull', 'rpetty', 'crisp',
            'warm', 'worthy', 'appealing', 'eveeeeeeeeeer', 'carefree',
            'clear', 'direct', 'fkn', 'graet', 'attractive', 'audible',
            'balanced', 'fair', 'slick', 'thorough',
            'distinguised', 'hella', 'stellar', 'revolutionary', 'evocative',
            'sooooooo', 'pleasant', 'entertaining', 'powerful', 'valueable',
            'seductive', 'true', 'refreshing', 'exciting', 'insanely',
            'truthfull', 'lightweight', 'affluent', 'lucky', 'phenomenal',
            'confident', 'niiice', 'no-nonsense', 'desirable', 'capable',
            'professionally', 'tight', 'hott', 'realistic',
            'eeeeeeeever', 'quality', 'positive', 'arwsome', 'unlimited',
            'outstanding', 'hypotic', 'freak\'n', 'honest', 'factual', 'cute',
            'sultry', 'cleverly', 'nimble', 'vast', 'quick', 'treasured',
            'frickin', 'comfy', 'vibrant', 'bonerville', 'proffesional',
            'pure', 'super', 'handsome', 'fast/beautiful', 'perfectly',
            'sophisticated', 'stunningly', 'prosperous', 'accurate', 'quirky',
            'freaken', 'unbeatable', 'complete', 'smoothly', 'free-spirited',
            'intersting', 'adorable', 'easy-to-use', 'sexy', 'uber', 'pumped',
            'nicely', 'genuine', 'beutifull', 'peaceful', 'priceless',
            'inovated', 'sensual', 'qualified', 'refined', 'quickly', 'decent',
            'reliable', 'bountiful', 'hilarious', 'happy', 'responsive', 'gr8',
            'compact', 'thoroughly', 'awsome', 'advantageous', 'helful',
            'also-good', 'legit', 'top', 'satisfied', 'mature', 'talented',
            'customizable', 'excited', 'flawless', 'attractive', 'valuable',
            'superbly', 'productive', 'fast', 'unique', 'comfortable', 'cool',
            'remarkable', 'gently', 'pretty', 'stable', 'incredibly', 'healthy',
            'reassuring', 'usefull', 'superb', 'tremendously', 'convenient',
            'beautifully', 'fierce', 'beutiful', 'pleased', 'affordable', 'epic',
            'comprehensive', 'jolly', 'forgiving', 'understated', 'delicious',
            'sick', 'highest', 'best-in-class', 'passionated',
            'aaawwwweeeessssooommmeeelllyyyyy', 'posh', 'brilliantly',
            'amazingly', 'orgasmic', 'glorious', 'inspiring', 'interesting',
            'great', 'beatiful', 'beaut', 'favorite', 'gorgeous', 'hysterical',
            'focused', 'upbeat', 'rugged', 'happily', 'freaaaaakiiiinnnngggg',
            'efficient', 'advanced', 'superior', 'underated', 'unmatched',
            'perfect', 'superior/high', 'successful', 'extensive', 'safe',
            'engaging', 'fav', 'magnificent', 'innovative', 'strong', 'excelent',
            'addictive', 'unbiased', 'georgeous', 'groovy', 'luxurious',
            'credible', 'sweet', 'classic', 'underrated', 'desired',
            'well-spoken', 'intelligent', 'knowledgeable', 'stunning',
            'dedicated', 'sik', 'wonderful', 'gooooood', 'sleek', 'consistently',
            'welcome', 'proud', 'versatile', 'awsme', 'appropriate',
            'fiiiinnnnneeee', 'funny', 'freaking', 'unbreakable', 'unparalleled',
            'enjoyable', 'psyched', 'awesome-30', 'professional', 'fun',
            'fine-tuned', 'gooood', 'amazing', 'poignant', 'phenominal',
            'splending', 'catchy', 'slim', 'dope', 'hottt', 'ridic', 'awesome',
            'promising', 'incredible', 'easy', 'gorgous', 'amaziin', 'neat',
            'desireable', 'relatable', 'brilliant', 'sharp', 'tasty',
            'best-looking', 'stoked', 'solid', 'faster', 'intuitive',
            'sufficient', 'fantastic', 'lovely', 'lean', 'magical', 'sexxy',
            'nice', 'smooth', 'prefect', 'ergonomic'}

negWords = {'costly', 'faulty', 'weird', 'pointless', 'freaking', 'raging',
            'worst:\'(', 'misleading', 'slowly', 'over-priced', 'clumsy', 'painful',
            'sluggish', 'fckin', 'awkward',
            'boooooooooooooooooooooooooooooooooooooring', 'false', 'hard',
            'predictable', 'overrated', 'freaken', 'inferior', 'disposable', 'cheezy',
            'pathetically', 'silly', 'unfocused', 'uneven', 'ass', 'stupid', 'horrific',
            'cheesy', 'unbalanced', 'fucken', 'garbled', 'petty', 'uninformed',
            'unwatchable', 'untrue', 'retarded', 'uncouth', 'creepy', 'twisted', 'desperately',
            'filthy', 'immature', 'badly', 'inane', 'lazy', 'mediocre', 'antiquated',
            'crappy', 'dumb', 'gay', 'rubbish', 'boring', 'clunky', 'suspicious',
            'rubbbbbiisshh', 'ugly', 'inconvenient', 'miserably', 'obscene', 'damaging',
            'shoddy', 'reckless', 'nasty', 'uncomfortably', 'weak', 'declining', 'slow', 'fugly',
            'naive', 'outdated', 'weepy', 'terrible', 'foolish', 'characterless', 'dirty',
            'intrusive', 'fake', 'backward', 'low-quality', 'disabled', 'stale', 'disgusting',
            'angry', 'illiterate', 'awkwardly', 'poorly', 'lacklustre', 'stained', 'stupidest',
            'fing', 'lame', 'painfully', 'usless', 'unfortunately', 'backwards', 'trashy',
            'frigging', 'rude', 'crass', 'evil', 'f**king', 'pissed', 'inexcusable',
            'disappointing', 'repulsive', 'useless', 'terrifying', 'messy', 'ignorant',
            'uncomfortable', 'unacceptable', 'agry', 'ashamed', 'defective', 'old',
            'tempermental', 'bogus', 'fucking', 'horribly', 'unfinished', 'godforsaken',
            'unhappy', 'bored', 'shameful', 'childish', 'corny', 'negatively', 'dangerous',
            'contrarian', 'flawed', 'skittish', 'appalling', 'plasticky',
            'shitty-plastic-choppy-complete-copies-of-apple\'-ideas-competition', 'grainy',
            'crippled', 'stupdily', 'baaaddd', 'lackluster', 'misinformed', 'freackn', 'greedy',
            'anti-ergonomic', 'unfortunate', 'horrible', 'sad', 'alas', 'vile', 'dead',
            'pathetic', 'fricken', 'brutal', 'unplayable', 'lumpy', 'infested', 'gawky', 'uneducated',
            'boooooring', 'powerless', 'glitchy', 'broke', 'droll', 'bankrupt', 'friendless',
            'frustratingly', 'overgrown', 'painfull', 'lousy', 'fat',' irrelevant', 'disturbed',
            'faulty/completely', 'talentless', 'irrational', 'unprofessional', 'unfortunatly',
            'sadly', 'fukin', 'sorry', 'bumpy', 'redundant', 'bloated', 'shameless', 'flimsy',
            'farcical', 'superficial', 'despicable', 'idiotic', 'laggy', 'spotty',
            'uuuuuuggggglllllyyyy', 'rotten', 'worthless', 'biased', 'sick', 'inoperable',
            'annoying', 'awful', 'negative', 'gross', 'imperfect', 'bad', 'dumn', 'cramped',
            'unresponsive', 'overpriced', 'boooringg', 'gayyyy', 'freakin', 'tacky', 'unusable',
            'pretentious', 'spoiled', 'tawdry', 'cumbersome', 'illegal', 'sloowwww', 'tinny',
            'embarrassing', 'dull', 'blurry', 'twat', 'friggin', 'incorrect', 'bitchy',
            'unbearable', 'fuckin', 'out-dated', 'fragile', 'impractical', 'upset', 'bland',
            'stinking', 'out-of-date', 'icky', 'fuckign', 'effin', 'difficult', 'jealous',
            'starved', 'desperate', 'hideous', 'depressing', 'noisy', 'scared',
            'shamelessly', 'absurd', 'embarassing', 'scary', 'gimmicky', 'obese', 'worst',
            'choppy', 'unfair', 'poor', 'failed', 'dissapointing', 'mushy', 'deffective',
            'unreliable', 'unsuccessful', 'nt', 'anoying', 'problematic', 'crapy', 'shitty',
            'broken', 'ancient', 'whiny'}

print(len(posWords))
print(len(negWords))
overlap = {x for x in posWords if x in negWords}
posWords = posWords - overlap
negWords = negWords - overlap
print(len(posWords))
print(len(negWords))
posWords = addToSeedSets(posWords, negWords, '/home/jemills/cs366/Final_Project/Testing Corpus/thirdStageComments.txt', 'p')
negWords = addToSeedSets(posWords, negWords, '/home/jemills/cs366/Final_Project/Testing Corpus/thirdStageComments.txt', 'n')
print(len(posWords))
print(len(negWords))
overlap = {x for x in posWords if x in negWords}
posWords = posWords - overlap
negWords = negWords - overlap
print(len(posWords))
print(len(negWords))

def buildFeatureDictionary():
    dictionary = {}
    for word in posWords:
        key = {word:'Pos_words'}
        dictionary.update(key)
    for word in negWords:
        key = {word:'Neg_words'}
        dictionary.update(key)
    
    return OrderedDict(sorted(dictionary.items(), key = lambda t:t[0]))

# Build a list of features that will be included in the arff file.
# This is where to add feature names if desired. Additional feature
# names shoud be added BEFORE "Average_token_length" and "Sentiment",
# which must be the last two features in the list
def buildFeatureList():

    feature_list = [
        "Pos_words",
        "Neg_words",
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
    for item in comment.split():
        try:
            tok = item.split('_')[0]
            tag = item.split('_')[1]
        except IndexError as e:
            tok = ''
            tag = ''
            print(e)

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
def buildArff():
    # Retrieve the path of the current directory (the one continaing this code)
    curdir = os.getcwd()
    # Create the path name to the input file, assumed to be in the current directory.
    # Change this to get the filename from input parameters 
    #infile_name = os.path.join(curdir,"finalTrainingComments.txt")
    infile_name = '/home/jemills/cs366/Final_Project/Testing Corpus/Training Data/finalData.txt'
    # Output written to a file in the current directory (by default).
    # Change this to get the filename from input parameters 
    outfile_name = "comments.arff"

    # Create the dictionary of "string", "feature type" pairs, and the list of features
    feature_dict= buildFeatureDictionary()
    feature_list = buildFeatureList()

    # Open the output file and write the arff header
    outfile = open(outfile_name,"w")

    writeArffHeader(outfile,"comments-sentiment",feature_list)

    # Read each line of the input file (assumed each is one tweet) and build
    # a vector of feature counts for the tweet, then append to the arff file
    infile = open(infile_name)
    for tweet in infile:
        feature_vector = buildFeatureVector(tweet,feature_list,feature_dict)
        writeInstance(outfile,feature_list,feature_vector)

#allow program to run from command line        
if __name__ =="__main__":
    buildArff()


