import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import joblib
import sys

# Load models and data
model = xgb.XGBClassifier()
model.load_model("xgb_model.json")
explainer = joblib.load("shap_explainer.pkl")
feature_names = joblib.load("feature_names.pkl")

laptops = pd.read_csv("laptop_matched.csv")
cpu_df = pd.read_csv("cpu_cleaned.csv")
gpu_df = pd.read_csv("gpu_cleaned.csv")
games = pd.read_csv("Videogame_Requirements.csv")

# Enrich laptops
laptop_rich = pd.merge(laptops, cpu_df, left_on='Matched_CPU', right_on='CPU', how='left')
laptop_rich = pd.merge(laptop_rich, gpu_df, left_on='Matched_GPU', right_on='GPU', how='left')
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

def predict_performance(laptop_id, game_name):
    lap = laptop_rich[laptop_rich['LaptopID'] == laptop_id]
    if len(lap) == 0:
        return "Laptop not found."
    lap = lap.iloc[0]
    
    game = games[games['Name'].str.contains(game_name, case=False, na=False)]
    if len(game) == 0:
        return "Game not found."
    game = game.iloc[0]
    
    # Construct feature array
    try:
        min_gpu = float(game['Min_GPU_Memory(MB)']) if not pd.isna(game['Min_GPU_Memory(MB)']) else 0
    except:
        min_gpu = 0
        
    try:
        rec_gpu = float(game['Recom_GPU_Memory(MB)']) if not pd.isna(game['Recom_GPU_Memory(MB)']) else 0
    except:
        rec_gpu = 0

    def clean_ram(val):
        try: return float(val)
        except: return 4.0

    min_ram = clean_ram(game['Min_Ram(GB)'])
    rec_ram = clean_ram(game['Recom_RAM(GB)'])

    data = {
        'Laptop_Ram_GB': lap['Laptop_Ram_GB'],
        'Max_Cores': lap['Max_Cores'],
        'Max_Clock(MHz)': lap['Max_Clock(MHz)'],
        'Memory (GB)': lap['Memory (GB)'],
        'GPU_Bandwidth': lap['GPU_Bandwidth'],
        'CPU_HPI': lap['CPU_HPI'],
        'GPU_HPI': lap['GPU_HPI'],
        'Min_CPU_Cores': float(game['Min_CPU_Cores']) if not pd.isna(game['Min_CPU_Cores']) else 0,
        'Min_GPU_Memory(MB)': min_gpu,
        'Min_Ram(GB)': min_ram,
        'Recom_CPU_Cores': float(game['Recom_CPU_Cores']) if not pd.isna(game['Recom_CPU_Cores']) else 0,
        'Recom_GPU_Memory(MB)': rec_gpu,
        'Recom_RAM(GB)': rec_ram,
    }
    
    df = pd.DataFrame([data])
    
    # Predict
    pred = model.predict(df)[0]
    classes = {0: "Cannot Run (Under Min)", 1: "Playable (Meets Min)", 2: "Optimal (Meets Recom)"}
    result = classes.get(pred, "Unknown")
    
    print("=" * 50)
    print(f"Prediction for Laptop: {lap['Company']} - {lap['CPU_x']} / {lap['Gpu']}")
    print(f"Game: {game['Name']}")
    print(f"--> RESULT: {result}")
    
    # Bottleneck Analysis using SHAP
    if pred != 2:
        print("\n--- Bottleneck Analysis (SHAP) ---")
        shap_vals = explainer.shap_values(df)
        
        # Explain why it didn't predict optimal (Class 2) or playable (Class 1)
        target_class = pred 
        # But we really want to know what features pushed it AWAY from class 2.
        # Shap values shape: (n_samples, n_features, n_classes) or list of classes
        # For class 2 (Optimal)
        if isinstance(shap_vals, list):
            class_2_shap = shap_vals[2][0]
        else: # sometimes 3D array
            class_2_shap = shap_vals[0, :, 2]
            
        feature_impacts = list(zip(feature_names, class_2_shap))
        # Sort by most negative impact (features pulling the prediction DOWN from Optimal)
        feature_impacts.sort(key=lambda x: x[1])
        
        print("Top Missing Requirements / Bottlenecks:")
        for feat, impact in feature_impacts[:3]:
            if impact < -0.1:
                val = df[feat].values[0]
                print(f"- {feat} (Current: {val}) is holding performance back.")
        
    print("=" * 50)

if __name__ == "__main__":
    predict_performance(422, "Cyberpunk 2077")
