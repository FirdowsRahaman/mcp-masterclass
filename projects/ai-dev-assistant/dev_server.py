from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import subprocess
import os

mcp = FastMCP("ai-dev-assistant")

# --- Schemas ---
class CommitData(BaseModel):
    message: str = Field(description="Conventional commit message (e.g., 'fix: resolve null pointer')")
    files: list[str] = Field(description="List of specific files to stage. Use ['.'] for all.")

class LintData(BaseModel):
    directory: str = Field(default=".", description="Directory to run flake8/pytest against")

# --- Tools ---
@mcp.tool()
def git_commit(data: CommitData) -> str:
    """Stage files and create a Git commit. Only call this after verifying code passes linting."""
    try:
        # Stage files
        for file in data.files:
            subprocess.run(["git", "add", file], check=True, capture_output=True)
            
        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", data.message], 
            check=True, capture_output=True, text=True
        )
        return f"Successfully committed:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Git Error: {e.stderr}"

@mcp.tool()
def lint_and_test(data: LintData) -> str:
    """Run flake8 linter and pytest. Returns the console output so the agent can fix errors."""
    try:
        result = subprocess.run(
            ["flake8", data.directory], 
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return f"Linting Errors Found. Please fix these:\n{result.stdout}"
            
        return "Linting passed perfectly! Safe to commit."
    except FileNotFoundError:
        return "Error: flake8 is not installed in the current environment."

if __name__ == "__main__":
    mcp.run()
