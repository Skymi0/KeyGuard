from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog, QScrollArea, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class InformationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        self.setGeometry(200, 200, 600, 500)
        self.setStyleSheet("background-color: #282a36;") 

        layout = QVBoxLayout(self)

        # Scroll area to handle long information text
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Title for the information window
        title_label = QLabel("<h2 style='color: #ff79c6;'>Welcome to KeyGuard</h2>")
        container_layout.addWidget(title_label)

        # Detailed information using HTML
        info_text = """
        <p style='color: #f8f8f2;'>KeyGuard is a security-focused application designed to help you safely manage and share sensitive information.</p>
        <p style='color: #f8f8f2;'><b>🌟 Key Features:</b></p>
        <ul style='color: #f8f8f2;'>
            <li>🔑 Generate secure encryption keys.</li>
            <li>🔒 Split your secret keys into multiple parts and store them in different locations (USB, cloud).</li>
            <li>🛠 Recover keys when needed from the stored parts.</li>
        </ul>
        <p style='color: #f8f8f2;'>This tool ensures a high level of data security for your important files. For further details on how to use the features, please visit the Help section.</p>
        <p style='color: #f8f8f2;'><b>Frequently Asked Questions (FAQ)</b></p>
        <ul style='color: #f8f8f2;'>
            <li><b>What is KeyGuard?</b> <br> A: KeyGuard is a secure key management and file encryption software.</li>
            <li><b>Is it safe to store keys in the cloud?</b> <br> A: It depends on your cloud provider. Always use two-factor authentication where possible.</li>
        </ul>
        <p style='color: #f8f8f2;'>For additional support or troubleshooting, feel free to contact us!</p>
        """

        info_label = QLabel(info_text)
        info_label.setFont(QFont("Arial", 12))
        info_label.setStyleSheet("color: #f8f8f2;") 
        info_label.setWordWrap(True)

        container_layout.addWidget(info_label)

        scroll.setWidget(container)

        self.setLayout(layout)
