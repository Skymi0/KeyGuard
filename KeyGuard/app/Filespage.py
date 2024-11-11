from datetime import datetime
import os
from pathlib import Path
from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QLabel, QMessageBox, QDialog
from utils import get_keys

class FilesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Files")
        self.setGeometry(200, 200, 400, 300)
        
        self.file_list = []
        self.file_details = {}

        try:
            userinfo = get_keys() 
            if isinstance(userinfo, list) and len(userinfo) > 0: 
                userinfo = userinfo[0] 

                current_dir = str(Path.cwd())
                file_path = os.path.join(current_dir, userinfo["directory"])

                if os.path.exists(file_path):
                    self.file_list = os.listdir(file_path)
                    self.file_details = self.get_file_details(file_path)
                else:
                    raise FileNotFoundError(f"Directory '{file_path}' not found.")
            else:
                raise ValueError("get_keys did not return a valid list or data.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Settings file not found.", QMessageBox.Ok)
        except KeyError as e:
            QMessageBox.critical(self, "Error", f"Missing key in settings file: {str(e)}", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}", QMessageBox.Ok)


        layout = QVBoxLayout(self)

        # Display file information
        self.file_info_label = QLabel("File Information:")
        layout.addWidget(self.file_info_label)

        self.file_list_widget = QListWidget()
        layout.addWidget(self.file_list_widget)

        # Populate file list
        self.populate_file_list()

        self.setLayout(layout)

    def get_file_details(self, directory):
        """Get details of files in the specified directory."""
        from decortion import check_user_settings_decorator  # تأجيل الاستيراد هنا

        @check_user_settings_decorator
        def inner_get_file_details(directory):
            file_details = {}
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    # Get creation time
                    creation_time = os.path.getctime(file_path)
                    # Convert to human-readable format
                    human_readable_time = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                    owner = get_keys()[0]["nickname"]
                    file_details[filename] = {
                        "creation_time": human_readable_time,
                        "owner": owner if owner != "keyguard" else "System",
                    }
            return file_details

        return inner_get_file_details(directory)

    def populate_file_list(self):
        """Populate the QListWidget with files and their details."""
        if not self.file_list:
            self.file_list_widget.addItem("No files found.")
        else:
            for filename in self.file_list:
                details = self.file_details.get(filename)
                creation_time = details["creation_time"] if details else "N/A"
                owner = details["owner"] if details else "N/A"
                self.file_list_widget.addItem(f"{filename} - Created on: {creation_time} by {owner}")
