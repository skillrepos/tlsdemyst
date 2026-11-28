#!/usr/bin/env python3
"""Builds kettlewick-handbook.pdf, the sample document for the RAG lab.
Kettlewick is a made-up shop. Run: python3 build-handbook-pdf.py   (needs: pip install reportlab)"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

NAVY = colors.HexColor("#002060")
T = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=NAVY)
SUB = ParagraphStyle("s", fontName="Helvetica-Oblique", fontSize=10.5, leading=14, textColor=colors.HexColor("#555555"))
H = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=NAVY, spaceBefore=16, spaceAfter=5)
B = ParagraphStyle("b", fontName="Helvetica", fontSize=11.5, leading=16.5)

PAGES = [
 [("Section 1: Returns and refunds",
   "You can return most items for a full refund within 30 days of delivery. From day 31 to day 60 we give store credit instead of money back, minus 10% of the price. After 60 days we cannot offer a refund or store credit. The item must be clean and in its original box."),
  ("Section 2: Final-sale items",
   "Items marked final sale cannot be returned or exchanged. The words final sale appear on the product page and on your receipt. A final-sale item that arrives damaged is still covered by Section 6."),
  ("Section 3: Duplicate charges",
   "If your card was charged twice for the same order by mistake, we refund the extra charge in full, whatever the date. You do not need to return anything. The money usually reaches your card in 5 business days."),
  ("Section 4: Who approves a refund",
   "Every refund is approved by a person on the support team before it is issued. Refunds over $200 also need a supervisor. No email goes to a customer until a person on the support team has read it.")],
 [("Section 5: Shipping and delivery",
   "Standard shipping takes 3 to 5 business days and is free on orders over $50. Under $50 it costs $6. Express shipping costs $12 and takes 1 to 2 business days. We ship to addresses in the United States only."),
  ("Section 6: Damaged on arrival",
   "If an item arrives broken, cracked or dented, tell us within 14 days of delivery and include a photo. We send a free replacement. For items that cost less than $100 you do not need to send the broken one back."),
  ("Section 7: Late or lost parcels",
   "If your order has not arrived 10 business days after it shipped, we treat it as lost. You choose: we send the order again at no cost, or we refund it in full. You do not need to wait for the carrier to finish its search.")],
 [("Section 8: Warranty",
   "Appliances with a motor, such as blenders, stand mixers and coffee grinders, have a 2-year warranty. Kettles and toasters have a 1-year warranty. The warranty covers faults in how the item was made. It does not cover misuse, drops, or use in a restaurant or other business."),
  ("Section 9: Repairs and spare parts",
   "We sell spare jugs, lids, blades and filters for every appliance for 5 years after we stop selling that model. For a fault under warranty we repair or replace the item, and we pay the shipping both ways."),
  ("Section 10: Changing or cancelling an order",
   "You can change or cancel an order free of charge within 2 hours of placing it. After 2 hours the order is already being packed, so we cannot stop it. Wait for it to arrive and then return it under Section 1.")],
 [("Section 11: Price promise",
   "If we lower the price of an item within 14 days of your purchase, ask us and we refund the difference to your card. The price promise does not apply to final-sale items or to prices at other shops."),
  ("Section 12: Loyalty points",
   "You earn 1 point for every dollar you spend. Every 100 points is worth $5 off a later order. Points expire if you make no purchase for 12 months. When an order is refunded, the points it earned are removed."),
  ("Section 13: Contacting us",
   "The support team is open from 8 a.m. to 8 p.m. Eastern time, Monday to Saturday. We answer email within one business day. Have your order number ready; it is on your receipt and starts with the letters ORD."),
  ("Section 14: Keeping your account safe",
   "We never ask for your password or your full card number by email or by phone. Changing the email address on an account is checked by a person on the support team before it takes effect.")],
]

def build(out="kettlewick-handbook.pdf"):
    s = [Paragraph("Kettlewick Customer Care Handbook", T), Spacer(1, 4),
         Paragraph("Kettlewick is a made-up shop used for training. Nothing in this handbook is a real policy.", SUB), Spacer(1, 6)]
    for i, page in enumerate(PAGES):
        if i: s.append(PageBreak())
        for head, body in page:
            s += [Paragraph(head, H), Paragraph(body, B)]
    SimpleDocTemplate(out, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.9 * inch, bottomMargin=0.9 * inch,
                      title="Kettlewick Customer Care Handbook", author="Tech Skills Transformations (training sample)").build(s)
    print("wrote", out)

if __name__ == "__main__":
    build()
