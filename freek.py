import argparse, base64


TWO_DECIMAL_PLACES = "{0:.2f}"


def get_delta_index_of_coincidence(pInput: bytearray) -> dict:
    # IOC:
    # Calculate the frequency of each byte and total number of bytes
    # For each frequency f, calculate f(f - 1) and sum these values
    MAX_POSITIONS_TO_ANALYZE = 300

    lBytesOfInput = len(pInput)
    lPositionsToAnalyze = min(lBytesOfInput, MAX_POSITIONS_TO_ANALYZE)
    lIOC = dict.fromkeys(range(1, lPositionsToAnalyze), 0)
    for lBytesShifted in range(1, lPositionsToAnalyze):
        lMatches = 0
        lBytesToTest = lPositionsToAnalyze - lBytesShifted
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

    lScaleFactor = 10

    for lByteOffset, lCoincidence in lIOC.items():
        lPercentCoincidence = lCoincidence * 100
        lCoincidenceBarLength = int(lPercentCoincidence * lScaleFactor)

        lOutput = 'Byte Offset: '
        lOutput += str(lByteOffset) + ' '
        lOutput += "(" + TWO_DECIMAL_PLACES.format(lPercentCoincidence) + "%) "
        lOutput += "#" * lCoincidenceBarLength
        print(lOutput)
    # end for


def print_results(pByteCounts: dict, pTotalBytes: int, pShowHistogram: bool, pShowASCII: bool, pPercent: bool, pVerbose: bool) -> None:

    lScaleFactor = 20

    for lByte, lByteCount in pByteCounts.items():
        lPercent = lByteCount / pTotalBytes * 100
        lFrequencyBarLength = int(lPercent * lScaleFactor)

        if pVerbose or lByteCount:
            lOutput = ''
            if pVerbose:
                lOutput = 'Byte: '
            lOutput += str(lByte) + ' '
            if pShowASCII:
                lOutput += chr(lByte) + ' '
            lOutput += str(lByteCount) + ' '
            if pPercent:
                lOutput += "(" + TWO_DECIMAL_PLACES.format(lPercent) + "%) "
            if pShowHistogram:
                lOutput += "#" * lFrequencyBarLength
            print(lOutput)
        # end if
    # end for


def analyze(pInput: bytearray, pShowHistogram: bool, pShowASCII: bool, pPercent: bool, pVerbose: bool) -> None:
    lByteCounts = dict.fromkeys(range(0,256), 0)
    lTotalBytes = 0

    for lByte in pInput:
        lByteCounts[lByte] += 1
        lTotalBytes += 1
    # end for

    print_results(lByteCounts, lTotalBytes, pShowHistogram, pShowASCII, pPercent, pVerbose)


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lArgParser.add_argument('-p', '--show-percent', help='Show percent representation for each byte of input', action='store_true')
    lArgParser.add_argument('-g', '--show-histogram', help='Show histogram for each byte of input', action='store_true')
    lArgParser.add_argument('-a', '--show-ascii', help='Show ascii representation for each byte of input', action='store_true')
    lArgParser.add_argument('-all', '--show-all', help='Show count, ascii, percent represenation and histogram for each byte of input. Equivalent to -gs', action='store_true')
    lArgParser.add_argument('-ioc', '--show-ioc', help='Show kappa (delta) index of coincidence', action='store_true')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lArgParser.add_argument('INPUT', nargs='?', help='INPUT to analyze', type=str, action='store')
    lArgs = lArgParser.parse_args()

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
        lArgs.show_percent = lArgs.show_histogram = lArgs.show_ascii = True

    #analyze(lInput, lArgs.show_histogram, lArgs.show_ascii,  lArgs.show_percent, lArgs.verbose)

    if lArgs.show_ioc:
        print_delta_index_of_coincidence(lInput)