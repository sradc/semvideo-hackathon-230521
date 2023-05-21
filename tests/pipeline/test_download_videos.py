from pipeline.download_videos import get_id


def test_get_id():
    url1 = "https://www.youtube.com/watch?v=frYIj2FGmMA&foo=bar"
    url2 = "https://www.youtube.com/watch?v=abcdefg"
    url3 = "https://www.youtube.com/watch?foo=bar&v=xyz123"
    assert get_id(url1) == "frYIj2FGmMA"
    assert get_id(url2) == "abcdefg"
    assert get_id(url3) == "xyz123"
