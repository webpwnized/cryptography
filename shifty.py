import argparse

# Shift Cipher
#   e(x) = (x + n) % 26
#   d(x) = (x - n) % 26

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def do_encryption_shift_cipher(pPlaintext, pKey):
    #Encrypt the string and return the ciphertext
    result = ''

    for lLetter in pPlaintext.lower():
        try:
            i = (ALPHABET.index(lLetter) + pKey) % 26
            result += ALPHABET[i]
        except ValueError:
            result += lLetter

    return result.lower()


def do_decryption_shift_cipher(pCiphertext, pKey):
    #Decrypt the string and return the plaintext
    result = ''

    for lLetter in pCiphertext:
        try:
            i = (ALPHABET.index(lLetter) - pKey) % 26
            result += ALPHABET[i]
        except ValueError:
            result += lLetter

    return result


def key_is_involutary(pKey):
    return 2 * pKey % 26 == 0

def show_result(pText, pKey, pEncrypt):

    print('Text: {}'.format(pText))
    print('Key: {}'.format(pKey))

    if key_is_involutary(pKey):
        print('[*] Warning: Key {} is involutary'.format(pKey))

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
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt TEXT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt TEXT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lEncryptionActionGroup.add_argument('-b', '--bruteforce', help='Rather than decrypt with KEY, try to brute force the plaintext.', action='store_true')
    lArgParser.add_argument('-k', '--key', help='Encryption/Decription key', type=int, action='store')
    lArgParser.add_argument('TEXT', help='Text value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if (lArgs.encrypt or lArgs.decrypt) and not lArgs.key:
        lArgParser.error('If -e/--encrypt or -d/--decrypt selected, -k/--key is required')

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
