import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://api.gitbook.com/v1"
ORG_ID = "M7Hsux2wvrs5Etd272Ma"
SITE_ID = "site_AXdbD"
SECTION_ID = "sitesc_pDfbk"
REPO = "exotec-demo-site-20260707"
REPO_OWNER = "gitbook-demo-sites"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO}.git"
STATE_PATH = ROOT / "gitbook-governance-variants.json"

VARIANTS = [
    {
        "key": "OPERATING_CONTROLS",
        "folder": "governance-operating-controls",
        "title": "Operating controls",
        "space_title": "Documentation Governance: Operating Controls",
        "emoji": "2705",
    },
    {
        "key": "PARTNER_CUSTOMER_ACCESS",
        "folder": "governance-partner-customer-access",
        "title": "Partner and customer access",
        "space_title": "Documentation Governance: Partner and Customer Access",
        "emoji": "1f510",
    },
    {
        "key": "DEVELOPER_API_GOVERNANCE",
        "folder": "governance-developer-api-governance",
        "title": "Developer API governance",
        "space_title": "Documentation Governance: Developer API Governance",
        "emoji": "1f9e9",
    },
]


def api(method: str, path: str, body=None, expected=(200, 201, 204)):
    token = os.environ["GITBOOK_TOKEN"]
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            text = resp.read().decode()
            payload = json.loads(text) if text else None
            if resp.status not in expected:
                raise RuntimeError(f"{method} {path} returned {resp.status}: {text}")
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"{method} {path} returned {exc.code}: {detail}") from exc


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"org": ORG_ID, "site": SITE_ID, "section": SECTION_ID, "variants": {}}


def save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def find_existing_site_space(space_id: str):
    _, structure = api("GET", f"/orgs/{ORG_ID}/sites/{SITE_ID}/structure")
    for section in structure.get("structure", []):
        if section.get("id") != SECTION_ID:
            continue
        for site_space in section.get("siteSpaces", []):
            if (site_space.get("space") or {}).get("id") == space_id:
                return site_space
    return None


def main():
    state = load_state()
    imports = {}

    for variant in VARIANTS:
        entry = state["variants"].setdefault(variant["key"], {})
        if "space" not in entry:
            _, space = api(
                "POST",
                f"/orgs/{ORG_ID}/spaces",
                {
                    "title": variant["space_title"],
                    "emoji": variant["emoji"],
                    "empty": True,
                    "editMode": "live",
                },
            )
            entry["space"] = space["id"]
            save_state(state)

        existing_site_space = find_existing_site_space(entry["space"])
        if existing_site_space:
            entry["site_space"] = existing_site_space["id"]
        else:
            _, site_space = api(
                "POST",
                f"/orgs/{ORG_ID}/sites/{SITE_ID}/site-spaces",
                {"spaceId": entry["space"], "sectionId": SECTION_ID},
            )
            entry["site_space"] = site_space["id"]
        entry["title"] = variant["title"]
        entry["folder"] = variant["folder"]

        status, _ = api(
            "POST",
            f"/spaces/{entry['space']}/git/import",
            {
                "url": REPO_URL,
                "ref": "refs/heads/main",
                "repoProjectDirectory": variant["folder"],
                "repoTreeURL": f"https://github.com/{REPO_OWNER}/{REPO}/tree/main",
                "repoCommitURL": f"https://github.com/{REPO_OWNER}/{REPO}/commit",
                "force": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            expected=(204,),
        )
        imports[variant["key"]] = {
            "status": status,
            "space": entry["space"],
            "site_space": entry["site_space"],
            "folder": variant["folder"],
        }
        save_state(state)

    state["last_imports"] = imports
    save_state(state)
    print(json.dumps(state, indent=2))


if __name__ == "__main__":
    main()
