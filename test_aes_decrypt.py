#!/usr/bin/env python3
"""
Test suite for the AES-128 decryption tool.
"""

import unittest
import subprocess
import tempfile
import os
from aes_decrypt import AES128Decryptor


class TestAES128Decryptor(unittest.TestCase):
    """Unit tests for the AES128Decryptor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.key = "mysecretkey12345"  # 16 bytes
        self.decryptor = AES128Decryptor(self.key)
        
    def test_key_validation(self):
        """Test key length validation."""
        # Valid 16-byte key
        try:
            AES128Decryptor("mysecretkey12345")
        except ValueError:
            self.fail("Valid 16-byte key should not raise ValueError")
        
        # Invalid key lengths
        with self.assertRaises(ValueError):
            AES128Decryptor("short")  # Too short
        
        with self.assertRaises(ValueError):
            AES128Decryptor("this_is_too_long_for_aes128")  # Too long
    
    def test_hex_format_decryption(self):
        """Test decryption with hex input format."""
        # Known encrypted data (CBC mode with prepended IV)
        encrypted_hex = "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69"
        expected = "Hello, World! This is a test message for AES-128 decryption."
        
        result = self.decryptor.decrypt_data(encrypted_hex, 'hex', 'CBC')
        self.assertEqual(result, expected)
    
    def test_base64_format_decryption(self):
        """Test decryption with base64 input format."""
        encrypted_b64 = "96eV3Lc22aZMObel4nQVXCrHW0KDFRkcVu5fKoi4SO8CzTLFCwOkH8tJ1k22SalS3I6sjtWkf60zFdWqP0pBA71nQ4o8ve3usEMG01+i3Wk="
        expected = "Hello, World! This is a test message for AES-128 decryption."
        
        result = self.decryptor.decrypt_data(encrypted_b64, 'base64', 'CBC')
        self.assertEqual(result, expected)
    
    def test_ecb_mode_decryption(self):
        """Test ECB mode decryption."""
        encrypted_hex = "ea6f5f44a313afd043e33bbf65d8bd8a6f6c8b9d44c39ba9e34cf40196ee78de4cbac9059786a35e235f700a1348b773f15e8fe78d6649572864f2547f09d23d"
        expected = "Hello, World! This is a test message for AES-128 decryption."
        
        result = self.decryptor.decrypt_data(encrypted_hex, 'hex', 'ECB')
        self.assertEqual(result, expected)
    
    def test_invalid_input_format(self):
        """Test error handling for invalid input formats."""
        with self.assertRaises(Exception):
            self.decryptor.decrypt_data("test", 'invalid_format')
    
    def test_invalid_aes_mode(self):
        """Test error handling for invalid AES modes."""
        with self.assertRaises(Exception):
            self.decryptor.decrypt_data("aa", 'hex', 'INVALID_MODE')


class TestCommandLineInterface(unittest.TestCase):
    """Integration tests for the command-line interface."""
    
    def run_command(self, args):
        """Helper method to run the CLI command."""
        cmd = ["python", "aes_decrypt.py"] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result
    
    def test_help_command(self):
        """Test help command."""
        result = self.run_command(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("AES-128 Decryption Tool", result.stdout)
    
    def test_successful_decryption(self):
        """Test successful decryption via CLI."""
        result = self.run_command([
            "-k", "mysecretkey12345",
            "-d", "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69",
            "-f", "hex"
        ])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Hello, World! This is a test message for AES-128 decryption.", result.stdout)
    
    def test_base64_input(self):
        """Test base64 input via CLI."""
        result = self.run_command([
            "-k", "mysecretkey12345",
            "-d", "96eV3Lc22aZMObel4nQVXCrHW0KDFRkcVu5fKoi4SO8CzTLFCwOkH8tJ1k22SalS3I6sjtWkf60zFdWqP0pBA71nQ4o8ve3usEMG01+i3Wk=",
            "-f", "base64"
        ])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Hello, World! This is a test message for AES-128 decryption.", result.stdout)
    
    def test_ecb_mode(self):
        """Test ECB mode via CLI."""
        result = self.run_command([
            "-k", "mysecretkey12345",
            "-d", "ea6f5f44a313afd043e33bbf65d8bd8a6f6c8b9d44c39ba9e34cf40196ee78de4cbac9059786a35e235f700a1348b773f15e8fe78d6649572864f2547f09d23d",
            "-f", "hex",
            "-m", "ECB"
        ])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Hello, World! This is a test message for AES-128 decryption.", result.stdout)
    
    def test_hex_key_format(self):
        """Test hex key format via CLI."""
        result = self.run_command([
            "-k", "6d797365637265746b65793132333435",  # "mysecretkey12345" in hex
            "--key-format", "hex",
            "-d", "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69",
            "-f", "hex"
        ])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Hello, World! This is a test message for AES-128 decryption.", result.stdout)
    
    def test_verbose_output(self):
        """Test verbose output via CLI."""
        result = self.run_command([
            "-k", "mysecretkey12345",
            "-d", "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69",
            "-f", "hex",
            "-v"
        ])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Key length: 16 bytes", result.stdout)
        self.assertIn("Input format: hex", result.stdout)
        self.assertIn("AES mode: CBC", result.stdout)
    
    def test_output_file(self):
        """Test output to file via CLI."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            output_file = tmp_file.name
        
        try:
            result = self.run_command([
                "-k", "mysecretkey12345",
                "-d", "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69",
                "-f", "hex",
                "-o", output_file
            ])
            self.assertEqual(result.returncode, 0)
            
            # Check if output file contains expected content
            with open(output_file, 'r') as f:
                content = f.read()
            self.assertIn("Hello, World! This is a test message for AES-128 decryption.", content)
        finally:
            # Clean up
            if os.path.exists(output_file):
                os.unlink(output_file)
    
    def test_invalid_key_length(self):
        """Test error handling for invalid key length."""
        result = self.run_command([
            "-k", "short",
            "-d", "test",
            "-f", "hex"
        ])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error:", result.stderr)
    
    def test_missing_required_args(self):
        """Test error handling for missing required arguments."""
        result = self.run_command(["-k", "mysecretkey12345"])
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    # Change to the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    unittest.main(verbosity=2)