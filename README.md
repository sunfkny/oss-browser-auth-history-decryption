# OSS Browser Auth History Decryption

## Overview

This script is designed to decrypt encrypted auth history stored in the local storage of OSS Browser.

## Dependencies

### PowerShell script
Before running this script, ensure you have the following components installed on your system:

[PowerShell](https://github.com/PowerShell/PowerShell)

[SQLite](https://www.sqlite.org/)

### Python script
Before running this script, ensure you have the following components installed on your system:

[Python](https://www.python.org/)

[pycryptodomex](https://pypi.org/project/pycryptodomex/)

## References
### OSS Browser uses a static password to encrypt local storage.
[OSS Browser Cipher Implementation.](https://github.com/aliyun/oss-browser/blob/922153a57efae80185be7fd645760b791ea7ff90/app/components/services/cipher.js#L3-L4)

### The crypto.createDecipher method is deprecated.
[Node.js Deprecations Documentation.](https://github.com/nodejs/node/blob/668e52339261ec21c7388884620987914c833395/doc/api/deprecations.md#dep0106-cryptocreatecipher-and-cryptocreatedecipher)

### The crypto.createCipher method uses EVP_BytesToKey to generate the key and IV.
[Node.js Crypto Implementation.](https://github.com/nodejs/node/blob/668e52339261ec21c7388884620987914c833395/src/crypto/crypto_cipher.cc#L414)

### Openssl command equivalent to EVP_BytesToKey
```bash
openssl aes192 -k "x82m#*lx8vv" -md md5 -P -nosalt
```
[Openssl options](https://docs.openssl.org/master/man1/openssl-enc/)
