import argparse

# Shift Cipher
#     E(x) = (x + n) % 26
#     D(x) = (x - n) % 26

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def do_encryption_shift_cipher(pPlaintext, pKey):
    #Encrypt the string and return the ciphertext
    result = ''

    for l in pPlaintext.lower():
        try:
            i = (ALPHABET.index(l) + pKey) % 26
            result += ALPHABET[i]
        except ValueError:
            result += l

    return result.lower()


def do_decryption_shift_cipher(pCiphertext, pKey):
    #Decrypt the string and return the plaintext
    result = ''

    for l in pCiphertext:
        try:
            i = (ALPHABET.index(l) - pKey) % 26
            result += ALPHABET[i]
        except ValueError:
            result += l

    return result


def show_result(pText, pKey, pEncrypt):

    print('Text: {}'.format(pText))
    print('Key: {}'.format(pKey))

    pText = pText.lower()

    if pEncrypt:
        lEncrypted = do_encryption_shift_cipher(pText, pKey)
        print('Encrytped: {}'.format(lEncrypted.upper()))
    else:
        lDecrypted = do_decryption_shift_cipher(pText, pKey)
        print('Decrytped: {}'.format(lDecrypted))

    print()


def decrypt(pText, pKey):
    show_result(pText, pKey, False)


def bruteforce(pText):
    for i in range(1, 26):
        show_result(pText, i, False)


def encrypt(pText, pKey):
    show_result(pText, pKey, True)


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lArgParser.add_argument('-e', '--encrypt', help='Encrypt TEXT. This option requires a KEY.', action='store_true')
    lArgParser.add_argument('-d', '--decrypt', help='Decrypt TEXT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lArgParser.add_argument('-b', '--bruteforce', help='Rather than decrypt with KEY, try to brute force the plaintext.', action='store_true')
    lArgParser.add_argument('-k', '--key', help='Encryption/Decription key', type=int, action='store')
    lArgParser.add_argument('TEXT', help='Text value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if lArgs.encrypt:
        encrypt(lArgs.TEXT, lArgs.key)
    elif lArgs.decrypt:
        if lArgs.bruteforce:
            # Test Case: BEEAKFYDJXUQYHYJIQRYHTYJIQFBQDUYJIIKFUHCQD
            bruteforce(lArgs.TEXT)
        else:
            decrypt(lArgs.TEXT, lArgs.key)
        # endif
    #endif
