# Automated Competitor Price Monitoring & Update System

This project demonstrates a complete, automated workflow for **monitoring competitor prices, calculating market-based pricing decisions, and updating product prices automatically**, with full orchestration handled by **n8n** and business logic powered by **Python + FastAPI**.

The system is designed as a **real-world business process automation example**, showing how pricing decisions can be made without manual intervention while still keeping visibility and control.

---

## Overview

The goal of this automation is to **track competitor prices, compare them with the current product price, and decide whether a price update is needed** based on a defined percentage threshold.

The workflow runs on a schedule, collects fresh market data, performs calculations, applies decision logic, updates the product price if required, and sends clear email notifications about the outcome.

---

## Architecture Breakdown

### **1. Product Display (Flask – Example Layer)**
- A simple Flask page is created only as a **visual example**.
- It displays:
  - Product title
  - Product image
  - Current product price
- This page is not part of the automation logic itself, but serves as a **clear visual proof** that the price update works in real time.

---

### **2. Automation Trigger (n8n Schedule Trigger)**
- The process starts with an **n8n Schedule Trigger**.
- It can be configured to run daily, weekly, or at any interval.
- This ensures the pricing logic runs automatically without manual execution.

---

### **3. Market Data Collection (FastAPI + Python Script)**
- n8n triggers a **FastAPI GET endpoint** using an HTTP Request node.
- This endpoint:
  - Executes a Python script that queries competitor prices (via SerpAPI).
  - Filters out unwanted results (used, refurbished, outlet, etc.).
  - Collects valid prices across multiple EU regions.
  - Saves all results into a **CSV file** (overwritten on each run).
  - Calculates the **median price** from the collected data.
- The endpoint returns to n8n:
  - Old product price (from JSON)
  - Median market price (from CSV)
  - Product title
  - Product SKU
  - Number of competitor items found

---

### **4. Data Normalization (n8n)**
- Inside n8n:
  - A **Set node** is used to explicitly convert values to numbers.
  - This ensures safety in case the API returns numeric values as strings.
- Clean numeric data is then passed to the next step.

---

### **5. Price Difference Calculation (n8n Code Node)**
- A Code node calculates the **percentage difference** between:
  - Old price
  - Median market price
- The absolute value of the difference is used to avoid direction issues.
- This prepares the data for decision-making.

---

### **6. Decision Logic (n8n IF Node)**
- The workflow checks:
  - **If the absolute price difference is greater than 5%**
- Two branches are created:
  - **Above 5% difference**
  - **Below or equal to 5% difference**

---

### **7A. Price Update Path (FastAPI POST)**
- If the difference is **greater than 5%**:
  - n8n triggers a **FastAPI POST endpoint**.
  - The new price (median price) is sent as a parameter.
  - FastAPI updates the product price directly in `product_data.json`.
  - The Flask page immediately reflects the new price.
- After updating:
  - An email is sent confirming:
    - Product name
    - Old price
    - New price
    - Confirmation that the price was updated successfully

---

### **7B. No Update Path (Email Notification)**
- If the difference is **below 5%**:
  - No price update is performed.
  - An email is sent stating that:
    - The product price is already aligned with the market
    - No update was required at this time

---

## Data Flow Summary

Schedule Trigger (n8n)
↓  
FastAPI GET → Run Python script → Generate CSV → Calculate median  
↓  
Return old price, median price, title, SKU  
↓  
n8n Set (type normalization)  
↓  
n8n Code (percentage difference calculation)  
↓  
n8n IF (difference > 5%)  
↓  
YES → FastAPI POST → Update price → Send update email  
NO  → Send “price is aligned” email  

---

## Key Features

- **Fully automated pricing logic**
- **Market-based median price calculation**
- **Configurable percentage threshold**
- **CSV overwrite protection (fresh data every run)**
- **FastAPI microservice architecture**
- **Clear decision branching**
- **Real-time price update visibility**
- **Business-ready email notifications**
- **Clean separation of logic and orchestration**

---

## Requirements

- Python 3.10+
- FastAPI
- Flask (demo page)
- n8n automation platform
- SerpAPI key
- Docker or mounted volumes for shared files
- Email provider credentials

---

## Why This Project Matters

This project demonstrates real-world skills in:

- Business process automation
- API-driven architectures
- Data collection and validation
- Pricing logic and decision thresholds
- Workflow orchestration with n8n
- Backend system integration
- Automation-first thinking

It is a strong portfolio example of how **automation can replace repetitive pricing decisions**, reduce manual work, and keep product pricing aligned with the market automatically.
