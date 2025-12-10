from lib.coding_agent import coding_agent as _coding_agent, log
from openai import OpenAI
from helper import load_env

# Ensure environment variables from a top-level .env are loaded before any
# OpenAI client is created. This lets `OpenAI()` pick up `OPENAI_API_KEY`.
load_env()
from lib.utils import create_sandbox
from lib.tools import execute_code
from lib.tools_schemas import execute_code_schema
from lib.logger import logger
from lib.ui import ui
import threading
import os

def _masked_key(key: str | None) -> str:
    if not key:
        return "<NONE>"
    if len(key) <= 12:
        return key
    return f"{key[:6]}...{key[-6:]}"


def coding_agent_demo_cli():
    client = OpenAI()
    print("[debug] find_dotenv:", __import__("dotenv").find_dotenv())
    print("[debug] OPENAI_API_KEY (masked):", _masked_key(os.getenv("OPENAI_API_KEY")))
    sbx = create_sandbox()
    messages = []
    logger.info("✨: Hello there! Ask me to code something!")
    while (query := input(">:")) != "/exit":
        messages, usage = log(
            _coding_agent,
            query=query,
            messages=messages,
            client=client,
            tools_schemas=[execute_code_schema],
            system="You are senior Python software engineer",
            tools={"execute_code": execute_code},
            sbx=sbx,
        )


def coding_agent_demo_ui():
    client = OpenAI()
    print("[debug] find_dotenv:", __import__("dotenv").find_dotenv())
    print("[debug] OPENAI_API_KEY (masked):", _masked_key(os.getenv("OPENAI_API_KEY")))
    sbx = create_sandbox()
    messages = []
    demo = ui(
        _coding_agent,
        messages=[],
        client=client,
        tools_schemas=[execute_code_schema],
        system="You are senior Python software engineer",
        tools={"execute_code": execute_code},
        sbx=sbx,
    )
    demo.launch(height=800, share=True)
