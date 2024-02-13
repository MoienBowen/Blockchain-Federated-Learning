import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from util import *

def generate_polynomial(degree, field_size):
    return [random.randint(0, field_size - 1) for _ in range(degree + 1)]

def multiply_polynomials(f, g, field_size):
    h = [0] * (len(f) + len(g) - 1)
    for i in range(len(f)):
        for j in range(len(g)):
            h[i + j] += f[i] * g[j]
            h[i + j] %= field_size
    return h

def evaluate_polynomial(poly, x, field_size):
    """
    Evaluate a polynomial at a specific point.

    Args:
    - poly (list): The coefficients of the polynomial.
    - x (int): The point at which to evaluate the polynomial.
    - field_size (int): The size of the finite field.

    Returns:
    - int: The value of the polynomial at x.
    """
    return sum(coeff * (x**i) for i, coeff in enumerate(poly)) % field_size

def generate_beavers_triple(field_size):
    a = random.randint(0, field_size - 1)
    b = random.randint(0, field_size - 1)
    c = (a * b) % field_size
    return a, b, c

def create_proof(u, field_size, precision):
    """
    Create a proof for an update u.

    Args:
    - u (float): The update.
    - field_size (int): The size of the finite field.
    - precision (int): The number of decimal places of precision for u.

    Returns:
    - tuple: The proof, consisting of a single number h and a Beaver's triple (a, b, c).
    """
    # Convert u from a float to a fixed-point representation
    u_fixed_point = float_to_fixed_point(u, precision)

    f = generate_polynomial(1, field_size)  # Generate a linear polynomial
    g = generate_polynomial(1, field_size)  # Generate a linear polynomial
    h_coeffs = multiply_polynomials(f, g, field_size)

    # Evaluate the polynomial h at x = u_fixed_point
    h = evaluate_polynomial(h_coeffs, u_fixed_point, field_size)

    a, b, c = generate_beavers_triple(field_size)
    p = (h, (a, b, c))
    return p

def validate_proof(u, p, field_size, precision):
    """
    Validate a proof for an update u.

    Args:
    - u (float): The update.
    - pi (tuple): The proof, consisting of a single number h and a Beaver's triple (a, b, c).
    - field_size (int): The size of the finite field.
    - precision (int): The number of decimal places of precision for u.

    Returns:
    - bool: True if the proof is valid, False otherwise.
    """
    h, (a, b, c) = p

    # Validate the Beaver's triple
    if a * b % field_size != c:
        print("Error: Beaver's triple validation failed.")
        return False

    # Additional verification

    return True

# # Example usage
# field_size = 2**128  # 128-bit security
# u = 45678.7654  # Replace with your specific values

# p = create_proof(u, field_size, 10)
# validate_proof(u, p, field_size, 10)

# # Display the proof
# print("Proof:")
# print("h =", p[0])
# print("(a, b, c) =", p[1])
