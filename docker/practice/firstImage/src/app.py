import sys

from utils import find_primes


def main():
    args = sys.argv

    n = None

    if len(args) == 1:
        n = 100
    
    elif len(args) == 2:
        try: 
            n = int(args[1])
        except:
            print("Make sure to pass an integer as a second argument")
            n = 100

    else:
        print(f"Expecting either 1 or 2 arguments... found: {len(args)}... abort !!")
        return 
    
    primes = find_primes(n)
    
    if len(primes) == 0:
        print(f"it seems that there are no prime numbers less or equal to {n}. Make sure to pass a number larger or equal to '2' (100 for things to get interesting)")    


    print(f"Here is the list of prime numbers less or equal to {n}") 

    for p in primes: 
        print(p)


def better_main():
    try:
        while True:
            n = int(input("Enter a number: "))
            primes = find_primes(n)
            print(primes)
    except KeyboardInterrupt:
        print("Sad to see you go...")
        print("Exiting...") 
        return

from time import sleep

def infinite_loop():
    while True:
        sleep(10)
        print("I'm alive..., just slept for 10 seconds")


if __name__ == '__main__':
    infinite_loop()
    
