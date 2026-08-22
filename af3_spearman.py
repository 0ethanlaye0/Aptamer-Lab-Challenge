import pandas as pd
from scipy import stats

df = pd.read_csv('/projects/bentosprg6/Ethan_Njamnshi/alphafold3/af3_results.csv')
valid = df[df['kd_nm'].notna() & df['iptm'].notna()]
corr, pval = stats.spearmanr(valid['iptm'], valid['kd_nm'])

print("=== AlphaFold 3 ===")
print(f"Complexes analyzed: {len(valid)}")
print(f"Spearman correlation (iPTM vs Kd): {corr:.4f}")
