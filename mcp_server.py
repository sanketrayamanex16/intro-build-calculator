"""Instructor demo: expose the Intro Build calculator over MCP."""
import os
import sys
from getpass import getpass

def _get_groq_api_key() -> str:
    while True:
        if not sys.stdin.isatty():
            line = sys.stdin.readline().strip()
            if line:
                return line
        try:
            key = getpass('Groq API key: ').strip()
        except Exception:
            key = input('Groq API key: ').strip()
        if key:
            return key
        print('Groq API key cannot be blank. Please enter a valid API key.', file=sys.stderr)

groq_api_key = _get_groq_api_key()
os.environ['GROQ_API_KEY'] = groq_api_key

from langchain_groq import ChatGroq
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=groq_api_key,
    temperature=0,
    timeout=30,
    max_retries=1,
)

from langchain.tools import tool
@tool
def add(a: int, b: int) -> int:
    """Add two whole-number quantities when they are combined."""
    return a + b

from math import isfinite, radians, tan

@tool
def tree_distance(height_m: float, angle_deg: float) -> float | str:
    """Find horizontal tree distance on level ground from height above eye level in metres and angle of elevation in degrees."""
    if not isfinite(height_m) or height_m <= 0:
        return "Invalid height. Supply a positive finite height above eye level."
    if not isfinite(angle_deg) or not 0 < angle_deg < 90:
        return "Invalid angle. Supply an angle strictly between 0 and 90 degrees."
    return round(height_m / tan(radians(angle_deg)), 2)

from langchain.agents import create_agent

INSTRUCTIONS = (
    "You are the Intelligent Calculator. Use add for combining two whole-number "
    "quantities. Use tree_distance only for horizontal distance on level ground "
    "when height above eye level in metres and angle of elevation in degrees "
    "are supplied. For supported complete problems, call the matching tool once "
    "and use its result. If a required value is missing, ask for it before "
    "calling a tool. Never guess inputs. If a tool reports an invalid input, ask "
    "for a correction. For other requests, explain what you can calculate. "
    "Give the final answer with units."
)
agent = create_agent(model=model, tools=[add, tree_distance], system_prompt=INSTRUCTIONS)
mcp = FastMCP(
    "Intelligent Calculator",
    host=os.environ.get("INTRO_MCP_HOST", "127.0.0.1"),
    stateless_http=True,
    json_response=True,
)

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def solve_math_problem(problem: str) -> str:
    """Solve an apples addition or tree-distance word problem. Pass the original wording."""
    problem = problem.strip()
    if not 1 <= len(problem) <= 1500:
        return "Enter an English word problem of 1 to 1500 characters."
    result = agent.invoke(
        {"messages": [("human", problem)]},
        config={"recursion_limit": 8, "run_name": "intro_calculator_mcp"},
    )
    return result["messages"][-1].text

if __name__ == "__main__":
    mcp.run(transport="streamable-http")