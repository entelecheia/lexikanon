import logging
import multiprocessing as mp
from functools import partial
from pathlib import Path
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from lexikanon import HyFI

logger = logging.getLogger(__name__)


def plot_dendrogram(model, **kwargs):
    """
    Plots the hierarchical clustering dendrogram.
    """
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = sum(
            1 if child_idx < n_samples else counts[child_idx - n_samples]
            for child_idx in merge
        )
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    plt.title("Hierarchical Clustering Dendrogram")
    dendrogram(linkage_matrix, truncate_mode="level", p=3)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.show()


def plot_similarity_distribution(
    similarity_matrix: np.ndarray,
    percentile: int = 80,
    distance_threshold: Optional[float] = None,
    title_name: str = "",
    title_fontsize: int = 10,
    output_dir: str = ".",
    show_fig: bool = False,
    save_fig: bool = True,
) -> str:
    """
    Plots the distribution of cosine similarities between pairs of documents.
    """
    # Flatten the matrix to a 1D array
    similarity_array = similarity_matrix[
        np.triu_indices(similarity_matrix.shape[0], k=1)
    ]

    # Compute the number of samples and the average similarity
    num_samples = len(similarity_array)
    med_similarity = np.median(similarity_array)
    pct_similarity = np.percentile(similarity_array, percentile)

    # Reset the matplotlib figure
    plt.clf()

    # Generate histogram
    plt.hist(similarity_array, bins="auto", color="#0504aa", alpha=0.7, rwidth=0.85)
    # If distance threshold is provided, plot a vertical line at that threshold
    if distance_threshold:
        sim_threshold = 1 - distance_threshold
        plt.axvline(x=sim_threshold, color="r", linestyle="dashed", linewidth=1)

    # Add plot labels
    plt.grid(axis="y", alpha=0.75)
    plt.xlabel("Cosine Similarity")
    plt.ylabel("Frequency")
    title = "Distribution of Cosine Similarities"
    title = f"{title} - {title_name}" if title_name else title
    plt.title(title, fontsize=title_fontsize)

    # Add labels for the number of samples and the average similarity
    x_pos = 0.4
    y_pos = 0.95
    plt.text(
        x_pos,
        y_pos,
        f"Number of Sample pairs: {num_samples}",
        transform=plt.gca().transAxes,
        fontsize=title_fontsize - 1,
    )
    plt.text(
        x_pos,
        y_pos - 0.05,
        f"Median Similarity: {med_similarity:.2f}",
        transform=plt.gca().transAxes,
        fontsize=title_fontsize - 1,
    )
    plt.text(
        x_pos,
        y_pos - 0.1,
        f"{percentile}th Percentile: {pct_similarity:.2f}",
        transform=plt.gca().transAxes,
        fontsize=title_fontsize - 1,
    )
    num_samples_over_threshold = np.sum(similarity_array > sim_threshold)
    plt.text(
        x_pos,
        y_pos - 0.15,
        f"Number of samples over threshold: {num_samples_over_threshold}",
        transform=plt.gca().transAxes,
        fontsize=title_fontsize - 1,
    )

    # Save and/or show the figure
    filename = title_name.replace(" ", "_").lower()
    filename = f"similarity_dist_{filename}.png"
    output_file = f"{output_dir}/{filename}"
    if save_fig:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        plt.savefig(output_file, dpi=300)
    if show_fig:
        plt.show()
    return filename


def _process_batch(
    data: Tuple[str, pd.DataFrame],
    min_num_docs: int = 5,
    percentile: int = 80,
    distance_threshold: Optional[float] = None,
    linkage: str = "average",
    token_col: str = "tokens",
    id_col: str = "id",
    timestamp_col: str = "timestamp",
    cluster_col: str = "cluster",
    duplicate_col: str = "duplicate",
    dist_fig_col: str = "dist_fig",
    output_dir: str = ".",
    show_fig: bool = False,
    save_fig: bool = False,
) -> pd.DataFrame:
    """
    Processes a batch of data by calculating the cosine similarity between all pairs of documents in the batch.
    """
    batch_name, batch_data = data
    batch_data.reset_index(inplace=True)
    if len(batch_data) < min_num_docs:
        logger.info(
            "Batch %s has %d documents, which is less than the minimum number of documents (%d). Skipping.",
            batch_name,
            len(batch_data),
            min_num_docs,
        )
        return batch_data
    # Custom tokenizer that uses the already tokenized words
    vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
    tfidf_matrix = vectorizer.fit_transform(batch_data[token_col])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    filename = plot_similarity_distribution(
        similarity_matrix,
        distance_threshold=distance_threshold,
        title_name=batch_name,
        percentile=percentile,
        output_dir=output_dir,
        show_fig=show_fig,
        save_fig=save_fig,
    )
    batch_data[dist_fig_col] = filename

    # Calculate the 90th percentile of the similarity scores
    percentile_thres = np.percentile(similarity_matrix, percentile)
    if not distance_threshold:
        distance_threshold = max(0.5, 1 - percentile_thres)
    distance_threshold = max(min(0.99, distance_threshold), 0.01)
    # Perform Agglomerative Clustering on the similarity matrix
    ac = AgglomerativeClustering(
        n_clusters=None,
        affinity="precomputed",
        linkage=linkage,
        distance_threshold=distance_threshold,
    )
    ac.fit(
        1 - similarity_matrix
    )  # AgglomerativeClustering expects distances, not similarities
    # plot_dendrogram(ac)

    # Create DataFrame df with cluster labels and Unix timestamp createdDt
    df = pd.DataFrame(
        {cluster_col: ac.labels_, timestamp_col: batch_data[timestamp_col]},
        index=batch_data[id_col],
    )
    batch_data[cluster_col] = batch_data[id_col].map(df[cluster_col])

    # create a column with the concatenation of the timestamp and the id
    concat_col = f"{timestamp_col}_{id_col}"
    df[concat_col] = df[timestamp_col].astype(str) + "|" + df.index

    # Find the minimum createdDt_newsId for each cluster
    min_ids = df.groupby(cluster_col)[concat_col].min()

    # Extract the index of the earliest document in each cluster
    earliest_doc_indices = min_ids.str.split("|").str[-1]
    similar_data = batch_data[~batch_data[id_col].isin(earliest_doc_indices)]
    batch_data.loc[similar_data.index, duplicate_col] = True

    return batch_data


def find_similar_docs_by_clustering(
    data: pd.DataFrame,
    num_workers: int = 2,
    min_num_docs: int = 5,
    percentile: int = 80,
    distance_threshold: Optional[float] = None,
    linkage: str = "average",
    grouping_freq: str = "W",
    grouping_name: str = "Week",
    timestamp_col: str = "timestamp",
    token_col: str = "tokens",
    id_col: str = "id",
    cluster_col: str = "cluster",
    duplicate_col: str = "duplicate",
    dist_fig_col: str = "dist_fig",
    output_dir: str = ".",
    show_fig: bool = False,
    save_fig: bool = False,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Finds similar documents in the given data using cosine similarity and Agglomerative Clustering.
    """
    # Convert timestamp_col to datetime and set it as the index
    data[timestamp_col] = pd.to_datetime(data[timestamp_col])
    data.set_index(timestamp_col, inplace=True)
    data[cluster_col] = None
    data[duplicate_col] = False
    data[dist_fig_col] = None

    # Group data by week
    batchs = [grp for _, grp in data.groupby(pd.Grouper(freq=grouping_freq))]
    batchs = [
        (f"{grouping_name} {min(week.index).date()}", week)
        for week in batchs
        if len(week) > 0
    ]

    # Prepare partial function for process_batch
    process_batch_partial = partial(
        _process_batch,
        min_num_docs=min_num_docs,
        percentile=percentile,
        distance_threshold=distance_threshold,
        linkage=linkage,
        token_col=token_col,
        id_col=id_col,
        timestamp_col=timestamp_col,
        cluster_col=cluster_col,
        duplicate_col=duplicate_col,
        dist_fig_col=dist_fig_col,
        output_dir=output_dir,
        show_fig=show_fig,
        save_fig=save_fig,
    )

    # Apply process_week to each group of data using multiprocessing
    with mp.Pool(processes=num_workers) as pool:
        batch_results = pool.map(
            process_batch_partial,
            batchs,
        )

    data = pd.concat(batch_results)
    # data.reset_index(inplace=True)
    logger.info("Number of documents: %d", len(data))
    if duplicate_col in data.columns:
        logger.info("Number of duplicate documents: %d", data[duplicate_col].sum())
    if verbose:
        print(data.tail(10))
    return data
