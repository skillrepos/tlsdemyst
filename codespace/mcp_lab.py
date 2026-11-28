#!/usr/bin/env python3
"""
MCP lab — ask a local model a question with and without a connection to the Kettlewick server.

  python codespace/mcp_lab.py ask "Was order 1182 charged twice? What should we do about it?"
  python codespace/mcp_lab.py tools
  python codespace/mcp_lab.py call look_up_order 1182
  python codespace/mcp_lab.py call issue_refund 1182
  python codespace/mcp_lab.py ask --connect "Was order 1182 charged twice? What should we do about it?"
"""

import asyncio
import json
import os
import sys
import urllib.request

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

BASE = os.path.dirname(os.path.abspath(__file__))
SERVER = StdioServerParameters(command=sys.executable, args=[os.path.join(BASE, "kettlewick_server.py")])
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
MAX_STEPS = 6                       # the most times the model may use the server for one question
RULES = ("You are a support assistant for a shop called Kettlewick. Answer in three sentences or fewer. "
         "If you cannot see the records you need, say so; do not guess.")


def line(char="-"):
    print(char * 72)


def chat(messages, tools=None):
    """Send the conversation so far to the local model and return its reply."""
    body = {"model": MODEL, "stream": False, "options": {"temperature": 0}, "messages": messages}
    if tools:
        body["tools"] = tools
    request = urllib.request.Request(OLLAMA_URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.loads(response.read())["message"]
    except OSError as error:
        sys.exit(f"Could not reach the local model ({error}).\nStart it with:  bash codespace/scripts/startOllama.sh")


def result_text(result):
    return "\n".join(part.text for part in result.content if hasattr(part, "text"))


# ------------------------------------------------- the model on its own ----
def ask_alone(question):
    print(f"Question: {question}\n")
    print(f"The model's answer with NO connection ({MODEL}):")
    line("=")
    print(chat([{"role": "system", "content": RULES}, {"role": "user", "content": question}])["content"].strip())
    line("=")


# ------------------------------------------- looking at the server by hand ----
async def show_tools():
    async with stdio_client(SERVER) as (read, write), ClientSession(read, write) as session:
        about = await session.initialize()
        offered = (await session.list_tools()).tools
        print(f"Connected to: {about.server_info.name}. It offers {len(offered)} things:\n")
        for tool in offered:
            print(f"  {tool.name}\n      {tool.description}")
        print("\nThis list is the whole of what an assistant can do through this connection.")


async def call_by_hand(name, order_id):
    arguments = {} if name == "get_refund_policy" else {"order_id": int(order_id)}
    async with stdio_client(SERVER) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool(name, arguments)
        print(f"Asked the server: {name} {arguments}\n")
        if result.is_error:
            print("The server refused. Its reply:")
        print(result_text(result))


# ------------------------------------- the model with the server connected ----
async def ask_connected(question):
    async with stdio_client(SERVER) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        offered = (await session.list_tools()).tools
        # Tell the model what the server offers, in the form the model expects.
        tools = [{"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.input_schema}}
                 for t in offered]
        print(f"Question: {question}\n")
        print(f"Connected. The model has been told about {len(tools)} things it may use.\n")
        messages = [{"role": "system", "content": RULES}, {"role": "user", "content": question}]
        for step in range(1, MAX_STEPS + 1):
            reply = chat(messages, tools)
            messages.append(reply)
            wanted = reply.get("tool_calls") or []
            if not wanted:                            # the model has finished and written its answer
                print(f"\nThe model's answer WITH the connection ({MODEL}):")
                line("=")
                print(reply["content"].strip())
                line("=")
                return
            for call in wanted:
                name, arguments = call["function"]["name"], call["function"].get("arguments") or {}
                result = await session.call_tool(name, arguments)
                text = result_text(result)
                print(f"  step {step}: the model asked the server for  {name} {arguments}")
                print("          " + text.replace("\n", "\n          ")[:400])
                messages.append({"role": "tool", "tool_name": name, "content": text})
        print(f"\nStopped after {MAX_STEPS} steps without a final answer. That limit is a budget someone set.")


def main():
    args = sys.argv[1:]
    step = args[0] if args else ""
    if step == "ask" and len(args) > 1:
        connect = "--connect" in args
        question = " ".join(a for a in args[1:] if a != "--connect")
        asyncio.run(ask_connected(question)) if connect else ask_alone(question)
    elif step == "tools":
        asyncio.run(show_tools())
    elif step == "call" and len(args) >= 2:
        asyncio.run(call_by_hand(args[1], args[2] if len(args) > 2 else 0))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
