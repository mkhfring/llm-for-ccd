import matplotlib.pyplot as plt

positive_samples = [0.038, 2.54]
negative_samples = [0.035, 3.16]
selected_problems = [0.058, 2.98]

labels = ['Positive Samples', 'Negative Samples', 'Selected Problems']
colors = ['blue', 'orange', 'green']
width = 0.25  # width of each bar

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))

# Acceptance Rate subplot
for i, (label, color) in enumerate(zip(labels, colors)):
    axes[0].bar(i , [positive_samples[0], negative_samples[0], selected_problems[0]][i], width, label=label, color=color)
axes[0].set_title('Acceptance Rate (a)')
axes[0].set_xticks(range(3))
axes[0].set_xticklabels(labels)

# Cyclomatic Complexity subplot
for i, (label, color) in enumerate(zip(labels, colors)):
    axes[1].bar(i, [positive_samples[1], negative_samples[1], selected_problems[1]][i], width, label=label, color=color)
axes[1].set_title('Cyclomatic Complexity (b)')
axes[1].set_xticks(range(3))
axes[1].set_xticklabels(labels)

# Add legend
# fig.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3)

plt.show()
