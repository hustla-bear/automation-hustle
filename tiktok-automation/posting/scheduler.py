#!/usr/bin/env python3
"""
TikTok Posting Scheduler
Manages optimal posting times and content queue
"""
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path

# Optimal posting times (EST timezone research-based)
POSTING_SLOTS = [
    {"time": "07:00", "type": "motivation", "audience": "morning_commuters"},
    {"time": "12:00", "type": "educational", "audience": "lunch_break"},
    {"time": "17:00", "type": "revenue", "audience": "after_work"},
    {"time": "21:00", "type": "transformation", "audience": "evening_relax"},
    {"time": "23:00", "type": "controversial", "audience": "night_owls"},
]

class TikTokScheduler:
    def __init__(self):
        self.queue_file = Path(__file__).parent.parent / "data" / "content_queue.json"
        self.stats_file = Path(__file__).parent.parent / "data" / "post_stats.json"
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
    def load_queue(self):
        """Load content queue"""
        if self.queue_file.exists():
            with open(self.queue_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_queue(self, queue):
        """Save content queue"""
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
    
    def get_next_post(self) -> dict:
        """Get next scheduled post"""
        queue = self.load_queue()
        now = datetime.now()
        
        # Find next slot
        for slot in POSTING_SLOTS:
            hour, minute = map(int, slot["time"].split(":"))
            slot_time = now.replace(hour=hour, minute=minute, second=0)
            
            if slot_time < now:
                # Slot passed, try tomorrow
                slot_time += timedelta(days=1)
            
            # Find matching content
            for content in queue:
                if not content.get("posted") and content.get("type") == slot["type"]:
                    content["scheduled_time"] = slot_time.isoformat()
                    return content
        
        # Fallback: any unposted content
        for content in queue:
            if not content.get("posted"):
                content["scheduled_time"] = (now + timedelta(hours=1)).isoformat()
                return content
        
        return None
    
    def mark_as_posted(self, content_id: str, stats: dict = None):
        """Mark content as posted with stats"""
        queue = self.load_queue()
        
        for content in queue:
            if content.get("id") == content_id:
                content["posted"] = True
                content["posted_at"] = datetime.now().isoformat()
                if stats:
                    content["stats"] = stats
                break
        
        self.save_queue(queue)
    
    def generate_weekly_schedule(self):
        """Generate optimal weekly posting schedule"""
        now = datetime.now()
        schedule = []
        
        for day in range(7):
            date = now + timedelta(days=day)
            
            # Assign 1-2 posts per day based on day
            if date.weekday() < 5:  # Weekdays
                slots = POSTING_SLOTS[:3]  # Morning, lunch, evening
            else:  # Weekends
                slots = POSTING_SLOTS[2:5]  # Afternoon, evening, night
            
            for slot in slots:
                schedule.append({
                    "day": date.strftime("%A %Y-%m-%d"),
                    "time": slot["time"],
                    "type": slot["type"],
                    "audience": slot["audience"],
                    "status": "scheduled"
                })
        
        return schedule
    
    def get_performance_summary(self):
        """Get posting performance stats"""
        queue = self.load_queue()
        
        posted = [c for c in queue if c.get("posted")]
        pending = [c for c in queue if not c.get("posted")]
        
        total_views = sum(c.get("stats", {}).get("views", 0) for c in posted)
        total_likes = sum(c.get("stats", {}).get("likes", 0) for c in posted)
        total_comments = sum(c.get("stats", {}).get("comments", 0) for c in posted)
        
        return {
            "total_scheduled": len(queue),
            "total_posted": len(posted),
            "total_pending": len(pending),
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "avg_engagement": (total_likes + total_comments) / len(posted) if posted else 0
        }

async def scheduler_daemon():
    """Background scheduler process"""
    scheduler = TikTokScheduler()
    
    print("🚀 TikTok Scheduler Started")
    print("="*60)
    
    while True:
        # Check if it's time to post
        next_post = scheduler.get_next_post()
        
        if next_post:
            scheduled_time = datetime.fromisoformat(next_post.get("scheduled_time", "2000-01-01"))
            time_until = (scheduled_time - datetime.now()).total_seconds()
            
            if time_until <= 0:
                print(f"\n⏰ POSTING at {datetime.now().strftime('%H:%M')}")
                print(f"   Type: {next_post.get('type')}")
                print(f"   Hook: {next_post.get('hook', 'Unknown')[:50]}...")
                
                # Here would be actual posting logic
                # For now, just log it
                scheduler.mark_as_posted(next_post.get("id"))
                
            else:
                hours = int(time_until / 3600)
                mins = int((time_until % 3600) / 60)
                print(f"Next post in {hours}h {mins}m")
        
        else:
            print("⚠️  No content in queue")
            print("   Run: python scripts/generate_viral_content.py")
        
        # Sleep and check again every minute
        await asyncio.sleep(60)

if __name__ == "__main__":
    import sys
    
    scheduler = TikTokScheduler()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "schedule":
            print("📅 WEEKLY SCHEDULE:")
            print("="*60)
            for item in scheduler.generate_weekly_schedule()[:10]:
                print(f"{item['day']} {item['time']} - {item['type'].upper()} ({item['audience']})")
        
        elif sys.argv[1] == "stats":
            stats = scheduler.get_performance_summary()
            print("📊 PERFORMANCE STATS:")
            print(json.dumps(stats, indent=2))
        
        elif sys.argv[1] == "next":
            post = scheduler.get_next_post()
            if post:
                print(f"🎬 NEXT POST:")
                print(f"   Time: {post.get('scheduled_time')}")
                print(f"   Type: {post.get('type')}")
                print(f"   Hook: {post.get('hook')}")
            else:
                print("⚠️  No upcoming posts")
    else:
        print("TikTok Scheduler")
        print("Commands:")
        print("  python scheduler.py schedule - Show weekly schedule")
        print("  python scheduler.py stats - Show stats")
        print("  python scheduler.py next - Show next post")
