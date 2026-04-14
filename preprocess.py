import pandas as pd
import numpy as np
import re

# Load data
print("Loading datasets...")
cpu_df = pd.read_csv("CPU_Specs.csv")
gpu_df = pd.read_csv("GPU_Specs.csv")
laptop_df = pd.read_csv("Laptop_Data.csv")
game_reqs_df = pd.read_csv("Videogame_Requirements.csv")

print("--- CPU Data Initial ---")
print(cpu_df.head())
print(cpu_df.columns)

print("--- GPU Data Initial ---")
print(gpu_df.head())
print(gpu_df.columns)

# 1. Clean CPU Data
print("\n--- Cleaning CPU Data ---")
# Keep relevant columns and fill NA
cpu_clean = cpu_df[['CPU', 'Min_Cores', 'Max_Cores', 'Max_Clock(MHz)', 'Process(NM)', 'TDP(Watts)', 'Release']].copy()

# Function to parse release year from strings like "Oct 9th, 2012"
def extract_year(date_str):
    if pd.isna(date_str) or date_str == 'Unknown':
        return 2014 # default middle year
    match = re.search(r'\b(19\d{2}|20\d{2})\b', str(date_str))
    return int(match.group(1)) if match else 2014

cpu_clean['Release_Year'] = cpu_clean['Release'].apply(extract_year)

# Numeric conversions
cpu_clean['Min_Cores'] = pd.to_numeric(cpu_clean['Min_Cores'], errors='coerce').fillna(2)
cpu_clean['Max_Cores'] = pd.to_numeric(cpu_clean['Max_Cores'], errors='coerce').fillna(2)
cpu_clean['Max_Clock(MHz)'] = pd.to_numeric(cpu_clean['Max_Clock(MHz)'], errors='coerce').fillna(1000)

# Process(NM) could have string or space, convert safely
def extract_nm(val):
    if pd.isna(val): return 28.0 # default
    match = re.search(r'(\d+)', str(val))
    return float(match.group(1)) if match else 28.0

cpu_clean['Process(NM)'] = cpu_clean['Process(NM)'].apply(extract_nm)
cpu_clean['TDP(Watts)'] = pd.to_numeric(cpu_clean['TDP(Watts)'], errors='coerce').fillna(65.0)

# Calculate a naive proxy "CPU_HPI" (Hardware Performance Index)
# more cores, higher clock, lower process nm is better
cpu_clean['CPU_HPI'] = (cpu_clean['Max_Cores'] * cpu_clean['Max_Clock(MHz)']) / cpu_clean['Process(NM)']
print("CPU Cleaned Sample:")
print(cpu_clean.head())

# 2. Clean GPU Data
print("\n--- Cleaning GPU Data ---")
gpu_clean = gpu_df[['GPU', 'Memory (GB)', 'Memory_bus(BIT)', 'Memory_Clock(MHz)', 'Year_Released']].copy()

# Clean Memory (GB) - Could have strings
def extract_gb(val):
    if pd.isna(val): return 2.0
    match = re.search(r'(\d+)', str(val))
    return float(match.group(1)) if match else 2.0

gpu_clean['Memory (GB)'] = gpu_clean['Memory (GB)'].apply(extract_gb)

# Clean BUS and Clock
gpu_clean['Memory_bus(BIT)'] = pd.to_numeric(gpu_clean['Memory_bus(BIT)'], errors='coerce').fillna(128.0)
gpu_clean['Memory_Clock(MHz)'] = pd.to_numeric(gpu_clean['Memory_Clock(MHz)'], errors='coerce').fillna(1000.0)

def gpu_year(val):
    if pd.isna(val) or val == 'Unknown\n': return 2014
    match = re.search(r'(\d{4})', str(val))
    return int(match.group(1)) if match else 2014

gpu_clean['Year_Released'] = gpu_clean['Year_Released'].apply(gpu_year)

# Calculate approximate Memory Bandwidth
gpu_clean['GPU_Bandwidth'] = gpu_clean['Memory_bus(BIT)'] * gpu_clean['Memory_Clock(MHz)']
gpu_clean['GPU_HPI'] = gpu_clean['Memory (GB)'] * gpu_clean['GPU_Bandwidth']

print("GPU Cleaned Sample:")
print(gpu_clean.head())

cpu_clean.to_csv("cpu_cleaned.csv", index=False)
gpu_clean.to_csv("gpu_cleaned.csv", index=False)
print("\nSaved intermediate data files to cpu_cleaned.csv and gpu_cleaned.csv")
