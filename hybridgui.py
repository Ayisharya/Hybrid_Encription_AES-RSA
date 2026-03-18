from flask import Flask, render_template, request
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64

app = Flask(__name__)

# Global storage (for demo)
ciphertext_global = None
nonce_global = None
encrypted_key_global = None


# Generate RSA keys
@app.route('/generate_keys')
def generate_keys():
    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open("private.pem", "wb") as f:
        f.write(private_key)

    with open("public.pem", "wb") as f:
        f.write(public_key)

    return "RSA Keys Generated Successfully!"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/encrypt_page')
def encrypt_page():
    return render_template('encrypt.html')


@app.route('/decrypt_page')
def decrypt_page():
    return render_template('decrypt.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    global ciphertext_global, nonce_global, encrypted_key_global

    message = request.form['message']

    # AES encryption
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())

    nonce = cipher_aes.nonce

    # RSA encryption
    public_key = RSA.import_key(open("public.pem").read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)

    # Store globally
    ciphertext_global = ciphertext
    nonce_global = nonce
    encrypted_key_global = encrypted_key

    return render_template('encrypt.html',
                           ciphertext=base64.b64encode(ciphertext).decode(),
                           encrypted_key=base64.b64encode(encrypted_key).decode())


@app.route('/decrypt', methods=['POST'])
def decrypt():
    global ciphertext_global, nonce_global, encrypted_key_global

    try:
        private_key = RSA.import_key(open("private.pem").read())
        cipher_rsa = PKCS1_OAEP.new(private_key)

        aes_key = cipher_rsa.decrypt(encrypted_key_global)

        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce_global)
        decrypted = cipher_aes.decrypt(ciphertext_global)

        return render_template('decrypt.html',
                               message=decrypted.decode())

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)