"""View All Phones Window using CustomTkinter."""
import customtkinter as ctk
from backend.phone_manager import list_phones
from backend.file_handler import read_json, write_json
from frontend.components.tables import create_table, clear_table, insert_table_row, get_table_selection
from frontend.components.buttons import create_danger_button
from frontend.components.image_display import create_phone_image_label
from frontend.components.message_boxes import show_error, ask_confirmation, show_success
from utils.constants import (
    ACTIVE_THEME, PADDING, FONT_MEDIUM, FONT_SMALL,
    PHONES_FILE
)


class ViewPhoneWindow:
    def __init__(self, window, on_complete):
        """Initialize view phones window."""
        self.window = window
        self.on_complete = on_complete
        self.window.title("View All Phones")
        self.window.geometry("1000x600")
        self.window.configure(fg_color=ACTIVE_THEME["background"])
        
        self.setup_ui()
        self.load_phones()
    
    def setup_ui(self):
        """Setup the view phones UI."""
        # Header
        header_frame = ctk.CTkFrame(
            self.window,
            fg_color=ACTIVE_THEME["surface"],
            corner_radius=8
        )
        header_frame.pack(fill="x", padx=PADDING, pady=PADDING)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👁️ View All Phones",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["accent"]
        )
        title_label.pack(pady=10, padx=PADDING, anchor="w")
        
        # Table container
        table_frame = ctk.CTkFrame(self.window, fg_color=ACTIVE_THEME["background"])
        table_frame.pack(fill="both", expand=True, padx=PADDING, pady=(0, PADDING))
        
        # Create table
        columns = [
            ("ID", 40),
            ("Name", 120),
            ("Brand", 100),
            ("Price", 80),
            ("RAM", 60),
            ("Storage", 80),
            ("Color", 80),
            ("Quantity", 70)
        ]
        
        self.table_frame, self.tree = create_table(table_frame, columns, height=15)
        self.table_frame.pack(fill="both", expand=True)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        button_frame.pack(fill="x", padx=PADDING, pady=(0, PADDING))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            command=self.load_phones,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["secondary"],
            text_color=ACTIVE_THEME["text"],
            width=150
        )
        refresh_btn.pack(side="left", padx=(0, 10))
        
        # View details button
        view_btn = ctk.CTkButton(
            button_frame,
            text="👁️ View Details",
            command=self.view_phone_details,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["secondary"],
            text_color=ACTIVE_THEME["text"],
            width=150
        )
        view_btn.pack(side="left", padx=(0, 10))
        
        # Delete button
        delete_btn = create_danger_button(
            button_frame,
            "🗑️ Delete Selected",
            command=self.delete_phone,
            width=150
        )
        delete_btn.pack(side="left")
        
        # Close button
        close_btn = ctk.CTkButton(
            button_frame,
            text="✖️ Close",
            command=self.window.destroy,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["primary"],
            text_color=ACTIVE_THEME["text"],
            width=150
        )
        close_btn.pack(side="right")
    
    def load_phones(self):
        """Load and display all phones."""
        clear_table(self.tree)
        
        phones = read_json(str(PHONES_FILE)) or []
        
        if not phones:
            # Show empty message
            insert_table_row(self.tree, ("No phones in inventory", "", "", "", "", "", "", ""))
            return
        
        for phone in phones:
            row = (
                str(phone.get("id", "")),
                phone.get("name", ""),
                phone.get("brand", ""),
                f"${phone.get('price', 0):.2f}",
                f"{phone.get('ram', 0)}GB",
                f"{phone.get('storage', 0)}GB",
                phone.get("color", ""),
                str(phone.get("quantity", 0))
            )
            insert_table_row(self.tree, row)
    
    def delete_phone(self):
        """Delete selected phone."""
        selection = get_table_selection(self.tree)
        
        if not selection:
            show_error("Selection Error", "Please select a phone to delete")
            return
        
        phone_id = int(selection[0])
        
        # Confirm deletion
        if not ask_confirmation("Confirm Delete", f"Are you sure you want to delete phone ID {phone_id}?"):
            return
        
        try:
            phones = read_json(str(PHONES_FILE)) or []
            phones = [p for p in phones if p.get("id") != phone_id]
            write_json(str(PHONES_FILE), phones)
            
            show_success(self.window, "Phone deleted successfully!")
            self.load_phones()
            self.on_complete()
            
        except Exception as e:
            show_error("Error", f"Failed to delete phone: {str(e)}")
    
    def view_phone_details(self):
        """View details of selected phone with image."""
        selection = get_table_selection(self.tree)
        
        if not selection:
            show_error("Selection Error", "Please select a phone to view")
            return
        
        phone_id = int(selection[0])
        phones = read_json(str(PHONES_FILE)) or []
        phone = next((p for p in phones if p.get("id") == phone_id), None)
        
        if not phone:
            show_error("Error", "Phone not found")
            return
        
        # Open details window
        win = ctk.CTkToplevel(self.window)
        win.title(f"Details - {phone.get('name')}")
        win.geometry("520x650")
        win.configure(fg_color=ACTIVE_THEME['background'])
        
        # Center the window
        try:
            win.update_idletasks()
            x = (win.winfo_screenwidth() // 2) - (520 // 2)
            y = (win.winfo_screenheight() // 2) - (650 // 2)
            win.geometry(f"+{x}+{y}")
        except Exception:
            pass
        
        # Main scrollable frame
        main_scroll = ctk.CTkScrollableFrame(win, fg_color=ACTIVE_THEME['background'])
        main_scroll.pack(fill='both', expand=True, padx=PADDING, pady=PADDING)

        # Image section (if available)
        image_path = phone.get('image_path')
        if image_path:
            try:
                img_label = create_phone_image_label(main_scroll, image_path, width=280, height=280)
                if img_label:
                    img_label.pack(pady=(0, 20))
            except Exception:
                pass

        # Phone details
        info_frame = ctk.CTkFrame(main_scroll, fg_color=ACTIVE_THEME['surface'], corner_radius=8)
        info_frame.pack(fill='x', pady=(0, 10))

        fields = [
            ("ID", phone.get('id')),
            ("Name", phone.get('name')),
            ("Brand", phone.get('brand')),
            ("Price", f"${phone.get('price', 0):.2f}"),
            ("RAM", f"{phone.get('ram')} GB"),
            ("Storage", f"{phone.get('storage')} GB"),
            ("Color", phone.get('color')),
            ("Quantity", phone.get('quantity')),
        ]

        for label, val in fields:
            l = ctk.CTkLabel(info_frame, text=f"{label}: {val}", font=FONT_SMALL, text_color=ACTIVE_THEME['text'])
            l.pack(anchor='w', pady=6, padx=8)

        close_btn = ctk.CTkButton(win, text='Close', command=win.destroy, fg_color=ACTIVE_THEME['accent'])
        close_btn.pack(pady=10)
