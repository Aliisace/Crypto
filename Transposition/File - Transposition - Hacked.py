import time, os, sys, detectEnglish, transpositionDecrypt

inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Transposition\\outputC'mon.txt"
outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Transposition\\outputC'monhacked.txt"
#==============================================================================
#     inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\outputTHNKSfrthMMRS.txt"
#     outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Transposition\\outputTHNKSfrthMMRShacked.txt"
#     inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\outputTHNKSfrthMMRS1.txt"
#     outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Transposition\\outputTHNKSfrthMMRS1hacked.txt"
#==============================================================================


def main():
    if not os.path.exists(inputFilename):
        print("Input file %s does not exist\nQuit" %(inputFilename))
        sys.exit()
   
    if os.path.exists(outputFilename):
        print("This will over write the output file %s. (C)ontinue or (Q)uit" %(outputFilename))
        response = input("> ")
        if not response.lower().startswith("c"):
            sys.exit()
    
    inputFile = open(inputFilename)
    content = inputFile.read()
    inputFile.close()
    
    hackedMessage = hackTransposition(content)
    
    if hackedMessage != None:
        print("Writing decrypted text to %s." %(outputFilename))
        
        outputFile = open(outputFilename, "w")
        outputFile.write(hackedMessage)
        outputFile.close()
    else:
        print("Failed to hack encryption")
        
def hackTransposition(message):
    print("Hacking...")
    print("(Press Ctrl-C to quit at any time)")
    
    for key in range(1, len(message)*2):
        print("Trying key #%s" %(key), end=" ")
        sys.stdout.flush()
        
        startTime = time.time()
        
        decryptedText = transpositionDecrypt.decryptMessage(key, message)
        englishPercentage = round(detectEnglish.getEnglishCount(decryptedText) * 100, 5)
        
        totalTime = round(time.time() - startTime, 3)
        print("Test time: %s seconds, " % (totalTime), end="")
        sys.stdout.flush() # Flush printed text to the screen.

        print("Percent English: %s%%" % (englishPercentage))
        if englishPercentage > 20:
            print()
            print("Key " + str(key) + ": " + decryptedText[:100])
            print()
            print("Enter D if done, anything else to continue hacking:")
            response = input("> ")
            if response.strip().upper().startswith("D"):
                return decryptedText
    return None


if __name__ == "__main__":
    main()