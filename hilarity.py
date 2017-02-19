import argparse, math


def derive_key(lKey: str, pModulus: int) -> bytearray:
    lKeyMatrix = bytearray()

    # split on comma into bytearray
    lKeyMatrix = bytearray(map(lambda x: get_int_modulo_n_in_zn(int(x), pModulus), lKey.split(',')))

    for lSubkey in lKeyMatrix:
        if type(lSubkey) != int:
            raise Exception('Keys not of type integer')

    lMatrixLength = len(lKeyMatrix)
    if math.sqrt(lMatrixLength) != math.floor(math.sqrt(lMatrixLength)):
        raise Exception('Matrix is not square')

    return lKeyMatrix


# return (g, x, y) a*x + b*y = gcd(x, y)
def extended_euclidian_algorithm(a:int, b:int) -> tuple:
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_euclidian_algorithm(b % a, a)
        return (g, y - (b // a) * x, x)


# x = mulinv(b) mod n, (x * b) % n == 1
def get_multiplicative_inverse(a:int, n:int) -> int:
    g, x, _ = extended_euclidian_algorithm(a, n)
    if g == 1:
        return x % n


def get_adjunct(pMatrix: bytearray, pModulus: int) -> bytearray:

    lAdjunct = bytearray()
    lSizeOfMatrix = len(pMatrix)

    if lSizeOfMatrix != 4:
        raise Exception('I dont know how to do non-2x2 matrices yet')

    a = pMatrix[0]
    b = pMatrix[1]
    c = pMatrix[2]
    d = pMatrix[3]

    # Calculate adjunct of matrix
    lAdjunct.append(d)
    lAdjunct.append(get_int_modulo_n_in_zn(-1 * b, pModulus))
    lAdjunct.append(get_int_modulo_n_in_zn(-1 * c, pModulus))
    lAdjunct.append(a)

    return lAdjunct


def get_determinant(pMatrix: bytearray, pModulus: int) -> int:

    lSizeOfMatrix = len(pMatrix)
    if lSizeOfMatrix != 4:
        raise Exception('I dont know how to do non-2x2 matrices yet')

    a = pMatrix[0]
    b = pMatrix[1]
    c = pMatrix[2]
    d = pMatrix[3]

    # Calculate determinant of matrix
    return ((a * d) - (b * c)) % pModulus


def get_int_modulo_n_in_zn(pInt, pModulus):
    lAModuloN = pInt % pModulus
    if lAModuloN < 0:
        lAModuloN = pModulus + lAModuloN
    return lAModuloN


def get_inverse_matrix(pMatrix: bytearray, pModulus: int) -> bytearray:

    lInverseMatrix = bytearray()
    lSizeOfMatrix = len(pMatrix)
    if lSizeOfMatrix != 4:
        raise Exception('I dont know how to do non-2x2 matrices yet')

    # Calculate adjunct of matrix
    lAdjunct = get_adjunct(pMatrix, pModulus)
    lDeterminant = get_determinant(pMatrix, pModulus)
    lInverseDeterminant = get_multiplicative_inverse(lDeterminant, pModulus)

    for i in range(0, lSizeOfMatrix):
        lInverseMatrix.append(get_int_modulo_n_in_zn(lInverseDeterminant * lAdjunct[i], pModulus))

    return lInverseMatrix


def key_is_involutary(pKey: bytearray, pModulus: int) -> bool:

    lSizeOfMatrix = len(pKey)
    if lSizeOfMatrix != 4:
        raise Exception('I dont know how to do non-2x2 matrices yet')

    lDeterminant = get_determinant(pKey, pModulus)

    lNegative1ModN = pModulus - 1
    if lDeterminant == lNegative1ModN or lDeterminant == 1:
        lInverseKey = get_inverse_matrix(pKey, pModulus)

        lKeyInvolutary = True
        for i in range(0, lSizeOfMatrix):
            if get_int_modulo_n_in_zn(pKey[i], pModulus) != get_int_modulo_n_in_zn(lInverseKey[i], pModulus):
                lKeyInvolutary = False

        return lKeyInvolutary

    return False


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Hilarity: An implementation of the Hill cipher system')
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key of integers in matrix format. The matrix must be square. For example a 2 X 2 matrix could be 1, 2, 3, 4', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lInputSourceGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lInputSourceGroup.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lInputSourceGroup.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    lModulus = lArgs.modulus
    lKey = derive_key(lArgs.key, lModulus)

    if lArgs.encrypt:

        if lArgs.verbose:
            #if key_is_trivial(lArgs.key):
            #   print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            if key_is_involutary(lKey, lArgs.modulus):
                print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        #endif

