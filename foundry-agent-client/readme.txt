========================================================================
 CALL A MICROSOFT FOUNDRY AGENT FROM PYTHON
 Agent: KnowledgeTest   Project: day1flow
========================================================================

WHAT THIS IS
------------
A tiny Python package that connects to your Microsoft Foundry agent and asks
it questions. The agent already has your Foundry IQ knowledge base attached,
so the search + grounding happens on the server automatically. You just send
a question and read the answer (with source citations).

Two scripts are included:

  call_agent.py         RECOMMENDED. Uses the azure-ai-projects 2.x SDK with
                        your project endpoint + agent name. Handles auth and
                        multi-turn conversation for you. Prints citations.

  call_agent_direct.py  ALTERNATIVE. Uses the OpenAI SDK pointed straight at
                        the exact per-agent endpoint URL you pasted, with an
                        Entra ID bearer token.

Start with call_agent.py. Use the direct one only if you specifically need to
hit the raw endpoint URL.


YOUR VALUES (already filled into the scripts)
---------------------------------------------
  Project endpoint : https://day1flow-resource.services.ai.azure.com/api/projects/day1flow
  Agent name       : KnowledgeTest
  Direct endpoint  : https://day1flow-resource.services.ai.azure.com/api/projects/day1flow/agents/KnowledgeTest/endpoint/protocols/openai/responses

You do NOT need to edit anything to run the demo. The values above are baked in
as defaults. (You can override them with environment variables or a .env file;
see .env.example.)


PREREQUISITES
-------------
  1. Python 3.10 or newer.        Check with:  python --version
  2. The Azure CLI installed.     Check with:  az version
  3. On your Foundry project, your signed-in account needs the "Foundry User"
     role (this is what lets you call the agent).
  4. The agent "KnowledgeTest" exists and its knowledge base source shows
     status = Active in the portal.


STEP-BY-STEP
------------
  1. Unzip this package and open a terminal in the unzipped folder.

  2. (Recommended) Create and activate a virtual environment.

       Windows (PowerShell):
         python -m venv .venv
         .\.venv\Scripts\Activate.ps1

       macOS / Linux:
         python3 -m venv .venv
         source .venv/bin/activate

  3. Install the dependencies:

         pip install -r requirements.txt

  4. Sign in to Azure (opens a browser once):

         az login

     If you belong to more than one tenant/subscription, select the one that
     holds the day1flow project, for example:

         az account set --subscription "<your-subscription-name-or-id>"

  5. Run the recommended script:

         python call_agent.py

     You should see the agent answer the sample questions, with a "Sources:"
     line showing which document grounded each answer.

  6. (Optional) Try the direct-endpoint version:

         python call_agent_direct.py


CHANGE THE QUESTIONS
--------------------
Open call_agent.py and edit the QUESTIONS list near the top. Good questions to
test against a policy/handbook knowledge base:

  - What is the maximum I can claim for meals per day?
  - How many days a week can I work from home?
  - How much annual leave do I get?
  - My laptop was stolen. What should I do and how quickly?
  - What are the password requirements?

Negative test (should say it does not know instead of guessing):
  - What is the pet-adoption policy?


TROUBLESHOOTING
---------------
  403 Forbidden when calling the agent
      Your account is missing the "Foundry User" role on the project.
      Assign it in the Azure portal under the Foundry resource ->
      Access control (IAM).

  Agent answers but never cites the knowledge base
      The agent's managed identity needs the "Search Index Data Reader" role
      on the Azure AI Search service. Add it, then retry.

  "DefaultAzureCredential failed to retrieve a token"
      You are not signed in, or you are on the wrong subscription/tenant.
      Run `az login` again and set the correct subscription (step 4).

  Token expired (direct script, long sessions)
      call_agent_direct.py uses a token provider that refreshes automatically.
      If you built your own client with a static token, get a fresh one.

  ImportError / "no attribute" errors
      You may have an old 1.x SDK. This code targets azure-ai-projects 2.x
      (no threads/runs/agent GUIDs). Reinstall with:
          pip install --upgrade -r requirements.txt

  Model field rejected (direct script only)
      Set MODEL to your deployed model's exact name (see Build -> Deployments
      in the portal), then run again:
          set MODEL=your-deployment-name        (Windows)
          export MODEL=your-deployment-name     (macOS/Linux)


NOTES
-----
  - Keep your terminal signed in with `az login`; no API keys are stored in
    these files.
  - The recommended script is the stable, documented path. Microsoft Foundry
    agents run on the Responses API by default since November 2025.
========================================================================
