"""Sales Report Window using CustomTkinter."""
import customtkinter as ctk
from backend.file_handler import read_json
from backend.phone_manager import list_phones
from frontend.components.tables import create_table, clear_table, insert_table_row
from utils.constants import (
    ACTIVE_THEME, PADDING, FONT_MEDIUM, FONT_SMALL,
    PHONES_FILE
)


class SalesReportWindow:
    def __init__(self, window):
        """Initialize sales report window."""
        self.window = window
        self.window.title("Sales Report")
        self.window.geometry("1000x650")
        self.window.configure(fg_color=ACTIVE_THEME["background"])
        
        self.setup_ui()
        self.load_report()
    
    def setup_ui(self):
        """Setup the sales report UI."""
        # Header
        header_frame = ctk.CTkFrame(
            self.window,
            fg_color=ACTIVE_THEME["surface"],
            corner_radius=8
        )
        header_frame.pack(fill="x", padx=PADDING, pady=PADDING)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Sales Report",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["accent"]
        )
        title_label.pack(pady=10, padx=PADDING, anchor="w")
        
        # Stats
        stats_frame = ctk.CTkFrame(header_frame, fg_color=ACTIVE_THEME["primary"], corner_radius=8)
        stats_frame.pack(fill="x", padx=PADDING, pady=(0, 10))
        
        self.total_value_label = ctk.CTkLabel(
            stats_frame,
            text="Total Inventory Value: $0.00",
            font=FONT_SMALL,
            text_color=ACTIVE_THEME["accent"]
        )
        self.total_value_label.pack(side="left", padx=20, pady=10)
        
        self.total_phones_label = ctk.CTkLabel(
            stats_frame,
            text="Total Phones in Stock: 0",
            font=FONT_SMALL,
            text_color=ACTIVE_THEME["text"]
        )
        self.total_phones_label.pack(side="left", padx=20, pady=10)
        
        # Table container
        table_frame = ctk.CTkFrame(self.window, fg_color=ACTIVE_THEME["background"])
        table_frame.pack(fill="both", expand=True, padx=PADDING, pady=(0, PADDING))
        
        # Create table
        # Use Sr# for display instead of raw ID, widths chosen for readability
        columns = [
            ("Sr#", 40),
            ("Name", 180),
            ("Brand", 120),
            ("Price", 100),
            ("Quantity", 100),
            ("Total Value", 120),
        ]
        
        self.table_frame, self.tree = create_table(table_frame, columns, height=15)
        self.table_frame.pack(fill="both", expand=True)
        # Use heading-only mode (no tree column) so table content starts at left edge
        try:
            self.tree.configure(show="headings")
        except Exception:
            pass
        # Align certain columns: Name left-aligned and allowed to expand
        try:
            self.tree.column("Name", anchor="w", stretch=True)
            self.tree.column("Brand", anchor="w")
            self.tree.column("Price", anchor="e")
            self.tree.column("Quantity", anchor="center")
            self.tree.column("Total Value", anchor="e")
            # Make heading anchors match column alignment so headers
            # line up with their column contents (as in the screenshot)
            self.tree.heading("Name", anchor="w")
            self.tree.heading("Brand", anchor="w")
            self.tree.heading("Price", anchor="e")
            self.tree.heading("Quantity", anchor="center")
            self.tree.heading("Total Value", anchor="e")
        except Exception:
            pass
        
        # Button frame
        button_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        button_frame.pack(fill="x", padx=PADDING, pady=(0, PADDING))
        
        # Export button
        export_btn = ctk.CTkButton(
            button_frame,
            text="Export Report",
            command=self.export_report,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["secondary"],
            text_color=ACTIVE_THEME["text"],
            width=150
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.load_report,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["secondary"],
            text_color=ACTIVE_THEME["text"],
            width=150
        )
        refresh_btn.pack(side="left", padx=(0, 10))
        
        # Close button
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.window.destroy,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["primary"],
            text_color=ACTIVE_THEME["text"],
            width=150
        )
        close_btn.pack(side="right")
    
    def load_report(self):
        """Load and display sales report."""
        clear_table(self.tree)
        
        phones = list_phones() or []

        total_value = 0.0
        total_stock = 0

        for idx, phone in enumerate(phones, start=1):
            price = float(phone.get("price", 0) or 0)
            qty = int(phone.get("quantity", 0) or 0)
            total = price * qty

            total_value += total
            total_stock += qty

            row = (
                str(idx),
                phone.get("name", ""),
                phone.get("brand", ""),
                f"${price:.2f}",
                str(qty),
                f"${total:.2f}"
            )
            insert_table_row(self.tree, row)
        
        # Update stats
        self.total_value_label.configure(text=f"Total Inventory Value: ${total_value:.2f}")
        self.total_phones_label.configure(text=f"Total Phones in Stock: {total_stock}")
    
    def export_report(self):
        """Export report to file."""
        import csv
        from datetime import datetime
        
        try:
            phones = list_phones() or []

            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sales_report_{timestamp}.csv"
            # Save to user's Downloads folder if available
            try:
                from pathlib import Path
                downloads = Path.home() / "Downloads"
                downloads.mkdir(parents=True, exist_ok=True)
                filepath = downloads / filename
            except Exception:
                filepath = filename

            # Write CSV with proper formatting
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Sr#", "ID", "Name", "Brand", "Price", "Quantity", "Total Value"])

                for idx, phone in enumerate(phones, start=1):
                    price = float(phone.get("price", 0) or 0)
                    qty = int(phone.get("quantity", 0) or 0)
                    total = price * qty

                    writer.writerow([
                        idx,
                        phone.get("id"),
                        phone.get("name"),
                        phone.get("brand"),
                        f"{price:.2f}",
                        qty,
                        f"{total:.2f}"
                    ])
            
            from frontend.components.message_boxes import show_success
            show_success(self.window, f"{str(filename)} exported successfully!")
            
        except Exception as e:
            from frontend.components.message_boxes import show_error
            show_error("Export Error", f"Failed to export report: {str(e)}")
