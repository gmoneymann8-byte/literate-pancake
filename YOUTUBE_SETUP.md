# YouTube Autopilot Setup Guide

## 🚀 What This Does

This automation uploads a video to your YouTube channel **every day at 9:00 AM UTC**.

## 📋 Setup Instructions

### Step 1: Get YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable **YouTube Data API v3**:
   - Click "Enable APIs and Services"
   - Search "YouTube Data API v3"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Choose "Desktop app"
   - Download as JSON file

### Step 2: Add Credentials to GitHub Secrets

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `YOUTUBE_CREDENTIALS`
4. Value: Copy the entire contents of your downloaded JSON file
5. Click **Add secret**

### Step 3: Prepare Your Videos

Edit `youtube-content.json` with your video information:

```json
{
  "videos": [
    {
      "id": 1,
      "title": "Your Video Title",
      "description": "Your video description",
      "tags": ["tag1", "tag2"],
      "video_url": "https://your-video-url.mp4",
      "thumbnail_url": "https://your-thumbnail-url.jpg",
      "uploaded": false
    }
  ]
}
```

### Step 4: Configure Upload Schedule

Edit `.github/workflows/youtube-autopilot.yml` and change this line:

```yaml
- cron: '0 9 * * *'  # Daily at 9 AM UTC
```

**Cron format:** `minute hour day month day-of-week`

Examples:
- `0 9 * * *` = Every day at 9 AM UTC
- `0 12 * * 1` = Every Monday at 12 PM UTC
- `30 6 * * *` = Every day at 6:30 AM UTC

[Cron timing reference](https://crontab.guru/)

### Step 5: Test It!

1. Go to **Actions** tab
2. Select **YouTube Daily Autopilot Upload**
3. Click **Run workflow**
4. Watch it go! 🎉

## ✨ What Happens

- Workflow triggers on schedule (or manually)
- Reads video metadata from `youtube-content.json`
- Uploads the first non-uploaded video
- Updates the `uploaded` flag to `true`
- Commits changes back to the repo

## 🔧 Customization

### Change Privacy Settings
In `youtube-autopilot.yml`, change `privacyStatus`:
- `'public'` - Everyone can see
- `'unlisted'` - Only people with link
- `'private'` - Only you

### Change Category
In `upload_to_youtube.py`, change `categoryId`:
- `'24'` = Entertainment
- `'25'` = News & Politics
- `'28'` = Science & Technology
- [Full list of category IDs](https://developers.google.com/youtube/v3/docs/videoCategories)

### Multiple Videos Per Day
Edit the Python script to upload multiple videos or adjust the JSON structure.

## ❓ Troubleshooting

- **Credentials error?** Make sure you added the secret correctly
- **Videos not uploading?** Check the Actions tab for error logs
- **Schedule not triggering?** GitHub Actions can have slight delays; manually trigger to test

## 📚 Learn More

- [YouTube API Documentation](https://developers.google.com/youtube)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Syntax Guide](https://crontab.guru/)

---

**Happy uploading! 🎬**
