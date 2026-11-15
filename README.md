# Intelligent Calculator

Workshop notebook: `intelligent_calculator.ipynb`

## Overview

An AI-assisted calculator built with LangChain and Groq. The agent chooses between two Python tools:

- `add(a, b)` — combines two whole-number quantities.
- `tree_distance(height_m, angle_deg)` — calculates horizontal distance on level ground using height above eye level and elevation angle.

Model: `openai/gpt-oss-20b` via Groq. MCP tool exposed by the local server: `solve_math_problem`.

## Notebook test evidence

1. Five apples plus ten apples: **15 apples** (`add`).
2. Tree height 10 m above eye level, angle 30°: **17.32 m** (`tree_distance`).
3. Tree problem without an angle: the agent asks for the missing angle and makes no calculator-tool call.
4. Fresh test, seven apples plus eight apples: **15 apples** (`add`).

The notebook retains the code-cell outputs for these tests and includes written observations.

## Integration status

- **Local MCP Inspector:** demonstrated during the workshop; `solve_math_problem` was discovered and the apples calculation returned 15.
- **LangSmith:** client configuration and three traced-run submissions are present in the notebook; visibility of the traces in the LangSmith workspace was not independently verified.
- **ChatGPT through OpenAI Secure MCP Tunnel:** unavailable / not verified. ChatGPT reported that the MCP server denied access and requested an authentication or tunnel-workspace-access check.

## Credentials

API keys are requested at runtime and must not be committed to this repository. If any credential has been exposed, rotate it in its provider dashboard.
