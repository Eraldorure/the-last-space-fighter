"""This file deals with the update of the game's elements, as well as the setup, which includes installing the required
dependencies and other things such as checking the default language."""

import os
import sys
import subprocess
from configparser import ConfigParser
from shutil import rmtree

if os.name == "nt":
    import ctypes
    from locale import windows_locale

CORE_COMPONENTS = ["pip", "venv"]  # Things that can be executed with `python -m <...>`
PACKAGES = ["pyxel", "requests"]  # Required dependencies
LANGUAGES = ["en", "fr"]  # Unsupported languages will fall back to 'en'


def check_python_components(executable: str = sys.executable):
    """Checks if the required components (Python, pip and venv) are installed. If not, exists the program while printing
    an error message.
    The 'executable' argument is the path to the Python executable that is going to get checked."""

    if sys.version_info.major < 3 and sys.version_info.minor < 11:  # Check Python (must be 3.11 or later)
        print(f"ERROR: Please use Python 3.11 or higher.", file=sys.stderr)
        sys.exit(1)

    for component in CORE_COMPONENTS:  # Check other required core components
        try:
            subprocess.check_call([executable, "-m", component, "--help"], stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"ERROR: {component.capitalize()} was not found, please install it.", file=sys.stderr)
            sys.exit(1)


def install_requirements(executable: str = sys.executable):
    """Installs all the required dependencies for the game.
    The 'executable' argument is the path to the Python executable to use for the installation."""

    for pkg in PACKAGES:
        subprocess.check_call([executable, "-m", "pip", "install", f"{pkg}", "-q", "--disable-pip-version-check"])


def get_system_language() -> str:
    """Checks the default language of the user's system. Returns English ('en') if the language is not supported or if
    the detection failed."""

    if os.name == "nt":  # Windows
        lang = windows_locale.get(ctypes.windll.kernel32.GetUserDefaultUILanguage(), "en_US")
    else:  # Unix-based systems
        lang = os.getenv("LANG", "en_US.UTF-8")

    lang = lang[:2].lower()
    if lang in LANGUAGES:
        return lang
    return "en"


def check_remnants():
    """Checks if there are remnants of a previous installation of the game. If so, it will remove them."""

    for directory in ["venv", "code/__pycache__"]:
        if os.path.exists(directory):
            rmtree(directory)


config = ConfigParser()
config.read("./data/config.ini")

venv_exec = os.getcwd() + ("/venv/Scripts/python.exe" if os.name == "nt" else "/venv/bin/python")  # Path to the virtual environment's Python executable

if config["info"]["first_launch"] == "yes":
    print("Deleting potential remnants...")
    check_remnants()

    print("Checking core components...")
    check_python_components()

    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"])

    print("Installing required dependencies...")
    install_requirements(venv_exec)

    print("Checking system language...")
    config["options"]["language"] = get_system_language()

    config["info"]["first_launch"] = "no"
    with open("./data/config.ini", "w") as file:
        config.write(file)
    print("Setup complete.")

try:
    subprocess.run([venv_exec, "game.py"])
except FileNotFoundError:
    print("ERROR: The virtual environment was not found. Please run the launch.py script again to fix the issue.", file=sys.stderr)
    config["info"]["first_launch"] = "yes"
    with open("./data/config.ini", "w") as file:
        config.write(file)
    input("Press enter to exit...")
    sys.exit(1)
