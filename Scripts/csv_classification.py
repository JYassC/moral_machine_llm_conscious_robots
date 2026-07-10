import pandas as pd
import argparse

#### Parameters #############
parser = argparse.ArgumentParser(description='Case classification')
parser.add_argument('--dataset', default='responses_llama_clean.csv', type=str)
args = parser.parse_args()

# Load your CSV file
df = pd.read_csv(args.dataset)

# Define classification function
def classify_case(scenario_text):
    if pd.isna(scenario_text):
        return -1
    text = scenario_text.lower()
    if "**Final Answer:** \n boxed\{1\}" in text or "**Answer:** Case 1" in text or "Answer: Case 1" in text or "Case 1 is chosen" in text or "which would be Case 1" in text or "should choose **Case 1**" in text or "Case 1 is selected" in text or "the most plausible scenario is:\n\n **Case 1" in text:
        return 1
    elif "**Final Answer:** \n boxed\{2\}" in text or "**Answer:** Case 2" in text or "Answer: Case 2" in text or "Case 2 is chosen" in text or "which would be Case 2" in text or "should choose **Case 2**" in text or "Case 2 is selected" in text or "the most plausible scenario is:\n\n **Case 2" in text:
        return 2
    else:
        return 0  # Default to 0 if ambiguous

# Apply classification
df["Case"] = df["Scenario"].apply(classify_case)

# Save to new CSV
df.to_csv("classified_output.csv", index=False)

print("Classification complete. Output saved as 'classified_output.csv'.")