import argparse, base64, sys


def get_relative_primes(pModulus: int) -> list:
    lRelativePrimes = []
    for i in range(1, pModulus):
        if get_gcd(i, pModulus) == 1:
            lRelativePrimes.append(i)
    return lRelativePrimes


# return (g, x, y) a*x + b*y = gcd(x, y)
def extended_euclidian_algorithm(a: int, b: int) -> tuple:
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_euclidian_algorithm(b % a, a)
        return (g, y - (b // a) * x, x)


# x = mulinv(b) mod n, (x * b) % pModulus == 1
def get_multiplicative_inverse(a: int, pModulus: int) -> int:
    g, x, _ = extended_euclidian_algorithm(a, pModulus)
    if g == 1:
        return x % pModulus


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

def derive_key(lKeyString: str) -> bytearray:

    lKey = bytearray(map(int, lKeyString.split(',')))
    for lSubkey in lKey:
        if type(lSubkey) != int:
            raise Exception('Keys not of type integer')

    if abs(lKey[0]) >= lModulus:
        lKey[0] = lKey[0] % lModulus

    if abs(lKey[1]) >= lModulus:
        lKey[1] = lKey[1] % lModulus

    return lKey


def get_involutary_keys(pRelativePrimes: list, pModulus: int) -> list:

    lInvolutaryKeys = []
    for lRelativePrime in lRelativePrimes:
        # Involutary means e(e(x)) = x where e(x) = ax + b. In other words, encrypting twice
        # outputs the original value. This implies
        # e(e(x)) = a(ax + b) + b = x (mod m) => a**2(x) + b(a + 1) = x (mod m)
        # We need a**2 = 1 (mod m) plus b(a + 1) = 0 (mod m)
        # This is true when a**2 = 1 (mod m) and either b = 0 or a = -1 (mod m)
        if ((lRelativePrime ** 2) % pModulus == 1):
            # (pModulus - 1) (mod m) is same as -1 (mod m)
            if (lRelativePrime % pModulus) == (pModulus - 1):
                lInvolutaryKeys.append([lRelativePrime, "Any b in 0-{}".format(pModulus)])
            else:
                for lAdditiveKeyParameter in range(0, pModulus):
                    if (lAdditiveKeyParameter * (lRelativePrime + 1)) % pModulus == 0:
                        lInvolutaryKeys.append([lRelativePrime, lAdditiveKeyParameter])
    return lInvolutaryKeys


def key_is_involutary(pKey: bytearray, pModulus: int) -> bool:
    # Given e(x) = (x + k) % n and d(x) = (x - k) % n
    # Involutary key means e(d(x)) = e(e(x)) = x (mod n)
    # e(e(x)) => a(ax + b) + b = x (mod n) => a^2(x) + ab + b = x (mod n)
    # => a^2(x) + b(a + 1) = x (mod n) =>
    # a^2 = 1 (mod n) AND b(a+1) = 0 (mod n)
    # Note: b(a+1) = 0 (mod n) when b = 0 or when a = -1 (mod n)
    a = pKey[0]
    b = pKey[1]
    return (((a**2) % pModulus) == 1) and ((b * (a + 1)) % pModulus) == 0


def key_is_trivial(pKey: bytearray) -> bool:
    # Given e(x) = (ax + b) % n and d(x) = 1/a(x - b) % n
    # Trival key means e(x) = x (mod n). This happens when a=1 and b=0.
    a = pKey[0]
    b = pKey[1]
    return a == 1 and b == 0


def do_encrypt(pByte: int, pKey: bytearray, pModulus: int) -> int:
    #e(x) = (ax + b) % n
    a = pKey[0]
    b = pKey[1]
    return (a * pByte + b) % pModulus


def do_decrypt(pByte: int, pInverseA: int, pB: int, pModulus: int) -> int:
    #d(x) =  a^-1(x - b) % n
    return (pInverseA * (pByte - pB)) % pModulus


def encrypt(pPlaintextBytes: bytearray, pKey: bytearray, pModulus: int) -> bytearray:
    lEncryptedBytes = bytearray()
    lEncryptedBytes.extend(map(lambda x: do_encrypt(x, pKey, pModulus), pPlaintextBytes))
    return lEncryptedBytes


def decrypt(pCiphertextBytes: bytearray, pa: int, pb: int, pModulus: int) -> bytearray:
    lDecryptedBytes = bytearray()
    lDecryptedBytes.extend(map(lambda x: do_decrypt(x, pa, pb, pModulus), pCiphertextBytes))
    return lDecryptedBytes


def print_plaintext(pInput: bytearray, pKey: bytearray, pModulus:int, pVerbose: bool, pDecodedKey: str) -> None:

    a = pKey[0]
    b = pKey[1]

    lInverseA = get_multiplicative_inverse(a, pModulus)
    lDecryptedInput = decrypt(pInput, lInverseA, b, pModulus)

    if pVerbose:
        print('Key: {}'.format(pDecodedKey))
        print('Modulus: {}'.format(pModulus))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lDecryptedInput)

    if pVerbose: print()


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127: return True
    return False


def print_ciphertext(pInput: bytearray, pKey: bytearray, pModulus:int, pVerbose: bool, pOutputFormat: str, pDecodedKey: str) -> None:

    lEncryptedInput = encrypt(pInput, pKey, pModulus)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput): pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Key: {}'.format(pDecodedKey))
        print('Modulus: {}'.format(pModulus))
        print('Output Format: {}'.format(pOutputFormat))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Affinity: An implementation of the affine cipher system')
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key in a,b format', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store', type=str)
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store', type=str)
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lInputSourceGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lInputSourceGroup.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store', type=str)
    lInputSourceGroup.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    lModulus = lArgs.modulus
    lKey = bytearray()
    lKeyString = str(lArgs.key)

    if (lArgs.encrypt or lArgs.decrypt) and lArgs.key is None:
        lArgParser.error('If -e/--encrypt or -d/--decrypt selected, -k/--key is required')

    if lArgs.key:
        try:
            lKey = derive_key(lKeyString)
        except:
            lArgParser.error("Affine cipher requires two keys of type integer. Input key in a,b format. i.e. --key=1,1")

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
                print('[*] Warning: Key {} is trivial'.format(lKeyString))

            if key_is_involutary(lKey, lModulus):
                print('[*] Warning: Key {} is involutary'.format(lKeyString))
        #endif

        a = lKey[0]
        b = lKey[1]

        lGCD = get_gcd(a, lModulus)
        if lGCD != 1:
            lNumberOfInverses = euler_totient_function(lModulus)
            lRelativePrimes = get_relative_primes(lModulus)
            lNumberPossibleKeys = lNumberOfInverses * lModulus
            lInvolutaryKeys = get_involutary_keys(lRelativePrimes, lModulus)
            lArgParser.error("Affine cipher requires the multiplicative key parameter {} be relatively prime to the modulus {}. "
                             "The GCD of {} and {} is {} rather than 1. Please choose a multiplicative key parameter relatively prime to {}. "
                             "There are {} integers relatively prime to {}. You may pick from {}. "
                             "Since the value of the additive key parameter can be any value between 0 and {} ({} possible values), there are {} * {} = {} possible keys. "
                             "Watch out for involutary keys {}.".format(a, lModulus, a, lModulus, lGCD, lModulus, lNumberOfInverses, lModulus, lRelativePrimes, lModulus - 1, lModulus, lNumberOfInverses, lModulus, lNumberPossibleKeys, lInvolutaryKeys))

        print_ciphertext(lInput, lKey, lModulus, lArgs.verbose, lArgs.output_format, lKeyString)

    elif lArgs.decrypt:
        print_plaintext(lInput, lKey, lModulus, lArgs.verbose, lKeyString)
    #endif
