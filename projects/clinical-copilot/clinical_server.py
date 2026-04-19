from mcp.server.fastmcp import FastMCP, Context
import re

mcp = FastMCP("clinical-copilot")

# --- Mock EMR Database ---
MOCK_EMR = {
    "P12345": {
        "name": "Jane Doe",
        "ssn": "123-45-6789",
        "condition": "Type 2 Diabetes",
        "medications": ["Metformin"]
    }
}

# --- Middleware Utilities ---
def anonymize_clinical_data(data: dict) -> dict:
    """Strip PII before sending context to the LLM."""
    safe_data = data.copy()
    safe_data["name"] = "[REDACTED_NAME]"
    safe_data["ssn"] = "[REDACTED_SSN]"
    return safe_data

# --- Tools ---
@mcp.tool()
def get_patient_history(patient_id: str, ctx: Context) -> dict:
    """
    Retrieve clinical history for diagnosis.
    Returns safe, anonymized data for the LLM to analyze.
    """
    ctx.info(f"Audit Log: Accessing records for {patient_id}")
    
    if patient_id not in MOCK_EMR:
        return {"error": "Patient not found."}
        
    raw_data = MOCK_EMR[patient_id]
    
    # CRITICAL: Scrub data before returning to the model
    safe_data = anonymize_clinical_data(raw_data)
    return safe_data

@mcp.tool()
def prescribe_medication(patient_id: str, medication: str, human_approved: bool, ctx: Context) -> str:
    """
    DANGEROUS: Prescribes medication.
    The LLM MUST ask the user to explicitly say 'I approve' before setting human_approved=True.
    """
    if not human_approved:
        ctx.warning(f"Rejected unapproved prescription attempt for {medication}")
        return "SECURITY ERROR: You must present the prescription plan to the attending physician and receive explicit text approval before executing this tool."
        
    ctx.info(f"Audit Log: Executing approved prescription for {medication} to {patient_id}")
    # Execute actual API call to EMR here...
    return f"SUCCESS: {medication} has been added to the patient's chart."

if __name__ == "__main__":
    mcp.run()
