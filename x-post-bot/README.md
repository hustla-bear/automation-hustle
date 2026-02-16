# X Post Bot - Browser Automation

No API key needed. Uses Playwright + Stealth to post via web interface.

## Setup
```bash
pip install playwright playwright-stealth
playwright install chromium
```

## Usage

**Post single tweet:**
```bash
python x_post.py "Your tweet here"
```

**Post marketing thread:**
```bash
python post_thread.py
```

**Post custom thread:**
```python
from x_post import XPoster
import asyncio

async def post():
    poster = XPoster()
    tweets = ["Tweet 1", "Tweet 2", "Tweet 3"]
    await poster.post_thread(tweets)

asyncio.run(post())
```

## Features
- Cookie persistence (no re-login needed)
- Stealth mode (undetectable automation)
- Rate limiting (5s between tweets)
- Thread support (reply chains)

## Credentials
Set in `.secrets/credentials.env`:
- X_EMAIL=hustlabear@gmail.com
- X_PASSWORD=\$D4.Hustla\$
- X_HANDLE=CityHustleGuy
