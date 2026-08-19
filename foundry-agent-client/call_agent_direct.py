"""
call_agent_direct.py  (ALTERNATIVE)
-----------------------------------
Calls the SAME agent using the OpenAI SDK pointed straight at the per-agent
Responses endpoint you pasted:

  https://day1flow-resource.services.ai.azure.com/api/projects/day1flow/agents/KnowledgeTest/endpoint/protocols/openai/responses

The OpenAI SDK appends "/responses" itself, so base_url is that URL WITHOUT the
trailing "/responses".

Auth: a Microsoft Entra ID bearer token from DefaultAzureCredential
(scope https://ai.azure.com/.default). Run `az login` first.
Note: tokens expire in ~60-90 min; the token provider below refreshes as needed.
"""

import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# base_url = your pasted endpoint minus the trailing "/responses"
BASE_URL = os.environ.get(
    "AGENT_OPENAI_BASE_URL",
    "https://day1flow-resource.services.ai.azure.com/api/projects/day1flow/agents/KnowledgeTest/endpoint/protocols/openai",
)

# The agent already defines its own model; the SDK still requires this field.
# Set it to your deployed model's name if the default is rejected.
MODEL = os.environ.get("MODEL", "gpt-4o-mini")


def main():
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )

    client = OpenAI(
        base_url=BASE_URL,
        api_key="placeholder",              # ignored; real auth is the header below
        default_headers={"Authorization": f"Bearer {token_provider()}"},
    )

    resp = client.responses.create(
        model=MODEL,
        input="What are the password requirements?",
    )
    print(resp.output_text)


if __name__ == "__main__":
    main()
