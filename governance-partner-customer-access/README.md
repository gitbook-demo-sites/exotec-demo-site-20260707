---
description: "A governance variant for controlling what customers, partners, and internal teams can see."
icon: users-gear
---

# Documentation Governance: Partner and Customer Access

This variant emphasizes access governance. It shows how Exotec could keep one documentation system while presenting different details to public visitors, customers, integrators, and internal teams.

{% hint style="success" %}
Best demo angle: gated documentation is not only a restriction. It is a way to give every audience the right level of detail without duplicating entire portals.
{% endhint %}

## Audience model

| Audience | Access pattern | Example content | Governance concern |
| --- | --- | --- | --- |
| Public | Share-link or public site | Solution overviews and evaluation guides | Keep positioning current |
| Customer | Authenticated customer access | Operator guides, support flows, release notes | Avoid exposing internal escalation detail |
| Partner | Partner-specific access | Integration playbooks and implementation checklists | Keep enablement aligned with partner status |
| Internal | Team-only access | Decision records, roadmap notes, contract context | Preserve sensitive context without fragmenting docs |

## What this demonstrates

* One canonical page can serve multiple audiences.
* Sensitive notes can live near operating content without becoming public.
* GitBook can support authenticated MCP and AI use cases where agents also need scoped knowledge access.
