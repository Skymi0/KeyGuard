import os
import subprocess
import sys

parent_dir = "KeyGuard"
env_name = os.path.join(parent_dir, "vevnKeyGuard")
script_path = os.path.join(parent_dir, "main.py")

current_dir = os.getcwd()
if os.path.basename(current_dir) != "KeyGuard":
    print("Please run the script inside the KeyGuard directory.")
    sys.exit(1)

if not os.path.isdir(parent_dir):
    print(f"The directory {parent_dir} does not exist. It will be created.")
    os.mkdir(parent_dir)

if not os.path.isfile(script_path):
    print(f"The program main.py does not exist inside the {parent_dir} directory.")
    print(f"Please place the main.py program inside the {parent_dir} directory.")
    sys.exit(1)

if not os.path.isdir(env_name):
    print(f"The Python environment does not exist. It will be created inside {parent_dir}.")
    subprocess.run(["python3", "-m", "venv", env_name])
else:
    print(f"The virtual environment {env_name} was found.")

# Activation of the virtual environment
if os.name == "nt":  # Windows
    activate_script = os.path.join(env_name, "Scripts", "activate")
    python_script = os.path.join(env_name, "Scripts", "python")
else:  # Linux/Unix
    activate_script = os.path.join(env_name, "bin", "activate")
    python_script = os.path.join(env_name, "bin", "python3")
if os.path.isfile(activate_script):
    print("Activating the virtual environment...")
    # Use subprocess to activate the environment
    subprocess.run([python_script, "-m", "pip", "install", "--upgrade","pip"])
    subprocess.run([python_script, "-m", "pip", "install", "-r","requirements.txt"])
    subprocess.run([python_script, "KeyGuard/main.py"])

else:
    print(f"Could not find the activation script at {activate_script}")
    sys.exit(1)
