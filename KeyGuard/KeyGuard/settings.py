## settings
import os

DEBUG = True
BASE_ROOT = os.getcwd() + "KeyGuard"
# Reset options
RESET_DB = False
RESET_APP = False

# Save Data
LAST_SAVE_STATUS = False
FILE_LOCATION = False


# PATH
PATH = os.environ["PATH"] = f"{BASE_ROOT}:{os.environ['PATH']}"
