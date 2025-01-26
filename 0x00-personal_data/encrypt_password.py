#!/usr/bin/env python3

"""
Model for Encrypt Password
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt.

    Args:
      password (str): The password to be hashed.

    Returns:
      bytes: The hashed password.

    """
    salt = bcrypt.gensalt()  # Generate a random salt
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if a password matches a hashed password.

    Args:
      hashed_password (bytes): The hashed password to compare against.
      password (str): The password to check.

    Returns:
      bool: True if the password matches the hashed password, False otherwise.
    """
    hashed_password_str = hashed_password.decode('utf-8')
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password_str.encode('utf-8')
    )