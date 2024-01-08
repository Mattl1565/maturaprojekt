
import matplotlib.pyplot as plt
import seaborn as sns

# Example confusion matrix values
cm = [[186+38, 6+2], [21+4, 768*3+297]]

# Calculating the accuracy
accuracy = (cm[0][0] + cm[1][1]) / sum(cm[0] + cm[1])

# Calculating the precision
precision = cm[0][0] / (cm[0][0] + cm[0][1])

# Calculating the recall
recall = cm[0][0] / (cm[0][0] + cm[1][0])

# Calculating the F1 score
f1 = 2 * ((precision * recall) / (precision + recall))

# Printing the accuracy, precision, recall, and F1 score
print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 Score:', f1)

# Plotting the confusion matrix as a heatmap
ax = sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                 xticklabels=['True', 'False'],
                 yticklabels=['True', 'False'])

# Move the x-axis labels to the top
ax.xaxis.tick_top()

# Set the y-axis to the right and center it
ax.yaxis.set_label_position('right')

plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')

plt.show()
