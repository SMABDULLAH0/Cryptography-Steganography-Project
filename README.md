<<<<<<< HEAD

# Enhanced Privacy in Data Transmission Using Steganography and Cryptography

This project integrates cryptography and steganography techniques to securely transmit sensitive information. Users can encrypt messages using a strong encryption algorithm and embed them within images for secure transmission. The system also supports decrypting and extracting messages from images using the decryption key.

The project features a Flask-based web interface, providing an intuitive and interactive way for users to perform encryption, embedding, decryption, and message extraction tasks.


## Features

- **Message Encryption:** Securely encrypts messages using a user-provided 32-character key.
- **Image Steganography:** Embeds the encrypted message into an image, creating a steganographic output image.
- **Message Extraction:** Decrypts and extracts hidden messages from steganographic images.
- **User-friendly Interface:** Web-based interface for seamless interaction.
- **Customizable Output:** Allows users to specify custom filenames for the output images.


## Technologies Used
- **Python:** Core language for backend logic.
- **Flask:** Framework for building the web interface.
- **Pillow:** Python Imaging Library for image manipulation.
- **Cryptography Library:** Implements encryption and decryption.
- **HTML/CSS/JavaScript:** For designing and enhancing the user interface.
- **Particles.js:** Adds dynamic background effects for an engaging user experience.
## Installation Instruction

Follow these steps to set up and run the project locally:

### Prerequisites:
- Python 3.x installed on your system.
- A virtual environment (optional but recommended).

### Steps:

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <project_directory>
## 2. Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```


## 3. Install Dependencies
   ```bash 
   pip install -r requirements.txt
```
## 4. Run The Flask Application
```bash 
pyhon app.py
```
## Access the Application: Open your web browser and navigate to:
```bash 
http://127.0.0.1:5000
```
## Usage Structure:
**1. Encrypt and Embed Messages:**
- Navigate to the Encrypt page.
- Enter the message you wish to encrypt.
- Provide a 32-character encryption key.
- Select the image where the message will be embedded.
- Specify a custom output filename (optional).
- Click Encrypt and Embed to generate the output image.
**2. Decrypt and Extract Messages:**
- Navigate to the Decrypt page.
- Upload the image containing the hidden message.
- Enter the correct decryption key.
- Click Decrypt and Extract to reveal the hidden message.
## Project Structure:
- project_directory/
- │
- ├── app.py                 # Flask application logic
- ├── static/                # Static assets (CSS, JavaScript)
- │   ├── styles.css         # Custom styles
- │   └── particles.js       # Particle.js script for dynamic background
- ├── templates/             # HTML templates
- │   ├── index.html         # Home page
- │   ├── encrypt.html       # Encryption page
- │   ├── decrypt.html       # Decryption page
- ├── utils/                 # Utility functions
- │   ├── crypto.py          # Encryption and decryption logic
- │   └── stego.py           # Image processing logic
- ├── requirements.txt       # Python dependencies
- └── README.md              # Project documentation

## Contributors:

- SM Abdullah (2iI-1732)
- Mohid Munir (21I-1719)
- Moiz Sajjad (21I-2691)
- Abdullah Iftikhar (21I-1687)


## Acknowledgements:
- The Flask Framework for simplifying web development.
- The Cryptography and Pillow libraries for secure encryption and image processing.
- Particles.js for enhancing user interface design with dynamic visuals.

 


## Notes

This README covers every aspect of your project, ensuring anyone can understand, install, and use it. Let me know if there’s anything you’d like to adjust or add!


=======
# Cryptography-Steganography-Project
This project combines cryptographic encryption and steganographic embedding techniques to securely transmit sensitive information. 
>>>>>>> dc54495331de7232dfa85b75b054e5c445ef2b4a
