import re
import subprocess
from pathlib import Path
from typing import List

from tqdm import tqdm

REPO_ROOT = Path(__file__).parents[1].resolve()
DATA_DIR = REPO_ROOT / "data"
VIDEO_DIR = DATA_DIR / "videos"
VIDEO_ID_FOLDER = DATA_DIR / "ids"


def get_id(url: str) -> str:
    return re.search(r"(?<=v=)[^&]+", url).group(0)


def download_videos(video_ids: List[str]) -> None:
    VIDEO_DIR.mkdir(exist_ok=True, parents=True)
    for video_id in tqdm(video_ids):
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_path = VIDEO_DIR / f"{video_id}.mp4"
        if video_path.exists():
            print(f"Skipping {video_path} because it already exists")
            continue
        subprocess.run(
            ["yt-dlp", "--quiet", "-f", "135", "-o", str(video_path), video_url]
        )


if __name__ == "__main__":
    print("Downloading videos...")
    ids = set()
    for file in VIDEO_ID_FOLDER.glob("*.txt"):
        ids.update(
            [x for x in file.read_text().strip().splitlines(keepends=False) if x]
        )
    download_videos(ids)
