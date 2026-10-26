# ex01 — JSON, URLs and status codes (plain Python)

**Target time:** 30 minutes. **Read first:** sections 2 to 4 of *Web APIs from the Ground Up*.
**Concepts:** taking a URL apart, status code families, `json.loads` / `json.dumps`,
validating incoming data (the thing that decides between 201 and 400).

No web server yet. Fill in the functions in `ex01_json/solution.py`; each docstring
says exactly what to return. The tests call them directly.

Useful standard-library tools (look them up in the Python docs if you need to):
`json.loads`, `json.dumps`, `urllib.parse.urlsplit`, `urllib.parse.parse_qsl`.

Run the tests with `python -m unittest ex01_json.tests` (or `python score.py ex01`).
