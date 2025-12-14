import numpy as np
import torch
import tqdm
from utils import (
    pad_to_multiple,
    free_gc_decorator,
)
from pathlib import Path


def _extract_embeddings(
    model: torch.nn.Module, data: np.ndarray, patch_size=None, device="cuda"
):
    embeddings = []
    extractor = model.to(device).eval()

    for i in tqdm.tqdm(
        range(data.shape[0]), total=data.shape[0], desc="Extracting embeddings..."
    ):
        d = torch.from_numpy(data[i]).float()
        # Apply instance z-normalization (zero mean, unit variance)
        d = (d - d.mean()) / (d.std() + 1e-8)
        img = d.unsqueeze(0).repeat(3, 1, 1).float().to(device)  # shape: (C, H, W)

        if patch_size is not None:
            img = pad_to_multiple(img, patch_size)

        # Add batch dimension
        img = img.unsqueeze(0)

        with torch.no_grad():
            embedding = extractor(img).squeeze().cpu().numpy()

        embeddings.append(embedding)

    embeddings = np.vstack(embeddings)
    return embeddings


@free_gc_decorator
def _load_or_extract_embeddings(
    model_instantiator_func,
    data: np.ndarray,
    output_file: Path,
    patch_size=None,
    device="cuda",
    save=True,
):
    model = model_instantiator_func()
    if output_file.exists():
        embeddings = np.load(output_file)
        print(f"Loaded embeddings from {output_file}")
    else:
        embeddings = _extract_embeddings(
            model, data, patch_size=patch_size, device=device
        )
        if save:
            np.save(output_file, embeddings)
            print(f"Embeddings saved to {output_file}")
    return embeddings


def load_or_extract_embeddings(
    model_instantiator_func,
    root_path: Path,
    output_file: Path,
    patch_size=None,
    device="cuda",
    save=True,
    direction: str = "inline",
):
    data = np.load(root_path).astype(np.float32)  # Load data as float32

    if direction == "inline":
        data = data.transpose(0, 2, 1)
    elif direction == "crossline":
        data = data.transpose(1, 2, 0)
    else:
        raise ValueError(f"Unknown direction: {direction}")

    # print(f"Original data shape: {data.shape}")
    # print(f"Data type: {data.dtype}")
    # print(f"Data min: {data.min()}, max: {data.max()}")

    return _load_or_extract_embeddings(
        model_instantiator_func=model_instantiator_func,
        data=data,
        output_file=output_file,
        patch_size=patch_size,
        device=device,
        save=save,
    )
