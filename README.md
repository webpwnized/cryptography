# Shifty

An Implementation of Shift Cipher

Usage: shifty.py [-h] [-e] [-d] [-b] [-k KEY] TEXT

Required arguments:
  
    TEXT               Text value to encrypt/decrypt

Optional arguments:
  
      -h, --help         show this help message and exit
      
      -e, --encrypt      Encrypt TEXT. This option requires a KEY.
      
      -d, --decrypt      Decrypt TEXT. This option requires a KEY or BRUTEFORCE
                         flag.
      
      -b, --bruteforce   Rather than decrypt with KEY, try to brute force the
                         plaintext.
      
      -k KEY, --key KEY  Encryption/Decription key

