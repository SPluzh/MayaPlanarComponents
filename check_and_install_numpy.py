import os
import sys
import subprocess
import importlib

def check_and_install(package_name):
    def get_version(name):
        try:
            module = importlib.import_module(name)
            version = getattr(module, '__version__', 'unknown')
            print(f"{name} is already installed. Version: {version}")
            return True
        except ImportError:
            print(f"{name} is not installed.")
            return False

    # First check
    if get_version(package_name):
        return

    # Locate mayapy.exe
    maya_exe_path = sys.executable
    maya_dir = os.path.dirname(maya_exe_path)
    mayapy_path = os.path.join(maya_dir, "mayapy.exe")

    if not os.path.exists(mayapy_path):
        print("mayapy.exe not found. Cannot proceed with installation.")
        return

    # Attempt to install
    try:
        print(f"Installing {package_name} using mayapy...")
        subprocess.check_call([mayapy_path, "-m", "pip", "install", package_name])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing {package_name}:", e)
        return

    # Final check after installation
    print("Checking installation result...")
    if get_version(package_name):
        print(f"{package_name} installed successfully.")
    else:
        print(f"Failed to install {package_name}.")

check_and_install("numpy")