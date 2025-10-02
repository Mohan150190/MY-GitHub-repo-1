# AES-128 Decryption Tool

A Python-based command-line tool for decrypting data encrypted with the AES-128 algorithm. This tool supports multiple input formats and AES modes, making it versatile for various decryption scenarios.

## Features

- **AES-128 decryption** with CBC and ECB modes
- **Multiple input formats**: hex, base64, and raw data
- **Flexible key input**: text or hex format
- **Command-line interface** with comprehensive options
- **Error handling** with descriptive messages
- **Output options**: console output or file output
- **Verbose mode** for debugging

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Mohan150190/MY-GitHub-repo-1.git
cd MY-GitHub-repo-1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python aes_decrypt.py -k "your16bytekey123" -d "encrypted_data_in_hex" -f hex
```

### Command-line Options

```
-k, --key KEY               Decryption key (must be 16 bytes for AES-128)
-d, --data DATA            Encrypted data to decrypt
-f, --format FORMAT        Input data format: hex, base64, raw (default: hex)
--key-format FORMAT        Key format: text, hex (default: text)
-m, --mode MODE           AES mode: CBC, ECB (default: CBC)
--iv IV                   Initialization vector (hex format, for CBC mode)
-o, --output FILE         Output file (default: console output)
-v, --verbose             Enable verbose output
-h, --help                Show help message
```

### Examples

#### 1. Decrypt hex-encoded data with text key (CBC mode)
```bash
python aes_decrypt.py -k "mysecretkey12345" -d "f7a795dcb736d9a64c39b7a5e274155c2ac75b428315191c56ee5f2a88b848ef02cd32c50b03a41fcb49d64db649a952dc8eac8ed5a47fad3315d5aa3f4a4103bd67438a3cbdedeeb04306d35fa2dd69" -f hex
```

#### 2. Decrypt base64-encoded data
```bash
python aes_decrypt.py -k "mysecretkey12345" -d "96eV3Lc22aZMObel4nQVXCrHW0KDFRkcVu5fKoi4SO8CzTLFCwOkH8tJ1k22SalS3I6sjtWkf60zFdWqP0pBA71nQ4o8ve3usEMG01+i3Wk=" -f base64
```

#### 3. Decrypt with ECB mode
```bash
python aes_decrypt.py -k "mysecretkey12345" -d "ea6f5f44a313afd043e33bbf65d8bd8a6f6c8b9d44c39ba9e34cf40196ee78de4cbac9059786a35e235f700a1348b773f15e8fe78d6649572864f2547f09d23d" -f hex -m ECB
```

#### 4. Use hex-formatted key
```bash
python aes_decrypt.py -k "6d797365637265746b65793132333435" --key-format hex -d "encrypted_data" -f hex
```

#### 5. Save output to file with verbose mode
```bash
python aes_decrypt.py -k "mysecretkey12345" -d "encrypted_data" -f hex -o decrypted.txt -v
```

#### 6. Specify custom IV for CBC mode
```bash
python aes_decrypt.py -k "mysecretkey12345" -d "encrypted_data_without_prepended_iv" -f hex --iv "f7a795dcb736d9a64c39b7a5e274155c"
```

## How It Works

### AES-128 Encryption/Decryption
- **Key Size**: 16 bytes (128 bits)
- **Block Size**: 16 bytes
- **Supported Modes**: CBC (Cipher Block Chaining), ECB (Electronic Code Book)

### Input Formats
- **Hex**: Hexadecimal representation (e.g., "48656c6c6f")
- **Base64**: Base64 encoding (e.g., "SGVsbG8=")
- **Raw**: Raw byte data

### CBC Mode (Default)
- **IV Handling**: By default, expects the IV to be prepended to the encrypted data
- **Custom IV**: Can specify a custom IV using the `--iv` option
- **Security**: More secure than ECB mode

### ECB Mode
- **No IV**: Does not use initialization vectors
- **Security**: Less secure than CBC mode, not recommended for production use

## Testing

Run the comprehensive test suite:

```bash
python test_aes_decrypt.py
```

Generate test data for experimentation:

```bash
python create_test_data.py
```

## Security Considerations

1. **Key Management**: Never hardcode keys in scripts or store them in plain text
2. **Mode Selection**: Use CBC mode for better security
3. **IV Handling**: Use unique IVs for each encryption operation
4. **Key Strength**: Ensure your 16-byte key has sufficient entropy

## Dependencies

- **pycryptodome**: Modern cryptographic library for Python
  ```bash
  pip install pycryptodome==3.19.0
  ```

## Error Handling

The tool provides comprehensive error handling for:
- Invalid key lengths
- Unsupported input formats
- Malformed encrypted data
- Invalid AES modes
- File I/O errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python test_aes_decrypt.py`
5. Submit a pull request

## License

This project is provided as-is for educational and utility purposes.
