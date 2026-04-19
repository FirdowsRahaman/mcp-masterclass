# Chapter 5: Resource Management

## Objective
In 10 minutes, you will understand:
- How to manage resources (files, databases) in MCP
- Context injection patterns for AI models
- Differences between RAG and MCP resource handling
- Security considerations for resource access

## The Concept
MCP enables AI models to access external resources through standardized interfaces. While Tools are for *taking action*, Resources are for *reading data*.

### The "Reference Library" Analogy
**Resources are the Reference Library; Tools are the Workshop.**
You wouldn't use a hammer to read a book. When an AI needs to understand context before acting, it doesn't "execute a tool"—it goes to the Reference Library.
The AI must ask the Librarian (the MCP Resource Manager) for a specific book (using a URI like `file:///logs/error.log`) to read *before* it takes any action in the workshop.

### Core Principles
- **Context Boundaries**: Clearly defined scope for resource access
- **Resource Lifecycle**: Proper initialization and cleanup
- **Execution Context**: Tools can use the `Context` object to access request metadata and stream logs back to the client.
- **Model Abstraction**: Models interact with resources through tools, not directly

## How It Works

### Resource Types Matrix
| Resource Type | Access Pattern | Security Model | Best For |
|---------------|----------------|----------------|----------|
| Local Files | Read/Write via tool | File permissions | Configuration, logs |
| Databases | Query interface | Row-level security | Structured data |
| APIs | Proxy calls | API keys, OAuth | External services |
| Knowledge Bases | Search interface | Content filtering | RAG implementations |

### Context Injection Patterns
1. **Explicit Injection**: Resources passed as tool parameters
2. **Implicit Context**: State maintained between interactions
3. **Context Window Management**: Prioritizing relevant information
4. **Metadata Enrichment**: Adding context about resource relevance

### RAG vs MCP Resource Handling
| Feature | Traditional RAG | MCP Resource Handling |
|---------|-----------------|------------------------|
| Access Control | Application-level | Protocol-level |
| Context Boundaries | Fixed window | Dynamic injection |
| Security Model | Per-application | Standardized |
| Error Handling | Custom | Standardized |

### Code Example
```python
# Resource Server Implementation using FastMCP
from mcp.server.fastmcp import FastMCP, Context
import sqlite3
import time

mcp = FastMCP("clinical-resource-server")

# --- 1. Resource: Data Context Injection ---
@mcp.resource("clinical://patients/{patient_id}")
def get_patient_data(patient_id: str) -> str:
    """Read patient records as a resource."""
    conn = sqlite3.connect('clinical.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    results = cursor.fetchall()
    return str(results)

# --- 2. Tool: Execution Context Management ---
@mcp.tool()
def analyze_patient(patient_id: str, ctx: Context) -> str:
    """Analyze a patient's data. Demonstrates execution context logging."""
    # The ctx object allows us to stream progress back to the AI Client
    ctx.info(f"Starting analysis for {patient_id}...")
    
    time.sleep(1) # Simulate work
    ctx.info("Fetching lab results...")
    
    # We can also issue warnings if something is amiss
    if patient_id.startswith("TEST"):
        ctx.warning("Using test patient data!")
        
    return "Analysis complete."
```

## Try It Yourself

1. Set up a SQLite database with sample patient data
2. Create a resource server with two tools:
   - One for querying patient records
   - One for accessing clinical guidelines
3. Connect via MCP Inspector and test:
   - Valid queries with proper patient ID
   - Attempted access with unauthorized patient ID
   - Context propagation between tool calls
4. Compare performance with traditional RAG implementation

## Checkpoint
1. When would you use implicit context vs explicit resource parameters?
2. How does MCP's security model differ from traditional RAG implementations?

## Architect Notes

### Trade-offs
- **Performance**: Direct database access is faster but less secure
- **Abstraction Cost**: Additional layer adds minimal latency
- **Context Size**: Large resources may exceed model context windows

### Production Considerations
- Implement resource access auditing and logging
- Design for resource failover and redundancy
- Use tokenization for sensitive data in context
- Monitor resource access patterns for anomalies
- Implement timeouts for resource operations
- Create resource health checks for production monitoring
- Consider data residency requirements for global deployments