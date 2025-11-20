import json
import urllib3
import time
import boto3

cloudwatch = boto3.client("cloudwatch")
http = urllib3.PoolManager()

URLS = [
    "https://aws.amazon.com",
    "https://example.com",
    "https://www.githubstatus.com",
    "https://www.google.com"
]

def lambda_handler(event, context):
    for url in URLS:
        start = time.time()

        try:
            response = http.request("GET", url, timeout=5.0)
            latency = (time.time() - start) * 1000
            available = 1 if response.status == 200 else 0

        except Exception:
            latency = 0
            available = 0

        metric_dimensions = [
            {"Name": "URL", "Value": url}
        ]

        cloudwatch.put_metric_data(
            Namespace="UptimeChecker",
            MetricData=[
                {
                    "MetricName": "Availability",
                    "Dimensions": metric_dimensions,
                    "Value": available
                },
                {
                    "MetricName": "LatencyMs",
                    "Dimensions": metric_dimensions,
                    "Value": latency
                }
            ]
        )

    return {"status": "ok"}
