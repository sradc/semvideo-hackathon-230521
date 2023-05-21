#!/usr/bin/env bash
set -e

poetry run python pipeline/download_videos.py
poetry run python pipeline/process_videos.py
