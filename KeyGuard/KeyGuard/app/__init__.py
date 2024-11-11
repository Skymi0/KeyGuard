# app/__init__.py
from app.Filespage import FilesWindow
from app.helppage import HelpWindow
from app.informationpage import InformationWindow
from app.recoverpage import RecoverPage
from app.settingpage import SettingsWindow
from utils import dir_serach, read_file, append_to_file, check_and_restore_important_file, create_or_edit_file, backup_file
from app.passwordmanager import PasswordManager
from app.resultpage import ResultWindow
