"""Maintainer Activity Checker."""
import requests
from datetime import datetime

class MaintainerChecker:
    def __init__(self, github_token=None):
        pass
    
    def check(self, package, ecosystem):
        result = {"abandoned": False, "low_activity": False, "single_maintainer": False, "days_since_update": 0}
        try:
            if ecosystem == "npm":
                resp = requests.get(f"https://registry.npmjs.org/{package}", timeout=10)
                if resp.status_code == 200:
                    t = resp.json().get("time", {}).get("modified")
                    if t:
                        d = datetime.fromisoformat(t.replace("Z", "+00:00"))
                        days = (datetime.now(d.tzinfo) - d).days
                        result["days_since_update"] = days
                        result["abandoned"] = days > 730
                        result["low_activity"] = days > 365
        except: pass
        return result