import argparse


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


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Inversion: inverts elements modulo a modulus')
    lArgParser.add_argument('-i', '--mutiplicative-inverse', help='Calculate multiplicative inverse of INPUT modulo MODULUS', action='store_true')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('INPUT', help='Integer input value of which to calculate inverse. Required.', action='store', type=int)
    lArgs = lArgParser.parse_args()

    lMultiplicativeInverse = (get_multiplicative_inverse(lArgs.INPUT, lArgs.modulus))

    if lArgs.verbose:
        lInverseTimesInput = (lMultiplicativeInverse * lArgs.INPUT) % lArgs.modulus
        print()
        print("Multiplicative inverse of {} modulo {} is {}".format(lArgs.INPUT, lArgs.modulus, lMultiplicativeInverse))
        print("We can verify with {} * {} modulo {} is {}".format(lArgs.INPUT, lMultiplicativeInverse, lArgs.modulus, lInverseTimesInput), end="")
        print()
    else:
        print(lMultiplicativeInverse)
