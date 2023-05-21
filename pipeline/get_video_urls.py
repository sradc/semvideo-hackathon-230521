import os
import hashlib
from pathlib import Path
from typing import Final, Optional

import youtube_dl

PLAYLIST_URL: Final[Optional[str]] = os.environ.get("PLAYLIST_URL")
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
        'ignoreerrors': True,
        'extract_flat': 'in_playlist',
        'dump_single_json': True,
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(channel_url, download=False)
        video_ids = [video['id'] for video in playlist_info['entries'] if 'id' in video]

    return video_ids


def main():
    assert PLAYLIST_URL is not None, "PLAYLIST_URL environment variable not set"
    ids = get_all_video_ids(PLAYLIST_URL)

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    output = "\n".join(
            f"https://www.youtube.com/watch?v={video_id}"
            for video_id in ids
        )
    output_path = output_dir / f"{hashlib.md5(output.encode()).hexdigest()}.txt"
    with output_path.open(mode="w") as f:
        f.write(output)


if __name__ == "__main__":
    main()
