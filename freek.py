import argparse, base64
from collections import OrderedDict


TWO_DECIMAL_PLACES = "{0:.2f}"
MODULUS = 256


def get_delta_index_of_coincidence(pInput: bytearray) -> dict:
    # IOC:
    # For each shift, add up the times the two bytes offset by lBytesShifted happen to match (coincidental)
    # We shift at least one character up to a max of MAX_SHIFTS_TO_ANALYZE characters
    # When the shift is equal to the length of the key, the bytes compared will have been encyrypted by
    # the same key and will be statistically more likely to be the same character. (About twice as likely)
    # These "bumps" will be evident in the histogram with a period equal to the length of the key

    MAX_SHIFTS_TO_ANALYZE = 60

    lBytesOfInput = len(pInput)
    lShiftsToAnalyze = min(lBytesOfInput, MAX_SHIFTS_TO_ANALYZE)
    lIOC = dict.fromkeys(range(1, lShiftsToAnalyze), 0)
    for lBytesShifted in range(1, lShiftsToAnalyze):
        lMatches = 0
        lBytesToTest = lBytesOfInput - lBytesShifted
        for lByte in range(0, lBytesToTest):
            if pInput[lByte] == pInput[lByte + lBytesShifted]:
                lMatches += 1
            # end if
        # end for lByte
        lIOC[lBytesShifted] = lMatches / lBytesToTest
    # end for lBytesShifted

    return lIOC


def print_delta_index_of_coincidence(pInput: bytearray) -> None:
    lIOC = get_delta_index_of_coincidence(pInput)

    lScaleFactor = 40

    for lByteOffset, lCoincidence in lIOC.items():
        lPercentCoincidence = lCoincidence * 100
        lCoincidenceBarLength = int(lPercentCoincidence * lScaleFactor)

        lOutput = 'Byte Offset: '
        lOutput += str(lByteOffset) + ' '
        lOutput += "(" + TWO_DECIMAL_PLACES.format(lPercentCoincidence) + "%) "
        lOutput += "#" * lCoincidenceBarLength
        print(lOutput)
    # end for


def print_byte_analysis(pByte: int, pByteCount: int, pTotalBytes: int, pShowCount: bool, pShowHistogram: bool, pShowASCII: bool, pShowPercent: bool, pShowGuesses: bool, pVerbose: bool) -> None:
    SCALE_FACTOR = 20
    lPercent = pByteCount / pTotalBytes * 100
    lFrequencyBarLength = int(lPercent * SCALE_FACTOR)

    lOutput = ''
    if pVerbose:
        lOutput = 'Byte: '
    lOutput += str(pByte) + '\t'
    if pShowASCII:
        lOutput += chr(pByte) + '\t'
    if pShowCount:
        lOutput += str(pByteCount) + '\t'
    if pShowPercent:
        lOutput += "(" + TWO_DECIMAL_PLACES.format(lPercent) + "%)\t"
    if pShowHistogram:
        lOutput += "#" * lFrequencyBarLength
    print(lOutput)
    # end if


def print_analysis(pInput: bytearray, pShowCount: bool, pShowHistogram: bool, pShowASCII: bool, pShowPercent: bool, pShowGuesses: bool, pVerbose: bool, pTopFrequencies: int, pColumnarAnalysis: int) -> None:

    lByteCounts = dict.fromkeys(range(0,256), 0)
    lTotalBytes = 0

    for lByte in pInput:
        lByteCounts[lByte] += 1
        lTotalBytes += 1
    # end for

    if pTopFrequencies:
        lBytesPrinted = 0
        lAnalyzingMostPopularByte = True
        for lByte, lByteCount in sorted(lByteCounts.items(), key=lambda x:x[1], reverse=True):
            if pVerbose or lByteCount:
                if pShowGuesses and lAnalyzingMostPopularByte:
                    print('\nBest guess\tLowercase: ' + chr((lByte + 97) % MODULUS) + '\tUppercase: ' + chr((lByte + 65) % MODULUS) + '\tNumeric: ' + chr((lByte + 48) % MODULUS))
                    lAnalyzingMostPopularByte = False
                print_byte_analysis(lByte, lByteCount, lTotalBytes, pShowCount, pShowHistogram, pShowASCII, pShowPercent, pShowGuesses, pVerbose)
            # end if
            lBytesPrinted += 1
            if lBytesPrinted > (pTopFrequencies - 1):
                break
    else:
        for lByte, lByteCount in lByteCounts.items():
            if pVerbose or lByteCount:
                print_byte_analysis(lByte, lByteCount, lTotalBytes, pShowCount, pShowHistogram, pShowASCII, pShowPercent, pShowGuesses, pVerbose)
            # end if
    # end for


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lOutputOptions = lArgParser.add_argument_group(title="Output Options", description="Choose the type(s) of output to display")
    lOutputOptions.add_argument('-c', '--show-count', help='Show count for each byte of input', action='store_true')
    lOutputOptions.add_argument('-p', '--show-percent', help='Show percent representation for each byte of input', action='store_true')
    lOutputOptions.add_argument('-m', '--show-histogram', help='Show histogram for each byte of input', action='store_true')
    lOutputOptions.add_argument('-a', '--show-ascii', help='Show ascii representation for each byte of input', action='store_true')
    lOutputOptions.add_argument('-ioc', '--show-ioc', help='Show kappa (delta) index of coincidence', action='store_true')
    lOutputOptions.add_argument('-all', '--show-all', help='Show count, ascii, percent represenation, histogram for each byte of input. Does NOT include index of coincidence. Equivalent to -cpmag.', action='store_true')
    lArgParser.add_argument('-t', '--top-frequencies', help='Only display top X frequencies. Particuarly useful when combined with columnar analysis or when less important bytes clutter analysis.', action='store', type=int)
    lArgParser.add_argument('-g', '--show-guesses', help='Show ascii representation for top byte of input. Tries ASCII lower, upper and numeric translations. Only works with -t/--top-frequencies.', action='store_true')
    lArgParser.add_argument('-col', '--columnar-analysis', help='Break INPUT into X columns and perform analysis on columns. Particuarly useful against polyalphabetic stream ciphers.', action='store', type=int)
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store', type=str)
    lInputSource = lArgParser.add_mutually_exclusive_group(required='True')
    lInputSource.add_argument('-i', '--input-file', help='Read INPUT to analyze from an input file', action='store', type=str)
    lInputSource.add_argument('INPUT', nargs='?', help='INPUT to analyze', action='store')
    lArgs = lArgParser.parse_args()

    if lArgs.show_all is False and lArgs.show_percent is False and lArgs.show_histogram is False and lArgs.show_ascii is False and lArgs.show_count is False and lArgs.show_ioc is False:
        lArgParser.error('No output chosen to display. Please choose at least one output option.')

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
    # end if

    if lArgs.show_all:
        lArgs.show_percent = lArgs.show_histogram = lArgs.show_ascii = lArgs.show_count = True

    if lArgs.show_percent or lArgs.show_histogram or lArgs.show_ascii or lArgs.show_count:

        if lArgs.columnar_analysis:
            lColumns = {lColumn: bytearray() for lColumn in range(0, lArgs.columnar_analysis)}
            lColumn = 0
            lCounter = 0
            for lByte in lInput:
                lColumns[lColumn].append(lByte)
                lColumn = (lColumn + 1) % lArgs.columnar_analysis

            for lColumn in lColumns:
                print("Analysis of Column {}".format(lColumn+1))
                print_analysis(lColumns[lColumn], lArgs.show_count, lArgs.show_histogram, lArgs.show_ascii, lArgs.show_percent, lArgs.show_guesses, lArgs.verbose, lArgs.top_frequencies, lArgs.columnar_analysis)
                print()
        else:
            print_analysis(lInput, lArgs.show_count, lArgs.show_histogram, lArgs.show_ascii, lArgs.show_percent, lArgs.show_guesses, lArgs.verbose, lArgs.top_frequencies, lArgs.columnar_analysis)

    if lArgs.show_ioc:
        print_delta_index_of_coincidence(lInput)