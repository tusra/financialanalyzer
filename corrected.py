import os
import glob
import datetime
from fpdf import FPDF
import streamlit as st

class CodePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Financial Statement Analyzer Codebase', 0, 1, 'C')
        self.cell(0, 10, f'Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_codebase_pdf(filename='financial_statement_analyzer_codebase.pdf'):
    pdf = CodePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Financial Statement Analyzer - Complete Codebase', 0, 1, 'C')
    pdf.ln(10)

    # Files to include
    python_files = ['app.py']
    utility_files = glob.glob('utils/*.py')
    config_files = ['.streamlit/config.toml']
    python_files.extend(utility_files)

    # --- Python Files ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Python Code Files', 0, 1, 'L')
    pdf.ln(5)

    for file_path in python_files:
        if os.path.exists(file_path):
            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f'File: {file_path}', 0, 1, 'L')
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

            with open(file_path, 'r') as file:
                content = file.read()
            lines = content.split('\n')
            pdf.set_font('Courier', '', 8)
            for i, line in enumerate(lines, 1):
                line_num = f"{i:4d}"
                if len(line) > 100:
                    chunks = [line[i:i+100] for i in range(0, len(line), 100)]
                    pdf.cell(10, 5, line_num, 0, 0, 'R')
                    pdf.cell(5, 5, '', 0, 0)
                    pdf.cell(0, 5, chunks[0], 0, 1)
                    for chunk in chunks[1:]:
                        pdf.cell(10, 5, '', 0, 0)
                        pdf.cell(5, 5, '', 0, 0)
                        pdf.cell(0, 5, chunk, 0, 1)
                else:
                    pdf.cell(10, 5, line_num, 0, 0, 'R')
                    pdf.cell(5, 5, '', 0, 0)
                    pdf.cell(0, 5, line, 0, 1)
            pdf.ln(5)

    # --- Config Files ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Configuration Files', 0, 1, 'L')
    pdf.ln(5)

    for file_path in config_files:
        if os.path.exists(file_path):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f'File: {file_path}', 0, 1, 'L')
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            with open(file_path, 'r') as file:
                content = file.read()
            lines = content.split('\n')
            pdf.set_font('Courier', '', 8)
            for i, line in enumerate(lines, 1):
                pdf.cell(10, 5, f"{i:4d}", 0, 0, 'R')
                pdf.cell(5, 5, '', 0, 0)
                pdf.cell(0, 5, line, 0, 1)
            pdf.ln(5)

    pdf.output(filename)
    return filename

# --- Streamlit UI ---
st.title("📄 Financial Statement Analyzer - Codebase PDF Generator")

if st.button("Generate PDF"):
    pdf_file = create_codebase_pdf()
    st.success("PDF generated successfully!")

    # Show download link
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📥 Download PDF",
            data=f,
            file_name=pdf_file,
            mime="application/pdf"
        )
