import argparse
import base64
import sys

def do_encrypt_character(pCharacter: str, pKey: int) -> int:
    #e(x) = (x + k) % 128
    return (ord(pCharacter) + pKey) % 256


def do_decrypt_character(pCharacter: str, pKey: int) -> int:
    #d(x) = (x - k) % 128
    return (ord(pCharacter) - pKey) % 256


def do_encrypt_byte(pByte: int, pKey: int) -> int:
    #e(x) = (x + k) % 256
    return (pByte + pKey) % 256


def do_decrypt_byte(pByte: int, pKey: int) -> int:
    #d(x) = (x - k) % 256
    return (pByte - pKey) % 256


def encrypt_characters(pPlaintextCharacters: str, pKey: int, pBase64Output: bool) -> str:
    lEncryptedBytes = bytearray()
    lEncryptedBytes.extend(map(lambda x: do_encrypt_character(x, pKey), pPlaintextCharacters))
    lUnprintable = False
    for x in lEncryptedBytes:
        if x > 127:
            lUnprintable = True
            break
    if lUnprintable or pBase64Output:
        return base64.b64encode(lEncryptedBytes).decode('utf-8')
    else:
        return lEncryptedBytes.decode('utf-8')


def encrypt_binary(pPlaintextBytes: bytearray, pKey: int) -> str:
    lEncryptedBytes = bytearray()
    lEncryptedBytes.extend(map(lambda x: do_encrypt_byte(x, pKey), pPlaintextBytes))
    return base64.b64encode(lEncryptedBytes)


def decrypt_characters(pCiphertextCharacters: str, pKey: int) -> str:
    lDecryptedBytes = bytearray()
    lDecryptedBytes.extend(map(lambda x: do_decrypt_character(x, pKey), pCiphertextCharacters))
    return lDecryptedBytes.decode("utf-8")


def decrypt_binary(pCiphertextBytes: bytearray, pKey: int) -> bytearray:
    lDecryptedBytes = bytearray()
    lDecryptedBytes.extend(map(lambda x: do_decrypt_byte(x, pKey), pCiphertextBytes))
    return lDecryptedBytes


def key_is_involutary(pKey: int) -> bool:
    # Given e(x) = (x + k) % 26 and d(x) = (x - k) % 26
    # Involutary key means e(d(x)) = e(e(x)) = x (mod 26)
    # e(e(x)) = x mod 26 => ((x + k) + k) = x mod 26 => 2k = 0 mod 26 => k = 0 or k = 13
    return ((2 * pKey) % 26) == 0


def key_is_trivial(pKey: int) -> bool:
    # Given e(x) = (x + k) % 26 and d(x) = (x - k) % 26
    # Trival key means e(x) = x (mod 26)
    return (pKey % 26) == 0


def print_character_plaintext(pInput: str, pKey: int, pVerbose: bool):

    lDecryptedInput = decrypt_characters(pInput, pKey)

    if pVerbose:
        print('Cipher Input: {}'.format(pInput))
        print('Key: {}'.format(pKey))
        print('Plain Input: {}'.format(lDecryptedInput))
        print()
    else:
        print(lDecryptedInput, end='')


def print_character_ciphertext(pInput: str, pKey: int, pVerbose: bool, pBase64Output: bool):

    lEncryptedInput = encrypt_characters(pInput, pKey, pBase64Output)

    if pVerbose:
        print('Plain Input: {}'.format(pInput))
        print('Key: {}'.format(pKey))
        print('Cipher Output: {}'.format(lEncryptedInput))
        print()
    else:
        print(lEncryptedInput, end='')


def print_binary_plaintext(pInput: bytearray, pKey: int, pVerbose: bool):

    lDecryptedInput = decrypt_binary(pInput, pKey)

    if pVerbose:
        print('Cipher Input: {}'.format(pInput))
        print('Key: {}'.format(pKey))
        print('Plain Input: ')
        sys.stdout.buffer.write(lDecryptedInput)
        print()
    else:
        sys.stdout.buffer.write(lDecryptedInput)


def print_binary_ciphertext(pInput: bytearray, pKey: int, pVerbose: bool):

    lEncryptedInput = encrypt_binary(pInput, pKey)

    if pVerbose:
        print('Plain Input: {}'.format(pInput))
        print('Key: {}'.format(pKey))
        print('Cipher Output: {}'.format(lEncryptedInput))
        print()
    else:
        sys.stdout.buffer.write(lEncryptedInput)


def bruteforce_character_plaintext(pInput: str, pVerbose: bool):
    for i in range(1, 128):
        print(i,'-> ',end='')
        print_character_plaintext(pInput, i, pVerbose)
        if not pVerbose: print()

def bruteforce_binary_plaintext(pInput: bytearray, pVerbose: bool):
    for i in range(1, 256):
        print(i,'-> ',end='')
        print_binary_plaintext(pInput, i, pVerbose)
        if not pVerbose: print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decription key', type=int, action='store')
    lKeyOrBruteforceActionGroup.add_argument('-b', '--bruteforce', help='Rather than decrypt with KEY, try to brute force the plaintext.', action='store_true')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-b64', '--base64-output', help='Output format will be base64. Only relevant for encryption.', action='store_true')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lArgParser.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if lArgs.encrypt and lArgs.key is None:
        lArgParser.error('If -e/--encrypt selected, -k/--key is required')

    if not lArgs.encrypt and lArgs.base64_output:
        lArgParser.error('-b64/--base64-output is only relevant if encrypting INPUT')

    if lArgs.decrypt and lArgs.key is None and lArgs.bruteforce is None:
        lArgParser.error("If -d/--decrypt selected, either -k/--key or -b/--bruteforce is required")

    if lArgs.input_file:
        if lArgs.input_format == 'character':
            lFile = open(lArgs.input_file, 'r')
            lInput = lFile.read()
            lFile.close()
        else:
            with open(lArgs.input_file, 'rb') as f:
                lInput = bytearray(f.read())
    else:
        lInput = lArgs.INPUT

    if lArgs.encrypt:

        if lArgs.verbose:
            if key_is_trivial(lArgs.key):
                print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            if key_is_involutary(lArgs.key):
                print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        #endif

        if lArgs.input_format == 'character':
            print_character_ciphertext(lInput, lArgs.key, lArgs.verbose, lArgs.base64_output)
        else:
            if lArgs.input_format == 'base64':
                lInput = base64.b64decode(lInput)
            print_binary_ciphertext(lInput, lArgs.key, lArgs.verbose)

    elif lArgs.decrypt:
        if lArgs.bruteforce:
            # Test Case: BEEAKFYDJXUQYHYJIQRYHTYJIQFBQDUYJIIKFUHCQD
            if lArgs.input_format == 'character':
                bruteforce_character_plaintext(lInput, lArgs.verbose)
            else:
                if lArgs.input_format == 'base64':
                    lInput = base64.b64decode(lInput)
                bruteforce_binary_plaintext(lInput, lArgs.verbose)

        else:
            if lArgs.input_format == 'character':
                print_character_plaintext(lInput, lArgs.key, lArgs.verbose)
            else:
                if lArgs.input_format == 'base64':
                    lInput = base64.b64decode(lInput)
                print_binary_plaintext(lInput, lArgs.key, lArgs.verbose)

        # endif
    #endif