# Python Double Ratchet CLI

The Python Double Ratchet CLI tool provides an easy-to-use command-line interface for encrypting payloads using the Double Ratchet algorithm.

## Installation

Follow these steps to set up and run the Python Double Ratchet CLI tool:

### System Dependencies

Ensure you have the required system packages installed:

```bash
sudo apt update
sudo apt install libsqlcipher-dev build-essential git cmake libsqlite3-dev
```

### Python Environment

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/smswithoutborders/py_double_ratchet_cli.git
   cd py_double_ratchet_cli
   ```

2. **Set Up a Virtual Environment:**

   Create a virtual environment in your project directory to isolate dependencies:

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**

   ```bash
   source venv/bin/activate
   ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Arguments

- `-c`, `--content` (required): The content to encrypt.
- `-p`, `--phone_number` (required): The phone number associated with the encryption state.
- `-s`, `--sk` (required): The base64 encoded secret key for encryption.
- `-k`, `--ppk` (required): The base64 encoded public key for encryption.
- `-b`, `--base_dir` (optional): Base directory for state storage. If not provided, the default path used is `$HOME/.local/share/relaysms/storage`.

### Examples

1. **Encrypting Content:**

   ```bash
   python3 cli.py -c "Hello, World!" -p "+1234567890" -s "bXlzZWNyZXRrZXkxMjM0NQ==" -k "bXlzZWNyZXRrZXkxMjM0NQ=="
   ```

   This command will encrypt the content `"Hello, World!"` using the specified secret key and public key, associating the encryption state with the phone number `+1234567890`.

2. **Specifying a Base Directory:**

   ```bash
   python3 cli.py -c "Sensitive Data" -p "+1234567890" -s "bXlzZWNyZXRrZXkxMjM0NQ==" -k "bXlzZWNyZXRrZXkxMjM0NQ==" -b "/path/to/base/dir"
   ```

   This command specifies a custom base directory for storing the encryption state. If `-b` is not provided, the default path used is `$HOME/.local/share/relaysms/storage`.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Please follow the project's code style and provide clear descriptions of your changes.
