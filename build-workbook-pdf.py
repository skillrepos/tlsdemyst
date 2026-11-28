#!/usr/bin/env python3
"""Builds lab-workbook.pdf for the 2-hour version of AI Demystified for Tech Leaders: four labs, and three to try on your own, as a PDF you can
type into (form fields) or print and write on. Nine sides: page 1 is how to use it, session 1 is pages 2-3, session 2 is pages 4-5, the three to try on your own are pages 6-8, takeaways on page 9.
Form field names were kept from the 3-hour version: Score the proposal still starts l9_, the pilot page l10_, RAG l2_, Manage the agent l4_, the security lab l5_.
Run:  python3 build-workbook-pdf.py [output.pdf]      (needs: pip install reportlab)
SITE below is the address of the lab page; change it here if the repository name changes.
The wording must match labs.md and index.html; check-labs.py compares the three."""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

SITE = "skillrepos.github.io/tlsdemyst"
OUT = sys.argv[1] if len(sys.argv) > 1 else "lab-workbook.pdf"

NAVY = colors.HexColor("#002060"); ORANGE = colors.HexColor("#ED7D31"); GREY = colors.HexColor("#4A5360")
LINE = colors.HexColor("#B8C0CC"); PALE = colors.HexColor("#DCE9F7"); YEL = colors.HexColor("#FFF6D6")
YLINE = colors.HexColor("#E0B400"); FIELD = colors.HexColor("#F5F8FC"); FLINE = colors.HexColor("#7A8696")
SAMPLE = colors.HexColor("#F3F4F6"); PURPLE = colors.HexColor("#7030A0"); LILAC = colors.HexColor("#EFE6F6")
PW, PH = letter; M = 0.7 * inch; W = PW - 2 * M; IND = 30  # IND: step text starts this far in

def st(**kw):
    base = dict(fontName="Helvetica", fontSize=11, leading=15, textColor=colors.black)
    base.update(kw); return ParagraphStyle("s", **base)
BODY = st(); SMALL = st(fontSize=9.5, leading=12.5, textColor=GREY); BOLD = st(fontName="Helvetica-Bold")
MONO = st(fontName="Courier", fontSize=10.5, leading=14); TH = st(fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=colors.white)
TD = st(fontSize=10.5, leading=13.5); TDB = st(fontName="Helvetica-Bold", fontSize=10.5, leading=13.5)
WHY = st(fontSize=10.5, leading=14.5, textColor=colors.HexColor("#12305A")); TAKE = st(fontSize=10.5, leading=14.5, textColor=colors.HexColor("#3D1A5C"))

class Doc:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=letter)
        self.c.setTitle("AI Demystified for Tech Leaders - Lab workbook"); self.c.setAuthor("Brent Laster, Tech Skills Transformations LLC")
        self.form = self.c.acroForm; self.page = 0; self.y = 0; self.stepn = 0; self.names = set()
    # ---- pages ----
    def new_page(self, session):
        if self.page:
            assert self.y >= 0.62 * inch, f"page {self.page} overflows: y={self.y:.0f}"
            self.c.showPage()
        self.page += 1; c = self.c
        c.setFont("Helvetica-Bold", 9); c.setFillColor(GREY); c.drawString(M, PH - 0.45 * inch, "AI Demystified for Tech Leaders — Lab workbook")
        c.setFont("Helvetica", 9); c.drawRightString(PW - M, PH - 0.45 * inch, session)
        c.setStrokeColor(ORANGE); c.setLineWidth(1.2); c.line(M, PH - 0.52 * inch, PW - M, PH - 0.52 * inch)
        c.setFont("Helvetica", 8); c.setFillColor(GREY)
        c.drawString(M, 0.42 * inch, "© 2026 Brent C. Laster & Tech Skills Transformations LLC · For educational use only by the attendees of our workshops.")
        c.drawRightString(PW - M, 0.42 * inch, f"Page {self.page} of 9")
        self.y = PH - 0.8 * inch
    def gap(self, h): self.y -= h
    # ---- text ----
    def para(self, text, style=BODY, x=0, w=None, after=4):
        p = Paragraph(text, style); w = (W - x) if w is None else w
        _, h = p.wrapOn(self.c, w, 2000); p.drawOn(self.c, M + x, self.y - h); self.y -= h + after; return h
    def boxed(self, text, style, fill, stroke=None, x=0, w=None, pad=7, after=8, bar=None):
        w = (W - x) if w is None else w; p = Paragraph(text, style); _, h = p.wrapOn(self.c, w - 2 * pad, 2000)
        c = self.c; c.setFillColor(fill); c.setStrokeColor(stroke or fill); c.setLineWidth(0.8)
        c.roundRect(M + x, self.y - h - 2 * pad, w, h + 2 * pad, 4, fill=1, stroke=1 if stroke else 0)
        if bar: c.setFillColor(bar); c.rect(M + x, self.y - h - 2 * pad, 3, h + 2 * pad, fill=1, stroke=0)
        p.drawOn(c, M + x + pad, self.y - h - pad); self.y -= h + 2 * pad + after
    def lab(self, n, title, meta, why):
        c = self.c; self.stepn = 0
        # Lab badge: bigger, darker orange so white text stays readable (BC, 11/24)
        c.setFillColor(colors.HexColor("#C55A11")); c.roundRect(M, self.y - 30, 78, 30, 5, fill=1, stroke=0)
        own = isinstance(n, str)                      # the three labs to try on your own have a grey label, not a number
        if own: c.setFillColor(GREY); c.roundRect(M, self.y - 30, 78, 30, 5, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9.5 if own else 16); c.drawCentredString(M + 39, self.y - (19 if own else 20.5), n if own else f"LAB {n}")
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 19); c.drawString(M + 90, self.y - 21.5, title)
        self.y -= 33; self.para(meta, SMALL, after=7)
        self.boxed("<b>Why:</b> " + why, WHY, PALE, after=10)
    def step(self, text, after=5):
        self.stepn += 1; c = self.c
        c.setFillColor(NAVY); c.circle(M + 10, self.y - 8, 10, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 10.5); c.drawCentredString(M + 10, self.y - 11.7, str(self.stepn))
        self.para(text, BODY, x=IND, after=after)
    # ---- form fields ----
    def _name(self, name):
        assert name not in self.names, name; self.names.add(name); return name
    def text(self, name, x, y, w, h=20, multiline=False, size=10.5):
        self.form.textfield(name=self._name(name), x=M + x, y=y, width=w, height=h, fontName="Helvetica", fontSize=size,
                            borderWidth=0.75, borderColor=FLINE, fillColor=FIELD, textColor=colors.black, forceBorder=True,
                            fieldFlags="multiline" if multiline else "", maxlen=2000 if multiline else 200, tooltip=name)
    def field(self, label, name, x=IND, w=None, h=20, multiline=False, after=8, label_style=None):
        """A label with a box under it."""
        w = (W - x) if w is None else w
        if label: self.para(label, label_style or BOLD, x=x, w=W - x, after=2)
        self.text(name, x, self.y - h, w, h, multiline); self.y -= h + after
    def inline(self, items, x=IND, h=20, after=8, gap=16):
        """Several 'label [box]' pairs on one line. items: (label, name, box width)."""
        c = self.c; cx = x
        for label, name, bw in items:
            c.setFont("Helvetica-Bold", 11); c.setFillColor(colors.black); c.drawString(M + cx, self.y - 14, label)
            cx += c.stringWidth(label, "Helvetica-Bold", 11) + 6
            self.text(name, cx, self.y - h, bw, h); cx += bw + gap
        self.y -= h + after
    def radios(self, label, group, options, x=IND, after=8, size=13, gap=18):
        c = self.c; cx = x
        if label:
            c.setFont("Helvetica-Bold", 11); c.setFillColor(colors.black); c.drawString(M + cx, self.y - 12, label)
            cx += c.stringWidth(label, "Helvetica-Bold", 11) + 12
        self._name(group)
        for opt in options:
            self.form.radio(name=group, value=opt.replace(" ", "_"), x=M + cx, y=self.y - 14, size=size, buttonStyle="circle", shape="square",
                            borderWidth=0.75, borderColor=FLINE, fillColor=FIELD, textColor=NAVY, forceBorder=True, selected=False)
            c.setFont("Helvetica", 11); c.setFillColor(colors.black); c.drawString(M + cx + size + 4, self.y - 12, opt)
            cx += size + 4 + c.stringWidth(opt, "Helvetica", 11) + gap
        self.y -= 16 + after
    def check(self, name, x, y, size=14):
        self.form.checkbox(name=self._name(name), x=M + x, y=y, size=size, buttonStyle="check", borderWidth=0.75, borderColor=FLINE,
                           fillColor=FIELD, textColor=NAVY, forceBorder=True, checked=False)
    # ---- tables ----
    def table(self, widths, head, rows, x=0, min_h=21, after=10, pad=5):
        """Cells: 'text' | ('b','text') | ('f', name) | ('fm', name) multiline | ('r', group, [opts]) | ('c', name) | None."""
        c = self.c; x0 = M + x
        def cell_h(cell, w):
            if isinstance(cell, str) or (isinstance(cell, tuple) and cell[0] == 'b'):
                t = cell if isinstance(cell, str) else cell[1]
                return Paragraph(t, TD if isinstance(cell, str) else TDB).wrapOn(c, w - 2 * pad, 2000)[1] + 2 * pad
            return 0
        if head:
            hh = max(Paragraph(t, TH).wrapOn(c, w - 2 * pad, 2000)[1] for t, w in zip(head, widths)) + 2 * pad
            c.setFillColor(NAVY); c.rect(x0, self.y - hh, sum(widths), hh, fill=1, stroke=0); cx = x0
            for t, w in zip(head, widths):
                p = Paragraph(t, TH); _, h = p.wrapOn(c, w - 2 * pad, 2000); p.drawOn(c, cx + pad, self.y - pad - h); cx += w
            self.y -= hh
        for row in rows:
            rh = row[-1] if isinstance(row[-1], (int, float)) else None
            cells = row[:-1] if rh is not None else row
            h = max([rh or min_h] + [cell_h(cl, w) for cl, w in zip(cells, widths)]); cx = x0
            for cl, w in zip(cells, widths):
                c.setStrokeColor(LINE); c.setLineWidth(0.6); c.rect(cx, self.y - h, w, h, fill=0, stroke=1)
                if isinstance(cl, str) or (isinstance(cl, tuple) and cl[0] == 'b'):
                    p = Paragraph(cl if isinstance(cl, str) else cl[1], TD if isinstance(cl, str) else TDB)
                    _, ph = p.wrapOn(c, w - 2 * pad, 2000); p.drawOn(c, cx + pad, self.y - (h + ph) / 2)
                elif cl and cl[0] in ('f', 'fm'):
                    self.text(cl[1], cx - M + 3, self.y - h + 3, w - 6, h - 6, multiline=(cl[0] == 'fm'))
                elif cl and cl[0] == 'c':
                    self.check(cl[1], cx - M + (w - 14) / 2, self.y - (h + 14) / 2)
                elif cl and cl[0] == 'r':
                    self._name(cl[1]); n = len(cl[2]); slot = (w - 8) / n
                    for i, opt in enumerate(cl[2]):
                        bx = cx + 4 + i * slot
                        self.form.radio(name=cl[1], value=opt, x=bx, y=self.y - (h + 12) / 2, size=12, buttonStyle="circle", shape="square",
                                        borderWidth=0.75, borderColor=FLINE, fillColor=FIELD, textColor=NAVY, forceBorder=True, selected=False)
                        c.setFont("Helvetica", 10); c.setFillColor(colors.black); c.drawString(bx + 15, self.y - h / 2 - 3.5, opt)
                cx += w
            self.y -= h
        self.y -= after
    def qr(self, url, x, y, size):
        w = QrCodeWidget("https://" + url, barLevel="M", barFillColor=NAVY); b = w.getBounds(); s = size / (b[2] - b[0])
        d = Drawing(size, size, transform=[s, 0, 0, s, 0, 0]); d.add(w); renderPDF.draw(d, self.c, M + x, y)
    def save(self):
        assert self.page == 9, self.page
        assert self.y >= 0.62 * inch, f"page {self.page} overflows: y={self.y:.0f}"; self.c.save()

d = Doc(OUT)
S1, S2, MORE = "Session 1: the technology", "Session 2: leading it", "More to try on your own"

# ---------------- page 1: how to use, and what is in the workbook ----------------
d.new_page("How to use this workbook")
d.c.setFillColor(NAVY); d.c.setFont("Helvetica-Bold", 20); d.c.drawString(M, d.y - 18, "Lab workbook"); d.y -= 30
qs = 78; top = d.y
tw = W - qs - 16
d.para("There are <b>four short labs</b>: two in session 1 and two in session 2. We do them one at a time during the session; each lab’s slide shows its number. You do every lab on your own, and there is nothing to install. <b>Three more</b>, on pages 6 to 8, are for you to try on your own afterwards. Labs 1, 2 and 3 also have their own page on the lab site, where you press the buttons to run the lab; you write your answers here.", BODY, w=tw, after=5)
d.para("<b>How to fill this in:</b> type into the shaded boxes, or print it and write on it. The same labs are on the lab page, where most of them have something to press or copy:", BODY, w=tw, after=3)
d.para(f"<b>{SITE}</b> &nbsp;— or scan the code. If your work laptop blocks it, use your phone.", BODY, w=tw, after=8)
d.qr(SITE, W - qs, top - qs, qs)
d.y = min(d.y, top - qs - 6)
d.boxed("<b>One rule: never paste company data into a chatbot.</b> Every lab here that uses a chatbot uses only the sample text in these labs. “Start your own pilot page” (page 8) is about your own work, but it uses no chatbot, and your answers stay with you. Kettlewick is a made-up shop.", st(fontSize=10.5, leading=14, textColor=colors.HexColor("#5A4500")), YEL, YLINE, after=16)

d.gap(6)
d.c.setFillColor(NAVY); d.c.setFont("Helvetica-Bold", 14); d.c.drawString(M, d.y - 12, "What is in this workbook"); d.y -= 22
d.table([64, 250, 150, 44], ["", "Lab", "You need", "Page"], [
    [("b", "Session 1"), "<b>Lab 1</b> · Real RAG, in your browser", "The Lab 1 page", "2", 24],
    [("b", ""), "<b>Lab 2</b> · Manage the agent", "The Lab 2 page", "3", 24],
    [("b", "Session 2"), "<b>Lab 3</b> · See the top AI security risk", "The Lab 3 page and any chatbot", "4", 24],
    [("b", ""), "<b>Lab 4</b> · Score the proposal", "Nothing", "5", 24],
    [("b", "On your own"), "Estimate the tokens", "The lab page", "6", 24],
    [("b", ""), "Teach it your rules", "Any chatbot", "7", 24],
    [("b", ""), "Start your own pilot page", "Nothing", "8", 24],
    [("b", ""), "Takeaways, one for each lab", "", "9", 24],
], x=0, after=10)
d.para("The first four are the labs we do together. The three marked “On your own” are not part of the two sessions: do them whenever you like.", SMALL)
# ---------------- page 2: Lab 1 (RAG) ----------------
d.new_page(S1)
d.lab(1, "Real RAG, in your browser", "On your own · uses the Lab 1 page on a phone or laptop",
      "RAG is how an AI system answers from your own documents. Here you run every step of it yourself on a 4-page customer care handbook, and see where it can go wrong.")
top = d.y; qs = 84; tw = W - qs - 16
d.para(f"<b>Open the Lab 1 page:</b> {SITE}/rag.html — or scan the code.", BODY, w=tw, after=5)
d.para("The Lab 1 page has <b>five lettered boxes (A to E)</b>. The steps below tell you which box to use. Write your answers here.", BODY, w=tw, after=5)
d.qr(SITE + "/rag.html", W - qs, top - qs + 4, qs); d.y = min(d.y, top - qs - 2); d.gap(8)
d.step("Wait until the bar at the top of the Lab 1 page says <b>Ready</b>. (The first visit downloads about 40 MB.)", after=12)
d.step("Press the button in <b>boxes A, B and C</b>, in order: <b>Read it for me</b> (the page reads the PDF, so you do not need to), <b>Split into passages</b>, and <b>Turn into numbers and store</b>. There is nothing to write down for these three. Just look at what each box shows.", after=16)
d.step("In <b>box D</b>, press a question button, then <b>Find the closest passages</b>. Do this for all three questions. For each, write which section came top and how strong the page says the match is.", after=8)
d.table([140, 160, W - IND - 300], ["Question button", "Top passage it found (section)", "How strong is the match?"], [
    ["Blender, 45 days", ("f", "l2_q1_sec"), ("r", "l2_q1_match", ["Strong", "Fair", "Weak"]), 32],
    ["Parcel turned up smashed", ("f", "l2_q2_sec"), ("r", "l2_q2_match", ["Strong", "Fair", "Weak"]), 32],
    ["Gift cards", ("f", "l2_q3_sec"), ("r", "l2_q3_match", ["Strong", "Fair", "Weak"]), 32],
], x=IND, after=16)
d.step("Press the <b>Blender, 45 days</b> question again. Then look at <b>box E</b>: it shows the message a chatbot would be sent, which is the passages that were found plus the question. Open <b>the expected answer</b> under it.", after=8)
d.field("What does the blender customer get?", "l2_answer", h=24, after=18)
d.para(f"<b>Optional, after the session:</b> with a laptop and a free GitHub account you can run the same lab with a full vector database and a small model that writes the answer. Steps: github.com/skillrepos/tlsdemyst", SMALL)

# ---------------- page 3: Lab 2 (Manage the agent) ----------------
d.new_page(S1)
d.lab(2, "Manage the agent", "On your own · uses the Lab 2 page on a phone or laptop",
      "An AI agent can take actions, not only write text. What you connect it to decides what it <i>can</i> reach (MCP is a standard way to connect it). Your policy decides what it <i>may</i> do on its own. Here you see the first, then decide the second.")
top = d.y; qs = 78; tw = W - qs - 16
d.para(f"<b>Open the Lab 2 page:</b> {SITE}/mcp.html — or scan the code, or tap <b>Lab 2: Manage the agent</b> at the top of the lab page.", BODY, w=tw, after=5)
d.para("The Lab 2 page has <b>five lettered boxes (A to E)</b>. The steps below tell you which box to use. Write your answers here.", BODY, w=tw, after=5)
d.qr(SITE + "/mcp.html", W - qs, top - qs + 4, qs); d.y = min(d.y, top - qs - 2); d.gap(4)
d.boxed("<b>The ticket:</b> <i>“I was charged twice for order 1182. Please refund one charge.”</i>", BODY, SAMPLE, bar=NAVY, after=6)
d.step("Read <b>box A</b>: with no connection, the assistant cannot see the order. Then, in <b>box B</b>, press <b>Connect</b>. The server sends back a list of what it offers.", after=4)
d.inline([("How many actions does it offer?", "l4_offers", 46), ("How many say “reads only”?", "l4_readonly", 46)], after=5)
d.step("In <b>box C</b>, press all three buttons. This is what the assistant would do on its own: look things up.", after=4)
d.step("In <b>box D</b>, press the red button to tell the server to issue a refund.", after=4)
d.field("What happened?", "l4_refund", h=22, after=5)
d.step("<b>Now you are the agent’s manager.</b> For each action, put a check mark under <b>On the list?</b> if the server you just connected to offers it. Then choose what you would allow it to do <b>if it could</b>.", after=3)
d.para("<b>Alone</b> = the agent does it by itself &nbsp;·&nbsp; <b>Person</b> = a person approves first &nbsp;·&nbsp; <b>Never</b> = not allowed", st(fontSize=10.5, leading=14), x=IND, after=6)
acts = ["Look up the order", "List the charges on the order", "Draft a reply", "Send the reply", "Refund $20", "Refund $500", "Change the customer’s email address"]
d.table([210, 70, W - IND - 280], ["What the agent could do", "On the list?", "Your answer"],
        [[f"{i+1}. {a}", ("c", f"l4_list_{i}"), ("r", f"l4_act_{i}", ["Alone", "Person", "Never"]), 21] for i, a in enumerate(acts)], x=IND, after=5)
d.step("<b>Which one were you least sure about?</b> The <b>On the list?</b> column has right answers; your Alone / Person / Never choices are your own policy.", after=4)
d.field(None, "l4_unsure", h=22, after=0)

# ---------------- page 4: Lab 3 (security) ----------------
d.new_page(S2)
d.lab(3, "See the top AI security risk", "On your own · uses the Lab 3 page, and any chatbot (ChatGPT, Copilot, Gemini, Claude)",
      "“Prompt injection” means slipping instructions, or false facts, into something the AI reads. It is the top risk on OWASP’s list for AI applications. Kettlewick’s assistant also searches its community forum, where anyone can post. Here someone uses that to get their own text into the search.")
d.step("Open the Lab 3 page (skillrepos.github.io/tlsdemyst/injection.html). Wait for <b>Ready</b>. You do not need to redo Lab 1.", after=6)
d.step("In <b>box A</b>, read <b>Try 1</b>, the attacker’s first post. Press <b>Try 1: add the post and ask again</b>.", after=4)
d.inline([("Which passage came top?", "l5_top", 230)], after=6)
d.step("Press <b>Copy this message</b>, paste it into a <b>new chat</b> in your chatbot and send. What did it do? Pick the closest.", after=4)
d.radios(None, "l5_try1", ["Fooled (full cash refund)", "Held (store credit)", "Warned me about the post"], gap=14, after=6)
d.step("In <b>box B</b>, read <b>Try 2</b>: no note to the AI, it just sounds official. Press <b>Try 2: swap in the edited post and ask again</b>.", after=6)
d.step("Copy the new message into another <b>new chat</b> and send. What did it do this time? Pick the closest.", after=4)
d.radios(None, "l5_try2", ["Fooled (full cash refund)", "Held (store credit)", "Warned me about the post"], gap=14, after=6)
d.inline([("Which chatbot did you use?", "l5_which", 200)], after=14)

# ---------------- page 5: Lab 4 (Score the proposal) ----------------
d.new_page(S2)
d.lab(4, "Score the proposal", "On your own · the main exercise",
      "You use four questions to decide whether to fund an AI proposal. The same four are on your takeaway handout: skillrepos.github.io/tlsdemyst/handout.pdf")
d.boxed("<b>The proposal, from Dana Ruiz, head of customer support:</b> an AI agent answers routine tickets on its own. It reads the ticket and the customer’s emails, looks up the order, sends the reply, and can issue refunds up to $500 without asking anyone.<br/>"
        "• <b>Why:</b> 50,000 tickets a month; a person takes 9 minutes on each. Target: under 2 minutes for routine tickets. I will own that number.<br/>"
        "• <b>Data:</b> three years of tickets in our help desk. Two versions of the refund policy are in use; nobody has said which is current.<br/>"
        "• <b>Build:</b> our own developers, about 4 months. We have not looked at tools we could buy.<br/>"
        "• <b>Running cost:</b> about 12¢ a ticket in AI fees, about $6,000 a month. No limit on steps.<br/>"
        "• <b>Measuring it:</b> handling time is recorded today; reply quality is not. Review after 6 months, across all ticket types.", st(fontSize=10.5, leading=13), SAMPLE, bar=NAVY, after=4)
d.step("<b>Score each question</b> (what is written, not what you hope). Then write what you would ask Dana about your <b>lowest</b> score.", after=3)
d.para("<b>1</b> = unclear or unacceptable &nbsp;·&nbsp; <b>2</b> = partly answered, needs work &nbsp;·&nbsp; <b>3</b> = clear, backed up, acceptable", st(fontSize=10.5, leading=14), x=IND, after=5)
qs4 = [("value", "1. Value", "Which number moves: time, cost, quality or revenue? Who has signed up to be measured on it?"),
       ("feas", "2. Feasibility", "Is the data available and clean? Does a bought tool already do this? Can one team own all of it?"),
       ("risk", "3. Risk <font color='#C00000'>(must pass)</font>", "What can it see? What can it do without approval? What is the worst it could do if it were tricked?"),
       ("meas", "4. Measurability <font color='#C00000'>(must pass)</font>", "Is there a baseline today? Can we see a result inside 90 days, on one workflow? <i>(A baseline is today’s number, measured before AI.)</i>")]
d.table([W - IND - 110, 110], ["Question", "Score"],
        [[f"<b>{n}</b><br/>{q}", ("r", f"l9_{k}", ["1", "2", "3"]), 30] for k, n, q in qs4], x=IND, after=4)
d.inline([("What I would ask Dana (lowest score):", "l9_ask", 276)], after=8)
d.step("<b>Do not add the scores up.</b> Risk and Measurability must pass: a 1 on either one means “not yet”.", after=5)
d.step("<b>Vote.</b>", after=6)
d.radios(None, "l9_vote", ["A · full rollout", "B · limited pilot", "C · no", "D · not yet: send it back"], gap=26, after=3)
d.step("<b>Write one condition you would attach to your vote.</b>", after=5)
d.field(None, "l9_condition", h=26, multiline=True)

# ---------------- page 6: on your own: Estimate the tokens ----------------
d.new_page(MORE)
d.lab("ON YOUR OWN", "Estimate the tokens", "On your own · uses the lab page (or platform.openai.com/tokenizer)",
      "AI is billed by the “token”: a piece of a word. Here you find out how many tokens three short lines are cut into, and why a short line can cost more than a long one.")
d.step("<b>Estimate first.</b> For each line in the table, write how many tokens you think it takes. Line C is the shortest of the three.")
d.step(f"<b>Then count.</b> On the lab page ({SITE}), go to “Estimate the tokens” near the bottom, type your estimate and press <b>Count the tokens</b>. Write the real count beside it.", after=3)
d.para("No lab page? Open platform.openai.com/tokenizer, type each line in exactly, and read the number under “Tokens”.", SMALL, x=IND, after=8)
d.table([22, 300, 66, 80], ["", "The line", "Estimate", "Tokens"], [
    [("b", "A"), "My blender arrived broken. Please send a replacement.<br/><font size=9 color='#4A5360'>A customer’s message in English</font>", ("f", "l1_a_guess"), ("f", "l1_a_count"), 38],
    [("b", "B"), "Mi licuadora llegó rota. Por favor, envíen un reemplazo.<br/><font size=9 color='#4A5360'>The same message in Spanish</font>", ("f", "l1_b_guess"), ("f", "l1_b_count"), 38],
    [("b", "C"), "ORD-2207 / KW-BLND-89 / 2026-11-20 / $89.00<br/><font size=9 color='#4A5360'>An order record</font>", ("f", "l1_c_guess"), ("f", "l1_c_count"), 38],
], x=IND, after=12)
d.step("<b>Answer two questions.</b>", after=6)
d.radios("Which line had the most tokens?", "l1_most", ["A", "B", "C"])
d.radios("Was it the longest line?", "l1_longest", ["Yes", "No"])

# ---------------- page 7: on your own: Teach it your rules ----------------
d.new_page(MORE)
d.lab("ON YOUR OWN", "Teach it your rules", "On your own · uses any chatbot (ChatGPT, Copilot, Gemini, Claude) and the lab page",
      "Every company has its own rules for what matters most, and the AI cannot guess them. Here you see what happens when you just ask, then when you show it a few examples.")
top = d.y; qs = 72; tw = W - qs - 16
d.para(f"<b>The two messages you send are long.</b> Copy them from “Teach it your rules” on the lab page: {SITE}/#rules — or scan the code. Write your answers here.", BODY, w=tw, after=5)
d.qr(SITE + "/#rules", W - qs, top - qs + 4, qs); d.y = min(d.y, top - qs + 2); d.gap(2)
d.step("<b>Guess first.</b> Read this ticket:", after=4)
d.boxed("<i>“The same blender is $15 cheaper at another shop. Not complaining, I love Kettlewick, just thought you'd want to know!”</i>", TD, SAMPLE, x=IND, bar=NAVY, after=4)
d.radios("The priority I would give it", "l3r_mine", ["P1", "P2", "P3", "P4"], after=2)
d.radios("The priority I think the AI will give it", "l3r_guess", ["P1", "P2", "P3", "P4"], after=0)
d.para("The same four levels the AI is given: <b>P1</b> = Critical &nbsp;·&nbsp; <b>P2</b> = High &nbsp;·&nbsp; <b>P3</b> = Medium &nbsp;·&nbsp; <b>P4</b> = Low", SMALL, x=IND, after=6)
d.step("<b>Just ask.</b> Open a <b>new chat</b>. Copy the first message (“Just ask”) from the lab page and send it. Write the AI’s five answers in the <b>Just ask</b> column in step 5.", after=5)
d.step("<b>Now see Kettlewick’s rules.</b> These are the rules the company actually uses:", after=3)
for r in ["Any mention of <b>another shop</b> is <b>P1</b>, even when the customer is happy.",
          "A <b>damaged item under $100</b> is <b>P4</b>. (A free replacement goes out automatically.)",
          "Any request to <b>change an account’s email address</b> is <b>P1</b>. (The most common way accounts get taken over.)",
          "A parcel <b>10 or more business days late</b> is treated as lost: <b>P2</b>.",
          "A <b>duplicate charge under $100</b> is <b>P4</b>. (It is refunded automatically overnight.)"]:
    d.para("• " + r, st(fontSize=10.5, leading=13.5), x=IND + 8, after=1)
d.gap(4)
d.step("<b>Show it examples.</b> Open <b>another new chat</b>. Copy the second message (“With examples”) and send it. It gives the AI six example tickets with Kettlewick’s answers, then the same five tickets.", after=5)
d.step("<b>Score the AI.</b> Mark what it said in each chat; count how many match Kettlewick’s rule.", after=4)
tk = ["1. Cheaper at another shop (happy)", "2. Dented $45 kettle (angry)", "3. Change account email (polite)", "4. Parcel 12 business days late", "5. Charged $89 twice"]
rules = ["P1", "P4", "P1", "P2", "P4"]
cw = (W - IND - 190 - 46) / 2
d.table([190, 46, cw, cw], ["Ticket", "Rule", "Just ask", "With examples"],
        [[t, ("b", r), ("r", f"l3r_plain_{i}", ["P1", "P2", "P3", "P4"]), ("r", f"l3r_ex_{i}", ["P1", "P2", "P3", "P4"]), 21] for i, (t, r) in enumerate(zip(tk, rules))]
        + [[("b", "AI matched the rule (of 5)"), "", ("f", "l3r_plain_right"), ("f", "l3r_ex_right"), 22]], x=IND, after=6)
d.para("How many did the AI get right with Just ask? How many with examples? <b>Want to go further?</b> Write a ticket that would fool the AI without the examples, and try it in both chats.", SMALL, x=IND)

# ---------------- page 8: on your own: Start your own pilot page ----------------
d.new_page(MORE)
d.lab("ON YOUR OWN", "Start your own pilot page", "On your own · this one goes home with you",
      "You start a pilot page: a one-page plan for trying one real AI idea from your organization in one small area first. Then you see whether any part of it is still unanswered.")
d.step("<b>Pick one real AI idea</b> from your organization: something proposed, or something already running. There is no chatbot in this lab, and your answers stay with you. Describe the idea in general terms.", after=6)
d.field("The idea", "l10_idea", h=26, after=16)
d.step("<b>Fill in four lines.</b> Leave a line empty if you cannot answer it.", after=8)
d.field("Business problem <font face='Helvetica' color='#4A5360'>· what is going wrong today, in one sentence?</font>", "l10_problem", h=52, multiline=True, after=10)
d.field("Scope <font face='Helvetica' color='#4A5360'>· which one workflow?</font>", "l10_scope", h=34, multiline=True, after=10)
d.field("Owner <font face='Helvetica' color='#4A5360'>· one person (a name or a job title)</font>", "l10_owner", h=26, after=10)
d.field("Success measure <font face='Helvetica' color='#4A5360'>· which number, from what to what?</font>", "l10_measure", h=34, multiline=True, after=16)
d.step("<b>Which line could you not fill in?</b>", after=6)
d.radios(None, "l10_stuck", ["Business problem", "Scope", "Owner", "Success measure", "None"], gap=14, after=20)
d.boxed("<b>Already have a pilot page?</b> Do not start a new one. Answer the Risk question from Lab 4 for your existing pilot, and write one line for what a single item will cost to run.", BODY, SAMPLE, after=8)
d.field("What one item will cost to run", "l10_cost", x=0, h=26)

# ---------------- page 9: takeaways ----------------
d.new_page("Both sessions")
d.c.setFillColor(NAVY); d.c.setFont("Helvetica-Bold", 20); d.c.drawString(M, d.y - 18, "Takeaways"); d.y -= 30
d.para("One for each lab. Read each of the first four after its debrief, and the last three when you have finished them.", SMALL, after=10)
takes = [
 ("1 · Real RAG, in your browser", "RAG is a search, then a hand-over. The search matches on meaning, not on matching words: the handbook never says “parcel” or “smashed”. But it always returns something, even when the handbook has no answer (gift cards). The model only sees what the search found."),
 ("2 · Manage the agent", "Two decisions keep an agent safe: what gets connected (this server offers no refund, so no wording can make the agent issue one), and your policy for what it may do alone among the things it can reach. That policy is often not written down. Writing it is the company’s job, not the vendor’s."),
 ("3 · See the top AI security risk", "The attacker never touched the chatbot. A forum post written to sound like the question got handed over by the search. A clumsy note to the AI often gets caught; a post that just sounds official often does not. Ask of any AI system: what does it search, and who can write there?"),
 ("4 · Score the proposal", "As written, the answer is D, not yet: Value is strong, but Risk scores 1 (outsiders’ messages, customer data, refunds up to $500 with nobody approving, no step limit), and Risk must pass. With conditions it becomes B: a person approves every refund, one ticket category for 90 days, a quality check, a step limit. Change the facts and the answer changes."),
 ("On your own · Estimate the tokens", "You pay by the token, not by the word. The same meaning in another language takes more tokens. Codes, dates and prices take more again. When a vendor quotes a price “per million tokens”, ask how many tokens your kind of work turns into."),
 ("On your own · Teach it your rules", "The AI did not get smarter between step 2 and step 4. It was told what your company cares about. Without that, it judges by general good sense and by tone, and loud tickets look urgent. When a team says “the AI keeps getting this wrong”, ask: did anyone show it what right looks like?"),
 ("On your own · Start your own pilot page", "Any line you could not fill in is your first question when you get back."),
]
for t, body in takes:
    d.boxed(f"<b>{t}.</b> {body}", TAKE, LILAC, after=6, pad=6)
print("lowest y on last page:", round(d.y), "(bottom margin is", round(0.6 * inch), ")")
d.save()
