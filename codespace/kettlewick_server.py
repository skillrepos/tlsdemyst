#!/usr/bin/env python3
"""
The Kettlewick support server — a small MCP server.

An MCP server is a program that offers a list of things an AI assistant may use.
This one offers four. Anything not on the list (issuing a refund, for example)
cannot be done through this server, whatever the assistant is asked to do.

You do not run this file yourself. The lab script starts it:  python codespace/mcp_lab.py tools
"""

import logging

from mcp.server.mcpserver import MCPServer

logging.disable(logging.WARNING)      # keep the server quiet so the lab output is easy to read

server = MCPServer("Kettlewick support server")

ORDERS = {
    1175: ("Priya Raman", "Stand mixer", 249.00, "2026-09-02", "2026-09-08", "no"),
    1179: ("Marcus Oyelaran", "Toaster", 39.00, "2026-09-28", "2026-10-03", "no"),
    1182: ("Dana Whitfield", "Blender", 89.00, "2026-10-14", "2026-10-19", "no"),
    1186: ("Tomas Lindqvist", "Kettle", 45.00, "2026-10-30", "2026-11-04", "no"),
    1190: ("Aiko Tanaka", "Coffee grinder", 59.00, "2026-11-06", "2026-11-11", "yes"),
}
CHARGES = [
    ("C-5001", 1175, "2026-09-02", 249.00),
    ("C-5007", 1179, "2026-09-28", 39.00),
    ("C-5012", 1182, "2026-10-14", 89.00),
    ("C-5013", 1182, "2026-10-14", 89.00),
    ("C-5020", 1186, "2026-10-30", 45.00),
    ("C-5026", 1190, "2026-11-06", 59.00),
]
POLICY = """Kettlewick refund policy
1. Returns. Full refund within 30 days of delivery. From day 31 to day 60: store credit, minus 10%. After 60 days: no refund and no credit.
2. Final-sale items. Items marked final sale cannot be returned.
3. Duplicate charges. If a customer was charged twice for the same order by mistake, the extra charge is refunded in full, whatever the date.
4. Approval. Every refund must be approved by a person on the support team before it is issued. Refunds over $200 also need a supervisor.
5. Replies to customers. No email goes to a customer until a person on the support team has read it."""


@server.tool()
def look_up_order(order_id: int) -> str:
    """Returns the customer, item, price and dates for one order number."""
    if order_id not in ORDERS:
        return f"No order with number {order_id}."
    customer, item, price, ordered, delivered, final_sale = ORDERS[order_id]
    return (f"Order {order_id}: {item}, ${price:.2f}, bought by {customer} on {ordered}, "
            f"delivered {delivered}. Final sale: {final_sale}.")


@server.tool()
def list_charges(order_id: int) -> str:
    """Returns every card charge recorded against one order number."""
    rows = [c for c in CHARGES if c[1] == order_id]
    if not rows:
        return f"No charges found for order {order_id}."
    lines = [f"  {charge_id}  {date}  ${amount:.2f}" for charge_id, _, date, amount in rows]
    return f"{len(rows)} charge(s) on order {order_id}:\n" + "\n".join(lines)


@server.tool()
def get_refund_policy() -> str:
    """Returns the five rules of the Kettlewick refund policy."""
    return POLICY


@server.tool()
def draft_reply(order_id: int, text: str) -> str:
    """Saves a draft email for a person on the support team to read. It does not send anything."""
    return "Draft saved. Not sent: a person on the support team must read it and send it."


if __name__ == "__main__":
    server.run()          # talks to whichever assistant started it
