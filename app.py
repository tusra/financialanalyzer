import os
import glob
from fpdf import FPDF
import datetime

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

def create_codebase_pdf():
    pdf = CodePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Financial Statement Analyzer - Complete Codebase', 0, 1, 'C')
    pdf.ln(10)
    
    # Get a list of all Python files
    python_files = ['app.py']
    
    # Add utility files
    utility_files = glob.glob('utils/*.py')
    python_files.extend(utility_files)
    
    # Add any other files
    config_files = ['.streamlit/config.toml']
    
    # Process Python files
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
            
            # Read file content
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Add content to PDF
            pdf.set_font('Courier', '', 8)
            
            # Split content into lines and add line numbers
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # Format line number
                line_num = f"{i:4d}"
                
                # Handle long lines by wrapping
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
    
    # Process configuration files
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
            
            # Read file content
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Add content to PDF
            pdf.set_font('Courier', '', 8)
            
            # Split content into lines
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                line_num = f"{i:4d}"
                pdf.cell(10, 5, line_num, 0, 0, 'R')
                pdf.cell(5, 5, '', 0, 0)
                pdf.cell(0, 5, line, 0, 1)
            
            pdf.ln(5)
    
    # Save the PDF
    pdf.output('financial_statement_analyzer_codebase.pdf')
    print("PDF generated successfully: financial_statement_analyzer_codebase.pdf")

if __name__ == "__main__":
    create_codebase_pdf()
