#!/usr/bin/env python3
"""Confirms the sample text and key numbers are the same in labs.md, index.html (+ labs.js) and
build-workbook-pdf.py. Run from the repo folder after changing any of them:  python3 check-labs.py"""
import sys, html
MUST = [
    "My blender arrived broken. Please send a replacement.",
    "Try 1: add the post and ask again",
    "Try 2: swap in the edited post and ask again",
    "Mi licuadora llegó rota. Por favor, envíen un reemplazo.",
    "ORD-2207 / KW-BLND-89 / 2026-11-20 / $89.00",
    "I was charged twice for order 1182. Please refund one charge.",
    "Look up the order", "List the charges on the order", "Draft a reply", "Send the reply", "Refund $20", "Refund $500",
    "Which number moves: time, cost, quality or revenue?",
    "Is there a baseline today? Can we see a result inside 90 days, on one workflow?",
    "What is the worst it could do if it were tricked?",
    "Estimate the tokens", "Real RAG, in your browser", "Teach it your rules", "Manage the agent", "See the top AI security risk",
    "Cheaper at another shop (happy)", "Dented $45 kettle (angry)", "Change account email (polite)", "Parcel 12 business days late", "Charged $89 twice",
    "The same blender is $15 cheaper at another shop. Not complaining, I love Kettlewick, just thought you'd want to know!",
    "10 or more business days late",
    "On the list",
    "Score the proposal", "Start your own pilot page",
    "lowest score", "reads only", "about 40 MB", "Line C is the shortest",
]
files = {"labs.md": open("labs.md", encoding="utf-8").read(),
         "index.html + labs.js": html.unescape(open("index.html", encoding="utf-8").read() + open("labs.js", encoding="utf-8").read()),
         "build-workbook-pdf.py": open("build-workbook-pdf.py", encoding="utf-8").read()}
# Labs 6 (Three ticks) and 7 (inventory) were cut on 11/23, and Price the ticket on 11/24 (now slides); the old numbers must not come back.
MUST_NOT = ["Read the ticket", "Check payment records", "end to end", "same length", "no right answer sheet", "25 to 40 MB", "Price the ticket", "Lab 8", "LAB 8", "eight short labs", "Three ticks", "three-minute inventory", "Lab 9", "Lab 10", "LAB 9", "LAB 10", "ten labs", "ten short labs",
            # 2-hour version (11/27): four numbered labs; the old numbers 5 to 7 and "seven labs" must not come back
            "Lab 5", "Lab 6", "Lab 7", "LAB 5", "LAB 6", "LAB 7", "seven short labs", "seven labs", "how of hands"]
bad = 0
for name, text in files.items():
    for m in MUST:
        if m not in text: print(f"MISSING in {name}: {m}"); bad += 1
    for m in MUST_NOT:
        if m in text: print(f"LEFT OVER in {name}: {m}"); bad += 1
print("All three match." if not bad else f"{bad} problem(s).")
sys.exit(1 if bad else 0)
