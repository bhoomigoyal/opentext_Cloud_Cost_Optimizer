import json
from src.llm_client import call_llm

def extract_project_profile():
    """
    Extract structured project profile from project description using LLM.
    Output: project_profile.json with name, budget_inr_per_month, description, 
    tech_stack, and non_functional_requirements.
    """
    try:
        with open("data/project_description.txt", "r") as f:
            description = f.read().strip()
        
        if not description:
            raise ValueError("Project description is empty. Please enter a project description first.")
    except FileNotFoundError:
        raise FileNotFoundError("project_description.txt not found. Please enter a project description first (Option 1).")

    prompt = f"""You are an AI assistant that extracts structured project details from free-form text.
Extract the following information and return ONLY valid JSON (no markdown, no code blocks, no explanations, just pure JSON).

CRITICAL: Return ONLY the JSON object. Do not include any text before or after the JSON. Do not use markdown code blocks.

Required JSON structure:
{{
  "name": "Project Name",
  "budget_inr_per_month": <number>,
  "description": "Full project description",
  "tech_stack": {{
    "frontend": "<technology>",
    "backend": "<technology>",
    "database": "<technology>",
    "hosting": "<cloud provider>",
    ... (add other relevant tech stack fields)
  }},
  "non_functional_requirements": ["requirement1", "requirement2", ...]
}}

Project Description:
{description}

Return ONLY the JSON object, nothing else."""

    try:
        profile = call_llm(prompt, max_tokens=1500)
        
        # Validate required fields
        required_fields = ["name", "budget_inr_per_month", "description", "tech_stack", "non_functional_requirements"]
        for field in required_fields:
            if field not in profile:
                raise ValueError(f"Missing required field: {field}")
        
        # Ensure budget is a number
        if not isinstance(profile["budget_inr_per_month"], (int, float)):
            raise ValueError("budget_inr_per_month must be a number")
        
        # Ensure tech_stack is an object
        if not isinstance(profile["tech_stack"], dict):
            raise ValueError("tech_stack must be an object")
        
        # Ensure non_functional_requirements is an array
        if not isinstance(profile["non_functional_requirements"], list):
            raise ValueError("non_functional_requirements must be an array")
        
    except Exception as e:
        raise Exception(f"Failed to extract project profile: {e}")

    with open("data/project_profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print("✅ project_profile.json generated")
    return profile
