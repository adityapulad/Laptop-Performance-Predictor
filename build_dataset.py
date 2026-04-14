import pandas as pd
import numpy as np
import random

print("Loading data...")
laptop_df = pd.read_csv("laptop_matched.csv")
cpu_df = pd.read_csv("cpu_cleaned.csv")
gpu_df = pd.read_csv("gpu_cleaned.csv")
games_df = pd.read_csv("Videogame_Requirements.csv")

print("Enriching laptops...")
# Merge laptop with CPU and GPU specs
laptop_rich = pd.merge(laptop_df, cpu_df, left_on='Matched_CPU', right_on='CPU', how='left')
laptop_rich = pd.merge(laptop_rich, gpu_df, left_on='Matched_GPU', right_on='GPU', how='left')

# Fill missing specs with median logic or defaults
laptop_rich['Max_Cores'] = laptop_rich['Max_Cores'].fillna(4)
laptop_rich['Max_Clock(MHz)'] = laptop_rich['Max_Clock(MHz)'].fillna(2500)
laptop_rich['Memory (GB)'] = laptop_rich['Memory (GB)'].fillna(2)
laptop_rich['GPU_Bandwidth'] = laptop_rich['GPU_Bandwidth'].fillna(100000)
laptop_rich['CPU_HPI'] = laptop_rich['CPU_HPI'].fillna(1000)
laptop_rich['GPU_HPI'] = laptop_rich['GPU_HPI'].fillna(100000)

def extract_ram(val):
    if pd.isna(val): return 8.0
    match = pd.Series(str(val)).str.extract(r'(\d+)')[0][0]
    try: return float(match)
    except: return 8.0

laptop_rich['Laptop_Ram_GB'] = laptop_rich['Ram'].apply(extract_ram)

print("Preparing pairs...")
# Random sample of combinations to avoid 9 million rows (let's do 250,000 pairs for training)
laptops_sampled = laptop_rich.sample(n=250000, replace=True, random_state=42).reset_index(drop=True)
games_sampled = games_df.sample(n=250000, replace=True, random_state=42).reset_index(drop=True)

dataset = pd.concat([laptops_sampled, games_sampled], axis=1)

# Clean Game numeric cols safely
for col in ['Min_CPU_Cores', 'Recom_CPU_Cores', 'Min_GPU_Memory(MB)', 'Recom_GPU_Memory(MB)']:
    dataset[col] = pd.to_numeric(dataset[col], errors='coerce').fillna(0)

def clean_game_ram(val):
    if pd.isna(val) or val == '#VALUE!': return 4.0
    return float(val)

dataset['Min_Ram(GB)'] = dataset['Min_Ram(GB)'].apply(clean_game_ram)
dataset['Recom_RAM(GB)'] = dataset['Recom_RAM(GB)'].apply(clean_game_ram)

print("Generating target labels...")
# Logical Check: 
# Meets min: Laptop Cores >= Min Cores & Laptop RAM >= Min RAM & Laptop GPU Mem >= Min GPU Mem/1024
# Meets rec: Laptop Cores >= Recom Cores & Laptop RAM >= Recom RAM & Laptop GPU Mem >= Recom GPU Mem/1024

def get_label(row):
    try:
        cpu_min_met = row['Max_Cores'] >= row['Min_CPU_Cores']
        gpu_min_met = row['Memory (GB)'] >= (row['Min_GPU_Memory(MB)'] / 1024)
        ram_min_met = row['Laptop_Ram_GB'] >= row['Min_Ram(GB)']
        min_met = cpu_min_met and gpu_min_met and ram_min_met

        cpu_rec_met = row['Max_Cores'] >= row['Recom_CPU_Cores']
        gpu_rec_met = row['Memory (GB)'] >= (row['Recom_GPU_Memory(MB)'] / 1024)
        ram_rec_met = row['Laptop_Ram_GB'] >= row['Recom_RAM(GB)']
        rec_met = cpu_rec_met and gpu_rec_met and ram_rec_met
        
        if rec_met:
            return 2 # Optimal
        elif min_met:
            return 1 # Playable
        else:
            return 0 # Under Min
    except:
        return 0

dataset['Target'] = dataset.apply(get_label, axis=1)

# Keep relevant features for ML
features = [
    'Laptop_Ram_GB', 'Max_Cores', 'Max_Clock(MHz)', 'Memory (GB)', 'GPU_Bandwidth', 
    'CPU_HPI', 'GPU_HPI',
    'Min_CPU_Cores', 'Min_GPU_Memory(MB)', 'Min_Ram(GB)',
    'Recom_CPU_Cores', 'Recom_GPU_Memory(MB)', 'Recom_RAM(GB)',
    'Target'
]

final_df = dataset[features]

print("Class distribution:")
print(final_df['Target'].value_counts(normalize=True))

final_df.to_csv("training_data.csv", index=False)
print("Saved training_data.csv with", len(final_df), "rows.")
