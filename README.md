# AI Vulnerability Triage Tool

An AI-assisted security tool that parses real DAST scan results from OWASP ZAP and automatically generates plain-English remediation reports using the Claude API.

## The Problem
Security teams using DAST scanners like OWASP ZAP can generate dozens of vulnerability findings per scan. Manually writing remediation documentation for each finding is time-consuming and creates reporting bottlenecks for analysts.

## The Solution
This tool automates the triage and documentation process by:
- Ingesting real OWASP ZAP scan output (JSON format)
- Sending each finding to Claude API using role-based prompt engineering
- Generating a structured, colour-coded HTML report with plain-English risk explanations and remediation recommendations

## Demo
The tool was tested by running OWASP ZAP against DVWA (Damn Vulnerable Web Application) hosted locally via Docker. Real vulnerabilities including CSP misconfigurations, missing security headers, and authentication weaknesses were discovered and documented automatically.

## Tech Stack
- Python
- Claude API (Anthropic)
- OWASP ZAP (DAST scanning)
- Docker + DVWA (local scan target)

## Security Practices
- API keys stored in `.env` file, never hardcoded
- `.gitignore` excludes all sensitive files
- AI-generated recommendations are intended for human analyst review before action

## Prerequisites
- Python 3.x
- Docker Desktop (to run DVWA locally)
- OWASP ZAP
- Anthropic API key

## How To Run
1. Clone the repo
2. Install dependencies: `pip install anthropic python-dotenv markdown`
3. Add your Claude API key to a `.env` file: `ANTHROPIC_API_KEY=your-key-here`
4. Run DVWA locally: `docker run -d -p 80:80 --name dvwa vulnerables/web-dvwa`
5. Scan DVWA using OWASP ZAP:
   - Open ZAP and run an Automated Scan against `http://localhost`
   - Once complete, go to Report → Generate Report
   - Select "Traditional JSON Report" as the template
   - Save the file as `zap_scan_results.json` into the project folder
6. Run: `python main.py`
7. Open `report.html` in your browser

## Sample Data
A sample scan results file `sample_scan_results.json` is included for testing without running a full ZAP scan.

## Limitations
- Authenticated scanning not yet configured — only publicly accessible pages are scanned
- AI-generated analysis may require human review for accuracy
- Currently processes one scan file at a time

## Future Improvements
- Direct integration with OWASP ZAP API to automate scan triggering and JSON export
- OWASP Top 10 mapping for each finding
- Severity-based filtering and prioritization
- Modular codebase separating scanning, analysis, and reporting concerns