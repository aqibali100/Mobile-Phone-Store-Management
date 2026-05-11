"""Modern button components using CustomTkinter."""
import customtkinter as ctk
from utils.constants import ACTIVE_THEME, BUTTON_HEIGHT, FONT_MEDIUM


def create_primary_button(parent, text, command=None, width=200):
    """Create a primary action button."""
    button = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=BUTTON_HEIGHT,
        font=FONT_MEDIUM,
        fg_color=ACTIVE_THEME["accent"],
        text_color=ACTIVE_THEME["background"],
        hover_color="#00b8d4",
        corner_radius=8,
        border_width=0
    )
    return button


def create_secondary_button(parent, text, command=None, width=200):
    """Create a secondary action button."""
    button = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=BUTTON_HEIGHT,
        font=FONT_MEDIUM,
        fg_color=ACTIVE_THEME["secondary"],
        text_color=ACTIVE_THEME["text"],
        hover_color=ACTIVE_THEME["primary"],
        corner_radius=8,
        border_width=2,
        border_color=ACTIVE_THEME["accent"]
    )
    return button


def create_danger_button(parent, text, command=None, width=200):
    """Create a danger action button (delete, remove)."""
    button = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=BUTTON_HEIGHT,
        font=FONT_MEDIUM,
        fg_color=ACTIVE_THEME["error"],
        text_color=ACTIVE_THEME["text"],
        hover_color="#dc2626",
        corner_radius=8,
        border_width=0
    )
    return button


def create_success_button(parent, text, command=None, width=200):
    """Create a success action button (save, confirm)."""
    button = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=BUTTON_HEIGHT,
        font=FONT_MEDIUM,
        fg_color=ACTIVE_THEME["success"],
        text_color=ACTIVE_THEME["background"],
        hover_color="#22c55e",
        corner_radius=8,
        border_width=0
    )
    return button
