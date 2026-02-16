#!/usr/bin/env python3
"""X (Twitter) Browser Post Automation - No API needed"""
import asyncio, os, json, sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
    from playwright_stealth import stealth_async
except ImportError:
    print("pip install playwright playwright-stealth && playwright install chromium")
    sys.exit(1)

class XPoster:
    def __init__(self):
        self.email = os.getenv("X_EMAIL", "hustlabear@gmail.com")
        self.password = os.getenv("X_PASSWORD", "$D4.Hustla$")
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.cookies_file = self.data_dir / "x_cookies.json"
        
    async def load_cookies(self, context):
        if self.cookies_file.exists():
            with open(self.cookies_file) as f:
                await context.add_cookies(json.load(f))
            return True
        return False
    
    async def save_cookies(self, context):
        with open(self.cookies_file, 'w') as f:
            json.dump(await context.cookies(), f, indent=2)
    
    async def login(self, page):
        print("🔐 Logging into X...")
        await page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded")
        await asyncio.sleep(4)
        
        await page.fill('input[name="text"]', self.email, timeout=10000)
        await asyncio.sleep(1)
        await page.click('div[role="button"]:has-text("Next")')
        
        await asyncio.sleep(2)
        await page.fill('input[name="password"]', self.password, timeout=10000)
        await asyncio.sleep(1)
        await page.click('div[data-testid="LoginForm_Login_Button"]')
        
        await asyncio.sleep(5)
        return "home" in page.url
    
    async def post_tweet(self, page, text: str) -> bool:
        print(f"📝 Posting: {text[:60]}...")
        await page.goto("https://x.com/compose/tweet", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        try:
            await page.fill('div[role="textbox"]', text, timeout=10000)
            await asyncio.sleep(1)
            await page.keyboard.press("Control+Enter")
            await asyncio.sleep(3)
            return True
        except Exception as e:
            print(f"❌ {e}")
            return False
    
    async def post_thread(self, tweets: list) -> list:
        results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"]
            )
            
            context = await browser.new_context(locale="en-US", timezone_id="America/New_York")
            await self.load_cookies(context)
            
            page = await context.new_page()
            await stealth_async(page)
            
            # Check login
            await page.goto("https://x.com/home", wait_until="domcontentloaded")
            await asyncio.sleep(3)
            
            if "login" in page.url:
                if await self.login(page):
                    await self.save_cookies(context)
            
            # Post tweets
            for i, text in enumerate(tweets):
                print(f"\n{i+1}/{len(tweets)}")
                success = await self.post_tweet(page, text)
                results.append(success)
                if not success:
                    break
                await asyncio.sleep(5)
            
            await browser.close()
        return results

async def main():
    """CLI: python x_post.py 'Tweet text here'"""
    poster = XPoster()
    
    if len(sys.argv) > 1:
        tweets = sys.argv[1:]
    else:
        # Default test tweet
        tweets = ["Test tweet from automation 🤖"]
    
    results = await poster.post_thread(tweets)
    print(f"\n✅ Posted {sum(results)}/{len(results)}")

if __name__ == "__main__":
    asyncio.run(main())
