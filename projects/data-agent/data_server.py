from mcp.server.fastmcp import FastMCP
import sqlite3
import pandas as pd

mcp = FastMCP("data-agent")

# Initialize an in-memory database for demonstration
def setup_mock_db():
    conn = sqlite3.connect('sales.db')
    df = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'product': ['Widget A', 'Widget B', 'Widget A'],
        'revenue': [100.50, 250.00, 150.75]
    })
    df.to_sql('daily_sales', conn, index=False, if_exists='replace')
    return conn

CONN = setup_mock_db()

# --- Resources (Context) ---
@mcp.resource("db://schema/public")
def get_database_schema() -> str:
    """Returns the complete database schema. 
    The AI should read this resource BEFORE attempting to write any SQL queries.
    """
    cursor = CONN.cursor()
    # SQLite specific schema query
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    schema_rows = cursor.fetchall()
    
    schema_text = "DATABASE SCHEMA:\n\n"
    for row in schema_rows:
        if row[0]:
            schema_text += f"{row[0]}\n\n"
        
    return schema_text

# --- Tools (Action) ---
@mcp.tool()
def execute_read_only_sql(query: str) -> str:
    """Executes a SELECT query against the data warehouse.
    Returns the results formatted as a Markdown table.
    """
    # 1. Security Check: Block destructive commands
    forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'GRANT']
    upper_query = query.upper()
    if any(keyword in upper_query for keyword in forbidden_keywords):
        return "ERROR: Only SELECT queries are permitted by the Data Agent."
        
    try:
        # 2. Execute and format results using Pandas
        df = pd.read_sql_query(query, CONN)
        return f"Query Results:\n\n{df.to_markdown(index=False)}"
    except Exception as e:
        return f"SQL Execution Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
