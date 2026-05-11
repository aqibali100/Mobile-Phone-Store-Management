"""Modern Dashboard Window using CustomTkinter."""
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from frontend.components.buttons import (
    create_primary_button, create_secondary_button, create_danger_button
)
from frontend.components.image_display import create_phone_image_label
from frontend.add_phone_window import AddPhoneWindow
from frontend.view_phone_window import ViewPhoneWindow
from frontend.search_phone_window import SearchPhoneWindow
from frontend.update_phone_window import UpdatePhoneWindow
from frontend.sales_report_window import SalesReportWindow
from backend.phone_manager import list_phones, delete_phone
from utils.constants import (
    ACTIVE_THEME, WINDOW_WIDTH, WINDOW_HEIGHT, PADDING,
    FONT_LARGE, FONT_MEDIUM, FONT_SMALL, LOW_STOCK_THRESHOLD
)


class Dashboard:
    def __init__(self, root):
        """Initialize the dashboard."""
        self.root = root
        self.root.title("Mobile Phone Store - Dashboard")
        self.root.geometry("1000x650")
        self.root.configure(fg_color=ACTIVE_THEME["background"])

        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"+{x}+{y}")

        self.setup_ui()
        self.update_stats()
    
    def setup_ui(self):
        """Setup the dashboard UI with search and table."""
        # Header
        header_frame = ctk.CTkFrame(
            self.root,
            fg_color=ACTIVE_THEME["surface"],
            height=80
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Dashboard - Mobile Phone Store Management",
            font=FONT_LARGE,
            text_color=ACTIVE_THEME["accent"]
        )
        title_label.pack(pady=10, anchor="w", padx=PADDING)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(
            header_frame,
            fg_color=ACTIVE_THEME["primary"],
            corner_radius=8
        )
        stats_frame.pack(fill="x", padx=PADDING, pady=(0, 10))
        
        # Stock stats
        self.stock_label = ctk.CTkLabel(
            stats_frame,
            text="Total Stock: 0",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["accent"]
        )
        self.stock_label.pack(side="left", padx=20, pady=10)
        
        # Low stock warning
        self.warning_label = ctk.CTkLabel(
            stats_frame,
            text="Low Stock Items: 0",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["warning"]
        )
        self.warning_label.pack(side="left", padx=20, pady=10)
        
        # Total items
        self.items_label = ctk.CTkLabel(
            stats_frame,
            text="Total Items: 0",
            font=FONT_MEDIUM,
            text_color=ACTIVE_THEME["text"]
        )
        self.items_label.pack(side="left", padx=20, pady=10)
        
        # Main content area
        content_frame = ctk.CTkFrame(
            self.root,
            fg_color=ACTIVE_THEME["background"]
        )
        content_frame.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)
        
        # Top bar with search and action buttons
        top_bar = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 15))
        
        # Search bar
        search_label = ctk.CTkLabel(top_bar, text="Search:", font=FONT_MEDIUM, text_color=ACTIVE_THEME["text"])
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.filter_table)
        
        self.search_entry = ctk.CTkEntry(
            top_bar,
            textvariable=self.search_var,
            placeholder_text="Type to search by name, brand, or color...",
            height=35,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["primary"],
            border_color=ACTIVE_THEME["accent"],
            placeholder_text_color=ACTIVE_THEME["text_secondary"]
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # Action buttons
        add_btn = create_primary_button(top_bar, "➕ Add Phone", command=self.open_add_phone, width=120)
        add_btn.pack(side="right", padx=(10, 0))
        
        report_btn = create_secondary_button(top_bar, "Report", command=self.open_sales_report, width=100)
        report_btn.pack(side="right", padx=(10, 0))
        
        # Table frame with scrollbar
        table_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)
        
        # Create Treeview with columns (show Sr# instead of internal id)
        columns = ("Sr#", "Name", "Brand", "Price", "RAM", "Storage", "Color", "Quantity", "Actions")
        
        # Configure style for treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                       background=ACTIVE_THEME["primary"],
                       foreground=ACTIVE_THEME["text"],
                       fieldbackground=ACTIVE_THEME["primary"],
                       borderwidth=0)
        style.map('Treeview', background=[('selected', ACTIVE_THEME["accent"])])
        
        style.configure("Treeview.Heading",
                       background=ACTIVE_THEME["surface"],
                       foreground=ACTIVE_THEME["accent"],
                       borderwidth=1)
        style.map("Treeview.Heading", background=[('active', ACTIVE_THEME["accent"])])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=18,
            yscrollcommand=scrollbar.set,
            show="headings"
        )
        scrollbar.config(command=self.tree.yview)
        
        # Define column headings and widths
        col_widths = {"Sr#": 50, "Name": 100, "Brand": 80, "Price": 70, "RAM": 50, "Storage": 70, "Color": 70, "Quantity": 70, "Actions": 140}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 80), anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Bind click/double-click to handle actions or view
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        
        # Footer with logout button
        footer_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        footer_frame.pack(fill="x", padx=PADDING, pady=(0, PADDING))
        
        exit_btn = create_danger_button(
            footer_frame,
            "Log out",
            command=self.root.quit,
            width=200
        )
        exit_btn.pack(side="right")
        
        # Load initial table data
        self.refresh_table()

    
    def update_stats(self):
        """Update the statistics display."""
        phones = list_phones()
        total_qty = sum(int(p.get("quantity", 0)) for p in phones)
        low_stock = sum(1 for p in phones if int(p.get("quantity", 0)) < LOW_STOCK_THRESHOLD)
        
        self.stock_label.configure(text=f"Total Stock: {total_qty}")
        self.warning_label.configure(text=f"Low Stock Items: {low_stock}")
        self.items_label.configure(text=f"Total Items: {len(phones)}")

    
    def open_sales_report(self):
        """Open sales report window."""
        window = ctk.CTkToplevel(self.root)
        SalesReportWindow(window)
    
    def on_action_complete(self):
        """Called when an action completes."""
        self.update_stats()
        self.refresh_table()
    
    def refresh_table(self):
        """Refresh the phone table with all data."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add phones to table
        phones = list_phones()
        for idx, phone in enumerate(phones, start=1):
            values = (
                idx,
                phone.get("name", ""),
                phone.get("brand", ""),
                f"${phone.get('price', '0')}",
                f"{phone.get('ram', '')}GB",
                f"{phone.get('storage', '')}GB",
                phone.get("color", ""),
                phone.get("quantity", ""),
                "View | Update | Delete"
            )
            # Insert and attach the real phone id as a tag for lookup
            item = self.tree.insert("", "end", values=values)
            try:
                self.tree.item(item, tags=(str(phone.get("id")),))
            except Exception:
                pass
    
    def filter_table(self, *args):
        """Filter table based on search query."""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered phones
        phones = list_phones()
        display_idx = 1
        for phone in phones:
            name = phone.get("name", "").lower()
            brand = phone.get("brand", "").lower()
            color = phone.get("color", "").lower()
            
            if search_term in name or search_term in brand or search_term in color:
                values = (
                    display_idx,
                    phone.get("name", ""),
                    phone.get("brand", ""),
                    f"${phone.get('price', '0')}",
                    f"{phone.get('ram', '')}GB",
                    f"{phone.get('storage', '')}GB",
                    phone.get("color", ""),
                    phone.get("quantity", ""),
                    "View | Update | Delete"
                )
                item = self.tree.insert("", "end", values=values)
                try:
                    self.tree.item(item, tags=(str(phone.get("id")),))
                except Exception:
                    pass
                display_idx += 1

    def on_tree_click(self, event):
        """Handle single-click: if Actions column clicked, show menu; else select row."""
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        col = self.tree.identify_column(event.x)  # e.g. '#1'..'#9'
        row = self.tree.identify_row(event.y)
        if not row:
            return

        try:
            tags = self.tree.item(row).get("tags", [])
            phone_id = tags[0] if tags else None
        except Exception:
            return

        phones = list_phones()
        phone = next((p for p in phones if str(p.get("id")) == str(phone_id)), None)
        if not phone:
            return

        # If Actions column (last column) clicked
        if col == f"#{len(self.tree['columns'])}":
            self.show_action_menu(phone)
        else:
            # just select/highlight the row
            self.tree.selection_set(row)

    def on_tree_double_click(self, event):
        """Handle double-click on tree item: open view details."""
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        row = self.tree.identify_row(event.y)
        if not row:
            return

        try:
            tags = self.tree.item(row).get("tags", [])
            phone_id = tags[0] if tags else None
        except Exception:
            phone_id = None

        if not phone_id:
            return

        phones = list_phones()
        phone = next((p for p in phones if str(p.get("id")) == str(phone_id)), None)
        if phone:
            self.view_phone_details(phone)

    def show_action_menu(self, phone):
        """Show small action menu for a phone (View/Edit/Delete)."""
        menu = ctk.CTkToplevel(self.root)
        menu.title("Actions")
        menu.geometry("260x160")
        menu.resizable(False, False)
        # Center the actions modal relative to the main window
        try:
            menu.update_idletasks()
            mwx = self.root.winfo_rootx()
            mwy = self.root.winfo_rooty()
            mww = self.root.winfo_width()
            mwh = self.root.winfo_height()
            ww = 260
            wh = 240
            x = mwx + (mww // 2) - (ww // 2)
            y = mwy + (mwh // 2) - (wh // 2)
            menu.geometry(f"{ww}x{wh}+{x}+{y}")
        except Exception:
            pass
        menu.transient(self.root)
        menu.grab_set()

        label = ctk.CTkLabel(menu, text=f"Actions for {phone.get('name')}", font=FONT_MEDIUM, text_color=ACTIVE_THEME['accent'])
        label.pack(pady=10)

        btn_frame = ctk.CTkFrame(menu, fg_color="transparent")
        btn_frame.pack(fill="both", expand=True, padx=10, pady=5)

        view_btn = create_secondary_button(btn_frame, "View Details", command=lambda: (menu.destroy(), self.view_phone_details(phone)), width=220)
        view_btn.pack(pady=6)

        edit_btn = create_secondary_button(btn_frame, "Update Phone", command=lambda: (menu.destroy(), self.edit_phone(phone)), width=220)
        edit_btn.pack(pady=6)

        del_btn = create_danger_button(btn_frame, "Delete Phone", command=lambda: (menu.destroy(), self.delete_phone_confirm(phone)), width=220)
        del_btn.pack(pady=6)

    def view_phone_details(self, phone):
        """Open a simple modal showing details of a single phone."""
        win = ctk.CTkToplevel(self.root)
        win.title(f"View - {phone.get('name')}")
        win.geometry("520x650")
        win.configure(fg_color=ACTIVE_THEME['background'])
        # center view modal relative to main window
        try:
            win.update_idletasks()
            mwx = self.root.winfo_rootx()
            mwy = self.root.winfo_rooty()
            mww = self.root.winfo_width()
            mwh = self.root.winfo_height()
            ww = 520
            wh = 650
            x = mwx + (mww // 2) - (ww // 2)
            y = mwy + (mwh // 2) - (wh // 2)
            win.geometry(f"{ww}x{wh}+{x}+{y}")
        except Exception:
            pass
        win.transient(self.root)
        win.grab_set()

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
            ("Price", f"${phone.get('price')}") ,
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

    def edit_phone(self, phone):
        """Open UpdatePhoneWindow preselected for this phone."""
        win = ctk.CTkToplevel(self.root)
        UpdatePhoneWindow(win, self.on_action_complete, phone=phone)

    def delete_phone_confirm(self, phone):
        """Confirm and delete phone using backend.delete_phone."""
        if not messagebox.askyesno("Confirm Delete", f"Delete {phone.get('name')} (ID {phone.get('id')})?"):
            return
        try:
            delete_phone(phone.get('id'))
            messagebox.showinfo("Deleted", "Phone deleted successfully")
            self.refresh_table()
            self.update_stats()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {str(e)}")
    
    def open_add_phone(self):
        """Open add phone window."""
        window = ctk.CTkToplevel(self.root)
        AddPhoneWindow(window, self.on_action_complete)
    
    def open_view_phones(self):
        """Open view phones window."""
        window = ctk.CTkToplevel(self.root)
        ViewPhoneWindow(window, self.on_action_complete)
    
    def open_search_phone(self):
        """Open search phone window."""
        window = ctk.CTkToplevel(self.root)
        SearchPhoneWindow(window, self.on_action_complete)
    
    def open_update_phone(self):
        """Open update phone window."""
        window = ctk.CTkToplevel(self.root)
        UpdatePhoneWindow(window, self.on_action_complete)
    
    def open_sales_report(self):
        """Open sales report window."""
        window = ctk.CTkToplevel(self.root)
        SalesReportWindow(window)
