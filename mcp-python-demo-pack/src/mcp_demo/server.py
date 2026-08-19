"""A classroom-ready MCP server with tools, resources, and prompts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Literal

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

mcp = MCPServer(
    "ITTechGenie Training MCP",
    instructions=(
        "Use employee tools for staff questions and inventory tools for product "
        "questions. Read the policy resource before proposing a reorder."
    ),
)


class Employee(BaseModel):
    id: int
    name: str
    department: str
    city: str
    skills: list[str]


class Product(BaseModel):
    sku: str
    name: str
    category: str
    price: float
    quantity: int


class ReorderResult(BaseModel):
    sku: str
    current_quantity: int
    reorder_level: int
    suggested_order: int
    status: str


def _load_json(filename: str) -> list[dict]:
    with (DATA_DIR / filename).open(encoding="utf-8") as handle:
        return json.load(handle)


@mcp.tool(
    title="Calculate",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def calculate(
    operation: Literal["add", "subtract", "multiply", "divide"],
    a: float,
    b: float,
) -> float:
    """Perform one safe arithmetic operation on two numbers."""
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@mcp.tool(
    title="Search employees",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def search_employees(
    query: Annotated[str, Field(min_length=1, description="Name, department, city, or skill")],
    limit: Annotated[int, Field(ge=1, le=20)] = 10,
) -> list[Employee]:
    """Search the local employee directory using a case-insensitive query."""
    needle = query.casefold()
    matches: list[Employee] = []
    for raw in _load_json("employees.json"):
        searchable = " ".join(
            [raw["name"], raw["department"], raw["city"], *raw["skills"]]
        ).casefold()
        if needle in searchable:
            matches.append(Employee.model_validate(raw))
    return matches[:limit]


@mcp.tool(
    title="Get employee",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def get_employee(employee_id: int) -> Employee:
    """Return one employee by numeric employee ID."""
    for raw in _load_json("employees.json"):
        if raw["id"] == employee_id:
            return Employee.model_validate(raw)
    raise ValueError(f"Employee {employee_id} was not found.")


@mcp.tool(
    title="Check inventory",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def check_inventory(sku: str) -> Product:
    """Return current product and stock information for a SKU."""
    wanted = sku.strip().upper()
    for raw in _load_json("inventory.json"):
        if raw["sku"] == wanted:
            return Product.model_validate(raw)
    raise ValueError(f"SKU {wanted!r} was not found.")


@mcp.tool(
    title="Suggest reorder",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def suggest_reorder(
    sku: str,
    reorder_level: Annotated[int, Field(ge=0, le=1000)] = 10,
    target_stock: Annotated[int, Field(ge=1, le=5000)] = 30,
) -> ReorderResult:
    """Calculate a stock reorder suggestion without changing inventory."""
    product = check_inventory(sku)
    if target_stock < reorder_level:
        raise ValueError("target_stock must be greater than or equal to reorder_level.")
    amount = max(0, target_stock - product.quantity) if product.quantity <= reorder_level else 0
    return ReorderResult(
        sku=product.sku,
        current_quantity=product.quantity,
        reorder_level=reorder_level,
        suggested_order=amount,
        status="REORDER" if amount else "STOCK_OK",
    )


@mcp.resource("company://employees", title="Employee directory")
def employee_directory() -> str:
    """Complete employee directory as formatted JSON."""
    return json.dumps(_load_json("employees.json"), indent=2)


@mcp.resource("company://employees/{employee_id}", title="Employee record")
def employee_resource(employee_id: str) -> str:
    """One employee record addressed through a resource URI template."""
    return get_employee(int(employee_id)).model_dump_json(indent=2)


@mcp.resource("inventory://catalog", title="Inventory catalog")
def inventory_catalog() -> str:
    """Full local inventory catalog as formatted JSON."""
    return json.dumps(_load_json("inventory.json"), indent=2)


@mcp.resource("policy://reorder", title="Reorder policy")
def reorder_policy() -> str:
    """Rules used when recommending a product reorder."""
    return (
        "Reorder policy:\n"
        "1. Recommend an order only when quantity is at or below the reorder level.\n"
        "2. Never change inventory automatically in this demo.\n"
        "3. A human must approve every purchase order.\n"
        "4. Do not expose data not returned by the MCP server."
    )


@mcp.prompt(title="Employee skill summary")
def employee_skill_summary(department: str = "Data Engineering") -> str:
    """Prepare a prompt that asks for a department skills summary."""
    return (
        f"Read company://employees and summarize the skills represented in the "
        f"{department} department. Mention skill gaps cautiously and do not invent data."
    )


@mcp.prompt(title="Inventory risk review")
def inventory_risk_review(reorder_level: str = "10") -> str:
    """Prepare a prompt for reviewing low-stock inventory."""
    return (
        "Read policy://reorder and inventory://catalog. Identify products at or below "
        f"a reorder level of {reorder_level}. Use suggest_reorder for calculations, "
        "then present a table. Do not place orders."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")

