import argparse


def derive_permutation(pPermutationString: str) -> list:
    lPermutation = list(map(int, pPermutationString.split(',')))

    lPermutationValid = True
    lPermutationLength = len(lPermutation)
    for i in range(0, lPermutationLength):
        if i not in lPermutation:
            lPermutationValid = False
            break
        # end if
    # end for

    if not lPermutationValid:
        raise Exception('Key missing digits')

    return lPermutation


def invert_permutation(pPermutation: list) -> list:
    lInvertedKey = []
    for lIndex, lKeyValue in enumerate(pPermutation):
        lInvertedKey.append(pPermutation.index(lIndex))
    return lInvertedKey


def get_permutation_cycles(pPermutation: list) -> list:

    lKeyLength = len(pPermutation)

    # Arbitrarily start at first byte in key
    lStartPosition = 0
    lCurrentPosition = 0
    lKeyBytesChecked = []
    lCurrentCycle = []
    lCycles = []
    # if value of current byte = position of current byte, then cycle is complete
    for i in range(0, lKeyLength):
        lCurrentCycle.append(pPermutation[lCurrentPosition])
        lKeyBytesChecked.append(pPermutation[lCurrentPosition])
        if pPermutation[lCurrentPosition] == lStartPosition:
            lCycles.append(lCurrentCycle)
            lCurrentCycle = []

            j = 0
            lNextPositionFound = False
            while j < lKeyLength and not lNextPositionFound:
                if pPermutation[j] not in lKeyBytesChecked:
                    lCurrentPosition = j
                    lStartPosition = j
                    lNextPositionFound = True
                j += 1
                # end if
            # end while j
        else:
            lCurrentPosition = pPermutation[lCurrentPosition]
            if i == (lKeyLength - 1):
                # Append last cycle
                lCycles.append(lCurrentCycle)
            # end if
    #end for i

    return lCycles


def get_relative_primes(pModulus: int) -> list:
    lRelativePrimes = []
    for i in range(1, pModulus):
        if get_gcd(i, pModulus) == 1:
            lRelativePrimes.append(i)
    return lRelativePrimes


def get_prime_factors(n: int) -> list:
    lPrimeFactors = []

    #Two is only even prime
    d = 2
    # Count how many times n is divisible by 2
    while (n % d) == 0:
        lPrimeFactors.append(d)
        n //= d

    # Rest of primes are odd numbers. We go faster skipping even numbers
    # We only need to check odd numbers up to square root of n
    d=3
    while d*d <= n:
        while (n % d) == 0:
            lPrimeFactors.append(d)
            n //= d
        d += 2

    if n > 1:
        lPrimeFactors.append(n)

    return lPrimeFactors


def euler_totient_function(pModulus: int) -> int:
    # phi(m) = product(from 1 to #prime factors):
    #           (prime-factor(i) - 1) * (prime-factor(i) ^ (exponent(prime-factor(i)) - 1)
    lPrimeFactors = get_prime_factors(pModulus)

    lPrimeFactorsAndExponents = []
    lCurrentPrime = [lPrimeFactors[0], 0]
    for lPrime in lPrimeFactors:
        if lCurrentPrime[0] != lPrime:
            lPrimeFactorsAndExponents.append(lCurrentPrime)
            lCurrentPrime = [lPrime, 0]
        lCurrentPrime[1] += 1
    lPrimeFactorsAndExponents.append(lCurrentPrime)

    lPhi = 1
    for p,e in lPrimeFactorsAndExponents:
        lPhi *= (p-1)*(p**(e-1))

    return lPhi


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


def get_int_modulo_n_in_zn(pInt: int, pModulus: int) -> int:
    lAModuloN = pInt % pModulus
    if lAModuloN < 0:
        lAModuloN = pModulus + lAModuloN
    return lAModuloN


def print_modulo(pInput: int, pModulus: int, pNormalizedInput: int, pVerbose: bool) -> None:

    if pVerbose:
        print()
        print("{} modulo {} is {}".format(pInput, pModulus, pNormalizedInput))
        print()
    else:
        print(pNormalizedInput)


def print_gcd(pNormalizedInput: int, pModulus: int, pGCD: int, pVerbose: bool) -> None:

    if pVerbose:
        print()
        print("The greatest common divisor of {} and modulo {} is {}".format(pNormalizedInput, pModulus, pGCD))
        print()
    else:
        print(pGCD)


def print_prime_factors(pModulus: int, pVerbose: bool) -> None:

    lPrimeFactors = get_prime_factors(pModulus)
    if pVerbose:
        print()
        print("The prime factors of modulus {} is {}".format(pModulus, lPrimeFactors))
        print()
    else:
        print(lPrimeFactors)


def print_count_multiplicative_inverses(pModulus: int, pVerbose: bool) -> None:

    lCountOfMultiplicativeInverses = euler_totient_function(pModulus)
    if pVerbose:
        print()
        print("The number of multiplicative inverses modulo {} is {}".format(pModulus, lCountOfMultiplicativeInverses))
        print()
    else:
        print(lCountOfMultiplicativeInverses)


def print_relative_primes(pModulus: int, pVerbose: bool) -> None:

    lRelativePrimes = get_relative_primes(pModulus)
    if pVerbose:
        print()
        print("The integers relatively prime to modulus {} are {}".format(pModulus, lRelativePrimes))
        print()
    else:
        print(lRelativePrimes)


def print_mutiplicative_inverse(pNormalizedInput: int, pModulus: int, pGCD: int, pVerbose: bool) -> None:

    if lGCD == 1:
        lMultiplicativeInverse = (get_multiplicative_inverse(pNormalizedInput, pModulus))

        if pVerbose:
            lInverseTimesInput = (lMultiplicativeInverse * pNormalizedInput) % pModulus
            print()
            print("The multiplicative inverse of {} modulo {} is {}".format(pNormalizedInput, pModulus,
                                                                            lMultiplicativeInverse))
            print(
                "We can verify with {} * {} modulo {} is {}".format(pNormalizedInput, lMultiplicativeInverse, pModulus,
                                                                    lInverseTimesInput), end="")
            print()
        else:
            print(lMultiplicativeInverse)
    else:
        if pVerbose:
            print()
            print("The multiplicative inverse of {} modulo {} does not exist. "
                  "The GCD of {} and {} is {}. To calculate multiplicative inverse, "
                  "the GCD must be 1.".format(pNormalizedInput, pModulus, pNormalizedInput, pModulus, pGCD))
            print()
        else:
            print("NaN")


def print_permutation_cycles(pPermutation: list, pVerbose: bool) -> None:

    lPermutationCycles = get_permutation_cycles(pPermutation)
    if pVerbose:
        print()
        print("The cycles of permutation {} are {}".format(pPermutation, lPermutationCycles))
        print()
    else:
        print(lPermutationCycles)


def print_permutation_inverse(pPermutation: list, pVerbose: bool) -> None:

    lPermutationInverse = invert_permutation(pPermutation)
    if pVerbose:
        print()
        print("The inverse of permutation {} is {}".format(pPermutation, lPermutationInverse))
        print()
    else:
        print(lPermutationInverse)


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Utility Belt: A variety of functions helpful when studying basic crytography')
    lArgParser.add_argument('-rp', '--relative-primes', help='Calculate the relative primes with respect to MODULUS. INPUT is not relevant with respect to this function.', action='store_true')
    lArgParser.add_argument('-pf', '--prime-factors', help='Calculate the prime factors with respect to MODULUS. INPUT is not relevant with respect to this function.', action='store_true')
    lArgParser.add_argument('-cmi', '--count-multiplicative-inverses', help='Count of multiplicative inverses with respect to MODULUS using Euler Phi function. INPUT is not relevant with respect to this function.', action='store_true')
    lArgParser.add_argument('-gcd', '--greatest-common-divisor', help='Calculate the greatest common divisor of INPUT and MODULUS', action='store_true')
    lArgParser.add_argument('-mi', '--mutiplicative-inverse', help='Calculate multiplicative inverse of INPUT modulo MODULUS', action='store_true')
    lArgParser.add_argument('-mod', '--modulo', help='Calculate modulo of INPUT modulo MODULUS', action='store_true')
    lArgParser.add_argument('-allmods', '--all-modulo-calculations', help='Perform all available calculations of INPUT modulo MODULUS', action='store_true')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgParser.add_argument('-pc', '--permutation-cycles', help='Calculate the permutation cycles relative to INPUT. INPUT must be a complete set of integers in any order starting from 0.', action='store_true')
    lArgParser.add_argument('-ip', '--invert-permutation', help='Calculate the inverse of the permutation INPUT. INPUT must be a complete set of integers in any order starting from 0.', action='store_true')
    lArgParser.add_argument('-allperms', '--all-permutation-calculations', help='Perform all available calculations of permutation INPUT', action='store_true')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('INPUT', help='Integer input value of which to calculate answer. Required. This program will normalize values outside of Z-modulus. For example, -1 mod 26 will be converted to 25.', action='store', type=str)
    lArgs = lArgParser.parse_args()

    if lArgs.all_permutation_calculations:
       lArgs.permutation_cycles = lArgs.invert_permutation = True

    if lArgs.permutation_cycles or lArgs.invert_permutation:
        try:
            lPermutation = derive_permutation(str(lArgs.INPUT))
        except:
            lArgParser.error('Permutation must be a complete set of integers in any order starting from 0. Examples include 2,1,3,0 and 3,2,0,5,6,7,1,4')

        if lArgs.permutation_cycles:
            print_permutation_cycles(lPermutation, lArgs.verbose)

        if lArgs.invert_permutation:
            print_permutation_inverse(lPermutation, lArgs.verbose)

    else:
        if lArgs.all_modulo_calculations:
            lArgs.modulo = lArgs.count_multiplicative_inverses = lArgs.greatest_common_divisor = lArgs.modulo = lArgs.mutiplicative_inverse = lArgs.prime_factors = lArgs.relative_primes = True

        try:
            lInput = int(lArgs.INPUT)
        except:
            lArgParser.error('When performing calculations with respect to modulus, INPUT must be an integer')

        lModulus = lArgs.modulus
        lNormalizedInput = get_int_modulo_n_in_zn(lInput, lModulus)

        if lArgs.modulo:
            print_modulo(lInput, lModulus, lNormalizedInput, lArgs.verbose)

        if lArgs.greatest_common_divisor or lArgs.mutiplicative_inverse:
            lGCD = get_gcd(lNormalizedInput, lModulus)

            if lArgs.greatest_common_divisor:
                print_gcd(lNormalizedInput, lModulus, lGCD, lArgs.verbose)

            if lArgs.mutiplicative_inverse:
                print_mutiplicative_inverse(lNormalizedInput, lModulus, lGCD, lArgs.verbose)

        if lArgs.prime_factors:
            print_prime_factors(lModulus, lArgs.verbose)

        if lArgs.count_multiplicative_inverses:
            print_count_multiplicative_inverses(lModulus, lArgs.verbose)

        if lArgs.relative_primes:
            print_relative_primes(lModulus, lArgs.verbose)