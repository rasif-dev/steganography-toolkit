# 🔐 Multi-Modal Steganography & Encryption Toolkit

**AES-128-CBC + LSB Steganography for Text, Images, and Audio**

A Python toolkit that encrypts secret messages using Fernet (AES-128-CBC + HMAC) and hides them inside innocent-looking carriers: text (zero-width Unicode encoding), images (LSB steganography), and audio (LSB steganography on WAV samples).

> Built with a **defensive security mindset**: bounds-checking, cryptographic integrity, and graceful failure on invalid inputs.

---

## 🛡️ Defensive Security Features

| Feature | Implementation |
| :--- | :--- |
| **Bounds-Checking** | Rejects payloads exceeding carrier capacity to prevent memory corruption |
| **Cryptographic Integrity** | Fernet (AES-128-CBC + HMAC) ensures data cannot be tampered with |
| **Graceful Failure** | Invalid keys, missing files, or corrupted data return user-friendly errors |
| **Input Validation** | Malformed paths and unsupported formats are caught safely |
| **Multi-Format Audio** | Handles 8, 16, 24, and 32-bit WAV samples with native type conversion |

---

## 🧩 Features

| Carrier Type | Technique | Encryption |
| :--- | :--- | :--- |
| **Text** | Zero-Width Unicode (`\u200B`, `\u200C`) | Fernet (AES-128-CBC) |
| **Images (PNG)** | LSB Steganography | Fernet (AES-128-CBC) |
| **Audio (WAV)** | LSB Steganography | Fernet (AES-128-CBC) |

---

## 📦 Installation

```bash
git clone https://github.com/rasif-dev/steganography-toolkit.git
cd steganography-toolkit
pip install -r requirements.txt
python main.py
```

---

## 🚀 Usage

### Hide a secret in an image
```bash
# Select option 2
# Enter your secret message, provide a cover image, and save the output
# A unique encryption key is generated — save this to decrypt later
```

### Extract a secret from an image
```bash
# Select option 5
# Provide the stego image and the correct decryption key
```

### Example
```
==================================================
 Secure Covert Channel Toolkit
 AES-128-CBC + LSB Steganography
==================================================

--- Main Menu ---
 1. Hide secret in TEXT (zero-width encoding)
 2. Hide secret in IMAGE (LSB steganography)
 3. Hide secret in AUDIO (LSB steganography)
 4. Extract secret from TEXT
 5. Extract secret from IMAGE
 6. Extract secret from AUDIO
 7. Exit
```

---

## 📂 Project Structure

```
steganography-toolkit/
├── main.py              # Main entry point
├── zeroWidthChara.py    # Text steganography (zero-width characters)
├── imageSteg.py         # Image steganography (LSB in RGB pixels)
├── audioSteg.py         # Audio steganography (LSB in WAV samples)
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── Project Report.pdf   # Comprehensive report (history, design, threat model)
```

---

## 🧠 Threat Model & Limitations

This toolkit is designed for **educational and portfolio purposes**. While encryption provides strong confidentiality, LSB steganography is vulnerable to:

- **Statistical steganalysis** (detection via pixel/sample distribution anomalies)
- **Zero-width character stripping** (platforms like Gmail/Slack remove invisible chars)
- **Lossy compression** (JPEG/MP3 destroy LSB data — forced to PNG/WAV)

**Mitigations implemented:**
- Encryption ensures data remains unreadable even if detected
- Bounds-checking prevents capacity overflows
- Force-saves to lossless formats (PNG, WAV) to preserve integrity

For a detailed analysis, see `Project_Report.pdf`.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **cryptography** (Fernet symmetric encryption)
- **Pillow** (Image processing)
- **NumPy** (Audio/Image array manipulation)
- **pyfiglet** (CLI banner styling)

---

## 👤 Author

**Raheel Asif**  
Computer Science @ UNSW Sydney (WAM: 76.4, Distinction)  
[LinkedIn](https://linkedin.com/in/rasif-dev) | [GitHub](https://github.com/rasif-dev)

---

## 📄 License

Educational and portfolio use only.