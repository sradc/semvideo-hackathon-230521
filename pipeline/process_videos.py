import cv2
import pandas as pd
from PIL import Image
from tqdm import tqdm

from pipeline.clip_wrapper import MODEL_DIM, ClipWrapper
from pipeline.download_videos import DATA_DIR, REPO_ROOT, VIDEO_DIR

FRAME_EXTRACT_RATE_SECONDS = 5  # Extract a frame every 5 seconds
IMAGES_DIR = DATA_DIR / "images"
DATAFRAME_PATH = DATA_DIR / "dataset.parquet"


def process_videos() -> None:
    "Runs clip on video frames, saves results to a parquet file"
    clip_wrapper = ClipWrapper()
    results = []
    for video_path in tqdm(list(VIDEO_DIR.glob("*.mp4")), desc="Processing videos"):
        video_id = video_path.stem
        extracted_images_dir = IMAGES_DIR / video_id
        extracted_images_dir.mkdir(exist_ok=True, parents=True)
        complete_file = extracted_images_dir / "complete"
        if complete_file.exists():
            continue
        for clip_vector, image, timestamp_secs, frame_idx in get_clip_vectors(
            video_path, clip_wrapper
        ):
            image_path = extracted_images_dir / f"{frame_idx}.jpg"
            image.save(image_path)
            results.append(
                [
                    video_id,
                    frame_idx,
                    timestamp_secs,
                    str(image_path.relative_to(REPO_ROOT)),
                    *clip_vector,
                ]
            )
        complete_file.touch()
    df = pd.DataFrame(
        results,
        columns=["video_id", "frame_idx", "timestamp", "image_path"]
        + [f"dim_{i}" for i in range(MODEL_DIM)],
    )
    print(f"Saving data to {DATAFRAME_PATH}")
    df.to_parquet(DATAFRAME_PATH, index=False)


def get_clip_vectors(video_path, clip_wrapper):
    cap = cv2.VideoCapture(str(video_path))
    num_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    extract_every_n_frames = FRAME_EXTRACT_RATE_SECONDS * fps
    for frame_idx in tqdm(range(num_video_frames), desc="Running CLIP on video"):
        ret, frame = cap.read()
        if frame_idx % extract_every_n_frames != 0:
            continue
        image = Image.fromarray(frame[..., ::-1])
        clip_vector = clip_wrapper.images2vec([image]).squeeze().numpy()
        timestamp_secs = frame_idx / fps
        yield clip_vector, image, timestamp_secs, frame_idx
    cap.release()


if __name__ == "__main__":
    process_videos()
