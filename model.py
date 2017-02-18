import argparse


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Model: Calculates modulus ensuring answer is positive')
    lArgParser.add_argument('-m', '--modulus', help='Modulus. Default is 256.', action='store', default=256, type=int)
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('INPUT', help='Integer input value of which to calculate modulus. Required.', action='store', type=int)
    lArgs = lArgParser.parse_args()

    lModulus = lArgs.INPUT % lArgs.modulus
    if lModulus < 0:
        lModulus = lArgs.modulus + lModulus

    if lArgs.verbose:
        print()
        print("{} modulo {} is {}".format(lArgs.INPUT, lArgs.modulus, lModulus))
        print()
    else:
        print(lModulus)
