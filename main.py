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

def modular_pow(base, exponent, modulus):
    result = 1
    
    while (exponent > 0):
        if (exponent % 2 == 1):
            result = (result * base) % modulus
        
        exponent = exponent >> 1
        base = (base * base) % modulus
    
    return result

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

# Solves the diophantine equation ax + by = 1 using the Extended Euclidean Algorithm
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

# Chinese Remainder Theorem
# Returns a solution to the system x = a (mod m) and x = b (mod n)
def chineseRemainderTheorem(a, m, b, n):
    if (extendedEuclidean(m, n, False) != 1):
        print("Error: ", m, " and ", n, " are not coprime.")
        return -1
    
    s, t = diophantine(m, n)

    return ((a * t * n) + (b * s * m)) % (m * n)

def RSA(p, q):
    phi = (p - 1) * (q - 1)

    e = random.randint(1, phi) # Encryption exponent
    while (extendedEuclidean(e, phi, False) != 1):
        e = random.randint(1, phi)

    d = diophantine(e, phi)[0] # Decryption exponent using diophantine equation (e * x) + (phi * y) = 1

    return e, d

def pollardRho(n, x_0):
    
    if (n == 1):
        return n
    
    if (n % 2 == 0):
        return 2
    
    x = x_0
    y = x

    d = 1

    while (d == 1):
        x = (modular_pow(x, 2, n) + 1) % n
        
        y = (modular_pow(y, 2, n) + 1) % n
        y = (modular_pow(y, 2, n) + 1) % n

        d = extendedEuclidean(abs(x - y), n, False)

        if d == n:
            return pollardRho(n, x_0 + 1)
    
    return d

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

    # L Basis: N = 0, E = 1
    # V Basis: NW = 0, NE = 1

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
        if (len(response) != n):
            print("Invalid input, please try again!")
            continue
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

def QKDBob(photons):
    
    bases = []
    bits = []

    for photon in photons:
        rand = random.randint(0, 1)
        if (rand <= 0.5):
            bases.append("V")
        else:
            bases.append("L")

    print("Bob measured using the following bases: ", bases)

    storedResponse = ""

    isValid = False
    while (not isValid):
        response = input("Enter the bases you used to measure the photons (V or L): ")
        if (len(response) != len(photons)):
            print("Invalid input, please try again!")
            continue
        for char in response:
            if (char != "V" and char != "L"):
                print("Invalid input, please try again!")
                continue
        isValid = True
        storedResponse = response

    print("Bob measured using the following bases: ", bases)

    for i in range(0, len(photons)):
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

    key = []

    for i in range(0, len(storedResponse)):
        if (storedResponse[i] == bases[i]):
            key.append(bits[i])

    print("Your shared key is: ", key)


def main():
    
    selection = input("Select an option:\n1. Quantum Key Distribution\n2. Extended Euclidean Algorithm\n3. Chinese Remainder Theorem\n4. Quadratic Sieve\n5. Pollard's Rho Algorithm\n6. RSA\n")

    while (selection not in ["1", "2", "3", "4", "5", "6"]):
        print("Invalid input, please try again!")
        selection = input("Select an option:\n1. Quantum Key Distribution\n2. Extended Euclidean Algorithm\n3. Chinese Remainder Theorem\n4. Quadratic Sieve\n5. Pollard's Rho Algorithm\n6. RSA\n")
    
    if (selection == "1"):
        who = input("Press 1 to play Alice or 2 to play Bob: ")
        while (who not in ["1", "2"]):
            print("Invalid input, please try again!")
            who = input("Press 1 to play Alice or 2 to play Bob: ")

        if (who == "1"):
            photons = ["N", "NW", "N", "N", "NE", "NW", "E", "E"] # Change this to edit the photons being sent to Bob
            QKDBob(photons)
        elif (who == "2"):
            num = int(input("Enter the number of photons Alice should send you: "))
            QKDAlice(num)

    elif (selection == "2"):
        ### Find the GCD of two numbers using the Extended Euclidean Algorithm
        # 42823, 6409 
        extEucl1 = int(input("Enter the first number: "))
        extEucl2 = int(input("Enter the second number: "))
        soln = diophantine(extEucl1, extEucl2)
        print(extEucl1, "*", soln[0], "+", extEucl2, "*", soln[1], "= 1.")

    elif (selection == "3"):
        ### Find a solution to the system x = a (mod n) and x = b (mod m) using Chinese Remainder Theorem
        a = int(input("Enter the first number: "))
        n = int(input("Enter the first modulus: "))
        b = int(input("Enter the second number: "))
        m = int(input("Enter the second modulus: "))
        print("The solution to the system {x =", a, "( mod", n, "), x =", b, "( mod", m, ")} is: x =", chineseRemainderTheorem(a, n, b, m))

    elif (selection == "4"):
        ### Find a factor of n using Quadratic Sieve
        # 17155, 31861, 2201, 21719
        num = int(input("Enter the number to factor: "))
        numFactors = int(input("Enter the number of prime factorizations to find: "))
        soln = quadraticSieve(num, numFactors)
        if (soln is not None):
            print(soln[0], "and", soln[1], "are factors of", num)
    
    elif (selection == "5"):
        ### Find a factor of n using Pollard's Rho Algorithm
        num = int(input("Enter the number to factor: "))
        x_0 = int(input("Enter the starting value for x: "))
        print("A factor of", num, "is:", pollardRho(num, x_0))
    
    elif (selection == "6"):
        ### Have a message encrypted using RSA
        # 103333487, 299909459 # Two primes
        p = int(input("Enter the first prime: "))
        q = int(input("Enter the second prime: "))
        e, d = RSA(p, q)
        n = p * q
        message = random.randint(1, n)
        c = modular_pow(message, e, n)
        print("Your public key is: ( Encryption exponent:", e, ", modulus:", p * q, ")")
        print("Your private key is: ( Decryption exponent:", d)
        print("Encrypting the message '", message, "' using your public key...")
        print("Your encrypted message is:", c)
        print("To decrypt, use your decryption exponent")
        print("Decrypted message:", modular_pow(c, d, n))

main()