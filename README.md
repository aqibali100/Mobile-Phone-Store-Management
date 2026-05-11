# Mobile Phone Store System

A lightweight desktop application for managing mobile phone inventory and sales, built with Python and CustomTkinter.

## Features

- Add, view, edit, and delete phone records (stored in `data/phones.json`).
- Dashboard with searchable table and serial numbering.
- Image upload support for phones (stored under `assets/phone_images/`).
- Sales report with CSV export.
- Simple JSON-backed backend (`backend/phone_manager.py`).

## Requirements

- Python 3.8+ (project was developed with Python 3.12).
- Install dependencies from `requirements.txt` (create a virtual environment first).

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the application:

```bash
python main.py
```

## Project Structure

- `main.py` — Application entry point.
- `backend/` — Backend helpers (phone manager, file handler, auth).
- `frontend/` — GUI windows and components built with CustomTkinter.
- `utils/` — Constants and utility helpers.
- `data/phones.json` — JSON store for phone records (sample data).
- `assets/phone_images/` — Saved phone images (created at runtime).

## Notes

- I removed some temporary/test files per request. If you need any removed file restored, tell me which and I will restore it if a copy is available.
- To run the GUI you need CustomTkinter available in your virtual environment.

---

If you want the README in Hindi or additional details (examples of JSON schema, screenshots, or contribution guide), tell me and I will add them.
# Mobile Phone Store Management System

A modern, feature-rich Python desktop application for managing mobile phone store inventory using CustomTkinter GUI.

## 📱 Features

### Core Functionality
- **Add New Phone** - Add phones with details: Name, Brand, Price, RAM, Storage, Color, Quantity
- **View All Phones** - Display all inventory in a professional table format
- **Search Phones** - Search by Name or Brand
- **Update Prices** - Modify phone prices easily
- **Delete Records** - Remove phones from inventory with confirmation
- **Sales Report** - View and export inventory reports
- **Low Stock Warning** - Automatic alerts for items below threshold (5 units)

### UI/UX Features
- Modern dark-themed interface using CustomTkinter
- Professional table views with sorting capability
- Real-time inventory statistics
- Responsive button layout
- Custom color themes (Dark Blue, Black & Gold, Purple Gradient, Light Gray)
- Smooth animations and transitions
- Input validation with helpful error messages

### Data Management
- JSON-based file persistence
- Automatic data saving
- CSV export functionality for reports
- Data validation before storage

## 🛠️ Technologies Used

- **Python 3.8+**
- **CustomTkinter** - Modern GUI framework
- **PIL/Pillow** - Image handling
- **JSON** - Data persistence
- **CSV** - Report export

## 📦 Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or extract the project**
```bash
cd mobile_phone_store
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

## 🚀 Getting Started

### Login Credentials (Demo)
- **Gmail:** admin@gmail.com
- **Password:** admin@123

### Quick Tutorial

1. **Login** - Use credentials above or register a new account
2. **View Dashboard** - See key statistics at a glance
3. **Add Phone** - Click "Add New Phone" to add inventory
4. **Search** - Find specific phones quickly
5. **View Report** - Check inventory value and stock levels
6. **Update** - Modify prices as needed

## 📁 Project Structure

```
mobile_phone_store/
├── main.py                    # Application entry point
# Mobile Phone Store System

A lightweight desktop application for managing mobile phone inventory and sales, built with Python and CustomTkinter.

## Quick Setup & Run (recommended)

Follow these commands from the project root to create an isolated environment, install dependencies, and run the app.

1) Create a virtual environment (if you don't already have one):

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
venv\Scripts\Activate.ps1
```

3) Install dependencies into the venv:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4) Start the application (from project root):

```bash
python main.py
```

Alternative: run using the project's venv Python without activating:

```bash
./venv/bin/python main.py
```

Or use the included launcher script which activates the venv (Unix):

```bash
./run.sh
```

## Detailed notes & troubleshooting

- Use the venv Python to avoid system-level package restrictions (PEP 668). If you see an error like "This environment is externally managed", it means you're trying to install packages to the system Python. Create and use the project `venv` as shown above.

- Verify which Python is active:

```bash
python -c "import sys; print(sys.executable)"
which python
```

- Check that `customtkinter` is installed in the venv:

```bash
./venv/bin/python -m pip show customtkinter
```

- If the GUI does not appear in a headless environment (no display), set your display variable appropriately (example for X11):

```bash
export DISPLAY=:0
./venv/bin/python main.py
```

## If something goes wrong

- To reinstall dependencies in the venv:

```bash
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

- If you accidentally used system `pip` and want to cleanly recreate the venv:

```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Project structure (high level)

- `main.py` — Application entry point
- `requirements.txt` — Python dependencies
- `run.sh` — small launcher that activates `venv` and runs `main.py`
- `frontend/` — GUI windows and components
- `backend/` — business logic and file handling
- `utils/` — constants and validators
- `data/` — JSON data files (`phones.json`, `users.json`, `sales.json`)
- `assets/phone_images/` — images saved by the app

## Common troubleshooting

- "No module named 'customtkinter'": make sure you run `./venv/bin/python main.py` or activate `venv` before running `python main.py`, then install `requirements.txt` into that venv.
- "externally-managed-environment": create and use a venv (see steps above).
- Permissions errors when saving files: ensure `data/` and `assets/phone_images/` are writable by your user.

## Developer notes

- Tested with Python 3.12 in a virtual environment.
- If you'd like a `Makefile`, desktop shortcut, or systemd user service to auto-start the app, I can add that.

---

File: [README.md](README.md)
