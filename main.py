# MATH 4440 Extra Credit
# Joel Luciano

from math import sqrt
from itertools import combinations
from collections import Counter
import math
import random

# Helper Functions
def diophantine(a, b):
    x_a = 1
    y_a = 0

    x_b = 0
    y_b = 1
    
    c = a % b

    while (c != 0):
        x_c = x_a - (int(a / b) * x_b)
        y_c = y_a - (int(a / b) * y_b)

        x_a = x_b
        y_a = y_b

        x_b = x_c
        y_b = y_c
        
        a = b
        b = c
        c = a % b

    return(x_c, y_c)

def eulerPhi(n):
    # Returns the number of integers less than n that are coprime to n
    factors = prime_factors(n)
    uniqueFactors = set(factors)

    phi = n
    for factor in uniqueFactors:
        phi *= (1 - (1 / factor))
    
    return int(phi)

def prime_factors(n):
    # Returns a list of prime factors of n
    # https://stackoverflow.com/questions/15347174/python-finding-prime-factors
    i = 2
    factors = []

    while (i * i <= n):
        if (n % i):
            i += 1
        else:
            n //= i
            factors.append(int(i))
    if (n > 1):
        factors.append(int(n))
    return factors

def find_even_occurrence_group(store):
    keys = list(store.keys())

    # Iterate over all possible combinations of the keys
    for r in range(1, len(keys) + 1):
        for combo in combinations(keys, r):
            # Flatten the lists corresponding to the combination of keys and count occurrences
            combined = [item for key in combo for item in store[key]]
            count = Counter(combined)

            # Check if all counts are even
            if all(c % 2 == 0 for c in count.values()):
                return combo

    # Return None if no group found
    return None

# Extended Euclidean Algorithm
# Returns the GCD of integers a and b
def extendedEuclidean(a, b, printSteps):
    
    if (b == 0):
        return a

    x = int(a / b)
    y = a % b

    if (printSteps):
        print(a, " = ", str(x), " * ", str(b), " + ", str(y))
    return extendedEuclidean(b, y, printSteps)

# Chinese Remainder Theorem
# Returns a solution to the system x = a (mod m) and x = b (mod n)
def chineseRemainderTheorem(a, m, b, n):
    if (extendedEuclidean(m, n, False) != 1):
        print("Error: ", m, " and ", n, " are not coprime.")
        return -1
    
    s, t = diophantine(m, n)

    return ((a * t * n) + (b * s * m)) % (m * n)

def RSA():
    # TODO
    return

def pollardRho():
    # TODO
    return

def indexCalculus():
    # TODO
    return

# Quadratic Sieve
# Returns two factors of n using the Quadratic Sieve algorithm
# Successful Examples: 17155, 31861, 2201
def quadraticSieve(n, numFactors):
    startingFactor = int(sqrt(n))

    if (startingFactor % 2 == 0):
        startingFactor += 1

    store = {}
    for i in range(0, numFactors):
        factor = startingFactor + (2 * i)
        store[factor] = prime_factors(math.pow(factor, 2) - n)

    group = find_even_occurrence_group(store)
    
    if (group == None):
        print("No suitable group of relations found.")
        return None
    
    else:
        a = 1
        b = 1
        for num in group:
            a = (a * num) % n
            b = b * math.prod(store[num]) % n
        
        b = sqrt(b)

        if (not b.is_integer()):
            print("No factors found")
            return None
        
        gcd = extendedEuclidean(a + b, n, False)

        return gcd, n / gcd

def QKDAlice(n):

    photons = []
    bases = []
    bits = []

    for i in range(0, n):
        rand = random.randint(0, 1)
        if (rand <= 0.25):
            photons.append("NW")
        elif (rand <= 0.5):
            photons.append("N")
        elif (rand <= 0.75):
            photons.append("NE")
        else:
            photons.append("E")

    for i in range(0, n):
        rand = random.randint(0, 1)
        if (rand <= 0.5):
            bases.append("V")
        else:
            bases.append("L")
    
    for i in range(0, n):
        if (bases[i] == "V"):
            if (photons[i] == "NW"):
                bits.append(0)
            elif (photons[i] == "NE"):
                bits.append(1)
            else:
                rand = random.randint(0, 1)
                if (rand <= 0.5):
                    bits.append(0)
                else:
                    bits.append(1)
        else:
            if (photons[i] == "N"):
                bits.append(0)
            elif (photons[i] == "E"):
                bits.append(1)
            else:
                rand = random.randint(0, 1)
                if (rand <= 0.5):
                    bits.append(0)
                else:
                    bits.append(1)

    print("Alice sends you the following photons: ", photons)

    storedResponse = ""

    isValid = False
    while (not isValid):
        response = input("Enter the bases you used to measure the photons (V or L): ")
        for char in response:
            if (char != "V" and char != "L"):
                print("Invalid input, please try again!")
                continue
        isValid = True
        storedResponse = response

    print("Alice measured using the following bases: ", bases)

    key = []
    for i in range(0, n):
        if (storedResponse[i] == bases[i]):
            key.append(bits[i])

    print("Your shared key is: ", key)

def QKDBob():
    # TODO
    return

def main():
    
    ### Find the GCD of two numbers using the Extended Euclidean Algorithm
    extEucl1, extEucl2 = 42823, 6409 
    
    print("The GCD of", extEucl1, "and", extEucl2, "is:", extendedEuclidean(extEucl1, extEucl2, True))
    ######################################################################

    ### Find a solution to the system x = a (mod n) and x = b (mod m) using Chinese Remainder Theorem
    a, n = 7, 11 # x = a (mod n)
    b, m = 3, 13 # x = b (mod m)
    
    print("The solution to the system {x =", a, "( mod", n, "), x =", b, "( mod", m, ")} is: x =", chineseRemainderTheorem(a, n, b, m))
    ######################################################################

    ### Find a factor of n using Quadratic Sieve
    num = 21719
    numFactors = 100 # Number of prime factorizations to find (don't set too high)
    
    print(quadraticSieve(num, numFactors))
    ######################################################################

    QKDAlice(8)


main()