
# KeyGuard Documentation

## Overview
**KeyGuard** is a security-focused application designed to help users manage, encrypt, and securely store sensitive information. It leverages strong encryption algorithms to ensure data confidentiality and integrity.

### Key Features
- **🔑 Generate Key**: Automatically generate a secure encryption key.
- **🛠️ Manual Key**: Manually enter and edit encryption keys.
- **📂 Split Key**: Split your encryption key into multiple parts for added security.
- **🔗 Recover Key**: Reassemble your encryption key from stored parts.
- **🔒 Encrypt Files**: Use encryption keys to secure sensitive files.
- **🔓 Decrypt Files**: Decrypt files by providing the correct encryption key.

---

## Getting Started

### Prerequisites
- Python 3.10 or later
- PyQt5 library
- Additional cryptographic libraries (e.g., `pycryptodome`)

required libraries using:
```bash
ChaCha20==1.1.1 Cython==3.0.11 PyQt5==5.15.11 PyQt5-Qt5==5.15.2 PyQt5_sip==12.15.0 cryptography==43.0.3 fpdf==1.7.2 six==1.16.0 utilitybelt==0.2.6 db-sqlite3==0.0.1
```

### Installation

#### Automatic Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Skymi0/KeyGuard.git
   cd KeyGuard
   ```

2. **Run the application:**
   ```bash
   python AUTORUN.py
   ```

#### Manual Installation
1. **Set up a virtual environment**:
   Using a virtual environment helps to avoid conflicts between project dependencies.

   - **Create a virtual environment**:
     ```bash
     python -m venv venvKeyGuard
     ```

   - **Activate the virtual environment**:
     - On **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - On **macOS/Linux**:
       ```bash
       source venv/bin/activate
       ```

2. **Install project dependencies**:
   - On **Windows**:
     ```bash
     venv\Scripts\python -m pip install -r requirements.txt
     ```
   - On **macOS/Linux**:
     ```bash
     venv/bin/python3 -m pip install -r requirements.txt
     ```

3. **Run the application**:
   ```bash
   python  KeyGuard/main.py
   ```

---

## How to Use KeyGuard

### Main Functionalities

#### 1. Generate Key
- Select **Generate Key** from the main menu.
- A secure encryption key will be generated using AES-256 or ChaCha20, and stored securely.

#### 2. Manual Key
- Choose **Manual Key** from the menu to enter a custom key.
- This feature is especially useful for advanced users who prefer to control their encryption keys.

#### 3. Split Key
- Use **Split Key** to divide your encryption key into multiple shares.
- Store these shares in separate, secure locations (e.g., USB, secure storage) to reduce risk.

#### 4. Recover Key
- Reassemble your encryption key by combining a specific number of shares.
- This ensures you can still recover the key even if one share is lost.

#### 5. Encrypt Files
- Select the files you want to secure, and use an encryption key to protect them.

#### 6. Decrypt Files
- Choose **Decrypt Files** and provide the correct encryption key to unlock and access the files.

---

## FAQ

1. **What encryption algorithms are supported?**
   - **AES-256**: A strong encryption method with a 256-bit key for enhanced security.
   - **ChaCha20**: A fast and secure stream cipher used in modern cryptography.

2. **Is it safe to store encryption keys in the cloud?**
   - This depends on the provider. Always enable two-factor authentication (2FA) and other security measures for added protection.

3. **Can I recover my key if I lose one of the shares?**
   - Yes, as long as you have enough shares to meet the minimum threshold, you can recover the key.

4. **Is there a limit on the number of keys I can generate?**
   - No, you can generate and manage an unlimited number of keys within KeyGuard.

---

## Security Considerations

- **Key Management**: Store your key shares securely. Unauthorized access to your key or its shares can lead to compromise.
- **Two-Factor Authentication**: When storing data in the cloud, enable two-factor authentication (2FA) for added security.
- **Encryption Algorithms**: KeyGuard uses industry-standard encryption algorithms like AES-256 and ChaCha20 to ensure strong data protection.

