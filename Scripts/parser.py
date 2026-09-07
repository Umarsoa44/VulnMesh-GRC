import argparse
import csv
import json
from pathlib import Path

def parse_vulnerabilities(data_file: Path, policy_file: Path, report_file: Path):
    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        return

    # Load policy thresholds
    max_crit = 0
    max_high = 2
    if policy_file.exists():
        with open(policy_file, mode="r", encoding="utf-8") as p_file:
            policy_data = json.load(p_file)
            max_crit = policy_data.get("max_allowed_critical", 0)
            max_high = policy_data.get("max_allowed_high", 2)

    critical_count = 0
    high_count = 0
    total_vulns = 0

    with open(data_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_vulns += 1
            severity = row.get("Severity", "").strip().lower()
            status = row.get("Status", "").strip().lower()
            
            if status == "open":
                if severity == "critical":
                    critical_count += 1
                elif severity == "high":
                    high_count += 1

    # Evaluate compliance policy
    compliant = (critical_count <= max_crit) and (high_count <= max_high)
    compliance_status = "PASSED - All vulnerabilities within acceptable threshold." if compliant else "FAILED - Policy thresholds exceeded!"

    report_content = (
        "=== VulnMesh-GRC Automated Risk & Policy Summary ===\n"
        f"Total Vulnerabilities Processed: {total_vulns}\n"
        f"Open Critical Risk Findings: {critical_count} (Max Allowed: {max_crit})\n"
        f"Open High Risk Findings: {high_count} (Max Allowed: {max_high})\n"
        f"Compliance Evaluation: {compliance_status}\n"
        "Status: Pipeline executed successfully via CLI.\n"
    )

    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, mode="w", encoding="utf-8") as r_file:
        r_file.write(report_content)

    print(f"Report generated successfully at: {report_file}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    
    parser = argparse.ArgumentParser(description="VulnMesh-GRC Air-Gapped Risk & Compliance Engine")
    parser.add_argument("--data", type=Path, default=base_dir / "Data" / "vulnerabilities.csv", help="Path to vulnerabilities CSV")
    parser.add_argument("--policy", type=Path, default=base_dir / "Policies" / "thresholds.json", help="Path to policy thresholds JSON")
    parser.add_argument("--output", type=Path, default=base_dir / "Report" / "risk_summary.txt", help="Path to output report")
    
    args = parser.parse_args()
    parse_vulnerabilities(args.data, args.policy, args.output)