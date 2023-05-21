import numpy as np
import os
from typing import Final

import faiss
import pandas as pd
import streamlit as st

_DEBUG = True


class SemanticSearcher:
    def __init__(self, dataset: pd.DataFrame):
        dim_columns = dataset.filter(regex="^dim_").columns

        self.metadata = dataset.drop(columns=dim_columns)
        self.index = faiss.IndexFlatL2(len(dim_columns))
        self.index.add(dataset[dim_columns].to_numpy(np.float32))
        # TODO: self.embedder = load_embedder()
        self.embedder = lambda _: np.random.rand(1, len(dim_columns))

    def search(self, query: str) -> pd.DataFrame:
        v = self.embedder(query)
        _, I = self.index.search(v, 10)
        return self.metadata.iloc[I[0]]


DATASET_PATH: Final[str] = os.environ.get("DATASET_PATH", "data/dataset.parquet")
SEARCHER: Final[SemanticSearcher] = SemanticSearcher(pd.read_parquet(DATASET_PATH))


def get_video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def main():
    st.set_page_config(page_title="video-semantic-search", layout="wide")
    st.header("Video Semantic Search")

    lc, rc = st.columns(2)
    lc.text_input("What are you looking for?", key="query")

    query = st.session_state["query"]
    if query:
        results = SEARCHER.search(query)
        for i, row in results.iterrows():
            url = get_video_url(row["id"])
            rc.video(url, start_time=row["second"])


if __name__ == "__main__":
    main()
