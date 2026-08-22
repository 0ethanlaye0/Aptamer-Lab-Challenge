import os
import json
import pandas as pd
from scipy import stats

output_dir = '/projects/bentosprg6/Ethan_Njamnshi/alphafold3/af3_output'
dataset_path = '/projects/bentosprg6/Ethan_Njamnshi/datasets/UTexas Aptamer Database dataset.xlsx'
input_dir = '/projects/bentosprg6/Ethan_Njamnshi/alphafold3/af3_inputs'

# Load dataset for Kd values
df = pd.read_excel(dataset_path)
df.columns = df.columns.str.strip()

# Build lookup from serial+name to Kd
kd_lookup = {}
for idx, row in df.iterrows():
    serial = str(row['Serial Number']).strip()
    aptamer_name = str(row['Name of Aptamer']).strip()
    kd = row['Kd (nM)']
    kd_lookup[f"{serial}_{idx}"] = {
        'kd': kd,
        'aptamer_name': aptamer_name,
        'target': str(row['Target']).strip()
    }

results = []

for complex_folder in os.listdir(output_dir):
    folder_path = os.path.join(output_dir, complex_folder)
    summary_path = os.path.join(folder_path, f'{complex_folder}_summary_confidences.json')
    if not os.path.exists(summary_path):
        continue

    with open(summary_path) as f:
        data = json.load(f)

    # Find matching JSON input file to get serial and idx
    matching_kd = None
    matching_name = None
    matching_target = None
    for json_file in os.listdir(input_dir):
        if json_file.endswith('.json'):
            parts = json_file.split('_', 2)
            if len(parts) >= 2:
                key = f"{parts[0]}_{parts[1]}"
                complex_name_from_file = '_'.join(json_file.split('_')[2:]).replace('.json','').lower()
                if complex_name_from_file == complex_folder:
                    if key in kd_lookup:
                        matching_kd = kd_lookup[key]['kd']
                        matching_name = kd_lookup[key]['aptamer_name']
                        matching_target = kd_lookup[key]['target']
                    break

    results.append({
        'complex_name': complex_folder,
        'aptamer_name': matching_name,
        'target': matching_target,
        'iptm': data.get('iptm'),
        'ptm': data.get('ptm'),
        'ranking_score': data.get('ranking_score'),
        'kd_nm': matching_kd
    })

results_df = pd.DataFrame(results)

# Sort by iptm
results_df = results_df.sort_values('iptm', ascending=False)

# Spearman correlation between iptm and Kd (only rows with both values)
valid = results_df[results_df['kd_nm'].notna() & results_df['iptm'].notna()].copy()

if len(valid) > 2:
    # Lower Kd = stronger binding, higher iptm = better prediction
    # So we expect negative correlation between iptm and Kd
    corr, pval = stats.spearmanr(valid['iptm'], valid['kd_nm'])
    print(f"\nSpearman correlation (iptm vs Kd): {corr:.4f} (p={pval:.4f})")
    print(f"Interpretation: {'negative correlation as expected' if corr < 0 else 'positive correlation — unexpected'}")
else:
    print("Not enough data points for correlation")

# Save results
output_path = '/projects/bentosprg6/Ethan_Njamnshi/alphafold3/results.csv'
results_df.to_csv(output_path, index=False)
print(f"\nResults saved to {output_path}")
print(results_df.to_string())
