"""
call_agent.py  (RECOMMENDED)
----------------------------
Calls your Microsoft Foundry agent "KnowledgeTest" using the azure-ai-projects
2.x SDK. Because the agent already has the Foundry IQ knowledge base attached,
retrieval + grounding happen automatically on the server. You just ask questions.

Auth: DefaultAzureCredential -> run `az login` once before running this file.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# --- Your values (already filled in; override with env vars if you like) -------
PROJECT_ENDPOINT = os.environ.get(
    "FOUNDRY_PROJECT_ENDPOINT",
    "https://day1flow-resource.services.ai.azure.com/api/projects/day1flow",
)
AGENT_NAME = os.environ.get("AGENT_NAME", "KnowledgeTest")

# Ask anything grounded in your uploaded documents.
QUESTIONS = [
    "What is the maximum I can claim for meals per day?",
    "And how long do I have to submit the claim?",
]


def print_citations(resp):
    """Best-effort: pull document/source citations out of the response."""
    seen = []
    for item in getattr(resp, "output", []) or []:
        if getattr(item, "type", None) != "message":
            continue
        for part in getattr(item, "content", []) or []:
            for ann in getattr(part, "annotations", []) or []:
                label = (
                    getattr(ann, "filename", None)
                    or getattr(ann, "title", None)
                    or getattr(ann, "url", None)
                    or getattr(ann, "text", None)
                )
                if label and label not in seen:
                    seen.append(label)
    if seen:
        print("   Sources: " + ", ".join(seen))


def main():
    project = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )

    # OpenAI client pre-bound to your agent.
    client = project.get_openai_client(agent_name=AGENT_NAME)

    # A server-side conversation keeps history for multi-turn chat.
    conversation = client.conversations.create()
    print(f"Connected to agent '{AGENT_NAME}'. Conversation: {conversation.id}\n")

    for q in QUESTIONS:
        print(f"You:   {q}")
        resp = client.responses.create(conversation=conversation.id, input=q)
        print(f"Agent: {resp.output_text}")
        print_citations(resp)
        print()


if __name__ == "__main__":
    main()
