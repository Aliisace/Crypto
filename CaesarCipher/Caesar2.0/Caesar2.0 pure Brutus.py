# Caesar Cipher
MAX_KEY_SIZE = 94

print("\tCaesar Cipher with Brutus Force" u"\u2122")

def getMessage():
    print("Please enter your message for translation")
    return input()

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

message = getMessage()

for key in range(1, MAX_KEY_SIZE + 1):
    print(key, getTranslatedMessage("Decrypt", message, key))