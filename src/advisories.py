"""Security Advisory Checker."""
import os
import requests

class AdvisoryChecker:
    def __init__(self, github_token=None, nvd_api_key=None):
        self.session = requests.Session()
    
    def check(self, package, version, ecosystem):
        try:
            eco_map = {"npm": "npm", "pypi": "PyPI", "cargo": "crates.io", "go": "Go"}
            resp = self.session.post("https://api.osv.dev/v1/query",
                json={"package": {"name": package, "ecosystem": eco_map.get(ecosystem, ecosystem)}, "version": version}, timeout=10)
            if resp.status_code == 200:
                return [{"id": v.get("aliases", [v["id"]])[0] if v.get("aliases") else v["id"],
                         "severity": "high", "title": v.get("summary", "")[:100],
                         "fixed_versions": []} for v in resp.json().get("vulns", [])]
        except: pass
        return []