---
description: "A governance variant for controlling what customers, partners, and internal teams can see."
icon: users-gear
---

# Variant B: Partner and Customer Access

This version emphasizes access governance. It shows how Exotec could keep one documentation system while presenting different details to public visitors, customers, integrators, and internal teams.

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

## Conditional content example

{% tabs %}
{% tab title="Customer view" %}
Customers see deployment steps, maintenance responsibilities, and how to escalate a support issue through the approved channel.
{% endtab %}

{% tab title="Partner view" %}
Partners see implementation assumptions, technical handoff notes, and enablement material connected to their program tier.
{% endtab %}

{% tab title="Internal view" %}
Internal teams see decision history, procurement notes, commercial context, and risk flags that should not be exposed externally.
{% endtab %}
{% endtabs %}

## What this demonstrates

* One canonical page can serve multiple audiences.
* Sensitive notes can live near the operating content without becoming public.
* GitBook can support authenticated MCP and AI use cases where agents also need scoped knowledge access.

{% hint style="warning" %}
In a live implementation, audience claims should come from the identity provider or customer portal, not manual page duplication.
{% endhint %}
