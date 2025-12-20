import numpy as np
import pandas as pd
from pathlib import Path
from embedding_namss import load_or_extract_embeddings as load_or_extract_embeddings_namss
from embedding_f3 import load_or_extract_embeddings as load_or_extract_embeddings_f3
from embedding_seamai import load_or_extract_embeddings as load_or_extract_embeddings_seamai
from umap import UMAP
from utils import (
    model_resnet50_coco,
    model_dinov2_vitb14,
)
import plotly.express as px
from plotly.subplots import make_subplots
import gc

UMAP_FIGURES_PATH = Path("figures/umap")

NAMSS_DATA_PATH = Path("../Data/unicamp-namss-dataset")
# F3 Netherlands block from Aludah. Download link: https://zenodo.org/record/3755060/files/raw.zip
F3_DATA_PATH = Path("Other_Data/F3/seismic_entire_volume.npy")
# AIcrowd SEAM AI dataset. Download link: https://www.aicrowd.com/challenges/seismic-facies-identification-challenge
SEAM_AI_DATA_PATH = "Other_Data/SEAM-AI/data_train.npy"

embedding_configs = {
    ## ResNet50 COCO embeddings
    "resnet50_coco": {
        "NAMSS": {
            "load_func": load_or_extract_embeddings_namss,
            "model_instantiator_func": model_resnet50_coco,
            "root_path": NAMSS_DATA_PATH,
            "output_file": Path("resnet50_coco_embeddings_namss.npy"),
            "patch_size": None,
            "direction": None,
        },
        "F3 (inline)": {
            "load_func": load_or_extract_embeddings_f3,
            "model_instantiator_func": model_resnet50_coco,
            "root_path": F3_DATA_PATH,
            "output_file": Path("resnet50_coco_embeddings_f3_inline.npy"),
            "patch_size": None,
            "direction": "inline",
        },
        "F3 (crossline)": {
            "load_func": load_or_extract_embeddings_f3,
            "model_instantiator_func": model_resnet50_coco,
            "root_path": F3_DATA_PATH,
            "output_file": Path("resnet50_coco_embeddings_f3_crossline.npy"),
            "patch_size": None,
            "direction": "crossline",
        },
        "SEAM AI (inline)": {
            "load_func": load_or_extract_embeddings_seamai,
            "model_instantiator_func": model_resnet50_coco,
            "root_path": SEAM_AI_DATA_PATH,
            "output_file": Path("resnet50_coco_embeddings_seamai_inline.npy"),
            "patch_size": None,
            "direction": "inline",
        },
        "SEAM AI (crossline)": {
            "load_func": load_or_extract_embeddings_seamai,
            "model_instantiator_func": model_resnet50_coco,
            "root_path": SEAM_AI_DATA_PATH,
            "output_file": Path("resnet50_coco_embeddings_seamai_crossline.npy"),
            "patch_size": None,
            "direction": "crossline",
        },
    },

    ## DINOv2 ViTB14 embeddings
    "dinov2_vitb14": {
        "NAMSS": {
            "load_func": load_or_extract_embeddings_namss,
            "model_instantiator_func": model_dinov2_vitb14,
            "root_path": NAMSS_DATA_PATH,
            "output_file": Path("dinov2_vitb14_embeddings_namss.npy"),
            "patch_size": 14,
            "direction": None,
        },
        "F3 (inline)": {
            "load_func": load_or_extract_embeddings_f3,
            "model_instantiator_func": model_dinov2_vitb14,
            "root_path": F3_DATA_PATH,
            "output_file": Path("dinov2_vitb14_embeddings_f3_inline.npy"),
            "patch_size": 14,
            "direction": "inline",
        },
        "F3 (crossline)": {
            "load_func": load_or_extract_embeddings_f3,
            "model_instantiator_func": model_dinov2_vitb14,
            "root_path": F3_DATA_PATH,
            "output_file": Path("dinov2_vitb14_embeddings_f3_crossline.npy"),
            "patch_size": 14,
            "direction": "crossline",
        },
        "SEAM AI (inline)": {
            "load_func": load_or_extract_embeddings_seamai,
            "model_instantiator_func": model_dinov2_vitb14,
            "root_path": SEAM_AI_DATA_PATH,
            "output_file": Path("dinov2_vitb14_embeddings_seamai_inline.npy"),
            "patch_size": 14,
            "direction": "inline",
        },
        "SEAM AI (crossline)": {
            "load_func": load_or_extract_embeddings_seamai,
            "model_instantiator_func": model_dinov2_vitb14,
            "root_path": SEAM_AI_DATA_PATH,
            "output_file": Path("dinov2_vitb14_embeddings_seamai_crossline.npy"),
            "patch_size": 14,
            "direction": "crossline",
        },
    },
}


def umap_embeddings(embeddings: np.ndarray, **kwargs) -> np.ndarray:
    n_components = kwargs.pop("n_components", 2)
    seed = kwargs.pop("random_state", 42)
    umap_model = UMAP(n_components=n_components, random_state=seed, **kwargs)
    embeddings_2d = umap_model.fit_transform(embeddings)
    return embeddings_2d


def load_features(model):
    configs = embedding_configs[model]
    feature_dict = {}
    for dataset_name, config in configs.items():
        print(f"Loading embeddings for {dataset_name}...")
        embeddings = config["load_func"](
            model_instantiator_func=config["model_instantiator_func"],
            root_path=config.get("root_path"),
            output_file=config["output_file"],
            patch_size=config.get("patch_size", None),
            direction=config.get("direction", None),
        )
        feature_dict[dataset_name] = embeddings
        print(f"Embeddings shape for {dataset_name}: {embeddings.shape}")

    return feature_dict


def get_umap_for_all_datasets(model: str, **umap_kwargs) -> pd.DataFrame:
    feature_dict = load_features(model)
    all_features = np.concatenate([
        feature_dict[k] for k in sorted(feature_dict.keys())], axis=0
    )
    print(f"All features shape: {all_features.shape}")
    umap_results = umap_embeddings(all_features, **umap_kwargs)
    print(f"UMAP results shape: {umap_results.shape}")

    # Create DataFrame
    umap_df = pd.DataFrame(umap_results, columns=["UMAP1", "UMAP2"])
    dataset_labels = []
    for dataset_name in sorted(feature_dict.keys()):
        embeddings = feature_dict[dataset_name]
        dataset_labels.extend([dataset_name] * embeddings.shape[0])
    umap_df["dataset"] = dataset_labels
    return umap_df


def plot_umap_with_density(
    df,
    color="dataset",
    density_type="contour",  # "contour" or "heatmap"
    height=800,
    width=1600,
    title=""
):
    """
    Creates a side-by-side figure with a UMAP scatter plot and a density map.
    """

    # --- Scatter (left) ---
    fig_scatter = px.scatter(
        df,
        x="UMAP1",
        y="UMAP2",
        color=color,
        symbol_sequence=["circle-open"],
        template="plotly_white",
    )

    # --- Density (right) ---
    if density_type == "contour":
        fig_density = px.density_contour(
            df,
            x="UMAP1",
            y="UMAP2",
            template="plotly_white",
        )

        # Fill contours + custom hover
        for t in fig_density.data:
            t.update(
                contours=dict(coloring="heatmap"),
            )

    elif density_type == "heatmap":
        fig_density = px.density_heatmap(
            df,
            x="UMAP1",
            y="UMAP2",
            nbinsx=150,
            nbinsy=150,
        )

    else:
        raise ValueError("density_type must be 'contour' or 'heatmap'")

    # --- Subplots 1×2 ---
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("UMAP Scatter", "UMAP Density"),
        horizontal_spacing=0.08,
    )

    # Add scatter traces (left)
    for trace in fig_scatter.data:
        fig.add_trace(trace, row=1, col=1)

    # Add density traces (right)
    for trace in fig_density.data:
        fig.add_trace(trace, row=1, col=2)

    # ------------------------------
    # Same axis ranges on both plots
    # ------------------------------
    # Try to use ranges from fig_density; if None, compute from data
    x_range = [
        float(df["UMAP1"].min()-1),
        float(df["UMAP1"].max())+1,
    ]
    y_range = [
        float(df["UMAP2"].min()-1),
        float(df["UMAP2"].max()+1),
    ]

    fig.update_xaxes(range=x_range, row=1, col=1)
    fig.update_yaxes(range=y_range, row=1, col=1)

    fig.update_xaxes(range=x_range, row=1, col=2)
    fig.update_yaxes(range=y_range, row=1, col=2)

    # Keep axes square (scatter + density)
    fig.update_xaxes(scaleanchor="y", row=1, col=1)
    fig.update_xaxes(scaleanchor="y", row=1, col=2)

    # Layout (normal interactivity preserved)
    fig.update_layout(
        height=height,
        width=width,
        title=title,
        template="plotly_white",
        showlegend=True,
        legend=dict(
            itemsizing="constant",
            orientation="h",
            yanchor="bottom",
            y=1.12,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="gray",
            borderwidth=1,
            font=dict(family="Times New Roman", size=20),
        ),
        margin=dict(t=120, b=40),
        font=dict(family="Times New Roman", size=20)
    )

    # Update subplot title fonts
    fig.update_layout(
        annotations=[
            dict(
                font=dict(
                    family="Times New Roman",
                    size=20
                )
            )
            for ann in fig.layout.annotations
        ]
    )

    # Move colorbar so legend doesn’t overlap (for density heatmap/contour)
    fig.update_coloraxes(colorbar=dict(
        x=0.98,       # push a bit to the right
        len=0.8,
        thickness=18,
        bgcolor="rgba(255,255,255,0.6)",
    ))

    return fig

def parse_name(umap_kwargs: dict) -> str:
    parts = []
    for k in sorted(umap_kwargs.keys()):
        v = umap_kwargs[k]
        parts.append(f"{k}-{v}")
    return "__".join(parts)


def main():
    UMAP_FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    
    for MODEL in ["resnet50_coco", "dinov2_vitb14"]:
        print(f"------ Processing model: {MODEL} -----")
        umap_kwargs = {
            "n_neighbors": 15,
            "min_dist": 0.1,
            "metric": "euclidean",
            # "random_state": 42,
            "init": "spectral",
        }
        
        embeddings = get_umap_for_all_datasets(model=MODEL, **umap_kwargs)
        fig = plot_umap_with_density(embeddings, color="dataset", density_type="contour")

        umap_params = "" if umap_kwargs is None else parse_name(umap_kwargs)
        filename = UMAP_FIGURES_PATH / f"datasets__model-{MODEL}__umap__{umap_params}.pdf"
        fig.write_image(filename)
        print(f"Figure written to {filename}")
        gc.collect()

if __name__ == "__main__":
    main()
