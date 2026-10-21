---
name: AI search access policy
description: Preserve the distinction between AI search access and training consent.
---

Allow legitimate AI search and user-requested retrieval while retaining AI model
training opt-outs.

**Why:** The owner approved this scope to improve GEO without broadly authorizing
model training. Crawl permission does not guarantee AI recommendations.

**How to apply:** Keep search and training agents separate when revising crawler
rules. Check the public robots.txt and Cloudflare policies as well as repository
configuration: the hosting layer can prepend managed rules or block requests
independently. Do not claim user-agent simulation proves verified crawler access.
