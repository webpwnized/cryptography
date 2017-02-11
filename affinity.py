import argparse, base64, sys

MODULUS = 256


# return (g, x, y) a*x + b*y = gcd(x, y)
def extended_euclidian_algorithm(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_euclidian_algorithm(b % a, a)
        return (g, y - (b // a) * x, x)


# x = mulinv(b) mod n, (x * b) % n == 1
def get_multiplicative_inverse(b, n):
    g, x, _ = extended_euclidian_algorithm(b, n)
    if g == 1:
        return x % n


def euler_totient_function(pInt: int) -> int:

    lPrimeFactors = get_prime_factors(pInt)

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
    while (n % d) == 0:
        lPrimeFactors.append(d)
        n //= d

    # Rest of primes are odd numbers. We go faster skipping even numbers
    d=3
    while d*d <= n:
        while (n % d) == 0:
            lPrimeFactors.append(d)
            n //= d
        d += 2

    if n > 1:
        lPrimeFactors.append(n)

    return lPrimeFactors


def gcd(x: int, y: int) -> int:
    if y > x:
        #Swap the arguments
        return gcd(y, x)

    if x % y == 0:
        #y divides a evenly so y is gcd(x, y)
        return y

    # We can make calculating GCD easier.
    # The GCD of a,b is the same as the GCD of a and the remainder of dividing a by b
    return gcd(y, x % y)


def key_is_involutary(pKey: bytearray) -> bool:
    # Given e(x) = (x + k) % n and d(x) = (x - k) % n
    # Involutary key means e(d(x)) = e(e(x)) = x (mod n)
    # e(e(x)) => a(ax + b) + b = x (mod n) => a^2(x) + ab + b = x (mod n)
    # => a^2(x) + b(a + 1) = x (mod n) =>
    # a^2 = 1 (mod n) AND b(a+1) = 0 (mod n)
    a = pKey[0]
    b = pKey[1]
    return (((a**2) % MODULUS) == 1) and ((b * (a + 1)) % MODULUS) == 0


def key_is_trivial(pKey: bytearray) -> bool:
    # Given e(x) = (ax + b) % n and d(x) = 1/a(x - b) % n
    # Trival key means e(x) = x (mod n). This happens when a=1 and b=0.
    a = pKey[0]
    b = pKey[1]
    return a == 1 and b == 0


def do_encrypt(pByte: int, pKey: bytearray) -> int:
    #e(x) = (x + k) % n
    a = pKey[0]
    b = pKey[1]
    return (a * pByte + b) % MODULUS


def do_decrypt(pByte: int, pa: int, pb: int) -> int:
    #d(x) = (x - k) % n
    return (pa * (pByte - pb)) % MODULUS


def encrypt(pPlaintextBytes: bytearray, pKey: int) -> bytearray:
    lEncryptedBytes = bytearray()
    lEncryptedBytes.extend(map(lambda x: do_encrypt(x, pKey), pPlaintextBytes))
    return lEncryptedBytes


def decrypt(pCiphertextBytes: bytearray, pa: int, pb: int) -> bytearray:
    lDecryptedBytes = bytearray()
    lDecryptedBytes.extend(map(lambda x: do_decrypt(x, pa, pb), pCiphertextBytes))
    return lDecryptedBytes


def print_plaintext(pInput: bytearray, pKey: int, pVerbose: bool, pDecodedKey: str) -> None:

    a = pKey[0]
    b = pKey[1]

    inverse_a = get_multiplicative_inverse(a, MODULUS)
    lDecryptedInput = decrypt(pInput, inverse_a, b)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lDecryptedInput)

    if pVerbose: print()


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127: return True
    return False


def print_ciphertext(pInput: bytearray, pKey: int, pVerbose: bool, pOutputFormat: str, pDecodedKey: str) -> None:

    lEncryptedInput = encrypt(pInput, pKey)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput): pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Key: {}'.format(pDecodedKey))
        print('Output Format: {}'.format(pOutputFormat))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key in a,b format', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lArgParser.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if (lArgs.encrypt or lArgs.decrypt) and lArgs.key is None:
        lArgParser.error('If -e/--encrypt or -d/--decrypt selected, -k/--key is required')

    if lArgs.key:
        try:
            lKey = bytearray(map(int, lArgs.key.split(',')))
            for lSubkey in lKey:
                if type(lSubkey) != int:
                    raise Exception('Keys not of type integer')

            if abs(lKey[0]) >= MODULUS:
                lKey[0] = lKey[0] % MODULUS

            if abs(lKey[1]) >= MODULUS:
                lKey[1] = lKey[1] % MODULUS
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
                print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            if key_is_involutary(lKey):
                print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        #endif

        a = lKey[0]
        b = lKey[1]

        lGCD = gcd(a, MODULUS)
        if lGCD != 1:
            lNumberOfInverses = euler_totient_function(MODULUS)
            lRelativePrimes = []
            for i in range(1,MODULUS):
                if gcd(i, MODULUS) == 1:
                    lRelativePrimes.append(i)
            lNumberPossibleKeys = lNumberOfInverses * MODULUS
            lArgParser.error("Affine cipher requires the multiplicative key parameter {} be relatively prime to the modulus {}. The GCD of {} and {} is {} rather than 1. Please choose a multiplicative key parameter relatively prime to {}. There are {} integers relatively prime to {}. You may pick from {}. Since the value of the additive key parameter can be any value between 0 and {}, there are {} possible keys.".format(a, MODULUS, a, MODULUS, lGCD, MODULUS, lNumberOfInverses, MODULUS, lRelativePrimes, MODULUS, lNumberPossibleKeys))

        print_ciphertext(lInput, lKey, lArgs.verbose, lArgs.output_format, lArgs.key)

    elif lArgs.decrypt:
        print_plaintext(lInput, lKey, lArgs.verbose, lArgs.key)
    #endif
