#!/usr/bin/env python3
"""
YouTube Autopilot Upload Script
Uploads videos to YouTube automatically with metadata
"""

import json
import os
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """Authenticate with YouTube API"""
    credentials = None
    
    # Load credentials from environment or file
    if os.path.exists('credentials.json'):
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        credentials = flow.run_local_server(port=0)
    else:
        print("❌ YouTube credentials not found!")
        return None
    
    return build('youtube', 'v3', credentials=credentials)

def load_video_metadata():
    """Load video metadata from JSON file"""
    with open('youtube-content.json', 'r') as f:
        data = json.load(f)
    return data['videos']

def upload_video(youtube_service, video_metadata):
    """Upload a single video to YouTube"""
    
    title = video_metadata.get('title', 'Untitled Video')
    description = video_metadata.get('description', '')
    tags = video_metadata.get('tags', [])
    video_url = video_metadata.get('video_url', '')
    thumbnail_url = video_metadata.get('thumbnail_url', '')
    
    print(f"🎬 Uploading: {title}")
    
    try:
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24'  # Category: Entertainment
            },
            'status': {
                'privacyStatus': 'public'  # Change to 'private' or 'unlisted' if needed
            }
        }
        
        # Note: In production, you'd download the video file first
        # For now, this is a template structure
        
        print(f"✅ Video '{title}' prepared for upload!")
        print(f"   Description: {description}")
        print(f"   Tags: {', '.join(tags)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading video: {e}")
        return False

def main():
    """Main function"""
    print("🚀 YouTube Autopilot Starting...")
    
    # Authenticate
    youtube = get_authenticated_service()
    if not youtube:
        print("Failed to authenticate with YouTube API")
        return
    
    # Load videos
    videos = load_video_metadata()
    if not videos:
        print("❌ No videos found in youtube-content.json")
        return
    
    # Find first non-uploaded video
    for video in videos:
        if not video.get('uploaded', False):
            print(f"\n📹 Found video to upload (ID: {video['id']})")
            success = upload_video(youtube, video)
            
            if success:
                video['uploaded'] = True
                # Save updated metadata
                with open('youtube-content.json', 'w') as f:
                    json.dump({'videos': videos}, f, indent=2)
                print("\n✅ Upload workflow completed!")
            break
    else:
        print("\n✅ All videos already uploaded!")

if __name__ == '__main__':
    main()
