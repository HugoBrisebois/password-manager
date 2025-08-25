
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

download the git repo. then find the file Dist file and the app should be there


## Usage

You can launch the app in several ways:

### 1. Run the packaged executable (Windows):

Double-click `dist/main.exe` or run it from the command line:

```sh
dist\main.exe
```

### 2. From the command line (cross-platform, with Python):

```sh
python -m generator_password
```

### 3. Windows Start Menu or Run dialog (after installing as a package):

Type `generator_password-gui` and press Enter.

---

## Packaging as an Executable (Windows)

To create a standalone Windows executable (no Python required for end users):

1. Install PyInstaller:

	```sh
	pip install pyinstaller
	```

2. Run this command from the project root:

	```sh
	python -m pyinstaller --onefile --windowed --add-data "logo.png;." --add-data "password_manager.db;." generator_password\main.py
	```

3. The executable will be in the `dist` folder as `main.exe`.

4. Distribute the `main.exe` file along with `logo.png` and `password_manager.db` if needed.

## Project Structure

- `generator_password/` — Main package with all source code
- `setup.py` — Packaging configuration
- `requirements.txt` — (empty, uses only standard library)
- `MANIFEST.in` — Includes database and README in package
- `password_manager.db` — SQLite database (created automatically if missing)
- `logo.png` — App logo (if used)
- `dist/` — Contains the packaged executable after running PyInstaller
## Notes

- All data is stored locally in `password_manager.db`.
- This app is for fun and learning only. Do not use for sensitive or production data.
- If you update the app, re-run the PyInstaller command to generate a new executable.

---

Made by Hugo Brisebois
