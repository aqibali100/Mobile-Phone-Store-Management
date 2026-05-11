"""Add New Phone Window using CustomTkinter."""
import customtkinter as ctk
from tkinter import filedialog
import shutil
import os
from backend.phone_manager import add_phone, list_phones
from backend.file_handler import read_json, write_json
from frontend.components.buttons import create_primary_button, create_danger_button
from frontend.components.message_boxes import show_error, show_success
from utils.constants import (
    ACTIVE_THEME, PADDING, FONT_MEDIUM, FONT_SMALL,
    PHONES_FILE, PHONE_IMAGES_DIR
)


class AddPhoneWindow:
    def __init__(self, window, on_complete):
        """Initialize add phone window."""
        self.window = window
        self.on_complete = on_complete
        self.window.title("Add New Phone")
        self.window.geometry("600x800")
        self.window.configure(fg_color=ACTIVE_THEME["background"])
        self.window.resizable(True, True)
        
        self.selected_image_path = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the add phone form."""
        # Main container
        main_frame = ctk.CTkScrollableFrame(
            self.window,
            fg_color=ACTIVE_THEME["background"]
        )
        main_frame.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Add New Phone",
            font=("Segoe UI", 16, "bold"),
            text_color=ACTIVE_THEME["accent"]
        )
        title_label.pack(pady=(0, 20))
        
        # Phone Name
        self.create_form_field(main_frame, "Phone Name", "name_entry")
        
        # Brand
        self.create_form_field(main_frame, "Brand", "brand_entry")
        
        # Price
        self.create_form_field(main_frame, "Price ($)", "price_entry")
        
        # RAM
        self.create_form_field(main_frame, "RAM (GB)", "ram_entry")
        
        # Storage
        self.create_form_field(main_frame, "Storage (GB)", "storage_entry")
        
        # Color
        self.create_form_field(main_frame, "Color", "color_entry")
        
        # Quantity
        self.create_form_field(main_frame, "Quantity", "quantity_entry")
        
        # Image upload section
        image_label = ctk.CTkLabel(
            main_frame,
            text="Phone Image (Optional)",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["accent"]
        )
        image_label.pack(anchor="w", pady=(20, 10))
        
        image_btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        image_btn_frame.pack(fill="x", pady=(0, 10))
        
        self.image_btn = ctk.CTkButton(
            image_btn_frame,
            text="📁 Choose Image",
            command=self.select_image,
            fg_color=ACTIVE_THEME["secondary"],
            text_color=ACTIVE_THEME["text"],
            font=FONT_SMALL
        )
        self.image_btn.pack(side="left", padx=(0, 10))
        
        self.image_status_label = ctk.CTkLabel(
            image_btn_frame,
            text="No image selected",
            font=FONT_SMALL,
            text_color=ACTIVE_THEME["text_secondary"]
        )
        self.image_status_label.pack(side="left")
        
        # Button frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))

        # Save button - right side
        save_btn = create_primary_button(
            button_frame,
            "Save Phone",
            command=self.save_phone,
            width=250
        )
        save_btn.pack(side="right")

        # Cancel button - left of save
        cancel_btn = create_danger_button(
            button_frame,
            "Cancel",
            command=self.window.destroy,
            width=250
        )
        cancel_btn.pack(side="right", padx=(0, 10))
    
    def create_form_field(self, parent, label_text, attr_name):
        """Create a form field with label and entry."""
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["text"]
        )
        label.pack(anchor="w", pady=(10, 5))
        
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=f"Enter {label_text.lower()}",
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["surface"],
            border_color=ACTIVE_THEME["accent"],
            text_color=ACTIVE_THEME["text"],
            placeholder_text_color=ACTIVE_THEME["text_secondary"],
            height=40
        )
        entry.pack(fill="x", pady=(0, 10))
        
        setattr(self, attr_name, entry)
    
    def select_image(self):
        """Open file dialog to select phone image."""
        file_path = filedialog.askopenfilename(
            title="Select Phone Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"), ("All files", "*.*")],
            initialdir=os.path.expanduser("~")
        )
        if file_path:
            self.selected_image_path = file_path
            filename = os.path.basename(file_path)
            self.image_status_label.configure(text=f"✓ {filename}")

    
    def save_phone(self):
        """Save the new phone to database."""
        # Validate inputs
        name = self.name_entry.get().strip()
        brand = self.brand_entry.get().strip()
        price = self.price_entry.get().strip()
        ram = self.ram_entry.get().strip()
        storage = self.storage_entry.get().strip()
        color = self.color_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        
        if not all([name, brand, price, ram, storage, color, quantity]):
            show_error("Validation Error", "All fields are required!")
            return
        
        try:
            # Get current phones and compute new unique id
            phones = list_phones() or []
            new_id = (max((p.get("id", 0) for p in phones), default=0) + 1)

            # Handle image if selected
            image_path = None
            if self.selected_image_path:
                try:
                    os.makedirs(PHONE_IMAGES_DIR, exist_ok=True)
                    ext = os.path.splitext(self.selected_image_path)[1]
                    image_filename = f"phone_{new_id}{ext}"
                    dest_path = os.path.join(PHONE_IMAGES_DIR, image_filename)
                    shutil.copy2(self.selected_image_path, dest_path)
                    image_path = dest_path
                except Exception as e:
                    show_error("Image Error", f"Failed to save image: {str(e)}")
                    return

            phone = {
                "id": new_id,
                "name": name,
                "brand": brand,
                "price": float(price),
                "ram": int(ram),
                "storage": int(storage),
                "color": color,
                "quantity": int(quantity),
                "image_path": image_path
            }

            # Persist via phone manager (which saves to JSON)
            add_phone(phone)

            # Notify and reset form for next entry
            show_success(self.window, f"Phone '{name}' added successfully!")
            # refresh parent lists / stats
            try:
                self.on_complete()
            except Exception:
                pass

            # Clear form fields
            self.name_entry.delete(0, "end")
            self.brand_entry.delete(0, "end")
            self.price_entry.delete(0, "end")
            self.ram_entry.delete(0, "end")
            self.storage_entry.delete(0, "end")
            self.color_entry.delete(0, "end")
            self.quantity_entry.delete(0, "end")
            self.selected_image_path = None
            self.image_status_label.configure(text="No image selected")
            self.name_entry.focus()

        except ValueError:
            show_error("Input Error", "Please enter valid numbers for Price, RAM, Storage, and Quantity")
    
    def close_window(self):
        """Close the window and notify completion."""
        self.on_complete()
        self.window.destroy()
