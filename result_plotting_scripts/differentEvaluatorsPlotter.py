import matplotlib.pyplot as plt

# Model sizes
model_sizes = ["Llama 1b", "Llama 3b", "Llama 8b"]

evaluation_methods = ["Human", "Selene", "Mistral", "Deepseek", "Granite"]

scores = {
    "Consistency": {
        "Human": [3.05, 3.62, 3.71],
        "Selene": [3.15, 3.63, 3.76],
        "Mistral": [3.72, 3.83, 3.88],
        "Deepseek": [3.91, 4.00, 3.93],
        "Granite": [3.87, 4.00, 3.97]
    },
    "Relevance": {
        "Human": [2.98, 3.74, 3.83],
        "Selene": [3.58, 4.00, 4.00],
        "Mistral": [3.76, 3.88, 3.90],
        "Deepseek": [3.86, 3.97, 4.00],
        "Granite": [3.88, 4.00, 4.00]
    },
    "Naturalness": {
        "Human": [2.26, 3.34, 2.93],
        "Selene": [3.09, 3.44, 3.67],
        "Mistral": [3.59, 3.70, 3.62],
        "Deepseek": [3.77, 3.83, 3.81],
        "Granite": [3.22, 3.45, 3.50]
    },
    "Fluency": {
        "Human": [3.75, 3.88, 3.95],
        "Selene": [3.33, 3.57, 3.78],
        "Mistral": [3.43, 3.40, 3.43],
        "Deepseek": [3.79, 3.88, 3.96],
        "Granite": [3.87, 3.95, 3.85]
    }
}

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Average Evaluation Scores Across Model Sizes")

for idx, (metric, values) in enumerate(scores.items()):
    ax = axes[idx // 2, idx % 2]
    
    # Plot each evaluation method
    for method in evaluation_methods:
        ax.plot(model_sizes, values[method], marker='o', label=method)

    ax.set_title(metric)
    ax.set_ylabel("Avg Score (out of 4.0)")
    ax.set_ylim(2.0, 4.2) 
    ax.legend(loc="lower right")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()