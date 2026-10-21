# AI search crawler access

## Intended policy

Allow AI search indexing and user-requested retrieval while retaining model-training
opt-outs. The origin robots.txt explicitly allows OAI-SearchBot, ChatGPT-User,
PerplexityBot, Perplexity-User, Claude-SearchBot and Claude-User. Ordinary Google
and Bing search crawling remains allowed.

These permissions support discovery; they do not guarantee indexing, citations,
recommendations, or an improved third-party GEO score. Training opt-outs rely on
crawler compliance and do not technically prevent access.

## What the accessibility check established

The public homepage, /landscaping-leicester and /case-studies returned HTTP 200,
real page titles and one H1 in requests using each supported search user-agent
name, plus Googlebot and bingbot. No X-Robots-Tag or Cloudflare challenge header
was observed in those responses.

These are user-agent simulations from the development environment, NOT requests
from verified provider IPs. They cannot establish that Cloudflare permits every
real crawler or that any provider has indexed the pages.

The live robots.txt includes Cloudflare-managed content prepended to the origin
file. It blocks training crawlers, has search=yes and ai-train=no content signals,
and currently uses use=reference. It also restricts Google-Extended, which has
uses beyond Google Search. This change does not remove that managed restriction
or promise visibility in every Gemini surface.

## Cloudflare checks still required

1. Select premium-landscapes.co.uk in Cloudflare.
2. In Security settings, filter by Bot traffic and open Configure AI bot policies
   (or the equivalent AI Crawl Control screen if the account uses a different UI).
3. Allow Search and, for user-directed AI retrieval, Agent access. Keep Training
   set to Disallow. Do not disable all bot protection.
4. Check AI Crawl Control and security events for blocked legitimate search bots.
   Any narrow exception should verify provider identity/IP ranges; never bypass
   protection based only on an easily spoofed user-agent name.
5. Review the content-use policy: the observed use=reference permits indexing,
   excerpts and links, rather than broad summary/reproduction permission. Do not
   treat it as proof that all forms of AI answer reuse are authorized.
6. After publishing, inspect /robots.txt to confirm the six search agents are
   allowed and training opt-outs remain. Check logs for real verified crawler
   traffic over time.

Website code cannot override an edge firewall block or reliably undo a conflicting
Cloudflare-managed robots.txt rule. Cloudflare settings must be changed separately
when necessary.

## Validation

Run:

    python3 -m unittest discover -s scripts -p 'test_robots_policy.py'

## Official references

- OpenAI crawler roles: https://developers.openai.com/api/docs/bots
- Anthropic crawler roles: https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Perplexity crawler roles and WAF guidance: https://docs.perplexity.ai/guides/bots
- Cloudflare managed robots.txt: https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/
