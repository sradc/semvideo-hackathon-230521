import hashlib
import logging
import os
from pathlib import Path
from typing import Final, Optional

import youtube_dl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

PLAYLIST_URLS = [
    "https://www.youtube.com/playlist?list=PL6Lt9p1lIRZ311J9ZHuzkR5A3xesae2pk",  # 570, Alternative rock of the 2000s (2000-2009)
    "https://www.youtube.com/playlist?list=PLMC9KNkIncKtGvr2kFRuXBVmBev6cAJ2u",  # 250, Best Pop Music Videos - Top Pop Hits Playlist
    "https://www.youtube.com/playlist?list=PLmXxqSJJq-yXrCPGIT2gn8b34JjOrl4Xf",  #  184, 80s Music Hits | Best 80s Music Playlist
    "https://www.youtube.com/playlist?list=PL7DA3D097D6FDBC02",  #  150, 90's Hits - Greatest 1990's Music Hits (Best 90’s Songs Playlist)
    "https://www.youtube.com/playlist?list=PLeDakahyfrO-4kuBioL5ZAoy4j6aCnzWy",  # 100, Best Music Videos of All Time
    "https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj",  #  200, Pop Music Playlist - Timeless Pop Songs (Updated Weekly 2023)
    "https://www.youtube.com/playlist?list=PLkqz3S84Tw-RfPS9HHi3MRmrinOBKxIr8",  # 82, Top POP Hits 2022 – Biggest Pop Music Videos - Vevo
    "https://www.youtube.com/playlist?list=PLyORnIW1xT6wqvszJbCdLdSjylYMf3sNZ",  # 100, Top 100 Music Videos 2023 - Best Music Videos 2023
    "https://www.youtube.com/playlist?list=PL1Mmsa-U48mea1oIN-Eus78giJANx4D9W",  # 119, 90s Music Videos
    "https://www.youtube.com/playlist?list=PLurPBtLcqJqcg3r-HOhR3LZ0aDxpI15Fa",  # 100, 100 Best Music Videos Of The Decade: 2010 - 2019
    "https://www.youtube.com/playlist?list=PLCQCtoOJpI_A5oktQImEdDBJ50BqHXujj",  # 495, MTV Classic 2000's music videos (US Version)
]
URL_FILE: Final[Optional[str]] = os.environ.get("URL_FILE")
OUTPUT_DIR: Final[str] = os.environ.get("OUTPUT_DIR", "data/url")


def get_all_video_ids(channel_url: str) -> list[str]:
    """Get all video IDs from a YouTube channel or playlist URL.

    Args:
        channel_url (str): URL of the YouTube channel or playlist.

    Returns:
        list[str]: List of video IDs.

    Notes:
        If you want the videos from a channel, make sure to pass the `/videos` endpoint of the channel.
    """
    ydl_opts = {
        "ignoreerrors": True,
        "extract_flat": "in_playlist",
        "dump_single_json": True,
        "quiet": True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(channel_url, download=False)
        video_ids = [video["id"] for video in playlist_info["entries"] if "id" in video]

    return video_ids


def process_youtube_url(url: str):
    logging.info(f"Processing {url}")
    ids = get_all_video_ids(url)

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    output = "\n".join(
        f"https://www.youtube.com/watch?v={video_id}" for video_id in ids
    )
    output_path = output_dir / f"{hashlib.md5(output.encode()).hexdigest()}.txt"
    logging.info(f"Writing {len(ids)} video IDs to {output_path}")
    with output_path.open(mode="w") as f:
        f.write(output)


def main():
    logging.info(f"Processing {len(PLAYLIST_URLS)} URLs")
    for url in PLAYLIST_URLS:
        process_youtube_url(url)


if __name__ == "__main__":
    main()
