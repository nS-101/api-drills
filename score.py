"""Scoreboard for every exercise, in the spirit of HackerRank's "x/y tests passed".

    python score.py          # every exercise
    python score.py ex05     # one exercise (or several: python score.py ex01 ex02)
    python score.py ex06 -v  # also list the names of failing (visible) tests
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (code, title, [(part name, runner, test label, show failing names?)])
# runner "unit" = plain Python unittest, "django" = python manage.py test
EXERCISES = [
    ("ex01", "JSON, URLs and status codes (plain Python)", [("tests", "unit", "ex01_json.tests", True)]),
    ("ex02", "Todo API by hand (plain Python)", [("tests", "unit", "ex02_http_server.tests", True)]),
    ("ex03", "Django basics: URLs, views, JSON", [("tests", "django", "ex03_basics", True)]),
    ("ex04", "Models and the ORM", [("tests", "django", "ex04_orm", True)]),
    ("ex05", "Full CRUD API", [("tests", "django", "ex05_crud", True)]),
    ("ex06", "Mock OA 1: Products (45 min)", [("visible", "django", "ex06_mock_oa.tests", True),
                                             ("hidden", "django", "ex06_mock_oa.tests_hidden", False)]),
    ("ex07", "Debugging: Library loans", [("tests", "django", "ex07_debug_library", True)]),
    ("ex08", "Debugging: Bank accounts", [("tests", "django", "ex08_debug_bank", True)]),
    ("ex09", "Write your own tests", None),  # graded separately
    ("ex10", "Mock OA 2: Events (45 min)", [("visible", "django", "ex10_mock_oa_2.tests", True),
                                           ("hidden", "django", "ex10_mock_oa_2.tests_hidden", False)]),
]
MUTANTS = ["m1", "m2", "m3", "m4", "m5", "m6"]


def runTests(runner, label, extraEnv=None):
    """Run one test label. Returns (passed, total, failingNames, rawOutput)."""
    env = dict(os.environ, **(extraEnv or {}))
    if runner == "unit":
        command = [sys.executable, "-m", "unittest", label]
    else:
        command = [sys.executable, "manage.py", "test", label, "--noinput"]
    result = subprocess.run(command, cwd=HERE, env=env, capture_output=True, text=True)
    output = result.stdout + result.stderr
    ranMatch = re.search(r"^Ran (\d+) tests?", output, re.MULTILINE)
    if not ranMatch:
        return None, None, [], output
    total = int(ranMatch.group(1))
    failures = sum(int(n) for n in re.findall(r"(?:failures|errors)=(\d+)", output))
    failingNames = re.findall(r"^(?:FAIL|ERROR): (\w+)", output, re.MULTILINE)
    return total - failures, total, failingNames, output


def bar(passed, total, width=20):
    filled = round(width * passed / total) if total else 0
    return "#" * filled + "." * (width - filled)


def lastLines(text, count=8):
    return "\n".join(text.strip().splitlines()[-count:])


def indent(text):
    return "\n".join("      " + line for line in text.splitlines())


def gradeWriteTests(verbose):
    passed, total, failing, output = runTests("django", "ex09_write_tests.test_mine")
    if total is None:
        print("    your tests could not run:\n" + indent(lastLines(output)))
        return
    print(f"    your tests vs the correct API: {passed}/{total} passing")
    if passed != total:
        print("    -> every test must pass against the correct API before broken versions count.")
        if verbose:
            print("    failing: " + ", ".join(failing))
        return
    caught = []
    for mutant in MUTANTS:
        mPassed, mTotal, _, _ = runTests("django", "ex09_write_tests.test_mine", {"EX09_MUTANT": mutant})
        if mTotal is None or mPassed < mTotal:
            caught.append(mutant)
    print(f"    broken APIs caught: [{bar(len(caught), len(MUTANTS), 12)}] {len(caught)}/{len(MUTANTS)}")
    survivors = [m for m in MUTANTS if m not in caught]
    if survivors:
        print(f"    not caught yet: {', '.join(survivors)} (which boundary in the rules isn't tested?)")


def main():
    args = [a.lower() for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "-v" in sys.argv
    chosen = [e for e in EXERCISES if not args or any(e[0] == a[:4] for a in args)]
    if not chosen:
        print("Unknown exercise. Use ex01 ... ex10.")
        return
    for code, title, parts in chosen:
        print(f"\n{code}  {title}")
        if parts is None:
            gradeWriteTests(verbose)
            continue
        for partName, runner, label, showNames in parts:
            passed, total, failing, output = runTests(runner, label)
            if total is None:
                print(f"    {partName}: could not run. Last lines of output:\n" + indent(lastLines(output)))
                continue
            print(f"    {partName:8} [{bar(passed, total)}] {passed}/{total}")
            if verbose and showNames and failing:
                print("             failing: " + ", ".join(failing))
    print()


if __name__ == "__main__":
    main()
