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
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
│
├── frontend/                  # UI Layer
│   ├── login_window.py       # Login form
│   ├── dashboard.py          # Main dashboard
│   ├── add_phone_window.py   # Add phone form
│   ├── view_phone_window.py  # View all phones
│   ├── search_phone_window.py # Search functionality
│   ├── update_phone_window.py # Update prices
│   ├── sales_report_window.py # Reports
│   ├── components/           # Reusable UI components
│   │   ├── buttons.py        # Custom button styles
│   │   ├── tables.py         # Table widget
│   │   └── message_boxes.py  # Dialogs & notifications
│   └── assets/              # Images and icons
│       ├── images/
│       └── icons/
│
├── backend/                   # Business Logic
│   ├── auth.py              # Authentication
│   ├── phone_manager.py     # Phone operations
│   ├── stock_manager.py     # Stock tracking
│   ├── sales_manager.py     # Sales records
│   └── file_handler.py      # File I/O
│
├── data/                      # Data Storage
│   ├── phones.json          # Phone inventory
│   ├── users.json           # User accounts
│   └── sales.json           # Sales records
│
└── utils/                     # Utilities
    ├── validators.py        # Input validation
    └── constants.py         # App constants & themes
```

## 💾 Data Format

### Phone Record (phones.json)
```json
{
  "id": 1,
  "name": "Samsung S24",
  "brand": "Samsung",
  "price": 25000.00,
  "ram": 8,
  "storage": 256,
  "color": "Midnight Black",
  "quantity": 5
}
```

## 🎨 Color Themes

The application includes multiple color themes:

- **Dark Blue** (Default) - Professional dark blue with cyan accents
- **Black & Gold** - Elegant black with gold highlights
- **Purple Gradient** - Modern purple gradient
- **Light Gray** - Clean light theme for better readability

To change theme, modify `ACTIVE_THEME` in `utils/constants.py`

## 📊 Sample Data

| ID | Name | Brand | Price | RAM | Storage | Qty |
|---|---|---|---|---|---|---|
| 1 | Samsung S24 | Samsung | $25,000 | 8GB | 256GB | 5 |
| 2 | iPhone 15 | Apple | $32,000 | 8GB | 256GB | 3 |

## ⚙️ Configuration

### Modify Low Stock Threshold
Edit in `utils/constants.py`:
```python
LOW_STOCK_THRESHOLD = 5  # Change to desired quantity
```

### Change Color Theme
Edit in `utils/constants.py`:
```python
ACTIVE_THEME = THEME_BLACK_GOLD  # Choose any theme
```

## 🐛 Troubleshooting

### Issue: CustomTkinter not found
**Solution:** Run `pip install customtkinter`

### Issue: File permission errors
**Solution:** Ensure write permissions in data/ directory

### Issue: GUI not displaying correctly
**Solution:** Ensure you have a compatible display manager and updated Python

## 📈 Future Enhancements

- Multi-user authentication with database
- Barcode scanning integration
- Email notifications for low stock
- Advanced analytics dashboard
- Mobile app version
- Cloud backup integration

## 📝 License

This project is for educational purposes.

## 👨‍💻 Developer Notes

- Built with CustomTkinter for modern UI
- Uses JSON for simplicity (upgrade to SQLite for production)
- Modular architecture for easy maintenance
- Component-based UI for code reusability

## 💡 Tips

- Export reports regularly for record keeping
- Monitor low stock warnings
- Regular database backups recommended
- Update prices based on market conditions

---

**Version:** 1.0.0  
**Last Updated:** May 2026  
**Status:** Active Development
