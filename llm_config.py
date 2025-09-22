import re
import json
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import GOOGLE_API_KEY


# Initialize the model (keep this fast-failing if not configured)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
    temperature=0,
    max_output_tokens=None,
    timeout=None,
)


def _extract_json_from_text(raw: str) -> str | None:
    """Extract the first balanced JSON object from raw text.

    This is safer than a greedy regex and handles surrounding backticks or markdown.
    Returns the JSON substring or None if not found.
    """
    # Look for a JSON-looking block starting with '{' and ending with the matching '}'
    start = raw.find('{')
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(raw)):
        ch = raw[i]
        if ch == '"' and not escape:
            in_string = not in_string
        if ch == '\\' and not escape:
            escape = True
        else:
            escape = False

        if not in_string:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return raw[start:i+1]

    return None


def create_questions(text: str) -> Dict[str, Any]:
    """
    Generates questions with weightage 2, 4, and 6 marks from the given text.
    Returns a dictionary with keys '2_marks', '4_marks', '6_marks' and lists of questions.

    If parsing fails, returns a dict with key 'raw' containing the LLM output and
    'error' describing the problem.
    """
    if not text or not text.strip():
        return {"2_marks": [], "4_marks": [], "6_marks": []}

    messages = [
        SystemMessage(
            content=(
                "You are a helpful assistant. Create questions from the given text with weightage 2 marks, 4 marks, and 6 marks. "
                "Return the output strictly as a JSON object with keys '2_marks', '4_marks', '6_marks' and lists of questions as values. Do NOT include any extra text."
            )
        ),
        HumanMessage(content=text)
    ]

    try:
        response = llm.invoke(messages)
    except Exception as e:
        return {"error": f"LLM invocation failed: {e}", "2_marks": [], "4_marks": [], "6_marks": []}

    raw = getattr(response, 'content', str(response))

    # Remove common markdown fences
    raw_clean = re.sub(r"```(?:json)?\n?", "", raw, flags=re.IGNORECASE)

    json_str = _extract_json_from_text(raw_clean)
    if not json_str:
        return {"error": "No JSON object found in LLM response.", "raw": raw_clean}

    try:
        questions_dict = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}", "raw": json_str}

    # Basic validation: ensure expected keys exist
    for k in ("2_marks", "4_marks", "6_marks"):
        if k not in questions_dict:
            questions_dict.setdefault(k, [])

    return questions_dict