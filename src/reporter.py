"""Risk Reporter."""
import json
from enum import Enum

class ReportFormat(Enum):
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"
    SARIF = "sarif"

class RiskReporter:
    def generate(self, result, fmt):
        if fmt == ReportFormat.JSON: return json.dumps(result.to_dict(), indent=2, default=str)
        if fmt == ReportFormat.MARKDOWN: return self._markdown(result)
        if fmt == ReportFormat.SARIF: return self._sarif(result)
        return self._text(result)
    
    def _text(self, r):
        lines = ["\n" + "="*50, " Vendor Risk Report", "="*50]
        lines.append(f"Total: {r.total_count} | High Risk: {r.high_risk_count} | CVEs: {r.critical_cve_count}")
        lines.append(f"Status: {'PASSED' if r.passed else 'FAILED'}")
        lines.append("-"*50)
        for d in sorted(r.dependencies, key=lambda x: x.risk_score, reverse=True)[:5]:
            if d.risk_score >= 40:
                lines.append(f"\n[{d.risk_score}] {d.name}@{d.version}")
                for c in d.cves[:2]: lines.append(f"  - {c['id']}: {c.get('title','')[:40]}")
        return "\n".join(lines)
    
    def _markdown(self, r):
        return f"# Vendor Risk Report\n\n| Deps | Risk | Status |\n|---|---|---|\n| {r.total_count} | {r.high_risk_count} | {'Pass' if r.passed else 'Fail'} |"
    
    def _sarif(self, r):
        return json.dumps({"version": "2.1.0", "runs": [{"tool": {"driver": {"name": "vendor-risk-monitor"}}, "results": []}]})
    
    def generate_sbom(self, r, fmt="cyclonedx"):
        return json.dumps({"bomFormat": "CycloneDX", "components": [{"name": d.name, "version": d.version} for d in r.dependencies]})
    
    def send_slack_alert(self, r, deps): pass