#!/usr/bin/env python3
"""Post the Automation Hustle marketing thread"""
import asyncio, sys
from x_post import XPoster

THREAD = [
    """Automation changed how I make money.

Not by working more. By working once and deploying 24/7.

Here's 5 systems running while I sleep:

🧵""",
    
    """1/ Price Monitor Bot

Scans 50 sites hourly.
Alerts when price drops below target.

Best arbitrage discovery.
Saves 10 hours/week.

Value: $100-500/week""",

    """2/ Lead Scraper

Extracts emails from directories.
Cleans, dedupes, exports CSV.

Sold lists for $50-200 each.
100% automated.

Value: $500-2000/month""",

    """3/ Content Pipeline

Reddit top posts → Twitter threads.
Feeds the machine.

Audience grows on autopilot → sponsorship cash.

Value: Indestructible""",

    """4/ Report Generator

Pulls data → builds charts → emails PDF.
Client gets report daily at 9am.
Never touched by human.

Value: $200-500/month per client""",

    """5/ Invoice Chaser

Auto-emails overdue invoices.
Escalates politely.

Recovers 10-15% more revenue.
No awkward conversations.

Value: $1k-5k/year in recovered payments""",

    """The pattern:
• Build once
• Run forever  
• Scale infinitely

Your time has a cap.
Your code doesn't.""",

    """Want the code?

github.com/hustla-bear/automation-hustle

DM if you need something built.
2-hour delivery."""
]

async def main():
    poster = XPoster()
    print(f"🚀 Posting {len(THREAD)}-tweet thread...")
    
    results = await poster.post_thread(THREAD)
    
    success_count = sum(1 for r in results if r)
    print(f"\n✅ Posted {success_count}/{len(THREAD)} tweets")
    
    if success_count == len(THREAD):
        print("🎉 Full thread posted successfully!")
    else:
        print("⚠️  Some tweets failed - check above for errors")

if __name__ == "__main__":
    asyncio.run(main())
