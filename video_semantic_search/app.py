import numpy as np
import os
from dataclasses import dataclass
from typing import Final

import faiss
import pandas as pd
import streamlit as st


class SemanticSearcher:
    def __init__(self, dataset: pd.DataFrame):
        dim_columns = dataset.filter(regex="^dim_").columns

        self.metadata = dataset.drop(columns=dim_columns)
        self.index = faiss.IndexFlatL2(len(dim_columns))
        self.index.add(dataset[dim_columns].to_numpy(np.float32))
        # TODO: self.embedder = load_embedder()
        self.embedder = lambda _: np.random.rand(1, len(dim_columns))

    def search(self, query: str) -> list["SearchResult"]:
        v = self.embedder(query)
        _, I = self.index.search(v, 10)
        return [
            SearchResult(id=row["id"], second=row["second"])
            for _, row in self.metadata.iloc[I[0]].iterrows()
        ]


DATASET_PATH: Final[str] = os.environ.get("DATASET_PATH", "data/dataset.parquet")
SEARCHER: Final[SemanticSearcher] = SemanticSearcher(pd.read_parquet(DATASET_PATH))


@dataclass
class SearchResult:
    id: str
    second: int


def get_video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def display_search_results(results: list[SearchResult]) -> None:
    col_count = 3  # Number of videos per row

    col_num = 0  # Counter to keep track of the current column
    row = st.empty()  # Placeholder for the current row

    for result in results:
        if col_num == 0:
            row = st.columns(col_count)  # Create a new row of columns

        with row[col_num]:
            # Apply CSS styling to the video container
            st.markdown(
                """
                <style>
                .video-container {
                    position: relative;
                    padding-bottom: 56.25%;
                    padding-top: 30px;
                    height: 0;
                    overflow: hidden;
                }
                .video-container iframe,
                .video-container object,
                .video-container embed {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # Display the embedded YouTube video
            st.video(get_video_url(result.id), start_time=result.second)

        col_num += 1
        if col_num >= col_count:
            col_num = 0


def main():
    st.set_page_config(page_title="video-semantic-search", layout="wide")
    st.header("Video Semantic Search")

    st.text_input("What are you looking for?", key="query")

    query = st.session_state["query"]
    if query:
        display_search_results(
            SEARCHER.search(query)
        )


if __name__ == "__main__":
    main()