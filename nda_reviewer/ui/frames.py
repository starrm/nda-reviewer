import customtkinter as ctk
from PIL import Image
import os
from nda_reviewer.utils.icon_loader import load_svg_icon
from nda_reviewer.utils.secrets import get_secret, set_secret
from nda_reviewer.settings import OPENAI_API_KEY_NAME, FONT_FAMILY


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, backend):
        super().__init__(master)
        self.backend = backend
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
            self.nda_frame, text="Upload NDA", command=self.upload_nda
        )
        self.upload_nda_button.grid(row=0, column=0, padx=5, pady=10)

        # Upload Guidelines button
        self.upload_guidelines_button = ctk.CTkButton(
            self.nda_frame, text="Upload Guidelines", command=self.upload_guidelines
        )
        self.upload_guidelines_button.grid(row=0, column=1, padx=5, pady=10)

        # Analyze and Revise NDA button
        self.analyze_button = ctk.CTkButton(
            self.nda_frame,
            text="Analyze and Revise NDA",
            command=self.analyze_and_revise_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.analyze_button.grid(row=0, column=2, padx=5, pady=10)

        # Download Revised NDA button
        self.download_nda_button = ctk.CTkButton(
            self.nda_frame,
            text="Download Revised NDA",
            command=self.download_revised_nda,
        )
        self.download_nda_button.grid(row=0, column=3, padx=5, pady=10)

    def upload_nda(self):
        try:
            result = self.backend.upload_nda()
            messagebox.showinfo("Upload NDA", result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def upload_guidelines(self):
        try:
            result = self.backend.upload_guidelines()
            messagebox.showinfo("Upload Guidelines", result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def download_revised_nda(self):
        try:
            result = self.backend.download_revised_nda()
            messagebox.showinfo("Download Revised NDA", result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def analyze_and_revise_nda(self):
        try:
            result = self.backend.analyze_and_revise_nda()
            if result == "Analysis complete. Ready to review changes.":
                self.review_changes()
            else:
                messagebox.showinfo("Analyze and Revise NDA", result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def review_changes(self):
        approved_changes = []
        for change in self.backend.review_changes():
            response = messagebox.askyesno(
                "Review Change",
                f"Original: {change['original_text']}\n\nSuggested: {change['suggested_change']}\n\nAccept this change?",
            )
            if response:
                approved_changes.append(change)

        result = self.backend.apply_approved_changes(approved_changes)
        messagebox.showinfo("Changes Applied", result)