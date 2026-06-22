"""
Daten: YouTube Data API Sammler (Beispiel)

Holt Channel-Statistiken und Performance der letzten Videos aus YouTube.
Diese Datei nach scripts/collect_youtube.py kopieren und auf deinen Channel anpassen.

Voraussetzungen:
    YOUTUBE_API_KEY     : holen unter console.cloud.google.com/apis/credentials
    YOUTUBE_CHANNEL_ID  : finden unter youtube.com/account_advanced

Erzeugte Tabellen: youtube_daily, youtube_videos
Zusätzliches pip: google-api-python-client google-auth
"""

import os
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

try:
    from googleapiclient.discovery import build
except ImportError:
    raise ImportError(
        "Paket 'google-api-python-client' fehlt, installier es mit: pip install google-api-python-client google-auth"
    )


def collect():
    """YouTube Channel- und Video-Daten holen."""
    api_key = os.getenv("YOUTUBE_API_KEY", "").strip()
    channel_id = os.getenv("YOUTUBE_CHANNEL_ID", "").strip()

    if not api_key:
        return {
            "source": "youtube", "status": "skipped",
            "reason": "YOUTUBE_API_KEY fehlt, trag ihn in die .env ein "
                      "(holen unter console.cloud.google.com/apis/credentials)"
        }
    if not channel_id:
        return {
            "source": "youtube", "status": "skipped",
            "reason": "YOUTUBE_CHANNEL_ID fehlt, finden unter youtube.com/account_advanced"
        }

    try:
        youtube = build("youtube", "v3", developerKey=api_key)

        # Channel-Statistiken
        channel_resp = youtube.channels().list(
            part="statistics,snippet", id=channel_id
        ).execute()

        if not channel_resp.get("items"):
            return {
                "source": "youtube", "status": "error",
                "reason": f"Channel {channel_id} nicht gefunden"
            }

        stats = channel_resp["items"][0]["statistics"]
        snippet = channel_resp["items"][0]["snippet"]

        channel_data = {
            "channel_name": snippet.get("title", ""),
            "subscribers": int(stats.get("subscriberCount", 0)),
            "total_views": int(stats.get("viewCount", 0)),
            "total_videos": int(stats.get("videoCount", 0)),
        }

        # Letzte Videos (30 Tage)
        thirty_days_ago = (
            datetime.now(timezone.utc) - timedelta(days=30)
        ).isoformat()

        search_resp = youtube.search().list(
            part="id", channelId=channel_id, type="video",
            publishedAfter=thirty_days_ago, order="date", maxResults=50
        ).execute()

        video_ids = [
            item["id"]["videoId"]
            for item in search_resp.get("items", [])
            if "videoId" in item.get("id", {})
        ]

        videos = []
        total_views_30d = 0

        # Video-Details in Blöcken von 50 holen
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i + 50]
            vid_resp = youtube.videos().list(
                part="statistics,snippet,contentDetails",
                id=",".join(batch)
            ).execute()

            for item in vid_resp.get("items", []):
                vid_stats = item.get("statistics", {})
                views = int(vid_stats.get("viewCount", 0))
                total_views_30d += views
                videos.append({
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "published": item["snippet"]["publishedAt"][:10],
                    "views": views,
                    "likes": int(vid_stats.get("likeCount", 0)),
                    "comments": int(vid_stats.get("commentCount", 0)),
                    "duration": item.get("contentDetails", {}).get("duration", ""),
                })

        return {
            "source": "youtube",
            "status": "success",
            "data": {
                "channel": channel_data,
                "videos_30d": videos,
                "total_views_30d": total_views_30d,
                "videos_published_30d": len(videos),
            }
        }

    except Exception as e:
        return {"source": "youtube", "status": "error", "reason": str(e)}


def write(conn, result, date):
    """YouTube-Daten in die Datenbank schreiben. Gibt Anzahl der Datensätze zurück."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS youtube_daily (
            date TEXT PRIMARY KEY,
            subscribers INTEGER,
            total_views INTEGER,
            total_videos INTEGER,
            views_30d INTEGER,
            videos_published_30d INTEGER,
            collected_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS youtube_videos (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            published_date TEXT,
            views INTEGER,
            likes INTEGER,
            comments INTEGER,
            duration TEXT,
            last_updated TEXT
        )
    """)

    if result.get("status") != "success":
        conn.commit()
        return 0

    data = result["data"]
    channel = data["channel"]
    collected_at = datetime.now(timezone.utc).isoformat()
    records = 0

    # Tagesstand des Channels
    conn.execute(
        "INSERT OR REPLACE INTO youtube_daily "
        "(date, subscribers, total_views, total_videos, views_30d, "
        "videos_published_30d, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (date, channel["subscribers"], channel["total_views"],
         channel["total_videos"], data["total_views_30d"],
         data["videos_published_30d"], collected_at)
    )
    records += 1

    # Video-Datensätze
    for video in data.get("videos_30d", []):
        conn.execute(
            "INSERT OR REPLACE INTO youtube_videos "
            "(video_id, title, published_date, views, likes, comments, "
            "duration, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (video["video_id"], video["title"], video["published"],
             video["views"], video["likes"], video["comments"],
             video["duration"], date)
        )
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        ch = result["data"]["channel"]
        print(f"Channel: {ch['channel_name']}")
        print(f"Abonnenten: {ch['subscribers']:,}")
        print(f"Videos (30 Tage): {result['data']['videos_published_30d']}")
        print(f"Aufrufe (30 Tage): {result['data']['total_views_30d']:,}")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")
