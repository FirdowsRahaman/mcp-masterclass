# Lab 5: Secure Tools

## Objective
Implement zero-trust security concepts within an MCP server to prevent unauthorized tool execution.

## Prerequisites
- Completion of Labs 1 and 2
- Python 3.10+

## Step 1: Project Setup

```bash
mkdir -p mcp-lab-05
cd mcp-lab-05
python -m venv venv
source venv/bin/activate
pip install mcp
```

## Step 2: Implementing Security Checks

Because MCP runs over `stdio` in standard deployments, the "Client" running the server is typically a trusted local host. However, when building enterprise tools, you often need application-level security, role-based access, or Human-in-the-Loop approvals.

Create `secure_server.py`:

```python
# secure_server.py
from mcp.server.fastmcp import FastMCP, Context
import os

mcp = FastMCP("secure-server")

# In a real app, this would be injected by the host or managed securely
# For this lab, we use an environment variable to simulate an authorized session
IS_ADMIN_SESSION = os.environ.get("ADMIN_MODE") == "1"

@mcp.tool()
def read_public_data() -> str:
    """Read public company data. Safe for all users."""
    return "Company was founded in 2020. Headquartered in SF."

@mcp.tool()
def delete_production_database(confirm: bool, ctx: Context) -> str:
    """
    DANGEROUS: Deletes the production database.
    Requires admin privileges and confirmation.
    """
    # 1. Authorization Check (Zero-Trust)
    if not IS_ADMIN_SESSION:
        # We can log the unauthorized attempt here
        ctx.info("Unauthorized attempt to delete production database blocked.")
        return "SECURITY ERROR: You do not have administrator privileges to perform this action."
        
    # 2. Input Validation (Defense-in-Depth)
    if not confirm:
        return "ERROR: Action aborted. You must explicitly set 'confirm' to True."
        
    ctx.warning("Executing production database deletion!")
    return "SUCCESS: Production database deleted."

if __name__ == "__main__":
    mcp.run()
```

## Step 3: Test Security Boundaries

**Test 1: Unprivileged Execution**
1. Run the server normally:
   ```bash
   npx @modelcontextprotocol/inspector python secure_server.py
   ```
2. Try to run `delete_production_database` with `confirm=true`. You should receive the Security Error.

**Test 2: Admin Execution**
1. Stop the Inspector.
2. Run the server with the admin environment variable:
   ```bash
   ADMIN_MODE=1 npx @modelcontextprotocol/inspector python secure_server.py
   ```
3. Try to run `delete_production_database` with `confirm=true`. The operation should succeed, and you will see the warning logged via the `Context` object in the Inspector logs.

## Success!
You've implemented application-level security within an MCP tool. In Chapter 7, we discussed how this pattern scales to massive multi-tenant architectures. Next, we'll tackle multi-server orchestration.
