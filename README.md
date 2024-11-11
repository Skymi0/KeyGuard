
# KeyGuard Documentation

## Introduction

**KeyGuard** is a security-focused application designed to help users manage, encrypt, and safely store sensitive information. The application leverages strong encryption algorithms to ensure the confidentiality and integrity of data.

### Key Features:
- 🔑 **Generate Key**: Automatically generate secure encryption keys.
- 🛠️ **Manual Key**: Users can manually input and edit their encryption keys for full control.
- 📂 **Split Key**: Split your encryption key into multiple shares for enhanced security.
- 🔗 **Recover Key**: Reassemble your encryption key from the stored shares.
- 🔒 **Encrypt Files**: Use encryption keys to secure sensitive files.
- 🔓 **Decrypt Files**: Decrypt encrypted files by providing the correct key.

## Getting Started

### Prerequisites
- Python 3.10 =<
- PyQt5 library
- Additional libraries for cryptographic functions (e.g., `pycryptodome`)

You can install the required libraries using `pip`:
```bash
pip install ChaCha20==1.1.1 Cython==3.0.11 PyQt5==5.15.11 PyQt5-Qt5==5.15.2 PyQt5_sip==12.15.0 cryptography==43.0.3 fpdf==1.7.2 six==1.16.0 utilitybelt==0.2.6 db-sqlite3==0.0.1


### Installation

### AUTO Installation
```bash
   git clone https://github.com/Skymi0/KeyGuard.git
   cd KeyGuard
   python AUTORUN.py
```
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Skymi0/KeyGuard.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd KeyGuard
   python AUTORUN.py
   ```

3. **Set up a virtual environment for security:**

   It's recommended to use a virtual environment to isolate the dependencies for the project, ensuring no conflicts with other projects or system libraries.

   - Create a virtual environment:
     ```bash
     python -m venv venvKeyGuard
     ```

   - Activate the virtual environment:
     - On **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - On **macOS/Linux**:
       ```bash
       source venv/bin/activate
       ```

4. **Install the project dependencies:**
   - On **Windows**:
   ```bash
   venv\Scripts\python -m pip install -r requirements.txt
   ```
   - On **macOS/Linux**:
   ```bash
   venv/bin/python3 -m pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python AUTORUN.py
   ``` 


## How to Use KeyGuard

### Main Functionalities

#### 1. Generate Key
- Navigate to the 'Generate Key' option from the main menu.
- A secure encryption key will be generated using AES-256, or ChaCha20.
- The key is saved securely for later use in encryption and decryption tasks.

#### 2. Manual Key
- Select 'Manual Key' from the menu to manually enter a key.
- This feature is particularly useful for advanced users who want to control their encryption keys.

#### 3. Split Key
- Use the 'Split Key' feature to divide your encryption key into multiple parts (shares).
- Store these shares in separate locations (e.g., USB,  storage) to minimize risk.

#### 4. Recover Key
- Reassemble your encryption key by combining a specific number of shares.
- This ensures that even if one share is lost, you can still recover your key using the remaining shares.

#### 5. Encrypt Files
- Select the files you wish to secure and use an encryption key to encrypt them.
- Supported encryption algorithms: AES-256, and ChaCha20.

#### 6. Decrypt Files
- Choose 'Decrypt Files' and provide the correct encryption key to unlock and access your encrypted files.
- Supported encryption algorithms: AES-256, and ChaCha20.

### Frequently Asked Questions (FAQ)

#### 1. **What encryption algorithms are supported?**
- **AES-256**: A stronger encryption method with a 256-bit key for enhanced security.
- **ChaCha20**: A fast and secure stream cipher used in modern cryptography.

#### 2. **Is it safe to store encryption keys in the ?**
- This depends on your  provider. Always enable two-factor authentication (2FA) and other security measures when storing sensitive keys in the .

#### 3. **Can I recover my key if I lose a share?**
- Yes, as long as you have enough shares to meet the minimum threshold, you can recover your key.

#### 4. **Is there a limit to how many keys I can generate?**
- No, there is no limit to the number of keys you can generate and manage within KeyGuard.

## Security Considerations

- **Key Management**: Be sure to store your key shares securely. Unauthorized access to your key or its shares can lead to a compromise.
- **Two-Factor Authentication**: When storing data in the , enable two-factor authentication (2FA) for an extra layer of protection.
- **Encryption Algorithms**: KeyGuard supports industry-standard encryption algorithms like AES-256, and ChaCha20 to ensure strong data protection.
