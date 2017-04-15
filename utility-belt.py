import argparse
import math
from functools import reduce
from itertools import permutations
from argparse import RawTextHelpFormatter


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


def do_lcm(a: int, b: int) -> int:
    # Return least common multiple
    return a * b // get_gcd(a, b)


def get_lcm(pIntegers: list) -> int:
    # Return lcm of args
    return reduce(do_lcm, pIntegers)


def get_permutation_order(pPermutationCycles: list) -> int:
    # The order of a permutation written as the product of disjoint cycles
    # is the least common multiple (lcm) of the lengths of those cycles
    lCycleSizes = []
    for lCycle in pPermutationCycles:
        lCycleSizes.append(len(lCycle))

    return get_lcm(lCycleSizes)


def generate_permutations(pPermutationSize: int) -> list:
    lElements = []
    if pPermutationSize > 0:
        for i in range(0, pPermutationSize):
            lElements.append(i)
        return permutations(lElements)
    else:
        return lElements


# def do_get_permutation_theoretical_cycles(pPermutationSize: int) -> list:
#     # todo
#     lCycle = []
#     lCycles = []
#     if pPermutationSize > 1:
#         for i in range(1, (pPermutationSize // 2) + 1):
#             lCycle = [pPermutationSize - i, i]
#             lCycles.append(lCycle)
#     return lCycles
#
#
# def get_permutation_theoretical_cycles(pPermutationSize: int) -> None:
#     # todo
#     # try to divide into n groups, then n-1 groups, then n-2 groups
#     lCycle = []
#     lCycles = []
#     lNewCycles = []
#     if pPermutationSize > 1:
#         for i in range(1, (pPermutationSize // 2) + 1):
#             lCycle = [pPermutationSize - i, i]
#             lCycles.append(lCycle)
#
#     for lCycle in lCycles:
#         lNewCycles.append([do_get_permutation_theoretical_cycles(lCycle[0]), do_get_permutation_theoretical_cycles(lCycle[1])])
#
#     lCycles.append(lNewCycles)
#     lCycles.append([pPermutationSize])
#
#     print(lCycles)
#
#     return lCycles
#
#
# def get_maximum_permutation_order(pPermutationSize: int) -> int:
#     # todo
#     return 0


# END PERMUTATION FUNCTIONS

# BEGIN MODULAR FUNCTIONS

def get_relative_primes(pModulus: int) -> list:
    lRelativePrimes = []
    for i in range(1, pModulus):
        if get_gcd(i, pModulus) == 1:
            lRelativePrimes.append(i)
    return lRelativePrimes


def get_prime_factors(pComposite: int) -> list:
    lPrimeFactors = []

    # Two is only even prime
    d = 2
    # Count how many times pComposite is divisible by 2
    while (pComposite % d) == 0:
        lPrimeFactors.append(d)
        pComposite //= d

    # Rest of primes are odd numbers. We go faster skipping even numbers
    # We only need to check odd numbers up to square root of n
    d=3
    while d*d <= pComposite:
        while (pComposite % d) == 0:
            lPrimeFactors.append(d)
            pComposite //= d
        d += 2

    if pComposite > 1:
        lPrimeFactors.append(pComposite)

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

def derive_probabilities(pCommaDelimitedProbabilities: str, pVerbose: bool) -> list:

    lProbabilities = list(map(float, pCommaDelimitedProbabilities.split(",")))

    if pVerbose:
        print("The sum of list {} is {}".format(lProbabilities, sum(lProbabilities)))

    return lProbabilities


def print_shannon_entropy_base_2(pCommaDelimitedProbabilities: str, pVerbose: bool) -> None:

    lProbabilities = derive_probabilities(pCommaDelimitedProbabilities, pVerbose)

    lShannonEntropy = 0
    for lProbability in lProbabilities:
        lShannonEntropy += (-1 * lProbability * math.log(lProbability, 2))

    if pVerbose:
        print()
        print("The shannon entropy of probabilities {} is {}".format(lProbabilities, lShannonEntropy))
        print()
    else:
        print(lShannonEntropy)


def derive_congruences(pCongruenceStrings: str) -> list:

    lCongruenceStrings = pCongruenceStrings.split(";")
    lCongruences = []
    for lCongruenceString in lCongruenceStrings:
        lCongruence = list(map(int, lCongruenceString.split(",")))
        lCongruences.append(lCongruence)
    # end for

    return lCongruences


def get_chinese_remainder_theorem(pCongruences: list, pVerbose: bool) -> int:

    # M is product of all moduli
    M = 1
    for lCongruence in pCongruences:
        M *= lCongruence[1]

    if pVerbose:
        print()
        print("M = {}".format(M))
        print()

    # mi is current modulus or the ith modulus
    # Mi is M / mi
    # yi is the multiplicative inverse of Mi mod mi
    # Intersection x is
    #   SUM(ai * Mi * yi) mod M
    # for all pairs of congruences
    x = 0
    for lCongruence in pCongruences:
        ai = lCongruence[0]
        mi = lCongruence[1]
        Mi = int(M / mi)  # guaranteed to be int because mi is a factor of M
        yi = get_multiplicative_inverse(Mi, mi)
        x += ai * Mi * yi
        if pVerbose:
            print("ai = {},\tmi = {},\tMi = M / mi = {} / {} = {},\tyi = {}^-1 modulo {} = {}".format(ai, mi, M, mi, Mi,
                                                                                                      Mi, mi, yi))
    return x % M


def print_chinese_remainder_theorem(pCongruenceStrings: str, pVerbose: bool) -> None:
    # This option ignores MODULUS and treats INPUT is a set of congruences specified by
    # CONSTANT 1, MODULUS 1; CONSTANT 2, MODULUS 2; ...;  CONSTANT N, MODULUS N.
    # For example, the set x = 12 mod 25, x = 9 mod 26, x = 23 mod 27 would be specified as 12, 25; 9, 26; 23, 27

    lCongruences = derive_congruences(pCongruenceStrings)
    lIntersection = get_chinese_remainder_theorem(lCongruences, pVerbose)

    if pVerbose:
        lCongruenceString = ""
        for lCongruence in lCongruences:
            lCongruenceString += "x = {} mod {}\n".format(str(lCongruence[0]), str(lCongruence[1]))
        print()
        print("The intersection x of congruences\n\n{}\nis {}".format(lCongruenceString, lIntersection))
        print()
    else:
        print(lIntersection)

def get_fast_exponentiation(pBase: int, pExponent: int, pModulus: int, pVerbose: bool) -> int:
    # Fast exponentiation: Given the exponent as a bit array, for each bit in the array, calculate
    # the answer for the current bit to be:
    #   if bit is 0: current answer is last answer ^ 2
    #   if bit is 1: current answer is last answer ^ 2 * base
    # The final answer is the answer for the last bit
    # Note: the "first" bit is the MSB and the "last" bit is the LSB

    lExponentBitArray = bin(pExponent)[2:]
    lLastCalculation = 1
    lCurrentCalulation = 0
    for lIndex, lBit in enumerate(lExponentBitArray):
        # Shortcut: Regardless we square the last answer
        lCurrentCalulation = (lLastCalculation ** 2) % pModulus
        # If the exponent bit is 1, we additionally multiply by the base
        if int(lBit) == 1:
            lCurrentCalulation = (lCurrentCalulation * pBase) % pModulus
            if pVerbose:
                print("{}\t{}\t({} ^ 2) * {} mod {} = {}".format(str(lIndex+1), lBit, lLastCalculation, pBase, pModulus, lCurrentCalulation))
        else:
            if pVerbose:
                print("{}\t{}\t({} ^ 2) mod {} = {}".format(str(lIndex+1), lBit, lLastCalculation, pModulus, lCurrentCalulation))
        lLastCalculation = lCurrentCalulation
    # end for

    return lCurrentCalulation


def print_fast_exponentiation(pBase: int, pExponent: int, pModulus: int, pVerbose: bool) -> None:
    # Fast exponentiation: Given the exponent as a bit array, for each bit in the array, calculate
    # the answer for the current bit to be:
    #   if bit is 0: current answer is last answer ^ 2
    #   if bit is 1: current answer is last answer ^ 2 * base
    # The final answer is the answer for the last bit
    # Note: the "first" bit is the MSB and the "last" bit is the LSB

    if pVerbose:
        print("-\t-----\t------")
        print("i\te-bit\tAnswer")
        print("-\t-----\t------")

    lAnswer = get_fast_exponentiation(pBase, pExponent, pModulus, pVerbose)

    if pVerbose:
        print()
        print("{} raised to the {} power modulo {} is {}".format(pBase, pExponent, pModulus, lAnswer))
        print()
        print("{} ^ {} % {} = {}".format(pBase, pExponent, pModulus, lAnswer))
    else:
        print(lAnswer)


def get_generator(pBase: int, pModulus: int, pVerbose: bool) -> tuple:
    # If a base number is a generator with respect to GF(pModulus),
    # raising the base to each of the integers in the ring defined
    # by pModulus (mod pModulus) will result in a permutation containing
    # exactly the (pModulus - 1) integers from 1 to (pModulus - 1)

    # Shortcut: Next member of permutation is the last member generated
    # times the base (mod pModulus). The first member is always the base
    # to the 1st power, which is always the base itself.

    lMembers = []
    lMembers.append(pBase)
    lLastMember = pBase
    for i in range(2, pModulus):
        lCurrentMember = (lLastMember * pBase) % pModulus
        lMembers.append(lCurrentMember)
        # 1 is always the last member generated. If this happens before we calculate exactly
        # (pModulus - 1) members, our permutation is incomplete and pBase is not a generator
        if (i < (pModulus - 1)) and lCurrentMember == 1:
            break
        else:
            lLastMember = lCurrentMember
    # end for i

    return (len(lMembers) == (pModulus - 1)), lMembers


def is_generator(pBase: int, pModulus: int, pVerbose: bool) -> bool:
    # formula is phi(m) = product(from 1 to #prime factors):
    #           (prime-factor(i) - 1) * (prime-factor(i) ^ (exponent(prime-factor(i)) - 1)
    # but for a prime number, there is only one factor besides the number 1
    # so (prime-factor(i) ^ (exponent(prime-factor(i)) - 1) always = 1
    # Therefore (prime-factor(i) - 1) ends up being phi(m)
    lCountRelativePrimesToModulus = pModulus - 1

    # Prime factors of (Modulus - 1)
    lPrimeFactors = get_prime_factors(lCountRelativePrimesToModulus)

    if pModulus < 3:
        return False

    for lPrimeFactor in lPrimeFactors:
        if (pBase**(lCountRelativePrimesToModulus/lPrimeFactor)) % pModulus == 1:
            return False

    return True


def print_generators(pModulus: int, pVerbose: bool) -> None:
    # A generator modulo m is a base (as in base number for exponentiation)
    # that produces all of the numbers in the integer ring Z-MODULUS
    # when the base is raised to the power of all of the numbers in the integer ring Z-MODULUS
    # (one at a time). What results is a permutation of the integer ring.

    # Shortcut: Generators for integer ring defined by Z-MODULUS must be found
    # in set {Z-MODULUS} - set {0,1} since 0 raised to any power is 0 and 1 raised to any
    # power is 1. A result of 1 defines the end of the set.

    if pVerbose:
        # The number of generators for GF(q) is euler_totient_function(q - 1)
        lNumberOfGenerators = euler_totient_function(pModulus - 1)
        print()
        print("The number of generators (primitive roots) for modulus {} is {} (phi({} - 1))".format(pModulus, lNumberOfGenerators, pModulus))
        print()

    for lBase in range(2, pModulus):
        if is_generator(lBase, pModulus, pVerbose):
            lIsGenerator, lMembers = get_generator(lBase, pModulus, pVerbose)
            if lIsGenerator:
                if pVerbose:
                    print("{} is a generator modulo {}".format(lBase, pModulus))
                    print("\tThe members are {}".format(lMembers))
                    for lIndex, lMember in enumerate(lMembers):
                        print("\t{} ^ {} modulo {} = {}".format(lBase, lIndex + 1, pModulus, lMember))
                    print()
                else:
                    print("{} -> {}".format(lBase, lMembers))
                # end if pVerbose
            # end if lIsGenerator
    # end for lBase


#########################
# Permutations          #
#########################
def print_permutation_cycles(pPermutation: list, pPermutationCycles: list, pVerbose: bool) -> None:

    if pVerbose:
        print()
        print("The cycles of permutation {} are {}".format(pPermutation, pPermutationCycles))
        print()
    else:
        print(pPermutationCycles)


def print_permutation_inverse(pPermutation: list, pVerbose: bool) -> None:

    lPermutationInverse = invert_permutation(pPermutation)
    if pVerbose:
        print()
        print("The inverse of permutation {} is {}".format(pPermutation, lPermutationInverse))
        print()
    else:
        print(lPermutationInverse)


def print_permutation_order(pPermutation: list, pPermutationCycles: list, pVerbose: bool) -> None:

    lPermutationOrder = get_permutation_order(pPermutationCycles)
    if pVerbose:
        print()
        print("The order of the permutation {} is {}".format(pPermutation, lPermutationOrder))
        print()
    else:
        print(lPermutationOrder)


def print_permutations(pPermutations: list, pPermutationSize: int, pVerbose: bool) -> None:

    if pVerbose:
        print()
        print("The permutations of size {} are {}".format(pPermutationSize, pPermutations))

    for lPermutation in pPermutations:
        print(lPermutation)

    if pVerbose:
        print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Utility Belt: A variety of functions helpful when studying basic crytography',
                                         epilog='**Calculate relative primes, prime factors and count multiplicative inverses with respect to modulus 26**\n\npython utility-belt.py -rp -pf -cmi -m 26 -v\n\n**Calculate the greatest common divisor and multiplicative inverse of 7 modulo 26. Note that 7 is relatively prime to 26.**\n\npython utility-belt.py -gcd -mi -m 26 -v 7\n\n**Calculate intersection for the set x = 12 mod 25, x = 9 mod 26, x = 23 mod 27**\n\npython utility-belt.py -crt "12,25;9,26;23,27" -v\n\n**Calculate 9726 ^ 3533 % 11413 = 5761 using fast exponentiation**\n\npython utility-belt.py -v -fe 3533 -m 11413 9726\n\n**Calculate all primitive root generators modulo 7**\n\npython utility-belt.py -fg -m 7 -v\n\n**Calculate the Shannon Entropy of probabilities 1/2, 1/3 and 1/6**\n\npython utility-belt.py -se2 -v .5,.33,.165\n\n**Calculate the permutation cycles, permutation order and invert permutation 3,4,2,0,1**\n\npython utility-belt.py -allperms -v 3,4,2,0,1\n\n**Generate permutations of size 5**\n\npython utility-belt.py -gp 5\n\n',
                                         formatter_class=RawTextHelpFormatter)

    lModuloOptions = lArgParser.add_argument_group(title="Options for working in finite fields", description="Choose the options for calulating with respect to a modulus")

    lModuloOptions.add_argument('-rp', '--relative-primes', help='Calculate the relative primes with respect to MODULUS. INPUT is not relevant with respect to this function.', action='store_true')
    lModuloOptions.add_argument('-pf', '--prime-factors', help='Calculate the prime factors with respect to MODULUS. INPUT is not relevant with respect to this function.', action='store_true')
    lModuloOptions.add_argument('-cmi', '--count-multiplicative-inverses', help='Count of multiplicative inverses with respect to MODULUS using Euler Phi function. INPUT is not relevant with respect to this function.', action='store_true')
    lModuloOptions.add_argument('-gcd', '--greatest-common-divisor', help='Calculate the greatest common divisor of INPUT and MODULUS', action='store_true')
    lModuloOptions.add_argument('-mi', '--mutiplicative-inverse', help='Calculate multiplicative inverse of INPUT modulo MODULUS', action='store_true')
    lModuloOptions.add_argument('-fe', '--fast-exponentiation', help='Calculate INPUT raised to this POWER modulo MODULUS. Set -fe/--fast-exponentiation to POWER.', type=int, action='store')
    lModuloOptions.add_argument('-mod', '--modulo', help='Calculate modulo of INPUT modulo MODULUS', action='store_true')
    lModuloOptions.add_argument('-allmods', '--all-modulo-calculations', help='Perform all available calculations of INPUT modulo MODULUS', action='store_true')
    lModuloOptions.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)

    lGaloisFeildOptions = lArgParser.add_argument_group(title="Options for working in Galois Fields", description="Choose the options for calulating with respect to a modulus of a Galois Fields")
    lGaloisFeildOptions.add_argument('-fg', '--find-generators', help='Calculate the generators for field of integers defined by Z-MODULUS', action='store_true')

    lCRTOptions = lArgParser.add_argument_group(title="Options for working with congruences", description="Choose the options for working with congruences")
    lCRTOptions.add_argument('-crt', '--chinese-remainder-theorem', help='Calculate the intersection of the set of congruences. INPUT is a set of congruences specified by CONSTANT 1, MODULUS 1; CONSTANT 2, MODULUS 2; ...;  CONSTANT N, MODULUS N. For example, the set x = 12 mod 25, x = 9 mod 26, x = 23 mod 27 would be specified as 12, 25; 9, 26; 23, 27', action='store_true')

    lShannonEntropyOptions = lArgParser.add_argument_group(title="Options for calculating Shannon Entropy", description="Choose the options for calulating Shannon Entropy")
    lShannonEntropyOptions.add_argument('-se2', '--shannon-entropy-base-2', help='Calculate the base-2 Shannon Entropy for list of probabilities. INPUT must be a comma-delimited list of floating point numbers between 0 and 1. Each of these numbers is the probability of the event occuring. For example 0.5,0.33,0.165 represents 1/2,1/3,1/6. To get meaningful results, the INPUT list must add up to 1.00 within reason.', action='store_true')

    lPermutationOptions = lArgParser.add_argument_group(title="Options for working with Permutations", description="Choose the options for working with Permutations")

    lPermutationOptions.add_argument('-pc', '--permutation-cycles', help='Calculate the permutation cycles of permutation INPUT. INPUT must be a complete set of integers in any order starting from 0.', action='store_true')
    lPermutationOptions.add_argument('-po', '--permutation-order', help='Calculate the order of the permutation INPUT. INPUT must be a complete set of integers in any order starting from 0.', action='store_true')
    lPermutationOptions.add_argument('-ip', '--invert-permutation', help='Calculate the inverse of the permutation INPUT. INPUT must be a complete set of integers in any order starting from 0.', action='store_true')
    lPermutationOptions.add_argument('-allperms', '--all-permutation-calculations', help='Perform all available calculations of permutation INPUT', action='store_true')
    lPermutationOptions.add_argument('-gp', '--generate-permutations', help='Generate permutations of size INPUT. INPUT must be an integer.', action='store_true')
    # lArgParser.add_argument('-tc', '--theoretical-cycles', help='Find the non-redundant cycles of all permutations of size INPUT. INPUT must be an integer.', action='store_true')
    # lArgParser.add_argument('-mo', '--maximum-order', help='Find the maximum order of all permutations of size INPUT. INPUT must be an integer.', action='store_true')

    lOtherOptions = lArgParser.add_argument_group(title="Other Options", description="Choose other options")

    lOtherOptions.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')

    lArgParser.add_argument('INPUT', nargs='?', help='INPUT to analyze', action='store')
    lArgs = lArgParser.parse_args()

    if lArgs.generate_permutations:
        lPermutationSize = int(lArgs.INPUT)
        lPermutations = list(generate_permutations(lPermutationSize))

        if lArgs.generate_permutations:
            print_permutations(lPermutations, lPermutationSize, lArgs.verbose)

        # if lArgs.theoretical_cycles or lArgs.find_maximum_order:

            # lMaxiumumOrder = 0
            # lTheoreticalCycles = get_permutation_theoretical_cycles(lPermutationSize)
                # if lArgs.theoretical_cycles:
                #     print_permutation_theoretical_cycles(lTheoreticalCycles, lArgs.verbose)
                #
                # if lArgs.find_maximum_order:
                #     lMaxiumumOrder = get_maximum_permutation_order(lTheoreticalCycles)
                #     print_maximum_permutation_order(lTheoreticalCycles, lArgs.verbose)

    if lArgs.all_permutation_calculations:
       lArgs.permutation_cycles = lArgs.permutation_order = lArgs.invert_permutation = True

    if lArgs.permutation_cycles or lArgs.invert_permutation:
        try:
            lPermutation = derive_permutation(str(lArgs.INPUT))
        except:
            lArgParser.error('Permutation must be a complete set of integers in any order starting from 0. Examples include 2,1,3,0 and 3,2,0,5,6,7,1,4')

        if lArgs.permutation_cycles or lArgs.permutation_order:

            lPermutationCycles = get_permutation_cycles(lPermutation)

            if lArgs.permutation_cycles:
                print_permutation_cycles(lPermutation, lPermutationCycles, lArgs.verbose)

            if lArgs.permutation_order:
                print_permutation_order(lPermutation, lPermutationCycles, lArgs.verbose)

        if lArgs.invert_permutation:
            print_permutation_inverse(lPermutation, lArgs.verbose)

    elif lArgs.chinese_remainder_theorem:
        print_chinese_remainder_theorem(lArgs.INPUT, lArgs.verbose)

    elif lArgs.shannon_entropy_base_2:
        print_shannon_entropy_base_2(lArgs.INPUT, lArgs.verbose)

    else:
        if lArgs.all_modulo_calculations:
            lArgs.modulo = lArgs.count_multiplicative_inverses = lArgs.greatest_common_divisor = lArgs.modulo = lArgs.mutiplicative_inverse = lArgs.prime_factors = lArgs.relative_primes = True

        lModulus = lArgs.modulus

        # These next three options ignore INPUT
        if lArgs.prime_factors:
            print_prime_factors(lModulus, lArgs.verbose)

        if lArgs.count_multiplicative_inverses:
            print_count_multiplicative_inverses(lModulus, lArgs.verbose)

        if lArgs.relative_primes:
            print_relative_primes(lModulus, lArgs.verbose)

        if lArgs.find_generators:
            print_generators(lModulus, lArgs.verbose)

        # These options require INPUT be the integer on which the calculation is performed
        if lArgs.modulo or lArgs.greatest_common_divisor or lArgs.mutiplicative_inverse or lArgs.fast_exponentiation:

            try:
                lInput = int(lArgs.INPUT)
            except:
                lArgParser.error('When performing calculations with respect to modulus, INPUT must be an integer')

            lNormalizedInput = get_int_modulo_n_in_zn(lInput, lModulus)

            if lArgs.modulo:
                print_modulo(lInput, lModulus, lNormalizedInput, lArgs.verbose)

            if lArgs.fast_exponentiation:
                lExponent = lArgs.fast_exponentiation
                print_fast_exponentiation(lInput, lExponent, lModulus, lArgs.verbose)

            if lArgs.greatest_common_divisor or lArgs.mutiplicative_inverse:
                lGCD = get_gcd(lNormalizedInput, lModulus)

                if lArgs.greatest_common_divisor:
                    print_gcd(lNormalizedInput, lModulus, lGCD, lArgs.verbose)

                if lArgs.mutiplicative_inverse:
                    print_mutiplicative_inverse(lNormalizedInput, lModulus, lGCD, lArgs.verbose)