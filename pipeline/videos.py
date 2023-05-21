import re


def get_id(url: str) -> str:
    return re.search(r"(?<=v=)[^&]+", url).group(0)
