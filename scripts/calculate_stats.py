import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt


def get_csv_data(csv: str):
    df = pd.read_csv(csv)
    return df


output_df = get_csv_data("data/first2k.csv")

original_df = get_csv_data("data/initial_data.csv")
#  calulate accuracy of method


def calculate_accuracy(original_df, output_df):
    """
    Calculate the accuracy of the output DataFrame compared to the original DataFrame.

    Args:
        original_df (pd.DataFrame): The original DataFrame.
        output_df (pd.DataFrame): The output DataFrame.

    Returns:
        float: The accuracy as a percentage.
    """
    correct = 0
    total = 0

    for i in range(len(original_df)):
        if original_df.iloc[i]["Method"] and not pd.isna(original_df.iloc[i]["Method"]):
            total += 1
            if original_df.iloc[i]["Method"] == output_df.iloc[i]["method"]:
                correct += 1
            else:
                print(
                    f"Original: {original_df.iloc[i]['Method']}, Predicted: {output_df.iloc[i]['method']}")
    print(f"Total: {total}, Correct: {correct}")
    accuracy = (correct / total) * 100
    return accuracy


acc = calculate_accuracy(original_df[:2000], output_df)
print(f"Accuracy: {acc:.2f}%")
# #


# Assume your DataFrames look like this:
# actual_df['label'], predicted_df['label']

# Combine both into one DataFrame to filter easily
def get_confusion_matrix(original_df, output_df):
    """
    Combine the original and output DataFrames to create a confusion matrix.

    Args:
        original_df (pd.DataFrame): The original DataFrame.
        output_df (pd.DataFrame): The output DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the actual and predicted labels.
    """
    # Create a new DataFrame with actual and predicted labels

    # Drop rows with NaNs in either actual or predicted
    df = pd.DataFrame({
        'actual': original_df,
        'predicted': output_df
    })

    # Drop rows with NaNs in either actual or predicted
    df = df.dropna(subset=['actual', 'predicted'])
    labels = sorted(df['actual'].unique())
    # Compute confusion matrix
    cm = confusion_matrix(df['actual'], df['predicted'],
                          labels=labels)
    return df, cm, labels


df, cm, labels = get_confusion_matrix(
    original_df[:2000]["Design"], output_df["design"])
report_dict = classification_report(
    df['actual'], df['predicted'], labels=labels, output_dict=True)

df2, cm2, labels2 = get_confusion_matrix(
    original_df[:2000]["Method"], output_df["method"])
# Display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(cmap='Blues')
plt.tight_layout()
plt.xticks(rotation=45, ha='right')
disp2 = ConfusionMatrixDisplay(confusion_matrix=cm2, display_labels=labels2)
disp2.plot(cmap='Blues')
plt.xticks(rotation=45, ha='right')
plt.show()
plt.figure(figsize=(12, 6))
