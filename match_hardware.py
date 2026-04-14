import pandas as pd
import numpy as np
import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import json
import os

print("Loading cleaned datasets & raw target sets...")
cpu_clean = pd.read_csv("cpu_cleaned.csv")
gpu_clean = pd.read_csv("gpu_cleaned.csv")
laptop_df = pd.read_csv("Laptop_Data.csv")
game_reqs_df = pd.read_csv("Videogame_Requirements.csv")

cpu_names = cpu_clean['CPU'].dropna().unique()
gpu_names = gpu_clean['GPU'].dropna().unique()

print("Setting up NLP Matching Cache...")
# Try caching matches because fuzzywuzzy is slow on large df
cpu_cache = {}
gpu_cache = {}
if os.path.exists("cache.json"):
    with open("cache.json", "r") as f:
        cache = json.load(f)
        cpu_cache = cache.get("cpu", {})
        gpu_cache = cache.get("gpu", {})

def match_cpu(query):
    if pd.isna(query): return None
    query = str(query).replace("Intel", "").replace("AMD", "").strip()
    if query in cpu_cache: return cpu_cache[query]
    
    # Simple token set ratio is better for specs
    match = process.extractOne(query, cpu_names, scorer=fuzz.token_set_ratio)
    if match and match[1] > 60:
        cpu_cache[query] = match[0]
        return match[0]
    cpu_cache[query] = None
    return None

def match_gpu(query):
    if pd.isna(query): return None
    query = str(query).replace("Nvidia", "").replace("AMD", "").replace("Intel", "").strip()
    if query in gpu_cache: return gpu_cache[query]
    
    match = process.extractOne(query, gpu_names, scorer=fuzz.token_set_ratio)
    if match and match[1] > 60:
        gpu_cache[query] = match[0]
        return match[0]
    gpu_cache[query] = None
    return None

print("Mapping Laptop Data...")
# We take a sample to speed up if testing, but here we run full
laptop_df['Matched_CPU'] = laptop_df['CPU'].apply(match_cpu)
laptop_df['Matched_GPU'] = laptop_df['Gpu'].apply(match_gpu)

print("Mapping Videogame Requirements Data...")
# Videogame requirements typically have Minimum CPU, Minimum GPU etc.
# Need to check actual column names
print("Game columns:", game_reqs_df.columns)

# Usually Videogame Requirements have: 'Name', 'Minimum CPU', 'Minimum GPU', 'Minimum RAM', 'Recommended CPU', 'Recommended GPU', 'Recommended RAM'
# Let's clean RAM into numeric
def extract_ram(val):
    if pd.isna(val): return 4.0
    match = re.search(r'(\d+)', str(val))
    return float(match.group(1)) if match else 4.0

if 'Requirements_Minimum_CPU' in game_reqs_df.columns:
    # Just generic columns check
    pass 
else:
    print("WARNING: Need to check actual videogame requirement columns.")

# Let's print out what we matched for laptops
print("Laptop Match Success Rate:")
print(f"CPU: {laptop_df['Matched_CPU'].notna().mean() * 100:.2f}%")
print(f"GPU: {laptop_df['Matched_GPU'].notna().mean() * 100:.2f}%")

laptop_df.to_csv("laptop_matched.csv", index=False)

with open("cache.json", "w") as f:
    json.dump({"cpu": cpu_cache, "gpu": gpu_cache}, f)

print("Done with basic mapping.")
