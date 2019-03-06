MAX_KEY_SIZE = 26

def getMode():
    while True:
        print("\tCaesar Cipher with Brutus Force" u"\u2122")
        mode = input().upper()
        if mode in "E D B".split():
            return mode[0]
        else:
            print("If you are Encrypting please press E\n If you are Decrypting please press D\n If you are using Brutus Force" u"\u2122" " please press B")
            
def main():
    LineNumber = 0
    mode = getMode()
    
    if mode[0] != "B":
        key = getKey()
    
    inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputTHNKSfrthMMRS.txt"
    outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\CaesarCipher\\Caesar\\outputTHNKSfrthMMRS.txt"
    # Write out the translated message to the output file:
    with open(inputFilename, 'r') as inputFileObj, open(outputFilename, 'w') as outputFileObj:
        for line in inputFileObj.readlines():
            if mode[0] != "B":
                outputFileObj.write(str(LineNumber) + " " + str(key) + " " + getTranslatedMessage(mode, line.rstrip(), key) + "\n")
            else:
                for key in range(1, MAX_KEY_SIZE + 1):
                    outputFileObj.write(str(LineNumber) + " " + str(key) + " " + getTranslatedMessage("Decrypt", line.rstrip(), key) + "\n")
            LineNumber += 1
        pass
    outputFileObj.close()
    inputFileObj.close()

def getKey():
    key = 0
    while True:
        print("Enter the key number (1-%s)" % (MAX_KEY_SIZE))
        key = int(input())
        if (key >= 1 and key <= MAX_KEY_SIZE):
            return key 

def getTranslatedMessage(mode, message, key):
    if mode[0] == "D":
        key = -key
    translated = ""
    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key            
            if symbol.isupper():
                if num > ord("Z"):
                    num -= 26
                elif num < ord("A"):
                    num += 26
            elif symbol.islower():
                if num > ord("z"):
                    num -= 26
                elif num < ord("a"):
                    num += 26          
            translated += chr(num)
        else:
            translated += symbol
    return translated

# If transpositionCipherFile.py is run (instead of imported as a module),
# call the main() function:
if __name__ == '__main__':
    main()
    
