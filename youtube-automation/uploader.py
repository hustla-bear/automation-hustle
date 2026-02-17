#!/usr/bin/env python3
"""
YouTube Shorts Uploader - Full Automation
Handles authentication, metadata, and upload via YouTube Data API v3
"""
import os
import sys
import json
import pickle
from datetime import datetime
from pathlib import Path

# Google API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("⚠️  Installing Google API dependencies...")
    os.system("pip3 install --user google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    print("✓ Dependencies installed. Restart script.")
    sys.exit(0)

# Configuration
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = Path(__file__).parent / 'client_secret.json'
TOKEN_FILE = Path(__file__).parent / 'token.pickle'

class YouTubeUploader:
    def __init__(self):
        self.credentials = None
        self.youtube = None
        self.authenticated = False
        
    def authenticate(self):
        """Authenticate with YouTube API"""
        # Load existing token
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # If no valid credentials, get them
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print("🔄 Refreshing token...")
                self.credentials.refresh(Request())
            else:
                if not CLIENT_SECRETS_FILE.exists():
                    print(f"❌ Missing {CLIENT_SECRETS_FILE}")
                    print("   Get it from: https://console.cloud.google.com/")
                    print("   Enable YouTube Data API v3 → Create OAuth 2.0 credentials → Download JSON")
                    return False
                
                print("🔐 Starting OAuth flow...")
                print("   A browser will open for authentication")
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRETS_FILE, SCOPES)
                self.credentials = flow.run_local_server(port=0)
            
            # Save token
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(self.credentials, token)
            print("✓ Token saved for future uploads")
        
        self.youtube = build('youtube', 'v3', credentials=self.credentials)
        self.authenticated = True
        return True
    
    def upload_short(self, video_path: str, metadata: dict) -> dict:
        """Upload a YouTube Short"""
        if not self.authenticated:
            print("❌ Not authenticated. Run authenticate() first.")
            return None
        
        # Validate video
        if not os.path.exists(video_path):
            print(f"❌ Video not found: {video_path}")
            return None
        
        # Build request body
        body = {
            'snippet': {
                'title': metadata.get('title', 'Automation Short'),
                'description': metadata.get('description', ''),
                'tags': metadata.get('tags', ['automation', 'python', 'ai']),
                'categoryId': metadata.get('category_id', '27')  # Education
            },
            'status': {
                'privacyStatus': metadata.get('privacy', 'public'),
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Handle shorts-specific tags
        if '#shorts' not in body['snippet']['title']:
            body['snippet']['title'] += ' #Shorts'
        
        # Upload
        print(f"📤 Uploading: {os.path.basename(video_path)}")
        print(f"   Title: {body['snippet']['title'][:50]}...")
        
        try:
            media = MediaFileUpload(
                video_path,
                mimetype='video/mp4',
                resumable=True
            )
            
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"   Progress: {int(status.progress() * 100)}%")
            
            print(f"✓ Upload complete!")
            print(f"   Video ID: {response['id']}")
            print(f"   URL: https://youtube.com/shorts/{response['id']}")
            
            return response
            
        except HttpError as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def upload_from_generated(self, content_file: str, video_file: str = None):
        """Upload using generated content JSON"""
        # Load content
        with open(content_file, 'r') as f:
            content = json.load(f)
        
        # Find video if not specified
        if video_file is None:
            content_dir = Path(content_file).parent
            video_files = list(content_dir.glob('*.mp4'))
            if video_files:
                video_file = str(video_files[0])
            else:
                print("❌ No video file found")
                return None
        
        # Build metadata
        metadata = {
            'title': content['hook'][:60] if len(content['hook']) <= 60 else content['hook'][:57] + '...',
            'description': f"{content['hook']}\n\n{content['caption_template']}\n\n#automation #python #ai #sidehustle",
            'tags': content['hashtags'] + ['automation', 'ai', 'python'],
            'privacy': 'public'
        }
        
        return self.upload_short(video_file, metadata)


def main():
    """CLI for testing uploads"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Upload YouTube Shorts')
    parser.add_argument('--video', '-v', help='Video file path')
    parser.add_argument('--metadata', '-m', help='Metadata JSON file')
    parser.add_argument('--title', '-t', help='Video title')
    parser.add_argument('--description', '-d', help='Video description')
    parser.add_argument('--auth-only', action='store_true', help='Just authenticate')
    
    args = parser.parse_args()
    
    uploader = YouTubeUploader()
    
    # Authenticate
    if not uploader.authenticate():
        print("❌ Authentication failed")
        sys.exit(1)
    
    if args.auth_only:
        print("✓ Authentication successful")
        return
    
    # Upload with metadata file
    if args.metadata:
        result = uploader.upload_from_generated(args.metadata, args.video)
        if result:
            print(f"\n🎉 Success! Video live at: https://youtube.com/shorts/{result['id']}")
        sys.exit(0 if result else 1)
    
    # Upload with manual metadata
    if args.video:
        metadata = {
            'title': args.title or 'Automation Short',
            'description': args.description or 'Built with Python automation',
            'tags': ['automation', 'python', 'ai'],
            'privacy': 'public'
        }
        result = uploader.upload_short(args.video, metadata)
        if result:
            print(f"\n🎉 Success! Video live at: https://youtube.com/shorts/{result['id']}")
        sys.exit(0 if result else 1)
    
    print("❌ No video specified")
    print("Usage:")
    print("  python uploader.py --auth-only                    # Test auth")
    print("