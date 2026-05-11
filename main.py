"""Mobile Phone Store System - Main Entry Point."""
import customtkinter as ctk
from frontend.login_window import LoginWindow
from frontend.dashboard import Dashboard
from utils.constants import ACTIVE_THEME


class App:
    def __init__(self):
        """Initialize the application."""
        self.root = ctk.CTk()
        self.root.configure(fg_color=ACTIVE_THEME["background"])
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.show_login()
    
    def show_login(self):
        """Show login window."""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        LoginWindow(self.root, self.show_dashboard)
    
    def show_dashboard(self):
        """Show dashboard after successful login."""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        Dashboard(self.root)
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
