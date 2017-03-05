import argparse, math

# Requires pip install bitarray
from bitarray import bitarray


def derive_transfer_function(pTransferFunctionString: str) -> list:

    lTransferFunction = list(map(int, pTransferFunctionString.split(',')))
    lTransferFunctionValid = True
    lLengthTransferFunction = len(lTransferFunction)
    for i in range(0, lLengthTransferFunction):
        if i not in lTransferFunction:
            lTransferFunctionValid = False
            break
        # end if
    # end for

    if not lTransferFunctionValid:
        raise Exception('Transfer function must contain all integers from 0 to N where (N - 1) is length of the substitution array.')

    lExponent = math.log(lLengthTransferFunction, 2)
    if lExponent != math.floor(lExponent):
        raise Exception('Transfer function length must be even power of 2.')

    return lTransferFunction


def print_transfer_function_table(pTransferFunction: list) -> None:

    lLengthTransferFunction = len(pTransferFunction)
    lNumberBits = int(math.log(lLengthTransferFunction, 2))
    lFormat = '0' + str(lNumberBits) + 'b'

    # print column headers
    print()
    for i in range(0, lNumberBits):
        print("x" + str(i) + "\t", end="")
    for i in range(0, lNumberBits):
        print("y" + str(i) + "\t", end="")
    print()

    # print values for transfer function
    for lIndex, lSubstitutionValue in enumerate(pTransferFunction):

        lBinaryIndex = bitarray(format(lIndex, lFormat))
        lBinarySV = bitarray(format(lSubstitutionValue, lFormat))

        for i in range(0, lNumberBits):
            print(int(lBinaryIndex[i]), end="")
            print("\t", end="")
        for i in range(0, lNumberBits):
            print(int(lBinarySV[i]), end="")
            print("\t", end="")
        print()
    print()


def print_linear_approximation_table(pTransferFunction: list) -> None:

    lLengthTransferFunction = len(pTransferFunction)
    lNumberBits = int(math.log(lLengthTransferFunction, 2))
    lFormat = '0' + str(lNumberBits) + 'b'

    # print column headers
    print("\t", end="")
    for i in range(0, lLengthTransferFunction):
        print("b" + str(i) + "\t", end="")
    print()

    for lA in range(0, lLengthTransferFunction):

        print("a" + str(lA) + "\t", end="")

        for lB in range(0, lLengthTransferFunction):

            a = bitarray(format(lA, lFormat))
            b = bitarray(format(lB, lFormat))

            lCount = 0
            for lX, lY in enumerate(pTransferFunction):

                x = bitarray(format(lX, lFormat))
                y = bitarray(format(lY, lFormat))

                lVectorXorOfAX = 0
                for i in range(0, lNumberBits):
                    lVectorXorOfAX ^= int(a[i]) * int(x[i])

                lVectorXorOfBY = 0
                for i in range(0, lNumberBits):
                    lVectorXorOfBY ^= int(b[i]) * int(y[i])

                lAXxorBY = lVectorXorOfAX ^ lVectorXorOfBY

                if lAXxorBY == 0:
                    lCount += 1
            # end looping through transfer function

            print(str(lCount) + "\t", end="")
        # end for b

        print()
    # end for a

if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Transference: A tool to help visualize s-boxes (substitution boxes or transfer functions)')
    lArgParser.add_argument('-tft', '--transfer-function-table', help='Print the transfer function table for the s-box', action='store_true')
    lArgParser.add_argument('-lat', '--linear-approximation-table', help='Calculate the linear transformation table for the s-box', action='store_true')
    lArgParser.add_argument('-all', '--all', help='Calculate the linear transformation table for the s-box', action='store_true')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('INPUT', action='store', type=str, help='The substitution table (s-box) represented as a comma delimted list of integers. The length of the list is the number of bits in the substitution. Required. Example: 3,2,0,1 means substitute 3 for 0, 2 for 1, 0 for 2 and 1 for 3. ')
    lArgs = lArgParser.parse_args()

    lTransferFunction = derive_transfer_function(lArgs.INPUT)

    if lArgs.all:
        lArgs.transfer_function_table = lArgs.linear_approximation_table = True

    if lArgs.transfer_function_table:
        print_transfer_function_table(lTransferFunction)

    if lArgs.linear_approximation_table:
        print_linear_approximation_table(lTransferFunction)


