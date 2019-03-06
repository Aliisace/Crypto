# makeRsaKeys

import random, sys, os, primeNum, cryptomath

def main():
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
    
    #create a public/private key pair with 1024 bit keys
    print("Making key files...")
    makeKeyFiles("abc", 1024)
    print("Key files made")
 
    
def generateKey(keySize):
    # Creates a public/private key pair with keys that are keySize bits in size.
    #This function may take a while to run
    
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    print("Generating p prime...")
    p = primeNum.generateLargePrime(keySize)
    print("Generating q prime...")
    q = primeNum.generateLargePrime(keySize)
    n = p * q
    
    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    print("Generating e that is relitively prime to (p-1)*(q-1)...")
    while True:
        # keep trying random numbers for e until a valid one is found
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p-1) * (q-1)) == 1:
            break
    
    # step 3: calculate d, the mod inverse of e
    print("calculating d, the mod inverse of e")
    d = cryptomath.findModInverse(e, (p-1) * (q-1))
    
    publicKey = (n, e)
    privateKey = (n, d)
    
    print("Public Key")
    print("Private Key")
    
    return (publicKey, privateKey)


def makeKeyFiles(name, keySize):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the value in name)
    # with the the n,e and d,e integers written in them, delimited by a comma.
    
    if os.path.exists('%s_pub.txt' % (name)) or os.path.exists('%s_priv.txt' % (name)):
        print("This will over write the output file %s. (C)ontinue or (Q)uit" %(name))
        response = input("> ")
        if not response.lower().startswith("c"):
            sys.exit()
        
    publicKey, privateKey = generateKey(keySize)
    
    print()
    print("The public key is a %s and a %s digit number." %(len(str(publicKey[0])), len(str(publicKey[1]))))
    print("Writing public key to file %s_pub.txt..." %(name))
    fo = open("%s_pub.txt" %(name), "w")
    fo.write("%s,%s,%s" %(keySize, publicKey[0], publicKey[1]))
    fo.close()
    
    print()
    print("The private key is a %s and a %s digit number." %(len(str(publicKey[0])), len(str(publicKey[1]))))
    print("Writing private key to file %s_priv.txt..." %(name))
    fo = open("%s_priv.txt" %(name), "w")
    fo.write("%s,%s,%s" %(keySize, privateKey[0], privateKey[1]))
    fo.close()
    

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

    
if __name__ == "__main__":
    main()