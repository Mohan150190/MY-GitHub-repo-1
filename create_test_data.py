#!/usr/bin/env python3
"""
Test script to generate encrypted data for testing the AES decryption tool.
"""

import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def create_test_data():
    """Create test encrypted data for testing the decryption tool."""
    
    # Test key and plaintext
    key = b"mysecretkey12345"  # 16 bytes for AES-128
    plaintext = "Hello, World! This is a test message for AES-128 decryption."
    
    print(f"Original text: {plaintext}")
    print(f"Key: {key.decode('utf-8')}")
    print(f"Key (hex): {key.hex()}")
    
    # Pad the plaintext
    padded_text = pad(plaintext.encode('utf-8'), AES.block_size)
    
    # Test with CBC mode
    print("\n=== CBC Mode Test ===")
    iv = get_random_bytes(16)
    cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
    ciphertext_cbc = cipher_cbc.encrypt(padded_text)
    
    # Combine IV and ciphertext (common practice)
    encrypted_data_cbc = iv + ciphertext_cbc
    
    print(f"IV: {iv.hex()}")
    print(f"Encrypted (hex): {encrypted_data_cbc.hex()}")
    print(f"Encrypted (base64): {base64.b64encode(encrypted_data_cbc).decode('utf-8')}")
    
    # Test with ECB mode
    print("\n=== ECB Mode Test ===")
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    ciphertext_ecb = cipher_ecb.encrypt(padded_text)
    
    print(f"Encrypted (hex): {ciphertext_ecb.hex()}")
    print(f"Encrypted (base64): {base64.b64encode(ciphertext_ecb).decode('utf-8')}")
    
    return {
        'key': key,
        'plaintext': plaintext,
        'cbc_data': encrypted_data_cbc,
        'ecb_data': ciphertext_ecb,
        'iv': iv
    }

if __name__ == "__main__":
    create_test_data()