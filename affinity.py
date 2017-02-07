import argparse, base64, sys

MODULUS = 256

def key_is_involutary(pKey: bytearray) -> bool:
    # Given e(x) = (x + k) % n and d(x) = (x - k) % n
    # Involutary key means e(d(x)) = e(e(x)) = x (mod n)
    # e(e(x)) => a(ax + b) + b = x (mod n) => a^2(x) + ab + b = x (mod n)
    # => a^2(x) + b(a + 1) = x (mod n) =>
    # a^2 = 1 (mod n) AND b(a+1) = 0 (mod n)
    return (((a**2) % MODULUS) == 1) and ((b * (a + 1)) % MODULUS) == 0


def key_is_trivial(pKey: bytearray) -> bool:
    # Given e(x) = (ax + b) % n and d(x) = 1/a(x - b) % n
    # Trival key means e(x) = x (mod n). This happens when a=1 and b=0.
    return pKey[0] == 1 and pKey[1] == 0


def do_encrypt(pByte: int, pKey: int) -> int:
    #e(x) = (x + k) % n
    return (pByte + pKey) % MODULUS


def do_decrypt(pByte: int, pKey: int) -> int:
    #d(x) = (x - k) % n
    return (pByte - pKey) % MODULUS


def encrypt(pPlaintextBytes: bytearray, pKey: int) -> bytearray:
    lEncryptedBytes = bytearray()
    lEncryptedBytes.extend(map(lambda x: do_encrypt(x, pKey), pPlaintextBytes))
    return lEncryptedBytes


def decrypt(pCiphertextBytes: bytearray, pKey: int) -> bytearray:
    lDecryptedBytes = bytearray()
    lDecryptedBytes.extend(map(lambda x: do_decrypt(x, pKey), pCiphertextBytes))
    return lDecryptedBytes


def print_plaintext(pInput: bytearray, pKey: int, pVerbose: bool):

    lDecryptedInput = decrypt(pInput, pKey)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lDecryptedInput)

    if pVerbose: print()


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127: return True
    return False


def print_ciphertext(pInput: bytearray, pKey: int, pVerbose: bool, pOutputFormat: str):

    lEncryptedInput = encrypt(pInput, pKey)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput): pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


def bruteforce_plaintext(pInput: bytearray, pVerbose: bool):
    for i in range(1, 256):
        print(i,'-> ',end='')
        print_plaintext(pInput, i, pVerbose)
        if not pVerbose: print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key in a,b format', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lArgParser.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if (lArgs.encrypt or lArgs.decrypt) and lArgs.key is None:
        lArgParser.error('If -e/--encrypt or -d/--decrypt selected, -k/--key is required')

    if lArgs.key:
        try:
            lKey = bytearray(map(int, lArgs.key.split(',')))
            for lSubkey in lKey:
                if type(lSubkey) != int:
                    raise Exception('Keys not of type integer')
        except:
            lArgParser.error("Affine cipher requires two keys of type integer. Input key in a,b format. i.e. --key=1,1")

    if lArgs.input_file:
        if lArgs.input_format == 'base64':
            with open(lArgs.input_file, 'rb') as lFile:
                lInput = bytearray(base64.b64decode(lFile.read()))
        else:
            with open(lArgs.input_file, 'rb') as lFile:
                lInput = bytearray(lFile.read())
    else:
        if lArgs.input_format == 'character':
            lInput = bytearray(lArgs.INPUT.encode())
        elif lArgs.input_format == 'base64':
            lInput = bytearray(base64.b64decode(lArgs.INPUT))
        elif lArgs.input_format == 'binary':
            lInput = bytearray(lArgs.INPUT)

    if lArgs.encrypt:

        if lArgs.verbose:
            if key_is_trivial(lKey):
                print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            if key_is_involutary(lKey):
                print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        #endif

        #print_ciphertext(lInput, lKey, lArgs.verbose, lArgs.output_format)

    elif lArgs.decrypt:
        if lArgs.bruteforce:
            # Test Case: BEEAKFYDJXUQYHYJIQRYHTYJIQFBQDUYJIIKFUHCQD
            bruteforce_plaintext(lInput, lArgs.verbose)
        else:
            print_plaintext(lInput, lKey, lArgs.verbose)
        # endif
    #endif
