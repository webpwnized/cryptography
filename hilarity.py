import argparse, math


def derive_matrix(lMatrixString: str, pModulus: int) -> bytearray:
    # split on comma into bytearray
    lMatrix = bytearray(map(lambda x: get_int_modulo_n_in_zn(int(x), pModulus), lMatrixString.split(',')))

    for lElement in lMatrix:
        if type(lElement) != int:
            raise Exception('Matrix elements not of type integer')

    lMatrixLength = len(lMatrix)
    if math.sqrt(lMatrixLength) != math.floor(math.sqrt(lMatrixLength)):
        raise Exception('Matrix is not square')

    return lMatrix


def get_gcd(x: int, y: int) -> int:

    if y > x and x != 0:
        #Swap the arguments
        return get_gcd(y, x)

    if x % y == 0:
        #y divides x evenly so y is gcd(x, y)
        return y

    # We can make calculating GCD easier.
    # The GCD of a,b is the same as the GCD of a and the remainder of dividing a by b
    return get_gcd(y, x % y)


# return (g, x, y) a*x + b*y = gcd(x, y)
def extended_euclidian_algorithm(a: int, b: int) -> tuple:
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_euclidian_algorithm(b % a, a)
        return (g, y - (b // a) * x, x)


# x = mulinv(b) mod n, (x * b) % n == 1
def get_multiplicative_inverse(a: int, n: int) -> int:
    g, x, _ = extended_euclidian_algorithm(a, n)
    if g == 1:
        return x % n


def get_int_modulo_n_in_zn(pInt: int, pModulus: int) -> int:
    lAModuloN = pInt % pModulus
    if lAModuloN < 0:
        lAModuloN = pModulus + lAModuloN
    return lAModuloN


def print_matrix(pMatrix: bytearray) -> None:

    lSizeOfMatrix = len(pMatrix)
    lRowLength = math.sqrt(lSizeOfMatrix)

    for lIndex, lByte in enumerate(pMatrix):
        if lIndex % lRowLength == 0:
            print()
        print(str(lByte) + '\t', end='')
    print()
    print()


def get_determinant(pMatrix: bytearray, pModulus: int) -> int:

    lSizeOfMatrix = len(pMatrix)
    if lSizeOfMatrix != 4 and lSizeOfMatrix != 9:
        raise Exception('I only know how to do 2x2 and 3x3 matrices')

    if lSizeOfMatrix == 4:
        a = pMatrix[0]
        b = pMatrix[1]
        c = pMatrix[2]
        d = pMatrix[3]

        # Calculate determinant of matrix
        return ((a * d) - (b * c)) % pModulus

    if lSizeOfMatrix == 9:
        # For a 3x3 matrix, the determinant can be calculated
        # by the rule of triangles. The value of the determinant is equal to the
        # sum of products of main diagonal elements and products of elements lying
        # on the triangles with side which parallel to the main diagonal, from which
        # subtracted the product of the antidiagonal elements and products of elements
        # lying on the triangles with side which parallel to the anti-diagonal.

        # a   b   c
        # d   e   f
        # g   h   i
        a = pMatrix[0]
        b = pMatrix[1]
        c = pMatrix[2]
        d = pMatrix[3]
        e = pMatrix[4]
        f = pMatrix[5]
        g = pMatrix[6]
        h = pMatrix[7]
        i = pMatrix[8]

        # a11·a22·a33 + a12·a23·a31 + a13·a21·a32 - a13·a22·a31 - a11·a23·a32 - a12·a21·a33
        return ((a * e * i) + (b * f * g) + (c * d * h) - (c * e * g) - (b * d * i) - (a * f * h)) % pModulus


def get_transpose(pMatrix: bytearray, pModulus: int) -> bytearray:
    # The transposed matrix is its reflection about the main diagonal
    # The columns become rows and rows become columns

    lTranspose = bytearray()
    lSizeOfMatrix = len(pMatrix)

    if lSizeOfMatrix != 4 and lSizeOfMatrix != 9:
        raise Exception('I only know how to do 2x2 and 3x3 matrices')

    if lSizeOfMatrix == 4:
        # For 2x2 matrix
        # a   c
        # b   d
        a = pMatrix[0]
        b = pMatrix[1]
        c = pMatrix[2]
        d = pMatrix[3]

        # Calculate adjunct of matrix
        lTranspose.append(a)
        lTranspose.append(c)
        lTranspose.append(b)
        lTranspose.append(d)

    if lSizeOfMatrix == 9:
        # For a 3x3 matrix
        # a   d   g
        # b   e   h
        # c   f   i

        a = pMatrix[0]
        b = pMatrix[1]
        c = pMatrix[2]
        d = pMatrix[3]
        e = pMatrix[4]
        f = pMatrix[5]
        g = pMatrix[6]
        h = pMatrix[7]
        i = pMatrix[8]

        lTranspose.append(a)
        lTranspose.append(d)
        lTranspose.append(g)
        lTranspose.append(b)
        lTranspose.append(e)
        lTranspose.append(h)
        lTranspose.append(c)
        lTranspose.append(f)
        lTranspose.append(i)

    return lTranspose


def get_adjunct(pMatrix: bytearray, pModulus: int) -> bytearray:
    # The adjunct is the transposed matrix of cofactors
    lSizeOfMatrix = len(pMatrix)

    if lSizeOfMatrix != 4 and lSizeOfMatrix != 9:
        raise Exception('I only know how to do 2x2 and 3x3 matrices')

    lCofactors = get_cofactors(pMatrix, pModulus)
    lAdjunct = get_transpose(lCofactors, pModulus)

    return lAdjunct


def get_minors(pMatrix: bytearray, pModulus:int) -> bytearray:
    # The minor of the matrix is found by calculating the
    # determinant of each element of the matrix. An elements
    # determinant is the determinant of the remaining elements
    # after disregarding the row and column in which the element sits
    lMinor = bytearray()
    lSizeOfMatrix = len(pMatrix)

    if lSizeOfMatrix != 4 and lSizeOfMatrix != 9:
        raise Exception('I only know how to do 2x2 and 3x3 matrices')

    if lSizeOfMatrix == 4:
        # For a 2x2 matrix, the minor of an element is the diagonally
        # opposed element
        a = pMatrix[0]
        b = pMatrix[1]
        c = pMatrix[2]
        d = pMatrix[3]

        # Calculate minor of matrix
        lMinor.append(d)
        lMinor.append(c)
        lMinor.append(b)
        lMinor.append(a)

    if lSizeOfMatrix == 9:
        # For a 3x3 matrix, the minor of an element is the diagonally
        # opposed determinant

        # a   b   c
        # d   e   f
        # g   h   i
        a = pMatrix[0]
        b = pMatrix[1]
        c = pMatrix[2]
        d = pMatrix[3]
        e = pMatrix[4]
        f = pMatrix[5]
        g = pMatrix[6]
        h = pMatrix[7]
        i = pMatrix[8]

        # Calculate minors of matrix
        lMinor.append(((e * i) - (f * h)) % pModulus) #a
        lMinor.append(((d * i) - (f * g)) % pModulus) #b
        lMinor.append(((d * h) - (e * g)) % pModulus) #c
        lMinor.append(((b * i) - (c * h)) % pModulus) #d
        lMinor.append(((a * i) - (c * g)) % pModulus) #e
        lMinor.append(((a * h) - (b * g)) % pModulus) #f
        lMinor.append(((b * f) - (c * e)) % pModulus) #g
        lMinor.append(((a * f) - (c * d)) % pModulus) #h
        lMinor.append(((a * e) - (b * d)) % pModulus) #i

    return lMinor


def get_cofactors(pMatrix: bytearray, pModulus: int) -> bytearray:

    lCofactors = bytearray()
    lSizeOfMatrix = len(pMatrix)

    if lSizeOfMatrix != 4 and lSizeOfMatrix != 9:
        raise Exception('I only know how to do 2x2 and 3x3 matrices')

    if lSizeOfMatrix == 4:
        lCofactors = get_minors(pMatrix, pModulus)

        b = lCofactors[1]
        c = lCofactors[2]

        # Calculate cofactors of matrix (negate odd row/col)
        lCofactors[1] = get_int_modulo_n_in_zn(-1 * b, pModulus)
        lCofactors[2] = get_int_modulo_n_in_zn(-1 * c, pModulus)

    if lSizeOfMatrix == 9:
        # For a 3x3 matrix, the minor of an element is the diagonally
        # opposed determinant. The cofactor is the minor when the
        # (column # + row #) is even and -1 * the minor otherwise

        #  a   -b   c
        # -d    e  -f
        #  g   -h   i
        lCofactors = get_minors(pMatrix, pModulus)

        b = lCofactors[1]
        d = lCofactors[3]
        f = lCofactors[5]
        h = lCofactors[7]

        lCofactors[1] = get_int_modulo_n_in_zn(-1 * b, pModulus)
        lCofactors[3] = get_int_modulo_n_in_zn(-1 * d, pModulus)
        lCofactors[5] = get_int_modulo_n_in_zn(-1 * f, pModulus)
        lCofactors[7] = get_int_modulo_n_in_zn(-1 * h, pModulus)

    return lCofactors


def get_inverse_matrix(pMatrix: bytearray, pModulus: int) -> bytearray:

    lInverseMatrix = bytearray()
    lSizeOfMatrix = len(pMatrix)
    if lSizeOfMatrix != 4 and lSizeOfMatrix != 9:
        raise Exception('I only know how to do 2x2 and 3x3 matrices')

    # Calculate adjunct of matrix
    lDeterminant = get_determinant(pMatrix, pModulus)
    if lDeterminant == 0:
        raise Exception('The determinant of the matrix is zero so the matrix cannot be inverted. Inversion requires inverse of the determinant. The inverse of 0 is undefined.')

    lGCD = get_gcd(lDeterminant, pModulus)
    if lGCD != 1:
        raise Exception('For the matrix to be invertible, the inverse of the determinant {} must be calculated (mod {}), but this is not possible since the GCD of the determinant and the modulus is not 1 but {}'.format(lDeterminant, pModulus, lGCD))

    lInverseDeterminant = get_multiplicative_inverse(lDeterminant, pModulus)
    lAdjunct = get_adjunct(pMatrix, pModulus)

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
    lKey = derive_matrix(lArgs.key, lModulus)

    if lArgs.encrypt:

        if lArgs.verbose:
            #if key_is_trivial(lArgs.key):
            #   print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            if key_is_involutary(lKey, lArgs.modulus):
                print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        #endif

