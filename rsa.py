import argparse, base64, sys, math
from argparse import RawTextHelpFormatter

SIZE_OF_ALPHABET = 256
PADDING_INDICATION_BLOCK_LENGTH = 10


def get_padblock() -> bytearray:
    lPadBlock = bytearray()
    for i in range(0, PADDING_INDICATION_BLOCK_LENGTH):
        lPadBlock.append(i)
    return lPadBlock


def key_is_involutary(pKey: int, pModulus:int) -> bool:
    # Involutary key means e(d(x)) = e(e(x)) = x (mod n)
    # This happens when key is 1 (mod n) or when the
    # encryption exponent is its own inverse
    return (pKey % pModulus) == 1


def key_is_trivial(pKey: int, pModulus:int) -> bool:
    # Trival key means e(x) = x (mod n)
    # This happens when key is 1 (mod n)
    return (pKey % pModulus) == 1


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


def is_prime(n):
    # check if integer n is a prime

    # make sure n is a positive integer
    n = abs(int(n))

    # 0 and 1 are not primes
    if n < 2:
        return False

    # 2 is the only even prime number
    if n == 2:
        return True

    # all other even numbers are not primes
    if not n & 1:
        return False

    # range starts with 3 and only needs to go up
    # the square root of n for all odd numbers
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False

    return True


def get_next_prime(pLowerLimit: int) -> int:
    # Finds the next prime number higher than pLowerLimit
    pLowerLimit += 1

    # ensure lower limit is odd
    if (pLowerLimit % 2) == 0:
        pLowerLimit += 1

    # check each odd number to see if prime
    while not is_prime(pLowerLimit):
        pLowerLimit += 2

    return pLowerLimit


def get_fast_exponentiation(pBase: int, pExponent: int, pModulus: int) -> int:
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
        lLastCalculation = lCurrentCalulation
    # end for

    return lCurrentCalulation


def do_encrypt(pByte: int, pKey: int, pModulus:int) -> int:
    #e(x) = (x + k) % n
    return (pByte + pKey) % pModulus


def do_decrypt(pByte: int, pKey: int, pModulus:int) -> int:
    #d(x) = (x - k) % n
    return (pByte - pKey) % pModulus


def encode(pBytes: bytearray) -> int:
    # Coding scheme converts BLOCKSIZE bytes into a number based on position of the byte
    # Each byte is "worth" (byte value) * 256**POSITION where POSITION is the 0-based
    # position reading from right to left
    # "ABCD" = 65 66 67 68 so coding is 65 * 256**3 + 66 * 256**2 + 67 * 256**1 + 68 * 256**0

    lCode = 0
    lExponenet = 0
    for lByte in reversed(pBytes):
        lCode += lByte * (SIZE_OF_ALPHABET**lExponenet)
        lExponenet += 1

    return lCode


def decode(pCode: int, pBlocksize: int) -> bytearray:
    # Coding scheme converts BLOCKSIZE bytes into a number based on position of the byte
    # Each byte is "worth" (byte value) * 256**POSITION where POSITION is the 0-based
    # position reading from right to left
    # "ABCD" = 65 66 67 68 so coding is 65 * 256**3 + 66 * 256**2 + 67 * 256**1 + 68 * 256**0 = 1094861636

    lDecodedBytes = bytearray()
    lByte = 0
    for lExponenet in range(0, pBlocksize):
        lByte = int(pCode % SIZE_OF_ALPHABET)
        pCode = int(((pCode - lByte) / SIZE_OF_ALPHABET))
        lDecodedBytes.append(lByte)

    lDecodedBytes.reverse()

    return lDecodedBytes


def encrypt(pPlaintextBytes: bytearray, pKey: int, pBlocksize: int, pModulus:int) -> bytearray:
    # x: plaintext blocks of BLOCKSIZE bytes
    # p: secret prime number
    # q: secret prime number
    # n: modulus = p * q
    # phi(n): euler number of n = (p - 1) * (q - 1)
    # b: encryption exponent portion of public key
    # a: decryption exponent portion of private key, a must be the multiplicative inverse of b modulo phi(n)
    # a * b mod phi(n) = 1 (a*b is congruent to 1 modulo phi(n))
    # e(x) = x**b mod n
    # d(x) = x**a mod n

    lEncryptedBytes = bytearray()
    lBytesOfPlaintext = len(pPlaintextBytes)

    # Calculate amount of padding needed
    lLengthLastBlock = lBytesOfPlaintext % pBlocksize
    lPadBytesNeeded = (pBlocksize - lLengthLastBlock) % pBlocksize

    # Append number of pad bytes needed to end of plaintext |pad bytes| times
    if lPadBytesNeeded > 0:
        for i in range(0, lPadBytesNeeded):
            pPlaintextBytes.append(lPadBytesNeeded)
        lBytesOfPlaintext += lPadBytesNeeded

    for lBytePosition in range(0, lBytesOfPlaintext, pBlocksize):
        lCode = encode(pPlaintextBytes[lBytePosition:lBytePosition+pBlocksize])
        lEncryptedCode = get_fast_exponentiation(lCode, pKey, pModulus)
        lDecodedByteArray = decode(lEncryptedCode, pBlocksize)
        lEncryptedBytes.extend(lDecodedByteArray)

    # If plaintext was padding, mark the end so decryption routine knows
    if lPadBytesNeeded > 0:
        lEncryptedBytes.extend(get_padblock())

    return lEncryptedBytes


def decrypt(pCiphertextBytes: bytearray, pKey: int, pBlocksize: int, pModulus:int) -> bytearray:
    # x: plaintext blocks of BLOCKSIZE bytes
    # p: secret prime number
    # q: secret prime number
    # n: modulus = p * q
    # phi(n): euler number of n = (p - 1) * (q - 1)
    # b: encryption exponent portion of public key
    # a: decryption exponent portion of private key, a must be the multiplicative inverse of b modulo phi(n)
    # a * b mod phi(n) = 1 (a*b is congruent to 1 modulo phi(n))
    # e(x) = x**b mod n
    # d(x) = x**a mod n

    lDecryptedBytes = bytearray()
    lBytesOfCiphertext = len(pCiphertextBytes)

    # Adjustments needed if plaintext block was padded before encryption
    lStartPaddingIndicationBlock = lBytesOfCiphertext - PADDING_INDICATION_BLOCK_LENGTH
    lEndPaddingIndicationBlock = lBytesOfCiphertext
    lPaddingDetected = False
    lPadBlock = get_padblock()
    lPadBytesNeeded = 0

    if pCiphertextBytes[lStartPaddingIndicationBlock:lEndPaddingIndicationBlock] == lPadBlock:
        lPaddingDetected = True
        lBytesOfCiphertext -= PADDING_INDICATION_BLOCK_LENGTH

    # Decryption
    for lBytePosition in range(0, lBytesOfCiphertext, pBlocksize):
        lCode = encode(pCiphertextBytes[lBytePosition:lBytePosition+pBlocksize])
        lDecryptedCode = get_fast_exponentiation(lCode, pKey, pModulus)
        lDecodedByteArray = decode(lDecryptedCode, pBlocksize)
        lDecryptedBytes.extend(lDecodedByteArray)

    # If padding occured, the amount needed is the value of the pad byte itself
    if lPaddingDetected:
        lPadBytesNeeded = lDecryptedBytes[lBytesOfCiphertext-1]

    return lDecryptedBytes[0:lBytesOfCiphertext-lPadBytesNeeded]


def print_plaintext(pInput: bytearray, pKey: int, pBlocksize: int, pModulus:int, pVerbose: bool) -> None:

    lDecryptedInput = decrypt(pInput, pKey, pBlocksize, pModulus)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Modulus: {}'.format(pModulus))
        print('Plaintext Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lDecryptedInput)

    if pVerbose: print()


def is_unprintable(pBytes: bytearray) -> bool:
    for x in pBytes:
        if x > 127: return True
    return False


def print_ciphertext(pInput: bytearray, pKey: int, pBlocksize: int, pModulus:int, pVerbose: bool, pOutputFormat: str) -> None:

    lEncryptedInput = encrypt(pInput, pKey, pBlocksize, pModulus)

    if pOutputFormat == 'character' and is_unprintable(lEncryptedInput): pOutputFormat = 'base64'

    if pOutputFormat == 'base64':
        lEncryptedInput = base64.b64encode(lEncryptedInput)

    if pVerbose:
        print('Key: {}'.format(pKey))
        print('Modulus: {}'.format(pModulus))
        print('Output Format: {}'.format(pOutputFormat))
        print('Cipher Output: ', end='')

    sys.stdout.flush()
    sys.stdout.buffer.write(lEncryptedInput)

    if pVerbose: print()


def print_next_prime(pLowerLimit: int, pVerbose: bool) -> None:

    lNextPrime = get_next_prime(pLowerLimit)
    if lArgs.verbose:
        print("The next prime number after {} is {}".format(pLowerLimit, lNextPrime))
    else:
        print(lNextPrime)
    # end if


def print_is_prime(pCandidate: int, pVerbose: bool) -> None:

    lIsPrime = is_prime(pCandidate)
    if lArgs.verbose:
        print("The number {} is {}".format(pCandidate, "prime" if lIsPrime else "not prime"))
    else:
        print(lIsPrime)
    # end if


def print_suggested_primes(pLowerLimit: int, pVerbose: bool) -> None:

    if lArgs.suggest_primes:
        lSquareRoot = int(math.sqrt(pLowerLimit))
        lFirstPrime = get_next_prime(lSquareRoot)
        lSecondPrime = get_next_prime(lFirstPrime)
        if lArgs.verbose:
            print("The next two prime numbers whos product is greater than {} are {} and {}. {} x {} = {}".format(pLowerLimit, lFirstPrime, lSecondPrime, lFirstPrime, lSecondPrime, lFirstPrime * lSecondPrime))
        else:
            print(lFirstPrime)
            print(lSecondPrime)
        # end if

def print_private_key(pEncryptionExponent: int, pPQString: str, pVerbose: bool) -> None:

    p, q = map(int, pPQString.split(","))

    if not is_prime(p):
        raise Exception('The value P must be prime.')

    if not is_prime(q):
        raise Exception('The value Q must be prime.')

    # phi(m) = product(from 1 to #prime factors):
    #           (prime-factor(i) - 1) * (prime-factor(i) ^ (exponent(prime-factor(i)) - 1)
    # However, for any prime number, the prime factors are 1 and that number. Therefore,
    #   phi(prime) = (prime - 1) * (prime-factor(i) ^ (0)) =  prime - 1
    # if m = p * q where p and q are prime, phi(m) = phi(p) * phi(q) by same formula
    lPhiP = p - 1
    lPhiQ = q - 1
    lModulus = p * q
    lPhiModulus = lPhiP * lPhiQ
    lGCD = get_gcd(pEncryptionExponent, lPhiModulus)

    if pVerbose:
        print("p: {}".format(p))
        print("q: {}".format(q))
        print("modulus (p * q): {}".format(lModulus))
        print("phi(p) = p - 1: {}".format(lPhiP))
        print("phi(q) = q - 1: {}".format(lPhiQ))
        print("phi(modulus) = phi(p) * phi(q): {}".format(lPhiModulus))
        print("GCD(encryption exponenet, phi(modulus)): {}".format(lGCD))

    if (lGCD != 1):
        lNumberOfRelativePrimes = euler_totient_function(lPhiModulus)
        lErrorMessage = 'The encryption exponent must be relative prime to phi(modulus) which is phi(p) * phi(q) ({} * {} = {}). {} is not relatively prime to {} since the greatest common divisor of {} and {} is {}. The number of relative primes is {}. Please try a different encryption exponent.'.format(lPhiP, lPhiQ, lPhiModulus, lKey, lPhiModulus, lKey, lPhiModulus, lGCD, lNumberOfRelativePrimes)
        raise Exception(lErrorMessage)

    lPrivateKeyExponent = get_multiplicative_inverse(pEncryptionExponent, lPhiModulus)

    if pVerbose:
        print("Encryption Exponent: {}".format(pEncryptionExponent))
        print("Decryption Exponent (multiplicative inverse of {} modulo {}): {}".format(pEncryptionExponent, lPhiModulus, lPrivateKeyExponent))
        print("Public Key: (The encryption exponent and the modulus): {}, {}".format(pEncryptionExponent, lModulus))
        print("Private Key: (The decryption exponent): {}".format(lPrivateKeyExponent))

if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='RSA: An implementation of the RSA cipher system. Each plaintext character is transformed into cipher text by converting the plaintext into a numeric value, then raising that value to a power (determined by the public key) modulo modulus. Decryption is done by raising the numeric value of the cipher text to a power (determined by the private key) modulo a modulus.',
                                         epilog='Check if number 65536 is prime\n\npython rsa.py -v -ip 65536\n\nFind the next prime number after 65536\n\npython rsa.py -v -np 65536\n\nAssuming we want to use a blocksize of 4, the modulus must be at least 256^4 because we will encode the block as a unit and each character can take on 256 different values. Calculate 256^4 (256 to the power of 4). Answer will be 4294967296.\n\npython -c print(256**4)\n\nKnowing we need a modulus of at least 4294967296, suggest two prime numbers whos product (the modulus) will be greater than 4294967296\n\npython rsa.py -v -sp 4294967296\n\nUsing prime numbers p = 65537 and q = 65539 along with public key exponent 13, calculate the modulus, phi of p, q and modulus, greatest common divisor of the encryption exponenet and the phi of the modulus, the decryption exponenet, public key and private key.\n\npython rsa.py -v -k 13 -c 65537,65539\n\nEncrypt plaintext ABCD with public key 13 modulo 4295229443. Encryption was done with blocksize of 4.\n\npython rsa.py -v -b 4 -k 13 -e -m 4295229443 ABCD\n\nDecrypt plaintext ABCD with private key 1982353093 modulo 4295229443. Encryption was done with blocksize of 4.\n\npython rsa.py -v -b 4 -k 1982353093 -d -m 4295229443 DELM\n\nEncrypt plaintext ABCDE with public key 13 modulo 4295229443. Encryption was done with blocksize of 4. Padding required because length of plaintext not divisible by blocksize.\n\npython rsa.py -v -b 4 -k 13 -e -m 4295229443 ABCDE\n\nDecrypt plaintext ABCDE with private key 1982353093 modulo 4295229443. Encryption was done with blocksize of 4. Padding required because length of plaintext not divisible by blocksize.\n\npython rsa.py -v -b 4 -k 1982353093 -d -m 4295229443 -if base64 REVMTRZIMtQAAQIDBAUGBwgJ\n\nEncrypt plaintext file chuck-d.txt with public key 13 modulo 4295229443. Encryption was done with blocksize of 4. Padding required because length of plaintext not divisible by blocksize.\n\npython rsa.py -b 4 -k 13 -e -m 4295229443 -of binary -i test-files\chuck-d.txt> encrypted-chuck.bin\n\nDecrypt plaintext file encrypted-chuck.bin with private key 1982353093 modulo 4295229443. Encryption was done with blocksize of 4. Padding required because length of plaintext not divisible by blocksize.\n\npython rsa.py -b 4 -k 1982353093 -d -m 4295229443 -if binary -i encrypted-chuck.bin > decrypted-chuck.txt',
                                         formatter_class=RawTextHelpFormatter)
    lEncryptionActionGroup = lArgParser.add_mutually_exclusive_group(required=False)
    lEncryptionActionGroup.add_argument('-e', '--encrypt', help='Encrypt INPUT. This option requires a PUBLIC KEY and MODULUS.', action='store_true')
    lEncryptionActionGroup.add_argument('-d', '--decrypt', help='Decrypt INPUT. This option requires a PRIVATE KEY and MODULUS.', action='store_true')
    lArgParser.add_argument('-k', '--key', help='Encryption/Decryption key. Encryption requires the PUBLIC KEY. Decryption requires the PRIVATE KEY.', type=int, action='store')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-of', '--output-format', help='Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.', choices=['character', 'binary', 'base64'], action='store')
    lArgParser.add_argument('-b', '--blocksize', help='Blocksize. Default is 1. Minimum is 1. Modulus must be at least 256**BLOCKSIZE.', action='store', default=1, type=int)
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256. Minimum is 256. Modulus must be at least 256**BLOCKSIZE.', action='store', default=256, type=int)
    lArgParser.add_argument('-np', '--next-prime', help='Finds next prime number above LOWER LIMIT. Default is zero.', action='store', default=0, type=int)
    lArgParser.add_argument('-sp', '--suggest-primes', help='Finds next two prime numbers above squart root of DESIRED NUMBER. Default is zero.', action='store', default=0, type=int)
    lArgParser.add_argument('-ip', '--is-prime', help='Checks if INPUT is prime.', action='store', type=int)
    lArgParser.add_argument('-c', '--calculate-private-key', help='Given public key exponent KEY and two prime numbers P and Q, calculate private key and modulus. P and Q must be entered as a comma-delimited ordered pair. For example, to choose 65537 and 65539, enter the values as 65537,65539', action='store', type=str)
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lInputSourceGroup = lArgParser.add_mutually_exclusive_group(required=False)
    lInputSourceGroup.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lInputSourceGroup.add_argument('INPUT', nargs='?', help='Input value to encrypt/decrypt', type=str, action='store')
    lArgs = lArgParser.parse_args()

    lModulus = lArgs.modulus
    lBlocksize = lArgs.blocksize

    if lArgs.next_prime:
        print_next_prime(lArgs.next_prime, lArgs.verbose)
        exit(0)

    if lArgs.is_prime:
        print_is_prime(lArgs.is_prime, lArgs.verbose)
        exit(0)

    if lArgs.suggest_primes:
        print_suggested_primes(lArgs.suggest_primes, lArgs.verbose)
        exit(0)

    lMinimumModulus = SIZE_OF_ALPHABET**lBlocksize
    if lModulus < lMinimumModulus:
        lArgParser.error('The modulus {} is not big enough to support a block size of {}. The modulus must be at least {}**{} which is {}.'.format(lModulus, lBlocksize, SIZE_OF_ALPHABET, lBlocksize, lMinimumModulus))

    if (lArgs.encrypt or lArgs.decrypt or lArgs.calculate_private_key) and lArgs.key is None:
        lArgParser.error('If -e/--encrypt, -d/--decrypt or -c/--calculate-private-key is selected, -k/--key is required')

    if lArgs.key is not None:
        try:
            lKey = int(lArgs.key)
        except:
            lArgParser.error('Key must be an integer greater than 0')

    if lArgs.calculate_private_key:
        print_private_key(lKey, lArgs.calculate_private_key, lArgs.verbose)
        exit(0)

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
            if key_is_trivial(lKey, lModulus):
                 print('[*] Warning: Key {} is trivial'.format(lKey))

            if key_is_involutary(lKey, lModulus):
                 print('[*] Warning: Key {} is involutary'.format(lKey))
        # endif

        print_ciphertext(lInput, lKey, lBlocksize, lModulus, lArgs.verbose, lArgs.output_format)

    elif lArgs.decrypt:
        print_plaintext(lInput, lKey, lBlocksize, lModulus, lArgs.verbose)
    #endif