#  Hybrid Encryption System (AES + RSA)

##  Overview

This project implements a Hybrid Encryption System combining AES and RSA algorithms to ensure secure communication.

* AES → Fast data encryption
* RSA → Secure key exchange

##  Features

* GUI-based application
* AES encryption (EAX mode)
* RSA key generation
* Secure encryption & decryption

##  Tech Stack

* Python
* Flask
* HTML, CSS
* PyCryptodome

##  Workflow

1. User inputs message
2. AES encrypts message
3. RSA encrypts AES key
4. Data stored securely
5. Decryption reverses process

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

##  Output

* Encrypted Message
* Encrypted AES Key
* Decrypted Message

##  Security Note

Private keys are not shared publicly.

## Future Improvements

* Database integration
* User authentication
* Cloud deployment
