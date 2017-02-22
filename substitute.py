import argparse, base64, sys, math


PADDING_INDICATION_BLOCK_LENGTH = 10


def get_padblock() -> bytearray:
    lPadBlock = bytearray()
    for i in range(0, PADDING_INDICATION_BLOCK_LENGTH):
        lPadBlock.append(i)
    return lPadBlock


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


def invert_key(pKey: list) -> list:
    lInvertedKey = []
    for lIndex, lKeyValue in enumerate(pKey):
        lInvertedKey.append(pKey.index(lIndex))
    return lInvertedKey


def get_permutation_cycles(pPermutation: list) -> list:

    lKeyLength = len(pPermutation)

    # Arbitrarily start at first byte in key
    lStartPosition = 0
    lCurrentPosition = 0
    lKeyBytesChecked = []
    lCurrentCycle = []
    lCycles = []
    # if value of current byte = position of current byte, then cycle is complete
    for i in range(0, lKeyLength):
        lCurrentCycle.append(pPermutation[lCurrentPosition])
        lKeyBytesChecked.append(pPermutation[lCurrentPosition])
        if pPermutation[lCurrentPosition] == lStartPosition:
            lCycles.append(lCurrentCycle)
            lCurrentCycle = []

            j = 0
            lNextPositionFound = False
            while j < lKeyLength and not lNextPositionFound:
                if pPermutation[j] not in lKeyBytesChecked:
                    lCurrentPosition = j
                    lStartPosition = j
                    lNextPositionFound = True
                j += 1
                # end if
            # end while j
        else:
            lCurrentPosition = pPermutation[lCurrentPosition]
            if i == (lKeyLength - 1):
                # Append last cycle
                lCycles.append(lCurrentCycle)
            # end if
    #end for i

    return lCycles


def key_is_involutary(pCycles: list) -> bool:
    # Given e(x) = permuation(x)
    # Involutary key means e(d(x)) = e(e(x)) = x
    # Key is involutary if it contains only cycles of length 1 or 2

    for lCycle in pCycles:
        if len(lCycle) > 2:
            return False
        # end if
    # end for
    return True


def key_is_trivial(pKey: list) -> bool:
    # Given e(x) = permuation(x)
    # Trivial key means e(x) = x
    # Key is trivial if digits are sequential
    lKeyLength = len(pKey)
    for i in range(0, lKeyLength):
        if i != pKey[i]:
            return False
    return True


def encrypt(pPlaintextBytes: bytearray, pKey: list) -> bytearray:
    lEncryptedBytes = bytearray()
    lLengthKey = len(pKey)
    lLengthPlaintext = len(pPlaintextBytes)
    lLengthLastBlock = lLengthPlaintext % lLengthKey
    if lLengthLastBlock > 0:
        lPadBytesNeeded = lLengthKey - (lLengthPlaintext % lLengthKey)
    else:
        lPadBytesNeeded = 0

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

    if lPadBytesNeeded > 0:
        lEncryptedBytes += get_padblock()

    return lEncryptedBytes


def decrypt(pCiphertextBytes: bytearray, pKey: list) -> bytearray:
    lDecryptedBytes = bytearray()
    lLengthCiphertext = len(pCiphertextBytes)
    lStartPaddingIndicationBlock = lLengthCiphertext-PADDING_INDICATION_BLOCK_LENGTH
    lEndPaddingIndicationBlock = lLengthCiphertext
    lPaddingDetected = False
    lPadBlock = get_padblock()
    lPadBytesNeeded = 0

    lDecryptionKey = invert_key(pKey)
    lLengthKey = len(lDecryptionKey)

    if pCiphertextBytes[lStartPaddingIndicationBlock:lEndPaddingIndicationBlock] == lPadBlock:
        lPaddingDetected = True
        lLengthCiphertext -= PADDING_INDICATION_BLOCK_LENGTH

    for lIndex in range(0, lLengthCiphertext):
        lRound = math.floor(lIndex / lLengthKey)
        lKeyIndex = lIndex % lLengthKey
        lKeyValue = lDecryptionKey[lKeyIndex]
        lCurrentBlock = lRound * lLengthKey
        lDecryptedBytes.append(pCiphertextBytes[lCurrentBlock + lKeyValue])

    if lPaddingDetected:
        lPadBytesNeeded = lDecryptedBytes[lLengthCiphertext-1]

    return lDecryptedBytes[0:lLengthCiphertext-lPadBytesNeeded]


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

    lEncryptedInput = encrypt(pInput, pKey)

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

    lArgParser = argparse.ArgumentParser(description='Substitute: An implementation of the substitution (permutation) cipher system')
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

            lCycles = get_permutation_cycles(lKey)
            print("Cycles of Key: {}".format(lCycles))

            if key_is_trivial(lKey):
                print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            if key_is_involutary(lCycles):
                print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        # end if

        print_ciphertext(lInput, lKey, lArgs.verbose, lArgs.output_format)

    elif lArgs.decrypt:

        print_plaintext(lInput, lKey, lArgs.verbose)

    #endif