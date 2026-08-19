# MCP Python Demo Pack

A no-paid-API, classroom-ready Model Context Protocol (MCP) project using the current Python SDK v2 API (`MCPServer` and `Client`).

## Included examples

| Path | Purpose |
|---|---|
| `examples/01_minimal_server.py` | Minimal tool, resource, and prompt |
| `src/mcp_demo/server.py` | Employee and inventory MCP server |
| `examples/02_in_memory_client.py` | Direct in-process client |
| `examples/03_stdio_client.py` | Subprocess client over stdio |
| `src/mcp_demo/http_server.py` | Streamable HTTP server |
| `examples/04_http_client.py` | Streamable HTTP client |
| `tests/test_server.py` | Automated tests |
| `config/` | VS Code and Claude Desktop templates |
| `tutorial.html` | Visual step-by-step trainer notes |

## Architecture

```text
User -> MCP Host/Client -> MCP Server -> Python functions / local JSON
                            |  Tools: operations
                            |  Resources: context
                            +  Prompts: templates
```

MCP does not replace an LLM. It standardizes how a host discovers and invokes capabilities supplied by a server.

## Prerequisites

- Python 3.10+ (Python 3.11 recommended for the classroom)
- VS Code or another editor
- Node.js only for MCP Inspector (`npx` must be available)
- No API key, paid model, database, or cloud subscription

## Windows quick start

1. Extract the ZIP and open the folder in VS Code.
2. Run `setup_windows.bat`.
3. Run `run_inspector.bat`.
4. Open the URL printed by MCP Inspector.
5. Call `calculate` with `operation=multiply`, `a=12`, `b=5`.
6. Read resource `policy://reorder`.
7. Render prompt `inventory_risk_review`.

## Manual Windows setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

## macOS/Linux setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

## Demo 1: minimal server

```bash
mcp dev examples/01_minimal_server.py
```

Try `add`, resource `greeting://Gopi`, and prompt `explain_mcp`.

## Demo 2: complete server in Inspector

```bash
mcp dev src/mcp_demo/server.py
```

| Tool | Arguments | Expected idea |
|---|---|---|
| `calculate` | `{"operation":"divide","a":100,"b":4}` | 25 |
| `search_employees` | `{"query":"Python"}` | Asha and Rahul |
| `get_employee` | `{"employee_id":102}` | Rahul's record |
| `check_inventory` | `{"sku":"MIC-401"}` | Quantity 3 |
| `suggest_reorder` | `{"sku":"MIC-401","reorder_level":10,"target_stock":30}` | Suggest 27 |

Also demonstrate division by zero. It becomes a tool error that the MCP host can present to a model.

## Demo 3: in-memory client

```bash
python examples/02_in_memory_client.py
```

This is the easiest client and best testing pattern: no port or subprocess.

## Demo 4: stdio client

```bash
python examples/03_stdio_client.py
```

The client starts the server as a child process. Never print debugging text to stdout in a stdio server; stdout carries protocol messages. Use stderr or logging configured for stderr.

## Demo 5: Streamable HTTP

Terminal 1:

```bash
python -m mcp_demo.http_server
```

Terminal 2:

```bash
python examples/04_http_client.py
```

Endpoint: `http://127.0.0.1:8000/mcp`. This binds to localhost and is for training, not public production deployment.

## Demo 6: tests

```bash
pytest -q
```

Tests use `Client(mcp, raise_exceptions=True)` to verify tools, structured output, a resource, and a prompt.

## Tools vs resources vs prompts

| Primitive | Controlled by | Use | Example |
|---|---|---|---|
| Tool | Usually model/host | Operation or action | `search_employees` |
| Resource | Application/user | Read-only URI context | `policy://reorder` |
| Prompt | User | Reusable message template | `inventory_risk_review` |

## Host configuration

Files in `config/` are templates. Replace placeholders with absolute paths. Host settings locations can change, so verify the host's current documentation.

For stdio, configure the virtual environment's Python executable, arguments `-m` and `mcp_demo.server`, plus `PYTHONPATH` pointing to this project's `src` directory.

## Trainer flow (45–60 minutes)

1. Explain host, client, server, and transport.
2. Run the minimal server in Inspector.
3. Connect each decorator to its Inspector tab.
4. Run the complete server and demonstrate validation.
5. Show structured employee/inventory output.
6. Read the policy resource and render the inventory prompt.
7. Run the in-memory client and tests.
8. Compare stdio and Streamable HTTP.

## Security checklist

- Treat all tool arguments as untrusted input.
- Require human approval for purchases, deletion, and messages.
- Authenticate and authorize before remote HTTP exposure.
- Keep credentials out of code and Git.
- Grant databases and cloud identities least privilege.
- Treat tool annotations as hints, not access control.

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named mcp` | Activate `.venv` and reinstall the project. |
| `No module named mcp_demo` | Run from the project root after editable install. |
| `No module named mcp.server.fastmcp` | That is v1; v2 uses `MCPServer`. |
| Inspector unavailable | Install Node.js and verify `npx --version`. |
| Port 8000 busy | Change it in the HTTP server and client. |
| Host shows no tools | Use absolute paths and verify `PYTHONPATH` ends in `src`. |

## Exercises

1. Add `search_inventory(category)`.
2. Add a `company://departments` resource.
3. Tighten the `target_stock` constraint and observe validation.
4. Add an employee to the JSON file and search again.
5. Test that division by zero returns `is_error=True`.
6. Design a write tool that requires human approval.

## Official references

- <https://py.sdk.modelcontextprotocol.io/>
- <https://modelcontextprotocol.io/specification/2026-07-28>
- <https://github.com/modelcontextprotocol/inspector>
