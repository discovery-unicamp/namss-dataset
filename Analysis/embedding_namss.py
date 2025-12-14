from imageio import imread
import numpy as np
import torch
import tqdm
from utils import (
    pad_to_multiple,
    free_gc_decorator,
)
from pathlib import Path


def load_data(fname):
    img = imread(fname)
    img = np.asarray(img)
    img = torch.from_numpy(img)
    img = img.unsqueeze(0).repeat(3, 1, 1).float()  # Convert to 3 channels
    return img


def _extract_embeddings(model, root_path, patch_size=None, device="cuda"):
    embeddings = []
    extractor = model.to(device).eval()
    files = list(sorted(Path(root_path).rglob("*.tiff")))

    for i, fname in enumerate(
        tqdm.tqdm(files, total=len(files), desc="Extracting embeddings...")
    ):
        img = load_data(fname).to(device)  # shape: (C, H, W)
        img = (img - img.mean()) / (img.std() + 1e-8)

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
def load_or_extract_embeddings(
    model_instantiator_func,
    root_path: Path,
    output_file: Path,
    patch_size=None,
    device="cuda",
    save=True,
    direction=None, # Unused for NAMSS
):
    model = model_instantiator_func()
    if output_file.exists():
        embeddings = np.load(output_file)
        print(f"Loaded embeddings from {output_file}")
    else:
        print(f"Extracting embeddings...")
        embeddings = _extract_embeddings(
            model, root_path, patch_size=patch_size, device=device
        )
        if save:
            np.save(output_file, embeddings)
            print(f"Embeddings saved to {output_file}")
    return embeddings

