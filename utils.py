""" Utilility functions for the main script """

import sys
from random import randint
from getpass import getpass
from typing import Union
from itertools import cycle
from functools import reduce
from operator import xor


def get_password():
    """ Requests for and reads password invisibly """

    pwd = getpass("Enter your password below. It is used to protect your credentials.\n"
                  "The password must have a minimum length of 8 characters "
                  "and can only contain alphanumeric characters and symbols.\n"
                  "Enter password (will be hidden): ")

    tries = 0  # Limit number of invalid attempts
    while True:
        if len(pwd) >= 8 and pwd.isascii() and pwd.isprintable() and ' ' not in pwd:
            if getpass("Confirm password: ") == pwd:
                return pwd
            else:
                print("Password mismatch!")
        else:
            print("Invalid characters in password or too short!")

        if tries == 3: return None
        pwd = getpass("\nRe-enter password: ")
        tries += 1


def xor_crypt(data: Union[bytes, bytearray], key: Union[int, bytes, bytearray]) -> bytes:
    """
    Encrypt/Decrypt data using XOR cipher

    Args:
        - data -> a bytes-like object, the content of which is to be en/decrypted.
        - key -> the en/decryption key, an integer in range(1, 256) or a bytes-like object.
    Returns the en/decrypted data as a `bytes` instance.

    Raises:
        - TypeError, if 'data' or 'key' is of an inappropriate type.
    """

    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("'data' must be bytes-like.")

    if isinstance(key, int):
        if not (0 < key < 256):  # 0 changes nothing
            raise ValueError("A integer key must be in range(1, 256).")
        return bytes([c^key for c in data])
    elif isinstance(key, (bytes, bytearray)) and key:
        return bytes([c^k for c, k in zip(data, cycle(key))])
    else:
        raise TypeError("'key' must be an integer or non-empty bytes-like object.")


def store_credentials(pwd:str, user: str, client_id: str, secret: str):
    """
    Encrypts the client secret and stores the credentials on-disk
    All arguments must to be ASCII-only strings for successful loading to be guaranteed.

    Note: Propagates any file-access exceptions.
    """

    pwd, user, client_id, secret = [s.encode() for s in (pwd, user, client_id, secret)]

    # 128 only sets the MSb (bit 7) and 255 simply flips the bits
    # MSb is always set, to ensure uniqueness of the delimeter used in the file.
    x = randint(129, 254)
    y = randint(129, 254)

    # The checksum is useless to a cracker without the original of
    # either the password or client secret
    checksum = xor_crypt(secret[7::-1]+secret[-1:-9:-1], pwd)
    pwd = xor_crypt(pwd, x)
    secret = xor_crypt(secret, y)
    user = xor_crypt(user, y)
    client_id = xor_crypt(client_id, y)
    secret = xor_crypt(secret, pwd)

    with open("credentials.bin", 'wb') as creds:
        # Getting original y requires encrypted password and original x
        # Getting encrpyted password requires original x
        # Getting original x requires the password
        creds.write(b'\0'.join((
                user,
                client_id,
                secret,
                bytes([reduce(xor, xor_crypt(pwd, x), x),
                       reduce(xor, pwd, x^y)
                      ]),
                # XOR-ed by 'y' to ensure every byte of the checksum has it's MSb set
                xor_crypt(checksum, y)
        )))


def load_credentials(pwd: str):
    """
    Reads stored credentials from disk

    Assumes that the credentials store exists and is readable.

    Returns:
        - A list containing the credentials, if the password is correct.
        - `None`, if the password is wrong.
    Raises `ValueError` if credentials store is corrupted. Also attaches original (causal) exception.
    """

    try:
        with open("credentials.bin", 'rb') as creds:
            user, client_id, secret, (x, y), checksum = creds.read().split(b'\0')
    except ValueError as e:
        raise ValueError("Corrupted credentials store.") from e

    pwd = pwd.encode()
    x = reduce(xor, pwd, x)
    pwd = xor_crypt(pwd, x)
    y = reduce(xor, pwd, x^y)
    secret = xor_crypt(secret, pwd)
    secret = xor_crypt(secret, y)
    user = xor_crypt(user, y)
    client_id = xor_crypt(client_id, y)

    checksum = xor_crypt(checksum, y)
    if xor_crypt(secret[7::-1]+secret[-1:-9:-1], xor_crypt(pwd, x)) == checksum:
        return [b.decode() for b in (user, client_id, secret)]

