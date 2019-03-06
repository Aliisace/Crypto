import sys, copy, cryptoMaths, random

SYMBOLS = """ !"#$%&"()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\] ^_`abcdefghijklmnopqrstuvwxyz{|}~""" # note the space at the front

def main():
    mode = getMode()
    key = 2023
    message = getMessage()
    
    if mode[0] == "E":
        mode = "Encrypt"
        translated = encryptMessage(key, message)
    elif mode[0] == "D":
        mode = "Decrypt"
        translated = decryptMessage(key, message)
    print("Key: %s" % (key))
    print("%sed text:" % (mode.title()))
    print(translated)
    copy.deepcopy(translated)
    print("Full %sed text copied to clipboard." % (mode))

def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return (keyA, keyB)

def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == "encrypt":
        sys.exit("The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.")
    
    if keyB == 0 and mode == "encrypt":
        sys.exit("The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.")
    
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        sys.exit("Key A must be greater than 0 and Key B must be between 0 and %s." % (len(SYMBOLS) - 1))
    
    if cryptoMaths.gcd(keyA, len(SYMBOLS)) != 1:
        sys.exit("Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key." % (keyA, len(SYMBOLS)))
    
def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, "encrypt")
    ciphertext = ""
    for symbol in message:
        if symbol in SYMBOLS:
            # encrypt this symbol
            symIndex = SYMBOLS.find(symbol)
            ciphertext += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            ciphertext += symbol # just append this symbol unencrypted
    return ciphertext

def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, "decrypt")
    plaintext = ""
    modInverseOfKeyA = cryptoMaths.findModInverse(keyA, len(SYMBOLS))
    
    for symbol in message:
        if symbol in SYMBOLS:
            # this symbol
            symIndex = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
        else:
            plaintext += symbol # just append this symbol undecrypted
    return plaintext

def getRandomKey():
    while True:
        keyA = random.randint(2, len(SYMBOLS))
        keyB = random.randint(2, len(SYMBOLS))
        if cryptoMaths.gcd(keyA, len(SYMBOLS)) == 1:
            return keyA * len(SYMBOLS) + keyB

def getMode():
    while True:
        print("\tAffine Cipher")
        mode = input().upper()
        if mode in "E D".split():
            if mode[0] == "E":
                   return mode
            elif mode[0] == "D":
                   return mode
        else:
            print("If you are Encrypting please press E\n If you are Decrypting please press D")
       
def getMessage():
    print("Please enter your message for translation")
    return input()

if __name__ == "__main__":
    main()