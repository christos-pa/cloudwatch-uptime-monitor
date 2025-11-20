# CloudWatch Uptime & Latency Monitor

AWS-based monitoring stack that checks website availability and response time, 
pushes custom metrics into **Amazon CloudWatch**, and visualises them on a 
custom **CloudWatch Dashboard**.

It’s a small but complete monitoring system you can reuse for any HTTP endpoint 
(SaaS status pages, customer portals, parking systems, etc).

---

## 🧱 Architecture Overview

**Components:**

- **AWS Lambda** (`uptime-checker`)
  - Runs on a schedule (e.g. every 5 minutes via EventBridge)
  - Sends HTTP GET requests to a list of URLs
  - Measures response time in milliseconds
  - Writes custom metrics to CloudWatch

- **Amazon CloudWatch Metrics**
  - **Namespace:** `UptimeChecker`
  - **Metric 1 – Availability**
    - Dimension: `URL`
    - Value: `1` if endpoint is up (HTTP 2xx–3xx), `0` if down
  - **Metric 2 – LatencyMs**
    - Dimension: `URL`
    - Value: response time in milliseconds

- **CloudWatch Dashboard**
  - Line graph: **LatencyMs** for all URLs over time  
  - Line graph: **Availability** for all URLs over time  
  - Number tiles: **Average Uptime (%)** per URL  
  - Number tiles: **Average Latency (ms)** per URL  
  - Text headers: “Uptime & Latency Monitor” and “Trends Over Time”

---

## 🚀 What this project demonstrates

- How to **emit custom metrics** from Lambda to CloudWatch
- How to use **dimensions** (e.g. `URL`) to split metrics per endpoint
- How to build a **CloudWatch Dashboard** with:
  - Line graphs
  - Number widgets
  - Text / Markdown widgets
- Basic uptime checking logic suitable for small systems or demos

This is ideal as a portfolio piece for DevOps / Cloud / SRE roles.

---

## 📂 Repository Structure

```text
cloudwatch-uptime-monitor/
├─ lambda/
│  └─ uptime_checker.py          # Lambda function that checks URLs & pushes metrics
├─ dashboard/
│  └─ uptime-monitor-dashboard.json   # Exported CloudWatch dashboard JSON (example)
└─ README.md
