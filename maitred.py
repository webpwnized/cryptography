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


def get_minors(pMatrix: bytearray) -> bytearray:

    lMinor = bytearray()
    lSizeOfMatrix = len(pMatrix)

    if lSizeOfMatrix != 4:
        raise Exception('I dont know how to do non-2x2 matrices yet')

    a = pMatrix[0]
    b = pMatrix[1]
    c = pMatrix[2]
    d = pMatrix[3]

    # Calculate minor of matrix
    lMinor.append(d)
    lMinor.append(c)
    lMinor.append(b)
    lMinor.append(a)

    return lMinor


def get_cofactors(pMatrix: bytearray, pModulus: int) -> bytearray:

    lCofactors = bytearray()
    lSizeOfMatrix = len(pMatrix)

    if lSizeOfMatrix != 4:
        raise Exception('I dont know how to do non-2x2 matrices yet')

    a = pMatrix[0]
    b = pMatrix[1]
    c = pMatrix[2]
    d = pMatrix[3]

    # Calculate cofactors of matrix
    lCofactors.append(d)
    lCofactors.append(get_int_modulo_n_in_zn(-1 * c, pModulus))
    lCofactors.append(get_int_modulo_n_in_zn(-1 * b, pModulus))
    lCofactors.append(a)

    return lCofactors


def get_determinant(pMatrix: bytearray, pModulus: int) -> int:

    lSizeOfMatrix = len(pMatrix)
    if lSizeOfMatrix != 4:
        raise Exception('I do not know how to do non-2x2 matrices yet')

    a = pMatrix[0]
    b = pMatrix[1]
    c = pMatrix[2]
    d = pMatrix[3]

    # Calculate determinant of matrix
    return ((a * d) - (b * c)) % pModulus


def get_inverse_matrix(pMatrix: bytearray, pModulus: int) -> bytearray:

    lInverseMatrix = bytearray()
    lSizeOfMatrix = len(pMatrix)
    if lSizeOfMatrix != 4:
        raise Exception('I do not know how to do non-2x2 matrices yet')

    # Calculate adjunct of matrix
    lAdjunct = get_adjunct(pMatrix, pModulus)
    lDeterminant = get_determinant(pMatrix, pModulus)
    lInverseDeterminant = get_multiplicative_inverse(lDeterminant, pModulus)

    for i in range(0, lSizeOfMatrix):
        lInverseMatrix.append(get_int_modulo_n_in_zn(lInverseDeterminant * lAdjunct[i], pModulus))

    return lInverseMatrix


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Maitre D: A matrix variant calculator within modulo MODULUS')
    lArgParser.add_argument('-d', '--determinant', help='Calculate the determinant of the matrix modulo MODULUS. Answer will be in Z-MODULUS.', action='store_true')
    lArgParser.add_argument('-id', '--inverse-determinant', help='Calculate the inverse of the determinant of the matrix modulo MODULUS. Answer will be in Z-MODULUS.', action='store_true')
    lArgParser.add_argument('-mi', '--minors', help='Calculate the minors of the matrix modulo MODULUS', action='store_true')
    lArgParser.add_argument('-c', '--cofactors', help='Calculate the cofactors of the matrix modulo MODULUS', action='store_true')
    lArgParser.add_argument('-a', '--adjunct', help='Calculate the adjunct of the matrix modulo MODULUS', action='store_true')
    lArgParser.add_argument('-i', '--inverse', help='Calculate the inverse of the matrix modulo MODULUS', action='store_true')
    lArgParser.add_argument('-all', '--all', help='Calculate the determinant, inverse determinant, adjunct and inverse of the matrix modulo MODULUS. Same as -id -dai', action='store_true')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgParser.add_argument('INPUT', nargs='?', help='Input matrix of integers. The matrix must be square. For example a 2 X 2 matrix could be 1, 2, 3, 4', type=str, action='store')
    lArgs = lArgParser.parse_args()

    lModulus = lArgs.modulus
    lMatrix = derive_matrix(lArgs.INPUT, lModulus)
    lDeterminant = 0

    if lArgs.all:
        lArgs.determinant = lArgs.inverse_determinant = lArgs.minors = lArgs.cofactors = lArgs.adjunct = lArgs.inverse = True

    if lArgs.verbose:
        print()
        print('Matrix (mod {}):'.format(lModulus))
        print_matrix(lMatrix)

    if lArgs.determinant or lArgs.inverse_determinant:
        lDeterminant = get_determinant(lMatrix, lModulus)

    if lArgs.determinant:
        if lArgs.verbose:
            print('Determinant of Matrix (mod {}): '.format(lModulus), end='')
        print(lDeterminant)
        if lArgs.verbose:
            print()

    if lArgs.inverse_determinant:
        lInverseDeterminant = get_multiplicative_inverse(lDeterminant, lModulus)
        if lArgs.verbose:
            print('Inverse of the determinant of Matrix (mod {}): '.format(lModulus), end='')
        print(lInverseDeterminant)
        if lArgs.verbose:
            print()

    if lArgs.minors:
        lMinorsMatrix = get_minors(lMatrix)
        if lArgs.verbose:
            print('Minors Matrix (mod {}): '.format(lModulus))
        print_matrix(lMinorsMatrix)

    if lArgs.cofactors:
        lCofactorsMatrix = get_cofactors(lMatrix, lModulus)
        if lArgs.verbose:
            print('Cofactors Matrix (mod {}): '.format(lModulus))
        print_matrix(lCofactorsMatrix)

    if lArgs.adjunct:
        lAdjunctMatrix = get_adjunct(lMatrix, lModulus)
        if lArgs.verbose:
            print('Adjunct Matrix (mod {}): '.format(lModulus))
        print_matrix(lAdjunctMatrix)

    if lArgs.inverse:
        lInverseMatrix = get_inverse_matrix(lMatrix, lModulus)
        if lArgs.verbose:
            print('Inverse Matrix: (mod {}): '.format(lModulus))
        print_matrix(lInverseMatrix)
