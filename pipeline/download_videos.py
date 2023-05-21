import re
import subprocess
from pathlib import Path
from typing import List

from tqdm import tqdm

REPO_ROOT = Path(__file__).parents[1].resolve()
DATA_DIR = REPO_ROOT / "data"
VIDEO_DIR = DATA_DIR / "videos"
VIDEO_IDS = [
    "frYIj2FGmMA",  # "Some of Buster Keaton's most amazing stunts"
    "1wkPMUZ9vX4",  # "Nature Makes You Happy | BBC Earth"
    "dGghkjpNCQ8",  # "Calvin Harris - Feel So Close (Official Video)"
    "p9_BsjMi4bM",  # "Nothing But Thieves - Sorry (Official Video)"
    "a0q6JMuLBYQ",  # "Conan Gray - Never Ending Song (Official Music Video)"
    # Taken from pop music playlist:
    "uqVHr8UYHJw",
    "b7QlX3yR2xs",
    "XXYlFuWEuKI",
    "RsEZmictANA",
    "l0U7SxXHkPY",
    "BSzSn-PRdtI",
    "TUVcZfQe-Kw",
    "6swmTBVI83k",
    "ssq6X6alZ3w",
    "r4P-WOOUPk4",
    "GQAOrCOknCY",
    "tQ0yjYUFKAE",
    "vMLk_T0PPbk",
    "RUQl6YcMalg",
    "3jo8E95fDqA",
    "0EVVKs6DQLo",
    "qrTiyVEW8gc",
    "SsdkvYdSzlg",
    "w8mBplMtwJ8",
    "uWRlisQu4fo",
    "ZmDBbnmKpqQ",
    "L0X03zR0rQk",
    "0ir1qkPXPVM",
    "9hbu9toStfc",
    "U6n2NcJ7rLc",
    "LQtkl3auvv8",
    "G6XthQpk8uk",
    "rCiBgLOcuKU",
    "JOHN4EnFqAU",
    "AoAm4om0wTs",
    "K-a8s8OLBSE",
    "Pkh8UtuejGw",
    "q0hyYWKXF0Q",
    "FFzH_9guHQM",
    "3CxtK7-XtE0",
    "ao4giEvkV0U",
    "rPgaYeq9NvI",
    "10ZxWboO5gM",
    "gQG_2O9Bu6c",
    "kvVyKycCE4I",
    "T-578RNysss",
    "FX-ZYNlC8fg",
    "MPbUaIZAaeA",
    "tcYodQoapMg",
    "lnWhiNodnX0",
    "JFm7YDVlqnI",
    "jr47YisIsz8",
    "zlJDTxahav0",
    "LWeiydKl0mU",
    "2p3zZoraK9g",
    "Bo5hepNudl0",
    "jJdlgKzVsnI",
    "Jtauh8GcxBY",
    "BjhW3vBA1QU",
    "AG-erEMhumc",
    "SlPhMPnQ58k",
    "JR49dyo-y0E",
    "e7HBypw4lhY",
    "B2SK_jb68dk",
    "lPckvzufS90",
    "FKXSh14svlQ",
    "E07s5ZYygMg",
    "4NRXx6U8ABQ",
    "IKKbboquS9s",
    "jIoEaTN7GGo",
    "0tn6nWYNK3Q",
    "aS1no1myeTM",
    "DyDfgMOUjCI",
    "cii6ruuycQA",
    "9vMLTcftlyI",
    "CnAmeh0-E-U",
    "FpOmSDJ-fLk",
    "xWggTb45brM",
    "aAiVsqfbn5g",
    "KIK3azN4w34",
    "ApXoWvfEYVU",
    "8nBFqZppIF0",
    "WXBHCQYxwr0",
    "h5WN3pkxPF0",
    "P00HMxdsVZI",
    "Dm9Zf1WYQ_A",
    "pok8H_KF1FA",
]


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
            ["yt-dlp", "--quiet", "-f", "133", "-o", str(video_path), video_url]
        )


if __name__ == "__main__":
    print("Downloading videos...")
    download_videos(VIDEO_IDS)
