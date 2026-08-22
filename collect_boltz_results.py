import os
import json
import pandas as pd
from scipy import stats

output_dir = '/projects/bentosprg6/Ethan_Njamnshi/boltz2/boltz_output/boltz_results_boltz_inputs/predictions'
dataset_path = '/projects/bentosprg6/Ethan_Njamnshi/datasets/UTexas Aptamer Database dataset.xlsx'

df = pd.read_excel(dataset_path)
df.columns = df.columns.str.strip()

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
    if not os.path.isdir(folder_path):
        continue

    affinity_path = os.path.join(folder_path, f'affinity_{complex_folder}.json')
    confidence_path = os.path.join(folder_path, f'confidence_{complex_folder}_model_0.json')

    if not os.path.exists(affinity_path):
        continue

    with open(affinity_path) as f:
        affinity_data = json.load(f)

    confidence_data = {}
    if os.path.exists(confidence_path):
        with open(confidence_path) as f:
            confidence_data = json.load(f)

    # Extract serial and idx directly from folder name
    parts = complex_folder.split('_')
    serial = parts[0]
    idx = parts[1]
    key = f"{serial}_{idx}"

    matching_kd = None
    matching_name = None
    matching_target = None

    if key in kd_lookup:
        matching_kd = kd_lookup[key]['kd']
        matching_name = kd_lookup[key]['aptamer_name']
        matching_target = kd_lookup[key]['target']

    results.append({
        'complex_name': complex_folder,
        'aptamer_name': matching_name,
        'target': matching_target,
        'affinity_pred_value': affinity_data.get('affinity_pred_value'),
        'affinity_probability_binary': affinity_data.get('affinity_probability_binary'),
        'iptm': confidence_data.get('iptm'),
        'ptm': confidence_data.get('ptm'),
        'kd_nm': matching_kd
    })

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('affinity_pred_value', ascending=True)

valid = results_df[results_df['kd_nm'].notna() & results_df['affinity_pred_value'].notna()].copy()

if len(valid) > 2:
    corr, pval = stats.spearmanr(valid['affinity_pred_value'], valid['kd_nm'])
    print(f"\nSpearman correlation (affinity_pred_value vs Kd): {corr:.4f} (p={pval:.4f})")
else:
    print("Not enough data points for correlation")

output_path = '/projects/bentosprg6/Ethan_Njamnshi/boltz2/boltz_results.csv'
results_df.to_csv(output_path, index=False)
print(f"\nResults saved to {output_path}")
print(results_df.to_string())
