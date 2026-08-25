# Vipana — AI Ad Copy Generator

A small tool that generates ad copy from a campaign brief using Claude, with a basic approve/reject/improve loop so you can refine a generation without starting over from scratch.

# What it does
1) Type a campaign brief (e.g. "football 5 a side competition launch, enthusiastic tone, targeting 18–25s").

2) Click Generate — sends the brief to Claude and shows the resulting ad copy.

3) Click Approve or Reject to record a decision on it, or type an instruction (e.g. "make it shorter") and click Improve to generate a refined version, linked back to the original.

4) Every generation is saved to a local SQLite database, so past results persist between sessions.

# Why I built it

I wanted to understand how AI content-generation tools actually work under the hood, past just calling an API once — specifically the iterative "generate, review, refine" loop that tools like this are actually built around, rather than a single one-shot prompt.

# Tech stack

Built deliberately simple, to actually finish it in the time I had (roughly 20 hours, alongside A-level study):

1) Streamlit — handles both the UI and the app logic in one file, no separate frontend/backend split.

2) SQLite (sqlite3, no ORM) — a single local database file, no server to set up.

3) Claude API (Anthropic) — one function, one model, one provider.