#!/usr/bin/env python3
"""
Price Monitor Pro - Client Deliverable
Tracks prices from any website, sends Discord/Email alerts on drops.

SETUP:
1. pip install requests beautifulsoup4
2. Configure DISCORD_WEBHOOK below
3. Add URLs to monitor_urls list
4. Run: python3 price_monitor.py
5. (Optional) Add to cron: */30 * * * * /usr/bin/python3 /path/to/price_monitor.py

Author: Barry Hustla
Delivery: 2 hours
Price: $75-150
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from typing import Dict, Optional

# ============== CONFIG ==============
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "YOUR_WEBHOOK_URL_HERE")
DATA_FILE = "prices.json"

# Products to monitor (CUSTOMIZE THIS)
monitor_urls = [
    {
        "name": "Example Product 1",
        "url": "https://example.com/product1",
        "selector": ".price",  # CSS selector for price element
        "price_format": "${:.2f}"  # Format for display
    },
    # Add more products here...
]

# ============== CORE FUNCTIONS ==============

def load_previous_prices() -> Dict:
    """Load price history from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_prices(prices: Dict):
    """Save current prices to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(prices, f, indent=2)

def extract_price(url: str, selector: str) -> Optional[float]:
    """Scrape price from URL using CSS selector"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        price_elem = soup.select_one(selector)
        
        if price_elem:
            # Extract number from text (handles $99.99, €99,99, 99.99, etc.)
            price_text = price_elem.text.strip()
            # Remove currency symbols and whitespace
            price_text = price_text.replace("$", "").replace("€", "").replace("£", "")
            price_text = price_text.replace(",", "").strip()
            return float(price_text)
            
    except Exception as e:
        print(f"Error extracting price from {url}: {e}")
    return None

def send_discord_alert(product_name: str, old_price: float, new_price: float, url: str):
    """Send price drop alert to Discord"""
    if DISCORD_WEBHOOK == "YOUR_WEBHOOK_URL_HERE":
        print(f"[ALERT] {product_name}: ${old_price} → ${new_price}")
        print("Set DISCORD_WEBHOOK to enable notifications")
        return
    
    savings = old_price - new_price
    savings_pct = (savings / old_price) * 100
    
    message = {
        "content": "🚨 Price Drop Alert!",
        "embeds": [{
            "title": product_name,
            "url": url,
            "color": 3066993,
            "fields": [
                {"name": "Old Price", "value": f"${old_price:.2f}", "inline": True},
                {"name": "New Price", "value": f"${new_price:.2f}", "inline": True},
                {"name": "You Save", "value": f"${savings:.2f} ({savings_pct:.1f}%)", "inline": True}
            ],
            "footer": {"text": f"Checked at {datetime.now().strftime('%Y-%m-%d %H:%M')}"}
        }]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK, json=message, timeout=10)
        if response.status_code == 204:
            print(f"✅ Discord alert sent for {product_name}")
        else:
            print(f"⚠️ Discord error: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send Discord alert: {e}")

def check_all_prices():
    """Main monitoring loop"""
    print(f"\n🔍 Price check started at {datetime.now()}")
    previous_prices = load_previous_prices()
    current_prices = {}
    
    for product in monitor_urls:
        print(f"  Checking: {product['name']}")
        
        current_price = extract_price(product['url'], product['selector'])
        
        if current_price is None:
            print(f"    ⚠️ Could not extract price")
            continue
        
        current_prices[product['url']] = {
            "price": current_price,
            "name": product['name'],
            "checked": datetime.now().isoformat()
        }
        
        # Check if price dropped
        if product['url'] in previous_prices:
            old_price = previous_prices[product['url']]['price']
            
            if current_price < old_price:
                print(f"    📉 PRICE DROP: ${old_price:.2f} → ${current_price:.2f}")
                send_discord_alert(product['name'], old_price, current_price, product['url'])
            elif current_price > old_price:
                print(f"    📈 Price increased: ${old_price:.2f} → ${current_price:.2f}")
            else:
                print(f"    ➖ No change: ${current_price:.2f}")
        else:
            print(f"    ✓ First price check: ${current_price:.2f}")
    
    # Save current prices for next run
    save_prices(current_prices)
    print(f"✅ Check complete. Next run will compare against these prices.\n")

# ============== MAIN ==============

if __name__ == "__main__":
    print("=" * 50)
    print("Price Monitor Pro")
    print("Built by Barry Hustla")
    print("=" * 50)
    
    check_all_prices()
    
    print("\n💡 Tips:")
    print("   - Add to cron: crontab -e")
    print("   - Check every 30min: */30 * * * * /usr/bin/python3 price_monitor.py")
    print("   - Set DISCORD_WEBHOOK env var for alerts")
