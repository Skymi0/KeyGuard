from datetime import datetime
import json
from PyQt5.QtWidgets import QPushButton,QComboBox,QVBoxLayout, QLabel, QLineEdit, QTextEdit, QFileDialog, QMessageBox, QDialog, QLabel,QCheckBox
from utils import create_database, get_keys, update_key
class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.saved = False
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 400)

        try:
            userinfo = get_keys()[0]
        except:
            userinfo = None
        if userinfo is None:
            self.reset_to_default()
            self.save_settings() 
        else:
            
            self.encryption_type_combo = QComboBox()
            self.encryption_type_combo.addItems(["AES", "ChaCha20"]) 
            self.security_level_combo = QComboBox()
            self.security_level_combo.addItems(["Normal", "Hard"])
            self.share_threshold_input = QLineEdit(str(userinfo.get("share_threshold", "3")))
            self.number_of_shares_input = QLineEdit(str(userinfo.get("num_shares", "5")))
            self.salt_key_checkbox = QCheckBox()
            self.salt_key_checkbox.setChecked(bool(userinfo["salt"]))
            self.nickname_input = QLineEdit(userinfo.get("nickname", "keyguard"))
            self.directory_input = QLineEdit(userinfo.get("directory", "room"))
            self.notes_input = QTextEdit(userinfo.get("notes", "I left the USB with my brother..."))

            current_sec_method = userinfo.get("security_level", "Normal")
            index_sec = self.security_level_combo.findText(current_sec_method)
            if index_sec != -1:
                self.security_level_combo.setCurrentIndex(index_sec)

            current_enc_method = userinfo.get("encryption_type", "AES")
            index_enc = self.encryption_type_combo.findText(current_enc_method)
            if index_enc != -1:
                self.encryption_type_combo.setCurrentIndex(index_enc)
            
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Share Threshold:"))
        layout.addWidget(self.share_threshold_input)
        layout.addWidget(QLabel("<small style='color: gray;'>Minimum number of shares required to reconstruct the secret.</small>"))

        layout.addWidget(QLabel("Number of Shares:"))
        layout.addWidget(self.number_of_shares_input)
        layout.addWidget(QLabel("<small style='color: gray;'>Total number of shares to be created.</small>"))

        layout.addWidget(QLabel("Nickname:"))
        layout.addWidget(self.nickname_input)
        layout.addWidget(QLabel("<small style='color: gray;'>Your preferred nickname.</small>"))

        layout.addWidget(QLabel("Directory:"))
        layout.addWidget(self.directory_input)
        layout.addWidget(QLabel("<small style='color: gray;'>Directory where files will be saved.</small>"))

        layout.addWidget(QLabel("Security Level"))
        layout.addWidget(self.security_level_combo)
        layout.addWidget(QLabel("<small style='color: gray;'>Choose your desired level of security.</small>"))

        layout.addWidget(QLabel("Salt Key"))
        layout.addWidget(self.salt_key_checkbox)
        layout.addWidget(QLabel("<small style='color: gray;'>For more security if you want.</small>"))

        layout.addWidget(QLabel("Encryption Type"))
        layout.addWidget(self.encryption_type_combo)
        layout.addWidget(QLabel("<small style='color: gray;'>Choose your preferred encryption type.</small>"))

        layout.addWidget(QLabel("Notes:"))
        layout.addWidget(self.notes_input)
        layout.addWidget(QLabel("<small style='color: gray;'>Any additional notes or reminders.</small>"))

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_button)

        import_button = QPushButton("Import Settings")
        import_button.clicked.connect(self.import_settings)
        layout.addWidget(import_button)

        export_button = QPushButton("Export Settings")
        export_button.clicked.connect(self.export_settings)
        layout.addWidget(export_button)

    def save_settings(self):
        """Save settings to settings.json."""
        try:
            settings = {
                "share_threshold": self.share_threshold_input.text(),
                "num_shares": self.number_of_shares_input.text(),
                "nickname": self.nickname_input.text(),
                "directory": self.directory_input.text(),
                "encryption_type": self.encryption_type_combo.currentText(),
                "security_level": self.security_level_combo.currentText(),
                "salt": 1 if self.salt_key_checkbox.isChecked() else 0,
                "notes": self.notes_input.toPlainText(),
            }
            try:
                share_threshold = int(self.share_threshold_input.text())
                number_of_shares = int(self.number_of_shares_input.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Please enter valid integers for share threshold and number of shares.", QMessageBox.Ok)
                return

            if share_threshold < 2 or number_of_shares < 2:
                QMessageBox.warning(self, "Error", "Share threshold and number of shares must be at least 2.", QMessageBox.Ok)
                return

            if share_threshold > number_of_shares:
                QMessageBox.warning(self, "Error", "Share threshold cannot be greater than the number of shares.", QMessageBox.Ok)
                return

            # Ensure the settings are updated correctly.
            update_key(1, **settings)
            QMessageBox.information(self, "Settings Saved", "Your settings have been saved successfully!", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving settings: {str(e)}", QMessageBox.Ok)

    def reset_to_default(self):
        """Reset settings to default values."""
        self.share_threshold_input.setText("3")
        self.number_of_shares_input.setText("5")
        self.directory_input.setText("room")
        self.encryption_type_combo.setCurrentIndex(0)
        self.security_level_combo.setCurrentIndex(0)
        self.salt_key_checkbox.setChecked(True)
        self.notes_input.setPlainText("I left the USB with my brother, which contains the split key.\nI uploaded the key to a keyguard service for my secret key project.")
        QMessageBox.information(self, "Reset", "Settings have been reset to default values.", QMessageBox.Ok)


    def import_settings(self):
        """Import settings from a JSON file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Settings", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    settings = json.load(file)
                    self.share_threshold_input.setText(str(settings.get("share_threshold", "3")))
                    self.number_of_shares_input.setText(str(settings.get("num_shares", "5")))
                    self.nickname_input.setText(settings.get("nickname", "keyguard"))
                    self.directory_input.setText(settings.get("directory", "room"))
                    self.security_level_combo.setCurrentText(settings.get("security_level", "Normal"))
                    self.salt_key_checkbox.setChecked(True)
                    self.notes_input.setPlainText(settings.get("notes", ""))
                    QMessageBox.information(self, "Import Successful", "Settings imported successfully!", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, "❗", f"An error occurred while importing settings: {str(e)}", QMessageBox.Ok)

    def export_settings(self):
        """Export current settings to a JSON file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Settings", "settings.json", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            try:
                settings = {
                    "share_threshold": self.share_threshold_input.text(),
                    "num_shares": self.number_of_shares_input.text(),
                    "nickname": self.nickname_input.text(),
                    "directory": self.directory_input.text(),
                    "security_level": self.security_level_combo.currentText(),
                    "salt": self.salt_key_checkbox.isChecked(),
                    "creation_date": datetime.now().isoformat(),
                    "last_modified": datetime.now().isoformat(),
                    "notes": self.notes_input.toPlainText(),
                }
                update_key(1, **settings)
                QMessageBox.information(self, "Export Successful", "Settings exported successfully!", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, "❗", f"An error occurred while exporting settings: {str(e)}", QMessageBox.Ok)