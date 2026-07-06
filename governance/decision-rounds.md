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
