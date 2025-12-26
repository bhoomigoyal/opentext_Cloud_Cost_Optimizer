# AI-Powered Cloud Cost Optimizer (LLM-Driven)

An intelligent cloud cost optimization tool that analyzes project descriptions, generates synthetic billing data, and provides actionable multi-cloud cost optimization recommendations using Large Language Models (LLMs).

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Sample Output](#sample-output)
- [Tools Used](#tools-used)
- [Step-by-Step Testing](#step-by-step-testing)
- [Troubleshooting](#troubleshooting)

## Overview

This project implements an AI-powered cloud cost optimization system that:
1. Extracts structured project profiles from free-form text descriptions using LLMs
2. Generates realistic, budget-aware synthetic cloud billing data (12-20 records)
3. Analyzes costs against budgets and generates 6-10 actionable optimization recommendations
4. Provides multi-cloud alternatives (AWS, Azure, GCP) and open-source solutions

## Features

### Mandatory Features

- ✅ **Project Profile Extraction** - LLM-based extraction from free-form text
  - Extracts: name, budget, description, tech stack, non-functional requirements
  - Output: `project_profile.json`

- ✅ **Synthetic Billing Generation** - Creates realistic cloud billing data
  - Generates 12-20 billing records
  - Budget-aware cost distribution
  - Includes: compute, database, storage, networking, monitoring services
  - Output: `mock_billing.json`

- ✅ **Cost Analysis & Recommendations** - Multi-cloud optimization suggestions
  - Analyzes costs vs budget
  - Generates 6-10 detailed recommendations
  - Includes: open-source alternatives, free-tier options, multi-cloud alternatives
  - Output: `cost_optimization_report.json`

- ✅ **CLI Menu-Driven Interface** - User-friendly command-line interface
  - Option 1: Enter new project description
  - Option 2: Run Complete Cost Analysis
  - Option 3: View Recommendations
  - Option 4: Export Report

## Prerequisites

- **Python 3.10+** (tested with Python 3.10.9)
- **Hugging Face API Key** - Get it from [Hugging Face Settings](https://huggingface.co/settings/tokens)
- **Internet Connection** - Required for LLM API calls

## Installation

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd cloud-cost-optimizer
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Create `.env` File
Create a `.env` file in the project root directory:

```env
HF_API_KEY=huggingface_api_key_here
HF_MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
```

**Note:** Replace `huggingface_api_key_here` with actual Hugging Face API key.

### Step 2: Get API Key
1. Go to [Hugging Face](https://huggingface.co/)
2. Sign up/Login
3. Navigate to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
4. Create a new token (read access is sufficient)
5. Copy the token and paste it in `.env` file

## Usage

we can use the application in two ways:
1. **Menu-Based Usage** - Use the interactive CLI menu (Recommended for beginners)
2. **Manual Testing** - Test individual components using command-line (For developers/testing)

---

## Option 1: Menu-Based Usage (Recommended)

### Quick Start

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Here see the menu:**
   ```
   ==================================================
      Cloud Cost Optimizer (LLM-Driven)
   ==================================================
   1. Enter new project description
   2. Run Complete Cost Analysis
   3. View Recommendations
   4. Export Report
   5. Exit
   ==================================================
   ```

### Step-by-Step Menu Workflow

#### Step 1: Enter Project Description
- Select option **1** from the menu
- Enter project description in free-form text
- Press Enter twice to finish
- Description is saved to `data/project_description.txt`

**Example Input:**
```
I want to build a food delivery app.
Backend: Node.js
Database: PostgreSQL
Hosting: AWS
Budget: 50000 per month
```

#### Step 2: Run Complete Cost Analysis
- Select option **2** from the menu
- The system will automatically:
  1. Extract project profile → `project_profile.json`
  2. Generate billing data → `mock_billing.json`
  3. Analyze costs and generate recommendations → `cost_optimization_report.json`

#### Step 3: View Recommendations
- Select option **3** from the menu
- View detailed cost analysis and recommendations

#### Step 4: Export Report
- Select option **4** from the menu
- Export a readable text report → `data/cost_optimization_report.txt`

**That's it!** The menu-based approach is simple and user-friendly.

---

## Option 2: Manual Testing (Step-by-Step Commands)

If want to test individual components manually or understand how each part works, follow these commands step by step.

## Project Structure

```
cloud-cost-optimizer/
├── src/
│   ├── llm_client.py          # LLM API client (Hugging Face)
│   ├── profile_extractor.py   # Project profile extraction
│   ├── billing_generator.py   # Synthetic billing generation
│   ├── cost_analyzer.py       # Cost analysis & recommendations
│   └── cli.py                 # Command-line interface
├── data/
│   ├── project_description.txt        # Input: User's project description
│   ├── project_profile.json           # Output: Structured profile
│   ├── mock_billing.json              # Output: Synthetic billing (12-20 records)
│   └── cost_optimization_report.json  # Output: Analysis & recommendations
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
└── README.md                  # This file
```

## Sample Output

### Project Profile (`project_profile.json`)
```json
{
  "name": "Food Delivery App",
  "budget_inr_per_month": 50000,
  "description": "A scalable food delivery platform serving ~10k monthly users.",
  "tech_stack": {
    "backend": "Node.js",
    "database": "PostgreSQL",
    "hosting": "AWS"
  },
  "non_functional_requirements": ["Scalability", "Cost efficiency", "Monitoring"]
}
```

### Billing Data (`mock_billing.json`)
```json
[
  {
    "month": "2025-01",
    "service": "EC2",
    "resource_id": "i-food-delivery-api-01",
    "region": "ap-south-1",
    "usage_type": "Linux/UNIX (on-demand)",
    "usage_quantity": 720,
    "unit": "hours",
    "cost_inr": 15000,
    "desc": "Backend API server"
  }
]
```

### Cost Optimization Report (`cost_optimization_report.json`)
```json
{
  "project_name": "Food Delivery App",
  "analysis": {
    "total_monthly_cost": 139900,
    "budget": 50000,
    "budget_variance": 89900,
    "is_over_budget": true,
    "service_costs": {
      "EC2": 45000,
      "RDS": 30000,
      "S3": 15000
    }
  },
  "recommendations": [
    {
      "title": "Migrate RDS to PostgreSQL on Open Source",
      "service": "RDS",
      "current_cost": 30000,
      "potential_savings": 16875,
      "recommendation_type": "open_source",
      "description": "Migrate to open-source PostgreSQL...",
      "implementation_effort": "medium",
      "risk_level": "medium",
      "steps": ["Assess migration requirements", "Plan migration", "Execute migration"],
      "cloud_providers": ["AWS", "Azure", "GCP"]
    }
  ],
  "summary": {
    "total_potential_savings": 67510,
    "savings_percentage": 48.3,
    "recommendations_count": 8
  }
}
```

## Tools Used

- **Python 3.10+** - Programming language
- **Hugging Face Inference API** - LLM access (meta-llama/Llama-3.1-8B-Instruct)
- **requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management
- **jsonschema** - JSON validation (optional)

---

## Option 2: Manual Testing (Step-by-Step Commands)

If want to test individual components manually or understand how each part works, follow these commands step by step.

### Prerequisites for Manual Testing

Before starting, ensure:
- Virtual environment is activated
- `.env` file is configured with API key
- Dependencies are installed

### Manual Testing Steps

Follow these commands **in order** to test each component:

### **STEP 1: Activate Virtual Environment**
```powershell
.\venv\Scripts\Activate.ps1
```
**What it does:** Activates Python virtual environment  

---

### **STEP 2: Verify Prerequisites**
```powershell
python --version
```
**Expected:** Should show Python 3.10.x or higher

---

### **STEP 3: Check Environment Variables**
```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', 'Set' if os.getenv('HF_API_KEY') else 'Missing'); print('Model:', os.getenv('HF_MODEL_NAME', 'Using default'))"
```
**Expected:** Should show "API Key: Set" and model name

---

### **STEP 4: Test LLM Client (First Component)**
```powershell
python -c "from src.llm_client import call_llm; result = call_llm('Return JSON only: {\"test\":\"ok\", \"status\":true}'); print('✅ LLM Result:', result)"
```
**Expected:** Should print `✅ LLM Result: {'test': 'ok', 'status': True}`  
**If error:** Check API key and model configuration

---

### **STEP 5: Check Project Description Exists**
```powershell
python -c "import os; print('✅ Description exists' if os.path.exists('data/project_description.txt') and os.path.getsize('data/project_description.txt') > 0 else '❌ Need to create description')"
```
**Expected:** Should show if description file exists  
**If missing:** create it in STEP 6

---

### **STEP 6: Test Profile Extraction (Second Component)**
```powershell
python -c "from src.profile_extractor import extract_project_profile; profile = extract_project_profile(); print('✅ Profile Name:', profile['name']); print('✅ Budget: ₹' + str(profile['budget_inr_per_month']) + '/month')"
```
**Expected:** Should print profile name and budget  
**What it does:** Creates `data/project_profile.json`

---

### **STEP 7: Verify Profile File Created**
```powershell
python -c "import json, os; f='data/project_profile.json'; print('✅ File exists:', os.path.exists(f)); p=json.load(open(f)); print('Name:', p['name']); print('Budget:', p['budget_inr_per_month'])"
```
**Expected:** Should show file exists and display name/budget

---

### **STEP 8: Test Billing Generation (Third Component)**
```powershell
python -c "from src.billing_generator import generate_billing; billing = generate_billing(); print('✅ Generated', len(billing), 'billing records')"
```
**Expected:** Should print `✅ Generated 12-20 billing records`  
**What it does:** Creates `data/mock_billing.json`

---

### **STEP 9: Verify Billing File Created**
```powershell
python -c "import json; b=json.load(open('data/mock_billing.json')); print('✅ Records:', len(b)); print('✅ Total Cost: ₹' + str(sum(r['cost_inr'] for r in b)))"
```
**Expected:** Should show number of records and total cost

---

### **STEP 10: Test Cost Analysis (Fourth Component)**
```powershell
python -c "from src.cost_analyzer import analyze_cost; report = analyze_cost(); print('✅ Generated', len(report['recommendations']), 'recommendations')"
```
**Expected:** Should print `✅ Generated 6-10 recommendations`  
**What it does:** Creates `data/cost_optimization_report.json`

---

### **STEP 11: Verify All Output Files**
```powershell
python -c "import os; files = ['project_profile.json', 'mock_billing.json', 'cost_optimization_report.json']; [print('✅ ' + f if os.path.exists('data/' + f) else '❌ ' + f) for f in files]"
```
**Expected:** Should show ✅ for all three files

---

### **STEP 12: Test Full CLI Application**
```powershell
python main.py
```
**What to do:**
1. Select option **1** - Enter project description (or skip if already exists)
2. Select option **2** - Run Complete Cost Analysis
3. Select option **3** - View Recommendations
4. Select option **4** - Export Report
5. Select option **5** - Exit

---

### Quick Reference - Copy & Paste Commands

**Copy these commands one by one and run them in order:**

```powershell
# Step 1: Activate Virtual Environment
.\venv\Scripts\Activate.ps1

# Step 2: Verify Prerequisites
python --version

# Step 3: Check Environment Variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', 'Set' if os.getenv('HF_API_KEY') else 'Missing'); print('Model:', os.getenv('HF_MODEL_NAME', 'Using default'))"

# Step 4: Test LLM Client
python -c "from src.llm_client import call_llm; result = call_llm('Return JSON only: {\"test\":\"ok\", \"status\":true}'); print('✅ LLM Result:', result)"

# Step 5: Check Project Description
python -c "import os; print('✅ Description exists' if os.path.exists('data/project_description.txt') and os.path.getsize('data/project_description.txt') > 0 else '❌ Need to create description')"

# Step 6: Test Profile Extraction
python -c "from src.profile_extractor import extract_project_profile; profile = extract_project_profile(); print('✅ Profile Name:', profile['name']); print('✅ Budget: ₹' + str(profile['budget_inr_per_month']) + '/month')"

# Step 7: Verify Profile File
python -c "import json, os; f='data/project_profile.json'; print('✅ File exists:', os.path.exists(f)); p=json.load(open(f)); print('Name:', p['name']); print('Budget:', p['budget_inr_per_month'])"

# Step 8: Test Billing Generation
python -c "from src.billing_generator import generate_billing; billing = generate_billing(); print('✅ Generated', len(billing), 'billing records')"

# Step 9: Verify Billing File
python -c "import json; b=json.load(open('data/mock_billing.json')); print('✅ Records:', len(b)); print('✅ Total Cost: ₹' + str(sum(r['cost_inr'] for r in b)))"

# Step 10: Test Cost Analysis
python -c "from src.cost_analyzer import analyze_cost; report = analyze_cost(); print('✅ Generated', len(report['recommendations']), 'recommendations')"

# Step 11: Verify All Output Files
python -c "import os; files = ['project_profile.json', 'mock_billing.json', 'cost_optimization_report.json']; [print('✅ ' + f if os.path.exists('data/' + f) else '❌ ' + f) for f in files]"

# Step 12: Test Full CLI Application
python main.py
```
