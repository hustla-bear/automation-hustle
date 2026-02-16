#!/usr/bin/env python3
"""
Reddit Poster - Automated r/slavelabour posting
Uses credentials from secrets vault
"""
import os, sys, time, random

try:
    import praw
except ImportError:
    print("pip3 install praw --break-system-packages")
    sys.exit(1)

# Credentials from vault
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "i3Xm09h2J38SKeyZI_mMQ")
REDDIT_SECRET = os.getenv("REDDIT_SECRET", "YOUR_SECRET_HERE")
REDDIT_USER = os.getenv("REDDIT_USER", "HustlaTheBear")
REDDIT_PASS = os.getenv("REDDIT_PASS", "YOUR_PASSWORD_HERE")

REDDIT_POST = """
[OFFER] Python automation scripts - $50-150 - 2 hr delivery

Need a script to scrape, automate, or process data? I write clean Python:

- Web scrapers (BeautifulSoup, Selenium, Playwright)
- API integrations  
- Data processing (Pandas, CSV, JSON)
- File organizers
- Report generators

Recent: $150 for 3-hour job scraping 5k product listings

$50-150 depending on complexity. 2-hour delivery for simple tasks.

PayPal, Venmo, Crypto accepted.

[Comment $bid below]
"""

def post_to_slavelabour():
    """Post offer to r/slavelabour"""
    print("🚀 Posting to r/slavelabour...")
    
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_SECRET,
            username=REDDIT_USER,
            password=REDDIT_PASS,
            user_agent="python:hustla-automation:v1.0 (by /u/" + REDDIT_USER + ")"
        )
        
        # Verify auth
        user = reddit.user.me()
        print(f"✅ Logged in as: {user.name}")
        
        # Post to r/slavelabour
        subreddit = reddit.subreddit("slavelabour")
        submission = subreddit.submit(
            title="[OFFER] Python automation scripts - $50-150 - 2 hr delivery",
            selftext=REDDIT_POST,
            flair_id=None  # Use default flair
        )
        
        print(f"✅ Posted: https://reddit.com{submission.permalink}")
        print(f"   Post ID: {submission.id}")
        return submission
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    post_to_slavelabour()
