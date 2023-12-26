import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PyPDF2 import PdfReader, PdfWriter
import os
import random

class TestPaperGenerator:
    def __init__(self):
        self.selected_papers = []
        self.subject = ""
        self.standard = ""

    def select_papers(self, file_paths):
        self.selected_papers = file_paths

    def set_subject_and_standard(self, subject, standard):
        self.subject = subject
        self.standard = standard
    
    def generate_test_paper(self, output_file_path):
     mcq_count = 5
     subjective_count = 5

     pdf_writer = PdfWriter()

     for paper_path in self.selected_papers:
        pdf_reader = PdfReader(paper_path)

        for i in range(mcq_count):
            mcq_page_number = random.randint(0, len(pdf_reader.pages) - 1)
            mcq_page = pdf_reader._get_page(mcq_page_number)
            pdf_writer.add_page(mcq_page)

        for i in range(subjective_count):
            subjective_page_number = random.randint(0, len(pdf_reader.pages) - 1)
            subjective_page = pdf_reader._get_page(subjective_page_number)
            pdf_writer.add_page(subjective_page)

     output_pdf_path = os.path.join(output_file_path, f"TestPaper_{self.subject}_{self.standard}.pdf")
     with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
     messagebox.showinfo("Success", f"Test paper generated successfully at {output_pdf_path}")


class TestPaperGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Paper Generator")

        self.generator = TestPaperGenerator()

        self.create_widgets()

    def create_widgets(self):
        # File Selection
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)

        tk.Label(file_frame, text="Select PDF Files:").grid(row=0, column=0, sticky="w", padx=5)
        tk.Button(file_frame, text="Browse", command=self.browse_files).grid(row=0, column=1, padx=5)

        # Subject and Standard Entry
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Subject:").grid(row=0, column=0, sticky="w", padx=5)
        tk.Entry(entry_frame, textvariable=tk.StringVar()).grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Standard:").grid(row=1, column=0, sticky="w", padx=5)
        tk.Entry(entry_frame, textvariable=tk.StringVar()).grid(row=1, column=1, padx=5)

        # Generate Button
        tk.Button(self.root, text="Generate Test Paper", command=self.generate_test_paper).pack(pady=10)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if not file_paths:
            messagebox.showinfo("Info", "No files selected.")
        else:
            self.generator.select_papers(file_paths)
            messagebox.showinfo("Info", f"{len(file_paths)} files selected.")

    def generate_test_paper(self):
        subject = self.get_entry_text(0)
        standard = self.get_entry_text(1)

        if not subject or not standard:
            messagebox.showwarning("Warning", "Please enter both subject and standard.")
            return

        self.generator.set_subject_and_standard(subject, standard)

        output_directory = r'C:\Users\dell\Desktop\test_paper'
        os.makedirs(output_directory, exist_ok=True)
        self.generator.generate_test_paper(output_directory)

    def get_entry_text(self, index):
        return self.root.winfo_children()[1].winfo_children()[index].cget("text")

if __name__ == "__main__":
    root = tk.Tk()
    app = TestPaperGeneratorGUI(root)
    root.mainloop()
