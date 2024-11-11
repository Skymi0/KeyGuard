# decorator/decortion.py
from utils import get_keys
from utils.database_manager import add_key, create_database

def check_user_info_decorator(func):
    def wrapper(self, *args):
        userinfo = get_keys()[0]


        if userinfo: 
                if not userinfo["nickname"] or userinfo["nickname"] == "keyguard":
                    self.clear_notification()
                    self.show_notification("Please check settings and provide a your nickname")
                    return
                
                if self.key1 is None:
                    self.clear_notification()
                    self.show_notification("Please generate a key.")
                    if func.__name__ == "encrypt_or_decrypt":
                        return self.key_management(*args)
        else:
            default_setting = {
                "share_threshold": 3,
                "num_shares": 5,
                "nickname": "keyguard",
                "directory": "room",
                "encryption_type":"AES",
                "security_level": "Normal",
                "creation_date": "",
                "last_modified": "",
                "notes": "I left the USB with my brother..."
            }
            add_key(default_setting)
        
        return func(self, *args)

    return wrapper


def check_user_settings_decorator(func):
    def wrapper(self, *args):
        usersettings = get_keys()[0]
        if usersettings is None:
            default_setting = [
                {
                "share_threshold": 3,
                "num_shares": 5,
                "nickname": "keyguard",
                "directory": "room",
                "encryption_type":"AES",
                "security_level": "Normal",
                "creation_date": "",
                "last_modified": "",
                "notes": "I left the USB with my brother..."
                }
            ]
            create_database()
            add_key(default_setting[0])
        
        return func(self, *args)

    return wrapper
