import json
from src.llm_client import call_llm

def generate_billing():
    """
    Generate realistic synthetic cloud billing data (12-20 records) based on project profile.
    Output: mock_billing.json with billing records including month, service, resource_id, 
    region, usage_type, usage_quantity, unit, cost_inr, desc.
    """
    try:
        with open("data/project_profile.json", "r") as f:
            profile = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("project_profile.json not found. Please run profile extraction first.")

    budget = profile.get("budget_inr_per_month", 10000)
    tech_stack = profile.get("tech_stack", {})
    name = profile.get("name", "Project")

    prompt = f"""You are a cloud billing data generator. Generate realistic synthetic cloud billing records.
Generate 12-20 billing records as a JSON array. Each record must have these exact fields:

CRITICAL: Return ONLY the JSON array. Do not include any text before or after the JSON. Do not use markdown code blocks.

Required structure for each record:
{{
  "month": "YYYY-MM",
  "service": "<service name like EC2, RDS, S3, Lambda, etc>",
  "resource_id": "<unique resource identifier>",
  "region": "<AWS region like ap-south-1, us-east-1, etc>",
  "usage_type": "<usage type description>",
  "usage_quantity": <number>,
  "unit": "<unit like hours, GB, requests, etc>",
  "cost_inr": <number>,
  "desc": "<description of the resource>"
}}

Rules:
1. Generate EXACTLY 12-20 records (preferably 15-18)
2. Total monthly cost should be close to but can exceed budget: ₹{budget} INR per month
3. Distribute costs across: compute (EC2, Lambda), database (RDS, DynamoDB), storage (S3), networking (CloudFront, Load Balancer), monitoring (CloudWatch)
4. Use realistic AWS service names and regions
5. Generate records for a single month (use same month for all records, e.g., "2025-01")
6. Ensure resource_id is unique for each record
7. Make usage_quantity and cost_inr realistic and proportional
8. Include variety: some high-cost items, some low-cost items

Project Profile:
{json.dumps(profile, indent=2)}

Return ONLY a JSON array, nothing else. No markdown, no code blocks, no explanations."""

    try:
        billing = call_llm(prompt, max_tokens=3000, return_array=True)
        
        # Validate it's a list
        if not isinstance(billing, list):
            raise ValueError("Billing data must be an array")
        
        # Validate record count
        if len(billing) < 12 or len(billing) > 20:
            print(f"Warning: Generated {len(billing)} records, expected 12-20")
        
        # Validate each record has required fields
        required_fields = ["month", "service", "resource_id", "region", "usage_type", 
                          "usage_quantity", "unit", "cost_inr", "desc"]
        for i, record in enumerate(billing):
            if not isinstance(record, dict):
                raise ValueError(f"Record {i} is not an object")
            for field in required_fields:
                if field not in record:
                    raise ValueError(f"Record {i} missing required field: {field}")
        
    except Exception as e:
        raise Exception(f"Failed to generate billing data: {e}")

    with open("data/mock_billing.json", "w", encoding="utf-8") as f:
        json.dump(billing, f, indent=2, ensure_ascii=False)

    print(f"✅ mock_billing.json generated with {len(billing)} records")
    return billing
