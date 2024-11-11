import os
import random
import string
from utils.database_manager import get_keys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionUtility:
    def __init__(self, salt=b"",saltbool=False):
        """Initialize the EncryptionUtility with a random salt if none is provided."""
        self.salt_parmter = self.salts if saltbool else salt
        self.salt = self.salt_parmter if isinstance(self.salt_parmter, bytes) else str(self.salt_parmter).encode()
        self.backend = default_backend()
        self.understandable = False
    def salts(self):
        return os.urandom(16)
    def generate_strong_password(self, length=16):
        """Generate a strong random password with the specified length."""
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def derive_key(self, password, iterations=100000):
        """Derive a cryptographic key from the provided password using PBKDF2 and SHA-256."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=iterations,
            backend=self.backend
        )
        return kdf.derive(str(password).encode())

    def encrypt_aes(self, data, key):
        """Encrypt data using AES encryption with the provided key and a random IV."""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        return iv + encryptor.update(data) + encryptor.finalize()

    def decrypt_aes(self, encrypted_data, key):
        """Decrypt AES-encrypted data using the provided key, extracting the IV from the data."""
        iv = encrypted_data[:16]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_data[16:]) + decryptor.finalize()

    def encrypt_chacha20(self, key, data):
        """Encrypt data using ChaCha20 encryption with the provided key and a random nonce."""
        nonce = os.urandom(16) 
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return nonce + ciphertext 

    def decrypt_chacha20(self, key, data):
        """Decrypt ChaCha20-encrypted data using the provided key, extracting the nonce from the data."""
        nonce = data[:16]  # Extract nonce
        ciphertext = data[16:]  # Extract ciphertext
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    def save_key(self, key, filename):
        """Save the provided key to a file specified by filename."""
        with open(filename, 'wb') as f:
            f.write(key)

    def load_key(self, filename):
        """Load a key from a file specified by filename."""
        with open(filename, 'rb') as f:
            return f.read()

    def encrypt_file(self, file_path, password1, password2=None, use_double=False, use_aes=True):
        """Encrypt the specified file using the provided password(s) and either AES or ChaCha20."""
        with open(file_path, 'rb') as file:
            data = file.read()

        key1 = self.derive_key(password1)
        try:
            fileex = str(os.path.basename(file_path)).split(".")[-1].encode()
        except:
            fileex = "bin".encode()
        keyguard_data = b"|keyguard|" + fileex
        if use_double and password2:
            key2 = self.derive_key(password2)
            if use_aes:
                encrypted_data = self.encrypt_aes(data + keyguard_data, key1)
                encrypted_data = self.encrypt_aes(encrypted_data, key2)
            else:
                encrypted_data = self.encrypt_chacha20(key1, data + keyguard_data)
                encrypted_data = self.encrypt_chacha20(key2, encrypted_data)
        else:
            if use_aes:
                encrypted_data = self.encrypt_aes(data + keyguard_data, key1)
            else:
                encrypted_data = self.encrypt_chacha20(key1, data + keyguard_data)

        with open(str(file_path).split(".")[0] + ".enc", 'wb') as file:
            file.write(encrypted_data)

        return f"File ex {os.path.basename(file_path)} encrypted successfully using {'AES' if use_aes else 'ChaCha20'}."

    def decrypt_file(self, file_path, password1, password2=None, use_double=False, use_aes=True):
        """Decrypt the specified encrypted file using the provided password(s) and either AES or ChaCha20."""
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        key1 = self.derive_key(password1)

        if use_double and password2:
            key2 = self.derive_key(password2)
            if use_aes:
                decrypted_data = self.decrypt_aes(encrypted_data, key2)
                decrypted_data = self.decrypt_aes(decrypted_data, key1)
            else:
                decrypted_data = self.decrypt_chacha20(key2, encrypted_data)
                decrypted_data = self.decrypt_chacha20(key1, decrypted_data)
        else:
            if use_aes:
                decrypted_data = self.decrypt_aes(encrypted_data, key1)
            else:
                decrypted_data = self.decrypt_chacha20(key1, encrypted_data)

        understood = self.is_data_understandable(decrypted_data)

        if understood:
            if b"|keyguard|" in decrypted_data:
                extension = decrypted_data.split(b"|keyguard|")[-1].decode('utf-8')
                with open(file_path[:-3] + extension, 'wb') as file:
                    file.write(decrypted_data.split(b"|keyguard|")[0])
                return f"File decrypted and saved with original extension: {extension}"

        else:
            if b"|keyguard|" in decrypted_data:
                extension = decrypted_data.split(b"|keyguard|")[-1].decode('utf-8')
                with open(file_path[:-3] + extension, 'wb') as file:
                    file.write(decrypted_data.split(b"|keyguard|")[0])
                return f"File decrypted but data was not understandable, saved with original extension: {extension}"

    def is_data_understandable(self, data):
        """Check if the decrypted data can be decoded as UTF-8 text."""
        try:
            data.decode('utf-8')
            return True
        except:
            return False
