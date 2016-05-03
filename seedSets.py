import math
posWords = {'snappy', 'favorable', 'helpfull', 'gritty', 'soothing',
            'distinctive', 'fond', 'favourite', 'bright', 'wisely', 'epicc',
            'interactive', 'kind', 'particularly', 'fancy', 'pleasurable',
            'breathtaking', 'beautiful', 'sooooooooo', 'gentle', 'faaaaaaaar',
            'excellent', 'clean', 'badass', 'dynamic', 'tough', 'finest',
            'winning-est', 'imaginative', 'knowledgable', 'enhanced', 'discreet',
            'duly', 'sound', 'freakin\'', 'stylish', 'grand', 'timeless',
            'correct', 'reasonable', 'genuinly', 'convincingly', 'thrilling',
            'concise', 'honestly', 'fricken\'', 'exponentially', 'not-douchey',
            'mindblowing', 'original', 'effective', 'overwhelming', 'respectful',
            'exotic', 'schweeet', 'durable', 'buttery', 'sturdy', 'elegant',
            'real', 'interested', 'scrumptious',
            'sooooooooooooooooooooooooooooooooooooooooooooooooooooooo', 'vivid',
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
            'balanced', 'fair', 'sooooooooooo', 'slick', 'thorough',
            'distinguised', 'hella', 'stellar', 'revolutionary', 'evocative',
            'sooooooo', 'pleasant', 'entertaining', 'powerful', 'valueable',
            'seductive', 'true', 'refreshing', 'exciting', 'insanely',
            'truthfull', 'lightweight', 'affluent', 'lucky', 'phenomenal',
            'confident', 'niiice', 'no-nonsense', 'desirable', 'capable',
            'professionally', 'tight', 'soooooooooooo', 'hott', 'realistic',
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
            'broken', 'ancient'}

def sentiment(filename):
    file = open(filename, 'r')
    numTotal = 0
    numCorrect = 0
    for line in file:
        numPos = 0
        numNeg = 0
        lineSent = ''
        sent = line.split('\t')[0]
        #print(sent)
        comment = line.split('\t')[1]
        tokenList = comment.split(' ')
        for token in tokenList:
            try:
                word = token.split('_')[0]
                tag = token.split('_')[1]
            except IndexError as e:
                tok = ''
                tag = ''
            if word in posWords:
                numPos+=1
            if word in negWords:
                numNeg+=1
        if numPos > numNeg:
            print(line)
            print(numPos)
            print(numNeg)
            lineSent = ' "1 "'
        if numNeg > numPos:
            lineSent = ' "-1 "'
        else:
            lineSent = ' "0 "'
        if lineSent == sent:
            numCorrect+=1
            #print(lineSent)
        numTotal +=1
    print(numCorrect/numTotal)
            

dictionary = {
        "great":"Pos_words",
        "happy":"Pos_words",
        "fantastic":"Pos_words",
        "wonderful":"Pos_words",
        "beautfiful":"Pos_words",
        "glad":"Pos_words",
        "best":"Pos_words",
        "awesome":"Pos_words",
        "love":"Pos_words",
        "ftw":"Pos_words",
        "outstanding":"Pos_words",
        "classy":"Pos_words",
        "clever":"Pos_words",
        "famous":"Pos_words",
        "intelligent":"Pos_words",
        "remarkable":"Pos_words",
        "reputed":"Pos_words",
        "classy":"Pos_words",
        "thriving":"Pos_words",
        "stupid":"Neg_words",
        "pointless":"Neg_words",
        "boring":"Neg_words",
        "fake":"Neg_words",
        "sucks":"Neg_words",
        "douche":"Neg_words",
        "racist":"Neg_words",
        "waste":"Neg_words",
        "idiot":"Neg_words",
        "contagious":"Neg_words",
        "drunken":"Neg_words",
        "ignorant":"Neg_words",
        "lanky":"Neg_words",
        "listless":"Neg_words",
        "primitive":"Neg_words",
        "strident":"Neg_words",
        "troublesome":"Neg_words",
        "unresolved":"Neg_words",
        "shitty":"Neg_words"
        }
