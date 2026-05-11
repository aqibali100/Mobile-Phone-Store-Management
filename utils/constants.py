"""Common constants and paths."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PHONES_FILE = DATA_DIR / "phones.json"
USERS_FILE = DATA_DIR / "users.json"
SALES_FILE = DATA_DIR / "sales.json"
PHONE_IMAGES_DIR = BASE_DIR / "assets" / "phone_images"

# Theme Constants
THEME_DARK_BLUE = {
    "primary": "#1f3a93",
    "secondary": "#2d5aa8",
    "accent": "#00d4ff",
    "background": "#0f1419",
    "surface": "#1a1f2e",
    "text": "#ffffff",
    "text_secondary": "#b0b8c8",
    "success": "#4ade80",
    "error": "#f87171",
    "warning": "#fbbf24"
}

THEME_BLACK_GOLD = {
    "primary": "#1a1a1a",
    "secondary": "#2d2d2d",
    "accent": "#d4af37",
    "background": "#0d0d0d",
    "surface": "#1a1a1a",
    "text": "#ffffff",
    "text_secondary": "#b8860b",
    "success": "#4ade80",
    "error": "#f87171",
    "warning": "#fbbf24"
}

THEME_PURPLE_GRADIENT = {
    "primary": "#6366f1",
    "secondary": "#8b5cf6",
    "accent": "#ec4899",
    "background": "#1a0933",
    "surface": "#2d1b4e",
    "text": "#ffffff",
    "text_secondary": "#d1b3e0",
    "success": "#4ade80",
    "error": "#f87171",
    "warning": "#fbbf24"
}

THEME_LIGHT_GRAY = {
    "primary": "#e5e7eb",
    "secondary": "#d1d5db",
    "accent": "#3b82f6",
    "background": "#f9fafb",
    "surface": "#ffffff",
    "text": "#1f2937",
    "text_secondary": "#6b7280",
    "success": "#10b981",
    "error": "#ef4444",
    "warning": "#f59e0b"
}

# Default theme
ACTIVE_THEME = THEME_DARK_BLUE

# UI Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
PADDING = 15
BUTTON_HEIGHT = 40
FONT_LARGE = ("Segoe UI", 18, "bold")
FONT_MEDIUM = ("Segoe UI", 14)
FONT_SMALL = ("Segoe UI", 11)
FONT_TINY = ("Segoe UI", 9)

# Low stock threshold
LOW_STOCK_THRESHOLD = 5
