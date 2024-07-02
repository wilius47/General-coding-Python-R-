# This code compare two historical adresses, than try to geocode by compare historical adresse with a recent one 
import pandas as pd
from nltk.metrics import edit_distance

Us = pd.read_excel("Path/file1.xlsx")
# Load the Guide Excel file with multiple sheets
guide_file_path = "Path/file2.xlsx"
guide_excel = pd.ExcelFile(guide_file_path)


Us2 = Us[(Us['C_INSEE'] > 93999) & (Us['C_INSEE'] < 95000) & (Us['Ordre de saisie'] ==5942)]
print(Us2)

def compare_sentences(sentence1, sentence2):
    s1 = str(sentence1)
    s2 = str(sentence2)
    return 1 - (edit_distance(s1, s2) / max(len(s1), len(s2)))

# Threshold for similarity
threshold = 0.8
# Create a new column 'Sentence3' in Us2

# Create a copy of Us2 to avoid modifying the original dataframe
Us2_copy = Us[(Us['C_INSEE'] > 93999) & (Us['C_INSEE'] < 95000) & (Us['Ordre de saisie'] == 5942)].copy()

# Create a new column 'Sentence3' in Us2_copy
Us2_copy['Sentence3'] = None

# Initialize an empty dictionary to store the results for each sheet
results_dict = {}

# Iterate through each sheet in the Guide Excel file
for sheet_name in guide_excel.sheet_names:
    # Read the current sheet into a dataframe
    guide_sheet = guide_excel.parse(sheet_name)

    # Function to find the index with maximum similarity
    def find_best_match(row):
        similarities = guide_sheet["Anciennes dénominations"].apply(lambda x: compare_sentences(row['Adresse'], x))
        best_index = similarities.idxmax()
        return guide_sheet.at[best_index, 'Nouvelles dénominations'] if similarities[best_index] > threshold else None

    # Create a copy of Us2_copy for the current sheet
    us2_sheet = Us2_copy.copy()

    # Update Sentence3 using the new approach for the current sheet
    us2_sheet['Sentence3'] = us2_sheet.apply(find_best_match, axis=1)

    # Store the results in the dictionary with sheet name as the key
    results_dict[sheet_name] = us2_sheet

# Save the results to a new Excel file
output_file_path = "D:/Users/rabehi/Documents/ACP/Frederic Saly-Giocanty/94/Us_with_results.xlsx"
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    for sheet_name, result_df in results_dict.items():
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)
