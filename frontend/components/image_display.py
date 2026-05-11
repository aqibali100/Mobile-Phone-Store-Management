"""Image display helper for phone images using CTkImage."""
import customtkinter as ctk
from PIL import Image
from pathlib import Path
import os


def create_phone_image_label(parent, image_path, width=300, height=300):
    """
    Create a CTkLabel displaying a phone image.
    
    Args:
        parent: Parent CTk widget
        image_path: Path to the image file (str or Path)
        width: Display width (default 300)
        height: Display height (default 300)
    
    Returns:
        CTkLabel with the image, or None if image not found
    """
    if not image_path:
        return None
    
    try:
        image_path = Path(image_path)
        if not image_path.exists():
            return None
        
        # Open and resize image
        img = Image.open(image_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Convert to CTkImage
        ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(width, height))
        
        # Create label with image
        label = ctk.CTkLabel(
            parent,
            image=ctk_image,
            text="",
            fg_color="transparent"
        )
        label.image = ctk_image  # Keep a reference
        return label
    
    except Exception as e:
        # Image couldn't be loaded or processed
        return None
