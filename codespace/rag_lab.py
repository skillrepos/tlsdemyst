#!/usr/bin/env python3
"""
RAG lab — the whole pipeline in one readable file.

  read    pull the plain text out of the PDF
  split   cut the text into passages, one per section
  store   turn each passage into numbers and save them in a vector database
  ask     find the passages closest to a question
  answer  hand those passages and the question to a model, and print its answer

Run each step in order:
  python codespace/rag_lab.py read
  python codespace/rag_lab.py split
  python codespace/rag_lab.py store
  python codespace/rag_lab.py ask "I bought a blender 45 days ago. Can I get my money back?"
  python codespace/rag_lab.py answer "I bought a blender 45 days ago. Can I get my money back?"
"""

import json
import os
import re
import sys
import urllib.request

import chromadb                      # the vector database
from pypdf import PdfReader          # reads text out of PDF files

BASE = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE, "..", "kettlewick-handbook.pdf")
DB_PATH = os.path.join(BASE, "vector_db")          # the database is a folder on disk
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_URL = "http://localhost:11434/api/chat"
HOW_MANY = 3                                        # passages to fetch for each question


# ------------------------------------------------------------ step 1: read ----
def read_pdf():
    """Return a list of (page number, plain text) pairs."""
    reader = PdfReader(PDF_PATH)
    return [(number, page.extract_text()) for number, page in enumerate(reader.pages, start=1)]


# ----------------------------------------------------------- step 2: split ----
def split_into_passages(pages):
    """Cut each page at its section headings. One section becomes one passage."""
    passages = []
    for number, text in pages:
        for piece in re.split(r"(?=Section \d+: )", text):
            match = re.match(r"(Section \d+: [^\n]+)\n(.+)", piece, flags=re.S)
            if not match:
                continue                             # the title and note at the top of page 1
            title = match.group(1).strip()
            body = " ".join(match.group(2).split())
            passages.append({"title": title, "text": body, "page": number})
    return passages


# ----------------------------------------------------------- step 3: store ----
def open_collection(fresh=False):
    """Open the vector database. Chroma turns text into numbers with a small built-in model."""
    client = chromadb.PersistentClient(path=DB_PATH)
    if fresh:
        try:
            client.delete_collection("handbook")
        except Exception:
            pass
    return client.get_or_create_collection("handbook", metadata={"hnsw:space": "cosine"})


def store(passages):
    collection = open_collection(fresh=True)
    collection.add(
        ids=[f"passage-{i}" for i in range(len(passages))],
        documents=[p["title"] + ". " + p["text"] for p in passages],
        metadatas=[{"title": p["title"], "page": p["page"]} for p in passages],
    )
    return collection


# ------------------------------------------------------------- step 4: ask ----
def find_closest(question):
    """Return the passages whose numbers are closest to the question's numbers."""
    collection = open_collection()
    if collection.count() == 0:
        sys.exit("The database is empty. Run the store step first:  python codespace/rag_lab.py store")
    found = collection.query(query_texts=[question], n_results=HOW_MANY)
    hits = []
    for text, meta, distance in zip(found["documents"][0], found["metadatas"][0], found["distances"][0]):
        hits.append({"title": meta["title"], "page": meta["page"], "text": text, "score": 1 - distance})
    return hits


def describe(score):
    return "strong match" if score >= 0.45 else "fair match" if score >= 0.3 else "weak match"


# ---------------------------------------------------------- step 5: answer ----
def build_message(question, hits):
    passages = "\n\n".join(f"[{h['title']}, page {h['page']}] {h['text']}" for h in hits)
    return (
        "Answer the customer's question using only the handbook passages below. "
        "If the passages do not contain the answer, say that the handbook does not say. "
        "Name the section you used.\n\n"
        f"Handbook passages:\n{passages}\n\nCustomer's question: {question}"
    )


def ask_model(message):
    """Send one message to the local model and return its reply."""
    body = json.dumps({"model": MODEL, "stream": False, "options": {"temperature": 0},
                       "messages": [{"role": "user", "content": message}]}).encode()
    request = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.loads(response.read())["message"]["content"].strip()
    except OSError as error:
        sys.exit(f"Could not reach the local model ({error}).\nStart it with:  bash codespace/scripts/startOllama.sh")


# ------------------------------------------------------------------- main ----
def line(char="-"):
    print(char * 72)


def main():
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    question = " ".join(sys.argv[2:]).strip()

    if step == "read":
        pages = read_pdf()
        words = sum(len(text.split()) for _, text in pages)
        print(f"Read {len(pages)} pages: about {words} words of plain text.\n")
        print("The first lines of page 1:")
        line()
        print("\n".join(pages[0][1].splitlines()[:8]))
        line()

    elif step == "split":
        passages = split_into_passages(read_pdf())
        average = sum(len(p["text"].split()) for p in passages) // len(passages)
        print(f"{len(passages)} passages, about {average} words each.\n")
        for p in passages:
            print(f"  page {p['page']}  {p['title']}")
        print("\nOne passage in full:")
        line()
        print(passages[0]["title"] + "\n" + passages[0]["text"])
        line()

    elif step == "store":
        passages = split_into_passages(read_pdf())
        collection = store(passages)
        numbers = collection.get(ids=["passage-0"], include=["embeddings"])["embeddings"][0]
        print(f"Stored {collection.count()} passages in the vector database ({DB_PATH}).")
        print(f"Each passage is now {len(numbers)} numbers.\n")
        print(f'What "{passages[0]["title"]}" looks like to the database:')
        print("  " + ", ".join(f"{x:.3f}" for x in numbers[:12]) + f", ... and {len(numbers) - 12} more")

    elif step in ("ask", "answer"):
        if not question:
            sys.exit(f'Add a question in quotes, for example:\n  python codespace/rag_lab.py {step} "Do you sell gift cards?"')
        hits = find_closest(question)
        print(f"Question: {question}\n")
        print(f"The {len(hits)} closest passages:")
        for number, h in enumerate(hits, start=1):
            print(f"\n  {number}. {h['title']} (page {h['page']})  -  {describe(h['score'])}, {h['score']:.2f}")
            print(f"     {h['text'][:150]}...")
        if hits[0]["score"] < 0.45:
            print("\n  No strong match. The database returns its closest passages whether or not")
            print("  any of them answers the question.")
        if step == "answer":
            message = build_message(question, hits)
            print("\nThe message sent to the model:")
            line()
            print(message)
            line()
            print(f"\nThe model's answer ({MODEL}, running in this Codespace):")
            line("=")
            print(ask_model(message))
            line("=")

    elif step == "warmup":
        # Run once while the Codespace is being created, so the first lab step does not wait for a download.
        store(split_into_passages(read_pdf()))
        print("The text-to-numbers model is downloaded.")

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
