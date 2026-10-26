# The plan: from zero to the Goldman OA

Your OA invitation (Oct 24) asks you to complete it within about 7 days, so this plan aims
to have you ready by **Saturday, Oct 31**. It's about 2 to 3 hours a day. Guide A is
`docs/1_web_apis_from_the_ground_up.pdf`; Guide B is `docs/2_django_guide.pdf`.

The OA has two parts: **Software Fundamentals** (30 min, DSA) and **Software Diagnostics**
(45 min, a Django / Node / Spring Boot project). This repo covers Diagnostics; keep your DSA
going alongside it with one or two NeetCode retries a day (blank file, timed).

| Day | Learn | Do | Alongside |
|---|---|---|---|
| **Mon 26** | Guide A sections 0-4 (about 45 min) | **ex01** (30 min). Then Guide A 5-7: type and run both servers, then **start ex02** | - |
| **Tue 27** | Guide A 8-14 | **Finish ex02** (aim for 16/16). Then Guide B 1-4 and **ex03** (25 min) | 1 DSA retry |
| **Wed 28** | Guide B 5-8 | **ex04** (30 min) and **ex05** (40 min) | 1 DSA retry |
| **Thu 29** | Guide B 9-10 | **ex06 Mock OA 1** (45 min timer, exam rules), review it; then **ex07** (45 min timer) | 30-min DSA mock |
| **Fri 30** | Guide B 11 | **ex08** (45 min timer), **ex09** (40 min); then **ex10 Mock OA 2** (45 min timer) | 1 DSA retry |
| **Sat 31** | Skim Guide B's debugging table (section 10) and exam-day plan (section 11) | **Take the OA** when you're fresh, ideally in the morning | - |

## If you fall behind

Do these in this order and skip the rest: **ex02, ex03, ex05, ex06, ex07, ex10**.
ex02 is the foundation for everything after it; ex06, ex07 and ex10 are the closest to the
real thing.

## Rules for the timed ones (ex06, ex07, ex08, ex10)

- A real timer, started before you read the task.
- No notes, no old code, no hints. The Django docs for syntax only.
- When time's up, stop. Run `python score.py exNN`, write down the score, commit, then
  finish it untimed and compare with the solutions.

## Your scorecard

Fill this in as you go (and send me the numbers so I can tell you where to focus).

| Exercise | Date | Time taken | Score | What went wrong |
|---|---|---|---|---|
| ex01 | | | /15 | |
| ex02 | | | /16 | |
| ex03 | | | /12 | |
| ex04 | | | /11 | |
| ex05 | | | /14 | |
| ex06 | | | /5 visible, /12 hidden | |
| ex07 | | | /9 | |
| ex08 | | | /12 | |
| ex09 | | | /6 caught | |
| ex10 | | | /5 visible, /12 hidden | |

## After the OA

- Reset ex06, ex07, ex08 and ex10 and redo them a week later.
- Learn Django REST Framework (django-rest-framework.org) and redo ex05 with it.
- Work through the official Django tutorial (templates, admin, forms).
