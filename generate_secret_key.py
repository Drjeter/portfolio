#!/usr/bin/env python
"""
Generate a secure SECRET_KEY for Django production use.
Run this script and copy the output to your Northflank environment variables.
"""
from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("=" * 70)
    print("Generated Django SECRET_KEY:")
    print("=" * 70)
    print(secret_key)
    print("=" * 70)
    print("\nCopy this key and add it to your Northflank environment variables.")
    print("NEVER commit this key to version control!")
