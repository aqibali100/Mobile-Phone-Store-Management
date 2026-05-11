"""Message box helpers for user feedback."""
import customtkinter as ctk
from tkinter import messagebox
from utils.constants import ACTIVE_THEME, FONT_MEDIUM


def show_info(title, message):
    """Show information message."""
    messagebox.showinfo(title, message)


def show_error(title, message):
    """Show error message."""
    messagebox.showerror(title, message)


def show_warning(title, message):
    """Show warning message."""
    messagebox.showwarning(title, message)


def show_success(parent, message):
    """Show success notification."""
    # Create a custom CTk toplevel for success message
    notification = ctk.CTkToplevel(parent)
    notification.geometry("400x100")
    notification.title("Success")
    notification.attributes("-topmost", True)
    
    label = ctk.CTkLabel(
        notification,
        text=message,
        font=FONT_MEDIUM,
        text_color=ACTIVE_THEME["success"]
    )
    label.pack(pady=20)
    
    notification.after(2000, notification.destroy)


def ask_confirmation(title, message):
    """Show confirmation dialog and return True if user confirms."""
    return messagebox.askyesno(title, message)
