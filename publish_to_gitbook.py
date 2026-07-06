import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://api.gitbook.com/v1"
REPO = "exotec-demo-site-20260707"
REPO_OWNER = "gitbook-demo-sites"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO}.git"
PETSTORE_URL = "https://gitbookio.github.io/onboarding-template-images/gitbook-petstore.yaml"
OPENAPI_SLUG = "gitbook-petstore-demo"

SPACES = [
    {
        "key": "HOME",
        "sentinel": "XSPACE_HOME",
        "folder": "home",
        "title": "Home",
        "emoji": "1f3e0",
        "icon": "house",
        "path": "home",
        "description": "Demo framing, discovery notes, and review checklist.",
    },
    {
        "key": "GOVERNANCE",
        "sentinel": "XSPACE_GOVERNANCE",
        "folder": "governance",
        "title": "Documentation Governance",
        "emoji": "1f6e1",
        "icon": "shield-halved",
        "path": "documentation-governance",
        "description": "Version ownership, access levels, decision rounds, owners, and procurement context.",
    },
    {
        "key": "API",
        "sentinel": "XSPACE_API",
        "folder": "developer-api",
        "title": "Developer & API Reference",
        "emoji": "1f4bb",
        "icon": "code",
        "path": "developer-api-reference",
        "description": "Developer account onboarding and OpenAPI-generated reference pages.",
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


def git_commit_push(message: str):
    subprocess.run(["git", "add", "."], cwd=ROOT, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", message], cwd=ROOT, check=True)
    subprocess.run(["git", "push"], cwd=ROOT, check=True)


def replace_sentinels(space_ids: dict[str, str]):
    replacements = {item["sentinel"]: space_ids[item["key"]] for item in SPACES}
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")


def ensure_openapi_spec(org_id: str) -> dict:
    try:
        _, spec = api(
            "POST",
            f"/orgs/{org_id}/openapi",
            {"slug": OPENAPI_SLUG, "source": {"url": PETSTORE_URL}},
        )
        return {"created": True, "spec": spec}
    except RuntimeError as exc:
        if "400" not in str(exc) and "409" not in str(exc):
            raise
        _, specs = api("GET", f"/orgs/{org_id}/openapi")
        for item in (specs.get("items") or specs.get("results") or specs if isinstance(specs, list) else []):
            if item.get("slug") == OPENAPI_SLUG:
                return {"created": False, "spec": item, "note": "slug already existed"}
        return {"created": False, "error": str(exc)}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: GITBOOK_TOKEN=... python3 publish_to_gitbook.py <gitbook_org_id>")

    org_id = sys.argv[1]
    openapi_result = ensure_openapi_spec(org_id)
    created_path = ROOT / "gitbook-created.json"
    if created_path.exists():
        created = json.loads(created_path.read_text(encoding="utf-8"))
        site_id = created["site"]
    else:
        _, site = api(
            "POST",
            f"/orgs/{org_id}/sites",
            {"type": "ultimate", "title": "Exotec Knowledge & Developer Portal", "visibility": "share-link"},
        )
        site_id = site["id"]
        api(
            "PATCH",
            f"/orgs/{org_id}/sites/{site_id}",
            {
                "title": "Exotec Knowledge & Developer Portal",
                "visibility": "share-link",
                "basename": "exotec-knowledge-developer-portal",
            },
        )

        created = {"org": org_id, "site": site_id, "spaces": {}, "sections": {}, "site_spaces": {}, "site_object": site}
        for item in SPACES:
            _, space = api(
                "POST",
                f"/orgs/{org_id}/spaces",
                {"title": item["title"], "emoji": item["emoji"], "empty": True, "editMode": "live"},
            )
            space_id = space["id"]
            created["spaces"][item["key"]] = space_id
            _, section = api(
                "POST",
                f"/orgs/{org_id}/sites/{site_id}/sections",
                {"spaceId": space_id, "title": item["title"], "icon": item["icon"], "draft": False},
            )
            section_id = section["id"]
            site_space_id = section["siteSpaces"][0]["id"]
            created["sections"][item["key"]] = section_id
            created["site_spaces"][item["key"]] = site_space_id
            api(
                "PATCH",
                f"/orgs/{org_id}/sites/{site_id}/sections/{section_id}",
                {
                    "path": item["path"],
                    "description": item["description"],
                    "draft": False,
                    "defaultSiteSpace": site_space_id,
                },
            )

        api(
            "PATCH",
            f"/orgs/{org_id}/sites/{site_id}",
            {"defaultSiteSection": created["sections"]["HOME"], "defaultSiteSpace": created["site_spaces"]["HOME"]},
        )

        replace_sentinels(created["spaces"])
        created["openapi"] = openapi_result
        created_path.write_text(json.dumps(created, indent=2) + "\n", encoding="utf-8")
        git_commit_push("Resolve Exotec GitBook space links")

    imports = {}
    for item in SPACES:
        status, _ = api(
            "POST",
            f"/spaces/{created['spaces'][item['key']]}/git/import",
            {
                "url": REPO_URL,
                "ref": "refs/heads/main",
                "repoProjectDirectory": item["folder"],
                "repoTreeURL": f"https://github.com/{REPO_OWNER}/{REPO}/tree/main",
                "repoCommitURL": f"https://github.com/{REPO_OWNER}/{REPO}/commit",
                "force": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            expected=(204,),
        )
        imports[item["key"]] = {"status": status, "space": created["spaces"][item["key"]], "folder": item["folder"]}
    (ROOT / "gitbook-import-results.json").write_text(json.dumps(imports, indent=2) + "\n", encoding="utf-8")

    logo = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/exotec-wordmark.svg"
    cover = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/exotec-demo-cover.svg"
    customization = {
        "title": "Exotec Knowledge & Developer Portal",
        "localizedTitle": {},
        "internationalization": {"locale": "en"},
        "styling": {
            "theme": "clean",
            "primaryColor": {"light": "#28AFB9", "dark": "#72DCE3"},
            "infoColor": {"light": "#28AFB9", "dark": "#72DCE3"},
            "successColor": {"light": "#28AFB9", "dark": "#72DCE3"},
            "warningColor": {"light": "#FF6900", "dark": "#FCB900"},
            "dangerColor": {"light": "#CF2E2E", "dark": "#F87171"},
            "tint": {"color": {"light": "#F6F6F6", "dark": "#000000"}},
            "corners": "straight",
            "depth": "flat",
            "links": "accent",
            "font": "Inter",
            "monospaceFont": "IBMPlexMono",
            "icons": "regular",
            "background": "plain",
            "sidebar": {"background": "filled", "list": "line"},
            "codeTheme": {
                "default": {"light": "default-light", "dark": "default-dark"},
                "openapi": {"light": "default-light", "dark": "default-dark"},
            },
            "search": "prominent",
        },
        "favicon": {"icon": {"light": "https://www.exotec.com/favicon-32x32.png", "dark": "https://www.exotec.com/favicon-32x32.png"}},
        "header": {
            "preset": "default",
            "logo": {"light": logo, "dark": logo},
            "links": [
                {"title": "Governance", "to": {"kind": "space", "space": created["spaces"]["GOVERNANCE"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Developer & API", "to": {"kind": "space", "space": created["spaces"]["API"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Exotec", "to": {"kind": "url", "url": "https://www.exotec.com/"}, "style": "button-secondary", "links": [], "localizedTitle": {}},
            ],
        },
        "footer": {
            "logo": {"light": logo, "dark": logo},
            "groups": [
                {
                    "title": "Demo sections",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Home", "to": {"kind": "space", "space": created["spaces"]["HOME"]}, "localizedTitle": {}},
                        {"title": "Documentation Governance", "to": {"kind": "space", "space": created["spaces"]["GOVERNANCE"]}, "localizedTitle": {}},
                        {"title": "Developer & API Reference", "to": {"kind": "space", "space": created["spaces"]["API"]}, "localizedTitle": {}},
                    ],
                },
                {
                    "title": "Sources",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Source repo", "to": {"kind": "url", "url": f"https://github.com/{REPO_OWNER}/{REPO}"}, "localizedTitle": {}},
                        {"title": "Exotec website", "to": {"kind": "url", "url": "https://www.exotec.com/"}, "localizedTitle": {}},
                        {"title": "Petstore OpenAPI spec", "to": {"kind": "url", "url": PETSTORE_URL}, "localizedTitle": {}},
                    ],
                },
            ],
            "copyright": "Exotec Knowledge & Developer Portal - first-draft GitBook demo.",
        },
        "themes": {"default": "light", "toggeable": True},
        "pdf": {"enabled": True},
        "feedback": {"enabled": True},
        "ai": {
            "mode": "assistant",
            "suggestions": [
                "How should Exotec manage versioned docs?",
                "What are the access levels in this demo?",
                "How does developer account setup work?",
                "Where is the generated API reference?",
            ],
        },
        "advancedCustomization": {"enabled": True},
        "trademark": {"enabled": True},
        "externalLinks": {"target": "self"},
        "pagination": {"enabled": True},
        "pageActions": {"externalAI": True, "markdown": True, "mcp": True, "items": ["assistant", "markdown", "external-ai", "mcp", "pdf"]},
        "git": {"showEditLink": False},
        "privacyPolicy": {"url": "https://www.exotec.com/privacy-policy/"},
        "socialPreview": {"url": cover},
        "socialAccounts": [
            {"platform": "linkedin", "handle": "company/exotec", "display": {"footer": True, "header": False}},
        ],
        "insights": {"trackingCookie": True},
    }
    _, customized = api("PUT", f"/orgs/{org_id}/sites/{site_id}/customization", customization)
    (ROOT / "gitbook-customization-result.json").write_text(json.dumps(customized, indent=2) + "\n", encoding="utf-8")

    publish_status, publish = api("POST", f"/orgs/{org_id}/sites/{site_id}/publish")
    share_status, share = api("POST", f"/orgs/{org_id}/sites/{site_id}/share-links", {"name": "Exotec demo review"})
    final = {
        "publish_status": publish_status,
        "publish": publish,
        "share_status": share_status,
        "share": share,
        "published_url": share["urls"]["published"],
        "app_url": publish["urls"]["app"],
        "preview_url": publish["urls"]["preview"],
        "repo": f"https://github.com/{REPO_OWNER}/{REPO}",
        "openapi": openapi_result,
    }
    (ROOT / "gitbook-publish-share.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    git_commit_push("Add Exotec GitBook publish artifacts")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
