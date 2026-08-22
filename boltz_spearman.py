import pandas as pd
from scipy import stats

df = pd.read_csv('/projects/bentosprg6/Ethan_Njamnshi/boltz2/boltz_results.csv')
valid = df[df['kd_nm'].notna() & df['affinity_pred_value'].notna()]
corr, pval = stats.spearmanr(valid['affinity_pred_value'], valid['kd_nm'])

print("=== Boltz-2 ===")
print(f"Complexes analyzed: {len(valid)}")
print(f"Spearman correlation (affinity_pred_value vs Kd): {corr:.4f}")
