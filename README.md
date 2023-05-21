# semvideo-hackathon-230521

## Project Description

This project let's you search YouTube videos using a text string. The search is done over the actual video frames,
rather than any associated text. The search results are displayed as a list of videos, with the most relevant video
shown first. The user can then click on any of the videos to play it.

## Quick Start

Run the following commands to get started:

```bash
git clone https://github.com/sradc/semvideo-hackathon-230521.git
cd semvideo-hackathon-230521
poetry install
PYTHONPATH=. poetry run streamlit run video_semantic_search/app.py
```

If you do not have `poetry` installed, refer to the [poetry documentation](https://python-poetry.org/docs/#installation).
