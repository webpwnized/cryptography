import argparse, base64, sys
from argparse import RawTextHelpFormatter

def key_is_involutary(pKey: int, pModulus:int) -> bool:
    # Given e(x) = (x + k) % n and d(x) = (x - k) % n
    # Involutary key means e(d(x)) = e(e(x)) = x (mod n)
    # e(e(x)) = x mod n => ((x + k) + k) = x mod n => 2k = 0 mod n => k = 0 or k = n/2 mod n
    return ((2 * pKey) % pModulus) == 0


def key_is_trivial(pKey: int, pModulus:int) -> bool:
    # Given e(x) = (x + k) % n and d(x) = (x - k) % n
    # Trival key means e(x) = x (mod n)
    return (pKey % pModulus) == 0


def do_encrypt(pByte: int, pKey: int, pModulus:int) -> int:
    #e(x) = (x + k) % n
    return (pByte + pKey) % pModulus


def do_decrypt(pByte: int, pKey: int, pModulus:int) -> int:
    #d(x) = (x - k) % n
    return (pByte - pKey) % pModulus


def encrypt(pPlaintextBytes: bytearray, pKey: int, pModulus:int) -> bytearray:
    lEncryptedBytes = bytearray()
    lEncryptedBytes.extend(map(lambda x: do_encrypt(x, pKey, pModulus), pPlaintextBytes))
    return lEncryptedBytes


def decrypt(pCiphertextBytes: bytearray, pKey: int, pModulus:int) -> bytearray:
    lDecryptedBytes = bytearray()
    lDecryptedBytes.extend(map(lambda x: do_decrypt(x, pKey, pModulus), pCiphertextBytes))
    return lDecryptedBytes


def print_plaintext(pInput: bytearray, pKey: int, pModulus:int, pVerbose: bool) -> None:

    lDecryptedInput = decrypt(pInput, pKey, pModulus)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Modulus: {}'.format(pModulus))
        print('Plaintext Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lDecryptedInput)

    if pVerbose: print()


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127: return True
    return False


def print_ciphertext(pInput: bytearray, pKey: int, pModulus:int, pVerbose: bool, pOutputFormat: str) -> None:

    lEncryptedInput = encrypt(pInput, pKey, pModulus)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput): pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Modulus: {}'.format(pModulus))
        print('Output Format: {}'.format(pOutputFormat))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


def bruteforce_plaintext(pInput: bytearray, pModulus:int, pVerbose: bool) -> None:
    for i in range(1, pModulus):
        print(i,'-> ',end='')
        print_plaintext(pInput, i, pModulus, pVerbose)
        if not pVerbose: print()


def derive_key(pKeyString: str, pModulus: int) -> int:

    return int(pKeyString) % pModulus


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Shifty: An implementation of the shift cipher system. Each plaintext character is shifted the same number of bytes as determined by the key. The shift occurs with respect to the modulus.',
                                         epilog='Encrypt the word hello with ceasar cipher:\n\npython shifty.py --encrypt --key 3 --verbose hello\n\nDecrypt the world hello with key 3:\n\npython shifty.py --decrypt --key 3 khoor\n\nBruteforce the world hello with key 3:\n\npython shifty.py --decrypt --bruteforce khoor\n\nExample using input from file, redirecting output to file and working with binary input. Combine these features to suit.\nEncrypt the contents of file binary-input.txt:\n\npython shifty.py --encrypt --key 3 --input-format=binary --output-format=binary --input-file binary-input.txt > binary-output.bin',
                                         formatter_class=RawTextHelpFormatter)
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key. Set to 3 for Caesar cipher. Set to 13 for Rot13 ciper.', type=int, action='store')
    lKeyOrBruteforceActionGroup.add_argument('-b', '--bruteforce', help='Rather than decrypt with KEY, try to brute force the plaintext.', action='store_true')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lInputSourceGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lInputSourceGroup.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lInputSourceGroup.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    lModulus = lArgs.modulus

    if lArgs.encrypt and lArgs.key is None:
        lArgParser.error('If -e/--encrypt selected, -k/--key is required')

    if lArgs.decrypt and lArgs.key is None and lArgs.bruteforce is None:
        lArgParser.error("If -d/--decrypt selected, either -k/--key or -b/--bruteforce is required")

    if lArgs.key:
        lKey = derive_key(lArgs.key, lModulus)

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
            if key_is_trivial(lKey, lModulus):
                print('[*] Warning: Key {} is trivial'.format(lKey))

            if key_is_involutary(lKey, lModulus):
                print('[*] Warning: Key {} is involutary'.format(lKey))
        #endif

        print_ciphertext(lInput, lKey, lModulus, lArgs.verbose, lArgs.output_format)

    elif lArgs.decrypt:
        if lArgs.bruteforce:
            # Test Case: BEEAKFYDJXUQYHYJIQRYHTYJIQFBQDUYJIIKFUHCQD
            bruteforce_plaintext(lInput, lModulus, lArgs.verbose)
        else:
            print_plaintext(lInput, lKey, lModulus, lArgs.verbose)
        # endif
    #endif