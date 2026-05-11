"""Update Phone Window using CustomTkinter."""
import customtkinter as ctk
from backend.file_handler import read_json, write_json
from frontend.components.buttons import create_primary_button, create_danger_button
from frontend.components.message_boxes import show_error, show_success
from utils.constants import (
    ACTIVE_THEME, PADDING, FONT_MEDIUM, FONT_SMALL,
    PHONES_FILE
)


class UpdatePhoneWindow:
    def __init__(self, window, on_complete, phone=None):
        """Initialize update phone window."""
        self.window = window
        self.on_complete = on_complete
        self.preselect_phone = phone
        self.window.title("Update Phone Price")
        self.window.geometry("600x500")
        # center this to screen
        try:
            self.window.update_idletasks()
            sw = self.window.winfo_screenwidth()
            sh = self.window.winfo_screenheight()
            w = 600
            h = 500
            x = (sw // 2) - (w // 2)
            y = (sh // 2) - (h // 2)
            self.window.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass
        self.window.configure(fg_color=ACTIVE_THEME["background"])
        self.window.resizable(True, True)
        
        self.selected_phone = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the update phone UI."""
        # Main container
        main_frame = ctk.CTkScrollableFrame(
            self.window,
            fg_color=ACTIVE_THEME["background"]
        )
        main_frame.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Update Phone Price",
            font=("Segoe UI", 16, "bold"),
            text_color=ACTIVE_THEME["accent"]
        )
        title_label.pack(pady=(0, 20))
        
        # Select phone section
        select_label = ctk.CTkLabel(
            main_frame,
            text="Select Phone",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["text"]
        )
        select_label.pack(anchor="w", pady=(10, 5))
        
        # Load phones and create dropdown
        self.phones = read_json(str(PHONES_FILE)) or []
        phone_options = [f"{p.get('id')} - {p.get('name')} ({p.get('brand')})" for p in self.phones]
        
        self.phone_combo = ctk.CTkComboBox(
            main_frame,
            values=phone_options if phone_options else ["No phones available"],
            state="readonly",
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["surface"],
            border_color=ACTIVE_THEME["accent"],
            text_color=ACTIVE_THEME["text"],
            dropdown_text_color=ACTIVE_THEME["text"],
            button_color=ACTIVE_THEME["accent"],
            dropdown_fg_color=ACTIVE_THEME["surface"],
            height=40
        )
        self.phone_combo.pack(fill="x", pady=(0, 20))
        self.phone_combo.bind("<<ComboboxSelected>>", lambda e: self.on_phone_selected(self.phones))
        
        # Phone info section
        info_frame = ctk.CTkFrame(
            main_frame,
            fg_color=ACTIVE_THEME["surface"],
            corner_radius=8
        )
        info_frame.pack(fill="x", pady=(0, 20))
        
        # Current price
        current_price_label = ctk.CTkLabel(
            info_frame,
            text="Current Price",
            font=FONT_SMALL,
            text_color=ACTIVE_THEME["text_secondary"]
        )
        current_price_label.pack(anchor="w", padx=PADDING, pady=(10, 2))
        
        self.current_price_display = ctk.CTkLabel(
            info_frame,
            text="$0.00",
            font=("Segoe UI", 14, "bold"),
            text_color=ACTIVE_THEME["accent"]
        )
        self.current_price_display.pack(anchor="w", padx=PADDING, pady=(0, 10))

        # If a phone was provided to preselect, set the combo and show current price
        if self.preselect_phone:
            try:
                sel = f"{self.preselect_phone.get('id')} - {self.preselect_phone.get('name')} ({self.preselect_phone.get('brand')})"
                # set combo if available
                try:
                    if sel in phone_options:
                        self.phone_combo.set(sel)
                except Exception:
                    pass
                # set selected phone and update display
                self.selected_phone = self.preselect_phone
                self.current_price_display.configure(text=f"${self.selected_phone.get('price', 0):.2f}")
            except Exception:
                pass
        
        # New price input
        new_price_label = ctk.CTkLabel(
            main_frame,
            text="New Price ($)",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["text"]
        )
        new_price_label.pack(anchor="w", pady=(10, 5))
        
        self.price_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter new price",
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["surface"],
            border_color=ACTIVE_THEME["accent"],
            text_color=ACTIVE_THEME["text"],
            placeholder_text_color=ACTIVE_THEME["text_secondary"],
            height=40
        )
        self.price_entry.pack(fill="x", pady=(0, 30))

        # Button frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        
        # Update button (right-most)
        update_btn = create_primary_button(
            button_frame,
            "Update Price",
            command=self.update_price,
            width=250
        )
        update_btn.pack(side="right", padx=(0, 10))

        # Cancel button (to the left of Update, both right-aligned)
        cancel_btn = create_danger_button(
            button_frame,
            "Cancel",
            command=self.window.destroy,
            width=250
        )
        cancel_btn.pack(side="right")
    
    def on_phone_selected(self, phones):
        """Handle phone selection."""
        selected = self.phone_combo.get()
        if not selected or selected == "No phones available":
            return
        
        # Extract phone ID from selection
        phone_id = int(selected.split(" - ")[0])
        
        # Find phone
        for phone in phones:
            if phone.get("id") == phone_id:
                self.selected_phone = phone
                self.current_price_display.configure(
                    text=f"${phone.get('price', 0):.2f}"
                )
                self.price_entry.delete(0, "end")
                return
    
    def update_price(self):
        """Update the phone price."""
        if not self.selected_phone:
            show_error("Selection Error", "Please select a phone first")
            return
        
        new_price = self.price_entry.get().strip()
        
        if not new_price:
            show_error("Input Error", "Please enter a new price")
            return
        
        try:
            new_price = float(new_price)
            
            if new_price < 0:
                show_error("Input Error", "Price cannot be negative")
                return
            
            # Read, update, and save
            phones = read_json(str(PHONES_FILE)) or []
            
            for phone in phones:
                if phone.get("id") == self.selected_phone.get("id"):
                    old_price = phone.get("price")
                    phone["price"] = new_price
                    break
            
            write_json(str(PHONES_FILE), phones)
            
            show_success(
                self.window,
                f"Price updated from ${old_price:.2f} to ${new_price:.2f}"
            )
            
            self.window.after(1500, self.close_window)
            
        except ValueError:
            show_error("Input Error", "Please enter a valid price number")
    
    def close_window(self):
        """Close window and notify completion."""
        self.on_complete()
        self.window.destroy()
