"""
Storage Module
"""

import sqlite3
import hashlib
import os
from contextlib import closing


class StateStorage:
    """
    Manages storage and retrieval of state data using an SQLite database.
    The data is identified by the MD5 hash of a phone number.
    """

    def __init__(self, db_name="state.db", base_dir=None):
        """
        Initializes the StateStorage.

        Args:
            db_name (str): The name of the SQLite database file. Defaults to 'state.db'.
            base_dir (str): The base directory for the database. If None, a common default
                            path is used.
        """
        self.db_path = self._get_db_path(db_name, base_dir)
        self._create_table()

    @staticmethod
    def _get_db_path(db_name, base_dir):
        """
        Determines the path for the SQLite database.

        Args:
            db_name (str): The name of the database file.
            base_dir (str): The base directory for the database. If None, a common default
                            path is used.

        Returns:
            str: The full path to the SQLite database file.
        """
        if base_dir is None:
            base_dir = os.path.join(
                os.getenv("HOME"), ".local", "share", "relaysms", "storage"
            )

        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, db_name)

    def _create_table(self):
        """Creates the state table if it doesn't exist."""
        with closing(sqlite3.connect(self.db_path)) as conn:
            with conn:
                conn.execute(
                    """CREATE TABLE IF NOT EXISTS state (
                                        id TEXT PRIMARY KEY,
                                        data BLOB NOT NULL
                                    );"""
                )

    @staticmethod
    def _hash_phone_number(phone_number):
        """
        Generates an MD5 hash of the phone number.

        Args:
            phone_number (str): The phone number to hash.

        Returns:
            str: The MD5 hash of the phone number.
        """
        return hashlib.md5(phone_number.encode("utf-8")).hexdigest()

    def store(self, phone_number, state_data):
        """
        Stores the state data using the hashed phone number as the key.

        Args:
            phone_number (str): The phone number to hash and use as the key.
            state_data (bytes): The state data to store.
        """
        record_id = self._hash_phone_number(phone_number)
        with closing(sqlite3.connect(self.db_path)) as conn:
            with conn:
                conn.execute(
                    """INSERT OR REPLACE INTO state (id, data) VALUES (?, ?);""",
                    (record_id, state_data),
                )

    def retrieve(self, phone_number):
        """
        Retrieves the state data for the given phone number.

        Args:
            phone_number (str): The phone number to hash and use as the key.

        Returns:
            bytes: The state data if found, otherwise None.
        """
        record_id = self._hash_phone_number(phone_number)
        with closing(sqlite3.connect(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT data FROM state WHERE id = ?;""", (record_id,))
            row = cursor.fetchone()
            return row[0] if row else None

    def delete(self, phone_number):
        """
        Deletes the state data for the given phone number.

        Args:
            phone_number (str): The phone number to hash and use as the key.
        """
        record_id = self._hash_phone_number(phone_number)
        with closing(sqlite3.connect(self.db_path)) as conn:
            with conn:
                conn.execute("""DELETE FROM state WHERE id = ?;""", (record_id,))
