import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Sample data
measures = ['Measure1', 'Measure2', 'Measure3', 'Measure4', 'Measure5']
t_scores = [60, 70, 50, 65, 55]
quintiles = [4, 5, 3, 4, 3]
significance_levels = [35, 50, 65, 70]  # Example significance levels

# Number of measures
num_measures = len(measures)

# Create figure and axis
fig, ax = plt.subplots()

# Bar chart for T-scores
bar_width = 0.4
x = np.arange(num_measures)
bars = ax.bar(x, t_scores, bar_width, label='T-Scores')

# Plotting quintiles as separate bars (if needed)
# bars2 = ax.bar(x + bar_width, quintiles, bar_width, label='Quintiles')

# Adding significance levels as dotted lines
for level in significance_levels:
    ax.axhline(y=level, color='r', linestyle='--', linewidth=1, label=f'Significance Level {level}')

# Adding text annotations for quintiles
for i in range(num_measures):
    ax.text(x[i], t_scores[i] + 1, f'Q{quintiles[i]}', ha='center', va='bottom')

# Labels and title
ax.set_xlabel('Measures')
ax.set_ylabel('T-Scores')
ax.set_title('T-Scores and Quintiles for Measures')
ax.set_xticks(x)
ax.set_xticklabels(measures)
ax.legend()
ax.set_ylim(0, 100)

# Show plot
plt.tight_layout()
plt.show()
