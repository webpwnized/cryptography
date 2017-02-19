import argparse, math


def derive_key(lKey: str) -> bytearray:
    lKeyMatrix = bytearray()

    # split on comma into bytearray
    lKeyMatrix = bytearray(map(int, lKey.split(',')))

    for lSubkey in lKeyMatrix:
        if type(lSubkey) != int:
            raise Exception('Keys not of type integer')

    lMatrixLength = len(lKeyMatrix)
    if math.sqrt(lMatrixLength) != math.floor(math.sqrt(lMatrixLength)):
        raise Exception('Matrix is not square')

    return lKeyMatrix


# return (g, x, y) a*x + b*y = gcd(x, y)
def extended_euclidian_algorithm(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_euclidian_algorithm(b % a, a)
        return (g, y - (b // a) * x, x)


# x = mulinv(b) mod n, (x * b) % n == 1
def get_multiplicative_inverse(a, n):
    g, x, _ = extended_euclidian_algorithm(a, n)
    if g == 1:
        return x % n


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


def get_adjunct(pMatrix: bytearray, pModulus: list) -> bytearray:

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


def get_determinant(pKey: bytearray, pModulus: int) -> int:

    lSizeOfMatrix = len(pKey)
    if lSizeOfMatrix != 4:
        raise Exception('I dont know how to do non-2x2 matrices yet')

    a = pKey[0]
    b = pKey[1]
    c = pKey[2]
    d = pKey[3]

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
        raise Exception('I only know how to do 2x2 matrices')

    # If key matrix is not invertible, it cannot be involutary
    lDeterminant = get_determinant(pKey, pModulus)
    if lDeterminant == 0:
        return False

    # If key matrix is not invertible, it cannot be involutary
    lGCD = get_gcd(lDeterminant, pModulus)
    if lGCD != 1:
        return False

    # For the matrix to be involutary, it is neccesary the determinant be +/-1 mod n
    lNegative1ModN = pModulus - 1
    if lDeterminant == lNegative1ModN or lDeterminant == 1:
        lInverseKey = get_inverse_matrix(pKey, pModulus)

        lKeyInvolutary = True
        for i in range(0, lSizeOfMatrix):
            if get_int_modulo_n_in_zn(pKey[i], pModulus) != get_int_modulo_n_in_zn(lInverseKey[i], pModulus):
                lKeyInvolutary = False

        return lKeyInvolutary

    return False


def get_count_involutary_keys(pModulus: int) -> int:

    lCountInvolutaryKeys = 0

    for a in range(0, pModulus):
        for b in range(0, pModulus):
            for c in range(0, pModulus):
                for d in range(0, pModulus):
                    lKeyMatrix = bytearray()
                    lKeyMatrix.append(a)
                    lKeyMatrix.append(b)
                    lKeyMatrix.append(c)
                    lKeyMatrix.append(d)
                    if key_is_involutary(lKeyMatrix, pModulus):
                        lCountInvolutaryKeys += 1
    return lCountInvolutaryKeys


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgs = lArgParser.parse_args()

    lCountInvolutaryKeys = get_count_involutary_keys(lArgs.modulus)

    print('There are {} involutary keys modulo {}'.format(lCountInvolutaryKeys, lArgs.modulus))