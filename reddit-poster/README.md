# Reddit Poster Automation

## Setup Required

1. **Get Reddit API credentials:**
   - Go to https://www.reddit.com/prefs/apps
   - Create app (script type)
   - Copy client_id and secret

2. **Set environment variables:**
```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_SECRET="your_secret"
export REDDIT_USER="HustlaTheBear"
export REDDIT_PASS="your_password"
```

3. **Install:**
```bash
pip3 install praw --break-system-packages
```

4. **Post:**
```bash
python3 post_to_slavelabour.py
```

## Automated Monitoring

`monitor_bids.py` - Runs every 5 minutes, alerts on new $bid comments

## Multiple Subreddits

- r/slavelabour → Main offering
- r/forhire → Professional services
- r/workonline → Remote work
- r/passive_income → Product sales

## Schedule

Use cron for regular posting:
```bash
# Post daily at 9am, 3pm, 9pm UTC
0 9,15,21 * * * cd /path/to/reddit-poster && python3 post_to_slavelabour.py
```
