import binascii
import pickle
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QMessageBox,QCheckBox)
from utils import EncryptionUtility
from keyshard.passwordcheck import is_strong_password
from utils import dir_serach, get_keys, update_key


class PasswordManager(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.saved = False
        self.generated_passwords = []
        self.history_visible = False
        self.settings = get_keys()[0]
        self.key1 = None
        self.key2 = None
        self.salt = None

    def initUI(self):
        self.setWindowTitle('Password Manager')
        self.setGeometry(100, 100, 450, 700)
        self.setStyleSheet("background-color: #2e3440; color: #d8dee9; font-family: Arial; border-radius: 10px;")

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.password_length_input = QtWidgets.QSpinBox(self)
        self.password_length_input.setRange(16, 64)
        self.password_length_input.setValue(16)
        self.password_length_input.setStyleSheet(self.get_input_style())
        layout.addWidget(QtWidgets.QLabel("Password Length (16-64 characters):"))
        layout.addWidget(self.password_length_input)

        self.password_input_layout = QtWidgets.QVBoxLayout()
        self.single_password_radio = QtWidgets.QRadioButton("Enter One Password", self)
        self.double_password_radio = QtWidgets.QRadioButton("Enter Two Passwords", self)
        self.single_password_radio.setChecked(True)


        self.password_input_layout.addWidget(self.single_password_radio)
        self.password_input_layout.addWidget(self.double_password_radio)
        layout.addLayout(self.password_input_layout)

        self.password_input1 = QtWidgets.QLineEdit(self)
        self.password_input1.setPlaceholderText('Enter your password')
        self.password_input1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input1.setStyleSheet(self.get_input_style())
        layout.addWidget(self.password_input1)

        self.password_input2 = QtWidgets.QLineEdit(self)
        self.password_input2.setPlaceholderText('Enter your second password')
        self.password_input2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input2.setStyleSheet(self.get_input_style())
        self.password_input2.setVisible(False)
        layout.addWidget(self.password_input2)



        self.salt_key_checkbox = QCheckBox("I want salt key:")
        layout.addWidget(self.salt_key_checkbox)


        self.salt_input = QtWidgets.QLineEdit(self)

        self.salt_input.setPlaceholderText('Enter your salt')
        self.salt_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.salt_input.setStyleSheet(self.get_input_style())
        self.salt_input.setVisible(False)
        layout.addWidget(self.salt_input)
        
            

        self.check_button = self.create_button('Check Password', self.check_password)
        layout.addWidget(self.check_button)

        self.generate_button = self.create_button('Generate Strong Password', self.generate_password)
        layout.addWidget(self.generate_button)

        self.save_button = self.create_button('Save Password', self.save_password)
        layout.addWidget(self.save_button)

        self.load_key_button = self.create_button('Load Key', self.load_key)
        layout.addWidget(self.load_key_button)

        self.show_password_button = self.create_button('Show Password', self.toggle_password_visibility)
        self.show_password_button.setCheckable(True)
        layout.addWidget(self.show_password_button)

        self.pass1_label = QtWidgets.QLabel(self)
        self.pass1_label.setStyleSheet("padding: 10px; font-weight: bold; font-size: 14px;")
        self.pass2_label = QtWidgets.QLabel(self)
        self.pass2_label.setStyleSheet("padding: 10px; font-weight: bold; font-size: 14px;")
        self.salt_label = QtWidgets.QLabel(self)
        self.salt_label.setStyleSheet("padding: 10px; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.pass1_label)
        layout.addWidget(self.pass2_label)
        layout.addWidget(self.salt_label)
        self.history_label = QtWidgets.QLabel("Generated Passwords:")
        self.history_display = QtWidgets.QTextEdit(self)
        self.history_display.setReadOnly(True)
        self.history_display.setStyleSheet(self.get_input_style())
        self.history_display.setVisible(False)
        self.toggle_history_button = self.create_button('Show History', self.toggle_history)
        layout.addWidget(self.toggle_history_button)
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_display)

        self.setLayout(layout)
        self.setFixedSize(450, 800)
        self.salt_key_checkbox.toggled.connect(self.update_password_check)
        self.single_password_radio.toggled.connect(self.toggle_password_fields)
        self.double_password_radio.toggled.connect(self.toggle_password_fields)

        self.password_button_group = QtWidgets.QButtonGroup(self)
        self.password_button_group.addButton(self.single_password_radio)
        self.password_button_group.addButton(self.double_password_radio)


    def get_input_style(self):
        return "background-color: #3b4252; color: #d8dee9; border: 1px solid #434c5e; padding: 10px; border-radius: 5px;"

    def get_button_style(self, background_color):
        return f"background-color: {background_color}; color: black; border: none; padding: 10px; border-radius: 5px; font-weight: bold;"

    def create_button(self, text, callback):
        button = QtWidgets.QPushButton(text, self)
        button.clicked.connect(callback)
        button.setStyleSheet(self.get_button_style('#5e81ac'))
        return button

    def toggle_password_fields(self):
        if self.single_password_radio.isChecked():
            self.password_input2.setVisible(False)
            self.password_input2.clear()
        else:
            self.password_input2.setVisible(True)

    def update_password_check(self):
        password1 = self.password_input1.text()
        password2 = self.password_input2.text() if self.double_password_radio.isChecked() else ""
        
        if self.salt_key_checkbox.isChecked():
            salt = self.salt_input.text()
            if is_strong_password(salt):
                self.salt_label.setText("Salt is strong.")
                self.salt_label.setStyleSheet("color: #A3BE8C;")
        if password1:
            if is_strong_password(password1):
                self.pass1_label.setText("First password is strong.")
                self.pass1_label.setStyleSheet("color: #A3BE8C;")
            else:
                self.pass1_label.setText("First password is weak. Please choose a stronger password.")
                self.pass1_label.setStyleSheet("color: #BF616A;")

        if password2:
            if is_strong_password(password2):
                self.pass2_label.setText("Second password is strong.")
                self.pass2_label.setStyleSheet("color: #A3BE8C;")
            else:
                self.pass2_label.setText("Second password is weak. Please choose a stronger password.")
                self.pass2_label.setStyleSheet("color: #BF616A;")

        if self.salt_key_checkbox.isChecked():
            self.salt_input.setVisible(True)
        else:
            self.salt_input.setVisible(False)

    def check_password(self):
        self.update_password_check()  

    def generate_password(self):
        length = self.password_length_input.value()
        strong_password1, strong_password2 = None, None

        def generate_unique_password(generate_func):
            while True:
                password = generate_func()
                if password != strong_password1:
                    return password


        strong_password1 = EncryptionUtility().generate_strong_password(length)
        strong_password2 = generate_unique_password(lambda: EncryptionUtility().generate_strong_password(length))
        salt = str(binascii.hexlify(EncryptionUtility().salts()))[2:-1:] if self.salt_key_checkbox.isChecked() else ""
        
        self.password_input1.setText(str(strong_password1))
        
        if strong_password2 is not None:
            self.password_input2.setText(str(strong_password2))

        self.pass1_label.setStyleSheet("color: #88c0d0;")
        self.pass2_label.setStyleSheet("color: #88c0d0;")
        self.salt_label.setStyleSheet("color: #88c0d0;")
        self.generated_passwords.append("passwd1: "+str(strong_password1))
        if self.salt_key_checkbox.isChecked() :
            self.salt_input.setText(salt)
            self.generated_passwords.append("salt: "+str(salt))
        if self.double_password_radio.isChecked():
            self.generated_passwords.append("passwd2: "+str(strong_password2))
        self.update_history_display()
    def process_salt(self,salt):
        try:
            if isinstance(salt, str) and all(c in '0123456789abcdefABCDEF' for c in salt):
                self.salt = binascii.unhexlify(salt)
            else:
                self.salt = salt 
        except (TypeError, ValueError) as e:
            return None
    def save_password(self):
        password1 = self.password_input1.text()
        password2 = self.password_input2.text()
        salt = self.salt_input.text() if self.salt_input.text() else "None"
        message = f"""
        <p style='font-size: 14px;'>The salt value in settings is <b style='color: red;'>False</b>. 
        To enhance security, you can go to the settings and change the checkbox to <b style='color: green;'>True</b>.</p>
        <p style='font-size: 16px; color: #50fa7b;'><b>Saved Salt Value:</b> <br>{salt}</p>
        <p style='font-size: 14px;'>Please make sure to update this setting for better encryption safety.</p>
        """
        if password1 and password2:
            if not bool(self.settings["salt"]):
                QMessageBox.information(self, "Salt Value", message, QMessageBox.Ok)


            
            if password1 == password2:
                self.pass1_label.setText("Cannot save: Both passwords are the same.")
                self.pass1_label.setStyleSheet("color: #BF616A;")  
                return 

            with open('guard.key', 'wb') as f:
                if salt != "None":
                    pickle.dump({'salt': salt, 'password1': password1, "password2":password2}, f)
                else:
                    pickle.dump({'password1': password1, "password2":password2}, f)
            self.pass1_label.setText("Passwords saved to guard.key")
            self.pass1_label.setStyleSheet("color: #A3BE8C;")  
            self.key1 = password1
            self.key2 = password2
            if self.salt_key_checkbox.isChecked():
                self.salt = self.process_salt(salt=salt)
            self.saved = True

        elif password1:
            if not bool(self.settings["salt"]):
                QMessageBox.information(self, "Salt Value", message, QMessageBox.Ok)
            with open('guard.key', 'wb') as f:
                pickle.dump({'salt': salt, 'password1': password1}, f)
            self.pass1_label.setText("Passwords saved to guard.key")
            self.pass1_label.setStyleSheet("color: #A3BE8C;")  
            self.key1 = password1
            if self.salt_key_checkbox.isChecked() :
                self.salt = salt
            self.saved = True
        else:
            self.pass1_label.setText("No passwords to save.")

    def load_key(self):
        try:
            file_path, _ = dir_serach("guard.key")
            with open(file_path, 'rb') as f:
                data = pickle.load(f)

                if isinstance(data, dict):
                    passwords = []
                    self.salt = data.get('salt', None)
                    
                    for key in data.keys():
                        if key.lower().startswith("password"):
                            passwords.append(data[key])
                    
                    if passwords:
                        self.key1 = passwords[0] 
                        self.key2 = passwords[1] if len(passwords) > 1 else None
                        if self.key1:
                            self.password_input1.setText(self.key1)
                        if self.key2:
                            self.password_input2.setText(self.key2)
                        password_info = [f"{len(passwords)} password(s) loaded."]
                        if self.salt:
                            password_info.append("Salt is present.")
                            self.salt_input.setText(self.salt)
                        else:
                            password_info.append("No salt provided.")
                        
                        self.pass1_label.setText(" ".join(password_info))
                        self.pass1_label.setStyleSheet("color: #A3BE8C;")
                    else:
                        self.pass1_label.setText("No passwords found.")
                        self.pass1_label.setStyleSheet("color: #BF616A;")
                else:
                    self.pass1_label.setText("Data format is incorrect.")
                    self.pass1_label.setStyleSheet("color: #BF616A;")
                    
        except FileNotFoundError:
            self.pass1_label.setText("No key file found. Please save a guard.key first.")
            self.pass1_label.setStyleSheet("color: #BF616A;")
        except PermissionError:
            self.pass1_label.setText("Permission denied: Cannot open the file.")
            self.pass1_label.setStyleSheet("color: #BF616A;")
        except Exception as e:
            self.pass1_label.setText(f"Error loading key: {str(e)}")
            self.pass1_label.setStyleSheet("color: #BF616A;")

    def update_history_display(self):
        self.history_display.clear()
        for password in self.generated_passwords:
            self.history_display.append(password)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input1.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.password_input2.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.salt_input.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.show_password_button.setText('Hide Passwords')
        else:
            self.password_input1.setEchoMode(QtWidgets.QLineEdit.Password)
            self.password_input2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.salt_input.setEchoMode(QtWidgets.QLineEdit.Password)
            self.show_password_button.setText('Show Passwords')

    def toggle_history(self):
        self.history_visible = not self.history_visible 
        self.history_display.setVisible(self.history_visible)  
        self.toggle_history_button.setText('Hide History' if self.history_visible else 'Show History')
