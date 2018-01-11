import argparse, base64, sys
from argparse import RawTextHelpFormatter


def do_derive_key(pLetter: str, pModulus:int) -> int:
    # Try our best to normalize the key. This action potentially lowers the strength of the cipher
    # but the goal is to make learning the concepts easier
    if pLetter.isdigit():
        return (ord(pLetter) - 48) % pModulus
    elif pLetter.islower():
        return (ord(pLetter) - 97) % pModulus
    elif pLetter.isupper():
        return (ord(pLetter) - 65) % pModulus
    else:
        return ord(pLetter) % pModulus


def derive_key(pKey: str, pModulus:int) -> bytearray:
    lKey = bytearray()
    lKey.extend(map(lambda x: do_derive_key(x, pModulus), pKey))
    return lKey


def key_is_involutary(pKey: bytearray, pModulus:int) -> bool:
    # Involutary key means e(d(x)) = e(e(x)) = x (mod n).
    # For any given byte, e(x) = x + k mod n so e(e(x)) = x (mod n) -> (x + k) + k = x (mod n)
    # Therefore 2k = 0 (mod n)
    # If for every byte in pKey, 2k = 0 (mod n), then pKey is involutary
    for lByte in pKey:
        if ((2 * lByte) % pModulus) != 0:
            return False
    return True


def key_is_trivial(pKey: bytearray, pModulus:int) -> bool:
    # Given e(x) = (x + k) % n and d(x) = (x - k) % n
    # Trival key means e(x) = x (mod n)
    # If every byte in pKey is 0 (mod n), then pKey is trivial
    for lByte in pKey:
        if lByte != 0:
            return False
    return True


def do_encrypt(pByte: int, pKey: int, pModulus:int) -> int:
    #e(x) = (x + k) % n
    return (pByte + pKey) % pModulus


def encrypt(pPlaintextBytes: bytearray, pKey: bytearray, pModulus:int) -> bytearray:
    lEncryptedBytes = bytearray()
    lLengthKey = len(pKey)
    for lIndex, lPlaintextByte in enumerate(pPlaintextBytes):
        lEncryptedBytes.append(do_encrypt(lPlaintextByte, pKey[(lIndex % lLengthKey)], pModulus))
    return lEncryptedBytes


def do_decrypt(pByte: int, pKey: int, pModulus:int) -> int:
    #d(x) = (x - k) % n
    return (pByte - pKey) % pModulus


def decrypt(pCiphertextBytes: bytearray, pKey: bytearray, pModulus:int) -> bytearray:
    lDecryptedBytes = bytearray()
    lLengthKey = len(pKey)
    for lIndex, lCiphertextByte in enumerate(pCiphertextBytes):
        lDecryptedBytes.append(do_decrypt(lCiphertextByte, pKey[lIndex % lLengthKey], pModulus))
    return lDecryptedBytes


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127: return True
    return False


def print_plaintext(pInput: bytearray, pKey: bytearray, pModulus:int, pVerbose: bool, pUnmodifiedKey: str) -> None:

    lDecryptedInput = decrypt(pInput, pKey, pModulus)

    if pVerbose:
        print('Unmodified Key: {}'.format(pUnmodifiedKey))
        print('Derived Key: {}'.format(list(pKey)))
        print('Modulus: {}'.format(pModulus))
        print('Plain Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lDecryptedInput)

    if pVerbose: print()


def print_ciphertext(pInput: bytearray, pKey: bytearray, pModulus:int, pVerbose: bool, pOutputFormat: str, pUnmodifiedKey: str) -> None:

    lEncryptedInput = encrypt(pInput, pKey, pModulus)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput):
        pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Unmodified Key: {}'.format(pUnmodifiedKey))
        print('Derived Key: {}'.format(list(pKey)))
        print('Modulus: {}'.format(pModulus))
        print('Output Format: {}'.format(pOutputFormat))
        print('Cipher Output: ', end='')
    # end if

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Visionary: An implementation of the vigenere cipher system. A key is provided. Each byte of the key shifts the respective byte of plaintext. If the plaintext is longer than the key, the key bytes start over. The key derivation normalizes the key weakening the cipher. For example, A = a = 1 = shift plaintext 1 byte. The shifts occurs with respect to the modulus.',
                                         epilog='Encrypt the word helloworld with key 12345:\n\npython visionary.py --encrypt --key 12345 --verbose "helloworld"\n\nDecrypt the world helloworld with key 12345:\n\npython visionary.py --decrypt --key 12345 "igoptxqupi"\n\nExample using input from file, redirecting output to file and working with binary input. Combine these features to suit.\nEncrypt the contents of file funny-cat-1.jpg:\n\npython visionary.py --encrypt --key rocky329 --input-format=binary --output-format=binary --input-file=funny-cat-1.jpg > encrypted-funny-cat-1.bin',
                                         formatter_class=RawTextHelpFormatter)
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lInputSourceGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lInputSourceGroup.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lInputSourceGroup.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    lModulus = lArgs.modulus

    if (lArgs.encrypt or lArgs.decrypt) and lArgs.key is None:
        lArgParser.error('If -e/--encrypt or -d/--decrypt selected, -k/--key is required')

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
                print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            if key_is_involutary(lKey, lModulus):
                print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        #endif

        print_ciphertext(lInput, lKey, lModulus, lArgs.verbose, lArgs.output_format, lArgs.key)

    elif lArgs.decrypt:

        print_plaintext(lInput, lKey, lModulus, lArgs.verbose, lArgs.key)

    #endif