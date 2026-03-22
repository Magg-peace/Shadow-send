# 🔐 ShadowSend PRO

### Secure Image-Based Messaging using Cryptography & Steganography

---

## 🚀 Overview

**ShadowSend PRO** is a web-based secure communication application that allows users to hide secret messages inside images.  
It combines **AES encryption** and **LSB steganography** to ensure that messages remain both **encrypted and invisible**.

The application is built using **Streamlit**, providing a simple, interactive, and user-friendly interface accessible via any web browser.

---

## ✨ Features

- 🔐 AES Encryption using Fernet
- 🔑 SHA-256 based password key generation
- 🖼️ Image Steganography using LSB (Least Significant Bit)
- 📤 Encode: Hide secret messages inside images
- 📥 Decode: Extract hidden messages using password
- 🎨 Clean and modern Streamlit UI
- 🔎 Password strength indicator
- 🖼️ Image preview (Original vs Encoded)
- 📥 Download encoded image

---

## 🧠 How It Works

1. User enters a secret message and password  
2. Password is converted into a secure key using SHA-256  
3. Message is encrypted using AES (Fernet encryption)  
4. Encrypted message is embedded into image pixels using LSB technique  
5. Receiver uploads the image and enters the password  
6. Hidden message is extracted and decrypted  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Cryptography (Fernet, SHA-256)  
- NumPy  
- Pillow  

---

## 📂 Project Structure

shadow-send/
│── app.py  
│── requirements.txt  
│── README.md  

---

## ⚙️ Installation & Run Locally

```bash
git clone https://github.com/Magg-peace/shadow-send.git
cd shadow-send
pip install -r requirements.txt
streamlit run app.py

🌐 Live Application

👉 https://shadow-send.streamlit.app/

🎯 Use Cases
Secure communication
Confidential information sharing
Digital watermarking
Learning cryptography & steganography concepts

🚀 Future Enhancements
User authentication system
Mobile responsive UI
Chat-based secure messaging
Multi-image support
AI-based steganography detection
👩‍💻 Author

Meghana S

🎓 Project Description

This project demonstrates how cryptography and steganography can be combined to build a secure communication system that is both practical and user-friendly.

⭐ Support

If you like this project:

⭐ Star this repository
🍴 Fork it
📢 Share it
