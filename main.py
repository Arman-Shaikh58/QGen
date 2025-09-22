import os
from pyfiglet import Figlet
from termcolor import colored
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pdf_reader import read_pdf  # your existing read_pdf function

def save_questions_to_pdf(questions: dict, output_file: str):
    """
    Save generated questions dictionary to a PDF file.
    :param questions: Dict with keys '2_marks', '4_marks', '6_marks'
    :param output_file: Path to output PDF file
    """
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - margin
    line_height = 18

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Generated Questions")
    y -= line_height * 2

    c.setFont("Helvetica", 12)
    for weight, qs in questions.items():
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, f"{weight.upper()}:")
        y -= line_height

        c.setFont("Helvetica", 12)
        if qs:
            for i, q in enumerate(qs, 1):
                text = f"{i}. {q}"
                # wrap text if too long
                for line in split_text(text, 90):
                    c.drawString(margin + 20, y, line)
                    y -= line_height
                    if y < margin:
                        c.showPage()
                        y = height - margin
        else:
            c.drawString(margin + 20, y, "No questions generated.")
            y -= line_height

        y -= line_height  # extra space between sections

    c.save()


def split_text(text, max_chars):
    """Simple text wrapper: splits a long string into lines of max_chars length"""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def main():
    # Banner
    f = Figlet(font="slant")
    print(colored(f.renderText("WELCOME-TO-QGEN"), 'green'))

    # Instruction
    print(colored("Select the PDF file listed below:", 'red'))

    # List PDFs in current directory
    pdf_files = [fn for fn in os.listdir('.') if fn.lower().endswith('.pdf')]

    if not pdf_files:
        print(colored("No PDF files found in this folder.", 'yellow'))
        return

    for i, pdf in enumerate(pdf_files):
        print(colored(f"[{i}] {pdf}", 'cyan'))

    print('\n' + colored("Enter the number of the file for which you want to create questions:", 'red'))
    file_index = int(input('> ').strip())
    
    selected_pdf = pdf_files[file_index]
    questions = read_pdf(selected_pdf)  # returns the questions dict

    print(colored(f"\nGenerated questions from {selected_pdf}:\n", 'green'))
    for weight, qs in questions.items():
        print(colored(f"{weight.upper()}:", 'yellow'))
        if qs:
            for i, q in enumerate(qs, 1):
                print(f"{i}. {q}")
        else:
            print("No questions generated.\n")
        print()

    # Save to PDF
    output_file = f"{os.path.splitext(selected_pdf)[0]}_questions.pdf"
    save_questions_to_pdf(questions, output_file)
    print(colored(f"\nQuestions saved to {output_file}", 'green'))


if __name__ == "__main__":
    main()
