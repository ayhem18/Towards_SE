import argparse
from math import sqrt
from math import floor

## check the greate introductory tutorial on argparse module:
## https://docs.python.org/3/howto/argparse.html#introducing-optional-arguments 


def parse_1():
    parser = argparse.ArgumentParser()
    parser.parse_args()     

def parse_2():
    # let's improve it a bit
    p = argparse.ArgumentParser()
    p.add_argument('same', help='The program will display the value passed to this argument')
    # don't forget to actually parse the command line arguments
    args = p.parse_args()
    print(f"{args.same.upper()}... That's what she said...")

def parse_3():
    # all these arguments are positional and thus mandatory 
    # there are different types of arguments... you know
    p = argparse.ArgumentParser()
    p.add_argument('root', help='the square root of this number will be displayed', type=float)
    p.add_argument('--verbose', help='a more detailed output')
    p.add_argument('--int', help='a display the numbers as int if possible')
    args = p.parse_args()
    if args.root < 0:
        raise ValueError("Keep in mind, only non-negative numbers have square roots xD")
    
    def int_if_pos(number: float):
        return int(number) if floor(number) == number else number

    number = args.root
    root = sqrt(number)
        
    if args.int:
        number = int_if_pos(args.root)
        root = int_if_pos(root)

    if args.verbose:
        print(f"Well your input is {number} . Its square root: {root}")
    else:
        print(f"input: {number}")
        print(f"root: {root}")


## let's introduce optional arguments
def parse_4():
    p = argparse.ArgumentParser()
    p.add_argument("-v", "--verbosity", help='display a detailed output', action='store_true') # specifying both short and complete options
    args = p.parse_args()
    if args.verbosity:
        print("a more verbose output")
    else:
        print("output")

def parse_5():
    # combining optional and mandantory arguements while adding the possible values to be passed
    p = argparse.ArgumentParser()
    p.add_argument("-c", "--cube", help='display the cube of the passed value',type=float)
    
    # p.add_argument("-v", "--verbose", help='a more detailed output', type=int, choices=[0, 1, 2])

    # apparently either have choices or actions but can't have both....
    p.add_argument('-i', '--as_int', help='display the values as integer when possible',  choices=[True, False], type=bool) 
    
    # alternatively we can use the 'count' action instead of settings the values manually like: this
    p.add_argument('-v', '--verbose', help='verbosity level', action='count', default=0)

    args = p.parse_args()

    def int_if_pos(number: float):
        return int(number) if floor(number) == number else number

    number = args.cube
    cube = number ** 3
        
    if args.as_int:
        number = int_if_pos(number)
        cube = int_if_pos(cube)

    if args.verbose == 0:
        print(cube)
    elif args.verbose == 1:
        print(f'{number} ^ 3 == {cube}')
    else:
        print(f'The cube of the number {number} is equal to {cube}')

parse_5()
