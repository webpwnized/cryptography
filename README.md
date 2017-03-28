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
    -a, --show-ascii      Show ascii representation for each byte of input
    -all, --show-all      Show statistics, count, ascii, percent represenation, histogram for each byte of input and Shannon entropy for input. Does NOT include index of coincidence. Equivalent to -cpmae -mean -median -mode -variance -stddev.

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
    
    -ioc, --show-ioc      Show kappa (kappa) index of coincidence

**Optional Columnar Analysis Options:**

    Choose the type(s) of output to display
    
    -t TOP_FREQUENCIES, --top-frequencies TOP_FREQUENCIES
                        Only display top X frequencies. Particuarly useful when combined with columnar analysis or when less important bytes clutter analysis.
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
  -t, --transpose       Calculate the transpose of the matrix modulo MODULUS
  -mi, --minors         Calculate the minors of the matrix modulo MODULUS
  -c, --cofactors       Calculate the cofactors of the matrix modulo MODULUS
  -a, --adjunct         Calculate the adjunct of the matrix modulo MODULUS
  -i, --inverse         Calculate the inverse of the matrix modulo MODULUS
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

`python maitred.py -all --modulus=26 --verbose 1,4,3,7`


 # Utility Belt
 
_A variety of functions helpful when studying basic crytography_

**Required arguments:**

    INPUT               Integer input value of which to calculate answer.
                        Required. This program will normalize values outside
                        of Z-modulus. For example, -1 mod 26 will be converted
                        to 25.

**Optional arguments:**

    -h, --help            show this help message and exit
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
    -mod, --modulo        Calculate modulo of INPUT modulo MODULUS
    -allmods, --all-modulo-calculations
                        Perform all available calculations of INPUT modulo
                        MODULUS
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
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
    -v, --verbose         Enables verbose output

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