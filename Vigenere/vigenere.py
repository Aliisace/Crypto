import os, sys, string
from random import choice, randint

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#==============================================================================
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputC'mon.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputC'mon.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputTHNKSfrthMMRS.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputTHNKSfrthMMRS1.txt"
# outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputTHNKSfrthMMRS1.txt"
#==============================================================================
inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\input\\inputGirlsGirlsBoys.txt"
outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Vigenere\\outputGirlsGirlsBoys.txt"

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
    
    if mode == "Encrypt":
        encryptMessage(key, content)
    elif mode == "Decrypt":
        decryptMessage(key, content)
    
    outputFileObj = open(outputFilename, 'w')
    outputFileObj.write(str(translatedMessage(key, content, mode)))
    outputFileObj.close()
    
    
def encryptMessage(key, message):
    return translatedMessage(key, message, "Encrypt")
    
def decryptMessage(key, message):
    translation = translatedMessage(key, message, "Decrypt")
    return translation

def translatedMessage(key, message, mode):
    translated = []
    
    keyIndex = 0
    key = key.upper()
    
    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if num != -1:
            if mode == "Encrypt":
                num += LETTERS.find(key[keyIndex])
            elif mode == "Decrypt":
                num -= LETTERS.find(key[keyIndex])
            
            num %= len(LETTERS)
            
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            
            keyIndex += 1 #move to next letter of key
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting
            translated.append(symbol)
    return "".join(translated)

def getKey():
    while True:
        keyMode = input("Key mode > ").upper()
        
        if keyMode[0] == "R":
            key = "".join(choice(string.ascii_uppercase) for x in range(randint(10, 18)))
            return key
        elif keyMode[0] == "I":
            response = input("> ")
            if response.isalpha():
                key = response.upper()
                return key
            else:
                keyMode[0] = "H"
        elif keyMode[0] == "H":
            key = "CHIVALROUSNESS"
            return key
        else:
            print("For a random key press R, for a hardcoded key press H, to input a key press I")
    
def getMode():
    while True:
        print("\tVigenere Cipher")
        mode = input("mode > ").upper()
        if mode in "E D".split():
            if mode[0] == "E":
                   mode = "Encrypt"
                   return mode
            elif mode[0] == "D":
                   mode = "Decrypt"
                   return mode
        else:
            print("If you are Encrypting please press E\n If you are Decrypting please press D")

if __name__ == "__main__":
    main()