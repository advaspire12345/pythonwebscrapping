import subprocess

# List of packages to install
packages = ["customtkinter", "tkinter", "selenium", "Pillow", "pyautogui"]

# Install each package using pip
for package in packages:
    subprocess.check_call(["pip", "install", package])