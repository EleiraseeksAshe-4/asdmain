import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Sample data
measures = ['Measure1', 'Measure2', 'Measure3', 'Measure4', 'Measure5']
t_scores = [60, 70, 50, 65, 55]
quintiles = [4, 5, 3, 4, 3]
significance_levels = [50, 60, 70]  # Example significance levels
custom_labels = ['Low', 'Average', 'High']  # Custom labels for second scale

# Number of measures
num_measures = len(measures)

# Create figure and axis
fig, ax = plt.subplots()

# Horizontal bar chart for T-scores
bar_height = 0.4
y = np.arange(num_measures)
colors = ['red' if t_score > 65 else 'blue' for t_score in t_scores]
bars = ax.barh(y, t_scores, bar_height, color=colors, label='T-Scores')

# Adding significance levels as dotted lines
for level in significance_levels:
    ax.axvline(x=level, color='r', linestyle='--', linewidth=1, label=f'Significance Level {level}')

# Adding text annotations for quintiles
for i in range(num_measures):
    ax.text(t_scores[i] + 1, y[i], f'Q{quintiles[i]}', va='center', ha='left')

# Labels and title
ax.set_ylabel('Measures')
ax.set_xlabel('T-Scores')
ax.set_title('T-Scores and Quintiles for Measures')
ax.set_yticks(y)
ax.set_yticklabels(measures)
ax.set_xlim(0, 100)

# Creating a secondary x-axis for custom labels
secax = ax.secondary_xaxis(-0.15)
secax.set_xticks([0, 50, 100])
secax.set_xticklabels(custom_labels)
secax.set_xlabel('Custom Scale')

# Show plot
plt.tight_layout()
plt.show()
