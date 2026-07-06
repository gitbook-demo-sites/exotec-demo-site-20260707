from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
REPO = "exotec-demo-site-20260707"
RAW = f"https://raw.githubusercontent.com/gitbook-demo-sites/{REPO}/main"


def write(path: str, content: str) -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def yaml(space: str) -> None:
    write(
        f"{space}/.gitbook.yaml",
        """
        root: ./
        structure:
          readme: README.md
          summary: SUMMARY.md
        """,
    )


def vars_file(space: str) -> None:
    write(
        f"{space}/.gitbook/vars.yaml",
        """
        company_name: Exotec
        demo_name: Exotec Knowledge & Developer Portal
        review_stage: First-draft demo
        discovery_source: GitBook Intro call on 2026-07-06
        petstore_spec: gitbook-petstore-demo
        """,
    )


def summary(space: str, lines: list[str]) -> None:
    write(f"{space}/SUMMARY.md", "# Table of contents\n\n" + "\n".join(lines))


def card(icon: str, title: str, desc: str, href: str) -> str:
    return (
        f'<tr><td><i class="fa-{icon}"></i></td><td><strong>{title}</strong></td>'
        f'<td>{desc}</td><td><a href="{href}">{title}</a></td></tr>'
    )


for slug in ["home", "governance", "developer-api"]:
    yaml(slug)
    vars_file(slug)

write(
    "README.md",
    """
    # Exotec demo site

    First-draft GitBook demo content for Exotec. Each top-level folder is imported into a GitBook space.
    """,
)

write(".gitignore", ".DS_Store\nThumbs.db\n*.swp\n*.swo\n.idea/\n.vscode/\n__pycache__/\n")

write(
    "assets/exotec-demo-cover.svg",
    """
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="520" viewBox="0 0 1600 520" role="img" aria-label="Exotec Knowledge and Developer Portal">
      <rect width="1600" height="520" fill="#F6F6F6"/>
      <rect x="0" y="0" width="1600" height="18" fill="#000000"/>
      <circle cx="1252" cy="180" r="210" fill="#28AFB9" opacity=".14"/>
      <circle cx="1370" cy="336" r="178" fill="#000000" opacity=".06"/>
      <rect x="1030" y="116" width="370" height="74" rx="4" fill="#FFFFFF" stroke="#DCDCDC"/>
      <rect x="1064" y="146" width="104" height="12" rx="6" fill="#000000"/>
      <rect x="1190" y="146" width="154" height="12" rx="6" fill="#28AFB9"/>
      <rect x="1030" y="214" width="452" height="74" rx="4" fill="#FFFFFF" stroke="#DCDCDC"/>
      <rect x="1064" y="244" width="86" height="12" rx="6" fill="#000000"/>
      <rect x="1172" y="244" width="244" height="12" rx="6" fill="#28AFB9"/>
      <rect x="1030" y="312" width="318" height="74" rx="4" fill="#FFFFFF" stroke="#DCDCDC"/>
      <rect x="1064" y="342" width="72" height="12" rx="6" fill="#000000"/>
      <rect x="1158" y="342" width="126" height="12" rx="6" fill="#28AFB9"/>
      <text x="96" y="188" font-family="Arial, Helvetica, sans-serif" font-size="92" font-weight="700" fill="#000000" letter-spacing="0">Exotec</text>
      <text x="102" y="254" font-family="Arial, Helvetica, sans-serif" font-size="31" fill="#262626">Knowledge governance, versioned docs, and API references</text>
      <rect x="102" y="326" width="292" height="44" rx="4" fill="#28AFB9"/>
      <text x="128" y="355" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#000000">Warehouse operations portal</text>
    </svg>
    """,
)

write(
    "assets/exotec-wordmark.svg",
    """
    <svg xmlns="http://www.w3.org/2000/svg" width="460" height="120" viewBox="0 0 460 120" role="img" aria-label="Exotec">
      <rect width="460" height="120" fill="#FFFFFF"/>
      <text x="24" y="76" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="700" fill="#000000">Exotec</text>
      <rect x="228" y="62" width="128" height="8" fill="#28AFB9"/>
    </svg>
    """,
)

write(
    "home/README.md",
    f"""
    ---
    description: "A branded first-draft portal for Exotec documentation governance, developer onboarding, and API reference."
    icon: house
    cover: "{RAW}/assets/exotec-demo-cover.svg"
    coverY: 0
    layout:
      width: wide
      cover:
        visible: true
        size: hero
      title:
        visible: true
      description:
        visible: true
      tableOfContents:
        visible: false
      outline:
        visible: false
      pagination:
        visible: true
    ---

    # Exotec Knowledge & Developer Portal

    A demo documentation hub for teams operating at the intersection of warehouse automation, software, partner implementation, and developer onboarding.

    Exotec's public positioning centers on flexible, reliable warehouse automation with faster time to value. This draft translates that message into a documentation model: clear version ownership, decision rounds, access tiers, developer account setup, procurement context, and an API section generated from OpenAPI.

    {{% hint style="info" %}}
    Discovery basis: the Fireflies summary called out version documentation, document responsibility, decision rounds, multi-level access, developer account procedures, and procurement/contractual alignment. The raw transcript was sparse, so the content is intentionally framed as a first draft for review.
    {{% endhint %}}

    ## Start here

    <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    {card("route", "Demo map", "How this site maps Exotec's website positioning and discovery-call themes into GitBook.", "demo-map.md")}
    {card("shield-halved", "Documentation governance", "Ownership, versioning, access levels, decision rounds, and review workflows.", "https://app.gitbook.com/s/XSPACE_GOVERNANCE/")}
    {card("code", "Developer & API Reference", "Developer account onboarding plus a generated OpenAPI reference using the GitBook Petstore spec.", "https://app.gitbook.com/s/XSPACE_API/")}
    </tbody></table>

    ## What this should show in the demo

    {{% columns %}}
    {{% column %}}
    **For Exotec operators**

    GitBook can give warehouse software, implementation, and support teams a governed source of truth: owners, version trails, access controls, review dates, and change history.
    {{% endcolumn %}}
    {{% column %}}
    **For Exotec developers**

    API documentation can be generated from OpenAPI, paired with onboarding pages, and kept close to account, plan, and procurement procedures.
    {{% endcolumn %}}
    {{% endcolumns %}}

    ## Suggested walkthrough

    1. Open the governance space and show the version-owner model.
    2. Search for "decision round" and show how implementation decisions get captured and approved.
    3. Open the developer space and show the account setup guide.
    4. Jump into the API reference and show that endpoint pages are generated from the OpenAPI spec.
    """,
)

summary(
    "home",
    [
        "* [Home](README.md)",
        "* [Demo map](demo-map.md)",
        "* [Discovery notes](discovery-notes.md)",
        "* [Review checklist](review-checklist.md)",
    ],
)

write(
    "home/demo-map.md",
    """
    ---
    description: "Connect Exotec's market message to the demo site's documentation architecture."
    icon: route
    ---

    # Demo Map

    The Exotec website emphasizes end-to-end warehouse automation, modular systems, reliable outcomes, faster time to value, and a software layer coordinating the warehouse ecosystem. The demo site turns those ideas into an information architecture for knowledge maintenance.

    <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><i class="fa-layer-group"></i></td><td><strong>Versioned documentation</strong></td><td>Keep product, software, implementation, and support pages clear across revisions.</td><td><a href="https://app.gitbook.com/s/XSPACE_GOVERNANCE/version-ownership.md">Version ownership</a></td></tr>
    <tr><td><i class="fa-user-lock"></i></td><td><strong>Tiered access</strong></td><td>Separate public docs, partner enablement, customer docs, and internal-only procedures.</td><td><a href="https://app.gitbook.com/s/XSPACE_GOVERNANCE/access-control-model.md">Access model</a></td></tr>
    <tr><td><i class="fa-code"></i></td><td><strong>API-first reference</strong></td><td>Generate endpoint pages from OpenAPI instead of hand-maintaining static reference pages.</td><td><a href="https://app.gitbook.com/s/XSPACE_API/api-overview.md">API overview</a></td></tr>
    <tr><td><i class="fa-file-signature"></i></td><td><strong>Procurement context</strong></td><td>Document contractual and procurement checkpoints alongside onboarding workflows.</td><td><a href="https://app.gitbook.com/s/XSPACE_GOVERNANCE/procurement-and-contract-docs.md">Procurement docs</a></td></tr>
    </tbody></table>

    ## Spaces

    * **Home**: framing, discovery notes, and review checklist.
    * **Documentation Governance**: versioning, owners, access levels, decision rounds, and procurement docs.
    * **Developer & API Reference**: developer account setup and OpenAPI-generated reference pages.
    """,
)

write(
    "home/discovery-notes.md",
    """
    ---
    description: "The key discovery-call themes used to shape this first draft."
    icon: microphone-lines
    ---

    # Discovery Notes

    The Fireflies summary from the Exotec intro call surfaced six themes that shaped the draft site.

    | Theme | How it appears in the site |
    | --- | --- |
    | Clear version documentation | Version ownership and release note patterns in Documentation Governance |
    | Document responsibility | Owner matrix and review workflow |
    | Decision rounds | Decision-round template for implementation and product-documentation choices |
    | Multi-level access control | Public, customer, partner, and internal documentation tiers |
    | Developer account procedures | Developer onboarding and account plan pages |
    | Contractual and procurement alignment | Procurement and contract documentation checkpoint page |

    {% hint style="warning" %}
    The transcript text available to the agent was very sparse. Treat this page as a transparent assumptions log and a place to collect Louis/Samuel corrections.
    {% endhint %}
    """,
)

write(
    "home/review-checklist.md",
    """
    ---
    description: "Review prompts for Louis and the Exotec demo owner."
    icon: clipboard-check
    ---

    # Review Checklist

    | Area | Question |
    | --- | --- |
    | Branding | Does the black, white, and Exotec teal styling feel close enough for a first demo? |
    | Structure | Should developer/API content be separate from governance, or merged into one docs space? |
    | Access | Are the proposed tiers the right way to show GitBook visitor access and permissions? |
    | API | Is the Petstore-generated reference enough, or should we add a mock Exotec warehouse API spec later? |
    | Call themes | Which discovery-call themes should be sharpened or removed? |
    """,
)

summary(
    "governance",
    [
        "* [Documentation Governance](README.md)",
        "",
        "## Operating model",
        "* [Version ownership](version-ownership.md)",
        "* [Decision rounds](decision-rounds.md)",
        "* [Access control model](access-control-model.md)",
        "",
        "## Business process",
        "* [Document owner matrix](document-owner-matrix.md)",
        "* [Procurement and contract docs](procurement-and-contract-docs.md)",
        "* [Release notes](release-notes.md)",
    ],
)

write(
    "governance/README.md",
    """
    ---
    description: "Govern Exotec documentation with owners, versions, access levels, and decision history."
    icon: shield-halved
    ---

    # Documentation Governance

    This space demonstrates how Exotec could maintain a reliable knowledge layer for product, implementation, support, and developer-facing documentation.

    ## Governance goals

    * Make current versions obvious.
    * Give every important document an owner.
    * Capture decision rounds before they disappear into Slack or meetings.
    * Separate public, customer, partner, and internal content.
    * Keep procurement and contractual context close to operational onboarding.

    {% hint style="success" %}
    Demo angle: this is the strongest place to show GitBook as a governed operating system for knowledge, not only a prettier docs front end.
    {% endhint %}
    """,
)

write(
    "governance/version-ownership.md",
    """
    ---
    description: "A practical pattern for versioned documentation ownership."
    icon: code-branch
    ---

    # Version Ownership

    Version confusion was one of the clearest discovery-call themes. This page models how GitBook can make version state visible without asking readers to inspect repository history.

    | Content type | Owner | Version signal | Review cadence |
    | --- | --- | --- | --- |
    | Warehouse software release notes | Product operations | Release month and system version | Monthly |
    | Developer API docs | Developer relations | OpenAPI spec slug and generated timestamp | On spec update |
    | Implementation playbooks | Deployment operations | Site template version | Quarterly |
    | Partner enablement | Partner programs | Access tier and program version | Quarterly |

    ## Version status labels

    * `current`: safe to use for implementation.
    * `preview`: visible to selected teams before rollout.
    * `deprecated`: still useful for installed-base support.
    * `archived`: retained for history only.

    {% hint style="info" %}
    GitBook can combine Git history, page feedback, change requests, and update blocks so version state is visible to readers and maintainers.
    {% endhint %}
    """,
)

write(
    "governance/decision-rounds.md",
    """
    ---
    description: "Capture implementation and documentation decisions in a reusable round format."
    icon: arrows-rotate
    ---

    # Decision Rounds

    Decision rounds keep cross-functional choices lightweight but traceable.

    {% stepper %}
    {% step %}
    ### Open the round

    State the question, owner, deadline, affected docs, and teams that need to weigh in.
    {% endstep %}

    {% step %}
    ### Collect options

    Capture the viable options, constraints, and consequences for implementation, support, and developer docs.
    {% endstep %}

    {% step %}
    ### Decide and publish

    Record the decision, update the affected pages, and link the decision round from the relevant docs.
    {% endstep %}

    {% step %}
    ### Review after rollout

    Add what changed after warehouse go-live or customer rollout so the page remains operationally true.
    {% endstep %}
    {% endstepper %}

    ## Template

    ```yaml
    decision_round:
      question:
      owner:
      deadline:
      affected_docs:
      options:
      decision:
      follow_up:
    ```
    """,
)

write(
    "governance/access-control-model.md",
    """
    ---
    description: "A tiered documentation access model for Exotec audiences."
    icon: user-lock
    ---

    # Access Control Model

    The discovery summary mentioned a multi-level access model. This draft uses four levels.

    | Level | Audience | Example content |
    | --- | --- | --- |
    | Public | Prospects and general readers | Solution overviews, industry pages, implementation philosophy |
    | Customer | Exotec customers | Deployment checklists, operator guides, support workflows |
    | Partner | Integrators and implementation partners | Partner programs, technical enablement, shared playbooks |
    | Internal | Exotec teams | Decision rounds, escalation paths, procurement notes, unpublished roadmap |

    ## GitBook demo notes

    * Use site visibility and permissions for broad access.
    * Use visitor claims or authenticated access for persona-specific content.
    * Keep source-of-truth pages in one place, then conditionally show callouts per audience.
    """,
)

write(
    "governance/document-owner-matrix.md",
    """
    ---
    description: "Document ownership matrix for high-value Exotec knowledge areas."
    icon: table
    ---

    # Document Owner Matrix

    | Area | Primary owner | Backup owner | Review trigger |
    | --- | --- | --- | --- |
    | System overview | Product marketing | Product operations | New module launch |
    | Warehouse software | Product operations | Engineering | Release or behavior change |
    | Deployment process | Deployment operations | Customer success | New implementation template |
    | Maintenance docs | Support operations | Field engineering | Escalation pattern or safety update |
    | API reference | Developer relations | Engineering | OpenAPI spec update |

    ## Owner rule

    A page without an owner is allowed to exist as a draft, but it should not be used as an operational source of truth.
    """,
)

write(
    "governance/procurement-and-contract-docs.md",
    """
    ---
    description: "Keep contractual and procurement context close to onboarding workflows."
    icon: file-signature
    ---

    # Procurement and Contract Docs

    Contractual and procurement alignment came up in the discovery summary. In GitBook, this can be shown as a controlled internal page linked from onboarding workflows.

    ## Procurement checkpoint

    * Confirm the plan or access level tied to the customer or partner.
    * Link the signed agreement or procurement status in the source CRM, not in public docs.
    * List any technical constraints that affect developer account setup.
    * Identify who can approve exceptions.

    {% hint style="warning" %}
    This page should not store contracts directly. It should explain process and link to the approved system of record.
    {% endhint %}
    """,
)

write(
    "governance/release-notes.md",
    """
    ---
    description: "A sample changelog using GitBook's Updates block."
    icon: clock-rotate-left
    layout:
      width: wide
    ---

    # Release Notes

    {% updates format="full" %}
    {% update date="2026-07-07" tags="demo,governance" %}
    ## First Exotec demo draft

    Added governance, developer onboarding, and API reference spaces based on the intro-call summary and Exotec's public website positioning.
    {% endupdate %}

    {% update date="2026-07-06" tags="discovery" %}
    ## Discovery-call themes captured

    Captured version documentation, document responsibility, decision rounds, access control, developer account setup, and procurement alignment as first-draft site themes.
    {% endupdate %}
    {% endupdates %}
    """,
)

write(
    "governance/.gitbook/tags.yaml",
    """
    - tag: demo
      label: Demo
      icon: wand-magic-sparkles
    - tag: governance
      label: Governance
      icon: shield-halved
    - tag: discovery
      label: Discovery
      icon: microphone-lines
    """,
)

summary(
    "developer-api",
    [
        "* [Developer & API Reference](README.md)",
        "* [Developer account setup](developer-account-setup.md)",
        "* [Account plans and access](account-plans-and-access.md)",
        "* [API overview](api-overview.md)",
        "",
        "## Generated API reference",
        "* ```yaml",
        "  type: builtin:openapi",
        "  props:",
        "    models: true",
        "    downloadLink: true",
        "  dependencies:",
        "    spec:",
        "      ref:",
        "        kind: openapi",
        "        spec: gitbook-petstore-demo",
        "  ```",
    ],
)

write(
    "developer-api/README.md",
    """
    ---
    description: "Developer onboarding plus an OpenAPI-generated reference section."
    icon: code
    ---

    # Developer & API Reference

    This space shows the API-reference motion Louis asked for. The generated endpoint pages come from the GitBook Petstore OpenAPI spec, while the surrounding pages show how Exotec could document developer accounts, access plans, and API conventions.

    ## What to demo

    <table data-view="cards"><thead><tr><th width="48"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><i class="fa-user-plus"></i></td><td><strong>Developer account setup</strong></td><td>Explain who can create accounts and what approvals are needed.</td><td><a href="developer-account-setup.md">Developer account setup</a></td></tr>
    <tr><td><i class="fa-layer-group"></i></td><td><strong>Plans and access</strong></td><td>Map account plan, customer or partner status, and API capability.</td><td><a href="account-plans-and-access.md">Account plans and access</a></td></tr>
    <tr><td><i class="fa-brackets-curly"></i></td><td><strong>Generated API reference</strong></td><td>Show endpoint pages generated from OpenAPI.</td><td><a href="api-overview.md">API overview</a></td></tr>
    </tbody></table>
    """,
)

write(
    "developer-api/developer-account-setup.md",
    """
    ---
    description: "A first-draft developer account onboarding workflow."
    icon: user-plus
    ---

    # Developer Account Setup

    The call summary referenced developers creating accounts and managing plans. This page turns that into a concrete onboarding flow.

    {% stepper %}
    {% step %}
    ### Confirm the audience

    Identify whether the developer is an Exotec employee, customer developer, implementation partner, or evaluator.
    {% endstep %}

    {% step %}
    ### Assign the access level

    Map the developer to public, customer, partner, or internal access before exposing environment details.
    {% endstep %}

    {% step %}
    ### Create the account

    Provision the account, attach it to the right organization or project, and confirm plan eligibility.
    {% endstep %}

    {% step %}
    ### Link to API reference

    Send the developer to the generated API pages and any environment-specific setup notes.
    {% endstep %}
    {% endstepper %}
    """,
)

write(
    "developer-api/account-plans-and-access.md",
    """
    ---
    description: "Show how plans and access levels shape developer documentation."
    icon: layer-group
    ---

    # Account Plans and Access

    | Plan or role | Docs shown | API behavior |
    | --- | --- | --- |
    | Evaluator | Public API overview and conceptual guides | No live credentials |
    | Customer developer | Customer onboarding, environment setup, API reference | Scoped credentials |
    | Partner developer | Partner enablement and integration playbooks | Partner sandbox |
    | Internal engineer | Internal decision rounds and operational runbooks | Internal environments |

    {% hint style="info" %}
    This is a demo model. Exotec should replace these labels with its real plan, project, and partner-access language.
    {% endhint %}
    """,
)

write(
    "developer-api/api-overview.md",
    """
    ---
    description: "Context page for the generated OpenAPI reference."
    icon: brackets-curly
    ---

    # API Overview

    The endpoint pages below are generated from the GitBook Petstore OpenAPI spec that Louis requested for the demo.

    ## Why this matters

    * The API reference stays aligned to a machine-readable spec.
    * Operation pages, schemas, examples, and download links can be refreshed without rewriting docs by hand.
    * Exotec can pair generated reference content with human-authored onboarding and governance pages.

    {% hint style="success" %}
    Demo action: open a generated endpoint from the sidebar, then show the Download spec control and schema pages.
    {% endhint %}
    """,
)

