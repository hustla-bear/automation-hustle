#!/usr/bin/env python3
"""
YouTube Shorts Content Generator
Specifically optimized for YouTube Shorts algorithm
"""
import json
import random
from datetime import datetime
from pathlib import Path
import sys

# Add parent dir for tiktok generator
sys.path.insert(0, str(Path(__file__).parent.parent / 'tiktok-automation' / 'scripts'))

# YouTube-specific viral patterns (different from TikTok)
YOUTUBE_PATTERNS = {
    "retention_hooks": [
        "Wait for the end...",
        "This one trick...",
        "Most people don't know...",
        "Stop doing this...",
        "I was today years old...",
        "This changed everything...",
        "POV: You finally learned...",
    ],
    "ctr_titles": [
        "From $0 to $10K with ONE script",
        "The automation they don't want you to know",
        "Why your code isn't making money",
        "This Python trick saves 10 hours/week",
        "I automated my entire income (proof)",
        "Stop learning Python wrong",
        "The $500/hour side hustle",
    ],
    "thumbnail_text": [
        "$0 → $10K",
        "10 hours → 10 min",
        "STOP",
        "AUTO",
        "SECRET",
        "MONEY",
        "PROOF",
    ],
    "description_templates": [
        "💰 Build systems that print money 24/7",
        "🚀 Free automation scripts below",
        "⚡ Turn code into cash flow",
        "📈 Systems > Hours",
        "💸 Build once, earn forever",
    ]
}

NICHE_SPECIFIC = {
    "automation": {
        "hashtags": ["#automation", "#python", "#sidehustle", "#passiveincome", "#aitools", "#makemoneyonline"],
        "tags": ["automation", "python", "side hustle", "passive income", "AI tools", "make money online"],
    },
    "coding": {
        "hashtags": ["#codinglife", "#programming", "#developer", "#softwareengineer", "#tech", "#learnpython"],
        "tags": ["coding life", "programming", "developer", "software engineer", "tech", "learn python"],
    },
    "entrepreneur": {
        "hashtags": ["#entrepreneur", "#business", "#startup", "#hustle", "#grind", "#success"],
        "tags": ["entrepreneur", "business", "startup", "hustle", "grind", "success"],
    }
}

def generate_youtube_content() -> dict:
    """Generate YouTube-specific content"""
    
    # Base content from TikTok generator (reusable)
    # Import the generator logic
    from generate_viral_content import HOOKS, TRENDING_SOUNDS
    
    # Select hook
    niche = random.choice(list(HOOKS.keys()))
    base_hook = random.choice(HOOKS[niche])
    
    # YouTube-ify it
    retention_hook = random.choice(YOUTUBE_PATTERNS["retention_hooks"])
    ctr_title = random.choice(YOUTUBE_PATTERNS["ctr_titles"])
    thumbnail = random.choice(YOUTUBE_PATTERNS["thumbnail_text"])
    desc_template = random.choice(YOUTUBE_PATTERNS["description_templates"])
    
    # Combine for YouTube algorithm
    title_options = [
        f"{ctr_title}",
        f"{retention_hook} {base_hook.split(':')[0] if ':' in base_hook else base_hook}",
        f"{base_hook} #Shorts",
    ]
    
    title = random.choice(title_options)
    
    # Ensure proper length
    if len(title) > 100:
        title = title[:97] + "..."
    
    # Build description optimized for YouTube
    description = f"""{desc_template}

{base_hook}

Learn to build systems that work while you sleep.

🚀 Free automation scripts: https://github.com/hustla-bear/automation-hustle
💸 Book custom build: https://hustla.ai/audit

Timestamps:
00:00 The problem
00:15 The solution
00:30 The results

#shorts #automation #python #sidehustle #makemoneyonline

Recommended videos:
→ How I 10x'd my income: https://youtube.com/...
→ Build your first bot: https://youtube.com/...
→ From $0 to $10K: https://youtube.com/...

About this channel:
Turn code into cash flow. Free scripts, paid builds, and the systems mindset.
"""
    
    # SEO tags (YouTube uses these differently)
    niche_tags = random.choice(list(NICHE_SPECIFIC.values()))
    tags = niche_tags["tags"] + ["shorts", "viral", "trending", "2026"]
    hashtags = niche_tags["hashtags"] + ["#shorts", "#viral"]
    
    content = {
        "platform": "youtube_shorts",
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "title": title,
        "description": description,
        "tags": tags,
        "hashtags": hashtags,
        "thumbnail_text": thumbnail,
        "retention_hook": retention_hook,
        "base_hook": base_hook,
        "niche": niche,
        "estimated_duration": random.choice([15, 30, 45, 60]),
        "seedance_prompts": [
            f"Cinematic YouTube Short: vertical 9:16, {base_hook.split('.')[0]}, tech aesthetic, neon highlights, professional",
            f"High-energy short: coding motion, fast cuts, satisfying keyboard typing, productivity vibe",
            f"Transformation ending: {desc_template}, sunrise lighting, hopeful music, 4K"
        ],
        "call_to_action": [
            "Link in bio for free scripts",
            "Comment CODE for the build",
            "Subscribe for daily automation tips",
            "Full system in description"
        ],
        "posting_strategy": {
            "optimal_times": ["05:00", "12:00", "17:00", "21:00", "23:00"],
            "frequency": "daily",
            "best_days": ["Tuesday", "Wednesday", "Thursday", "Saturday"]
        },
        "monetization_tags": [
            "automation software",
            "python course",
            "side hustle guide",
            "passive income system"
        ]
    }
    
    return content

def generate_batch(count: int = 10) -> list:
    """Generate batch of YouTube content"""
    batch = []
    
    for i in range(count):
        content = generate_youtube_content()
        content['batch_id'] = i + 1
        batch.append(content)
    
    return batch

def save_batch(batch: list):
    """Save batch to file"""
    output_dir = Path(__file__).parent / "content_generated"
    output_dir.mkdir(exist_ok=True)
    
    filename = output_dir / f"youtube_batch_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    with open(filename, 'w') as f:
        json.dump(batch, f, indent=2)
    
    print(f"✓ Generated {len(batch)} YouTube Shorts concepts")
    print(f"📁 Saved to: {filename}")
    
    # Print sample
    print("\n" + "="*60)
    print("🎬 SAMPLE YOUTUBE SHORT:")
    print("="*60)
    print(f"Title: {batch[0]['title']}")
    print(f"Thumbnail text: {batch[0]['thumbnail_text']}")
    print(f"Duration: {batch[0]['estimated_duration']}s")
    print(f"Tags: {', '.join(batch[0]['tags'][:5])}...")
    print(f"\nSeedance prompt:")
    print(f"  {batch[0]['seedance_prompts'][0][:80]}...")
    
    return filename

def generate_seo_optimized():
    """Generate content specifically for SEO discovery"""
    seo_queries = [
        "how to automate income",
        "python side hustle 2026",
        "passive income with code",
        "make money with automation",
        "python scripts that pay",
        "ai tools entrepreneur",
        "quit 9 to 5 coding",
        "automated business ideas",
    ]
    
    seo_content = []
    for query in seo_queries:
        content = generate_youtube_content()
        content['seo_target'] = query
        content['title'] = f"{query.title()} | #Shorts"
        seo_content.append(content)
    
    return seo_content

if __name__ == "__main__":
    print("🚀 YouTube Shorts Content Generator\n")
    
    #