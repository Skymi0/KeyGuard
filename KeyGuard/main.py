import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,QGraphicsDropShadowEffect,
                             QWidget, QLabel, QHBoxLayout, QMessageBox, QInputDialog,
                             QFileDialog,QDialog
                             )
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer,QPoint
import sys
from app import *
import settings
from utils import get_keys, EncryptionUtility
from decortion import check_user_info_decorator
from keyshard import SecretSharer

class NotificationDialog(QDialog):
    def __init__(self, message, duration=10000, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Notification")
        self.setGeometry(100, 20, 700, 80)
        self.setStyleSheet("background-color: #44475a; color: white; padding: 10px;")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout()
        
        self.icon_label = QLabel()
        layout.addWidget(self.icon_label, alignment=Qt.AlignLeft)
        
        self.label = QLabel(message)
        self.label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.label)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: #ff5555; color: white; border-radius: 5px; padding: 5px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.scroll_text(duration)

    def scroll_text(self, duration):
        if not isinstance(duration, int):
            raise ValueError("Duration must be an integer representing milliseconds.")
            
        self.animation = QPropertyAnimation(self.label, b"pos")
        self.animation.setDuration(duration)  
        self.animation.setStartValue(QPoint(700, 0)) 
        self.animation.setEndValue(QPoint(-self.label.width(), 0))  
        self.animation.setLoopCount(-1) 
        self.animation.start()



        QTimer.singleShot(duration + 1000, self.close)  



class KeyGuard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.SecretSharer = SecretSharer()
        self.setup_ui()
        self.key1 = None
        self.key2 = None
        self.salt = None
        
        try:
            self.user_info = get_keys()[0]
        except:
            get_keys()
            exit(1)
        if settings.RESET_DB:
            get_keys(reset=settings.RESET_DB)[0]
            print("You can turn off Reset DB in settings.py (RESET_DB = False)")
        self.EncryptionUtility = EncryptionUtility(salt=self.salt,saltbool=bool(self.user_info["salt"]))
        self.notification_dialog = NotificationDialog("Welcome to KeyGuard!", duration=10000, parent=self)
        self.update_notification_position()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_notification_position)
        self.timer.start(1) 
        if settings.DEBUG:
            print(f"Debug: key1 = {self.key1}, key2 = {self.key2}, salt = {self.salt}") 


    def create_main_widget(self):
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        welcome_label = QLabel("Welcome to KeyGuard!", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: #50fa7b; font-size: 22px; font-weight: bold;")
        layout.addWidget(welcome_label)

        button_layout = QHBoxLayout()

        dashboard_button = QPushButton("Go to Dashboard", self)
        dashboard_button.setMinimumHeight(50)
        dashboard_button.setStyleSheet("""
            QPushButton {
                background-color: #6272a4;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #44475a;
            }
            QPushButton:pressed {
                background-color: #282a36;
                color: #ff79c6;
            }
        """)
        dashboard_button.clicked.connect(self.show_dashboard)
        button_layout.addWidget(dashboard_button)

        layout.addLayout(button_layout)
        return widget


    def show_notification(self, message):
        self.notification_dialog = NotificationDialog(message, duration=10000, parent=self)
        self.notification_dialog.show()
    def show_main_widget(self):
        self.central_widget.setCurrentWidget(self.main_widget)
    def clear_notification(self):
        self.notification_dialog = NotificationDialog("", duration=10, parent=self)
        self.notification_dialog.close()
    def update_notification_position(self):
        pos = self.mapToGlobal(QPoint(0, 0))
        self.notification_dialog.move(pos.x() + 100, pos.y() + 50)
    def setup_ui(self):
        self.setWindowTitle("KeyGuard")
        self.setGeometry(100, 100, 900, 250)
        self.setStyleSheet("background-color: #282a36;")
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title_label = QLabel("Welcome to KeyGuard", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #ff79c6; font-size: 28px; font-weight: bold;")
        layout.addWidget(title_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.add_button(button_layout, "Key Management", "#50fa7b",self.key_management)
        self.add_button(button_layout, "Key Splitter", "#8be9fd",self.split_or_recover)
        self.add_button(button_layout, "File Encryptor", "#ff5555",self.encrypt_or_decrypt)
        layout.addLayout(button_layout)

        self.add_sidebar_buttons(layout)

        self.animate_buttons()

    def add_button(self, layout, text, color,callback):
        button = QPushButton(text, self)
        button.setMinimumHeight(50)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #282a36;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #44475a;
                color: white;
            }}
            QPushButton:pressed {{
                background-color: #282a36;
                color: #ff79c6;
            }}
        """)
        layout.addWidget(button)
        button.clicked.connect(callback)

    def add_sidebar_buttons(self, layout):
        sidebar_layout = QHBoxLayout()
        sidebar_layout.setSpacing(15)

        self.add_sidebar_button(sidebar_layout, "PasswordHub", "#bd93f9", self.open_Password_window)
        self.add_sidebar_button(sidebar_layout, "⚙️ Settings", "#bd93f9", self.open_settings_window)
        self.add_sidebar_button(sidebar_layout, "📁 Files", "#ffb86c",self.open_files_window)
        self.add_sidebar_button(sidebar_layout, "ℹ️ Information", "#ff79c6",self.open_information_window)
        self.add_sidebar_button(sidebar_layout, "❓ Help", "#ff5555",self.open_help_window)

        layout.addLayout(sidebar_layout)

    def add_sidebar_button(self, layout, text, color,callback):
        button = QPushButton(text, self)
        button.setMinimumHeight(40)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #282a36;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #44475a;
                color: white;
            }}
            QPushButton:pressed {{
                background-color: #282a36;
                color: #ff79c6;
            }}
        """)
        layout.addWidget(button)
        button.clicked.connect(callback)
    def open_files_window(self):
        files_window = FilesWindow()
        files_window.exec_()

    def open_information_window(self):
        information_window = InformationWindow()
        information_window.exec_()

    def open_help_window(self):
        help_window = HelpWindow()
        help_window.exec_()

    def open_settings_window(self):
        settings_window = SettingsWindow()
        settings_window.exec_()
        if settings_window.saved:
            self.show_notification("Good job all is great")
    def open_Password_window(self):
        Password_window = PasswordManager()
        Password_window.exec_()
        if Password_window.saved:
            self.show_notification("! great")
            self.key1 = Password_window.key1
            self.key2 = Password_window.key2
            self.salt = str(Password_window.salt).encode()
            return Password_window.key1, Password_window.key2, Password_window.salt
    def key_management(self, *args):
        options = ["🔑 Generate Key", "✏️ Manual Key"]
        try:
            choice, ok = QInputDialog.getItem(self, "🔒 Key Management", "Please select an option:", options, 0, False)
            if ok:
                getattr(self, f"{choice.split(' ')[1].lower()}_key")()
                if settings.DEBUG:
                    print(f"Debug: key1 = {self.key1}, key2 = {self.key2}, salt = {self.salt}\n\nkey_management: {choice, ok}")
        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: key1 = {self.key1}, key2 = {self.key2}, salt = {self.salt}\n\nkey_management: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "❗", f"An error occurred in Key Management: {str(e)}", QMessageBox.Ok)

    def split_or_recover(self):
        options = ["🔨 Split Key", "🛠️ Recover Key"]
        try:
            choice, ok = QInputDialog.getItem(self, "🔑 Split/Recover", "Please select an option:", options, 0, False)
            if ok:
                getattr(self, f"{choice.split(' ')[1].lower()}_key")()
                if settings.DEBUG:
                    print(f"Debug: choice = {choice}, ok = {ok}\n\nsplit_or_recover: {choice.split(' ')[1].lower()}")
        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: split_or_recover: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "❗", f"An error occurred in Split/Recover: {str(e)}", QMessageBox.Ok)

    @check_user_info_decorator
    def encrypt_or_decrypt(self, *args):
        options = ["🔒 Encrypt Files", "🔓 Decrypt Files"]
        try:
            choice, ok = QInputDialog.getItem(self, "🔑 Encrypt/Decrypt", "Please select an option:", options, 0, False)
            if ok:
                getattr(self, f"{choice.split(' ')[1].lower()}_files")()
                if settings.DEBUG:
                    print(f"Debug: choice = {choice}, ok = {ok}\n\nencrypt_or_decrypt: {choice.split(' ')[1].lower()}")
        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: encrypt_or_decrypt: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "❗", f"An error occurred in Encrypt/Decrypt: {str(e)}", QMessageBox.Ok)

    def generate_key(self):
        try:
            userinfo = get_keys()[0]
            self.key1 = self.EncryptionUtility.generate_strong_password(length=32) 
            if bool(userinfo["salt"]):
                self.salt = self.EncryptionUtility.salts()
            else:
                self.salt = b""
            message = f"Key1:{self.key1}"
            if userinfo["security_level"] != "Hard":
                message = f"Key1:{self.key1}\n\nsalt:{self.salt.hex()}"
            if userinfo["security_level"] == "Hard":
                self.key2 = self.EncryptionUtility.generate_strong_password(length=32) 
                while self.key1 == self.key2:
                    self.key2 = self.EncryptionUtility.generate_strong_password(length=32) 
                message += f"\n\nKey2:{self.key2}\n\nsalt:{self.salt.hex()}"
            
            QMessageBox.information(self, "Key Generated", f"{message}", QMessageBox.Ok)
            
            # Debug message
            if settings.DEBUG:
                print(f"Debug: userinfo = {userinfo}, key1 = {self.key1}, key2 = {self.key2}, salt = {self.salt}")
                
        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: Error generating key: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "❗", f"An error occurred while generating the key: {str(e)}", QMessageBox.Ok)

    def manual_key(self):
        try:
            key1, key2, salt = self.open_Password_window()
            if key1:
                self.key1 = key1
                self.salt = str(salt).encode()
                QMessageBox.information(self, "Key Set", f"Key set successfully!", QMessageBox.Ok)
            if key1 and key2:
                self.key1 = key1
                self.key2 = key2
                self.salt = str(salt).encode()
                QMessageBox.information(self, "Key Set", f"Key set successfully!", QMessageBox.Ok)
            
            # Debug message
            if settings.DEBUG:
                print(f"Debug: key1 = {self.key1}, key2 = {self.key2}, salt = {self.salt.hex()}")
            
        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: Error setting manual key: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}", QMessageBox.Ok)

    @check_user_info_decorator
    def split_key(self):
        try:
            if not self.key1:
                self.key_management()
                return

            # Step 1: Split the key1 and salt
            userinfo = get_keys()[0]
            shares1 = self.SecretSharer.split_secret(self.key1, int(userinfo["share_threshold"]), int(userinfo["num_shares"]))
            salt = self.SecretSharer.split_secret(self.salt, int(userinfo["share_threshold"]), int(userinfo["num_shares"]))
            data = {
                "key1": shares1,
                "salt": salt
            }
            # Debug message
            if settings.DEBUG:
                print(f"Debug: Splitting key1 = {self.key1}, salt = {self.salt.hex()}\nShares1: {shares1}, Salt: {salt}")

            # Step 2: Split key2 if it exists
            if self.key2:
                shares2 = self.SecretSharer.split_secret(self.key2, int(userinfo["share_threshold"]), int(userinfo["num_shares"]))
                data = {
                    "key1": shares1,
                    "key2": shares2,
                    "salt": salt
                }
                # Debug message
                if settings.DEBUG:
                    print(f"Debug: Splitting key2 = {self.key2}, Shares2: {shares2}")

            # Step 3: Ask the user how they want to handle the split keys
            response = self.choose_storage_option()

            if response == "Show Result":
                add = shares2 if self.key2 else [""]
                result_window = ResultWindow(shares1, key2_value=add, salt1_value=salt)
                result_window.exec_()
            elif response == "Local Storage":
                _, filename = create_or_edit_file(f"{userinfo['nickname']}_shares.json", data)
                QMessageBox.information(self, "Local Storage", f"Your file name is {filename}. Storage in {userinfo['directory']}", QMessageBox.Ok)

            elif response == "Both":
                add = shares2 if self.key2 else [""]
                _, filename = create_or_edit_file(f"{userinfo['nickname']}_shares.json", data)
                QMessageBox.information(self, "Local Storage", f"Your file name is {filename}. Storage in {userinfo['directory']}. Click Ok to Show Result", QMessageBox.Ok)
                ResultWindow(shares1, key2_value=add, salt1_value=salt).exec_()

            # Debug message for response
            if settings.DEBUG:
                print(f"Debug: Storage response = {response}, Data: {data}")

        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: Error splitting key: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "❗", f"An error occurred while splitting the key: {str(e)}", QMessageBox.Ok)


    def choose_storage_option(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Storage Option")
        
        layout = QVBoxLayout()
        
        label = QLabel("How would you like to receive the split key?")
        layout.addWidget(label)

        # Create buttons
        button_drive = QPushButton("Show Result")
        button_local = QPushButton("Local Storage")
        button_Both = QPushButton("Both")

        # Connect buttons to accept
        button_drive.clicked.connect(lambda: self.storage_selected(dialog, "Show Result"))
        button_local.clicked.connect(lambda: self.storage_selected(dialog, "Local Storage"))
        button_Both.clicked.connect(lambda: self.storage_selected(dialog, "Both"))

        layout.addWidget(button_drive)
        layout.addWidget(button_local)
        layout.addWidget(button_Both)

        dialog.setLayout(layout)
        dialog.exec_()  # Show dialog

        # Wait for the dialog to close and return the selected option
        return self.selected_option  # Return the selected option


    def storage_selected(self, dialog, option):
        self.selected_option = option  # Save the selected option
        dialog.done(1)  # Close the dialog

    def recover_key(self):
        try:
            my_data_window = RecoverPage()
            my_data_window.exec_()
            
            # Debug message
            if settings.DEBUG:
                print(f"Debug: Recovering key process executed successfully.")
                
        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: Error recovering key: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "❗", f"An error occurred while recovering the key: {str(e)}", QMessageBox.Ok)

    def encrypt_files(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
            if bool(self.user_info["salt"]):
                if not isinstance(self.salt, bytes):
                    self.salt.encode()

            if str(self.user_info["encryption_type"]).lower() == "chacha20":
                if file_path:
                    if not self.key2:                       
                        message = self.EncryptionUtility.encrypt_file(file_path, self.key1, use_aes=False)
                    if self.key2: 
                        message = self.EncryptionUtility.encrypt_file(file_path, self.key1, self.key2, use_double=True, use_aes=False)
                    QMessageBox.information(self, "Success", str(message), QMessageBox.Ok)
                
                # Debug message
                if settings.DEBUG:
                    print(f"Debug: Encrypting file with ChaCha20, file_path = {file_path}, key1 = {self.key1}, key2 = {self.key2}")
            else:
                if file_path:
                    if not self.key2:
                        print(isinstance(self.salt, bytes))
                        message = self.EncryptionUtility.encrypt_file(file_path, self.key1, use_aes=True)
                    if self.key2:
                        message = self.EncryptionUtility.encrypt_file(file_path, self.key1, self.key2, use_double=True, use_aes=True)
                    QMessageBox.information(self, "File Encrypted", str(message), QMessageBox.Ok)
                
                # Debug message
                if settings.DEBUG:
                    print(f"Debug: Encrypting file with AES, file_path = {file_path}, key1 = {self.key1}, key2 = {self.key2}")

        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: Error encrypting file: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "❗", f"An error occurred while encrypting the file: {str(e)}", QMessageBox.Ok)

    def decrypt_files(self):
        try:         
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Decrypt", filter="Encrypted Files (*.enc)")
            
            if str(self.user_info["encryption_type"]).lower() == "chacha20":
                if file_path:
                    if not self.key2:
                        if bool(self.user_info["salt"]):
                            if not isinstance(self.salt, bytes):
                                self.salt.encode()  
                        message = self.EncryptionUtility.decrypt_file(file_path, self.key1, use_aes=False)
                    if self.key2:
                        if bool(self.user_info["salt"]):
                            if not isinstance(self.salt, bytes):
                                self.salt.encode()  
                        message = self.EncryptionUtility.decrypt_file(file_path, self.key1, self.key2, use_double=True, use_aes=False)
                    QMessageBox.information(self, "Success", str(message), QMessageBox.Ok)
                
                # Debug message
                if settings.DEBUG:
                    print(f"Debug: Decrypting file with ChaCha20, file_path = {file_path}, key1 = {self.key1}, key2 = {self.key2}")
            else:
                if file_path:
                    if not self.key2:
                        message = self.EncryptionUtility.decrypt_file(file_path, self.key1, use_aes=True)
                    if self.key2:
                        message = self.EncryptionUtility.decrypt_file(file_path, self.key1, self.key2, use_double=True, use_aes=True)
                    QMessageBox.information(self, "File Decrypted", str(message), QMessageBox.Ok)
                
                # Debug message
                if settings.DEBUG:
                    print(f"Debug: Decrypting file with AES, file_path = {file_path}, key1 = {self.key1}, key2 = {self.key2}")

        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: Error decrypting file: {e}\n\nYou can close debug from settings.py\n\nSwitch DEBUG to False (DEBUG = False)")
            QMessageBox.critical(self, "❗", f"An error occurred while decrypting the file: {str(e)}", QMessageBox.Ok)

    def animate_buttons(self):
        buttons = self.findChildren(QPushButton)
        for i, button in enumerate(buttons):
            animation = QPropertyAnimation(button, b"geometry")
            animation.setDuration(1000 + i * 100)
            animation.setStartValue(QRect(button.x(), button.y() + 50, button.width(), button.height()))
            animation.setEndValue(QRect(button.x(), button.y(), button.width(), button.height()))
            animation.setEasingCurve(QEasingCurve.OutBounce)
            animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KeyGuard()
    window.show()
    sys.exit(app.exec_())