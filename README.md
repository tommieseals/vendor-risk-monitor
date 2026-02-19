# 🛡️ Vendor Risk Monitor

[![CI](https://github.com/tommieseals/vendor-risk-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/tommieseals/vendor-risk-monitor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Enterprise-grade dependency risk monitoring for modern software supply chains.**

Monitor your dependencies for:
- 🔒 **Security Advisories** (CVEs from NVD, GitHub, OSV)
- 👻 **Abandoned Packages** (maintainer activity analysis)
- 📜 **License Changes** (compatibility & compliance)
- 💥 **Breaking Changes** (semver violations, deprecations)
- ⛓️ **Supply Chain Risks** (typosquatting, dependency confusion)

## 🚀 Quick Start

\\ash
# Clone and install
git clone https://github.com/tommieseals/vendor-risk-monitor.git
cd vendor-risk-monitor
pip install -r requirements.txt

# Scan a project
python -m src.scanner /path/to/project

# Generate SBOM
python -m src.scanner . --sbom --output sbom.json

# Output as SARIF for GitHub Security
python -m src.scanner . --format sarif --output results.sarif
\\

## 📊 Risk Scoring (0-100)

| Score | Level | Action |
|-------|-------|--------|
| 0-20 | 🟢 Low | Monitor |
| 21-40 | 🟡 Medium | Review |
| 41-60 | 🟠 High | Plan remediation |
| 61-80 | 🔴 Critical | Immediate action |
| 81-100 | ⛔ Severe | Block deployment |

## 📦 Supported Ecosystems

- **npm/yarn** - package.json, package-lock.json
- **pip** - requirements.txt, pyproject.toml, Pipfile
- **Cargo** - Cargo.toml, Cargo.lock
- **Go** - go.mod, go.sum
- **Maven** - pom.xml
- **NuGet** - *.csproj

## 🔌 GitHub Actions Integration

\\yaml
- name: Vendor Risk Scan
  run: |
    pip install git+https://github.com/tommieseals/vendor-risk-monitor.git
    python -m src.scanner . --format sarif --output vendor-risk.sarif
    
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: vendor-risk.sarif
\\

## 📜 License

MIT License - See [LICENSE](LICENSE)
