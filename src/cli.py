import json
import os
from src.profile_extractor import extract_project_profile
from src.billing_generator import generate_billing
from src.cost_analyzer import analyze_cost

def view_recommendations():
    """Display recommendations from the cost optimization report."""
    try:
        with open("data/cost_optimization_report.json", "r", encoding="utf-8") as f:
            report = json.load(f)
    except FileNotFoundError:
        print("❌ No cost optimization report found. Please run 'Complete Cost Analysis' first.")
        return
    
    analysis = report.get("analysis", {})
    recommendations = report.get("recommendations", [])
    summary = report.get("summary", {})
    
    print("\n" + "="*70)
    print(f"Project: {report.get('project_name', 'N/A')}")
    print("="*70)
    print(f"\nCost Analysis:")
    print(f"  Total Monthly Cost: ₹{analysis.get('total_monthly_cost', 0)}")
    print(f"  Budget: ₹{analysis.get('budget', 0)}")
    print(f"  Variance: ₹{analysis.get('budget_variance', 0)} ({'Over' if analysis.get('is_over_budget') else 'Under'} budget)")
    print(f"\nPotential Savings: ₹{summary.get('total_potential_savings', 0)} ({summary.get('savings_percentage', 0)}%)")
    print(f"Total Recommendations: {summary.get('recommendations_count', 0)}")
    
    print("\n" + "-"*70)
    print("RECOMMENDATIONS:")
    print("-"*70)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.get('title', 'N/A')}")
        print(f"   Service: {rec.get('service', 'N/A')}")
        print(f"   Current Cost: ₹{rec.get('current_cost', 0)}")
        print(f"   Potential Savings: ₹{rec.get('potential_savings', 0)}")
        print(f"   Type: {rec.get('recommendation_type', 'N/A')}")
        print(f"   Effort: {rec.get('implementation_effort', 'N/A')} | Risk: {rec.get('risk_level', 'N/A')}")
        print(f"   Description: {rec.get('description', 'N/A')}")
        print(f"   Cloud Providers: {', '.join(rec.get('cloud_providers', []))}")
        print(f"   Steps:")
        for step in rec.get('steps', []):
            print(f"     - {step}")

def export_report():
    """Export the cost optimization report to a readable format."""
    try:
        with open("data/cost_optimization_report.json", "r", encoding="utf-8") as f:
            report = json.load(f)
    except FileNotFoundError:
        print("❌ No cost optimization report found. Please run 'Complete Cost Analysis' first.")
        return
    
    # Export as text file
    output_file = "data/cost_optimization_report.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("="*70 + "\n")
        f.write(f"COST OPTIMIZATION REPORT\n")
        f.write("="*70 + "\n\n")
        f.write(f"Project: {report.get('project_name', 'N/A')}\n\n")
        
        analysis = report.get("analysis", {})
        f.write("COST ANALYSIS\n")
        f.write("-"*70 + "\n")
        f.write(f"Total Monthly Cost: ₹{analysis.get('total_monthly_cost', 0)}\n")
        f.write(f"Budget: ₹{analysis.get('budget', 0)}\n")
        f.write(f"Budget Variance: ₹{analysis.get('budget_variance', 0)}\n")
        f.write(f"Status: {'OVER BUDGET' if analysis.get('is_over_budget') else 'WITHIN BUDGET'}\n\n")
        
        f.write("Service Costs:\n")
        for service, cost in analysis.get('service_costs', {}).items():
            f.write(f"  {service}: ₹{cost}\n")
        f.write("\n")
        
        summary = report.get("summary", {})
        f.write("SUMMARY\n")
        f.write("-"*70 + "\n")
        f.write(f"Total Potential Savings: ₹{summary.get('total_potential_savings', 0)}\n")
        f.write(f"Savings Percentage: {summary.get('savings_percentage', 0)}%\n")
        f.write(f"Recommendations Count: {summary.get('recommendations_count', 0)}\n\n")
        
        recommendations = report.get("recommendations", [])
        f.write("RECOMMENDATIONS\n")
        f.write("-"*70 + "\n\n")
        
        for i, rec in enumerate(recommendations, 1):
            f.write(f"{i}. {rec.get('title', 'N/A')}\n")
            f.write(f"   Service: {rec.get('service', 'N/A')}\n")
            f.write(f"   Current Cost: ₹{rec.get('current_cost', 0)}\n")
            f.write(f"   Potential Savings: ₹{rec.get('potential_savings', 0)}\n")
            f.write(f"   Type: {rec.get('recommendation_type', 'N/A')}\n")
            f.write(f"   Implementation Effort: {rec.get('implementation_effort', 'N/A')}\n")
            f.write(f"   Risk Level: {rec.get('risk_level', 'N/A')}\n")
            f.write(f"   Description: {rec.get('description', 'N/A')}\n")
            f.write(f"   Cloud Providers: {', '.join(rec.get('cloud_providers', []))}\n")
            f.write(f"   Implementation Steps:\n")
            for step in rec.get('steps', []):
                f.write(f"     - {step}\n")
            f.write("\n")
    
    print(f"✅ Report exported to {output_file}")

def menu():
    """Main CLI menu for Cloud Cost Optimizer."""
    while True:
        print("\n" + "="*50)
        print("   Cloud Cost Optimizer (LLM-Driven)")
        print("="*50)
        print("1. Enter new project description")
        print("2. Run Complete Cost Analysis")
        print("3. View Recommendations")
        print("4. Export Report")
        print("5. Exit")
        print("="*50)

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            print("\nEnter your project description (press Enter twice to finish):")
            lines = []
            while True:
                try:
                    line = input()
                    if line == "" and lines and lines[-1] == "":
                        break
                    lines.append(line)
                except EOFError:
                    break
            
            description = "\n".join(lines).strip()
            
            if not description:
                print("❌ Project description cannot be empty.")
                continue
            
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            
            with open("data/project_description.txt", "w", encoding="utf-8") as f:
                f.write(description)
            
            print("✅ Project description saved to data/project_description.txt")

        elif choice == "2":
            print("\n🔄 Running Complete Cost Analysis...")
            print("-"*50)
            try:
                print("\nStep 1: Extracting project profile...")
                extract_project_profile()
                
                print("\nStep 2: Generating synthetic billing data...")
                generate_billing()
                
                print("\nStep 3: Analyzing costs and generating recommendations...")
                analyze_cost()
                
                print("\n" + "="*50)
                print("✅ Complete Cost Analysis finished successfully!")
                print("="*50)
            except Exception as e:
                print(f"\n❌ Error during analysis: {e}")
                print("Please check your inputs and try again.")

        elif choice == "3":
            view_recommendations()

        elif choice == "4":
            export_report()

        elif choice == "5":
            print("\n👋 Thank you for using Cloud Cost Optimizer!")
            break
        else:
            print("❌ Invalid option. Please choose 1-5.")
