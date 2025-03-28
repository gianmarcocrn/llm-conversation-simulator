import os
import json
import re
import numpy as np
import matplotlib.pyplot as plt

# Customize these paths, assumes results directories are moved inside the result_plotting_scripts directory
HUMAN_EVAL_DIR = "human_eval_results_15_completed"
LLM_EVAL_DIRS = {
    "Selene": "selene_eval_all",
    "Mistral": "mistral_eval_all",
    "Deepseek": "deepseek_eval_all",
    "Granite": "granite_eval_all"
}

metrics = ["consistency", "relevance", "naturalness", "fluency"]
rating_scores = {
    "highly consistent": 4, "mostly consistent": 3, "somewhat inconsistent": 2, "highly inconsistent": 1,
    "highly relevant": 4, "mostly relevant": 3, "somewhat irrelevant": 2, "highly irrelevant": 1,
    "highly natural": 4, "mostly natural": 3, "somewhat unnatural": 2, "highly unnatural": 1,
    "highly fluent": 4, "mostly fluent": 3, "somewhat fluent": 2, "not fluent": 1
}

human_scores = {metric: [] for metric in metrics}
llm_scores = {model: {metric: [] for metric in metrics} for model in LLM_EVAL_DIRS.keys()}

def extract_info(filename):
    match = re.search(r'(persona_[12]).*_(experiment[789])(?:_log|_conversation_log)?_(\d{2}-\d{2}-\d{4}_\d{2}:\d{2}:\d{2})', filename)
    return match.groups() if match else (None, None, None)

def load_scores(human_dir, llm_dir):
    scores = {metric: [] for metric in metrics}
    human_files = {}
    llm_files = {}

    for f in os.listdir(human_dir):
        if f.endswith(".txt"):
            persona, exp, timestamp = extract_info(f)
            if persona and exp and timestamp:
                human_files[(exp, persona, timestamp)] = f

    for f in os.listdir(llm_dir):
        if f.endswith(".txt"):
            persona, exp, timestamp = extract_info(f)
            if persona and exp and timestamp:
                llm_files[(exp, persona, timestamp)] = f

    common_keys = set(human_files.keys()).intersection(llm_files.keys())

    for key in common_keys:
        with open(os.path.join(human_dir, human_files[key]), "r", encoding="utf-8") as hf, \
             open(os.path.join(llm_dir, llm_files[key]), "r", encoding="utf-8") as lf:
            h_data = json.load(hf)
            l_data = json.load(lf)

            for metric in metrics:
                h_rating = h_data[metric]["rating"].lower().strip()
                l_rating = l_data[metric]["rating"].lower().strip()

                if h_rating in rating_scores and l_rating in rating_scores:
                    scores[metric].append(rating_scores[l_rating])
                    if key not in seen_keys:  # Add human rating once per conversation
                        human_scores[metric].append(rating_scores[h_rating])
            seen_keys.add(key)
    return scores

# Load all LLM model scores
seen_keys = set()
for model_name, model_dir in LLM_EVAL_DIRS.items():
    llm_scores[model_name] = load_scores(HUMAN_EVAL_DIR, model_dir)

# Plotting
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Score Distributions Across LLM Judge Models on all Evaluated Conversations", fontsize=16)
bar_width = 0.15
x_labels = [1, 2, 3, 4]
model_colors = ["blue", "green", "red", "orange", "purple"]

for idx, metric in enumerate(metrics):
    ax = axes[idx // 2, idx % 2]

    all_counts = []
    models = ["Human"] + list(LLM_EVAL_DIRS.keys())

    for i, model in enumerate(models):
        if model == "Human":
            counts, _ = np.histogram(human_scores[metric], bins=np.arange(0.5, 5.5, 1))
        else:
            counts, _ = np.histogram(llm_scores[model][metric], bins=np.arange(0.5, 5.5, 1))
        all_counts.append(counts)

    x = np.arange(len(x_labels))
    for i, counts in enumerate(all_counts):
        ax.bar(x + i * bar_width, counts, width=bar_width, label=models[i], edgecolor="black")

    ax.set_xticks(x + bar_width * len(models) / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel(f"{metric.capitalize()} Rating")
    ax.set_ylabel("Frequency")
    ax.set_title(metric.capitalize())
    ax.legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()