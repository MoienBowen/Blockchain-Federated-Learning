import hashlib
from sympy import nextprime

def hash_(data):
    sha256_hash = hashlib.sha256(data.encode()).hexdigest()
    return sha256_hash

def gen_prime_2(n):
    range_min = 2**n
    range_max = range_min * 2
    prime_modulus = nextprime(random.randint(range_min, range_max))
    while prime_modulus >= range_max:
        prime_modulus = nextprime(random.randint(range_min, range_max))
    return prime_modulus

def gen_random(interval):
    r = random.choice(interval)
    return r

def gen_n_random(interval, n):
    r_list = [random.choice(interval) for _ in range(n)]
    return r_list

def char_to_num(char):
    """Convert a character to its numerical value."""
    return ord(char)

def num_to_char(num):
    """Convert a numerical value to its corresponding character."""
    return chr(num)

# def keep_n_digits(num, precision):
#     if precision < 1:
#         raise ValueError("precision must be a positive integer")

#     if num == 0:
#         return 0

#     integer_part = math.floor(num)
#     decimal_part = num - integer_part

#     if precision >= len(str(decimal_part)):
#         return num

#     decimal_part = str(decimal_part)[:precision]
#     decimal_part = "0" * (precision - len(decimal_part)) + decimal_part

#     return float(str(integer_part) + decimal_part)

def float_to_fixed_point(f, precision):
    """
    Convert a float to a fixed-point representation.

    Args:
    - f (float): The float to convert.
    - precision (int): The number of decimal places of precision.

    Returns:
    - int: The fixed-point representation of the float.
    """
    return int(round(f * 10**precision))

def fixed_point_to_float(i, precision):
    """
    Convert a fixed-point representation back to a float.

    Args:
    - i (int): The fixed-point representation.
    - precision (int): The number of decimal places of precision.

    Returns:
    - float: The original float.
    """
    return i / 10**precision
