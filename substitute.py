import argparse, base64, sys, math


def derive_key(pKey: str) -> list:
    lKey = list(map(int, lArgs.key.split(',')))

    lKeyValid = True
    lKeyLength = len(lKey)
    for i in range(0, lKeyLength):
        if i not in lKey:
            lKeyValid = False
            break
        # end if
    # end for

    if not lKeyValid:
        raise Exception('Key missing digits')

    return lKey


def key_is_involutary(pKey: list) -> bool:
    # Given e(x) = permuation(x)
    # Involutary key means e(d(x)) = e(e(x)) = x
    # Key is involutary if it contains only cycles of length 1 or 2
    return False


def key_is_trivial(pKey: list) -> bool:
    # Given e(x) = permuation(x)
    # Trivial key means e(x) = x
    # Key is trivial if digits are sequential
    lKeyLength = len(pKey)
    for i in range(0, lKeyLength):
        if i != pKey[i]:
            return False
    return True


def do_encrypt(pByte: int, pKey: int) -> int:
    #e(x) = (x + k) % n
    return (pByte + pKey) % MODULUS


def do_decrypt(pByte: int, pKey: int) -> int:
    #d(x) = (x - k) % n
    return (pByte - pKey) % MODULUS


def encrypt(pPlaintextBytes: bytearray, pKey: list) -> tuple:
    lEncryptedBytes = bytearray()
    lLengthKey = len(pKey)
    lLengthPlaintext = len(pPlaintextBytes)
    lPadBytesNeeded = lLengthPlaintext % lLengthKey

    if lPadBytesNeeded > 0:
        for i in range(0, lPadBytesNeeded):
            pPlaintextBytes.append(lPadBytesNeeded)
        lLengthPlaintext += lPadBytesNeeded

    for lIndex in range(0, lLengthPlaintext):
        lRound = math.floor(lIndex / lLengthKey)
        lKeyIndex = lIndex % lLengthKey
        lKeyValue = pKey[lKeyIndex]
        lCurrentBlock = lRound * lLengthKey
        lEncryptedBytes.append(pPlaintextBytes[lCurrentBlock + lKeyValue])
        print(pKey, lRound, lKeyIndex, lKeyValue, lCurrentBlock, lEncryptedBytes)

    return lEncryptedBytes, lPadBytesNeeded


def decrypt(pCiphertextBytes: bytearray, pKey: list) -> bytearray:
    lDecryptedBytes = bytearray()
    lLengthKey = len(pKey)
    for lIndex, lCiphertextByte in enumerate(pCiphertextBytes):
        lDecryptedBytes.append(do_decrypt(lCiphertextByte, pKey[(lIndex % lLengthKey)]))
    return lDecryptedBytes


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127: return True
    return False


def print_plaintext(pInput: bytearray, pKey: list, pVerbose: bool) -> None:

    lDecryptedInput = decrypt(pInput, pKey)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Derived Key: {}'.format(list(pKey)))
        print('Plain Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lDecryptedInput)

    if pVerbose: print()


def print_ciphertext(pInput: bytearray, pKey: list, pVerbose: bool, pOutputFormat: str) -> None:

    lEncryptedInput, lPadBytesNeeded = encrypt(pInput, pKey)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput):
        pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Output Format: {}'.format(pOutputFormat))
        print('Cipher Output: ', end='')
    # end if

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lInputSourceGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lInputSourceGroup.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lInputSourceGroup.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if (lArgs.encrypt or lArgs.decrypt) and lArgs.key is None:
        lArgParser.error('If -e/--encrypt or -d/--decrypt selected, -k/--key is required')

    if lArgs.key:
        try:
            lKey = derive_key(str(lArgs.key))
        except:
            lArgParser.error('Key must be a complete set of integers in any order starting from 0. Examples include 2,1,3,0 and 3,2,0,5,6,7,1,4')

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

    if lArgs.input_format and not lArgs.output_format:
        lArgs.output_format = lArgs.input_format

    if lArgs.encrypt:

        if lArgs.verbose:
            if key_is_trivial(lKey):
                print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            # TODO
            # if key_is_involutary(lKey):
                # print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        #endif

        print_ciphertext(lInput, lKey, lArgs.verbose, lArgs.output_format)

    elif lArgs.decrypt:

        print_plaintext(lInput, lKey, lArgs.verbose)

    #endif