import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_first_n_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

n = int(input("Enter the number of prime numbers to generate: "))
primes = get_first_n_primes(n)

print("First", n, "prime numbers are:")
for i, prime in enumerate(primes):
    print(f"Number {i+1}: {prime}")