import logging
import os
import hashlib
from pathlib import Path
from typing import Final, Optional

import youtube_dl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

URL_FILE: Final[Optional[str]] = os.environ.get("URL_FILE")
OUTPUT_DIR: Final[str] = os.environ.get("OUTPUT_DIR", "data/ids")


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
        'ignoreerrors': True,
        'extract_flat': 'in_playlist',
        'dump_single_json': True,
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(channel_url, download=False)
        video_ids = [video['id'] for video in playlist_info['entries'] if 'id' in video]

    return video_ids


def process_youtube_url(url: str):
    logging.info(f"Processing {url}")
    ids = get_all_video_ids(url)

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    output = "\n".join(ids)
    output_path = output_dir / f"{hashlib.md5(output.encode()).hexdigest()}.txt"
    logging.info(f"Writing {len(ids)} video IDs to {output_path}")
    with output_path.open(mode="w") as f:
        f.write(output)


def main():
    assert URL_FILE is not None, "URL_FILE environment variable must be set."
    with open(URL_FILE, "r") as f:
        logging.info(f"Reading URLs from {URL_FILE}")
        urls = f.readlines()

    logging.info(f"Processing {len(urls)} URLs")
    for url in urls:
        process_youtube_url(url)


if __name__ == "__main__":
    main()
