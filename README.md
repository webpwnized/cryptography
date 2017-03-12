# Shifty

An Implementation of Shift Cipher

Usage: shifty.py [-h] (-e | -d) (-k KEY | -b) [-if {character,binary,base64}]
                 [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                 [INPUT]

Required arguments:
  
    INPUT                 Input value to encrypt/decrypt

Optional arguments:

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

# Affinity

    An implementation of Affine Cipher

Usage: affinity.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                   [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                   [INPUT]

Required arguments:

    INPUT                 Input value to encrypt/decrypt

Optional arguments:

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

# Visionary

    An implementation of Vigenère Cipher

Usage: visionary.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                    [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                    [INPUT]

Required arguments:
    
    INPUT                 Input value to encrypt/decrypt

Optional arguments:

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

# Substitute

    An implementation of Substitution Cipher
    
Usage: substitute.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                     [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                     [INPUT]

Required arguments:
  INPUT                 Input value to encrypt/decrypt

Optional arguments:

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

# Hilarity

    An implementation of the Hill cipher system

Required arguments:
    
    INPUT                 Input value to encrypt/decrypt

Optional arguments:

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

# Content Scrambling System

    An implementation of the css cipher system using two
    linear feedback shift registers

    Required arguments:
      INPUT                 Input value to encrypt/decrypt

    Optional arguments:
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

# Freak

    Byte frequency analyzer

Usage: freak.py [-h] [-c] [-p] [-m] [-a] [-ioc] [-all] [-t TOP_FREQUENCIES]
                [-g] [-col COLUMNAR_ANALYSIS] [-v]
                [-if {character,binary,base64}] [-i INPUT_FILE]
                [INPUT]

Required arguments:
    
    INPUT                 INPUT to analyze

Optional arguments:

    -h, --help            show this help message and exit
    -t TOP_FREQUENCIES, --top-frequencies TOP_FREQUENCIES
                        Only display top X frequencies. Particuarly useful
                        when combined with columnar analysis or when less
                        important bytes clutter analysis.
    -g, --show-guesses    Show ascii representation for top byte of input. Tries
                        ASCII lower, upper and numeric translations. Only
                        works with -t/--top-frequencies.
    -col COLUMNAR_ANALYSIS, --columnar-analysis COLUMNAR_ANALYSIS
                        Break INPUT into X columns and perform analysis on
                        columns. Particuarly useful against polyalphabetic
                        stream ciphers.
    -v, --verbose         Enables verbose output
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT to analyze from an input file
    
    Output Options:
    Choose the type(s) of output to display
    
    -c, --show-count      Show count for each byte of input
    -p, --show-percent    Show percent representation for each byte of input
    -m, --show-histogram  Show histogram for each byte of input
    -a, --show-ascii      Show ascii representation for each byte of input
    -mean, --show-mean    Show Arithmetic Mean (Average)
    -median, --show-median              Show Median
    -mode, --show-mode                  Show Mode
    -variance, --show-variance          Show Variance
    -stddev, --show-standard-deviation  Show Standard Deviation
    -e, --show-entropy    Show Shannon entropy
    -ioc, --show-ioc      Show kappa (delta) index of coincidence
    -all, --show-all      Show count, ascii, percent represenation, histogram
                        for each byte of input and Shannon entropy for input.
                        Does NOT include index of coincidence. Equivalent to
                        -cpmae.

# Maitre D

A matrix variant calculator within modulo MODULUS

Usage: maitred.py [-h] [-d] [-id] [-mi] [-c] [-a] [-i] [-all] [-v]
                  [-m MODULUS]
                  [INPUT]

Required arguments:

    INPUT                 Input matrix of integers. The matrix must be square.
                        For example a 2 X 2 matrix could be 1, 2, 3, 4

Optional arguments:

    -h, --help          Show this help message and exit
    -d, --determinant   Calculate the determinant of the matrix modulo
                        MODULUS. Answer will be in Z-MODULUS.
    -id, --inverse-determinant
                        Calculate the inverse of the determinant of the matrix
                        modulo MODULUS. Answer will be in Z-MODULUS.
    -t, --transpose     Calculate the transpose of the matrix modulo MODULUS 
    -mi, --minors       Calculate the minors of the matrix modulo MODULUS
    -c, --cofactors     Calculate the cofactors of the matrix modulo MODULUS
    -a, --adjunct       Calculate the adjunct of the matrix modulo MODULUS
    -i, --inverse       Calculate the inverse of the matrix modulo MODULUS
    -all, --all         Calculate the determinant, inverse determinant,
                        transpose, adjunct and inverse of the matrix modulo
                        MODULUS. Same as -id -dai
    -phi, --count-invertible-matrices
                        Calculate the number of invertible matrices of size
                        INPUT modulo MODULUS.
    -v, --verbose       Enables verbose output
    -m MODULUS, --modulus MODULUS   Modulus. Default is 256.

 # Utility Belt
 
    A variety of functions helpful when studying basic crytography

Required arguments:

    INPUT               Integer input value of which to calculate answer.
                        Required. This program will normalize values outside
                        of Z-modulus. For example, -1 mod 26 will be converted
                        to 25.

Optional arguments:

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

usage: transference.py [-h] [-tft] [-lat] [-all] [-v] INPUT

    A tool to help visualize s-boxes (substitution boxes or transfer functions)

Required arguments:

    INPUT                 The substitution table (s-box) represented as a comma
                        delimted list of integers. The length of the list is
                        the number of bits in the substitution. Required.
                        Example: 3,2,0,1 means substitute 3 for 0, 2 for 1, 0
                        for 2 and 1 for 3.

Optional arguments:

    -h, --help            show this help message and exit
    -tft, --transfer-function-table
                        Print the transfer function table for the s-box
    -lat, --linear-approximation-table
                        Calculate the linear transformation table for the
                        s-box
    -all, --all           Calculate the linear transformation table for the
                        s-box
    -v, --verbose         Enables verbose output