"""Modern Login Window (redesigned).

This login uses email + password and authenticates only users with role
`admin`. It performs input validation and shows clear error messages.
"""
import customtkinter as ctk
from frontend.components.message_boxes import show_error, show_info
from backend import auth
from utils.validators import validate_email
from utils.constants import ACTIVE_THEME, FONT_LARGE, FONT_MEDIUM, FONT_SMALL, PADDING


class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Mobile Phone Store - Login")
        self.root.geometry("520x400")
        self.root.resizable(True, True)
        self.root.configure(fg_color=ACTIVE_THEME["background"])

        # Center
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (520 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"+{x}+{y}")

        self.setup_ui()

    def setup_ui(self):
        main = ctk.CTkFrame(self.root, fg_color=ACTIVE_THEME["surface"], corner_radius=12)
        main.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Header with icon and title
        header = ctk.CTkFrame(main, fg_color=ACTIVE_THEME["surface"], corner_radius=8)
        header.pack(fill="x", pady=(0, 20), padx=20)

        # Title
        title = ctk.CTkLabel(header, text="Mobile Phone Store", font=FONT_LARGE, text_color=ACTIVE_THEME["accent"])
        title.pack(side="left", pady=15)

        # Form
        form = ctk.CTkFrame(main, fg_color=ACTIVE_THEME["background"])
        form.pack(fill="both", expand=True, padx=20, pady=10)

        # Email
        email_label = ctk.CTkLabel(form, text="Email", font=FONT_MEDIUM, text_color=ACTIVE_THEME["text"])
        email_label.pack(anchor="w", pady=(20, 6))
        # Use background color for entry so it blends (no dark box behind text)
        self.email_entry = ctk.CTkEntry(
            form,
            placeholder_text="you@example.com",
            height=38,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["background"],
            border_color=ACTIVE_THEME["accent"],
            placeholder_text_color=ACTIVE_THEME["text_secondary"]
        )
        self.email_entry.pack(fill="x")

        # Password
        pwd_label = ctk.CTkLabel(form, text="Password", font=FONT_MEDIUM, text_color=ACTIVE_THEME["text"])
        pwd_label.pack(anchor="w", pady=(12, 6))
        self.pwd_entry = ctk.CTkEntry(
            form,
            placeholder_text="Enter password",
            show="•",
            height=38,
            font=FONT_SMALL,
            fg_color=ACTIVE_THEME["background"],
            border_color=ACTIVE_THEME["accent"],
            placeholder_text_color=ACTIVE_THEME["text_secondary"]
        )
        self.pwd_entry.pack(fill="x")

        # Buttons
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=25)

        login_btn = ctk.CTkButton(btn_frame, text="Login", command=self.handle_login, fg_color=ACTIVE_THEME["accent"],
                                  hover_color="#00b8d4", font=FONT_MEDIUM, height=45)
        login_btn.pack(fill="x", padx=(0, 0))

        # Bind Enter key to login
        self.email_entry.bind("<Return>", lambda e: self.handle_login())
        self.pwd_entry.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.pwd_entry.get().strip()

        # Validate
        if not email or not password:
            show_error("Validation Error", "Please enter both email and password")
            return

        if not validate_email(email):
            show_error("Validation Error", "Please enter a valid email address")
            return

        try:
            result = auth.authenticate_user(email, password)
            if not result.get("ok"):
                show_error("Login Failed", result.get("message", "Authentication failed"))
                return

            show_info("Success", "Login successful — welcome!")
            self.on_login_success()

        except Exception as e:
            show_error("Error", f"An unexpected error occurred: {str(e)}")
