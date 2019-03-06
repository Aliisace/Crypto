import os, sys, detectEnglish, vigenere

#==============================================================================
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputC'mon.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputC'mon - dictionary hacked.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS - dictionary hacked.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS1.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS1 - dictionary hacked.txt"
#==============================================================================
inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputGirlsGirlsBoys.txt"
outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputGirlsGirlsBoys - dictionary hacked.txt"


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
    content = fileObj.read()
    fileObj.close()

   
    hackedMessage = hackVigenere(content)
    
    if hackedMessage != None:
        print("Writing hacked message to file")
        outputFileObj = open(outputFilename, 'w')
        outputFileObj.write(str(hackedMessage))
        outputFileObj.close()
        print("Message written to file")
    else:
        print("Failed to decrypt message")

def hackVigenere(ciphertext):
    wordNumber = 1
    
    fo = open("C:\\Users\\theka\\Desktop\\Crypto\\Input\\dictionary.txt")
    words = fo.readlines()
    fo.close()
    
    print("Attempting dictionary decryption")
    
    for word in words:
        print(str(wordNumber))
        word = word.strip()
        decryptedText = vigenere.decryptMessage(word, ciphertext)
        if detectEnglish.isEnglish(decryptedText, wordPercentage = 40):
            print()
            print("Possible encryption break:")
            print()
            print("key" + str(word) + ": " + decryptedText[:100])
            print("Enter ""D"" for done, or hit enter to continue")
            
            response = input("> ")
            
            if response.upper().startswith("D"):
                return decryptedText
        wordNumber += 1
            
if __name__ == "__main__":
    main()