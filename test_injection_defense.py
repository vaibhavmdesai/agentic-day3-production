from langchain.messages import SystemMessage, HumanMessage
from typing import Final
import re
import yaml
from llm import llm

INJECTION_PATTERNS: Final[list[str]] = [
	r"ignore (your |all |previous )?instructions",
	r"system prompt.*disabled",
	r"new role",
	r"repeat.*system prompt",
	r"jailbreak",
]

def prompt_builder(user_input: str) -> str:

    """Load System prompt from YAML and build messages for the agent."""

    prompt_file = "/home/vaibhav/Study/agentic-ai/agentic-ai-bootcamp/assigments/week2/agentic-day3-production/prompts/support_agent_v1.yaml"

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = yaml.safe_load(f) 
	
    return [SystemMessage(content=prompt["system"]), HumanMessage(content=user_input)]


def core_agent_invoke(user_input: str) -> str:
    """Invoke the agent with the user input and return the response."""

    messages = prompt_builder(user_input)
    response = llm.invoke(messages)
    return response.content


def detect_injection(user_input: str) -> bool:
	"""Return True if the input looks like a prompt injection attempt."""
	text = user_input.lower()
	for pattern in INJECTION_PATTERNS:
		if re.search(pattern, text):
			return True
	return False

def safe_agent_invoke(user_input: str) -> str:
	# Layer 1: input validation
	if detect_injection(user_input):
		return "I can only assist with product support. (Request blocked)"

	# Layer 2: hardened system prompt (from YAML)
	# Build messages / graph input using the hardened system prompt.

	raw_response = core_agent_invoke(user_input=user_input)  # your existing logic
	

	# Layer 3: output validation
	dangerous_markers = ["hack", "fraud", "system prompt:", "ignore your previous instructions"]
	text = raw_response.lower()
	if any(marker in text for marker in dangerous_markers):
		return "I can only assist with product support."
	
	return raw_response

