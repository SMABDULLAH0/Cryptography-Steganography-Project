from flask import Flask, render_template, request, flash, redirect, url_for
import os
import base64
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# AES Encryption Function
def encrypt_AES(key, plaintext, iv=None):
    if iv is None:
        iv = os.urandom(16)  # Initialization vector (IV) for better security
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext


# AES Decryption Function
def decrypt_AES(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()


def embed_text_in_image(image_path, data, output_image_path):
    img = Image.open(image_path)
    binary_data = ''.join(format(byte, '08b') for byte in data)
    
    length_binary = format(len(binary_data), '032b')
    binary_data = length_binary + binary_data
    
    pixels = list(img.getdata())
    new_pixels = []

    binary_index = 0
    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(3):  # Adjust RGB channels
            if binary_index < len(binary_data):
                new_pixel[i] = (new_pixel[i] & ~1) | int(binary_data[binary_index])
                binary_index += 1
        new_pixels.append(tuple(new_pixel))

    img.putdata(new_pixels)
    img.save(output_image_path)


def extract_text_from_image(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_data = ""

    # Extract the length of the binary data
    for pixel in pixels[:11]:  # First 11 pixels are enough for 32 bits
        for i in range(3):  # RGB channels
            binary_data += str(pixel[i] & 1)
            if len(binary_data) >= 32:
                break
        if len(binary_data) >= 32:
            break

    length_binary = binary_data[:32]
    data_length = int(length_binary, 2)
    
    # Extract the rest of the data
    binary_data = ""
    for pixel in pixels:
        for i in range(3):  # RGB channels
            binary_data += str(pixel[i] & 1)
            if len(binary_data) >= 32 + data_length:
                break
        if len(binary_data) >= 32 + data_length:
            break

    binary_data = binary_data[32:]  # Remove the length info
    byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return bytes([int(byte, 2) for byte in byte_data])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt_embed', methods=['GET', 'POST'])
def encrypt_embed():
    if request.method == 'POST':
        plaintext = request.form['message']
        key = request.form['key']
        if len(key) != 32:
            flash("Error: The encryption key must be exactly 32 characters long!", "error")
            return redirect(url_for('encrypt_embed'))

        image = request.files['image']
        output_filename = request.form['output_filename'] or 'output_image.png'
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        image.save(image_path)

        iv, ciphertext = encrypt_AES(key.encode(), plaintext)
        encrypted_message = base64.b64encode(iv + ciphertext)

        try:
            embed_text_in_image(image_path, encrypted_message, output_path)
            flash(f"Message embedded successfully! Output saved at: {output_path}", "success")
        except Exception as e:
            flash(f"Error embedding message: {e}", "error")
        
    return render_template('encrypt_embed.html')


@app.route('/decrypt_extract', methods=['GET', 'POST'])
def decrypt_extract():
    decrypted_message = None  # Initialize to None for conditional display
    if request.method == 'POST':
        key = request.form['key']
        if len(key) != 32:
            flash("Error: The decryption key must be exactly 32 characters long!", "error")
            return redirect(url_for('decrypt_extract'))

        stego_image = request.files['stego_image']
        stego_path = os.path.join(UPLOAD_FOLDER, stego_image.filename)
        stego_image.save(stego_path)

        try:
            # Extract and decrypt the message
            extracted_data = extract_text_from_image(stego_path)
            missing_padding = len(extracted_data) % 4
            if missing_padding:
                extracted_data += b'=' * (4 - missing_padding)
            extracted_message = base64.b64decode(extracted_data)

            iv_extracted = extracted_message[:16]
            ciphertext_extracted = extracted_message[16:]
            decrypted_message = decrypt_AES(key.encode(), iv_extracted, ciphertext_extracted)

            flash("Decryption successful!", "success")
        except Exception as e:
            flash(f"Error decrypting the message: {e}", "error")

    return render_template('decrypt_extract.html', decrypted_message=decrypted_message)



if __name__ == '__main__':
    app.run(debug=True)
