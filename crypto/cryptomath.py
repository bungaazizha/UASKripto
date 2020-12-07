import random


class ModularInverseError(BaseException):
    """
    Error raised when modular inversion on a number cannot be performed
    """


class NotPrimeError(BaseException):
    """
    Raised when a number is not prime and fails to perform an operation that requires prime number
    such as finding the primitive root.
    """


def gcd(num_a: int, num_b: int) -> int:
    """
    Find the greatest common divisor between two numbers
    """
    while num_a != 0:
        num_a, num_b = num_b % num_a, num_a
    return num_b


def mod_inverse(num: int, modulus: int) -> int:
    """
    Perform modular inverse on `num` in `modulus`
    """
    if gcd(num, modulus) != 1:
        raise ModularInverseError('gcd is equals to 1')
    u_1, u_2, u_3 = 1, 0, num
    v_1, v_2, v_3 = 0, 1, modulus

    while v_3 != 0:
        quot = u_3 // v_3
        v_1, v_2, v_3, u_1, u_2, u_3 = (
            u_1 - quot * v_1), (u_2 - quot * v_2), (u_3 - quot * v_3), v_1, v_2, v_3
    return u_1 % modulus


def primitive_root(num: int) -> int:
    """
    Find a primitive root for prime `p`.

    This function was implemented from the algorithm described here:

    http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
    """

    if not is_prime(num):
        raise NotPrimeError()

    if num == 2:
        return 1

    # the prime divisors of p-1 are 2 and (p-1)/2 because
    # p = 2x + 1 where x is a prime
    p_1 = 2
    p_2 = (num - 1) // p_1

    # test random g's until one is found that is a primitive root mod p
    while True:
        # g is a primitive root if for all prime factors of p-1, p[i]
        g = random.randint(2, num-1)

        # g^((p-1)/p[i]) (mod p) is not congruent to 1
        if not pow(g, (num-1) // p_1, num) == 1:
            if not pow(g, (num-1) // p_2, num) == 1:
                return g


def rabin_miller(num: int) -> bool:
    """
    Rabin–Miller primality test
    """
    # pylint: disable=invalid-name

    s = num - 1
    t = 0

    while s % 2 == 0:
        s = s // 2
        t += 1
    for _ in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                i = i + 1
                v = (v ** 2) % num
        return True
    return False


def is_prime(num: int) -> bool:
    """
    Check if an integer is prime
    """
    if num < 2:
        return False
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
                  79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
                  167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251,
                  257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
                  353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                  449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557,
                  563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647,
                  653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757,
                  761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
                  877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                  991, 997]
    if num in low_primes:
        return True
    for prime in low_primes:
        if num % prime == 0:
            return False
    return rabin_miller(num)


def generate_prime(size: int) -> int:
    """
    Generate a random prime integer with `size`-bit
    """
    while True:
        num = random.randrange(2 ** (size - 1), 2 ** (size))
        if is_prime(num):
            return num
