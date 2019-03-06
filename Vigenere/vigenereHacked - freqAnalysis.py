import itertools, re, os, sys
import vigenere, frequencyFinder, detectEnglish

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SILENT_MODE = False # if set to True, program doesn't print attempts
NUM_MOST_FREQ_LETTERS = 4 # attempts this many letters per subkey
MAX_KEY_LENGTH = 18 # will not attempt keys longer than this
NONLETTERS_PATTERN = re.compile("[^A-Z]")

#==============================================================================
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputC'mon.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputC'mon - Frequency hacked.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS - Frequency hacked.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS1.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS1 - Frequency hacked.txt"
#==============================================================================
inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputGirlsGirlsBoys.txt"
outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputGirlsGirlsBoys - Frequency hacked.txt"


def main():
    if not os.path.exists(inputFilename):
        print("Input file %s does not exist\nQuit" %(inputFilename))
        sys.exit()
   
    if os.path.exists(outputFilename):
        print("This will over write the output file %s. (C)ontinue or (Q)uit" %(outputFilename))
        response = input("> ")
        if not response.lower().startswith("c"):
            sys.exit()
    
    fileObj = open(inputFilename)
    ciphertext = fileObj.read()
    fileObj.close()
    
    hackedMessage = hackVigenere(ciphertext)
    
    if hackedMessage != None:
        print("Writing hacked message to file")
        outputFileObj = open(outputFilename, 'w')
        outputFileObj.write(str(hackedMessage))
        outputFileObj.close()
        print("Message written to file")
    else:
        print("failed to hack encryption")
    
def findRepeatSequencesSpacings(content):
    # Goes through the message and finds any 3 to 5 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).
    
    # use a egular expression to remove non-letters from the message.
    content = NONLETTERS_PATTERN.sub("", content.upper())
    
    # compile list of seqLen-letter sequences found in the message.
    seqSpacings = {} #keys are sequences, values found are list of int spaces
    for seqLen in range(3, 6):
        for seqStart in range(len(content) - seqLen):
            # Determine what the sequence is, and store it in seq
            seq = content[seqStart:seqStart + seqLen]
            
            # Look for this sequence in the rest of the message
            for i in range(seqStart + seqLen, len(content) - seqLen):
                if content[i:i + seqLen] == seq:
                    # Found a repeated sequence.
                    if seq not in seqSpacings:
                       seqSpacings[seq] = [] # initialise blank list

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence.
                    seqSpacings[seq].append(i - seqStart)
                    
    return seqSpacings

def getUsefulFactors(num):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1. For example, getUsefulFactors(144)
    # returns [2, 72, 3, 48, 4, 36, 6, 24, 8, 18, 9, 16, 12]
    
    if num < 2:
        return [] # numbers less than 2 have no useful factors
    
    factors = [] # list of factors found

    # when finding factors, you only need to check the interegers up to MAX_KEY_LENGTH
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))
    if 1 in factors:
        factors.remove(1)
    return list(set(factors))

def getItemAtIndexOne(x):
    return x[1]

def getMostCommonFactors(seqFactors):
    # First, get a count of how many times a factor occurs in seqFactors.
    factorCounts = {} # key is a factor, value is how often if occurs
    
    # seqFactors keys are sequences, values are lists of factors of the spacings.
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0

    # Second, put the factor and its count into a tuple, and make a list of these tuples so we can sort them.
    factorsByCount = []
    for factor in factorCounts:
        # exclude factors larger than MAX_KEY_LENGTH
        if factor <= MAX_KEY_LENGTH:
            # factorsByCount is a list of tuples: (factor, factorCount)
            # factorsByCount has a value like: [(3, 497), (2, 487), ...]
            factorsByCount.append( (factor, factorCounts[factor]) )
    
    # Sort the list by the factor count.
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)
    
    return factorsByCount

def kasiskiExamination(ciphertext):
    # Find out the sequences of 3 to 5 letters that occur multiple times
    # in the ciphertext. repeatedSeqSpacings has a value like:
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)
    
    # See getMostCommonFactors() for a description of seqFactors.
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))
    
    # See getMostCommonFactors() for a description of factorsByCount.
    factorsByCount = getMostCommonFactors(seqFactors)
    
    # Now we extract the factor counts from factorsByCount and 
    # put them in allLikelyKeyLengths so that they are easier to use later.
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])
    
    return allLikelyKeyLengths

def getNthSubkeyLetters(n, keyLength, content):
    # Returns every Nth letter for each keyLength set of letters in text.
    
    # Use a regular expression to remove non-letters from the message.
    content = NONLETTERS_PATTERN.sub("", content)
    
    i = n - 1
    letters = []
    while i < len(content):
        letters.append(content[i])
        i += keyLength
    return "".join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # determines the most likely letters for each letter in the key.
    
    ciphertextUp = ciphertext.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # These inner lists are the freqScores lists.
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeyLetters(nth, mostLikelyKeyLength, ciphertextUp)
        
        # freqScores is a list of tuples
        # List is sorted by match score. Higher score means better match.
        freqScores = []
        for possibleKey in LETTERS:
            decryptText = vigenere.decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, frequencyFinder.englishFreqMatchScore(decryptText))
            freqScores.append(keyAndFreqMatchTuple)
        # Sort by match score
        freqScores.sort(key=getItemAtIndexOne, reverse = True)
        
        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])
        
    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            print("Possible letters for letter %s of the key: " % (i + 1), end="")
            
            for freqScore in allFreqScores[i]:
                print("%s " % freqScore[0], end="")
            print()
            
    # Try every combination of the most likely letters for each position in the key.
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat = mostLikelyKeyLength):
        # Create a possible key from the letters in allFreqScores

        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]
        
        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))
            
        decryptedText = vigenere.decryptMessage(possibleKey, ciphertextUp)
        
        if detectEnglish.isEnglish(decryptedText):
            # Set the hacked cipher text to the original casing
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = "".join(origCase)
            
            # Check with user to see if the key has been found.
            print("Possible encryption hack with key %s:" % (possibleKey))
            print(decryptedText[:200]) # only show first 200 characters
            print()
            print("Enter D for done, or just press Enter to continue hacking:")
            response = input("> ")

            if response.strip().upper().startswith("D"):
                return decryptedText

    # No English-looking decryption found, so return None.
    return None

def hackVigenere(ciphertext):
    # First, we need to do Kasiski Examination to figure out what the
    # length of the ciphertext's encryption key is.
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ""
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += "%s " % (keyLength)
        print("Kasiski Examination results say the most likely key lengths are: " + keyLengthStr + "\n")
            
    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print("Attempting hack with key length %s (%s possible keys)..." % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break
    # If none of the key lengths we found using Kasiski Examination
    # worked, start brute-forcing through key lengths.
    if hackedMessage == None:
        if not SILENT_MODE:
            print("Unable to hack message with likely key length(s). Brute-forcing key length...")
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # don't re-check key lengths already tried from Kasiski
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print("Attempting hack with key length %s (%s possible keys)..." % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage != None:
                    break
    return hackedMessage

if __name__ == "__main__":
    main()