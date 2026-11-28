---
name: kettlewick-ticket
description: Handle a Kettlewick customer-support ticket from start to finish. Sets the ticket's priority by Kettlewick's rules, checks the order and its charges, and drafts a reply in Kettlewick's house style for a person to approve. Use whenever someone asks to handle, work, answer or prioritize a Kettlewick ticket or customer email.
---

# Handling a Kettlewick ticket

*Kettlewick is a made-up shop used for training demos.*

Follow these steps in order. Never send an email and never issue a refund: a person on the support team does both.

## Steps

1. **Read the customer's email** and find the order number.
2. **Look up the order** in `orders.csv`.
3. **If the email mentions a charge**, run this from the folder's top level and use what it prints:
   `python3 .agents/skills/kettlewick-ticket/scripts/find_duplicate_charges.py charges.csv <order number>`
4. **Set the priority** with the rules below. Go by the rules, not by how upset the customer sounds.
5. **Check `refund-policy.md`** for what the customer is owed and who must approve it.
6. **Write the reply** using `reply-template.md` (in this skill's folder). Save it as `replies/order-<order number>-reply.md`.
7. **Finish with a short summary in the chat**: the priority and the rule that set it, what you found, and what a person needs to approve.

## Kettlewick's priority rules

| Priority | When |
|---|---|
| **P1 Critical** | The customer mentions another shop, even happily (keeping customers is this year's top goal). Or the customer asks to change the email on their account (the most common way accounts get taken over). |
| **P2 High** | A damaged item of $100 or more. Or a parcel 10 or more business days late (treated as lost). |
| **P3 Medium** | Anything else a person needs to act on. |
| **P4 Low** | A damaged item under $100 (a free replacement goes out the same day). Or a duplicate charge under $100 (routine: the extra charge is refunded in full once a person approves). |

## House style for replies

- Use the customer's first name.
- Say plainly what we found, with the date and amount.
- Never say a refund **has been** issued. Say a teammate will approve it, and when the customer will hear from us (within one business day).
- No exclamation marks. No "we apologize for any inconvenience".
- Sign off as "The Kettlewick Support Team" and include the ticket reference `KW-<order number>`.
