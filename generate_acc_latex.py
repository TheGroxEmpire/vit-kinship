import os
import re
import collections
import pandas as pd

# Dictionary to map feature fusion names to LaTeX expressions
feature_fusion_dict = {
    'features_only': '$x \\oplus y$',
    'input_dis_and_square_diff_and_multiplication': '$(x-y)^2 \\oplus (x^2-y^2) \\oplus (x \\cdot y)$',
    'multiplication_and_input_dis': '$(x \\cdot y) \\oplus (x-y)^2$',
    'multiplication_only': '$(x \\cdot y)$',
    'square_diff_and_input_dis': '$(x^2-y^2) \\oplus (x-y)^2$',
    'square_diff_and_multiplication': '$(x^2-y^2) \\oplus (x \\cdot y)$',
    'square_diff_only': '$(x^2-y^2)$'
}

processed_backbones = set()  # To keep track of processed backbones

def parse_csv_filename(filename):
    # Extract backbone and feature fusion information from the filename
    match = re.match(r'([a-zA-Z0-9]+)_([a-zA-Z_]+)_accuracy\.csv', filename)
    if match:
        backbone, feature_fusion = match.groups()
        return backbone.capitalize(), feature_fusion
    else:
        return None, None

def generate_latex_table(df, backbone, feature_fusion):
    # If the filtered DataFrame is empty, return an empty string
    if df.empty:
        return ''

    # Merged model name for LaTeX code
    latex_model_name = f"% {backbone}_{feature_fusion}"
    
    # Generate the LaTeX code without 'average' and 'nan'
    if backbone not in processed_backbones:
        latex_code = f"\midrule \n{latex_model_name} \n\\multirow{{7}}{{*}}{{{backbone}}} & {feature_fusion_dict[feature_fusion]} "

        # Iterate through rows of the DataFrame
        for _, row in df.iterrows():
            formatted_value = str(row['accuracy'])

            # Add the formatted value to the LaTeX code
            latex_code += f" & {formatted_value}"

        # Add the row ending and processed backbone
        latex_code += " \\\\\n"
        processed_backbones.add(backbone)
    else:
        latex_code = f"{latex_model_name} \n& {feature_fusion_dict[feature_fusion]} "

        # Iterate through rows of the DataFrame
        for _, row in df.iterrows():
            formatted_value = str(row['accuracy'])

            # Add the formatted value to the LaTeX code
            latex_code += f" & {formatted_value}"

        # Add the row ending
        latex_code += " \\\\\n"

    return latex_code

# Folder containing CSV files
csv_folder = 'evaluation/acc_csv'

# Output LaTeX file
latex_output_file = 'accuracy_results.tex'

# Iterate through df_dict to generate LaTeX code
with open(latex_output_file, 'w') as latex_file:
    # LaTeX document preamble
    latex_file.write(r'\documentclass{article}' + '\n')
    latex_file.write(r'\usepackage{geometry}' + '\n')
    latex_file.write(r'\usepackage{booktabs}' + '\n')
    latex_file.write(r'\usepackage{multirow}' + '\n')
    latex_file.write(r'\usepackage{xcolor}' + '\n\n')

    latex_file.write(r'\begin{document}' + '\n\n')

    latex_file.write(r'\begin{table}[htbp]' + '\n')
    latex_file.write(r'\centering' + '\n')
    latex_file.write(r'\caption{Accuracy Results}' + '\n')
    latex_file.write(r'\label{tab:accuracy_results}' + '\n')
    latex_file.write(r'\begin{tabular}{lcccccccccc}' + '\n')
    latex_file.write(r'\toprule' + '\n')
    latex_file.write(r'\textbf{Backbone} & \textbf{Feature Fusion} & \textbf{FD} & \textbf{FS} & \textbf{MD} & \textbf{MS} & \textbf{SS} & \textbf{BB} & \textbf{SiBs} & \textbf{Average} \\' + '\n')

    # Iterate through CSV files in the specified folder
    for idx, csv_file in enumerate(os.listdir(csv_folder)):
        if csv_file.endswith('.csv'):
            # Extract backbone and feature fusion from the file name
            backbone, feature_fusion = parse_csv_filename(csv_file)

            if backbone and feature_fusion:
                # Construct the full path to the CSV file
                csv_path = os.path.join(csv_folder, csv_file)

                # Read CSV and calculate average
                df = pd.read_csv(csv_path)

                latex_code = generate_latex_table(df, backbone, feature_fusion)
                latex_file.write(latex_code)

    # LaTeX document ending
    latex_file.write(r'\bottomrule' + '\n')
    latex_file.write(r'\end{tabular}' + '\n')
    latex_file.write(r'\end{table}' + '\n\n')
    latex_file.write(r'\end{document}' + '\n')

print(f'LaTeX code saved to {latex_output_file}')
