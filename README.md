# AI Vulnerability Triage Tool

An AI-assisted security tool that parses DAST scan results and automatically generates plain-English remediation reports using the Claude API.

## The Problem
Security teams using DAST scanners like OWASP ZAP can generate hundreds of vulnerability findings per scan. Manually writing remediation documentation for each finding is time-consuming and creates reporting bottlenecks.

## The Solution
This tool automates the triage and documentation process by:
- Ingesting vulnerability scan output (JSON format)
- Sending each finding to Claude API with a security analyst prompt
- Generating a structured HTML report with plain-English explanations and remediation recommendations

## Tech Stack
- Python
- Claude API (Anthropic)
- OWASP ZAP (DAST scanning)
- Docker (running DVWA for real scan targets)

## Security Practices
- API keys stored in `.env` file, never hardcoded
- `.gitignore` excludes all sensitive files
- AI-generated recommendations reviewed by human analyst before use

## How To Run
1. Clone the repo
2. Install dependencies: `pip install anthropic python-dotenv markdown`
3. Add your Claude API key to a `.env` file: `ANTHROPIC_API_KEY=your-key-here`
4. Add your scan results to `scan_results.json`
5. Run: `python main.py`
6. Open `report.html` in your browser

## Future Improvements
- Direct integration with OWASP ZAP API to eliminate manual JSON export
- OWASP Top 10 mapping for each finding
- Severity-based prioritization and filtering
- Separate modules for scanning, analysis, and reporting