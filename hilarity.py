import argparse


def derive_key(lKey: str) -> list:
    lKeyMatrix = []

    # split on semicolon into list of strings
    lRows = lKey.split(';')

    for lRow in lRows:
        lKeyMatrix.append(bytearray(map(int, lRow.split(','))))

    print(lKeyMatrix)
    exit(0)

    return lKeyMatrix


def get_count_involutary_keys(lKey: list, lModulus: int) -> int:

    lSizeOfMatrix = len(lKey)
    lCountInvolutaryKeys = 0

    if lSizeOfMatrix == 2:
        a = lKey[0][0]
        b = lKey[0][1]
        c = lKey[1][0]
        d = lKey[1][1]

        for i in range(0, lModulus):
            for j in range(0, lModulus):
                for k in range(0, lModulus):
                    for l in range(0, lModulus):
                        lDeterminant = ((a * d) - (b * c)) % lModulus
                        if lDeterminant == -1 or lDeterminant == 1:
                            lCountInvolutaryKeys += 1

        return lCountInvolutaryKeys
    else:
        print('I dont know how to do non-2x2 matrices yet')
        return 0


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lEncryptionActionGroup.add_argument('-fi', '--find-involutary', help='Find involutary keys modulo MODULUS', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key of integers in matrix format. The matrix must be square. For example a 2 X 2 matrix could be 1, 2; 3, 4', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lInputSourceGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lInputSourceGroup.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lInputSourceGroup.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    lKey = derive_key(lArgs.key)
    lModulus = lArgs.modulus

    lCountInvolutaryKeys = get_count_involutary_keys(lKey)

    if lArgs.find_involutary:
        print('There are {} involutary keys modulo {}'.format(lCountInvolutaryKeys, lModulus))