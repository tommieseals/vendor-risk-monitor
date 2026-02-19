"""License Checker."""
import requests

class LicenseChecker:
    ALLOWED = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"}
    BLOCKED = {"UNLICENSED", "UNKNOWN"}
    REVIEW = {"GPL-2.0", "GPL-3.0", "AGPL-3.0"}
    
    def __init__(self, config=None):
        pass
    
    def check(self, package, ecosystem):
        spdx = self._fetch(package, ecosystem)
        return {"spdx": spdx, "allowed": spdx in self.ALLOWED, "blocked": spdx in self.BLOCKED,
                "review_required": spdx in self.REVIEW, "unknown": spdx == "UNKNOWN"}
    
    def _fetch(self, package, ecosystem):
        try:
            if ecosystem == "npm":
                r = requests.get(f"https://registry.npmjs.org/{package}", timeout=10)
                if r.status_code == 200: return r.json().get("license", "UNKNOWN")
            elif ecosystem == "pypi":
                r = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=10)
                if r.status_code == 200: return r.json().get("info", {}).get("license") or "UNKNOWN"
        except: pass
        return "UNKNOWN"