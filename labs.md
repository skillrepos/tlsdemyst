# AI Demystified for Tech Leaders — Labs

**Tech Leader Summit, December 2026 · Brent Laster, Tech Skills Transformations**
**Revision 5.0 · 11/27/26 · the 2-hour version**

There are four short labs: two in session 1 and two in session 2. You do every one on your own. Three more, at the end, are for you to try on your own afterwards.

## How to use these labs

- **Where you work:** the lab page, <https://skillrepos.github.io/tlsdemyst/>. Type your answers there; they are saved on your own device and are not sent anywhere. **Labs 1, 2 and 3** also have a page of their own with the buttons you press (linked from the top of the lab page). You still type those labs' answers on the lab page.
- **What you need:** a phone or a laptop with a web browser. There is nothing to install. For Lab 3 (and for “Teach it your rules”, one of the three to try on your own) you also need any chatbot you already use (ChatGPT, Copilot, Gemini, Claude). If your work laptop blocks the lab page, use your phone.
- **Prefer paper or a file?** Download `lab-workbook.pdf` from the lab page and type into it, or write on a printed copy.
- **One rule:** never paste company data into a chatbot. Every lab here that uses a chatbot uses only the sample text in these labs. “Start your own pilot page”, at the end, is about your own work, but it uses no chatbot, and your answers stay with you.

Kettlewick is a made-up shop. Its orders, customers and policies are samples for this session.

| Lab | Title | You need |
|---|---|---|
| **Session 1** | | |
| 1 | Real RAG, in your browser | Lab 1 page |
| 2 | Manage the agent | Lab 2 page |
| **Session 2** | | |
| 3 | See the top AI security risk | Lab 3 page and any chatbot |
| 4 | Score the proposal | Nothing |
| **More to try on your own** | | |
| | Estimate the tokens | Lab page (or OpenAI's tokenizer page) |
| | Teach it your rules | Any chatbot |
| | Start your own pilot page | Nothing |

---

# Session 1: the technology

## Lab 1: Real RAG, in your browser

**You need:** the Lab 1 page: <https://skillrepos.github.io/tlsdemyst/rag.html>

**Purpose:** RAG is how an AI system answers from your own documents. In this lab you run every step of it yourself on a 4-page customer care handbook, and see where it can go wrong.

The Lab 1 page has five lettered boxes, A to E. The steps below tell you which box to use.

1. Open the Lab 1 page. Wait until the bar at the top says **Ready**. (The first visit downloads about 40 MB.)

2. Press the button in **boxes A, B and C**, in order: **Read it for me** (the page reads the handbook PDF, so you do not need to), **Split into passages**, and **Turn into numbers and store**. There is nothing to write down for these three. Just look at what each box shows.

3. In **box D**, press the **Blender, 45 days** button, then **Find the closest passages**. Write down which section came top, and whether the page calls the match strong, fair or weak.

4. Do the same for **Parcel turned up smashed**.

5. Do the same for **Gift cards**.

6. Look at **box E**. It shows the message a chatbot would be sent: the passages that were found, plus the question. Open **the expected answer** on the page. What does the blender customer get? Write it down.

**That is the end of Lab 1.**

<details><summary><b>Takeaway (open after the debrief)</b></summary>

RAG is a search, then a hand-over. The search matches on meaning, not on matching words: the handbook never says "parcel" or "smashed". But it always returns something, even when the handbook has no answer (gift cards). The model only sees what the search found.
</details>

**Optional, after the session:** if you have a laptop and a free GitHub account, the same lab runs with a full vector database and a small model that writes the answer. Steps are in the [README](README.md).

---

## Lab 2: Manage the agent

**You need:** the Lab 2 page: <https://skillrepos.github.io/tlsdemyst/mcp.html>

**Purpose:** An AI agent can take actions, not only write text. Two decisions set what it does. What you connect it to decides what it *can* reach. (MCP is a standard way to make that connection.) Your policy decides what it *may* do on its own. In this lab you see the first, then make the second as the agent's manager.

**The ticket:** *"I was charged twice for order 1182. Please refund one charge."*

The Lab 2 page has five lettered boxes (A to E). The steps below tell you which box to use.

1. Open the Lab 2 page and read **box A**: with no connection, the assistant cannot see the order. Then, in **box B**, press **Connect**. The server sends back a list of what it offers. Write down how many actions the server offers, and how many of those are marked **reads only**.

2. In **box C**, press all three buttons. (This is what the assistant would do on its own: look things up.) Then look at **box E**. It shows the message a chatbot would be sent: what came back from the server, plus the question. Open **the expected answer** under it.

3. In **box D**, press the red button to tell the server to issue a refund. Write down what happened.

4. Now you are the agent's manager. Below are seven things an agent could do to resolve the ticket. For each one:
   - put a check mark in **On the list?** if the Kettlewick server you just connected to offers it, and
   - mark one letter for what you would allow it to do **if it could**: **A** = the agent does it **alone**, **P** = a **person** approves first, **N** = **never**.

   Some of these are not on the list. Decide anyway: that is your policy for the day someone connects them.

| | What the agent could do | On the list? | A / P / N |
|---|---|---|---|
| 1 | Look up the order | | |
| 2 | List the charges on the order | | |
| 3 | Draft a reply | | |
| 4 | Send the reply | | |
| 5 | Refund $20 | | |
| 6 | Refund $500 | | |
| 7 | Change the customer's email address | | |

5. Write down the one you were least sure about.

The **On the list?** column has right answers: they come from the list the server sent back in box B, and the instructor will go over them. The **A / P / N** column is your own policy, so there is no single right answer there. The instructor will run a quick poll to see how the room split.

<details><summary><b>Takeaway (open after the debrief)</b></summary>

Two separate decisions keep an agent safe. The first is what gets connected: this server offers no refund at all, so no clever wording can make the agent issue one. The second is your policy for what it may do alone among the things it *can* reach. When the room disagrees on the second, it is not about how smart the AI is. In many companies that policy is not written down anywhere. Writing it is the company's job, not the vendor's. When your team connects an assistant to a system, ask to see the list, and ask who decided what is on it.
</details>

**Optional, after the session:** the fuller version connects a small model to a separate server and lets the model choose what to use. Steps are in the [README](README.md).

---

# Session 2: leading it

## Lab 3: See the top AI security risk

**You need:** the Lab 3 page: <https://skillrepos.github.io/tlsdemyst/injection.html>, and any chatbot (ChatGPT, Copilot, Gemini, Claude)

**Purpose:** "Prompt injection" means slipping instructions, or false facts, into something the AI reads. It is the top risk on OWASP's list for AI applications. In Lab 1 you saw that the chatbot only sees what the search finds. Kettlewick's assistant also searches its community forum, where anyone with an account can post. In this lab someone uses that to get their own text into the search.

The Lab 3 page has two lettered boxes, A and B.

1. Open the Lab 3 page. Wait until the bar at the top says **Ready**. You do not need to redo Lab 1: the page builds the same handbook search for you.

2. In **box A**, read **Try 1**, the attacker's first post. Press **Try 1: add the post and ask again**. Which passage came top?

3. Press **Copy this message**. Open a **new chat** in your chatbot, paste it and send. What did your chatbot do? Pick the closest:
   - **Fooled:** it promised a full cash refund.
   - **Held:** it said store credit (Section 1) and did not mention the post.
   - **Warned me** about the forum post.

4. In **box B**, read **Try 2**. The attacker has taken out the note to the AI and made the post sound official. Press **Try 2: swap in the edited post and ask again**.

5. Copy the new message into another **new chat** and send. What did your chatbot do this time? (Same three choices; pick the closest.)

6. Which chatbot did you use?

<details><summary><b>Takeaway (open after the debrief)</b></summary>

The attacker never touched the chatbot. They wrote a forum post that sounds like the question, so the search handed it over. A clumsy note to the AI often gets caught. A post that just sounds official often does not: in our test, the same chatbot ignored the first post and promised a full cash refund for the second. That is why "it caught it when I tried" is not a defense. Attackers do not write clumsy ones, and they get unlimited tries. Ask of any AI system: what does it search, and who can write there? Here the chatbot only wrote an answer. A support agent could have issued the refund.
</details>

---

## Lab 4: Score the proposal

**You need:** nothing (the same four questions are on your [takeaway handout](https://skillrepos.github.io/tlsdemyst/handout.pdf))

**Purpose:** This is the main exercise. You use four questions to decide whether to fund an AI proposal.

**The proposal, from Dana Ruiz, head of customer support at Kettlewick:** an AI agent answers routine support tickets on its own. It reads the ticket and the customer's emails, looks up the order, sends the reply, and can issue refunds up to $500 without asking anyone.

- **Why:** we get 50,000 tickets a month, and a person takes 9 minutes on each. The agent should cut routine tickets to under 2 minutes. I will own that number.
- **Data:** three years of tickets are in our help desk. Two versions of the refund policy are in use, and nobody has said which one is current.
- **Build:** our own developers, about 4 months. We have not looked at tools we could buy.
- **Running cost:** about 12¢ a ticket in AI fees, about $6,000 a month. No limit on steps.
- **Measuring it:** the help desk already records handling time. We have no measure of reply quality. We will review after 6 months, across all ticket types.

Some parts are strong and some are weak. Score what is written, not what you hope is true.

1. **Score each of the four questions from 1 to 3:**
   - **1** = unclear or unacceptable
   - **2** = partly answered, needs work
   - **3** = clear, backed up, acceptable

| | Question | Score (1–3) |
|---|---|---|
| 1 | **Value.** Which number moves: time, cost, quality or revenue? Who has signed up to be measured on it? | |
| 2 | **Feasibility.** Is the data available and clean? Does a bought tool already do this? Can one team own all of it? | |
| 3 | **Risk (must pass).** What can it see? What can it do without approval? What is the worst it could do if it were tricked? | |
| 4 | **Measurability (must pass).** Is there a baseline today? Can we see a result inside 90 days, on one workflow? (A baseline is today's number, measured before AI.) | |

2. For your **lowest score**, **write what you would ask** Dana before you decide. (If two are tied, pick one.)

   **What I would ask Dana:**

3. **Do not add the scores up.** Risk and Measurability must pass: a 1 on either one means "not yet", however good the Value story is.

4. **Vote:** **A** = full rollout · **B** = limited pilot · **C** = no · **D** = not yet: send it back for more evaluation.

5. **Write one condition** you would attach to your vote.

<details><summary><b>Takeaway (open after the debrief)</b></summary>

As written, the answer is D, not yet. Value is strong (a number and an owner), but Risk scores 1: the agent reads outsiders' messages, sees customer data, and refunds up to $500 with nobody approving and no step limit. Risk must pass. Attach conditions and it becomes B, a limited pilot: a person approves every refund, one ticket category for 90 days, a check on reply quality, and a step limit. Change the facts and the answer changes. That is the point of asking.
</details>

---

# More to try on your own

These three are not part of the two sessions. Each one is a short lab you can do by yourself, on the lab page, whenever you like.

## Estimate the tokens

**You need:** the lab page, or <https://platform.openai.com/tokenizer>

**Purpose:** AI is billed by the "token": a piece of a word. In this lab you find out how many tokens three short lines turn into, and why a short line can cost more than a long one.

The three lines:

| | Line | What it is |
|---|---|---|
| A | `My blender arrived broken. Please send a replacement.` | A customer's message in English |
| B | `Mi licuadora llegó rota. Por favor, envíen un reemplazo.` | The same message in Spanish |
| C | `ORD-2207 / KW-BLND-89 / 2026-11-20 / $89.00` | An order record |

Line C is the shortest of the three.

1. **Estimate first.** For each line, write down how many tokens you think it will be cut into.

2. **Count.** On the lab page, press **Count the tokens** next to each line. (If you are using OpenAI's tokenizer page instead, type each line in and read the number under "Tokens".)

3. Write the real count next to your estimate.

4. Answer two questions: Which line had the most tokens? Was it the longest line?

<details><summary><b>Takeaway (open when you have finished)</b></summary>

You pay by the token, not by the word. The same meaning in another language takes more tokens. Codes, dates and prices take more again. When a vendor quotes a price "per million tokens", ask how many tokens your kind of work turns into.
</details>

---

## Teach it your rules

**You need:** any chatbot you already use (ChatGPT, Copilot, Gemini, Claude)

**Purpose:** In Lab 1 the AI looked up Kettlewick's facts. But every company also has its own rules for what matters most, and the AI cannot guess them. In this lab you see what happens when you just ask, and then what happens when you show it a few examples.

1. **Guess first.** Read this ticket:

   > *"The same blender is $15 cheaper at another shop. Not complaining, I love Kettlewick, just thought you'd want to know!"*

   Write down the priority you would give it, using the same four levels the AI will be given: **P1-Critical**, **P2-High**, **P3-Medium** or **P4-Low**. Then write down the priority you think the AI will give it.

2. **Just ask.** Open a **new chat**. Copy everything in the box below and send it. (On the lab page there is a **Copy** button.)

```
You are a support ticket classifier for Kettlewick, an online shop that sells kitchen appliances. Give each ticket exactly one priority: P1-Critical, P2-High, P3-Medium, or P4-Low.

Present the results as a table: Ticket #, Priority, Reason (one sentence).

Ticket 1: "The same blender is $15 cheaper at another shop. Not complaining, I love Kettlewick, just thought you'd want to know!"
Ticket 2: "URGENT!!! My $45 kettle arrived with a huge dent. This is completely unacceptable. I need this sorted TODAY!!!"
Ticket 3: "Hi, could you change the email address on my account to dana.new@example.com? Thanks!"
Ticket 4: "My order shipped 12 business days ago and still hasn't arrived. It's a birthday present for Saturday."
Ticket 5: "I was charged $89 twice for my blender order. Can someone look into it?"
```

   Copy the AI's whole reply and paste it into the box under the message on the lab page. The page picks out the five priorities and puts them in the **Just ask** column in step 5, so you don't type them. (On paper, write them in that column.)

3. **Now see Kettlewick's rules.** These are the rules the company actually uses:
   - Any mention of **another shop** is **P1**, even when the customer is happy. (Keeping customers is the top goal this year.)
   - A **damaged item under $100** is **P4**. (A free replacement goes out automatically, the same day.)
   - Any request to **change an account's email address** is **P1**. (It is the most common way accounts get taken over.)
   - A parcel **10 or more business days late** is treated as lost: **P2**.
   - A **duplicate charge under $100** is **P4**. (It is refunded automatically overnight.)

   On the lab page, step 5 further down already shows which of the five the AI followed. (On paper, compare its answers with these rules.) Did it match your guess in step 1?

4. **Show it examples.** Open **another new chat**. Copy the box below and send it. It gives the AI six example tickets with Kettlewick's answers, then the same five tickets. Paste the AI's reply into the box under this message too: it fills the **With examples** column.

```
You are a support ticket classifier for Kettlewick, an online shop that sells kitchen appliances. Give each ticket exactly one priority: P1-Critical, P2-High, P3-Medium, or P4-Low.

Here is how Kettlewick prioritizes tickets, shown by example:

Ticket: "Saw a toaster sale at the shop down the road. Mine's still great though!"
Priority: P1-Critical
(Any mention of another shop is P1, even when the customer is happy. Keeping customers is our top goal this year.)

Ticket: "HELP!!! My $59 coffee grinder came with a cracked lid. I'm furious. Fix this NOW."
Priority: P4-Low
(Damaged items under $100 are P4. Our damage form sends a free replacement automatically, the same day.)

Ticket: "My new $249 stand mixer arrived with a cracked bowl."
Priority: P2-High
(Damaged items of $100 or more are P2. A person arranges the return and replacement.)

Ticket: "Can you update the email on my account? I've switched providers."
Priority: P1-Critical
(Any request to change an account's email address is P1. It is the most common way accounts get taken over, so a person checks it right away.)

Ticket: "Tracking on my order hasn't moved in 11 business days."
Priority: P2-High
(A parcel 10 or more business days late is treated as lost: P2.)

Ticket: "Looks like I paid twice for my toaster, $39 each time."
Priority: P4-Low
(A duplicate charge under $100 is P4. Our payment system finds and refunds it automatically overnight.)

Now classify these tickets. Present the results as a table: Ticket #, Priority, Reason (one sentence).

Ticket 1: "The same blender is $15 cheaper at another shop. Not complaining, I love Kettlewick, just thought you'd want to know!"
Ticket 2: "URGENT!!! My $45 kettle arrived with a huge dent. This is completely unacceptable. I need this sorted TODAY!!!"
Ticket 3: "Hi, could you change the email address on my account to dana.new@example.com? Thanks!"
Ticket 4: "My order shipped 12 business days ago and still hasn't arrived. It's a birthday present for Saturday."
Ticket 5: "I was charged $89 twice for my blender order. Can someone look into it?"
```

5. **See how the AI did.** On the lab page this fills in by itself from the two replies you pasted, and marks each answer ✓ (followed Kettlewick's rule) or ✗ (did not), with a total for each chat. Nothing here scores you. If the page could not read a reply, tap the P1–P4 buttons under each ticket to enter what the AI said. (On paper: write the AI's answers in the two columns and count how many match the rule.)

| Ticket | Kettlewick's rule | Just ask | With examples |
|---|---|---|---|
| 1 Cheaper at another shop (happy) | P1 | | |
| 2 Dented $45 kettle (angry) | P4 | | |
| 3 Change account email (polite) | P1 | | |
| 4 Parcel 12 business days late | P2 | | |
| 5 Charged $89 twice | P4 | | |
| **AI's answers that match the rule (out of 5)** | | | |

Compare the two totals: on how many of the 5 tickets did the AI follow the rule with **Just ask**, and on how many **with examples**?

**If you finish early:** write a ticket of your own that you think would fool the AI without the examples (hint: make it sound calm but break one of Kettlewick's rules, or sound furious about something minor). Paste it into both chats and compare.

<details><summary><b>Takeaway (open when you have finished)</b></summary>

The AI did not get smarter between step 2 and step 4. It was told what your company cares about. Without that, it judges by general good sense and by tone, and loud tickets look urgent. A few examples of your own rules usually fix it. When a team says "the AI keeps getting this wrong", the first question is: did anyone show it what right looks like?
</details>

---

## Start your own pilot page

**You need:** nothing

**Purpose:** This one goes home with you. You start a pilot page: a one-page plan for trying one real AI idea from your organization in one small area first, before anyone commits to more.

1. **Pick one real AI idea** from your organization: something proposed, or something already running. There is no chatbot in this lab, and your answers stay on your device (or on your paper). Describe the idea in general terms.

2. **Fill in four lines:**

| Line | Your answer |
|---|---|
| **Business problem:** what is going wrong today, in one sentence? | |
| **Scope:** which one workflow? | |
| **Owner:** one person (a name or a job title) | |
| **Success measure:** which number, from what to what? | |

3. **Mark any line you could not fill in.**

*Already have a pilot page?* Do not start a new one. Answer the Risk question from Lab 4 for your existing pilot, and write one line for what a single item will cost to run.

<details><summary><b>Takeaway (open when you have finished)</b></summary>

Any line you could not fill in is your first question when you get back.
</details>

The [takeaway handout](https://skillrepos.github.io/tlsdemyst/handout.pdf) has all seven pilot lines to finish this at home.

---

<p align="center">
<b>For educational use only by the attendees of our workshops.</b>
</p>

<p align="center">
<b>(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.</b>
</p>
