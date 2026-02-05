#!/usr/bin/env python
"""
Generate a secure SECRET_KEY for Django production use.
Run this script and copy the output to your Northflank environment variables.
"""
import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 70)
    print("Generated Django SECRET_KEY:")
    print("=" * 70)
    print(secret_key)
    print("=" * 70)
    print("\nCopy this key and add it to your Northflank environment variables.")
    print("NEVER commit this key to version control!")
