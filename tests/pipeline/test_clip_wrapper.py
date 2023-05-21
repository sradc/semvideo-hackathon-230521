import torch

from pipeline.clip_wrapper import ClipWrapper


def test_ClipWrapper():
    clip_wrapper = ClipWrapper()

    images = [torch.rand(3, 224, 224) for _ in range(2)]
    assert clip_wrapper.images2vec(images).shape[-1] == 512

    texts = ["a photo of a cat", "a photo of a dog"]
    assert clip_wrapper.texts2vec(texts).shape[-1] == 512
