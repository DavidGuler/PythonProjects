"""
Name: ssprco.py

Purpose: A code for calculating Substring sums of prime concatenations.

Description: 
There are 3 definitions:
- S(n) = Sum of all integer substrings possible of n.
- P(n) = An integer formed by concatenating the first n primes together.
- C(n,k) = An integer formed by concatenating k copies of P(n).

The code evaluates the following equation:
S(C(P(10 ^ 6), 10 ^ 12)) % (10 ^ 9 + 7)

Process:
S(C(P(n), m)) % MOD

|
V

P(n) = p1 + p2*10**l2 + p3*10**l3 + ... + pn*10**ln

C(k, n) = k + k*10**lk*1 + k*10**lk*2 + k*10**lk*3 + ... + k*10**lk*(n - 1) = k * ((10 ** lk) ** n - 1) / 10 ** lk - 1

S(n) = s1(n, 1) + s2(n, 2) + s3(n, 3) + ... + sln(n, ln) = 

========================================================

C(P(n), m) = P(n) * ((10 ** lP(n)) ** m - 1) / 10 ** lP(n) - 1

S(C(P(n), m)) = s1(C(P(n), m), 1) + s2(C(P(n), m), 2) + s3(C(P(n), m), 3) + ... + C(P(n), m*lP(n))

Author: David.G
"""

### Imports.
import pyprimes
import gmpy2
import math
from mod import Mod

### Consts.
WORKING_BASE = 10
BINARY = 2
MOD = 10**9 + 7
MAX_POWER = 100

### Functions.

def get_gp_sum(a1, q, n):
	"""
	"""

	return (a1 * (q**n - 1)) / (q - 1)

def to_bin(num, working_base=WORKING_BASE):
    """
    to_bin(num) -> int(bin_num)

    Calculates the binary of num.

    @param        num(int) -> A number.
    @param        working_base(int) -> num's base.
    @return        bin_num(int) -> num's binary value.
    """

    # Initialize.
    bin_num = 0

    # Finding the closest power of 2 to num. Then summerizing
    # the binary value of num and decreasing num until it's zero.
    while num > 0:
        bin_digit = int(gmpy2.log2(num))
        bin_num += working_base ** bin_digit
        num -= BINARY ** bin_digit

    return bin_num

def sum_num_digits(num, base_log, working_base=WORKING_BASE):
    """
    sum_num_digits(num, num_len, base_log, working_base) -> int(summary)

    Summerize all the base_log length's sub-numbers possible within num.
    sub-numbers are the digits of the number in (working_base ** base_log)'
    base.
    
    @param        num(int) - A number.
    @param        num_len(int) - Num's length.
    @param        base_log(int) - Each num's sub-number's length; Also the numerical 
                                base's log.
    @param        working_base(int) - Num's numerical base.
    @return       summary(int) - The summary of all sub-numbers found.
    """

    # Initialize.
    summary = 0
    base = working_base ** base_log
    num_len = int(math.log10(num)) + 1

    # Summerizing all sub-numbers for base_log amount of iterations,
    # due to amount of options of base_log lengths' sub-numbers in num.
    for i in range(0, base_log):

        # Break out of loop if the length of num is too small.
        if num_len < base_log:
            break

        # Make sure that base_log is a root of num's length.
        temp_num_len = num_len - (num_len % base_log)
        temp_num = num % (working_base ** temp_num_len)
        num_of_digits = int(round(temp_num_len / base_log))
        
        # Summerize all the digits.
        # Note: This equation doesn't calculate all the possible digits.
        for j in range(0, num_of_digits):
            summary += (((1 / base ** j) % MOD) * ((((temp_num % (base ** (j + 1) % MOD))) % MOD) - ((temp_num % (base ** j)) % MOD)) % MOD) % MOD

        # Prepare num for next iteration, for finding more sub-numbers.
        num /= working_base
        num_len -= 1

    return int(summary)


def sum_num_substrings(num, num_len):
    """
    sum_num_substrings(num) -> int(number)

    Summerizing all num's substrings.

    :@param     num(int) - A number.
    :@param     num_len(int) - Num's length.
    :@return    sum_num_substrings(int) - Num's substrings' summary.
    """

    # Verbose.
    print("Calculating the sum of all substrings of the number by length {1}".format(num_len))

    # Summerizing all the possible substrings within num.
    return sum([sum_num_digits(num, num_len, base_log) for base_log in range(1, num_len + 1)])

def concat_n_primes(n):
    """
    concat_n_primes(n) -> int(number)
    
    Concatenating the first n primes from zero into a number.

    :@param     n(int) - An index number.
    :@return    concat_n_primes(int) - A number formed by concatenating 
                                       the n first primes.
    """

    # Verbose.
    print("Concatenating first {0} primes together".format(n))

    # Initialize.
    num_len = 0
    result = Mod(0, MOD)

    # Concatenating the first n primes.
    for prime_num in pyprimes.nprimes(n):
        result += prime_num
        num_len += len(str(prime_num))

    return result, num_len

def concat_clones_of_num(num, num_len, k):
    """
    concat_clones_of_num(num, k) -> number

    Creates a number formed of concatenating k appearences of num.
    For multiplying num for k times, using the summary of the geometric 
    progression of:
        an = a1 * 2 ** (num_len * k)

    Which represents the binary digits that in decimal base can multiply
    num fo k times.

    :@param        num(int) - A number
    :@param        k(int) - A number presenting the amount of appearnces
    :@result       tuple(int, int) - A tuple of the result of concatenating num to itself 
                                     k times, and the result length.
    """

    # Verbose.
    print("Concatenating the number for {0} times".format(k))

    # Initialize.
    res_num = 0

    # 
    result = get_gp_sum(num, Mod(10 ** num_len, MOD), k)

    # Returning num multiplied, and its length for future calculations.
    return result, num_len*k
        

if __name__ == "__main__":
    
    num1 = 10
    num2 = 7

    s = sum_num_substrings(concat_clones_of_num(*concat_n_primes(num1 ** 6), num1 ** 12)) % MOD

    print("The result of S(C(10 ** 6, 10 ** 12)) mod (10 ** 9 + 7) is {0}".format(s))