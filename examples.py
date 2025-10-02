#!/usr/bin/env python3
"""
Example script demonstrating the AES-128 decryption tool usage.
This script shows how to use the tool with different scenarios.
"""

import subprocess
import sys
import os

def run_command(args, description):
    """Run a command and display the results."""
    print(f"\n{'='*60}")
    print(f"Example: {description}")
    print(f"Command: python aes_decrypt.py {' '.join(args)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            ["python", "aes_decrypt.py"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("Error output:")
        print(e.stderr)

def main():
    """Run example demonstrations."""
    print("AES-128 Decryption Tool - Examples")
    print("This script demonstrates various usage scenarios")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Example 1: Basic CBC decryption with hex input
    run_command([
        "-k", "mysecretkey12345",
        "-d", "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69",
        "-f", "hex"
    ], "Basic CBC decryption with hex input")
    
    # Example 2: Base64 input format
    run_command([
        "-k", "mysecretkey12345",
        "-d", "96eV3Lc22aZMObel4nQVXCrHW0KDFRkcVu5fKoi4SO8CzTLFCwOkH8tJ1k22SalS3I6sjtWkf60zFdWqP0pBA71nQ4o8ve3usEMG01+i3Wk=",
        "-f", "base64"
    ], "Decryption with base64 input format")
    
    # Example 3: ECB mode decryption
    run_command([
        "-k", "mysecretkey12345",
        "-d", "ea6f5f44a313afd043e33bbf65d8bd8a6f6c8b9d44c39ba9e34cf40196ee78de4cbac9059786a35e235f700a1348b773f15e8fe78d6649572864f2547f09d23d",
        "-f", "hex",
        "-m", "ECB"
    ], "ECB mode decryption")
    
    # Example 4: Hex key format
    run_command([
        "-k", "6d797365637265746b65793132333435",  # "mysecretkey12345" in hex
        "--key-format", "hex",
        "-d", "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69",
        "-f", "hex"
    ], "Using hex-formatted key")
    
    # Example 5: Verbose output
    run_command([
        "-k", "mysecretkey12345",
        "-d", "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69",
        "-f", "hex",
        "-v"
    ], "Verbose output mode")
    
    # Example 6: Error case - invalid key length
    run_command([
        "-k", "short",
        "-d", "test",
        "-f", "hex"
    ], "Error handling - invalid key length")
    
    print(f"\n{'='*60}")
    print("Examples completed!")
    print("For more information, run: python aes_decrypt.py --help")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()