# Shifty

_An implementation of the shift cipher system. Each plaintext character is shifted the same number of bytes as determined by the key. The shift occurs with respect to the modulus._

**Usage**: python shifty.py [-h] (-e | -d) (-k KEY | -b) [-if {character,binary,base64}]
                 [-of {character,binary,base64}] [-m MODULUS] [-v]
                 [-i INPUT_FILE]
                 [INPUT]

**Required arguments:**
  
    INPUT                 Input value to encrypt/decrypt

**Optional arguments:**

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY or
                        BRUTEFORCE flag.
    -k KEY, --key KEY     Encryption/Decription key
    -b, --bruteforce      Rather than decrypt with KEY, try to brute force the
                        plaintext.
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

**Encrypt the word hello with ceasar cipher:**

`python shifty.py --encrypt --key 3 --verbose hello`

**Decrypt the world hello with key 3:**

`python shifty.py --decrypt --key 3 khoor`

**Bruteforce the world hello with key 3:**

`python shifty.py --decrypt --bruteforce khoor`

**Example using input from file, redirecting output to file and working with binary input. Combine these features to suit.
Encrypt the contents of file binary-input.txt:**

`python shifty.py --encrypt --key 3 --input-format=binary --output-format=binary --input-file binary-input.txt > binary-output.bin`

# Affinity

_An implementation of the affine cipher system. A key is provided as a vector of two integers. The key integers a,b determine the shift of each byte of the plaintext by the formula ax + b modulo MODULUS. The shifts occurs with respect to the modulus._

**Usage**: python affinity.py [-h] (-e | -d) [-k KEY] [-if {character,binary,base64}]
                   [-of {character,binary,base64}] [-m MODULUS] [-v]
                   [-i INPUT_FILE]
                   [INPUT]

**Required arguments:**

    INPUT                 Input value to encrypt/decrypt

**Optional arguments:**

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY or
                        BRUTEFORCE flag.
    -k KEY, --key KEY     Encryption/Decryption key in a,b format
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

**Encrypt the word hello with key 3,1:**

`python affinity.py --encrypt --key 3,1 --verbose "hello"`

**Decrypt the world hello with key 3,1:**

`python affinity.py --decrypt --key 3,1 --verbose "90EEN"`

**Example using input from file, redirecting output to file and working with binary input. Combine these features to suit.
Encrypt the contents of file funny-cat-1.jpg:**

`python affinity.py --encrypt --key 3,1 --input-format=binary --output-format=binary --input-file funny-cat-1.jpg > encrypted-funny-cat-1.bin`

# Visionary

_An implementation of the vigenere cipher system. A key is provided. Each byte of the key shifts the respective byte of plaintext. If the plaintext is longer than the key, the key bytes start over. The key derivation normalizes the key weakening the cipher. For example, A = a = 1 = shift plaintext 1 byte. The shifts occurs with respect to the modulus._

**Usage**: python visionary.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                    [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                    [INPUT]

**Required arguments:**
    
    INPUT                 Input value to encrypt/decrypt

**Optional arguments:**

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY or
                        BRUTEFORCE flag.
    -k KEY, --key KEY     Encryption/Decryption key
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

**Encrypt the phrase helloworld with key 12345:**

`python visionary.py --encrypt --key 12345 --verbose "helloworld"`

**Decrypt the phrase helloworld with key 12345:**

`python visionary.py --decrypt --key 12345 "igoptxqupi"`

**Example using input from file, redirecting output to file and working with binary input. Combine these features to suit. Encrypt the contents of file funny-cat-1.jpg:**

`python visionary.py --encrypt --key rocky329 --input-format=binary --output-format=binary --input-file=funny-cat-1.jpg > encrypted-funny-cat-1.bin`


# Substitute

_An implementation of Substitution Cipher_
    
**Usage**: python substitute.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                     [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                     [INPUT]

**Required arguments:**

    INPUT                 Input value to encrypt/decrypt

**Optional arguments:**

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY.
    -k KEY, --key KEY     Encryption/Decryption key
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64. If
                        input format provided, but output format is not
                        provided, output format defaults to match input
                        format.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

**Encrypt the phrase helloworld with key 3,2,0,1,4:**

python substitute.py --encrypt --key 3,2,0,1,4 --verbose helloworld

**Decrypt the phrase helloworld with key 3,2,0,1,4:**

python substitute.py --decrypt --key 3,2,0,1,4 --verbose llheolrwod

**Example using input from file, redirecting output to file and working with binary input. Combine these features to suit. Encrypt the contents of file binary-input.txt:**

python substitute.py --encrypt --key 3,2,0,1,4 --input-format=binary --output-format=binary --input-file=binary-input.txt > encrypted-binary-input.bin

# Hilarity

_An implementation of the Hill cipher system_

**Usage**: python hilarity.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                   [-of {character,binary,base64}] [-m MODULUS] [-v]
                   [-i INPUT_FILE]
                   [INPUT]
                   
**Required arguments:**
    
    INPUT                 Input value to encrypt/decrypt

**Optional arguments:**

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY or
                        BRUTEFORCE flag.
    -k KEY, --key KEY     Encryption/Decryption key of integers in matrix
                        format. The matrix must be square. For example a 2 X 2
                        matrix could be 1, 2, 3, 4
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64. If
                        input format provided, but output format is not
                        provided, output format defaults to match input
                        format.
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

**Encrypt the phrase helloworld with key 7,11,3,8:**

python hilarity.py --encrypt --key 7,11,3,8 helloworld

**Decrypt the phrase helloworld with key 7,11,3,8:**

python hilarity.py --decrypt --key 7,11,3,8 --input-format=base64 B6A4BG59X1UgxA==

**Example using input from file, redirecting output to file and working with binary input. Combine these features to suit. Encrypt the contents of file binary-input.txt:**

python hilarity.py --encrypt --key 7,11,3,8 --input-format=binary --output-format=binary --input-file=binary-input.txt > encrypted-binary-input.bin


# Content Scrambling System

_An implementation of the css cipher system using two linear feedback shift registers_

**Usage**: content-scrambing-system.py [-h] (-e | -d) [-k KEY]
                                   [-if {character,binary,base64}]
                                   [-of {character,binary,base64}] [-v]
                                   [-i INPUT_FILE]
                                   [INPUT]
          
**Required arguments:**

      INPUT                 Input value to encrypt/decrypt

**Optional arguments:**

      -h, --help            show this help message and exit
      -e, --encrypt         Encrypt INPUT. This option requires a KEY.
      -d, --decrypt         Decrypt INPUT. This option requires a KEY.
      -k KEY, --key KEY     Encryption/Decryption key. Must be 5 bytes. Enter the
                            bytes as a list of comma-delimited integers between
                            0-255. Example: 25,230,3,64,12
      -if {character,binary,base64}, --input-format {character,binary,base64}
                            Input format can be character, binary, or base64
      -of {character,binary,base64}, --output-format {character,binary,base64}
                            Output format can be character, binary, or base64. If
                            input format provided, but output format is not
                            provided, output format defaults to match input
                            format.
      -v, --verbose         Enables verbose output
      -i INPUT_FILE, --input-file INPUT_FILE
                            Read INPUT from an input file

**Encrypt the phrase helloworld with key 25,230,3,64,12:**

python content-scrambing-system.py --encrypt --key 25,230,3,64,12 --verbose helloworld

**Decrypt the phrase helloworld with key 25,230,3,64,12:**

python content-scrambing-system.py --decrypt --key 25,230,3,64,12 --input-format=base64 --output-format=character wr8B+CWpEqgqAw==

**Example using input from file, redirecting output to file and working with binary input. Combine these features to suit. Encrypt the contents of file binary-input.txt:**

python content-scrambing-system.py --encrypt --key 25,230,3,64,12 --input-format=binary --output-format=binary --input-file=test-files\binary-input.txt > encrypted-binary-input.bin

**Example using input from file, redirecting output to file and working with binary input. Combine these features to suit. Decrypt the contents of file encrypted-binary-input.bin:**

python content-scrambing-system.py --decrypt --key 25,230,3,64,12 --input-format=binary --output-format=character --input-file=encrypted-binary-input.bin

# RSA Training Tool

**Usage**: rsa.py [-h] [-e | -d] [-k KEY] [-if {character,binary,base64}]
              [-of {character,binary,base64}] [-b BLOCKSIZE] [-m MODULUS]
              [-np NEXT_PRIME] [-sp SUGGEST_PRIMES] [-ip IS_PRIME]
              [-c CALCULATE_PRIVATE_KEY] [-v] [-i INPUT_FILE]
              [INPUT]

_RSA Training Tool: An implementation of the RSA cipher system. Each plaintext character is transformed into cipher text by converting the plaintext into a numeric value, then raising that value to a power (determined by the public key) modulo modulus. Decryption is done by raising the numeric value of the cipher text to a power (determined by the private key) modulo a modulus._

**Required arguments:**
    
    INPUT                 Input value to encrypt/decrypt

**Optional arguments:**

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a PUBLIC KEY and MODULUS.
    -d, --decrypt         Decrypt INPUT. This option requires a PRIVATE KEY and MODULUS.
    -k KEY, --key KEY     Encryption/Decryption key. Encryption requires the PUBLIC KEY. Decryption requires the PRIVATE KEY.
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64. If input format provided, but output format is not provided, output format defaults to match input format.
    -b BLOCKSIZE, --blocksize BLOCKSIZE
                        Blocksize. Default is 1. Minimum is 1. Modulus must be at least 256**BLOCKSIZE.
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256. Minimum is 256. Modulus must be at least 256**BLOCKSIZE.
    -np NEXT_PRIME, --next-prime NEXT_PRIME
                        Finds next prime number above LOWER LIMIT. Default is zero.
    -sp SUGGEST_PRIMES, --suggest-primes SUGGEST_PRIMES
                        Finds next two prime numbers above squart root of DESIRED NUMBER. Default is zero.
    -ip IS_PRIME, --is-prime IS_PRIME
                        Checks if INPUT is prime.
    -c CALCULATE_PRIVATE_KEY, --calculate-private-key CALCULATE_PRIVATE_KEY
                        Given public key exponent KEY and two prime numbers P and Q, calculate private key and modulus. P and Q must be entered as a comma-delimited ordered pair. For example, to choose 65537 and 65539, enter the values as 65537,65539
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

**Check if number 65536 is prime**

`python rsa.py -v -ip 65536`

**Find the next prime number after 65536**

`python rsa.py -v -np 65536`

**Assuming we want to use a blocksize of 4, the modulus must be at least 256^4 because we will encode the block as a unit and each character can take on 256 different values. Calculate 256^4 (256 to the power of 4). Answer will be 4294967296.**

`python -c print(256**4)`

**Knowing we need a modulus of at least 4294967296, suggest two prime numbers whos product (the modulus) will be greater than 4294967296**

`python rsa.py -v -sp 4294967296`

**Using prime numbers p = 65537 and q = 65539 along with public key exponent 13, calculate the modulus, phi of p, q and modulus, greatest common divisor of the encryption exponenet and the phi of the modulus, the decryption exponenet, public key and private key.**

`python rsa.py -v -k 13 -c 65537,65539`

**Encrypt plaintext ABCD with public key 13 modulo 4295229443. Encryption was done with blocksize of 4.**

`python rsa.py -v -b 4 -k 13 -e -m 4295229443 ABCD`

**Decrypt plaintext ABCD with private key 1982353093 modulo 4295229443. Encryption was done with blocksize of 4.**

`python rsa.py -v -b 4 -k 1982353093 -d -m 4295229443 DELM`

**Encrypt plaintext ABCDE with public key 13 modulo 4295229443. Encryption was done with blocksize of 4. Padding required because length of plaintext not divisible by blocksize.**

`python rsa.py -v -b 4 -k 13 -e -m 4295229443 ABCDE`

**Decrypt plaintext ABCDE with private key 1982353093 modulo 4295229443. Encryption was done with blocksize of 4. Padding required because length of plaintext not divisible by blocksize.**

`python rsa.py -v -b 4 -k 1982353093 -d -m 4295229443 -if base64 REVMTRZIMtQAAQIDBAUGBwgJ`

**Encrypt plaintext file chuck-d.txt with public key 13 modulo 4295229443. Encryption was done with blocksize of 4. Padding required because length of plaintext not divisible by blocksize.**

`python rsa.py -b 4 -k 13 -e -m 4295229443 -of binary -i test-files\chuck-d.txt> encrypted-chuck.bin`

**Decrypt plaintext file encrypted-chuck.bin with private key 1982353093 modulo 4295229443. Encryption was done with blocksize of 4. Padding required because length of plaintext not divisible by blocksize.**

`python rsa.py -b 4 -k 1982353093 -d -m 4295229443 -if binary -i encrypted-chuck.bin > decrypted-chuck.txt`

# Freak

_An implementation of a frequency and cryptography analyzer_

**Usage**: freak.py [-h] [-c] [-p] [-m] [-a] [-all] [-mean] [-median] [-mode]
                [-antimode] [-variance] [-stddev] [-e] [-stats] [-ioc]
                [-t TOP_FREQUENCIES] [-g] [-col COLUMNAR_ANALYSIS] [-v]
                [-if {character,binary,base64}] [-i INPUT_FILE]
                [INPUT]
                
**Required arguments:**

    INPUT                 INPUT to analyze

**Optional arguments:**

    -h, --help            show this help message and exit
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT to analyze from an input file

**Optional Histogram Options:**

    Choose the type(s) of histogram output to display
    
    -c, --show-count      Show count for each byte of input
    -p, --show-percent    Show percent representation for each byte of input
    -m, --show-histogram  Show histogram for each byte of input
    -a, --show-ascii      Show ASCII representation for each byte of input
    -all, --show-all      Show statistics, count, ASCII, percent represenation, histogram for each byte of input and Shannon entropy for input. Does NOT include index of coincidence. Equivalent to -cpmae -mean -median -mode -variance -stddev.

**Optional Statistics Options:**

    Choose the type(s) of statistical output to display
    
    -mean, --show-mean    Show Arithmetic Mean (Average)
    -median, --show-median
                        Show Median
    -mode, --show-mode    Show Mode (Most popular byte)
    -antimode, --show-anti-mode
                        Show Anti-Mode (Least popular byte)
    -variance, --show-variance
                        Show Variance
    -stddev, --show-standard-deviation
                        Show Standard Deviation
    -e, --show-entropy    Show Shannon entropy
    -stats, --show-statistics
                        Show mean, median, mode, variance and standard deviation for each byte of input and Shannon entropy for input. Equivalent to -e -mean -median -mode -variance -stddev.

**Optional Index of Coincidence Options:**

    Choose the type(s) of IOC output to display
    
    -ioc, --show-ioc      Show kappa index of coincidence

**Optional Columnar Analysis Options:**

    Choose the type(s) of output to display
    
    -t TOP_FREQUENCIES, --top-frequencies TOP_FREQUENCIES
                        Only display top X frequencies. Particuarly useful when combined with columnar analysis, histogram or when less important bytes clutter analysis.
    -g, --show-guesses    Show ascii representation for top byte of input. Tries ASCII lower, upper and numeric translations. Only works with -t/--top-frequencies.
    -col COLUMNAR_ANALYSIS, --columnar-analysis COLUMNAR_ANALYSIS
                        Break INPUT into X columns and perform analysis on columns. Particuarly useful against polyalphabetic stream ciphers.

**Optional Other Options:**

    Choose other options
    
    -v, --verbose         Enables verbose output
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64

**For each byte in file encrypted-funny-cat-1.jpg, show count, percent and histogram.**

`python freak.py -cpm --verbose -i encrypted-funny-cat-1.jpg`

**For each byte in file encrypted-funny-cat-1.jpg, show count, percent, histogram and all statistics**
 
`python freak.py --show-all --verbose -i encrypted-funny-cat-1.jpg`

**For each byte in file encrypted-funny-cat-1.jpg, show all statistics: mean, median, mode, anti-mode, variance, standard deviation, and Shannon entropy** 

`python freak.py --show-statistics --verbose -i encrypted-funny-cat-1.jpg`

**Determine the index of coincidence of file encrypted-funny-cat-1.jpg in order to determine the length of a Vigenere password. This only works if the input file is encrypted with the Vigenere file.**

`python freak.py -ioc --verbose --input-file=encrypted-funny-cat-1.bin`

**For each byte in file encrypted-funny-cat-1.jpg, group input into columns. For example, -col 5 groups together byte 1, 6, 11, etc. Analysis is performed independently on each column.** 

`python freak.py -cpm -col 8 --input-file=encrypted-funny-cat-1.bin`

**For each byte in file encrypted-funny-cat-1.jpg, group input into columns. For example, -col 5 groups together byte 1, 6, 11, etc. Analysis is performed independently on each column. -t sorts the results then only shows top t results. In this example, the top 5 results.** 

`python freak.py -cpm -col 8 -t 5 --input-file=encrypted-funny-cat-1.bin`

**To guess a Vigenere password of length "col", add -g option. This only works if output is grouped into columns first. This example assumes the password is 8 characters long.** 

`python freak.py -cpm -g -t 1 -col 8 --input-file=encrypted-funny-cat-1.bin`

# Maitre D

_A matrix variant calculator within modulo MODULUS_

**Usage**: python maitred.py [-h] [-d] [-id] [-t] [-mi] [-c] [-a] [-i] [-all] [-phi] [-v]
                  [-m MODULUS]
                  [INPUT]

**Required arguments:**

    INPUT                 Input matrix of integers. The matrix must be square.
                        For example a 2 X 2 matrix could be 1, 2, 3, 4

**Optional arguments:**
    
    -h, --help            show this help message and exit
    -d, --determinant     Calculate the determinant of the matrix modulo
                        MODULUS. Answer will be in Z-MODULUS.
    -id, --inverse-determinant
                        Calculate the inverse of the determinant of the matrix
                        modulo MODULUS. Answer will be in Z-MODULUS. 
                        The determinant must not be zero.
    -t, --transpose       Calculate the transpose of the matrix modulo MODULUS
    -mi, --minors         Calculate the minors of the matrix modulo MODULUS
    -c, --cofactors       Calculate the cofactors of the matrix modulo MODULUS
    -a, --adjunct         Calculate the adjunct of the matrix modulo MODULUS
    -i, --inverse       Calculate the inverse of the matrix modulo MODULUS.
                        The determinant must not be zero since the inverse of the 
                        determinant must be found modulo MODULUS.
    -all, --all           Calculate the determinant, inverse determinant,
                        transpose, adjunct and inverse of the matrix modulo
                        MODULUS. Same as -id -dai
    -phi, --count-invertible-matrices
                        Calculate the number of invertible matrices of size
                        INPUT modulo MODULUS.
    -v, --verbose         Enables verbose output
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.

**Calculate Matrix, Determinant of Matrix, Inverse of the determinant of Matrix, Transpose Matrix, Minors Matrix, Cofactors Matrix, Adjunct Matrix and Inverse Matrix (mod 26)**

**Matrix: 1 4 3 7**

`python maitred.py -all --modulus=26 --verbose 1,4,3,7`

**Matrix: 2 5 9 5**

`python maitred.py -all --modulus=26 --verbose 2,5,9,5`

**Calculate number of invertible matrices of size 2x2 with respect to modulo 6**

`python maitred.py -phi -m 6 2`

 # Utility Belt
 
_A variety of functions helpful when studying basic crytography_

**Required arguments:**

    INPUT               Integer input value of which to calculate answer.
                        Required. This program will normalize values outside
                        of Z-modulus. For example, -1 mod 26 will be converted
                        to 25.

**Optional arguments:**
 
    -h, --help            show this help message and exit

**Options for calculating in finite fields:**

    -rp, --relative-primes
                        Calculate the relative primes with respect to MODULUS.
                        INPUT is not relevant with respect to this function.
    -pf, --prime-factors  Calculate the prime factors with respect to MODULUS.
                        INPUT is not relevant with respect to this function.
    -cmi, --count-multiplicative-inverses
                        Count of multiplicative inverses with respect to
                        MODULUS using Euler Phi function. INPUT is not
                        relevant with respect to this function.
    -gcd, --greatest-common-divisor
                        Calculate the greatest common divisor of INPUT and
                        MODULUS
    -mi, --mutiplicative-inverse
                        Calculate multiplicative inverse of INPUT modulo
                        MODULUS
    -fe FAST_EXPONENTIATION, --fast-exponentiation FAST_EXPONENTIATION
                            Calculate INPUT raised to this POWER modulo MODULUS.
                            Set -fe/--fast-exponentiation to POWER.
    -mod, --modulo        Calculate modulo of INPUT modulo MODULUS
    -allmods, --all-modulo-calculations
                        Perform all available calculations of INPUT modulo
                        MODULUS
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.

**Options for working in Galois Fields:**

    -fg, --find-generators
                        Calculate the generators for field of integers defined
                        by Z-MODULUS

**Options for working with Congruences:**

    -crt, --chinese-remainder-theorem
                        Calculate the intersection of the set of congruences.
                        INPUT is a set of congruences specified by CONSTANT 1,
                        MODULUS 1; CONSTANT 2, MODULUS 2; ...; CONSTANT N,
                        MODULUS N. For example, the set x = 12 mod 25, x = 9
                        mod 26, x = 23 mod 27 would be specified as 12, 25; 9,
                        26; 23, 27

**Options for calculating Shannon Entropy:**

    -se2, --shannon-entropy-base-2
                        Calculate the base-2 Shannon Entropy for list of
                        probabilities. INPUT must be a comma-delimited list of
                        floating point numbers between 0 and 1. Each of these
                        numbers is the probability of the event occuring. For
                        example 0.5,0.33,0.165 represents 1/2,1/3,1/6. To get
                        meaningful results, the INPUT list must add up to 1.00
                        within reason.
                        
**Options for working with Permutations:**

    -pc, --permutation-cycles
                        Calculate the permutation cycles of permutation INPUT.
                        INPUT must be a complete set of integers in any order
                        starting from 0.
    -po, --permutation-order
                        Calculate the order of the permutation INPUT. INPUT
                        must be a complete set of integers in any order
                        starting from 0.
    -ip, --invert-permutation
                        Calculate the inverse of the permutation INPUT. INPUT
                        must be a complete set of integers in any order
                        starting from 0.
    -allperms, --all-permutation-calculations
                        Perform all available calculations of permutation
                        INPUT
    -gp, --generate-permutations
                        Generate permutations of size INPUT. INPUT must be an
                        integer.

**Other Options:**

    -v, --verbose         Enables verbose output

**Calculate relative primes, prime factors and count multiplicative inverses with respect to modulus 26**

`python utility-belt.py -rp -pf -cmi -m 26 -v`

**Calculate the greatest common divisor and multiplicative inverse of 7 modulo 26. Note that 7 is relatively prime to 26.**

`python utility-belt.py -gcd -mi -m 26 -v 7`

**Calculate intersection for the set x = 12 mod 25, x = 9 mod 26, x = 23 mod 27**

`python utility-belt.py -crt "12,25;9,26;23,27" -v`

**Calculate 9726 ^ 3533 % 11413 = 5761 using fast exponentiation**

`python utility-belt.py -v -fe 3533 -m 11413 9726`

**Calculate all primitive root generators modulo 7**

`python utility-belt.py -fg -m 7 -v`

**Calculate the Shannon Entropy of probabilities 1/2, 1/3 and 1/6**

`python utility-belt.py -se2 -v .5,.33,.165`

**Calculate the permutation cycles, permutation order and invert permutation 3,4,2,0,1**

`python utility-belt.py -allperms -v 3,4,2,0,1`

**Generate permutations of size 5**

`python utility-belt.py -gp 5`

# Transference

**Usage**: transference.py [-h] [-tft] [-lat] [-all] [-v] INPUT

    A tool to help visualize s-boxes (substitution boxes or transfer functions)

**Required arguments:**

    INPUT               The substitution table (s-box) represented as a comma
                        delimted list of integers. The length of the list is
                        the number of bits in the substitution. Required.
                        Example: 3,2,0,1 means substitute 3 for 0, 2 for 1, 0
                        for 2 and 1 for 3.

**Optional arguments:**

    -h, --help            show this help message and exit
    -tft, --transfer-function-table
                        Print the transfer function table for the s-box
    -lat, --linear-approximation-table
                        Calculate the linear transformation table for the
                        s-box
    -all, --all           Calculate the linear transformation table for the
                        s-box
    -v, --verbose         Enables verbose output
    
**Print the transfer function table and calculate the linear approximation table for s-box 3,7,1,0,5,6,4,2**
    
`python transference.py -all 3,7,1,0,5,6,4,2`