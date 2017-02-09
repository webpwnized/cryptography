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

    -v, --verbose         Enables verbose output

    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

# Affinity

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
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

# Freek

Byte frequency analyzer

Usage: freek.py [-h] [-g] [-s] [-c] [-a] [-v] [-if {character,binary,base64}]
                [-i INPUT_FILE]
                [INPUT]

Required arguments:

    INPUT                 INPUT to analyze

Optional arguments:

    -h, --help            show this help message and exit

    -g, --show-histogram  Show histogram for each byte of input

    -s, --show-ascii      Show ascii representation for each byte of input

    -c, --show-byte-count
                        Show count for each byte of input

    -a, --show-all        Show count, ascii represenation and histogram for each
                        byte of input. Equivalent to -gsc

    -v, --verbose         Enables verbose output

    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64

    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file
