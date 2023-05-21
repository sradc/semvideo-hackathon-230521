import re
import subprocess
from pathlib import Path
from typing import List

from tqdm import tqdm

VIDEO_DIR = Path("videos")
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=frYIj2FGmMA"  # buster keaton stunts
]  # hardcode for POC


def get_id(url: str) -> str:
    return re.search(r"(?<=v=)[^&]+", url).group(0)


def download_videos(video_urls: List[str]) -> None:
    VIDEO_DIR.mkdir(exist_ok=True)
    (VIDEO_DIR / ".gitignore").write_text("**")
    for video_url in tqdm(video_urls):
        video_id = get_id(video_url)
        video_path = VIDEO_DIR / f"{video_id}.mp4"
        if video_path.exists():
            print(f"Skipping {video_path} because it already exists")
            continue
        subprocess.run(
            ["yt-dlp", "--quiet", "-f", "133", "-o", str(video_path), video_url]
        )


if __name__ == "__main__":
    assert Path("pipeline").exists(), "Run this from the repo root"
    print("Downloading videos...")
    download_videos(VIDEO_URLS)
