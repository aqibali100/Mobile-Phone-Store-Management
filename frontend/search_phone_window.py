"""Search Phone Window using CustomTkinter."""
import customtkinter as ctk
from backend.file_handler import read_json
from frontend.components.buttons import create_primary_button, create_secondary_button
from frontend.components.tables import create_table, clear_table, insert_table_row
from frontend.components.message_boxes import show_error
from utils.constants import (
    ACTIVE_THEME, PADDING, FONT_MEDIUM, FONT_SMALL,
    PHONES_FILE
)


class SearchPhoneWindow:
    def __init__(self, window, on_complete):
        """Initialize search phone window."""
        self.window = window
        self.on_complete = on_complete
        self.window.title("Search Phone")
        self.window.geometry("900x650")
        self.window.configure(fg_color=ACTIVE_THEME["background"])
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the search phone UI."""
        # Header
        header_frame = ctk.CTkFrame(
            self.window,
            fg_color=ACTIVE_THEME["surface"],
            corner_radius=8
        )
        header_frame.pack(fill="x", padx=PADDING, pady=PADDING)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔍 Search Phones",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["accent"]
        )
        title_label.pack(pady=(10, 5), padx=PADDING, anchor="w")
        
        # Search options
        search_options_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_options_frame.pack(fill="x", padx=PADDING, pady=(0, 10))
        
        # Search by label
        search_label = ctk.CTkLabel(
            search_options_frame,
            text="Search by:",
            font=FONT_SMALL,
            text_color=ACTIVE_THEME["text"]
        )
        search_label.pack(side="left", padx=(0, 10))
        
        # Radio buttons
        self.search_type = ctk.StringVar(value="name")
        
        name_radio = ctk.CTkRadioButton(
            search_options_frame,
            text="Name",
            variable=self.search_type,
            value="name",
            text_color=ACTIVE_THEME["text"]
        )
        name_radio.pack(side="left", padx=(0, 20))
        
        brand_radio = ctk.CTkRadioButton(
            search_options_frame,
            text="Brand",
            variable=self.search_type,
            value="brand",
            text_color=ACTIVE_THEME["text"]
        )
        brand_radio.pack(side="left")
        
        # Search box
        search_box_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_box_frame.pack(fill="x", padx=PADDING, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_box_frame,
            placeholder_text="Enter search term...",
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["background"],
            border_color=ACTIVE_THEME["accent"],
            text_color=ACTIVE_THEME["text"],
            placeholder_text_color=ACTIVE_THEME["text_secondary"],
            height=35
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        search_btn = create_primary_button(
            search_box_frame,
            "Search",
            command=self.perform_search,
            width=100
        )
        search_btn.pack(side="left")
        
        # Results label
        self.results_label = ctk.CTkLabel(
            header_frame,
            text="Results: 0",
            font=FONT_SMALL,
            text_color=ACTIVE_THEME["text_secondary"]
        )
        self.results_label.pack(anchor="w", padx=PADDING, pady=(0, 10))
        
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
    
    def perform_search(self):
        """Perform the search."""
        search_term = self.search_entry.get().strip().lower()
        search_by = self.search_type.get()
        
        if not search_term:
            show_error("Input Error", "Please enter a search term")
            return
        
        phones = read_json(str(PHONES_FILE)) or []
        
        # Filter phones
        results = []
        if search_by == "name":
            results = [p for p in phones if search_term in p.get("name", "").lower()]
        elif search_by == "brand":
            results = [p for p in phones if search_term in p.get("brand", "").lower()]
        
        # Clear and populate table
        clear_table(self.tree)
        
        if not results:
            self.results_label.configure(text="Results: 0")
            return
        
        for phone in results:
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
        
        self.results_label.configure(text=f"Results: {len(results)}")
