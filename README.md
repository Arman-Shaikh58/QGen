
# Question Generator (QGen)

A small CLI tool that reads a PDF, sends the text to a configurable LLM (Google Gemini via `langchain_google_genai`), and generates exam-style questions grouped by weightage (2, 4, and 6 marks).

## Features
- List PDF files in the current folder and pick one to generate questions for
- Extracts text from the PDF using `pypdf`
- Sends text to an LLM and expects a JSON response with keys `2_marks`, `4_marks`, `6_marks`
- Returns structured output and prints helpful error messages when parsing or invocation fails

## Requirements
- Python 3.10+ recommended
- The project depends on several packages (install with pip). Minimal list:

```powershell
pip install pypdf pyfiglet termcolor langchain-google-genai langchain-core
```

Note: Package names for `langchain` or the Google GenAI integration may differ depending on your environment or the provider. Adjust accordingly.

## Configuration
Create or edit `config.py` in the project root and set your Google API key:

```python
# config.py
GOOGLE_API_KEY = "your-google-api-key-here"
```

Make sure the key is valid and that the `langchain_google_genai` package and its dependencies are installed and configured for the target model (the code currently uses `gemini-2.5-flash`).

## Usage
1. Put the PDF(s) you want to use into the project folder (same folder as `main.py`).
2. Run the application:

```powershell
python main.py
```

3. The CLI will print a numbered list of PDFs. Enter the index of the file to process (e.g., `0`).

Behavior after selecting a PDF:
- The program extracts the full text from the PDF and calls the LLM with a system prompt asking for a JSON object containing `2_marks`, `4_marks`, and `6_marks` lists of questions.
- The program prints or returns a structured dictionary (depending on how you call it).

## Example (programmatic use)
If you prefer to use it from another script, `read_pdf` returns the questions dictionary or an error dict:

```python
from pdf_reader import read_pdf
questions = read_pdf('Notes_chapter 1.pdf')
print(questions)
```

Expected return shape on success:

```json
{
	"2_marks": ["..."],
	"4_marks": ["..."],
	"6_marks": ["..."]
}
```

On failure you'll get a dictionary with an `error` key and possibly `raw` output for debugging.

## Troubleshooting
- "No JSON object found in LLM response": The model did not return a clean JSON object. Check `raw` in the returned dict. Consider tightening the system prompt or trimming input length.
- "LLM invocation failed": Check `GOOGLE_API_KEY`, network access, and that `langchain_google_genai` is correctly installed and authenticated.
- If extraction returns empty text: Some PDFs are image-only. Use an OCR step (e.g., Tesseract) to extract text before passing to this tool.
- Token limits: Very large PDFs may exceed the LLM's token limits. Consider chunking the text into sections and calling `create_questions` for each chunk, then merging results.

## Next steps and improvements
- Add chunking of very long documents and aggregation logic.
- Add unit tests that mock the LLM to validate parsing and error handling.
- Add an option to save the generated questions as JSON or plaintext files.
- Add support for image-based PDFs via optional OCR step.

## License
This project has no license file. Add a LICENSE if you plan to share or publish.

