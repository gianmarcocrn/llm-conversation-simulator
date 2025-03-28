import os
import json
import re
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import spearmanr, kendalltau
from sklearn.metrics import cohen_kappa_score

# Define directories, modify as needed, assumes results directories are moved to result_plotting_scripts
HUMAN_EVAL_DIR = "human_eval_results_15_completed"
LLM_EVAL_DIR = "selene_eval_all"

# Define metric categories
rating_options = {
    "consistency": ["highly consistent", "mostly consistent", "somewhat inconsistent", "highly inconsistent"],
    "relevance": ["highly relevant", "mostly relevant", "somewhat irrelevant", "highly irrelevant"],
    "naturalness": ["highly natural", "mostly natural", "somewhat unnatural", "highly unnatural"],
    "fluency": ["highly fluent", "mostly fluent", "somewhat fluent", "not fluent"]
}

# Assign scores to each rating (best=4, worst=1)
rating_scores = {
    "highly consistent": 4, "mostly consistent": 3, "somewhat inconsistent": 2, "highly inconsistent": 1,
    "highly relevant": 4, "mostly relevant": 3, "somewhat irrelevant": 2, "highly irrelevant": 1,
    "highly natural": 4, "mostly natural": 3, "somewhat unnatural": 2, "highly unnatural": 1,
    "highly fluent": 4, "mostly fluent": 3, "somewhat fluent": 2, "not fluent": 1
}

# Initialize lists for correlation analysis
metrics = ["consistency", "relevance", "naturalness", "fluency"]
human_scores = {metric: [] for metric in metrics}
llm_scores = {metric: [] for metric in metrics}

#Extracts persona (persona_1/persona_2), experiment number (experiment7, 8, 9), and timestamp from filename.
def extract_info(filename):
    match = re.search(r'(persona_[12]).*_(experiment[789])(?:_log|_conversation_log)?_(\d{2}-\d{2}-\d{4}_\d{2}:\d{2}:\d{2})', filename)
    return match.groups() if match else (None, None, None)

# Store filenames indexed by (experiment, persona, timestamp)
human_files = {}
llm_files = {}

for filename in os.listdir(HUMAN_EVAL_DIR):
    if filename.endswith(".txt"):
        persona, experiment, timestamp = extract_info(filename)
        if persona and experiment and timestamp:
            human_files[(experiment, persona, timestamp)] = filename

for filename in os.listdir(LLM_EVAL_DIR):
    if filename.endswith(".txt"):
        persona, experiment, timestamp = extract_info(filename)
        if persona and experiment and timestamp:
            llm_files[(experiment, persona, timestamp)] = filename

# Find valid matching evaluations
common_keys = sorted(set(human_files.keys()).intersection(llm_files.keys()), key=lambda x: x[0])  # Sort by experiment

print(f"Found {len(common_keys)} corresponding evaluation files")

experiment7_last_index = {metric: 0 for metric in metrics}
experiment8_last_index = {metric: 0 for metric in metrics}
experiment9_last_index = {metric: 0 for metric in metrics}

skipped_files_count = 0

for experiment, persona, timestamp in common_keys:  # Ensures we process in order
    human_file_path = os.path.join(HUMAN_EVAL_DIR, human_files[(experiment, persona, timestamp)])
    llm_file_path = os.path.join(LLM_EVAL_DIR, llm_files[(experiment, persona, timestamp)])

    with open(human_file_path, "r", encoding="utf-8") as hf, open(llm_file_path, "r", encoding="utf-8") as lf:
        human_data = json.load(hf)
        llm_data = json.load(lf)

        # Convert string ratings to numerical values
        for metric in metrics:
            human_rating = human_data[metric]["rating"].lower().rstrip().lstrip()
            llm_rating = llm_data[metric]["rating"].lower().rstrip().lstrip()

            if human_rating in rating_scores and llm_rating in rating_scores:
                human_scores[metric].append(rating_scores[human_rating])
                llm_scores[metric].append(rating_scores[llm_rating])
                if (experiment == "experiment7"):
                    experiment7_last_index[metric] = len(human_scores[metric])
                if (experiment == "experiment8"):
                    experiment8_last_index[metric] = len(human_scores[metric])
                if (experiment == "experiment9"):
                    experiment9_last_index[metric] = len(human_scores[metric])
            else:
                print(f"Skipping due to invalid rating: Human --> {human_rating} in {human_file_path}, LLM --> {llm_rating} in {llm_file_path}")
                skipped_files_count += 1

print(experiment7_last_index, experiment8_last_index, experiment9_last_index)
print(f"Skipped {skipped_files_count} ratings due to incompatible evaluation ratings")

for metric in metrics:
    # Compute mean and standard deviation
    human_mean, human_std = np.mean(human_scores[metric]), np.std(human_scores[metric])
    llm_mean, llm_std = np.mean(llm_scores[metric]), np.std(llm_scores[metric])

# Compute and display Spearman’s correlation for each metric
for metric in metrics:
    if human_scores[metric] and llm_scores[metric]:  # Ensure data exists
        spearman_corr, spearman_pvalue = spearmanr(human_scores[metric], llm_scores[metric])
        kendall_corr, kendall_pvalue = kendalltau(human_scores[metric], llm_scores[metric])
        cohen_kappa_squared = cohen_kappa_score(human_scores[metric], llm_scores[metric], weights="quadratic")
        
        print(f"{metric.capitalize()}")
        print(f"- Spearman's Correlation: {spearman_corr:.3f}, Spearman pvalue: {spearman_pvalue:.5f} ({'statistically significant' if spearman_pvalue < 0.05 else 'statistically insignificant'})")
        print(f"- Kendall's τ: {kendall_corr:.3f}, Kendall's pvalue: {kendall_pvalue:.5f} ({'statistically significant' if kendall_pvalue < 0.05 else 'statistically insignificant'})")
        print(f"- Quadratically Weighted Cohen Kappa Score: {cohen_kappa_squared:.3f}")
    else:
        print(f"{metric.capitalize()} - Not enough data for correlation")


# Bar Chart: Side-by-Side Comparison of Ratings (Subplots for all metrics)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Distribution of Ratings: Human vs. LLM")

# Find the max y-axis value across all metrics for uniformity
max_y = 0
bar_width = 0.4  # Width of each bar

for metric in metrics:
    human_counts, bins = np.histogram(human_scores[metric], bins=np.arange(0.5, 5.5, 1))
    llm_counts, _ = np.histogram(llm_scores[metric], bins=np.arange(0.5, 5.5, 1))
    max_y = max(max_y, max(human_counts), max(llm_counts))  # Update max y-axis limit

for idx, metric in enumerate(metrics):
    ax = axes[idx // 2, idx % 2]
    
    human_counts, bins = np.histogram(human_scores[metric], bins=np.arange(0.5, 5.5, 1))
    llm_counts, _ = np.histogram(llm_scores[metric], bins=np.arange(0.5, 5.5, 1))

    # Define positions for the bars
    x_vals = np.array([1, 2, 3, 4])  
    human_x = x_vals - bar_width / 2  
    llm_x = x_vals + bar_width / 2 

    # Plot bars side-by-side
    ax.bar(human_x, human_counts, width=bar_width, label="Human", alpha=0.8, edgecolor="black")
    ax.bar(llm_x, llm_counts, width=bar_width, label="LLM", alpha=0.8, edgecolor="black")

    # Set labels and titles
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["1", "2", "3", "4"])
    ax.set_xlabel(f"{metric.capitalize()} Score")
    ax.set_ylabel("Frequency")
    ax.set_title(f"{metric.capitalize()} Ratings")
    ax.legend()
    
    # Set uniform y-axis limit for all subplots
    ax.set_ylim(0, max_y + 2) 

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Heatmap: Agreement Levels
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Selene-Human Agreement Heatmaps for All Metrics")

conversion_dict = {0: 3, 1:2, 2:1, 3:0}

for idx, metric in enumerate(metrics):
    agreement_matrix = np.zeros((4, 4))
    for h, l in zip(human_scores[metric], llm_scores[metric]):
        agreement_matrix[conversion_dict[h-1], l-1] += 1  # Adjust indices for 1-4 scale

    ax = axes[idx // 2, idx % 2]
    sns.heatmap(agreement_matrix, annot=True, fmt=".0f", cmap="Blues", xticklabels=[1,2,3,4], yticklabels=[4,3,2,1], ax=ax)
    ax.set_title(metric.capitalize())
    ax.set_xlabel("LLM Ratings")
    ax.set_ylabel("Human Ratings")
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout for title space
plt.show()

# Line Graphs: One subplot per metric
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Human vs. LLM Scores Across Evaluations")

for idx, metric in enumerate(metrics):
    ax = axes[idx // 2, idx % 2]
    x_vals = list(range(1, len(human_scores[metric]) + 1))
    
    ax.plot(x_vals, human_scores[metric], label='Human', marker='o', linestyle='-', color='blue')
    ax.plot(x_vals, llm_scores[metric], label='LLM', marker='x', linestyle='--', color='red')
    ax.axvline(x = experiment7_last_index[metric], color='green', label='End of Llama 1b')
    ax.axvline(x = experiment8_last_index[metric], color='cyan', label='End of Llama 3b')
    ax.axvline(x = experiment9_last_index[metric], color='orange', label='End of Llama 8b')

    ax.set_title(metric.capitalize())
    ax.set_xlabel("Evaluation Index")
    ax.set_ylabel("Rating (1-4 Scale)")
    ax.set_ylim(0.8, 4.2)
    ax.set_yticks([1, 2, 3, 4])
    ax.legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Generate Bland-Altman plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Bland-Altman Plots: Human vs. LLM Ratings")

for idx, metric in enumerate(metrics):
    mean_scores = [(h + l) / 2 for h, l in zip(human_scores[metric], llm_scores[metric])]
    diff_scores = [h - l for h, l in zip(human_scores[metric], llm_scores[metric])]
    mean_diff = np.mean(diff_scores)
    std_diff = np.std(diff_scores)
    upper_limit = mean_diff + 1.96 * std_diff
    lower_limit = mean_diff - 1.96 * std_diff

    ax = axes[idx // 2, idx % 2]
    ax.scatter(mean_scores, diff_scores, alpha=0.2)
    ax.axhline(mean_diff, color='red', linestyle='--', label=f'Mean Diff: {mean_diff:.2f}')
    ax.axhline(upper_limit, color='gray', linestyle='--', label=f'+1.96 SD: {upper_limit:.2f}')
    ax.axhline(lower_limit, color='gray', linestyle='--', label=f'-1.96 SD: {lower_limit:.2f}')
    ax.set_title(metric.capitalize())
    ax.set_xlabel("Mean of Human and LLM Scores")
    ax.set_ylabel("Difference (Human - LLM)")
    ax.set_yticks([-3, -2 , -1 , 0, 1, 2, 3])
    ax.legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()