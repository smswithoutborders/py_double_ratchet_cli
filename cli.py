"""Python Double Ratchet CLI"""

import os
import argparse
import base64
import struct
import sys
import traceback

from smswithoutborders_libsig.ratchets import Ratchets, States
from storage import StateStorage


def encrypt_payload(content, phone_number, sk, ppk, base_dir=None):
    """Encrypts a given payload string using the Double Ratchet algorithm.

    Args:
        content (str): The payload content to encrypt.
        phone_number (str): The phone number associated with the encryption state.
        sk (str): The base64 encoded secret key for encryption.
        ppk (str): The base64 encoded public key for encryption.
        base_dir (str, optional): Base directory for state storage. Defaults to None.

    Returns:
        str: The base64 encoded encrypted payload.
    """
    sk_decoded = base64.b64decode(sk)
    ppk_decoded = base64.b64decode(ppk)

    state_storage = StateStorage(base_dir=base_dir)
    current_state = state_storage.retrieve(phone_number=phone_number)
    ratchet_db_path = os.path.join(os.path.dirname(state_storage.db_path), "ratchet.db")

    if not current_state:
        if os.path.exists(ratchet_db_path):
            os.remove(ratchet_db_path)

        state = States()
        Ratchets.alice_init(state, sk_decoded, ppk_decoded, ratchet_db_path)
    else:
        state = States.deserialize(current_state)

    header, content_ciphertext = Ratchets.encrypt(
        state=state, data=content.encode("utf-8"), AD=ppk_decoded
    )

    serialized_header = header.serialize()
    len_header = len(serialized_header)

    state_storage.store(phone_number=phone_number, state_data=state.serialize())

    return base64.b64encode(
        struct.pack("<i", len_header) + serialized_header + content_ciphertext
    ).decode("utf-8")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Python Double Ratchet CLI.")
    parser.add_argument(
        "-c", "--content", type=str, required=True, help="The content to encrypt."
    )
    parser.add_argument(
        "-p",
        "--phone_number",
        type=str,
        required=True,
        help="The phone number associated with the encryption state.",
    )
    parser.add_argument(
        "-s", "--sk", type=str, required=True, help="The secret key for encryption."
    )
    parser.add_argument(
        "-k", "--ppk", type=str, required=True, help="The public key for encryption."
    )
    parser.add_argument(
        "-b",
        "--base_dir",
        type=str,
        default=None,
        help="Base directory for state storage (optional).",
    )
    return parser.parse_args()


def main():
    """Main entry point for the CLI tool."""
    args = parse_arguments()

    try:
        encrypted_payload = encrypt_payload(
            content=args.content,
            phone_number=args.phone_number,
            sk=args.sk,
            ppk=args.ppk,
            base_dir=args.base_dir,
        )
        print(encrypted_payload)
        sys.exit(0)
    except Exception:
        print("Oops! An error occurred:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
