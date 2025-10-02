#!/usr/bin/env python3
"""
AES128 Decryption Tool

This tool decrypts data encrypted with AES-128 algorithm using a provided security key.
Supports multiple input formats: hex, base64, and raw text.
"""

import argparse
import base64
import binascii
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class AES128Decryptor:
    """AES-128 decryption utility class."""
    
    def __init__(self, key):
        """
        Initialize the decryptor with a key.
        
        Args:
            key (str or bytes): The decryption key (must be 16 bytes for AES-128)
        """
        if isinstance(key, str):
            # If key is a string, encode it to bytes
            key = key.encode('utf-8')
        
        if len(key) != 16:
            raise ValueError("AES-128 requires a 16-byte key")
        
        self.key = key
    
    def decrypt_data(self, encrypted_data, input_format='hex', mode='CBC', iv=None):
        """
        Decrypt the encrypted data.
        
        Args:
            encrypted_data (str or bytes): The encrypted data to decrypt
            input_format (str): Format of input data ('hex', 'base64', 'raw')
            mode (str): AES mode ('CBC', 'ECB')
            iv (bytes): Initialization vector for CBC mode (if None, assumes it's prepended to data)
        
        Returns:
            str: The decrypted plaintext
        """
        try:
            # Convert input data to bytes based on format
            if input_format == 'hex':
                data_bytes = binascii.unhexlify(encrypted_data)
            elif input_format == 'base64':
                data_bytes = base64.b64decode(encrypted_data)
            elif input_format == 'raw':
                if isinstance(encrypted_data, str):
                    data_bytes = encrypted_data.encode('utf-8')
                else:
                    data_bytes = encrypted_data
            else:
                raise ValueError(f"Unsupported input format: {input_format}")
            
            # Handle different AES modes
            if mode.upper() == 'CBC':
                if iv is None:
                    # Assume IV is prepended to the encrypted data (first 16 bytes)
                    if len(data_bytes) < 16:
                        raise ValueError("Data too short to contain IV")
                    iv = data_bytes[:16]
                    ciphertext = data_bytes[16:]
                else:
                    ciphertext = data_bytes
                
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
            elif mode.upper() == 'ECB':
                cipher = AES.new(self.key, AES.MODE_ECB)
                ciphertext = data_bytes
            else:
                raise ValueError(f"Unsupported AES mode: {mode}")
            
            # Decrypt the data
            decrypted_padded = cipher.decrypt(ciphertext)
            
            # Remove PKCS7 padding
            try:
                decrypted = unpad(decrypted_padded, AES.block_size)
            except ValueError:
                # If unpadding fails, return the raw decrypted data
                print("Warning: Could not remove padding. Returning raw decrypted data.")
                decrypted = decrypted_padded
            
            # Try to decode as UTF-8, fall back to raw bytes representation
            try:
                return decrypted.decode('utf-8')
            except UnicodeDecodeError:
                return f"Raw bytes: {decrypted.hex()}"
                
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description='AES-128 Decryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Decrypt hex-encoded data with string key
  python aes_decrypt.py -k "mysecretkey12345" -d "1a2b3c4d..." -f hex

  # Decrypt base64-encoded data with hex key
  python aes_decrypt.py -k "6d79736563726574" -d "SGVsbG8gV29ybGQ=" -f base64 --key-format hex

  # Decrypt using ECB mode
  python aes_decrypt.py -k "mysecretkey12345" -d "1a2b3c4d..." -f hex -m ECB
        """
    )
    
    parser.add_argument('-k', '--key', required=True,
                       help='Decryption key (16 bytes for AES-128)')
    parser.add_argument('-d', '--data', required=True,
                       help='Encrypted data to decrypt')
    parser.add_argument('-f', '--format', choices=['hex', 'base64', 'raw'],
                       default='hex', help='Input data format (default: hex)')
    parser.add_argument('--key-format', choices=['text', 'hex'], default='text',
                       help='Key format (default: text)')
    parser.add_argument('-m', '--mode', choices=['CBC', 'ECB'], default='CBC',
                       help='AES mode (default: CBC)')
    parser.add_argument('--iv', help='Initialization vector (hex format, for CBC mode)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        # Process the key
        if args.key_format == 'hex':
            key = binascii.unhexlify(args.key)
        else:
            key = args.key
        
        # Process IV if provided
        iv = None
        if args.iv:
            iv = binascii.unhexlify(args.iv)
        
        if args.verbose:
            print(f"Key length: {len(key)} bytes")
            print(f"Input format: {args.format}")
            print(f"AES mode: {args.mode}")
            if iv:
                print(f"IV: {args.iv}")
        
        # Create decryptor and decrypt data
        decryptor = AES128Decryptor(key)
        result = decryptor.decrypt_data(args.data, args.format, args.mode, iv)
        
        # Output result
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            if args.verbose:
                print(f"Decrypted data written to: {args.output}")
        else:
            print("Decrypted data:")
            print(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()