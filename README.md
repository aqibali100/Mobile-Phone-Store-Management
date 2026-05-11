# Mobile Phone Store Management System

A lightweight desktop application for managing mobile phone inventory and sales, built with Python and CustomTkinter.

## Features

- Add, view, edit, and delete phone records (stored in `data/phones.json`).
- Dashboard with searchable table and serial numbering.
- Image upload support for phones (stored under `assets/phone_images/`).
- Sales report with CSV export.

## Quick Setup & Run (recommended)

From the project root, run these commands to create an isolated environment, install dependencies, and start the app.

1) Create a virtual environment:

```bash
python -m venv venv
```

2) Activate the virtual environment:

Linux / macOS (bash/zsh):
```bash
source venv/bin/activate
```

Windows (PowerShell):
```powershell
venv\\Scripts\\Activate.ps1
```

3) Install dependencies into the venv:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4) Start the application:

```bash
python main.py
```

Alternative: run without activating the venv:

```bash
./venv/bin/python main.py
```

Or use the included launcher script (Unix):

```bash
./run.sh
```

## Getting Started

### Demo login
- **Gmail:** admin@gmail.com
- **Password:** admin@123

### Quick Tutorial

1. Login (use demo credentials or register)
2. View dashboard
3. Add phone
4. Search and update records
5. Export sales/report as needed

## Project structure (high level)

- `main.py` — Application entry point
- `requirements.txt` — Python dependencies
- `run.sh` — launcher that activates `venv` and runs `main.py`
- `frontend/` — GUI windows and components
- `backend/` — business logic and file handling
- `utils/` — constants and validators
- `data/` — JSON data files (`phones.json`, `users.json`, `sales.json`)
- `assets/phone_images/` — images saved by the app

---
