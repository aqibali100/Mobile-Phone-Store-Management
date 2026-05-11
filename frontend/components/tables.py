"""Table component using Treeview for modern table display."""
import customtkinter as ctk
from tkinter import ttk
from utils.constants import ACTIVE_THEME, FONT_SMALL, FONT_TINY


def create_table(parent, columns, height=15):
    """
    Create a modern table (Treeview) with custom styling.
    
    Args:
        parent: Parent CTk widget
        columns: List of tuples (column_name, width)
        height: Number of rows to display
    """
    # Define style for the treeview
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configure colors
    bg_color = ACTIVE_THEME["surface"]
    fg_color = ACTIVE_THEME["text"]
    accent_color = ACTIVE_THEME["accent"]
    
    style.configure(
        "Treeview",
        background=bg_color,
        foreground=fg_color,
        fieldbackground=bg_color,
        font=FONT_TINY,
        rowheight=30,
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        background=ACTIVE_THEME["primary"],
        foreground=fg_color,
        borderwidth=1,
        font=FONT_SMALL,
        relief="flat"
    )
    style.map("Treeview", background=[("selected", accent_color)])
    style.map("Treeview.Heading", background=[("active", ACTIVE_THEME["secondary"])])
    
    # Create frame for table and scrollbar
    table_frame = ctk.CTkFrame(parent, fg_color=ACTIVE_THEME["background"])
    
    # Create scrollbars
    v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
    h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
    
    # Create treeview
    col_names = [col[0] for col in columns]
    col_widths = [col[1] if len(col) > 1 else 100 for col in columns]
    
    tree = ttk.Treeview(
        table_frame,
        columns=col_names,
        height=height,
        yscrollcommand=v_scrollbar.set,
        xscrollcommand=h_scrollbar.set,
        show="tree headings"
    )
    
    v_scrollbar.config(command=tree.yview)
    h_scrollbar.config(command=tree.xview)
    
    # Define column headings and widths
    for col_name, col_width in zip(col_names, col_widths):
        tree.column(col_name, width=col_width, anchor="center")
        tree.heading(col_name, text=col_name, anchor="center")
    
    # Grid layout
    tree.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")
    
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    
    return table_frame, tree


def insert_table_row(tree, values):
    """Insert a row into the table."""
    tree.insert("", "end", values=values)


def get_table_selection(tree):
    """Get the selected row from the table."""
    selection = tree.selection()
    if selection:
        item = selection[0]
        return tree.item(item, "values")
    return None


def clear_table(tree):
    """Clear all rows from the table."""
    for item in tree.get_children():
        tree.delete(item)
