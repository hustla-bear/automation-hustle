#!/usr/bin/env python3
"""Lead Scraper Pro - Client Deliverable"""
import requests, re, time, csv
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin

TARGET_URLS = []  # Add URLs to scrape
OUTPUT_FILE = "leads.csv"
DELAY = 1

def extract_emails(text):
    return re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)

def extract_phones(text):
    return re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)

def fetch_page(url):
    try:
        r = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        }, timeout=15)
        return r.text if r.status_code == 200 else ""
    except:
        return ""

def scrape_leads(url: str) -> List[Dict]:
    print(f"Scraping: {url}")
    html = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")
    
    leads = []
    # Generic: find all divs with business-like content
    for item in soup.find_all(["div", "li"], class_=lambda x: x and any(
        word in x.lower() for word in ["business", "listing", "result", "place"]
    )):
        text = item.get_text(separator=" ")
        name = item.find(["h2", "h3", "a", "span"])
        name = name.text.strip() if name else ""
        
        emails = extract_emails(text)
        phones = extract_phones(text)
        
        if name and (emails or phones):
            leads.append({
                "name": name[:100],
                "emails": ",".join(emails[:3]),
                "phones": ",".join(phones[:2]),
                "source": url,
                "snippet": text[:200].replace("\n", " ")
            })
    
    time.sleep(DELAY)
    return leads

def save_leads(leads):
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "emails", "phones", "source", "snippet"])
        writer.writeheader()
        writer.writerows(leads)
    print(f"Saved {len(leads)} leads to {OUTPUT_FILE}")

if __name__ == "__main__":
    if not TARGET_URLS:
        print("Add URLs to TARGET_URLS list first!")
        exit(1)
    
    all_leads = []
    for url in TARGET_URLS:
        leads = scrape_leads(url)
        all_leads.extend(leads)
        print(f"  Found {len(leads)} leads")
    
    save_leads(all_leads)
    print(f"\nTotal: {len(all_leads)} leads ready in {OUTPUT_FILE}")
