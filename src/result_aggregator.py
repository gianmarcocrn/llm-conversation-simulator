import os
import json
import matplotlib.pyplot as plt
from collections import Counter

from config import EVAL_TO_PLOT  # Directory containing the JSON files

# Define relevant ratings per category with order from best to worst
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

# Initialize counters for each category
rating_counts_per_category = {category: Counter({rating: 0 for rating in rating_options[category]}) for category in rating_options}

# Initialize total scores and counts for mean calculation
total_scores = {category: 0 for category in rating_options}
total_counts = {category: 0 for category in rating_options}

# Process each JSON file in the directory
for filename in os.listdir(EVAL_TO_PLOT):
    file_path = os.path.join(EVAL_TO_PLOT, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)

            # Extract ratings and compute totals for mean
            for category in rating_options:
                rating = data.get(category, {}).get("rating", "Unknown").lower().rstrip()
                if rating in rating_options[category]:
                    rating_counts_per_category[category][rating] += 1
                    total_scores[category] += rating_scores[rating]
                    total_counts[category] += 1
                else:
                    print(f"Unable to read rating for {category} in {file_path}")
        except Exception as e:
            print(f"{file_path} could not be read. Error: {e}")

# Calculate and print mean scores per metric
mean_scores = {}
print("\n=== Mean Scores per Metric ===")
for category in rating_options:
    mean_score = total_scores[category] / total_counts[category] if total_counts[category] > 0 else 0
    mean_scores[category] = mean_score
    print(f"{category.capitalize()}: Mean Score = {mean_score:.2f} (Scale: 1-4)")

# Plot subplots with mean score annotations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 grid for 4 categories
axes = axes.flatten()

for i, category in enumerate(rating_options):
    ax = axes[i]
    ratings = rating_options[category]
    counts = [rating_counts_per_category[category][rating] for rating in ratings]

    # Plot bars
    bars = ax.bar(ratings, counts, color='blue')

    # Add mean score as text inside the plot
    ax.text(0.95, 0.90, f"Mean Score: {mean_scores[category]:.2f}",
            transform=ax.transAxes, ha='right', va='top', fontsize=12,
            bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray'))

    ax.set_title(f"{category.capitalize()} Ratings")
    ax.set_ylabel("Count")
    ax.set_xticks(range(len(ratings)))
    ax.set_xticklabels(ratings, rotation=20, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

# Adjust layout and display
plt.tight_layout()
plt.show()