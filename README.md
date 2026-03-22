<div align="center">

# 🔐 ShadowSend PRO

### Secure Image-Based Messaging using Cryptography & Steganography

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![AES Encryption](https://img.shields.io/badge/AES--128-Encryption-6342FF?style=for-the-badge&logo=letsencrypt&logoColor=white)
![LSB Steganography](https://img.shields.io/badge/LSB-Steganography-0E7490?style=for-the-badge)

**Hide encrypted messages inside images. No one will know they exist.**

[🚀 Live Demo](https://shadow-send.streamlit.app/) · [🐛 Report Bug](https://github.com/your-username/shadow-send/issues) · [✨ Request Feature](https://github.com/your-username/shadow-send/issues)

</div>

---

## 📖 Overview

**ShadowSend PRO** is a web-based secure communication application that allows users to hide secret messages inside images. It combines **AES encryption** and **LSB steganography** to ensure that messages remain both **encrypted** and **invisible**.

> 🔒 **Dual-Layer Protection:** Even if an attacker finds the image, they can't read the message without the correct password. Steganography hides *the existence* of the message. Encryption hides *the content*.

Built with **Streamlit** — runs in any web browser, no installation required for end users.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 AES Encryption | Message encrypted via Fernet (AES-128-CBC) before embedding |
| 🔑 SHA-256 Key Derivation | Password converted to a secure 32-byte key using SHA-256 |
| 🖼️ LSB Steganography | Encrypted data hidden in pixel least-significant bits |
| 📤 Encode Mode | Upload image → type message → set password → download secret image |
| 📥 Decode Mode | Upload secret image → enter password → reveal message |
| 🎨 Modern UI | Clean Streamlit interface with password strength indicator |
| 🖼️ Image Preview | Side-by-side original vs. encoded image comparison |
| 📥 Download | One-click download of the stego image |

---

## 🧠 How It Works
```
User Input  ──►  SHA-256 Key  ──►  AES Encrypt  ──►  LSB Embed  ──►  Secret Image
  message          from             message            in pixels        (PNG output)
  password         password         → cipher bytes
```

1. User enters a **secret message** and **password** in the web interface
2. Password is hashed with **SHA-256** to produce a 32-byte AES-compatible key
3. Message is **encrypted** using Fernet (AES-128 symmetric encryption)
4. Encrypted bytes are **embedded** into image pixels by flipping each pixel's least-significant bit — a change invisible to the human eye
5. Receiver uploads the image and enters the password
6. App **extracts** the LSB data, reconstructs the cipher bytes, and **decrypts** the original message

---

## 🛠️ Tech Stack

| Component | Purpose |
|---|---|
| **Python 3.x** | Core programming language |
| **Streamlit** | Web application framework |
| **cryptography** | Fernet / AES-128 encryption + SHA-256 key derivation |
| **NumPy** | Pixel array manipulation for LSB operations |
| **Pillow (PIL)** | Image loading, conversion, and saving |

---

## 📂 Project Structure
```
shadow-send/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation & Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Magg-peace/shadow-send.git
cd shadow-send
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

**4. Open in browser**
```
http://localhost:8501
```

### `requirements.txt`
```
streamlit
cryptography
numpy
Pillow
```

---

## 🌐 Live Application

👉 **[https://shadow-send.streamlit.app/](https://shadow-send.streamlit.app/)**

---

## 🎯 Use Cases

- 🔒 **Secure communication** — Send private messages hidden inside public images
- 📁 **Confidential data sharing** — Embed sensitive info in innocuous cover images
- 🏷️ **Digital watermarking** — Invisibly mark images with ownership or metadata
- 🎓 **Academic / learning** — Practical demo of cryptography + steganography concepts
- 🧩 **CTF / Security challenges** — Reference implementation for steganography puzzles

---

## 🚀 Future Enhancements

- [ ] User authentication system
- [ ] Mobile responsive UI
- [ ] Chat-based secure messaging interface
- [ ] Multi-image support (distribute message across several images)
- [ ] AI-based steganography detection module
- [ ] Video steganography support

---

## 👩‍💻 Author

**Meghana S**

This project demonstrates how **cryptography** and **steganography** can be combined to build a secure communication system that is both practical and user-friendly — applying theoretical security concepts in an accessible web application.

---

## ⭐ Support

If you find this project useful:

- ⭐ **Star** this repository
- 🍴 **Fork** it and build your own version
- 📢 **Share** it with others learning cybersecurity
- 🐛 **Open an issue** to report bugs or suggest features

---

<div align="center">

Made with ❤️ by Meghana S · Built with Python & Streamlit

</div>