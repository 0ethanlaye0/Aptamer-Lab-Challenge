import pandas as pd
import requests
import os
import re

df = pd.read_excel(r'C:\Users\0etha\research_tests\UTexas Aptamer Database dataset.xlsx')
df.columns = df.columns.str.strip()
df = df[df['Aptamer Sequence'].notna() & df['Kd (nM)'].notna() & df['Target'].notna()]

os.makedirs(r'C:\Users\0etha\research_tests\boltz_inputs', exist_ok=True)

def get_protein_sequence(target_name):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        'query': f'"{target_name}" AND reviewed:true',
        'format': 'json',
        'size': 1,
        'fields': 'sequence,protein_name'
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200 and r.text.strip():
            data = r.json()
            if not data['results']:
                return None
            result = data['results'][0]
            protein_names = str(result.get('proteinDescription', '')).lower()
            search_words = [w.lower() for w in target_name.split() if len(w) > 3]
            if not any(word in protein_names for word in search_words):
                return None
            return result['sequence']['value']
        return None
    except:
        return None

def clean_aptamer_sequence(seq):
    seq = str(seq)
    seq = re.sub(r"5'|3'|5′|3′|-", '', seq)
    seq = re.sub(r'\[.*?\]', '', seq)
    seq = re.sub(r'N\d*', '', seq)
    seq = seq.strip().upper()
    return seq

def clean_name(s):
    s = re.sub(r'[^\w\s-]', '', s)
    s = s.replace(' ', '_')
    return s[:40]

protein_cache = {}
generated = 0
skipped = 0

for idx, row in df.iterrows():
    target = str(row['Target']).strip()
    aptamer_seq = clean_aptamer_sequence(row['Aptamer Sequence'])
    nucleic_acid_type = str(row['Type of Nucleic Acid']).lower()
    serial = str(row['Serial Number']).strip()
    aptamer_name = str(row['Name of Aptamer']).strip() if pd.notna(row['Name of Aptamer']) else serial

    if not aptamer_seq or len(aptamer_seq) < 5:
        skipped += 1
        continue

    if target not in protein_cache:
        protein_cache[target] = get_protein_sequence(target)

    protein_seq = protein_cache[target]

    if not protein_seq:
        skipped += 1
        continue

    is_dna = "dna" in nucleic_acid_type
    na_key = "dna" if is_dna else "rna"

    complex_name = f"{clean_name(aptamer_name)}_{clean_name(target)}"
    filename = f"{serial}_{idx}_{complex_name}.yaml"

    yaml_content = f"""version: 1
sequences:
  - protein:
      id: A
      sequence: {protein_seq}
  - {na_key}:
      id: B
      sequence: {aptamer_seq}
properties:
  - affinity:
      binder: B
"""

    output_path = os.path.join(r'C:\Users\0etha\research_tests\boltz_inputs', filename)
    with open(output_path, 'w') as f:
        f.write(yaml_content)

    generated += 1
    print(f"Generated: {filename}")

print(f"\nDone. Generated: {generated}, Skipped: {skipped}")
