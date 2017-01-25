from collections import Counter
import argparse

gEnglishLetterFrequencies = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99,
                     'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
                     'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

LETTERS_SORTED_BY_POPULARITY = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS_SORTED_ALPHABETICALLY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_DICTIONARY = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
                'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0,
                'Y': 0, 'Z': 0}

def do_analysis(pText):

    lTotalCount = 0

    for character in pText.upper():
        if character in LETTERS_SORTED_ALPHABETICALLY:
            LETTERS_DICTIONARY[character]+=1
            lTotalCount+=1

    for letter, frequency in LETTERS_DICTIONARY.items():
        print(letter,frequency,"{0:.2f}".format(frequency/lTotalCount*100),"#"*int(frequency/lTotalCount*500))

def do_analysis(pFile):

    lTotalCount = 0

    for line in pFile:
        for character in line.upper():
            if character in LETTERS_SORTED_ALPHABETICALLY:
                LETTERS_DICTIONARY[character]+=1
                lTotalCount+=1

    for letter, frequency in LETTERS_DICTIONARY.items():
        print(letter,frequency,"{0:.2f}".format(frequency/lTotalCount*100),"#"*int(frequency/lTotalCount*500))


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lArgParser.add_argument('-i', '--input-file', help='Read TEXT from an input file', action='store')
    lArgParser.add_argument('TEXT', nargs="?", help='Text to analyze', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if lArgs.input_file:
        lFile = open(lArgs.input_file, 'r')
        do_analysis(lFile)
        lFile.close()
    else:
        do_analysis(lArgs.TEXT)