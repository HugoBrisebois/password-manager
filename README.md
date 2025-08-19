
# Password Manager

**This is a simple password manager application for learning and personal use only. Not for commercial or production use.**

This app lets you manage your passwords in a modern, organized way, with a GUI inspired by Microsoft Authenticator. Passwords are sorted alphabetically, and you can easily add, delete, and export them.

## Features

- Modern Tkinter GUI (Microsoft Authenticator style)
- Add, delete, and search passwords
- Export passwords to CSV (Excel-compatible)
- Alphabetical sorting and grouping

## Requirements

- Python 3.7 or newer (tested on 3.7+)
- Standard library only (tkinter, sqlite3, csv)

> **Note:** `tkinter` is included with most Python installations. If you get an error about missing `tkinter`, install it via your OS package manager (e.g., `sudo apt install python3-tk` on Ubuntu).

## Installation

You can install the app as a Python package:

```sh
pip install dist/generator_password-1.0.0-py3-none-any.whl
```

Or build from source:

```sh
python setup.py sdist bdist_wheel
```

## Usage

After installation, you can launch the app in several ways(make sure to be in directory(Visual Studio Code)):

### 1. From the command line (cross-platform):

```sh
python -m generator_password
```

### 2. Windows Start Menu or Run dialog:

Type `generator_password-gui` and press Enter (after installing the package).

### 3. From source (for development):

```sh
python -m generator_password
```

## Project Structure

- `generator_password/` — Main package with all source code
- `setup.py` — Packaging configuration
- `requirements.txt` — (empty, uses only standard library)
- `MANIFEST.in` — Includes database and README in package
- `password_manager.db` — SQLite database (created automatically if missing)
- `logo.png` — App logo (if used)

## Notes

- All data is stored locally in `password_manager.db`.
- This app is for fun and learning only. Do not use for sensitive or production data.

---

Made by Hugo Brisebois
