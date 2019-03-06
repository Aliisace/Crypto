import sys, os, math

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputC'mon.txt"
outputFilenamePub = "C:\\Users\\theka\\Desktop\\Crypto\\RSA Cipher\\outputC'monPub.txt"
outputFilenamePriv = "C:\\Users\\theka\\Desktop\\Crypto\\RSA Cipher\\outputC'monPriv.txt"
# =============================================================================
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputTHNKSfrthMMRS.txt"
# outputFilenamePub = "C:\\Users\\theka\\Desktop\\Crypto\\RSA Cipher\\outputTHNKSfrthMMRSPub.txt"
# outputFilenamePriv = "C:\\Users\\theka\\Desktop\\Crypto\\RSA Cipher\\outputTHNKSfrthMMRSPriv.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\Input\\inputTHNKSfrthMMRS1.txt"
# outputFilenamePub = "C:\\Users\\theka\\Desktop\\Crypto\\RSA Cipher\\outputTHNKSfrthMMRS1Pub.txt"
# outputFilenamePriv = "C:\\Users\\theka\\Desktop\\Crypto\\RSA Cipher\\outputTHNKSfrthMMRS1Priv.txt"
# inputFilename = "C:\\Users\\theka\\Desktop\\Crypto\\input\\inputGirlsGirlsBoys.txt"
# outputFilenamePub = "C:\\Users\\theka\\Desktop\\Crypto\\RSA Cipher\\outputGirlsGirlsBoysPub.txt"
# outputFilenamePriv = "C:\\Users\\theka\\Desktop\\Crypto\\RSA Cipher\\outputGirlsGirlsBoysPriv.txt"
# =============================================================================

def main():
#    mode = "Encrypt"
#    mode = "Decrypt"
    mode = getMode()

    if mode == "Encrypt":
        fileObj = open(inputFilename)
        message = fileObj.read()
        fileObj.close()

        if not os.path.exists(inputFilename):
            print("Input file %s does not exist\nQuit" %(inputFilename))
            sys.exit()

        if os.path.exists(outputFilenamePub):
            print("This will over write the output file %s. (C)ontinue or (Q)uit" %(outputFilenamePub))
            response = input("> ")
            if not response.lower().startswith("c"):
                sys.exit()

        pubKeyFilename = "abc_pub.txt"
        print("Encrypting and writing to %s..." % (outputFilenamePub))

        encryptedText = encryptAndWriteToFile(inputFilename, pubKeyFilename, message, outputFilenamePub)
        print("Writing to encrypted output file")

        outputFileObj = open(outputFilenamePub, 'w')
        outputFileObj.write(str(encryptedText))
        outputFileObj.close()

        print("Encrypted File: " + outputFilenamePub)

    elif mode == "Decrypt":
        if not os.path.exists(outputFilenamePub):
            print("Input file %s does not exist\nQuit" %(inputFilename))
            sys.exit()

        if os.path.exists(outputFilenamePriv):
            print("This will over write the output file %s. (C)ontinue or (Q)uit" %(outputFilenamePriv))
            response = input("> ")
            if not response.lower().startswith("c"):
                sys.exit()

        privKeyFilename = "abc_priv.txt"
        print("Decrypting and writing to %s..." % (outputFilenamePriv))
        decryptedText = readFromFileAndDecrypt(outputFilenamePub, privKeyFilename)

        print("Writing to decrypted pub key file")

        outputFileObj = open(outputFilenamePriv, 'w')
        outputFileObj.write(str(decryptedText))
        outputFileObj.close()

        print("Decrypted File: " + outputFilenamePriv)


def getBlocksFromText(message, blockSize):
    # Converts a string message to a list of block integers

    message = removeNonLetters(message)

    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        # Calculate the block integer for this block of text:
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))):
            blockInt += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize):
    #  Converts a list of block integers to the original message string.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                # Decode the message string for the 128 (or whatever
                # blockSize is set to) characters from this block integer:
                charIndex = blockInt // (len(SYMBOLS) ** i)
                blockInt = blockInt % (len(SYMBOLS) ** i)
                blockMessage.insert(0, SYMBOLS[charIndex])
        message.extend(blockMessage)
    return ''.join(message)

def encryptMessage(message, key, blockSize):
    # Converts the message string into a list of block integers,
    # and then encrypts each block integer. Pass the PUBLIC key to encrypt.
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # ciphertext = plaintext ^ e mod n
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks

def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n,e) or (n,d) tuple value.

    if not os.path.exists(keyFilename):
        print("Input file %s does not exist\nQuit" %(keyFilename))
        sys.exit()

    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, outputFilenamePub, blockSize=None):
    # Using a key from a key file, encrypt the message
    # and save it to a file. Returns the encrypted message string.
    keySize, n, e = readKeyFile(keyFilename)
    if blockSize == None:
        # If blockSize is not given, set it to the largest size allowed by the key size and symbol set size.
        blockSize = int(math.log(2 ** keySize, len(SYMBOLS)))
    # Check that key size is large enough for the block size:
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit("ERROR: Block size is too large for the key and symbol file. Did you specify the correct key file and encrypted file??")
    # Encrypt the message
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    # Convert the large int values to one string value:
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ",".join(encryptedBlocks)
    # Write out the encrypted string to the output file:
    encryptedContent = "%s_%s_%s" % (len(message), blockSize, encryptedContent)
    fo = open(outputFilenamePub, 'w')
    fo.write(encryptedContent)
    fo.close()
    # Also return the encrypted string
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    keySize, n, d = readKeyFile(keyFilename)

    # read in the message length and the encrypted message from the file:
    fo = open(messageFilename)
    content = fo.read()
    fo.close()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(float(blockSize))

    # check that the key size is not to big for the block size
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit("ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?")

    # Convert the encrypted message into large blocks
    encryptedBlocks = []
    for block in encryptedMessage.split(","):
        encryptedBlocks.append(int(block))

    # Decrypt the large int values
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)


def getMode():
    while True:
        print("\tRSACipher Cipher")
        mode = input("mode > ").upper()
        if mode in "E D Q".split():
            if mode[0] == "E":
                   mode = "Encrypt"
                   return mode
            elif mode[0] == "D":
                   mode = "Decrypt"
                   return mode
            elif mode[0] == "Q":
                sys.exit()
        else:
            print("If you are Encrypting please press E\n If you are Decrypting please press D")


def removeNonLetters(message):
    lettersOnly = []
    for symbol in message:
        if symbol in SYMBOLS:
            lettersOnly.append(symbol)
    message = ''.join(lettersOnly)
    return message


if __name__ == "__main__":
    main()