from PyQt5.QtWidgets import QVBoxLayout, QTextBrowser, QDialog, QScrollArea, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ResultWindow(QDialog):
    def __init__(self, key1_value, key2_value, salt1_value):
        super().__init__()
        self.setWindowTitle("Show Result")
        self.setGeometry(200, 200, 600, 500)
        self.setStyleSheet("background-color: #282a36;")

        layout = QVBoxLayout(self)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        title_label = QLabel("<h2 style='color: #2980B9;'>Results</h2>")
        container_layout.addWidget(title_label)

        result_browser = QTextBrowser()
        result_browser.setOpenExternalLinks(True)
        result_browser.setStyleSheet("""
            background-color: #44475a;
            color: #f8f8f2;
            font-family: Arial, sans-serif;
            padding: 15px;
            border: 1px solid #6272a4;
            border-radius: 5px;
            white-space: pre-wrap; /* Wrap long lines */
        """)
        add = f"""<hr style='border: 1px solid #6272a4;'>
        <p style='font-weight: bold; color: #ff79c6;'>Key-2:</p>
        <ul style='list-style-type: none; padding-left: 0;'>
            {"".join(f"<li style='padding: 5px;'>{value}</li>" for value in key2_value)}
        </ul>"""
        message = f"""
        <h2 style='color: #2980B9;'>🎉 Results Summary 🎉</h2>
        <p style='font-size: 14px;'>Here are the keys and salts generated:</p>
        <hr style='border: 1px solid #6272a4;'>
        <p style='font-weight: bold; color: #50fa7b;'>Key-1:</p>
        <ul style='list-style-type: none; padding-left: 0;'>
            {"".join(f"<li style='padding: 5px;'>{value}</li>" for value in key1_value)}
        </ul>
        {add if key2_value else ""}
        <hr style='border: 1px solid #6272a4;'>
        <p style='font-weight: bold; color: #ffb86c;'>Salt-1:</p>
        <ul style='list-style-type: none; padding-left: 0;'>
            {"".join(f"<li style='padding: 5px;'>{value}</li>" for value in salt1_value)}
        </ul>
        <p style='font-size: 14px; color: #f8f8f2;'>Thank you for using our service!</p>
        """

        result_browser.setHtml(message)

        container_layout.addWidget(result_browser)

        scroll.setWidget(container)

        self.setLayout(layout)
