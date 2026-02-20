# 🛡️ Vendor Risk Monitor

[![CI](https://github.com/tommieseals/vendor-risk-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/tommieseals/vendor-risk-monitor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![SBOM](https://img.shields.io/badge/SBOM-CycloneDX-blue)](https://cyclonedx.org/)

**Enterprise-grade dependency risk monitoring for modern software supply chains.**

Your dependencies are your attack surface. Vendor Risk Monitor continuously scans for security vulnerabilities, abandoned packages, license violations, and supply chain threats—before they become incidents.

## 🎯 What It Catches

| Threat | Detection Method | Example |
|--------|------------------|---------|
| 🔒 **CVEs** | NVD, GitHub Advisory, OSV databases | `lodash < 4.17.21` prototype pollution |
| 👻 **Abandoned Packages** | Maintainer activity analysis | No commits in 2+ years, archived repos |
| 📜 **License Risks** | SPDX compliance checking | GPL in MIT project, license changes |
| 💥 **Breaking Changes** | Semver violation detection | Major bump in minor version |
| ⛓️ **Supply Chain Attacks** | Typosquatting, confusion detection | `lod-ash` vs `lodash` |
| 🔄 **Deprecated APIs** | Deprecation notice parsing | `request` package sunset |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    VENDOR RISK MONITOR                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │   Package    │   │   Advisory   │   │   License    │        │
│  │   Parser     │   │   Fetcher    │   │   Analyzer   │        │
│  │              │   │              │   │              │        │
│  │ • npm        │   │ • NVD API    │   │ • SPDX       │        │
│  │ • pip        │   │ • GitHub     │   │ • Compliance │        │
│  │ • cargo      │   │ • OSV        │   │ • Conflicts  │        │
│  │ • go mod     │   │ • Snyk       │   │              │        │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘        │
│         │                  │                  │                 │
│         └────────────┬─────┴─────┬────────────┘                 │
│                      │           │                              │
│              ┌───────▼───────────▼───────┐                      │
│              │      Risk Aggregator      │                      │
│              │                           │                      │
│              │  • Severity weighting     │                      │
│              │  • Exploitability score   │                      │
│              │  • Business impact        │                      │
│              └───────────┬───────────────┘                      │
│                          │                                      │
│  ┌───────────────────────▼───────────────────────────────┐     │
│  │                    OUTPUT FORMATS                      │     │
│  │   • JSON Report    • SARIF (GitHub)    • SBOM         │     │
│  │   • HTML Dashboard • Slack/Teams       • CSV Export   │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Installation

```bash
# Clone and install
git clone https://github.com/tommieseals/vendor-risk-monitor.git
cd vendor-risk-monitor
pip install -r requirements.txt

# Or install directly
pip install git+https://github.com/tommieseals/vendor-risk-monitor.git
```

### Basic Usage

```bash
# Scan current project
python -m src.scanner .

# Scan with detailed output
python -m src.scanner /path/to/project --verbose

# Generate SBOM (Software Bill of Materials)
python -m src.scanner . --sbom --output sbom.json

# Output as SARIF for GitHub Security tab
python -m src.scanner . --format sarif --output results.sarif

# Export as CSV for compliance reporting
python -m src.scanner . --format csv --output risks.csv
```

### Example Output

```
Vendor Risk Report - myproject
==============================

CRITICAL (2)
  ┌─────────────────────────────────────────────────────────────┐
  │ lodash@4.17.15                                              │
  │ CVE-2021-23337 - Command Injection (CVSS 7.2)               │
  │ Fix: Upgrade to 4.17.21                                     │
  │ Risk Score: 85/100                                          │
  └─────────────────────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────────────────────┐
  │ node-fetch@2.6.0                                            │
  │ CVE-2022-0235 - Information Disclosure (CVSS 6.1)           │
  │ Fix: Upgrade to 2.6.7                                       │
  │ Risk Score: 72/100                                          │
  └─────────────────────────────────────────────────────────────┘

HIGH (1)
  • event-stream@3.3.4 - ABANDONED (no activity since 2018)
    Risk Score: 65/100 - Consider alternatives: highland, rxjs

MEDIUM (3)
  • moment@2.29.0 - DEPRECATED (maintenance mode)
  • request@2.88.2 - DEPRECATED (sunset April 2020)
  • colors@1.4.0 - License changed to SSPL (was MIT)

Summary: 2 critical, 1 high, 3 medium, 12 low
Overall Risk Score: 68/100 (HIGH)
Recommendation: Address critical vulnerabilities before deployment
```

## 📊 Risk Scoring Methodology

Each dependency is scored 0-100 based on weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| CVE Severity | 40% | CVSS score of known vulnerabilities |
| Exploitability | 20% | Public exploits, attack complexity |
| Maintainer Activity | 15% | Commit frequency, issue response time |
| License Risk | 10% | Compatibility, compliance requirements |
| Popularity | 10% | Downloads, dependents (abandoned = higher risk) |
| Age | 5% | Time since last release |

### Risk Levels

| Score | Level | Action | SLA |
|-------|-------|--------|-----|
| 0-20 | 🟢 Low | Monitor | 90 days |
| 21-40 | 🟡 Medium | Review | 30 days |
| 41-60 | 🟠 High | Plan remediation | 14 days |
| 61-80 | 🔴 Critical | Immediate action | 48 hours |
| 81-100 | ⛔ Severe | Block deployment | Immediate |

## 📦 Supported Ecosystems

| Ecosystem | Files Parsed | Advisory Sources |
|-----------|--------------|------------------|
| **npm/yarn** | package.json, package-lock.json, yarn.lock | npm audit, GitHub, Snyk |
| **pip** | requirements.txt, pyproject.toml, Pipfile, Pipfile.lock | PyPI, Safety DB, OSV |
| **Cargo** | Cargo.toml, Cargo.lock | RustSec, GitHub |
| **Go** | go.mod, go.sum | Go vulnerability DB |
| **Maven** | pom.xml | NVD, Sonatype |
| **NuGet** | *.csproj, packages.config | NuGet Gallery, GitHub |
| **Ruby** | Gemfile, Gemfile.lock | Ruby Advisory DB |

## 🔌 CI/CD Integration

### GitHub Actions

```yaml
name: Vendor Risk Scan

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install scanner
        run: pip install git+https://github.com/tommieseals/vendor-risk-monitor.git
      
      - name: Run scan
        run: python -m src.scanner . --format sarif --output vendor-risk.sarif
      
      - name: Upload to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: vendor-risk.sarif
      
      - name: Fail on critical
        run: |
          python -m src.scanner . --fail-on critical
```

### GitLab CI

```yaml
vendor-risk:
  image: python:3.11
  script:
    - pip install git+https://github.com/tommieseals/vendor-risk-monitor.git
    - python -m src.scanner . --format json --output gl-dependency-scanning-report.json
  artifacts:
    reports:
      dependency_scanning: gl-dependency-scanning-report.json
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/tommieseals/vendor-risk-monitor
    rev: v1.0.0
    hooks:
      - id: vendor-risk-scan
        args: ['--fail-on', 'high']
```

## 🔧 Configuration

Create `vendor-risk.yaml` in your project root:

```yaml
# Severity thresholds
fail_on: critical  # critical, high, medium, low
warn_on: medium

# Ignore specific vulnerabilities
ignore:
  - CVE-2021-12345  # False positive, not exploitable in our context
  - GHSA-xxxx-yyyy  # Mitigated by WAF

# Ignore specific packages
ignore_packages:
  - dev-only-tool  # Not in production

# License allowlist
allowed_licenses:
  - MIT
  - Apache-2.0
  - BSD-3-Clause
  - ISC

# Alert channels
alerts:
  slack:
    webhook: ${SLACK_WEBHOOK}
    channel: "#security"
    on: [critical, high]
  email:
    to: security@company.com
    on: [critical]
```

## 📈 Comparison with Alternatives

| Feature | Vendor Risk Monitor | Snyk | Dependabot | npm audit |
|---------|---------------------|------|------------|-----------|
| Multi-ecosystem | ✅ 7+ | ✅ | ✅ | ❌ npm only |
| Abandoned detection | ✅ | ❌ | ❌ | ❌ |
| License scanning | ✅ | ✅ | ❌ | ❌ |
| SBOM generation | ✅ | ✅ | ❌ | ❌ |
| Self-hosted | ✅ | ❌ | ❌ | ✅ |
| Cost | Free | $$ | Free | Free |
| Supply chain risks | ✅ | ✅ | ❌ | ❌ |

## 🧪 API Usage

```python
from vendor_risk import Scanner, RiskLevel

# Initialize scanner
scanner = Scanner(
    advisory_sources=["nvd", "github", "osv"],
    cache_ttl=3600  # Cache advisories for 1 hour
)

# Scan a project
results = scanner.scan("/path/to/project")

# Check risk level
if results.max_risk >= RiskLevel.CRITICAL:
    print("Critical vulnerabilities found!")
    for vuln in results.critical:
        print(f"  {vuln.package}: {vuln.cve_id}")

# Generate SBOM
sbom = scanner.generate_sbom("/path/to/project", format="cyclonedx")
sbom.save("sbom.json")

# Custom risk policy
policy = RiskPolicy(
    fail_on=RiskLevel.HIGH,
    ignore_cves=["CVE-2021-12345"],
    license_allowlist=["MIT", "Apache-2.0"]
)
results = scanner.scan("/path/to/project", policy=policy)
```

## 📜 License

MIT License - See [LICENSE](LICENSE)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas we'd love help with:**
- Additional ecosystem support (Composer, Hex, etc.)
- Advisory source integrations
- Dashboard improvements
- Documentation translations
