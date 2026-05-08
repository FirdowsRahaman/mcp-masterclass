# Chapter 7: Security & Auth

## Objective
In 10 minutes, you will understand:
- Implementing zero-trust security models for MCP systems
- Designing human-in-the-loop approval workflows
- Building permission systems at tool and resource levels
- Governance patterns for enterprise MCP deployments

## The Concept
Security in MCP requires a comprehensive approach spanning from individual tool execution to enterprise-wide governance.

### The "Bank Vault" Analogy
**MCP Security is like walking into a Bank.**
The AI Agent is a customer. It cannot just walk directly into the vault (your hard drive or database). 
Instead, it must hand a request slip to the **Teller** (the MCP Middleware).
- The Teller checks ID (Authentication).
- The Teller checks the account balance (Permissions).
- For massive withdrawals, the Teller asks the **Manager** for approval (Human-in-the-loop workflows).

### Core Security Principles
- **Zero-Trust**: Verify every request, even from trusted sources
- **Least Privilege**: Grant minimal necessary permissions
- **Auditability**: Full traceability of all actions
- **Defense-in-Depth**: Multiple security layers

## How It Works

### Security Architecture Layers
```
┌─────────────────────────────────────────────────────┐
│               Security Implementation               │
├───────────────┬───────────────────┬─────────────────┤
│  Host Layer   │  Protocol Layer   │  Tool Layer     │
├───────────────┼───────────────────┼─────────────────┤
│  Identity     │  Message Signing  │  Input          │
│  Verification │  & Encryption     │  Validation     │
│               │                   │                 │
│  Network      │  Session          │  Permission     │
│  Policies     │  Management       │  Checks         │
└───────────────┴───────────────────┴─────────────────┘
```

### Human-in-the-Loop Workflow
1. **Request Initiation**: Model requests sensitive operation
2. **Approval Trigger**: System identifies need for human review
3. **Context Presentation**: Relevant information shown to reviewer
4. **Decision Point**: Human approves/rejects with rationale
5. **Execution**: Action proceeds based on approval

### Permission System Design
| Permission Level | Scope | Example |
|------------------|-------|---------|
| System-wide | All tools | Admin rights |
| Tool-specific | Single tool | Database access |
| Resource-level | Data items | Patient records |
| Session-based | Current interaction | Temporary elevation |

### Code Example

```python
# Zero-Trust MCP Security Implementation
from mcp.server.fastmcp import FastMCP, Context
import os

mcp = FastMCP("secure-tools")

# Security check utility
def verify_authorization(ctx: Context) -> bool:
    """Simulate a token or session check."""
    # In practice, headers/auth tokens can be passed via transport config
    is_admin = os.environ.get("ADMIN_MODE") == "1"
    if not is_admin:
        ctx.error("Unauthorized access attempt detected.")
        return False
    return True

@mcp.tool()
def process_patient_data(patient_id: str, action: str, ctx: Context) -> str:
    """Process sensitive patient data. Requires admin authorization."""
    # 1. Authentication & Permission Check
    if not verify_authorization(ctx):
        return "SECURITY ERROR: Insufficient privileges."
        
    # 2. Audit Logging
    ctx.info(f"AUDIT: Admin processing patient {patient_id} with action: {action}")
    
    # Implementation...
    return "Data processed securely."
```

## Try It Yourself

Let's test this security implementation using the Inspector.

1. Save the code example above as `server.py`.
2. First, try to run it **without** admin privileges:
   ```bash
   npx @modelcontextprotocol/inspector python server.py
   ```
3. Open the Inspector browser UI, click on **Tools**, and execute `process_patient_data`. You will see it return `"SECURITY ERROR: Insufficient privileges."` and the `ctx.error()` log will appear.
4. Now, stop the inspector (`Ctrl+C` in the terminal) and run it again **with** admin privileges by injecting the environment variable:
   ```bash
   ADMIN_MODE=1 npx @modelcontextprotocol/inspector python server.py
   ```
5. Execute the tool again in the Inspector. This time, it will succeed and you will see the `ctx.info()` audit log confirming the action!

## Checkpoint
1. How does zero-trust differ from traditional perimeter security?
2. When would you implement human-in-the-loop versus automated security checks?

## Architect Notes

### Trade-offs
- **Security vs Usability**: More security layers increase friction
- **Performance Impact**: Security checks add latency
- **Complexity Management**: Security systems can become difficult to maintain

### Production Considerations
- Implement security policy as code for version control
- Create security playbooks for common scenarios
- Design for security incident response and forensics
- Regularly rotate credentials and keys
- Implement automated security testing in CI/CD
- Conduct regular security audits and penetration testing
- Plan for security policy evolution as systems grow