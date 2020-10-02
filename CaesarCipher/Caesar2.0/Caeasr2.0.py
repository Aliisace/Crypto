# Caesar Cipher 2.0

MAX_KEY_SIZE = 94

def getMode():
    while True:
        print("\tCaesar Cipher with Brutus Force" u"\u2122")
        mode = input().upper()
        if mode in "E D B".split():
            return mode[0]
        else:
            print("If you are Encrypting please press E\n If you are Decrypting please press D\n If you are using "
                  "Brutus Force" u"\u2122" " please press B")
            
def getMessage():
    print("Please enter your message for translation")
    return input()

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
        num = ord(symbol)
        num += key 
        if num > ord("~"):
            num -= 94
        elif num < ord(" "):
            num += 94
        translated += chr(num)
    return translated

mode = getMode()
message = getMessage()

if mode[0] != "B":
    key = getKey()
    print("Your translated message is: ")
    print(getTranslatedMessage(mode, message, key))
else:
    for key in range(1, MAX_KEY_SIZE + 1):
        print(key, getTranslatedMessage("Decrypt", message, key))