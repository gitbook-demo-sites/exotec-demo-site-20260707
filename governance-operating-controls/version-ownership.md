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
