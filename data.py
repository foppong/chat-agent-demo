# data.py

# CHALLENGE: The "Fire Drill" Hijack (Resource Contention)
# 1. Mike commits to Profile v2 by Thursday.
# 2. Lisa mentions a dependency (soft blocker).
# 3. Alex (Sales) interrupts with a P0 emergency for a major client.
# 4. Sarah (PM) says "All hands on deck" for the sales issue.
# TRAP: V1 often keeps Profile v2 as "ACTIVE" because Mike never explicitly un-committed to it,
# even though he is now fully occupied by the sales fire.
MESSY_CHAT_THREAD = """
[10:00] Sarah (PM): Team, final push for User Profile v2. We need it by Friday. Mike, you good for backend?
[10:02] Mike (Backend): Yep, I'm clear. I'll have it on staging by Thursday EOD.
[10:10] Lisa (Design Sys): Just FYI, that uses the new Universal Uploader. It's a bit flaky in QA right now, might slow you down.
[10:12] Alex (Sales): URGENT!! @channel We just lost the Acme Corp demo because of a 500 error on the login page. They are furious. We need this fixed NOW or we lose a $1M deal.
[10:13] Sarah (PM): Whoa, okay. P0. Mike, can you investigate that 500 error immediately?
[10:14] Mike (Backend): On it. Checking logs now.
[10:15] Sarah (PM): Everyone else, stand by to help Mike if he needs it. We cannot lose Acme.
"""

GOLDEN_TASKS = [
    {
        "task": "Investigate/Fix Acme Corp 500 Error",
        "owner": "Mike",
        "due_date": "IMMEDIATE (P0)",
        "status": "active"
    },
    {
        "task": "Ship User Profile v2 Backend",
        "owner": "Mike",
        "due_date": "Thursday EOD",
        "status": "blocked" # Blocked by P0 Fire Drill + Design dependency
    }
]