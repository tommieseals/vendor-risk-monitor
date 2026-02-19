import os
import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

class Ecosystem(Enum):
    NPM = "npm"
    PYPI = "pypi"
    CARGO = "cargo"
    GO = "go"

@dataclass
class Dependency:
    name: str
    version: str
    ecosystem: Ecosystem
    source_file: str
    is_dev: bool = False
    risk_score: int = 0
    cves: list = field(default_factory=list)
    license_info: Optional[dict] = None
    maintenance_status: Optional[dict] = None
    risk_factors: list = field(default_factory=list)
    supply_chain_risks: list = field(default_factory=list)
    
    def to_dict(self):
        return {"name": self.name, "version": self.version, "ecosystem": self.ecosystem.value,
                "risk_score": self.risk_score, "cves": self.cves}

@dataclass  
class ScanResult:
    project_path: str
    scan_time: datetime
    dependencies: list
    total_count: int = 0
    high_risk_count: int = 0
    critical_cve_count: int = 0
    abandoned_count: int = 0
    license_issues_count: int = 0
    overall_score: int = 0
    passed: bool = True
    
    def to_dict(self):
        return {"total_count": self.total_count, "high_risk_count": self.high_risk_count,
                "passed": self.passed, "dependencies": [d.to_dict() for d in self.dependencies]}

class DependencyScanner:
    def __init__(self, config_path=None, github_token=None, nvd_api_key=None):
        from .advisories import AdvisoryChecker
        from .maintainer import MaintainerChecker
        from .license import LicenseChecker
        self.config = {"thresholds": {"fail_score": 60, "warn_score": 40}}
        self.advisory_checker = AdvisoryChecker(github_token=github_token)
        self.maintainer_checker = MaintainerChecker(github_token=github_token)
        self.license_checker = LicenseChecker()
    
    def scan(self, path, recursive=True):
        path = Path(path).resolve()
        deps = []
        if path.is_file():
            deps = self._parse_manifest(path)
        else:
            for f in path.rglob("*package.json"):
                if "node_modules" not in str(f): deps.extend(self._parse_manifest(f))
            for f in path.rglob("*requirements*.txt"):
                if "venv" not in str(f): deps.extend(self._parse_manifest(f))
            for f in path.rglob("Cargo.toml"):
                if "target" not in str(f): deps.extend(self._parse_manifest(f))
            for f in path.rglob("go.mod"):
                deps.extend(self._parse_manifest(f))
        for dep in deps: self._analyze(dep)
        fail_th = self.config["thresholds"]["fail_score"]
        return ScanResult(str(path), datetime.utcnow(), deps, len(deps),
            sum(1 for d in deps if d.risk_score >= 40),
            sum(1 for d in deps for c in d.cves if c.get("severity")=="critical"),
            0, 0, sum(d.risk_score for d in deps)//max(len(deps),1),
            all(d.risk_score < fail_th for d in deps))
    
    def _parse_manifest(self, path):
        deps = []
        name = path.name.lower()
        try:
            if name.endswith("package.json"):
                data = json.loads(path.read_text())
                for n, v in data.get("dependencies", {}).items():
                    deps.append(Dependency(n, re.sub(r"^[\^~>=<]+", "", str(v)), Ecosystem.NPM, str(path)))
                for n, v in data.get("devDependencies", {}).items():
                    deps.append(Dependency(n, re.sub(r"^[\^~>=<]+", "", str(v)), Ecosystem.NPM, str(path), True))
            elif "requirements" in name and name.endswith(".txt"):
                for line in path.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("-"):
                        m = re.match(r"^([a-zA-Z0-9_-]+)", line)
                        if m: deps.append(Dependency(m.group(1), "latest", Ecosystem.PYPI, str(path)))
            elif name == "cargo.toml":
                import toml
                data = toml.loads(path.read_text())
                for n, v in data.get("dependencies", {}).items():
                    ver = v if isinstance(v, str) else v.get("version", "latest")
                    deps.append(Dependency(n, ver, Ecosystem.CARGO, str(path)))
            elif name == "go.mod":
                content = path.read_text()
                for m in re.finditer(r"^\s*(\S+)\s+v?([\d.]+)", content, re.MULTILINE):
                    if not m.group(1).startswith("//"): deps.append(Dependency(m.group(1), m.group(2), Ecosystem.GO, str(path)))
        except Exception as e:
            print(f"Warning: Error parsing {path}: {e}")
        return deps
    
    def _analyze(self, dep):
        score = 0
        dep.cves = self.advisory_checker.check(dep.name, dep.version, dep.ecosystem.value)
        for cve in dep.cves:
            sev = cve.get("severity", "medium").lower()
            score += {"critical": 30, "high": 20, "medium": 10}.get(sev, 5)
        dep.maintenance_status = self.maintainer_checker.check(dep.name, dep.ecosystem.value)
        if dep.maintenance_status.get("abandoned"): score += 25
        dep.license_info = self.license_checker.check(dep.name, dep.ecosystem.value)
        if dep.license_info.get("blocked"): score += 40
        dep.risk_score = min(score, 100)

def main():
    import argparse, sys
    from .reporter import RiskReporter, ReportFormat
    parser = argparse.ArgumentParser(description="Vendor Risk Monitor")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--format", choices=["text","json","markdown","sarif"], default="text")
    parser.add_argument("--output", "-o")
    parser.add_argument("--sbom", action="store_true")
    args = parser.parse_args()
    result = DependencyScanner().scan(args.path)
    fmt_map = {"text": ReportFormat.TEXT, "json": ReportFormat.JSON, "markdown": ReportFormat.MARKDOWN, "sarif": ReportFormat.SARIF}
    report = RiskReporter().generate(result, fmt_map[args.format])
    if args.output:
        Path(args.output).write_text(report)
    else:
        print(report)
    sys.exit(0 if result.passed else 1)

if __name__ == "__main__": main()