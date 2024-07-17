import customtkinter as ctk
from PIL import Image
import os
from nda_reviewer.utils.icon_loader import load_svg_icon
from nda_reviewer.utils.secrets import get_secret, set_secret
from nda_reviewer.settings import OPENAI_API_KEY_NAME, FONT_FAMILY
import tkinter as tk
from tkinter import messagebox


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, backend):
        super().__init__(master)
        self.backend = backend
        self.button_config = {
            "font": ctk.CTkFont(family=FONT_FAMILY, size=13),
            "height": 25,
            "corner_radius": 3,
        }
        self.active_button_config = {
            "fg_color": "#1E90FF",
            "hover_color": "#4169E1",
        }
        self.inactive_button_config = {
            "fg_color": "#808080",
            "hover_color": "#808080",
            "state": "disabled",
        }
        self.completed_button_config = {
            "fg_color": "#28A745",
            "hover_color": "#218838",
            "state": "disabled",
        }
        self.create_widgets()

    def create_widgets(self):
        # ... (existing widgets)

        # Add a new frame for NDA-related buttons
        self.nda_frame = ctk.CTkFrame(self)
        self.nda_frame.grid(
            row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew"
        )

        # Upload NDA button
        self.upload_nda_button = ctk.CTkButton(
            self.nda_frame,
            text="Upload NDA",
            image=self.upload_icon,
            compound="left",
            command=self.upload_nda,
            **self.button_config,
            **self.active_button_config,
        )
        self.upload_nda_button.grid(row=0, column=0, padx=2, pady=(3, 3))

        # Upload Guidelines button
        self.upload_guidelines_button = ctk.CTkButton(
            self.nda_frame,
            text="Upload Guidelines",
            image=self.upload_icon,
            compound="left",
            command=self.upload_guidelines,
            **self.button_config,
            **self.inactive_button_config,
        )
        self.upload_guidelines_button.grid(row=0, column=1, padx=2, pady=(3, 3))

        # Analyze and Revise NDA button
        self.analyze_button = ctk.CTkButton(
            self.nda_frame,
            text="Revise NDA",
            image=self.edit_icon,
            compound="left",
            command=self.analyze_and_revise_nda,
            **self.button_config,
            **self.inactive_button_config,
        )
        self.analyze_button.grid(row=0, column=2, padx=2, pady=(3, 3))

        # Download Revised NDA button
        self.download_nda_button = ctk.CTkButton(
            self.nda_frame,
            text="Download Revised NDA",
            image=self.download_icon,
            compound="left",
            command=self.download_revised_nda,
            **self.button_config,
            **self.inactive_button_config,
        )
        self.download_nda_button.grid(row=0, column=3, padx=2, pady=(3, 3))

    def upload_nda(self):
        try:
            result = self.backend.upload_nda()
            tk.messagebox.showinfo("Upload NDA", result)
            if "successfully" in result:
                self.upload_nda_button.configure(**self.completed_button_config)
                self.upload_guidelines_button.configure(**self.active_button_config, state="normal")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def upload_guidelines(self):
        try:
            result = self.backend.upload_guidelines()
            tk.messagebox.showinfo("Upload Guidelines", result)
            if "successfully" in result:
                self.upload_guidelines_button.configure(**self.completed_button_config)
                self.analyze_button.configure(**self.active_button_config, state="normal")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def download_revised_nda(self):
        try:
            result = self.backend.download_revised_nda()
            tk.messagebox.showinfo("Download Revised NDA", result)
            if "successfully" in result:
                self.download_nda_button.configure(**self.completed_button_config)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def analyze_and_revise_nda(self):
        try:
            result = self.backend.analyze_and_revise_nda()
            if result == "Analysis complete. Ready to review changes.":
                self.review_changes()
                self.analyze_button.configure(**self.completed_button_config)
                self.download_nda_button.configure(**self.active_button_config, state="normal")
            else:
                tk.messagebox.showinfo("Analyze and Revise NDA", result)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
        except Exception as e:
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def review_changes(self):
        approved_changes = []
        for change in self.backend.review_changes():
            response = tk.messagebox.askyesno(
                "Review Change",
                f"Original: {change['original_text']}\n\nSuggested: {change['suggested_change']}\n\nAccept this change?",
            )
            if response:
                approved_changes.append(change)

        result = self.backend.apply_approved_changes(approved_changes)
        tk.messagebox.showinfo("Changes Applied", result)