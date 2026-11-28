# AI Demystified for Tech Leaders — Labs

This repository holds the labs of *AI Demystified for Tech Leaders* (Tech Leader Summit, December 2026): four labs done in the two sessions, and three more to try on your own.

**Open the lab page — https://skillrepos.github.io/tlsdemyst/** — and follow along there. You can type your answers into the page (they stay on your own device), or download the fill-in PDF from it. The takeaway handout is at https://skillrepos.github.io/tlsdemyst/handout.pdf. The same labs are written out in [labs.md](labs.md).

Two of the labs have a page of their own where you run something, and an optional deeper version in a GitHub Codespace. (“Teach it your rules”, one of the three to try on your own, uses any chatbot you already use; its two messages have Copy buttons on the lab page.)

- **Lab 1: Real RAG.** You take a 4-page PDF, pull the text out, split it into passages, store the passages in a vector database, and search it with a question — the same steps every RAG system runs.
- **Lab 2: Manage the agent.** You connect an assistant to a system through MCP (the Model Context Protocol), see the list of things the system offers, use them, and find out what happens when you ask for something that is not on the list. Then, as the agent's manager, you decide which actions it may take on its own.

Kettlewick is a made-up shop. The handbook is a training sample, not a real policy.

There are two ways to do each lab. Both ways use the same made-up data and get the same results.

| | In your browser | In a GitHub Codespace (optional) |
|---|---|---|
| You need | A phone or laptop | A laptop and a free GitHub account |
| Setup | None. Open the page. | About 5 minutes while it builds |
| Lab 1: vector database | Runs inside the browser page | Chroma, saved as a folder |
| Lab 2: the server | Runs inside the browser page | A separate program the lab starts |
| Who writes the answer | You paste the message into any chatbot | A small model running in the Codespace |

---

## Way 1: in your browser (everyone)

- **Lab 1:** open **https://skillrepos.github.io/tlsdemyst/rag.html** (or tap **Lab 1: RAG** at the top of the lab page) and work through the five boxes on the page.
- **Lab 2:** open **https://skillrepos.github.io/tlsdemyst/mcp.html** (or tap **Lab 2: Manage the agent** at the top) and work through its five boxes.
- **Lab 3:** open **https://skillrepos.github.io/tlsdemyst/injection.html** (or tap **Lab 3: Prompt injection** at the top) and work through its two boxes. It builds the same handbook search as Lab 1 by itself, so Lab 1 does not need to be open.

The Lab 1, Lab 2 and Lab 3 pages are **teal**; the main lab page is **navy**, so you can tell them apart.

The first visit to the Lab 1 page downloads about 25–40 MB (the small model that turns text into numbers, and the code that runs it). After that it is saved on your device. Nothing you type leaves your device.

---

## Way 2: in a GitHub Codespace (optional, deeper)

### Lab 1: Real RAG

**1.** Sign in to GitHub. On this repository's page, click the green **Code** button, then the **Codespaces** tab, then **Create codespace on main**.

**2.** Wait for setup to finish — about 5 minutes. It installs the vector database and downloads two models: a small one that turns text into numbers, and one that writes answers. It is done when the terminal at the bottom shows a prompt and no more messages scroll past.

**3.** Have the script read the PDF. In the terminal, run:

```
python codespace/rag_lab.py read
```

It prints how many pages and words it found, and the first lines of page 1.

**4.** Split the text into passages:

```
python codespace/rag_lab.py split
```

You should see 14 passages, one per section of the handbook.

**5.** Turn each passage into numbers and store them in the vector database:

```
python codespace/rag_lab.py store
```

It prints the first 12 of the 384 numbers that now stand for Section 1. A new folder, `codespace/vector_db`, appears in the file list on the left: that folder is the database.

**6.** Ask a question. This step only searches; no model writes anything yet:

```
python codespace/rag_lab.py ask "I bought a blender 45 days ago. Can I get my money back?"
```

Look at the three passages it found and how close each one is.

**7.** Ask in words the handbook does not use:

```
python codespace/rag_lab.py ask "My parcel turned up smashed. What now?"
```

The handbook never says "parcel" or "smashed" in that section. The search matched on meaning.

**8.** Ask something the handbook does not cover:

```
python codespace/rag_lab.py ask "Do you sell gift cards?"
```

It still returns three passages. None is about gift cards. A vector database always returns its closest matches, whether or not they answer the question.

**9.** Now run the whole of RAG — search, then hand the passages to a model:

```
python codespace/rag_lab.py answer "I bought a blender 45 days ago. Can I get my money back?"
```

It prints the exact message sent to the model, then the model's answer. The right answer is store credit, minus 10%.

**10.** Try the gift-card question with `answer` instead of `ask`:

```
python codespace/rag_lab.py answer "Do you sell gift cards?"
```

A good answer says the handbook does not say. Note what yours does.

**11.** Open `codespace/rag_lab.py` in the editor. The whole pipeline is about 100 lines. Find the five functions that match the five steps: `read_pdf`, `split_into_passages`, `store`, `find_closest`, `build_message`.

### Lab 2: Manage the agent (the connection part)

Use the same Codespace. If you have not created it yet, do steps 1 and 2 of Lab 1 first.

**1.** Ask the local model about an order, with no connection to anything:

```
python codespace/mcp_lab.py ask "Was order 1182 charged twice? What should we do about it?"
```

It has never seen Kettlewick's records. Note whether it says so or guesses.

**2.** Connect to the Kettlewick server and see what it offers:

```
python codespace/mcp_lab.py tools
```

Four things are on the list. That list is the whole of what an assistant can do through this connection.

**3.** Use one of them yourself:

```
python codespace/mcp_lab.py call look_up_order 1182
```

**4.** Use another:

```
python codespace/mcp_lab.py call list_charges 1182
```

There are two charges of $89.00 on the same day.

**5.** Ask for something that is not on the list:

```
python codespace/mcp_lab.py call issue_refund 1182
```

The server refuses. There is no refund tool, so no assistant using this server can issue one.

**6.** Now ask the model the same question as step 1, this time with the server connected:

```
python codespace/mcp_lab.py ask --connect "Was order 1182 charged twice? What should we do about it?"
```

Watch the steps: the model chooses what to ask the server for, reads what comes back, and then answers. The right answer is yes — refund one $89.00 charge in full (rule 3), once a person approves it (rule 4).

**7.** Open `codespace/kettlewick_server.py` in the editor. Each thing the server offers is one short function with `@server.tool()` above it. Notice what is not there.

**8.** Compare your answers from step 1 and step 6. The model did not change. What changed is what it could reach.

**If something goes wrong**

- *"Could not reach the local model"* — run `bash codespace/scripts/startOllama.sh`, wait for "Ollama is running.", and try again.
- *"The database is empty"* — run step 5 again.
- *The answer is slow* — normal. The model runs on the Codespace's own processor, with no graphics card.

---

## What is in this repository

| File or folder | What it is |
|---|---|
| `index.html` | The lab page: the four labs, then the three to try on your own, with boxes to type answers into. Answers are saved in your own browser and are not sent anywhere. |
| `labs.md` | The same labs written out in full |
| `lab-workbook.pdf` | The same labs as a PDF to type into or print |
| `handout.pdf` | The takeaway handout |
| `rag.html`, `mcp.html`, `injection.html` | The browser pages for Labs 1, 2 and 3 |
| `kettlewick-handbook.pdf` | The sample document used in Labs 1 and 3 |
| `codespace/` | The Codespace versions of Labs 1 and 2 |

## License

For educational use only by the attendees of our workshops. See [LICENSE](LICENSE).
(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
