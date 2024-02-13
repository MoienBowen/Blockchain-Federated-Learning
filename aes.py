from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def encrypt_aes(key, plaintext):
    """
    Encrypt a plaintext using AES with a 128-bit key.

    Args:
    - key (bytes): The 128-bit AES key.
    - plaintext (bytes): The plaintext to be encrypted.

    Returns:
    - bytes: The ciphertext.
    """
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)

    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

    # Create a padder for PKCS7 padding
    padder = padding.PKCS7(128).padder()

    # Encrypt the plaintext
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padder.update(plaintext) + padder.finalize()) + encryptor.finalize()

    # Return the IV and ciphertext
    return iv + ciphertext

def decrypt_aes(key, ciphertext):
    """
    Decrypt a ciphertext using AES with a 128-bit key.

    Args:
    - key (bytes): The 128-bit AES key.
    - ciphertext (bytes): The ciphertext to be decrypted.

    Returns:
    - bytes: The decrypted plaintext.
    """
    # Extract the IV from the ciphertext
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    # Create an AES cipher object with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

    # Create an unpadder for PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()

    # Decrypt the ciphertext
    decryptor = cipher.decryptor()
    plaintext = unpadder.update(decryptor.update(ciphertext) + decryptor.finalize()) + unpadder.finalize()

    return plaintext

# # Example usage:
# key = os.urandom(16)  # 128-bit AES key

# plaintext = b"This is a secret message."

# # Encrypt the plaintext
# ciphertext = encrypt_aes(key, plaintext)
# print(f"Ciphertext: {ciphertext.hex()}")

# # Decrypt the ciphertext
# decrypted_text = decrypt_aes(key, ciphertext)
# print(f"Decrypted Text: {decrypted_text.decode('utf-8')}")
