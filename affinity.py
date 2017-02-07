import argparse, base64, sys

MODULUS = 256

def euler_totient_function(pInt: int) -> int:

    lPrimeFactors = primes(pInt)

    lPrimeExponents = []
    lCurrentPrime = [lPrimeFactors[0], 0]
    for lPrime in lPrimeFactors:
        if lCurrentPrime[0] != lPrime:
            lPrimeExponents.append(lCurrentPrime)
            lCurrentPrime = [lPrime, 0]
        lCurrentPrime[1] += 1
    lPrimeExponents.append(lCurrentPrime)

    lPhi = 0
    for p,e in lPrimeExponents:
        lPhi *= (p-1)*(p**(e-1))

    return lPhi

def primes(n: int) -> list:
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


def do_decrypt(pByte: int, pKey: int) -> int:
    #d(x) = (x - k) % n
    a = pKey[0]
    b = pKey[1]
    return (pByte - b) % MODULUS


def encrypt(pPlaintextBytes: bytearray, pKey: int) -> bytearray:
    lEncryptedBytes = bytearray()
    lEncryptedBytes.extend(map(lambda x: do_encrypt(x, pKey), pPlaintextBytes))
    return lEncryptedBytes


def decrypt(pCiphertextBytes: bytearray, pKey: int) -> bytearray:
    lDecryptedBytes = bytearray()
    lDecryptedBytes.extend(map(lambda x: do_decrypt(x, pKey), pCiphertextBytes))
    return lDecryptedBytes


def print_plaintext(pInput: bytearray, pKey: int, pVerbose: bool):

    lDecryptedInput = decrypt(pInput, pKey)

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


def print_ciphertext(pInput: bytearray, pKey: int, pVerbose: bool, pOutputFormat: str):

    lEncryptedInput = encrypt(pInput, pKey)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput): pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


def bruteforce_plaintext(pInput: bytearray, pVerbose: bool):
    for i in range(1, 256):
        print(i,'-> ',end='')
        print_plaintext(pInput, i, pVerbose)
        if not pVerbose: print()


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a KEY.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a KEY or BRUTEFORCE flag.', action='store_true')
    lKeyOrBruteforceActionGroup = lArgParser.add_mutually_exclusive_group(required=True)
    lKeyOrBruteforceActionGroup.add_argument('-k', '--key', help='Encryption/Decryption key in a,b format', type=str, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
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

    if lArgs.encrypt:

        if lArgs.verbose:
            if key_is_trivial(lKey):
                print('[*] Warning: Key {} is trivial'.format(lArgs.key))

            if key_is_involutary(lKey):
                print('[*] Warning: Key {} is involutary'.format(lArgs.key))
        #endif

        a = lKey[0]
        b = lKey[1]

        if abs(a) >= MODULUS:
            lKey[0] = a % MODULUS

        if abs(b) >= MODULUS:
            lKey[1] = b % MODULUS

        for i in range(2,30):
            print(euler_totient_function(i))

        lETF = euler_totient_function(MODULUS)
        lGCD = gcd(a, MODULUS)
        if gcd(a, MODULUS) != 1:
            lArgParser.error("Affine cipher requires the multiplicative key parameter {} be relatively prime to the modulus {}. The GCD of {} and {} is {} rather than 1. Please choose a multiplicative key parameter relatively prime to {}".format(a, MODULUS, a, MODULUS, lGCD, MODULUS))



        # print_ciphertext(lInput, lKey, lArgs.verbose, lArgs.output_format)

    elif lArgs.decrypt:
        if lArgs.bruteforce:
            # Test Case: BEEAKFYDJXUQYHYJIQRYHTYJIQFBQDUYJIIKFUHCQD
            bruteforce_plaintext(lInput, lArgs.verbose)
        else:
            print_plaintext(lInput, lKey, lArgs.verbose)
        # endif
    #endif
