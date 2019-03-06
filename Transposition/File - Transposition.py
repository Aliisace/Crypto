import time, os, sys, transpositionEncrypt, transpositionDecrypt

inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputC'mon.txt"
outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Transposition\\outputC'mon.txt"
#==============================================================================
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputTHNKSfrthMMRS.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Transposition\\outputTHNKSfrthMMRS.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputTHNKSfrthMMRS1.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Transposition\\outputTHNKSfrthMMRS1.txt"
#==============================================================================

def main():
    
    mode = getMode()
    key = getKey()
    
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
    
    print("%sing" %(mode.title()))
    
    startTime = time.time()
    if mode[0] == "E":
        translated = transpositionEncrypt.encryptMessage(key, content)
    elif mode[0] == "D":
        translated == transpositionDecrypt.decryptMessage(key, content)
    totalTime = round(time.time() - startTime, 2)
    print("%sion time: % seconds" % (mode.title(), totalTime))
    
    outputFileObj = open(outputFilename, "w")
    outputFileObj.write(translated)
    outputFileObj.close()
    
    print('Done %sing %s (%s characters).' % (mode, inputFilename, len(content)))
    print("%sed file is %s" %(mode.title(), outputFilename))

def getMode():
    while True:
        print("\tTransposition Cipher")
        mode = input().upper()
        if mode in "E D".split():
            if mode[0] == "E":
                   mode = "Encryption"
                   return mode
            elif mode[0] == "D":
                   mode = "Decryption"
                   return mode
        else:
            print("If you are Encrypting please press E\n If you are Decrypting please press D")

def getKey():
    key = 0
    while True:
        print("Enter the key number: ")
        key = int(input())
        if (key >= 1):
            return key 
        
if __name__ == '__main__':
    main()