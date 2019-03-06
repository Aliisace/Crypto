MAX_KEY_SIZE = 26

print("\tCaesar Cipher with Brutus Force" u"\u2122")

def main():
    LineNumber = 0
    inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputTHNKSfrthMMRS.txt"
    # BE CAREFUL! If a file with the outputFilename name already exists,
    # this program will overwrite that file:
    outputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\CaesarCipher\\Caesar\\outputTHNKSfrthMMRSb.txt"
    # Write out the translated message to the output file:
    with open(inputFilename, 'r') as inputFileObj, open(outputFilename, 'w') as outputFileObj:
        for line in inputFileObj.readlines():
            for key in range(1, MAX_KEY_SIZE + 1):
                outputFileObj.write(str(LineNumber) + " " + str(key) + " " + getTranslatedMessage("Decrypt", line.rstrip(), key) + "\n")
            LineNumber += 1
        pass
    outputFileObj.close()
    
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