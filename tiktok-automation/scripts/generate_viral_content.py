#!/usr/bin/env python3
"""
TikTok Viral Content Generator
Creates scripts, storyboards, and prompts for Seedance 2.0 + LLM workflow
"""
import json
import random
from datetime import datetime
from pathlib import Path

# Viral hooks database
HOOKS = {
    "money": [
        "I made $500 while you were sleeping",
        "POV: Your automation just hit $10K",
        "I quit my 9-5 with this one script",
        "This AI system prints money 24/7",
        "From broke to $50K/month with Python",
    ],
    "controversy": [
        "Unpopular opinion: 9-5s are a trap",
        "Your boss doesn't want you to see this",
        "Why coding bootcamps are a scam",
        "AI won't replace you, but this might",
        "Stop learning frameworks. Start earning.",
    ],
    "satisfaction": [
        "The most satisfying automation you'll see today",
        "This code runs smoother than your morning coffee",
        "POV: You finally fixed that memory leak",
        "ASMR for developers",
        "Clean code hits differently at 3am",
    ],
    "transformation": [
        "Day in the life: 6-figure solo dev",
        "From factory worker to AI automation expert",
        "How I 10x'd my income in 6 months",
        "POV: You escaped the matrix",
        "This is what freedom looks like",
    ],
    "educational": [
        "Python trick that will save you hours",
        "Stop paying $99/month for this",
        "This automation replaces 5 tools",
        "GPT-4 vs Claude: The real cost breakdown",
        "One-click deployment hack",
    ]
}

STORY_STRUCTURE = {
    "hook": "{hook_text}",
    "scene_1": "{setup_context}",
    "transition": "{visual_transition}",
    "scene_2": "{the_solution}",
    "payoff": "{result_cta}"
}

TRENDING_SOUNDS = [
    "lo-fi chill beats",
    "corporate technology documentary",
    "satisfying keyboard typing ASMR",
    "dramatic revelation",
    "motivational orchestral",
]

def generate_video_idea(niche: str = None) -> dict:
    """Generate a complete video concept"""
    
    if niche is None:
        niche = random.choice(list(HOOKS.keys()))
    
    hook = random.choice(HOOKS[niche])
    sound = random.choice(TRENDING_SOUNDS)
    duration = random.choice([15, 30, 45, 60])
    
    # Generate scene descriptions for Seedance
    scenes = {
        "opening": f"Cinematic shot of {random.choice(['modern workspace', 'coding setup', 'city skyline through window', 'multiple monitors'])}",
        "middle": f"Dynamic shot of {random.choice(['typing furiously on keyboard', 'code scrolling on screen', 'phone notification', 'coffee cup with steam'])} in {random.choice(['blue hour lighting', 'warm desk lamp', 'minimalist aesthetic', 'cyberpunk neon'])} style",
        "closing": f"Satisfying shot of {random.choice(['payment notification', 'success dashboard', 'sunrise through window', 'relaxed developer'])}"
    }
    
    concept = {
        "niche": niche,
        "duration": duration,
        "hook": hook,
        "sound": sound,
        "scenes": scenes,
        "caption_template": f"{hook}\n\n📦 Full system in bio\n👇 Comment for access",
        "hashtags": ["#automation", "#python", "#sidehustletok", "#ai", "#passiveincome", "#developer"],
        "seedance_prompts": [
            f"Cinematic 1080p vertical video: {scenes['opening']}, depth of field, professional lighting", 
            f"Smooth motion: {scenes['middle']}, 9:16 aspect ratio, tech aesthetic",
            f"Feel-good ending: {scenes['closing']}, warm color grade, satisfying"
        ],
        "script": {
            "voiceover": hook,
            "captions": [
                f"{hook[:50]}...",
                "This changed everything ↓",
                "Link in bio 💰"
            ],
            "cta": "Follow for the full blueprint"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    return concept

def generate_daily_content_calendar(days: int = 7) -> list:
    """Generate a week of content"""
    calendar = []
    niches_to_rotate = ["money", "controversy", "satisfaction", "transformation", "educational", "money", "controversy"]
    
    for day in range(days):
        niche = niches_to_rotate[day % len(niches_to_rotate)]
        concept = generate_video_idea(niche)
        
        calendar.append({
            "day": day + 1,
            "date": (datetime.now().replace(hour=0, minute=0, second=0) + __import__('datetime').timedelta(days=day)).strftime("%Y-%m-%d"),
            "concept": concept
        })
    
    return calendar

def save_content_batch(count: int = 10):
    """Generate and save content batch"""
    output_dir = Path(__file__).parent.parent / "content_generated"
    output_dir.mkdir(exist_ok=True)
    
    batch = []
    for i in range(count):
        concept = generate_video_idea()
        batch.append(concept)
    
    filename = output_dir / f"content_batch_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filename, 'w') as f:
        json.dump(batch, f, indent=2)
    
    print(f"✅ Generated {count} video concepts")
    print(f"📁 Saved to: {filename}")
    
    # Also print first one
    print("\n" + "="*60)
    print("🎬 SAMPLE CONTENT:")
    print("="*60)
    print(f"Hook: {batch[0]['hook']}")
    print(f"Scenes: {len(batch[0]['scenes'])}")
    print(f"Seedance Prompt: {batch[0]['seedance_prompts'][0][:80]}...")
    print(f"Caption: {batch[0]['caption_template'][:100]}")

if __name__ == "__main__":
    print("🚀 TikTok Viral Content Generator\n")
    save_content_batch(10)
    
    print("\n📅 WEEKLY CALENDAR:")
    calendar = generate_daily_content_calendar(7)
    for day in calendar[:3]:
        print(f"\nDay {day['day']} ({day['date']}): {day['concept']['niche'].upper()}")
        print(f"  → {day['concept']['hook'][:60]}...")
