# /// script
# dependencies = [
#     "pycryptodomex",
# ]
# ///
import hashlib
import json
import os
import pathlib
import sqlite3
import sys

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def green(message: str):
    return f"{bcolors.OKGREEN}{message}{bcolors.ENDC}"


def EVP_BytesToKey(
    password: bytes,
    salt: bytes | None,
    key_bits: int,
    iv_len: int,
):
    """
    https://www.npmjs.com/package/evp_bytestokey
    """
    if salt is not None and len(salt) != 8:
        raise ValueError("salt should be bytes with 8 byte length")

    key_len = key_bits // 8
    key = bytearray(key_len)
    iv = bytearray(iv_len)
    tmp = bytearray()

    while key_len > 0 or iv_len > 0:
        hash_md5 = hashlib.md5()
        hash_md5.update(tmp)
        hash_md5.update(password)
        if salt:
            hash_md5.update(salt)
        tmp = hash_md5.digest()

        used = 0

        if key_len > 0:
            key_start = len(key) - key_len
            used = min(key_len, len(tmp))
            key[key_start : key_start + used] = tmp[:used]
            key_len -= used

        if used < len(tmp) and iv_len > 0:
            iv_start = len(iv) - iv_len
            length = min(iv_len, len(tmp) - used)
            iv[iv_start : iv_start + length] = tmp[used : used + length]
            iv_len -= length

    return bytes(key), bytes(iv)


def decipher(encrypted: str):
    # from EVP_BytesToKey or `openssl aes192 -k "x82m#*lx8vv" -md md5 -P -nosalt`
    key = bytes.fromhex("fee4f348522b12260fec6ba9925686333635fae3febafca0")
    iv = bytes.fromhex("aac0e22065147dbd9f97881dae73f545")
    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = cipher.decrypt(bytes.fromhex(encrypted))
    decrypted = unpad(decrypted, AES.block_size)
    return decrypted.decode("utf8")


# https://www.electronjs.org/docs/latest/api/app#appgetpathname
if sys.platform == "win32":
    app_data = pathlib.Path(os.environ["APPDATA"])
elif sys.platform == "darwin":
    app_data = pathlib.Path("~/Library/Application Support")
else:
    app_data = pathlib.Path(os.environ.get("XDG_CONFIG_HOME", "~/.config"))

print(green("App Data Path:"))
print(app_data)

db_path = app_data / "oss-browser" / "Local Storage" / "file__0.localstorage"
db_path = db_path.expanduser()

print(green("Local Storage Path:"))
print(db_path)

with sqlite3.connect(db_path) as db:
    cursor = db.cursor()
    cursor.execute("SELECT value FROM ItemTable where key = 'auth-his'")
    value: bytes = cursor.fetchone()[0]

encrypted_hex = value.decode("utf16")
print(green("Encrypted Hex:"))
print(encrypted_hex)

decrypted_text = decipher(encrypted_hex)
print(green("Decrypted Text:"))
print(decrypted_text)

decrypted_data: list[dict] = json.loads(decrypted_text)
print(green("Decrypted Data:"))

for his in decrypted_data:
    for k, v in his.items():
        print(green(f"{k:<17}:"), v)
