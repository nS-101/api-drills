# API Drills

Learn web APIs from the ground up, then Django, with exercises built like the Goldman Sachs
HackerRank **Software Diagnostics** section: a spec, unit tests you make pass, and a score.

Start with **`PLAN.md`**: the day-by-day plan up to the OA.

## What's in here

| Folder | What it is |
|---|---|
| `docs/1_web_apis_from_the_ground_up.pdf` | Guide A: the web, HTTP, JSON, REST, building a server by hand. No prior knowledge assumed. |
| `docs/2_django_guide.pdf` | Guide B: Django, step by step, plus the debugging playbook and exam-day plan. |
| `ex01` ... `ex10` | The exercises. Each has a `TASK.md` (the problem statement). |
| `HINTS.md` | Three hint levels per exercise. |
| `score.py` | The scoreboard. |

| # | Exercise | Stage | Time | Guide |
|---|---|---|---|---|
| ex01 | JSON, URLs and status codes | plain Python | 30 min | A 2-4 |
| ex02 | Build a todo API by hand | plain Python | 60-75 min | A 5-8 |
| ex03 | Django basics: URLs, views, JSON | Django | 25 min | B 1-4 |
| ex04 | Models and the ORM, a migration | Django | 30 min | B 6 |
| ex05 | Full CRUD API | Django | 40 min | B 5-8 |
| ex06 | **Mock OA 1**: Products (visible + hidden tests) | Django | 45 min, timed | B 1-8 |
| ex07 | **Debugging**: Library loans | Django | 45 min, timed | B 10 |
| ex08 | **Debugging**: Bank accounts (harder) | Django | 45 min, timed | B 10 |
| ex09 | Writing your own tests | Django | 40 min | B 9 |
| ex10 | **Mock OA 2**: Events, the final rehearsal | Django | 45 min, timed | all |

## Setup (once)

You need Python 3.10 or newer (`python3 --version`). In Terminal:

```bash
cd ~/api-drills
python3 -m venv .venv
source .venv/bin/activate          # do this every time you open a new Terminal window
pip install -r requirements.txt
python score.py ex01               # shows 0/15: that's the starting point
```

When the virtual environment is active your prompt starts with `(.venv)`, and `python`
means the right Python.

## The loop for every exercise

1. Read the guide sections listed above, then the exercise's `TASK.md`.
2. Start a timer. Write a one-line plan as a comment, then code.
3. Run the tests often: `python score.py ex05` (add `-v` to list failing test names), or the
   command at the bottom of each `TASK.md` for full error output.
4. Stuck? Read **one** level of `HINTS.md`, then try again.
5. Done (or out of time)? Commit your attempt with the time and score in the message, then
   compare with the solutions zip.

Some tests pass before you write anything (for example "a missing id gives 404"). The real
exam is the same, so judge by the total.

## Saving attempts and redoing exercises

This folder is a git repository. The first commit holds the untouched starting code.

```bash
git add -A && git commit -m "ex05 attempt 1: 35 min, 14/14"     # save an attempt
git log --oneline                                                 # find the first commit's hash
git checkout <first-commit-hash> -- ex05_crud                     # reset ex05 to redo it later
```

Redo the mocks and debugging exercises from a reset a few days later, like your LeetCode retries.

## Putting it on GitHub

Create an **empty** repository called `api-drills` on github.com (don't tick "Add a README").
Then, from inside this folder:

```bash
git remote add origin https://github.com/nS-101/api-drills.git
git push -u origin main
```

If it asks for a password, GitHub needs a personal access token, not your account password.
Alternatively install the GitHub CLI (`brew install gh`), run `gh auth login`, then
`gh repo create api-drills --private --source=. --push`.

## Practicing with an AI assistant

The real Diagnostics section has a limited built-in assistant. To rehearse, you may ask Claude
**narrow** questions while you practice ("what's the ORM lookup for case-insensitive
equality?"), never "solve this".
