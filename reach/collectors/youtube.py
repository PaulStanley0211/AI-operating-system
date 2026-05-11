# youtube.py — v1.0.0
# Collects YouTube channel stats and recent video performance via YouTube Data API v3.

import sys
import json
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID, DB_PATH
from db import get_conn

from googleapiclient.discovery import build


def collect():
    if not YOUTUBE_API_KEY or not YOUTUBE_CHANNEL_ID:
        print("YouTube: skipping — YOUTUBE_API_KEY or YOUTUBE_CHANNEL_ID not set")
        return

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    today = date.today().isoformat()

    # Channel stats
    resp = youtube.channels().list(
        part="statistics",
        id=YOUTUBE_CHANNEL_ID
    ).execute()

    if not resp.get("items"):
        print("YouTube: channel not found — check YOUTUBE_CHANNEL_ID")
        return

    stats = resp["items"][0]["statistics"]
    subscribers = int(stats.get("subscriberCount", 0))
    total_views = int(stats.get("viewCount", 0))
    video_count = int(stats.get("videoCount", 0))

    # Recent videos (last 30 days)
    cutoff = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    search_resp = youtube.search().list(
        part="id",
        channelId=YOUTUBE_CHANNEL_ID,
        type="video",
        publishedAfter=cutoff,
        maxResults=50,
        order="date"
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_resp.get("items", [])]
    views_30d = 0
    video_rows = []

    if video_ids:
        videos_resp = youtube.videos().list(
            part="statistics,snippet",
            id=",".join(video_ids)
        ).execute()

        for v in videos_resp.get("items", []):
            vstats = v.get("statistics", {})
            views = int(vstats.get("viewCount", 0))
            views_30d += views
            video_rows.append({
                "video_id": v["id"],
                "date": today,
                "title": v["snippet"]["title"][:200],
                "views": views,
                "likes": int(vstats.get("likeCount", 0)),
                "comments": int(vstats.get("commentCount", 0)),
                "published_at": v["snippet"]["publishedAt"],
            })

    # Write to DB
    conn = get_conn(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT OR REPLACE INTO youtube_daily (date, subscribers, total_views, video_count, views_30d)
        VALUES (?, ?, ?, ?, ?)
    """, (today, subscribers, total_views, video_count, views_30d))

    for row in video_rows:
        c.execute("""
            INSERT OR REPLACE INTO youtube_videos
            (video_id, date, title, views, likes, comments, published_at)
            VALUES (:video_id, :date, :title, :views, :likes, :comments, :published_at)
        """, row)

    conn.commit()
    conn.close()

    print(f"YouTube: {subscribers:,} subscribers | {views_30d:,} views (30d) | {len(video_rows)} videos")


if __name__ == "__main__":
    collect()
