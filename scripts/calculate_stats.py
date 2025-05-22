import pandas as pd


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
        if original_df.iloc[i]["Design"] and not pd.isna(original_df.iloc[i]["Design"]):
            total += 1
            if original_df.iloc[i]["Design"] == output_df.iloc[i]["predicted_design"]:
                correct += 1
            else:
                print(
                    f"Original: {original_df.iloc[i]['Design']}, Predicted: {output_df.iloc[i]['predicted_design']}")
    print(f"Total: {total}, Correct: {correct}")
    accuracy = (correct / total) * 100
    return accuracy


acc = calculate_accuracy(original_df[:2000], output_df)
print(f"Accuracy: {acc:.2f}%")
#
