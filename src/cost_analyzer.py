import json
from collections import defaultdict
from src.llm_client import call_llm

def analyze_cost():
    """
    Analyze costs and generate optimization recommendations.
    Input: project_profile.json, mock_billing.json
    Output: cost_optimization_report.json with analysis and detailed recommendations.
    """
    try:
        with open("data/project_profile.json", "r") as f:
            profile = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("project_profile.json not found. Please run profile extraction first.")

    try:
        with open("data/mock_billing.json", "r") as f:
            billing = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("mock_billing.json not found. Please run billing generation first.")

    # Calculate total cost
    total_cost = sum(item["cost_inr"] for item in billing)

    # Calculate service costs
    service_costs = defaultdict(int)
    for item in billing:
        service_costs[item["service"]] += item["cost_inr"]

    # Find high cost services (top 3)
    sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
    high_cost_services = {service: cost for service, cost in sorted_services[:3]}

    budget = profile["budget_inr_per_month"]
    budget_variance = total_cost - budget
    is_over_budget = total_cost > budget

    analysis = {
        "total_monthly_cost": total_cost,
        "budget": budget,
        "budget_variance": budget_variance,
        "service_costs": dict(service_costs),
        "high_cost_services": high_cost_services,
        "is_over_budget": is_over_budget
    }

    # Generate recommendations using LLM
    prompt = f"""You are a cloud cost optimization expert. Generate 6-10 detailed cost optimization recommendations.

CRITICAL: Return ONLY the JSON object. Do not include any text before or after the JSON. Do not use markdown code blocks.

Return ONLY a JSON object with this exact structure:
{{
  "recommendations": [
    {{
      "title": "<recommendation title>",
      "service": "<service name>",
      "current_cost": <number>,
      "potential_savings": <number>,
      "recommendation_type": "<open_source|free_tier|alternative_provider|optimization|right_sizing|cost-effective_storage>",
      "description": "<detailed description>",
      "implementation_effort": "<low|medium|high>",
      "risk_level": "<low|medium|high>",
      "steps": ["step1", "step2", "step3"],
      "cloud_providers": ["AWS", "Azure", "GCP", "Open Source", ...]
    }},
    ...
  ]
}}

Requirements:
1. Generate EXACTLY 6-10 recommendations (preferably 7-9)
2. Include multi-cloud alternatives (AWS, Azure, GCP)
3. Include open-source/free-tier alternatives where applicable
4. Focus on high-cost services first
5. Each recommendation must have all fields above
6. recommendation_type should be one of: open_source, free_tier, alternative_provider, optimization, right_sizing, cost-effective_storage
7. Make potential_savings realistic (typically 20-50% of current_cost)
8. Include at least one open-source alternative recommendation
9. Each recommendation must have at least 3 steps in the steps array

Project Profile:
{json.dumps(profile, indent=2)}

Cost Analysis:
{json.dumps(analysis, indent=2)}

Billing Data (sample):
{json.dumps(billing[:5], indent=2)}

Return ONLY the JSON object with recommendations array, nothing else."""

    try:
        llm_response = call_llm(prompt, max_tokens=4000)
        
        # Extract recommendations
        if isinstance(llm_response, dict) and "recommendations" in llm_response:
            recommendations = llm_response["recommendations"]
        elif isinstance(llm_response, list):
            recommendations = llm_response
        else:
            raise ValueError("LLM response format invalid")
        
        # Validate recommendations structure
        required_fields = ["title", "service", "current_cost", "potential_savings", 
                          "recommendation_type", "description", "implementation_effort", 
                          "risk_level", "steps", "cloud_providers"]
        
        for i, rec in enumerate(recommendations):
            if not isinstance(rec, dict):
                raise ValueError(f"Recommendation {i} is not an object")
            for field in required_fields:
                if field not in rec:
                    raise ValueError(f"Recommendation {i} missing required field: {field}")
        
        # Calculate summary statistics
        total_potential_savings = sum(rec.get("potential_savings", 0) for rec in recommendations)
        savings_percentage = (total_potential_savings / total_cost * 100) if total_cost > 0 else 0
        high_impact_count = sum(1 for rec in recommendations if rec.get("potential_savings", 0) > total_cost * 0.1)
        
        summary = {
            "total_potential_savings": total_potential_savings,
            "savings_percentage": round(savings_percentage, 2),
            "recommendations_count": len(recommendations),
            "high_impact_recommendations": high_impact_count
        }
        
    except Exception as e:
        raise Exception(f"Failed to generate recommendations: {e}")

    # Build final report
    report = {
        "project_name": profile["name"],
        "analysis": analysis,
        "recommendations": recommendations,
        "summary": summary
    }

    with open("data/cost_optimization_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("✅ cost_optimization_report.json generated")
    print(f"   Total Cost: ₹{total_cost}")
    print(f"   Budget: ₹{budget}")
    print(f"   Variance: ₹{budget_variance} ({'Over' if is_over_budget else 'Under'} budget)")
    print(f"   Recommendations: {len(recommendations)}")
    print(f"   Potential Savings: ₹{total_potential_savings} ({savings_percentage:.2f}%)")
    
    return report
