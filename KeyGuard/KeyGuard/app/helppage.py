from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog, QScrollArea, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(200, 200, 600, 500)
        self.setStyleSheet("background-color: #282a36;")

        layout = QVBoxLayout(self)

        # Scroll area to handle long help text
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Title for the help window
        title_label = QLabel("<h2 style='color: #2980B9;'>How to Use KeyGuard</h2>")
        container_layout.addWidget(title_label)

        # Detailed instructions using HTML
        help_text = """
        <p style='color: #f8f8f2;'>Welcome to KeyGuard's Help section! Here's how to use the key features:</p>
        <ol style='color: #f8f8f2;'>
            <li><b>Generate Key</b>
                <ul>
                    <li>Select 'Generate Key' from the main menu.</li>
                    <li>A secure encryption key will be created and saved for use in encryption tasks.</li>
                </ul>
            </li>
            <li><b>Manual Key</b>
                <ul>
                    <li>Choose 'Manual Key' if you'd like to enter or edit a key manually.</li>
                    <li>This feature is ideal for more advanced users who prefer greater control over the keys.</li>
                </ul>
            </li>
            <li><b>Split Key</b>
                <ul>
                    <li>Use the 'Split Key' option to divide a secret key into multiple shares.</li>
                    <li>Each share can be stored in different locations (USB, etc.) for added security.</li>
                </ul>
            </li>
            <li><b>Recover Key</b>
                <ul>
                    <li>Select 'Recover Key' to reassemble the original secret from the shares.</li>
                    <li>You’ll need a certain number of shares to successfully recover the key.</li>
                </ul>
            </li>
            <li><b>Encrypt Files</b>
                <ul>
                    <li>After generating or entering a key, you can encrypt sensitive files to protect them.</li>
                    <li>Choose the files you wish to secure, and the application will handle the encryption process.</li>
                </ul>
            </li>
            <li><b>Decrypt Files</b>
                <ul>
                    <li>Select 'Decrypt Files' and provide the appropriate key to decrypt previously encrypted files.</li>
                    <li>Ensure that you have the correct key for successful decryption.</li>
                </ul>
            </li>
        </ol>
        <p style='color: #f8f8f2;'>For additional support or troubleshooting, feel free to contact us!</p>
        <p style='color: #f8f8f2;'><b>Frequently Asked Questions (FAQ)</b></p>
        <ul style='color: #f8f8f2;'>
            <li><b>What is KeyGuard?</b> <br> A: KeyGuard is a secure key management and file encryption software.</li>
            <li><b>How can I recover a lost key?</b> <br> A: If you lose your key, you can use the Split Key feature to reconstruct it if you have the necessary shares.</li>
            <li><b>Can I share keys with others?</b> <br> A: Yes, you can share key parts securely, but be cautious about sharing the full key to maintain security.</li>
            <li><b>What encryption standards does KeyGuard use?</b> <br> A: KeyGuard supports various encryption standards, including:</li>
            <ul>
                <li><b>AES-128:</b> A symmetric encryption algorithm that uses a 128-bit key for secure data encryption.</li>
                <li><b>AES-256:</b> A stronger version of AES that uses a 256-bit key, providing higher security for sensitive data.</li>
                <li><b>ChaCha20:</b> A stream cipher known for its speed and security, often used in modern applications for secure encryption.</li>
            </ul>
            <li><b>Is there a limit to how many keys I can generate?</b> <br> A: No, you can generate as many keys as needed for your projects.</li>
        </ul>
        """

        help_label = QLabel(help_text)
        help_label.setFont(QFont("Arial", 12))
        help_label.setStyleSheet("color: #f8f8f2;")
        help_label.setWordWrap(True)

        container_layout.addWidget(help_label)

        scroll.setWidget(container)

        self.setLayout(layout)
