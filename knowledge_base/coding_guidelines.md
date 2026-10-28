# Nexus Project Coding Guidelines

## Python Standards
- **Type Hints:** All Python functions MUST include type hints (e.g., `def parse_data(input_str: str) -> dict:`).
- **Docstrings:** Use Google-style docstrings for all classes and complex functions.
- **Library Preferences:**
  - For HTTP requests, always use `requests` over `urllib`.
  - For data validation and structured schemas, use `pydantic`. DO NOT use standard `dataclasses`.
  - For frontend dashboards, use `streamlit`.

## API Security
- Never hardcode API keys in scripts. Always use `os.environ.get("API_KEY")`.
- When dealing with user input, sanitize against basic prompt injection before sending payloads.

## System Architecture
- Agents should fail gracefully. If an API times out, return a structured JSON object: `{"error": "API timeout", "code": 504}`.
