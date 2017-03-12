# Requires pip install bitarray
from bitarray import bitarray
import argparse, base64, sys


def derive_key(pKeyString: str) -> list:
    l8BitFormat = '08b'
    lKeyBitStrings = []
    lLeftKey = bitarray()
    lRightKey = bitarray()
    lKey = []

    # Parse 5 bytes from comma delimited input
    lKeyBytes = list(map(int, pKeyString.split(",")))

    if len(lKeyBytes) != 5:
        raise Exception('Key must be 5 bytes in length. Enter the bytes as a list of comma-delimited integers between 0-255. Example: 25,230,3,64,12.')

    # Transform each byte from integer to string of bits after validating byte is an integer
    for lKeyByte in lKeyBytes:
        if type(lKeyByte) != int:
            raise Exception('Key bytes must be entered as integers. Enter the bytes as a list of comma-delimited integers between 0-255. Example: 25,230,3,64,12.')
        lKeyBitStrings.append(format(lKeyByte, l8BitFormat))

    # Initialization vector for first register is first two bytes of key (16 bits)
    lLeftKey.extend(lKeyBitStrings[0])
    lLeftKey.extend(lKeyBitStrings[1])

    # Initialization vector for second register is last three bytes of key (24 bits)
    lRightKey.extend(lKeyBitStrings[2])
    lRightKey.extend(lKeyBitStrings[3])
    lRightKey.extend(lKeyBitStrings[4])

    # represent key as list of two bit stings
    lKey.append(lLeftKey)
    lKey.append(lRightKey)

    return(lKey)


def key_is_involutary(pKey: list) -> bool:
    # Involutary key means e(d(x)) = e(e(x)) = x
    # x = d(e(x)) = ((x XOR key) XOR key)
    # Since (key XOR key) = 0 and x XOR 0 = x then ((x XOR key) XOR key) = x
    # Therefore all keys are involutary for CSS cipher
    return True


def key_is_trivial(pKey: list) -> bool:
    # Trivial key means e(x) = x
    # This is true when key is 0,0,0,0,0
    for lKey in pKey:
        if int.from_bytes(lKey.tobytes(), byteorder='little') != 0:
            return False
    return True


def initialize_registers(pKey: list) -> tuple:

    lRegister1 = bitarray()
    lRegister2 = bitarray()

    # Register 1 is initialized with left two bytes of KEY in bits 17 - 2 then a value of 1 in bit 1
    # The hardcoded value of 1 in bit position 1 guarantees the register is not initialized with zeros
    lRegister1.extend(pKey[0])
    lRegister1.append('1')

    # Register 2 is initialized with right three bytes of KEY in bits 25 - 2 then a value of 1 in bit 1
    # The hardcoded value of 1 in bit position 1 guarantees the register is not initialized with zeros
    lRegister2.extend(pKey[1])
    lRegister2.append('1')

    return lRegister1, lRegister2


def encrypt(pInput: bytearray, pKey: list) -> bytearray:

    lRegister1, lRegister2 = initialize_registers(pKey)
    lCarryBit = False # Bitwise 0
    l8BitFormat = '08b'
    lCiphertext = bytearray()

    for lByte in pInput:

        lPlaintextBits = bitarray(format(lByte, l8BitFormat))
        lCiphertextBits = bitarray()

        # generate byte from each LFSR
        # This is hard to follow because we consider MSB to be bit 17 but this code considers MSB to be bit 1
        for i in range(0, 8):
            # xor bit 17 and 3
            lR1Bit17 = lRegister1[0]    # 17
            lR1Bit3 = lRegister1[14]    # 3

            lNextR1Bit = lR1Bit17 ^ lR1Bit3

            # discard right-most bit
            lRegister1.pop(16)

            # append new bit as MSB
            lRegister1.insert(0, lNextR1Bit)

            # xor bits 25, 8, 6 and 2
            lR2Bit25 = lRegister2[0]    # 25
            lR2Bit8 = lRegister2[17]    # 8
            lR2Bit6 = lRegister2[19]    # 6
            lR2Bit2 = lRegister2[23]    # 2

            lNextR2Bit = lR2Bit25 ^ lR2Bit8 ^ lR2Bit6 ^ lR2Bit2

            # discard right-most bit
            lRegister2.pop(24)

            # append new bit as MSB
            lRegister2.insert(0, lNextR2Bit)

            # Add the two bits that were just generated and save the carry bit for next addition
            a = lNextR1Bit
            b = lNextR2Bit
            cin = lCarryBit
            lAdderSum = a ^ b ^ cin
            lCarryBit = (a and b) or ((a ^ b) and cin)

            # encrypt by xoring plaintext with ciphertext
            lCiphertextBits.append(lPlaintextBits[i] ^ lAdderSum)

        # tobytes() returns an array, so we take first (only) element
        lCiphertext.append(int(lCiphertextBits.tobytes()[0]))

    return lCiphertext


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127:
            return True
    return False


def print_ciphertext(pInput: bytearray, pKey: list, pVerbose: bool, pOutputFormat: str) -> None:

    lEncryptedInput = encrypt(pInput, pKey)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput): pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Output Format: {}'.format(pOutputFormat))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Content Scrambing System: An implementation of the css cipher system using two linear feedback shift registers')
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY.', action='store_true')
    lArgParser.add_argument('-k', '--key', help='Encryption/Decryption key. Must be 5 bytes. Enter the bytes as a list of comma-delimited integers between 0-255. Example: 25,230,3,64,12', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lInputSourceGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lInputSourceGroup.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lInputSourceGroup.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if lArgs.encrypt and lArgs.key is None:
        lArgParser.error('If -e/--encrypt selected or -d/--decrypt selected, -k/--key is required')

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

    if lArgs.input_format and not lArgs.output_format:
        lArgs.output_format = lArgs.input_format

    if lArgs.encrypt:

        if lArgs.verbose:
             if key_is_trivial(lKey):
                 print('[*] Warning: Key {} is trivial'.format(lArgs.key))

             if key_is_involutary(lKey):
                 print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        # endif

        print_ciphertext(lInput, lKey, lArgs.verbose, lArgs.output_format)

    elif lArgs.decrypt:

        # For CSS every key is involutary
        # x = d(e(x)) = ((x XOR key) XOR key) = x
        # Therefore to decrypt, it is only neccesary to encrypt a second time
        print_ciphertext(lInput, lKey, lArgs.verbose, lArgs.output_format)

    # endif