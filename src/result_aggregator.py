import os
import json
import matplotlib.pyplot as plt
from collections import Counter

from config import EVAL_RESULTS_DIR_NAME, EVAL_TO_PLOT # Directory containing the JSON files

# Define relevant ratings per category
rating_options = {
    "consistency": ["highly consistent", "mostly consistent", "somewhat inconsistent", "highly inconsistent"],
    "relevance": ["highly relevant", "mostly relevant", "somewhat irrelevant", "highly irrelevant"],
    "naturalness": ["highly natural", "mostly natural", "somewhat unnatural", "highly unnatural"],
    "fluency": ["highly fluent", "mostly fluent", "somewhat fluent", "not fluent"]
}

# Initialize counters for each category with predefined rating options (ensures all ratings appear even if count is 0)
rating_counts_per_category = {category: Counter({rating: 0 for rating in rating_options[category]}) for category in rating_options}

# Process each JSON file in the directory
for filename in os.listdir(EVAL_TO_PLOT):
    # Assuming all files contain JSON
    file_path = os.path.join(EVAL_TO_PLOT, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)  # Load JSON content

            # Extract ratings for each category and count occurrences
            for category in rating_options:
                rating = data.get(category, {}).get("rating", "Unknown").lower()
                if rating in rating_options[category]:  # Only count relevant ratings
                    rating_counts_per_category[category][rating] += 1
                else:
                    print(f"Unable to read rating for {category} for {file_path}")
        except:
            print(f"{file_path} could not be read")

# Plot subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 grid for 4 categories
axes = axes.flatten()  # Convert to 1D array for easy looping

for i, category in enumerate(rating_options):
    ax = axes[i]

    # Extract only relevant ratings for this metric
    ratings = rating_options[category]  # Ensure predefined order
    counts = [rating_counts_per_category[category][rating] for rating in ratings]

    ax.bar(ratings, counts, color='skyblue')
    ax.set_title(f"{category.capitalize()} Ratings")
    ax.set_ylabel("Count")
    ax.set_xticks(ratings)
    ax.set_xticklabels(ratings, rotation=20, ha="right")  # Rotate labels for readability
    ax.grid(axis="y", linestyle="--", alpha=0.7)

# Adjust layout and display the plots
plt.tight_layout()
plt.show()