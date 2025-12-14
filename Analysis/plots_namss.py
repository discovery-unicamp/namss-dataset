from typing import Optional, Union
import pandas as pd
import numpy as np
from pathlib import Path
from umap import UMAP
import plotly.express as px
import itertools
import tqdm
import time
from embedding_namss import load_or_extract_embeddings
from utils import (
    model_resnet50_coco,
    model_dinov2_vitb14,
)

METADATA_ALL_PATH = Path("../NAMSS_Metadata/2DSeismic_all_metadata.csv")
DATA_PATH = Path("../Data/NAMSS")
UMAP_FIGURES_PATH = Path("figures/umap")


def load_metadata():
    macro_map = {
        # ---------------- TEST ----------------
        "Bering Sea": "Bering Sea",  # test
        "Washington": "Washington-Oregon",  # test
        "South Atlantic Ocean": "Argentine Basin",  # falls under test macro-region
        "Atlantic Ocean": "Argentine Basin",  # test subset (appears in train too, override below)
        # ---------------- TRAIN ----------------
        "Baltimore Canyon": "Atlantic Ocean",
        "": None,
        "Cay Sal (Old Bahama Channel)": "Atlantic Ocean",
        "North Atlantic Ocean": "Atlantic Ocean",
        "Gulf of Maine": "Atlantic Ocean",
        "Blake Plateau": "Atlantic Ocean",
        "Mid-south Atlantic Ocean": "Atlantic Ocean",
        "Yarmouth Arch": "Atlantic Ocean",
        "Georges Bank": "Atlantic Ocean",
        "Mid-Atlantic Ocean": "Atlantic Ocean",
        "Cape Hatteras": "Atlantic Ocean",
        "Commandant": "Atlantic Ocean",
        "Block Canyon": "Atlantic Ocean",
        "Georgia Embayment": "Atlantic Ocean",
        "East Georges Bank": "Atlantic Ocean",
        "South Baltimore Canyon": "Atlantic Ocean",
        "Chukchi Sea": "Arctic Ocean",
        "Beaufort Sea": "Arctic Ocean",
        "Arctic Ocean": "Arctic Ocean",
        "North Slope": "Arctic Ocean",
        "Gulf of Alaska": "Gulf of Alaska",
        "Western Gulf of Alaska": "Gulf of Alaska",
        "Southern California": "South California",
        "Central California": "South California",
        "Aleutian Arc": "Gulf of Alaska",
        # ---------------- VALID ----------------
        "Caribbean Sea": "Caribbean Sea",
        "San Francisco Bay": "North California",
        "Northern California": "North California",
        "Monterey Bay": "North California",
    }

    def parse_filename(link):
        return link.split("/")[-3].lower().strip()

    metadata_all = pd.read_csv(METADATA_ALL_PATH, sep="\t")
    metadata_all["FileName"] = metadata_all[
        "datasetInformation.datasetContentLink"
    ].map(parse_filename)

    lines = []

    for i, f in tqdm.tqdm(
        enumerate(sorted(list(Path(DATA_PATH).rglob("*.tiff")))),
        desc="Processing metadata...",
    ):
        survey = f.stem.split(".")[0].lower().strip()
        partition = f.parent.name.split("_")[1]
        res = metadata_all[metadata_all["FileName"] == survey]
        if len(res) != 1:
            raise ValueError(
                f"Expected one metadata entry for survey {survey}. There are {len(res)}"
            )
        res = res.iloc[0].to_dict()
        lines.append(
            {
                "file": str(f),
                "survey": survey,
                "partition": partition,
                "year": res["datasetInformation.temporalExtent.startDate"].split("-")[
                    0
                ],
                "receiver": res[
                    "acquisitionInformation.acquisitionParameters.receiverType"
                ],
                "location": res["datasetInformation.geographicFeatures.featureName"],
                "sampling_interval_micro_seconds": res[
                    "acquisitionInformation.acquisitionParameters.sampleInterval_inMicroseconds"
                ],
                "processed_method": res["datasetInformation.processedMethod"],
            }
        )

    df = pd.DataFrame(lines)
    df["macro_region"] = df["location"].map(macro_map)
    return df


def year_map(x):
    x = int(x)
    if x < 1970:
        return "1970"
    elif x < 1980:
        return "1980"
    elif x < 1990:
        return "1990"
    elif x < 2000:
        return "2000"
    elif x < 2010:
        return "2010"
    else:
        return "2020"


def umap_embeddings(embeddings: np.ndarray, **kwargs) -> np.ndarray:
    n_components = kwargs.pop("n_components", 2)
    seed = kwargs.pop("random_state", 42)
    umap_model = UMAP(n_components=n_components, random_state=seed, **kwargs)
    embeddings_2d = umap_model.fit_transform(embeddings)
    return embeddings_2d


def parse_name(umap_kwargs: dict) -> str:
    parts = []
    for k in sorted(umap_kwargs.keys()):
        v = umap_kwargs[k]
        parts.append(f"{k}-{v}")
    return "__".join(parts)


def multi_plot(
    embeddings: np.ndarray,
    df: pd.DataFrame,
    umap_kwargs: Optional[dict] = None,
    fname_prefix: Optional[str] = None,
    figures_path: Union[Path, str] = "figures",
):
    # Get embeddings
    embeddings_2d = umap_embeddings(embeddings, **(umap_kwargs or {}))
    # Create a dataframe that holds the 2D embeddings and metadata
    umap_df = pd.DataFrame(embeddings_2d, columns=["UMAP1", "UMAP2"])
    umap_df["Survey"] = df["survey"]
    umap_df["Partition"] = df["partition"]
    umap_df["Year"] = df["year"].map(lambda x: year_map(x))
    umap_df["Receiver"] = df["receiver"]
    umap_df["Location"] = df["location"]
    umap_df["Sampling Interval"] = df["sampling_interval_micro_seconds"]
    umap_df["Processed Method"] = df["processed_method"]
    umap_df["Macro Region"] = df["macro_region"]

    umap_params = "" if umap_kwargs is None else parse_name(umap_kwargs)
    figures_path = Path(figures_path)
    figures_path.mkdir(parents=True, exist_ok=True)

    def do_plot(color_by: str):
        fig = px.scatter(
            umap_df,
            x="UMAP1",
            y="UMAP2",
            color=color_by,
            hover_data=[
                "Survey",
                "Partition",
                "Year",
                "Receiver",
                "Location",
                "Sampling Interval",
                "Processed Method",
                "Macro Region",
            ],
            height=800,
            width=800,
            symbol_sequence=["circle-open"],
        )
        fig.update_layout(font=dict(family="Times New Roman", size=24))

        output_path = Path(
            figures_path
            / f"{fname_prefix}__color-{color_by}__embedder-umap__{umap_params}.pdf"
        )
        fig.write_image(output_path)
        print(f"Saved figure to {output_path}")

        return fig

    do_plot(color_by="Partition")
    do_plot(color_by="Year")
    do_plot(color_by="Macro Region")
    return umap_df


def main():
    df = load_metadata()
    embedding_configs = {
        "resnet50_coco": {
            "model_instantiator_func": model_resnet50_coco,
            "output_file": Path("resnet50_coco_embeddings_namss.npy"),
            "patch_size": None,
        },
        "dinov2_vitb14": {
            "model_instantiator_func": model_dinov2_vitb14,
            "output_file": Path("dinov2_vitb14_embeddings_namss.npy"),
            "patch_size": 14,
        },
    }

    n_neighbors_list = [15]  # [15, 45, 90, 122]
    min_dist_list = [0.1]  # [0.1, 0.5]
    metric_list = ["euclidean"]  # ["euclidean", "cosine"]
    init_list = ["spectral"]  # ["spectral", "pca"]

    umap_params_list = []

    # Create a list of all combinations of UMAP parameters
    for nn, md, metric, init in itertools.product(
        n_neighbors_list, min_dist_list, metric_list, init_list
    ):

        params = {
            "n_components": 2,
            "random_state": 42,
            "n_neighbors": nn,
            "min_dist": md,
            "metric": metric,
            "init": init,
        }

        umap_params_list.append(params)

    print(f"There are {len(umap_params_list)} UMAP parameter combinations!")

    for name, config in embedding_configs.items():
        print(f"--- Processing embeddings: {name} ---")
        embeddings = load_or_extract_embeddings(
            model_instantiator_func=config["model_instantiator_func"],
            root_path=DATA_PATH,
            output_file=config["output_file"],
            patch_size=config["patch_size"],
        )
        print(f"Loaded embeddings for {name}, shape: {embeddings.shape}!")

        for i, umap_kwargs in enumerate(umap_params_list):
            start_time = time.time()
            print(
                f"--- [Config no. {i+1:03d}/{len(umap_params_list):03d}] UMAP with params: {umap_kwargs}"
            )
            multi_plot(
                embeddings=embeddings,
                df=df,
                umap_kwargs=umap_kwargs,
                fname_prefix=f"namss_{name}",
                figures_path=UMAP_FIGURES_PATH,
            )
            end_time = time.time()
            print(f"--- UMAP completed in {end_time - start_time:.2f} seconds")

            remaining_seconds = (end_time - start_time) * (
                len(umap_params_list) - i - 1
            )
            print(f"--- Estimated time remaining: {remaining_seconds} seconds")
        print("")


if __name__ == "__main__":
    main()
