# CloudWatch Uptime & Latency Monitor – Architecture

This document explains how the uptime/latency monitoring stack is built around
AWS Lambda, CloudWatch Metrics, and a custom CloudWatch Dashboard.

---

## 1. High-Level Design

**Goal:** Continuously check a list of HTTP endpoints and surface:

- **Latency (ms)** for each request
- **Availability (1/0)** for success / failure
- Clean visualisation in a **CloudWatch Dashboard**
- Room to add **alarms and notifications** later (SNS / email / Slack, etc.)

---

## 2. Components

### 2.1 AWS Lambda – `uptime-checker.py`

- Python Lambda function.
- Reads a list of URLs from an environment variable or inline list.
- For each URL, performs an HTTP GET and measures:
  - response time in milliseconds
  - whether the status code is considered “healthy” (e.g. 200–399).
- Publishes custom metrics to CloudWatch using `put_metric_data`:
  - `Namespace`: **UptimeChecker**
  - `Metrics`:
    - `LatencyMs` (dimension: `URL`)
    - `Availability` (1 = up, 0 = down, dimension: `URL`)

### 2.2 EventBridge (CloudWatch Events) – Scheduler

- A **rule** triggers the Lambda function periodically  
  (for example **every 5 minutes**).
- Keeps the Lambda “serverless” – no EC2 or containers are needed.
- The frequency can be tuned per environment (prod vs dev).

### 2.3 CloudWatch Metrics

- Stores the time-series data sent by the Lambda:
  - `UptimeChecker / LatencyMs`
  - `UptimeChecker / Availability`
- Dimensions:
  - `URL` – one metric stream per endpoint.
- Retention and resolution use CloudWatch defaults
  (can be customised if needed).

### 2.4 CloudWatch Dashboard

Defined in **`cloudwatch-dashboard.json`**.

The dashboard includes:

1. **LatencyMs time-series graph**  
   – shows all URLs, useful to spot spikes and slowdowns.

2. **Availability (%) time-series graph**  
   – shows whether any endpoint has dropped out over time.

3. **“Trends Over Time” section** (text widget)  
   – labels the bottom part of the dashboard.

4. **Average Uptime tiles (Number widgets)**  
   – single-value tiles per URL so you can instantly see which
     endpoint has the best/worst uptime over the selected time range.

The JSON file makes the dashboard **reproducible**:  
you can import it into any AWS account without clicking around.

---

## 3. Data Flow

1. **EventBridge** triggers the Lambda on a schedule.
2. **Lambda** calls each URL:
   - measures latency
   - classifies the request as up/down
   - sends one or more `PutMetricData` calls to CloudWatch.
3. **CloudWatch Metrics** stores the latency and availability values.
4. **CloudWatch Dashboard** queries those metrics and renders:
   - graphs (Latencies & Availability)
   - summary tiles (Average Uptime / Average Latency).
5. (Optional future step) **CloudWatch Alarms** watch the metrics and
   push notifications via SNS (email, Slack, Teams, etc.) when:
   - latency goes above a threshold
   - availability drops below 1 for a given period.

---

## 4. Deployment Notes

Typical deployment steps:

1. Create the **Lambda function** and upload `uptime-checker.py`.
2. Add necessary **IAM permissions**:
   - `cloudwatch:PutMetricData`
   - basic Lambda execution permissions (logs, etc.).
3. Configure an **EventBridge schedule rule**  
   (e.g. `rate(5 minutes)`) targeting the Lambda.
4. In CloudWatch **Dashboards**, create a new dashboard and  
   **import `cloudwatch-dashboard.json`**.
5. Select a time range (e.g. last 1h / last 3h) and confirm metrics are
   appearing.

---

## 5. Future Improvements

Ideas you could add later:

- Add **CloudWatch Alarms** and SNS notifications.
- Read endpoints from:
  - a **DynamoDB table** or
  - **SSM Parameter Store** instead of hard-coded list.
- Tag metrics by **environment** (dev / test / prod).
- Export metrics to **Prometheus / Grafana** or other monitoring stacks.

---

This architecture keeps everything **serverless, simple, and cheap**,
but still gives a professional monitoring view for any HTTP-based system.
