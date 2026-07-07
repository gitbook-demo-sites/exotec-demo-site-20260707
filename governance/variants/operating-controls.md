---
description: "A governance variant for operational playbooks, release readiness, and field execution."
icon: list-check
---

# Variant A: Operating Controls

This version frames Documentation Governance around operational readiness: which Exotec teams own knowledge, how changes move from draft to approved, and what field teams can trust during customer rollout.

{% hint style="info" %}
Best demo angle: show GitBook as the layer that turns fast-changing internal knowledge into controlled, trusted operating documentation.
{% endhint %}

## When to use this variant

Use this variant when the buyer cares most about:

* release readiness across product, support, and deployment teams
* reducing ambiguity around the latest operating procedure
* auditability for decisions and handoffs
* keeping field teams aligned during robotics system changes

## Governance model

| Control | Primary owner | Approval signal | Reader outcome |
| --- | --- | --- | --- |
| Release readiness page | Product operations | Published release tag | Teams know which version is current |
| Deployment playbook | Deployment operations | Owner review complete | Field teams follow the approved rollout path |
| Escalation procedure | Support leadership | Review date and approver | Support teams route issues consistently |
| Decision record | Program lead | Decision round closed | Readers understand why the rule changed |

## Example workflow

{% stepper %}
{% step %}
### Draft the change

The owning team drafts the new operating guidance in GitBook and tags the page as `preview` until the release window is confirmed.
{% endstep %}

{% step %}
### Run the decision round

Product operations, deployment, and support review the change in one place. Comments and decisions stay attached to the source page.
{% endstep %}

{% step %}
### Publish the approved version

The page moves to `current`, release notes are updated, and the previous version is retained for installed-base support.
{% endstep %}
{% endstepper %}

## Demo talking points

* Version state is visible to both readers and maintainers.
* Review history makes decisions easier to defend later.
* Teams can keep operational detail close to the customer-facing docs it supports.
