#!/usr/bin/env python3
"""
YouTube Shorts Scheduler - Automated Publishing
Optimal timing for maximum reach
"""
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import List, Dict

# Optimal posting times for YouTube Shorts (EST)
# Based on analytics data for automation/personal development niches
POSTING_SLOTS = [
    {"time": "05:00", "type": "morning_motivation", "audience": "early_commuters", "reason": "EU market wakes up, US early birds"},
    {"time": "12:00", "type": "lunch_educational", "audience": "lunch_break", "reason": "Peak mobile scrolling time"},
    {"time": "17:00", "type": "after_work", "audience": "post_work", "reason": "Commute/home browsing peak"},
    {"time": "21:00", "type": "evening_transformation", "audience": "evening_relax", "reason": "Wind-down content consumption"},
    {"time": "23:00", "type": "late_night", "audience": "night_owls", "reason": "High engagement, low competition"},
]

class YouTubeScheduler:
    def __init__(self):
        self.queue_file = Path(__file__).parent / "data" / "upload_queue.json"
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
    
    def load_queue(self) -> List[Dict]:
        """Load pending uploads"""
        if self.queue_file.exists():
            with open(self.queue_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_queue(self, queue: List[Dict]):
        """Save upload queue"""
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
    
    def get_next_upload(self) -> Dict:
        """Get next item to upload"""
        queue = self.load_queue()
        
        # Find first unposted item
        for item in queue:
            if not item.get('posted', False):
                # Find optimal slot
                next_slot = self.find_optimal_slot()
                item['scheduled_time'] = next_slot['time']
                return item
        
        return None
    
    def find_optimal_slot(self) -> Dict:
        """Find next optimal time slot"""
        now = datetime.now()
        current_hour = now.hour
        
        # Find next available slot
        for slot in POSTING_SLOTS:
            slot_hour, slot_min = map(int, slot['time'].split(':'))
            
            if slot_hour > current_hour:
                # This slot is available today
                return slot
        
        # If passed all slots, return first slot for tomorrow
        return POSTING_SLOTS[0]
    
    def generate_daily_schedule(self) -> List[Dict]:
        """Generate optimal posting schedule"""
        now = datetime.now()
        schedule = []
        
        for day_offset in range(7):
            date = now + timedelta(days=day_offset)
            
            # Use all slots on weekends, fewer on weekdays
            if date.weekday() >= 5:  # Weekend
                slots = POSTING_SLOTS  # All 5 slots
            else:  # Weekday
                slots = [POSTING_SLOTS[1], POSTING_SLOTS[2], POSTING_SLOTS[3]]  # Lunch, after-work, evening
            
            for slot in slots:
                schedule.append({
                    "day": date.strftime("%A %Y-%m-%d"),
                    "time": slot["time"],
                    "type": slot["type"],
                    "audience": slot["audience"],
                    "reason": slot["reason"],
                    "status": "available"
                })
        
        return schedule
    
    def mark_as_posted(self, video_id: str, video_url: str = None):
        """Mark item as posted"""
        queue = self.load_queue()
        
        for item in queue:
            if item.get('video_path') == video_id or item.get('title') == video_id:
                item['posted'] = True
                item['posted_at'] = datetime.now().isoformat()
                if video_url:
                    item['url'] = video_url
                item['status'] = 'published'
                break
        
        self.save_queue(queue)
    
    def add_to_queue(self, content: Dict):
        """Add new content to queue"""
        queue = self.load_queue()
        
        # Generate unique ID
        content['id'] = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        content['added'] = datetime.now().isoformat()
        content['posted'] = False
        content['status'] = 'pending'
        
        queue.append(content)
        self.save_queue(queue)
        
        print(f"✓ Added to queue: {content['title'][:50]}...")
        return content['id']
    
    def get_stats(self) -> Dict:
        """Get queue statistics"""
        queue = self.load_queue()
        
        return {
            "total_videos": len(queue),
            "posted": sum(1 for q in queue if q.get('posted')),
            "pending": sum(1 for q in queue if not q.get('posted')),
            "next_upload": self.get_next_upload()['title'][:50] if self.get_next_upload() else "None"
        }


def main():
    """CLI for scheduler"""
    import sys
    
    scheduler = YouTubeScheduler()
    
    if len(sys.argv) < 2:
        print("YouTube Shorts Scheduler")
        print("\nUsage:")
        print("  python scheduler.py stats       - Show queue stats")
        print("  python scheduler.py schedule    - Show weekly schedule")
        print("  python scheduler.py next          - Show next upload")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "stats":
        stats = scheduler.get_stats()
        print("📊 Upload Queue Stats:")
        print(f"  Total:    {stats['total_videos']}")
        print(f"  Posted:   {stats['posted']}")
        print(f"  Pending:  {stats['pending']}")
        print(f"  Next:     {stats['next_upload']}")
    
    elif command == "schedule":
        schedule = scheduler.generate_daily_schedule()
        print("📅 Weekly Upload Schedule:")
        print("=" * 60)
        
        current_day = ""
        for item in schedule[:15]:  # Show 15 slots
            if item['day'] != current_day:
                print(f"\n{item['day']}:")
                current_day = item['day']
            
            print(f"  {item['time']} - {item['type'].replace('_', ' ').title()}")
            print(f"    ({item['reason']})")
    
    elif command == "next":
        next_up = scheduler.get_next_upload()
        if next_up:
            print("🎬 Next Upload:")
            print(f"  Title: {next_up['title']}")
            print(f"  Type:  {next_up.get('type', 'unknown')}")
            print(f"  Added: {next_up.get('added', 'unknown')}")
        else:
            print("⚠️  No videos in queue")
            print("    Run: generate_content.py to create videos")


if __name__ == "__main__":
    main()
