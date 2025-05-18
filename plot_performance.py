import matplotlib.pyplot as plt
import numpy as np

# Data provided by the user
data = {
    "o3": "47/47",
    "o4-mini": "47/47",
    "o1": "44/47",
    "4.1-mini": "42/47",
    "4.1": "41/47",
    "4o": "39/47",
    "3.7 sonnet thinking": "47/47",
    "3.7 sonnet": "46/47",
    "3.5 sonnet": "39/47",
    "Gemini 2.5 Pro": "47/47",
    "Gemini 2.0 Flash": "44/47",
    "Deepseek R1": "47/47",
}

# Extract models and scores
models_scores = []
for model, value in data.items():
    score = int(value.split('/')[0])
    models_scores.append((model, score))

# Sort by score (descending), then by model name (ascending) as a tie-breaker
models_scores.sort(key=lambda x: (-x[1], x[0]))

# Unpack sorted models and scores
sorted_models = [item[0] for item in models_scores]
sorted_scores = [item[1] for item in models_scores]

total_possible = int(data[sorted_models[0]].split('/')[1]) # Assuming all have the same total

# Calculate percentages for better comparison if needed, or use raw scores
# percentages = [(score / total_possible) * 100 for score in sorted_scores] # Not used in current plot

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 8))

# Create the bar chart
bars = ax.bar(sorted_models, sorted_scores, color=plt.cm.get_cmap('viridis', len(sorted_models)).colors)

# Add labels and title
ax.set_ylabel(f'correctly balanced equations (out of {total_possible})', fontsize=14)
ax.set_xlabel('Model', fontsize=14)
ax.set_title('BalanceBench performance by model', fontsize=16, fontweight='bold')

# Add data labels to the bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height}', ha='center', va='bottom', fontsize=10)

# Improve layout
plt.xticks(rotation=45, ha='right', fontsize=12) # Rotate model names for better readability
plt.yticks(fontsize=12)
# ax.invert_yaxis() # Removed as sorting handles the order for highest at top
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

# Save the figure
plt.savefig('img.png', dpi=300)
