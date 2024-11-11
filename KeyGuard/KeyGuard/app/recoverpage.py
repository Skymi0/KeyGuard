import csv
import json
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QLineEdit, QApplication, QGroupBox,
                             QFileDialog, QDialog, QRadioButton, QScrollArea, QWidget,QCheckBox,QButtonGroup)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
from fpdf import FPDF
from keyshard import SecretSharer
import settings
from utils import get_keys

class RecoverPage(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recover Keys")
        self.setGeometry(200, 200, 400, 500)
        self.setStyleSheet("background-color: #2c3e50; color: #ecf0f1;")
        
        layout = QVBoxLayout(self)
        self.setting = get_keys()[0]
        self.SecretSharer = SecretSharer()
        title_label = QLabel("<h2 style='color: #2980B9;'>Recover Keys</h2>")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        self.key_choice_label = QLabel("Select key option:")
        layout.addWidget(self.key_choice_label)

        self.one_key_radio = QRadioButton("One Key")
        self.two_key_radio = QRadioButton("Two Keys")
        self.one_key_radio.setChecked(True)

        layout.addWidget(self.one_key_radio)
        layout.addWidget(self.two_key_radio)

        # Salt Key Checkbox
        self.salt_key_checkbox = QCheckBox("I have salt key")
        layout.addWidget(self.salt_key_checkbox)

        self.label = QLabel("Salt key status: Not checked")
        layout.addWidget(self.label)

        self.recover_label = QLabel("Enter key parts to recover the original key.")
        layout.addWidget(self.recover_label)

        # Scroll Area for Key Parts
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.parts_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.parts_layout)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Buttons Layout
        button_layout = QVBoxLayout()
        
        # Recover Key Button
        self.recover_button = QPushButton("Recover Key")
        self.recover_button.setStyleSheet("""
            background-color: #2980B9; 
            color: white; 
            border-radius: 5px; 
            padding: 5px 8px;  
            font-size: 16px;     
        """)
        self.recover_button.setFixedSize(375, 30) 

        # Recover with JSON File Button
        self.recover_button_file = QPushButton("Recover with JSON file")
        self.recover_button_file.setStyleSheet("""
            background-color: #27ae60; 
            color: white; 
            border-radius: 5px; 
            padding: 5px 8px;  
            font-size: 16px;     
        """)
        self.recover_button_file.setFixedSize(375, 30) 
        
        button_layout.addWidget(self.recover_button)
        button_layout.addWidget(self.recover_button_file)

        layout.addLayout(button_layout)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Connect buttons to functions
        self.recover_button.clicked.connect(self.recover_key)
        self.recover_button_file.clicked.connect(self.recover_key_file)

        self.one_key_radio.setChecked(get_keys()[0]["security_level"] != "High")
        self.two_key_radio.setChecked(get_keys()[0]["security_level"] == "High")
        # Connect radio buttons and checkbox to update input
        self.one_key_radio.toggled.connect(self.update_parts_input)
        self.two_key_radio.toggled.connect(self.update_parts_input)
        self.salt_key_checkbox.stateChanged.connect(self.update_parts_input)

        self.parts_input = []
        self.update_parts_input()

    def update_parts_input(self):
        # This function will dynamically update the parts input fields based on selected options
        # Clear previous inputs
        for input_field in self.parts_input:
            self.parts_layout.removeWidget(input_field)
            input_field.deleteLater()
        self.parts_input.clear()

        # Add new input fields based on selection
        if self.one_key_radio.isChecked():
            self.add_input_field("Key Part 1")
        else:
            self.add_input_field("Key Part 1")
            self.add_input_field("Key Part 2")

        # Update salt key status
        self.label.setText("Salt key status: Checked" if self.salt_key_checkbox.isChecked() else "Salt key status: Not checked")

    def add_input_field(self, placeholder):
        # Create a new input field and add it to the layout
        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #34495e; border-radius: 5px; margin: 5px; padding: 10px;")
        input_layout = QVBoxLayout(input_frame)

        input_label = QLabel(placeholder)
        input_layout.addWidget(input_label)

        # You can replace this with an actual input field (like QLineEdit) if needed
        input_field = QLabel("Enter " + placeholder)
        input_layout.addWidget(input_field)
        
        self.parts_layout.addWidget(input_frame)
        self.parts_input.append(input_frame)
    def adjust_window_size(self):
        threshold = int(self.setting["share_threshold"])

        base_height = 400
        additional_height_per_part = 20

        window_height = base_height + (additional_height_per_part * (threshold - 1))

        self.setFixedSize(400, window_height)

    def update_parts_input(self):
        for part_input in self.parts_input:
            part_input.deleteLater()
        self.parts_input.clear()
        self.parts_layout.addStretch()

        if self.two_key_radio.isChecked():
            total_shares = int(self.setting["share_threshold"]) 
            loops = 2
        else:
            total_shares = int(self.setting["share_threshold"])
            loops = 1
        if self.salt_key_checkbox.isChecked():
            for i in range(total_shares):
                part_input = QLineEdit(f"{i + 1}-salt")
                self.parts_input.append(part_input)
                self.parts_layout.addWidget(part_input)

        for i in range(loops):
            for i in range(total_shares):
                part_input = QLineEdit(f"{i + 1}-part")
                self.parts_input.append(part_input)
                self.parts_layout.addWidget(part_input)

        if self.salt_key_checkbox.isChecked():
            self.label.setText("Salt key status: Checked")
        else:
            self.label.setText("Salt key status: Not checked")
        self.adjust_window_size()

    def is_hex(self, s):
        """Helper function to check if a string is valid hex."""
        try:
            int(s, 16)
            return True
        except ValueError:
            return False



    def show_recovered_keys(self, message, key1, key2, key3,DEBUG=settings.DEBUG):
        if DEBUG:
            print(f"Debug: key1 = {key1}, key2 = {key2}, key3 = {key3}") 

        dialog = QDialog(self)
        dialog.setWindowTitle("Recovered Keys")
        dialog.setGeometry(200, 200, 600, 500)
        dialog.setStyleSheet("background-color: #282a36;")  # الخلفية الغامقة

        layout = QVBoxLayout(dialog)

        # Scroll area to handle long key text
        scroll = QScrollArea(dialog)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Title for the recovered keys window
        title_label = QLabel("<h2 style='color: #2980B9;'>Recovered Keys</h2>")
        container_layout.addWidget(title_label)

        # Instructions message
        instructions_label = QLabel("<p style='color: #f8f8f2;'>Here are your recovered keys. Click to copy:</p>")
        container_layout.addWidget(instructions_label)

        # Prepare the key display
        key_display_style = """
            QFrame {
                border: 1px solid #007BFF;
                border-radius: 5px;
                background-color: #282a36;
                padding: 10px;
                margin: 5px 0;
            }
            QLabel {
                font-size: 16px;
                color: #f8f8f2;
            }
        """
        
        def create_key_frame(key_label, key_value):
            frame = QFrame()
            frame.setStyleSheet(key_display_style)
            layout = QVBoxLayout(frame)

            if key_value:
                label = QLabel()
                label.setTextFormat(Qt.PlainText) 
                label.setText(f"{key_label}: {str(bytes.fromhex(key_value))[2:-1:]}")
                layout.addWidget(label)
                frame.mousePressEvent = lambda event: self.copy_to_clipboard(str(bytes.fromhex(key_value))[2:-1:]) if key_value else None
                return frame
            return None
        
        # Adding keys to the display
        for i, (key_label, key_value) in enumerate(zip(["Key 1", "Key 2", "salt 1"], [key1, key2, key3])):
            key_frame = create_key_frame(key_label, key_value)
            if key_frame:
                container_layout.addWidget(key_frame)

        # Add file format selection
        format_group = QButtonGroup(dialog)
        formats = ["CSV", "TXT", "PDF", "HTML"]
        format_box = QGroupBox("Select Format:")
        format_layout = QVBoxLayout()

        for format_name in formats:
            radio_button = QRadioButton(format_name)
            format_layout.addWidget(radio_button)
            format_group.addButton(radio_button)

        format_box.setLayout(format_layout)
        container_layout.addWidget(format_box)

        # Save button
        save_button = QPushButton("Save Keys")
        save_button.clicked.connect(lambda: self.save_keys_to_file(format_group, key1, key2, key3))
        container_layout.addWidget(save_button)

        scroll.setWidget(container)

        dialog.setLayout(layout)
        dialog.exec_()

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def save_keys_to_file(self, format_group, key1, key2, key3):
        key1 = str(bytes.fromhex(key1))[2:-1:] if self.is_hex(key1) else key1
        key2 = str(bytes.fromhex(key2))[2:-1:] if self.is_hex(key2) else key2
        key3 = str(bytes.fromhex(key3))[2:-1:] if self.is_hex(key3) else key3

        format_selected = format_group.checkedButton().text() if format_group.checkedButton() else None

        if format_selected:
            file_extension = format_selected.lower()

            default_file_name = f"recovered_keys.{file_extension}"

            file_path, _ = QFileDialog.getSaveFileName(self, "Save Keys", default_file_name, f"{format_selected} Files (*.{file_extension})")
            if not file_path.endswith(f".{file_extension}"):
                file_path += f".{file_extension}"
            if file_path:
                if format_selected == "TXT":
                    with open(file_path, 'w') as f:
                        f.write(f"Key 1: {key1 if key1 else 'Not Available'}\n")
                        if key2:
                            f.write(f"Key 2: {key2}\n")
                        if key3:
                            f.write(f"Key 3: {key3}\n")
                elif format_selected == "PDF":
                    self.save_as_pdf(file_path, key1, key2, key3) 
                elif format_selected == "HTML":
                    with open(file_path, 'w') as f:
                        f.write(f"""
                        <html lang="ar">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Recovered Keys</title>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    background-color: #f0f0f0;
                                    color: #333;
                                    margin: 20px;
                                    padding: 20px;
                                    border-radius: 10px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                }}
                                h2 {{
                                    color: #2980B9;
                                    text-align: center;
                                }}
                                p {{
                                    font-size: 16px;
                                    line-height: 1.6;
                                    background-color: white;
                                    padding: 10px;
                                    border-radius: 5px;
                                    margin: 10px 0;
                                }}
                            </style>
                        </head>
                        <body>
                            <h2>Recovered Keys</h2>
                            <p>Key 1: {key1 if key1 else 'Not Available'}</p>
                            {"<p>Key 2: " + key2 + "</p>" if key2 else ""}
                            {"<p>Key 3: " + key3 + "</p>" if key3 else ""}
                        </body>
                        </html>
                        """)
    def save_as_pdf(self, file_path, key1, key2="", key3=""):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=20)
        pdf.cell(200, 10, txt="Recovered Encryption Keys", ln=True, align='C')
        
        pdf.set_line_width(0.5)
        pdf.set_draw_color(0, 0, 0)
        pdf.line(10, 20, 200, 20)
        
        pdf.set_font("Arial", size=12)
        pdf.ln(15)
        
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, txt="Key 1:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=key1 if key1 else 'Not Available')
        
        if key2:
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 10, txt="Key 2:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=key2)
        
        if key3:
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 10, txt="Salt:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=key3)

        pdf.output(file_path)

    def recover_key(self):
        parts = [part.text() for index, part in enumerate(self.parts_input) ]
        part1 = [part.text() for index, part in enumerate(self.parts_input)  if index in range(int(self.userinfo["share_threshold"]))]
        part2 = [part.text() for index, part in enumerate(self.parts_input)  if index in range(int(self.userinfo["share_threshold"]),int(self.userinfo["share_threshold"])*2)]
        part3 = [part.text() for index, part in enumerate(self.parts_input)  if index in range(int(self.userinfo["share_threshold"])*2, int(self.userinfo["share_threshold"])*3)]
        self.status_label.setText("")

        if all(parts):
            if all(self.is_hex(part.split("-")[1]) for part in parts if "-" in part):
                try:
                    if self.one_key_radio.isChecked():
                        recovered_key1 = self.SecretSharer.recover_secret(part1)
                        recovered_key2 = "None"
                        recovered_key2 = self.SecretSharer.recover_secret(part2) if part2 else recovered_key2
                        self.show_recovered_keys(
                                                key1=recovered_key1,
                                                key3=recovered_key2)

                    elif self.two_key_radio.isChecked():
                        recovered_key1 = self.SecretSharer.recover_secret(part1)
                        recovered_key2 = "None"
                        recovered_key3 = "None"
                        recovered_key2 = self.SecretSharer.recover_secret(part2) if part2 else recovered_key2
                        recovered_key3 = self.SecretSharer.recover_secret(part3) if part3 else recovered_key3
                        self.show_recovered_keys(
                                                key1=recovered_key1,
                                                key2=recovered_key2,
                                                key3=recovered_key3
                                                    )

                except ValueError as e:
                    self.status_label.setText(f"❗: Value error occurred - {str(e)}")
                except TypeError as e:
                    self.status_label.setText(f"❗: Type error occurred - {str(e)}")
                except Exception as e:
                    self.status_label.setText(f"❗: An unexpected error occurred - {str(e)}")
            else:
                self.status_label.setText("❗: One or more parts are not valid hex values (expected format: '1-hex').")
        else:
            self.status_label.setText("❗: Please enter all key parts.")

    def recover_key_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Recover")
        self.status_label.setText("")

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    shares_list = json.load(file)

                def find_lists_in_json(data):
                    lists = []
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if isinstance(value, list):
                                temp_dict = {"key" + str(len(lists) + 1): value}
                                lists.append(temp_dict)
                            elif isinstance(value, dict):
                                lists.extend(find_lists_in_json(value))
                    return lists

                lists_in_json = find_lists_in_json(shares_list)
                if self.one_key_radio.isChecked():
                    recovered_key1 = self.SecretSharer.recover_secret(lists_in_json[0]["key1"])
                    if self.setting["salt"]:
                        try:
                            lists_in_json[2]["key3"]
                        except:
                            return "Error: Please check your choice of keys and ensure you have the correct number of keys required."
                        recovered_key2 = self.SecretSharer.recover_secret(lists_in_json[1]["key2"]) if lists_in_json[1]["key2"] else "None"
                    else:
                        recovered_key2 = "None"

                    self.show_recovered_keys(key1=recovered_key1,
                                             key3=recovered_key2)

                elif self.two_key_radio.isChecked():
                    recovered_key1 = self.SecretSharer.recover_secret(lists_in_json[0]["key1"])
                    if self.setting["salt"]:
                        recovered_key2 = self.SecretSharer.recover_secret(lists_in_json[1]["key2"]) if lists_in_json[1]["key2"] else "None"
                    else:
                        recovered_key2 = "None"
                    recovered_key2 = self.SecretSharer.recover_secret(lists_in_json[1]["key2"]) if lists_in_json[1]["key2"] else recovered_key2
                    recovered_key3 = self.SecretSharer.recover_secret(lists_in_json[2]["key3"]) if lists_in_json[2]["key3"] else recovered_key3
                    message = f"\n\nKey-1: {str(bytes.fromhex(recovered_key1))[2:-1:]}\n\nKey-2: {str(bytes.fromhex(recovered_key2))[2:-1:]}"
                    self.show_recovered_keys(message,
                                             key1=recovered_key1,
                                             key2=recovered_key2,
                                             key3=recovered_key3)

            except json.JSONDecodeError:
                self.status_label.setText("❗: Failed to decode JSON file.")
            except FileNotFoundError:
                self.status_label.setText("❗: File not found.")
            except Exception as e:
                print(f"An unexpected error occurred - {str(e)}")
