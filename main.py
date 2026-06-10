import json
import markdown
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

with open("zap_scan_results.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

vulnerabilities = []
for site in raw.get("site", []):
    for alert in site.get("alerts", []):
        vulnerabilities.append({
            "id": alert.get("pluginid"),
            "vulnerability": alert.get("name"),
            "severity": alert.get("riskdesc"),
            "url": alert.get("instances", [{}])[0].get("uri", "N/A"),
            "description": alert.get("desc", "")
        })

results = []

for vuln in vulnerabilities:
    print(f"Analyzing: {vuln['vulnerability']}...")
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a senior application security analyst.
A DAST scan found the following vulnerability in a logistics web application:

Vulnerability: {vuln['vulnerability']}
Severity: {vuln['severity']}
URL: {vuln['url']}
Description: {vuln['description']}

Provide:
1. A plain-English explanation of the risk (2-3 sentences, written for a developer)
2. A concrete remediation recommendation (2-3 sentences)
Keep it concise and practical."""
            }
        ]
    )
    
    results.append({
        "id": vuln["id"],
        "vulnerability": vuln["vulnerability"],
        "severity": vuln["severity"],
        "url": vuln["url"],
        "ai_analysis": message.content[0].text
    })

html = """
<html>
<head>
    <title>AI Vulnerability Triage Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }
        h1 { color: #2c3e50; }
        .vuln { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 6px solid #e74c3c; }
        .medium { border-left-color: #f39c12; }
        .high { border-left-color: #e74c3c; }
        .severity { font-weight: bold; text-transform: uppercase; }
        .url { color: #7f8c8d; font-size: 0.9em; }
        .ai-analysis { margin-top: 15px; padding: 15px; background: #eaf4fb; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>AI-Assisted Vulnerability Triage Report</h1>
    <p>Generated for: DVWA (Damn Vulnerable Web Application) | Tool: OWASP ZAP + Claude AI</p>
"""

for result in results:
    severity_class = result["severity"].lower()
    html += f"""
    <div class="vuln {severity_class}">
        <h2>{result['vulnerability']}</h2>
        <p class="severity">Severity: {result['severity']}</p>
        <p class="url">URL: {result['url']}</p>
        <div class="ai-analysis">
            <strong>AI Analysis & Recommendation:</strong><br><br>
            {markdown.markdown(result['ai_analysis'])}
        </div>
    </div>
"""

html += """
<footer style="margin-top: 40px; padding: 20px; text-align: center; color: #7f8c8d; font-size: 0.85em; border-top: 1px solid #ddd;">
    © 2026 Muhammed Bilal Ozdemir. All rights reserved.
</footer>
</body></html>"""

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Report generated: report.html")