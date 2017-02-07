import argparse, base64, sys

MODULUS = 256


def do_derive_key(pLetter: str) -> int:
    return ord(pLetter) - 65


def derive_key(pKey: str) -> bytearray:
    lKey = bytearray()
    lKey.extend(map(lambda x: do_derive_key(x), pKey))
    return lKey


def key_is_involutary(pKey: bytearray) -> bool:
    # Given e(x) = (x + k) % n and d(x) = (x - k) % n for all bytes k in pKey
    # Involutary key means e(d(x)) = e(e(x)) = x (mod n)
    # For all bytes k in pKey: e(e(x)) = x mod n => ((x + k) + k) = x mod n => 2k = 0 mod n => k = 0 or k = n/2 mod n
    # If any one byte is not involutary, the key is not involutary
    for lByte in pKey:
        if ((2 * lByte) % MODULUS) != 0:
            return False
    return True


def key_is_trivial(pKey: bytearray) -> bool:
    # Given e(x) = (x + k) % n and d(x) = (x - k) % n
    # Trival key means e(x) = x (mod n)
    # If every byte in pKey is 0, then pKey is trivial
    for lByte in pKey:
        if lByte != 0:
            return False
    return True


def do_encrypt(pByte: int, pKey: int) -> int:
    #e(x) = (x + k) % n
    return (pByte + pKey) % MODULUS


def do_decrypt(pByte: int, pKey: int) -> int:
    #d(x) = (x - k) % n
    return (pByte - pKey) % MODULUS


def encrypt(pPlaintextBytes: bytearray, pKey: bytearray) -> bytearray:
    lEncryptedBytes = bytearray()
    lLengthKey = len(pKey)
    for lIndex, lPlaintextByte in enumerate(pPlaintextBytes):
        lEncryptedBytes.append(do_encrypt(lPlaintextByte, pKey[(lIndex % lLengthKey)]))
    return lEncryptedBytes


def decrypt(pCiphertextBytes: bytearray, pKey: int) -> bytearray:
    lDecryptedBytes = bytearray()
    lLengthKey = len(pKey)
    for lIndex, lCiphertextByte in enumerate(pCiphertextBytes):
        lDecryptedBytes.append(do_decrypt(lCiphertextByte, pKey[(lIndex % lLengthKey)]))
    return lDecryptedBytes


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127: return True
    return False


def print_plaintext(pInput: bytearray, pKey: int, pVerbose: bool) -> None:

    lDecryptedInput = decrypt(pInput, pKey)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lDecryptedInput)

    if pVerbose: print()


def print_ciphertext(pInput: bytearray, pKey: bytearray, pVerbose: bool, pOutputFormat: str) -> None:

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


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lArgParser.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if (lArgs.encrypt or lArgs.decrypt) and lArgs.key is None:
        lArgParser.error('If -e/--encrypt or -d/--decrypt selected, -k/--key is required')

    if lArgs.key:
        lKey = derive_key(lArgs.key)

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

        print_ciphertext(lInput, lKey, lArgs.verbose, lArgs.output_format)

    elif lArgs.decrypt:

        print_plaintext(lInput, lKey, lArgs.verbose)

    #endif