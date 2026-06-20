
# Content Agent

A CLI tool that generates, drafts, and revises social media posts using the Claude API. Give it a topic, and it generates 3 platform-specific post ideas (LinkedIn, Twitter, Instagram), drafts a full post for your selected idea, and lets you iteratively revise it before saving.

## Setup

1. Clone the repo:
``` bash
git clone https://github.com/siyajariwala/social-media-automation.git
cd social-media-automation 
```

2. Create and activate a virtual environment:
``` bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
``` bash
pip install anthropic python-dotenv
```

4. Set up your API key:
```bash
cp .env.example .env
```
Then open `.env` and paste in your own Anthropic API key.


## How to Run
```bash
python3 content_agent.py
```

You'll be prompted to:
1. Enter a topic
2. Pick one of 3 generated post ideas (1, 2, or 3)
3. Review the drafted post
4. Type `approve` to save it, or give feedback (e.g. "make it shorter") to revise

Approved posts are saved to `output/posts.json`.


## Judgment Calls

Platform variety in idea generation:
-  The assignment didn't specify whether all 3 ideas needed different platforms or could repeat.
-  I constrained the prompt to require one idea per platform (LinkedIn, Twitter, Instagram). 
-  The tradeoff: some topics naturally fit one platform better than others, so an idea can occasionally feel slightly forced  
   onto its assigned platform. 
-  I accepted this because it guarantees variety and better demonstrates platform-specific adaptation in a single demo run.

Structured output via JSON instead of plain text parsing:
- Early on I considered extracting platform info by parsing bracketed text (e.g. `[LinkedIn]`) out of plain strings. 
- I switched `generate_post_ideas()` to return structured JSON instead, since it's deterministic — it doesn't depend on Claude 
  consistently following an exact text format across every call, and it keeps Claude focused on generating good content rather than formatting compliance. 
- I added a fallback to strip markdown code fences in case Claude wraps the JSON in ```` ```json ```` blocks anyway, since LLM 
  output isn't 100% predictable even with explicit instructions.

Tone matching left to the revision loop:
- I noticed idea generation sometimes produced a contrarian or optimistic angle even when the topic itself had a frustrated or 
  negative tone, since the system prompt rewards specific, sharp claims over generic ones. 
- Rather than over-constraining the ideation prompt to force tone-matching (which risks limiting genuinely interesting 
  angles), I left this to the revision loop — if a user wants the post to better match their original tone, they can request that directly via feedback, which the tool handles correctly.


## What I'd Improve Next

If this were used daily by a real team, I'd add a few things: a `--platform` flag to skip ideation and go straight to drafting for a specific platform, persistent storage of past approved posts to use as few-shot examples in future ideation prompts (so brand voice stays consistent over time), and streaming responses so users see output as it's generated rather than waiting for the full response. I'd also add stricter JSON schema validation beyond the basic markdown-fence stripping I have now, in case Claude's output format drifts in unexpected ways.
