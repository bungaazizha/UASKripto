import random
from typing import List, Tuple

from .cryptomath import generate_prime, primitive_root


class PrivateKey:
    """
    ElGamal private key values
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, p: int, g: int, x: int, num_bits: int) -> None:
        self.p = p
        self.g = g
        self.x = x
        self.num_bits = num_bits


class PublicKey:
    """
    ElGamal public key values
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, p: int, g: int, h: int, num_bits: int) -> None:
        self.p = p
        self.g = g
        self.h = h
        self.num_bits = num_bits


class DecryptionError(BaseException):
    """
    Error when ElGamal decryption fails to perform
    """


def encode(plain: str, num_bits: int) -> List[int]:
    """
    Encodes string to array of integers through utf-16
    """
    byte_array = bytearray(plain, 'utf-16')

    # z is the array of integers mod p
    int_array = []

    # each encoded integer will be a linear combination of k message bytes
    # k must be the number of bits in the prime divided by 8 because each
    # message byte is 8 bits long
    k = num_bits // 8

    # j marks the jth encoded integer
    # j will start at 0 but make it -k because j will be incremented during first iteration
    j = -1 * k

    # i iterates through byte array
    for i, _ in enumerate(byte_array):
        # if i is divisible by k, start a new encoded integer
        if i % k == 0:
            j += k
            # num = 0
            int_array.append(0)
        # add the byte multiplied by 2 raised to a multiple of 8
        int_array[j // k] += byte_array[i] * (2 ** (8 * (i % k)))

    # example
        # if n = 24, k = n / 8 = 3
        # z[0] = (summation from i = 0 to i = k)m[i]*(2^(8*i))
        # where m[i] is the ith message byte

    # return array of encoded integers
    return int_array


def decode(ints: List[int], num_bits: int) -> str:
    """
    Decode array of integers to string through utf-16
    """

    # bytes array will hold the decoded original message bytes
    bytes_array = []

    # same deal as in the encode function.
    # each encoded integer is a linear combination of k message bytes
    # k must be the number of bits in the prime divided by 8 because each
    # message byte is 8 bits long
    k = num_bits // 8

    for num in ints:
        # get the k message bytes from the integer, i counts from 0 to k-1
        for i in range(k):
            # temporary integer
            temp = num

            # j goes from i+1 to k-1
            for j in range(i + 1, k):
                # get remainder from dividing integer by 2^(8*j)
                temp = temp % (2 ** (8 * j))

            # message byte representing a letter is equal to temp divided by 2^(8*i)
            letter = temp // (2 ** (8 * i))

            # add the message byte letter to the byte array
            bytes_array.append(letter)

            # subtract the letter multiplied by the power of two from num so
            # so the next message byte can be found
            num = num - (letter * (2 ** (8 * i)))

    decoded = bytearray(b for b in bytes_array).decode('utf-16')

    return decoded


def generate_keys(key_size: int = 256) -> Tuple[PrivateKey, PublicKey]:
    """
    Generate ElGamal public and private keypair
    """

    # p is the prime
    # g is the primitve root
    # x is random in (0, p-1) inclusive
    # h = g ^ x mod p
    p = generate_prime(key_size)
    g = primitive_root(p)
    g = pow(g, 2, p)
    x = random.randint(1, (p - 1) // 2)
    h = pow(g, x, p)

    public_key = PublicKey(p, g, h, key_size)
    private_key = PrivateKey(p, g, x, key_size)

    return private_key, public_key


def encrypt(key: PublicKey, plaintext: str) -> str:
    """
    Encrypts a plaintext string using the public key
    """

    encoded: List[int] = encode(plaintext, key.num_bits)

    # cipher_pairs list will hold pairs (c, d) corresponding to each integer in z
    cipher_pairs: List[Tuple[int, int]] = []

    # i is an integer in z
    for i in encoded:
        # pylint: disable=invalid-name

        # pick random y from (0, p-1) inclusive
        y = random.randint(0, key.p)

        # c = g^y mod p
        c = pow(key.g, y, key.p)

        # d = ih^y mod p
        d = (i * pow(key.h, y, key.p)) % key.p

        # add the pair to the cipher pairs list
        cipher_pairs.append((c, d))

    encrypted = ""
    for pair in cipher_pairs:
        encrypted += str(pair[0]) + ' ' + str(pair[1]) + ' '

    return encrypted


def decrypt(key: PrivateKey, cipher: str) -> str:
    """
    Performs decryption on the cipher pairs string using private key and returns the
    decrypted values
    """

    # decrpyts each pair and adds the decrypted integer to list of plaintext integers
    plaintext = []

    cipher_array = cipher.split()
    if not len(cipher_array) % 2 == 0:
        raise DecryptionError('Malformed Cipher Text')

    decrypted = ''
    for i in range(0, len(cipher_array), 2):
        # pylint: disable=invalid-name

        # c = first number in pair
        c = int(cipher_array[i])

        # d = second number in pair
        d = int(cipher_array[i+1])

        # s = c^x mod p
        s = pow(c, key.x, key.p)

        # plaintext integer = ds^-1 mod p
        plain = (d * pow(s, key.p - 2, key.p)) % key.p

        # add plain to list of plaintext integers
        plaintext.append(plain)

        decrypted = decode(plaintext, key.num_bits)

        # remove trailing null bytes
        decrypted = "".join([ch for ch in decrypted if ch != '\x00'])

    return decrypted
