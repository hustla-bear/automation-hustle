#!/usr/bin/env python3
"""YouTube Shorts Content Generator"""
import json
import random
from datetime import datetime
from pathlib import Path

HOOKS = {
    'money': [
        'I made $500 while you were sleeping',
        'POV: Your automation just hit $10K',
        'I quit my 9-5 with this one script',
        'This AI system prints money 24/7',
        'From broke to $50K/month with Python',
    ],
    'controversy': [
        'Unpopular opinion: 9-5s are a trap',
        'Your boss does not want you to see this',
        'Why coding bootcamps are a scam',
        'AI will not replace you, but this might',
        'Stop learning frameworks. Start earning.',
    ],
    'satisfaction': [
        'The most satisfying automation you will see today',
        'This code runs smoother than your morning coffee',
        'POV: You finally fixed that memory leak',
        'ASMR for developers',
        'Clean code hits differently at 3am',
    ],
    'transformation': [
        'Day in the life: 6-figure solo dev',
        'From factory worker to AI automation expert',
        'How I 10x my income in 6 months',
        'POV: You escaped the matrix',
        'This is what freedom looks like',
    ],
    'educational': [
        'Python trick that will save you hours',
        'Stop paying $99/month for this',
        'This automation replaces 5 tools',
        'GPT-4 vs Claude: The real cost breakdown',
        'One-click deployment hack',
    ]
}

RETENTION_HOOKS = [
    'Wait for the end...',
    'This one trick...',
    'Most people do not know...',
    'Stop doing this...',
    'I was today years old...',
    'This changed everything...',
    'POV: You finally learned...',
]

CTR_TITLES = [
    'From $0 to $10K with ONE script',
    'The automation they do not want you to know',
    'Why your code is not making money',
    'This Python trick saves 10 hours/week',
    'I automated my entire income (proof)',
    'Stop learning Python wrong',
    'The $500/hour side hustle',
]

def generate_youtube_content():
    niche = random.choice(list(HOOKS.keys()))
    base_hook = random.choice(HOOKS[niche])
    retention = random.choice(RETENTION_HOOKS)
    ctr = random.choice(CTR_TITLES)
    
    title_options = [
        f"{ctr} #Shorts",
        f"{retention} {base_hook[:40]} #Shorts",
        f"{base_hook[:50]}... #Shorts",
    ]
    
    title = random.choice(title_options)
    
    description = f"""{base_hook}

Learn to build systems that work while you sleep.

Free automation scripts: https://github.com/hustla-bear/automation-hustle
Book custom build: hustlabear@gmail.com

#shorts #automation #python #sidehustle #makemoneyonline #ai
"""
    
    tags = ['automation', 'python', 'side hustle', 'passive income', 'ai', 'make money online', 'shorts', 'viral']
    
    return {
        'platform': 'youtube_shorts',
        'title': title,
        'description': description,
        'tags': tags,
        'niche': niche,
        'hook': base_hook,
        'retention': retention,
        'timestamp': datetime.now().isoformat(),
        'seedance_prompts': [
            f'Cinematic YouTube Short: vertical 9:16, {base_hook}, tech aesthetic, neon highlights, professional',
            f'High-energy short: coding motion, fast cuts, satisfying keyboard typing, productivity vibe',
            f'Transformation ending: {retention}, sunrise lighting, hopeful music, 4K'
        ]
    }

def generate_batch(count=10):
    batch = []
    for i in range(count):
        content = generate_youtube_content()
        content['id'] = i + 1
        batch.append(content)
    return batch

if __name__ == "__main__":
    print("🚀 YouTube Shorts Content Generator")
    print("=" * 60)
    
    output_dir = Path('content_generated')
    output_dir.mkdir(exist_ok=True)
    
    batch = generate_batch(10)
    
    filename = output_dir / f'youtube_batch_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
    with open(filename, 'w') as f:
        json.dump(batch, f, indent=2)
    
    print(f"✅ Generated {len(batch)} YouTube content concepts")
    print(f"📁 Saved to: {filename}")
    print("\n🎬 Sample Videos:")
    print("=" * 60)
    
    for i, video in enumerate(batch[:3], 1):
        print(f"\nVideo {i}:")
        print(f"  Title: {video['title']}")
        print(f"  Niche: {video['niche']}")
        print(f"  Hook: {video['hook'][:50]}...")
