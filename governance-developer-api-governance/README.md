---
description: "A governance variant for API reference ownership, OpenAPI freshness, and developer onboarding."
icon: code-pull-request
---

# Documentation Governance: Developer API Governance

This variant connects Documentation Governance to the Developer & API Reference space. It is built for a conversation about keeping API docs current while still giving business teams visibility into ownership and change control.

{% hint style="info" %}
Best demo angle: GitBook can combine human-authored guidance with generated OpenAPI reference pages, so API documentation is useful to developers and governed by the teams that own it.
{% endhint %}

## API governance checklist

| Area | Governance rule | Evidence in GitBook |
| --- | --- | --- |
| Spec ownership | Every OpenAPI spec has a technical owner | Spec slug, source URL, generated timestamp |
| Breaking changes | Breaking changes require a decision round | Linked decision record and release note |
| Developer onboarding | Account setup docs match active access plans | Connected guide in Developer & API Reference |
| Deprecation | Deprecated endpoints keep a sunset path | Version status and migration guidance |

## Maintainer responsibilities

* Product engineering owns OpenAPI source freshness.
* Developer relations owns onboarding narrative and examples.
* Product operations owns release notes and decision records.
* Support owns known-issue guidance and escalation paths.
