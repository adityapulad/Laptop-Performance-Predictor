import os
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import joblib
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load models and data globally
print("Loading model and datasets...")
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

# Cache options for the frontend
laptop_options = []
for _, row in laptop_rich.iterrows():
    name = f"[{row['Company']}] {row['CPU_x']} | {row['Gpu']} | {row['Ram']} RAM"
    laptop_options.append({"id": row['LaptopID'], "name": name})

game_options = list(games['Name'].dropna().unique())

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dream')
def dream():
    return render_template("dream.html")

@app.route('/api/options', methods=['GET'])
def get_options():
    return jsonify({
        "laptops": laptop_options,
        "games": game_options
    })

@app.route('/api/predict', methods=['POST'])
def predict_endpoint():
    data_in = request.json
    laptop_id = int(data_in.get('laptop_id'))
    game_name = data_in.get('game_name')
    
    lap = laptop_rich[laptop_rich['LaptopID'] == laptop_id]
    if len(lap) == 0:
        return jsonify({"error": "Laptop not found"}), 404
    lap = lap.iloc[0]
    
    game = games[games['Name'].str.contains(game_name, case=False, na=False, regex=False)]
    if len(game) == 0:
        return jsonify({"error": "Game not found"}), 404
    game = game.iloc[0]
    
    try: min_gpu = float(game['Min_GPU_Memory(MB)']) if not pd.isna(game['Min_GPU_Memory(MB)']) else 0
    except: min_gpu = 0
        
    try: rec_gpu = float(game['Recom_GPU_Memory(MB)']) if not pd.isna(game['Recom_GPU_Memory(MB)']) else 0
    except: rec_gpu = 0

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
    
    pred = model.predict(df)[0]
    classes = {0: "Cannot Run", 1: "Playable (Meets Minimum)", 2: "Optimal (Meets Recommended)"}
    result = classes.get(int(pred), "Unknown")
    
    bottlenecks = []
    if pred != 2:
        shap_vals = explainer.shap_values(df)
        if isinstance(shap_vals, list):
            class_2_shap = shap_vals[2][0]
        else:
            class_2_shap = shap_vals[0, :, 2]
            
        feature_impacts = list(zip(feature_names, class_2_shap))
        feature_impacts.sort(key=lambda x: x[1])
        
        for feat, impact in feature_impacts[:3]:
            if impact < -0.1:
                val = df[feat].values[0]
                bottlenecks.append({"feature": feat, "value": val, "impact": float(impact)})

    return jsonify({
        "laptop": f"{lap['Company']} - {lap['CPU_x']} / {lap['Gpu']}",
        "game": game['Name'],
        "prediction": result,
        "prediction_code": int(pred),
        "bottlenecks": bottlenecks
    })

@app.route('/api/predict_dream', methods=['POST'])
def predict_dream_endpoint():
    data_in = request.json
    
    cores = float(data_in.get('cores', 8))
    ram = float(data_in.get('ram', 16))
    vram = float(data_in.get('vram', 8))
    game_name = data_in.get('game_name')
    
    game = games[games['Name'].str.contains(game_name, case=False, na=False, regex=False)]
    if len(game) == 0:
        return jsonify({"error": "Game not found"}), 404
    game = game.iloc[0]
    
    try: min_gpu = float(game['Min_GPU_Memory(MB)']) if not pd.isna(game['Min_GPU_Memory(MB)']) else 0
    except: min_gpu = 0
        
    try: rec_gpu = float(game['Recom_GPU_Memory(MB)']) if not pd.isna(game['Recom_GPU_Memory(MB)']) else 0
    except: rec_gpu = 0

    def clean_ram(val):
        try: return float(val)
        except: return 4.0

    min_ram = clean_ram(game['Min_Ram(GB)'])
    rec_ram = clean_ram(game['Recom_RAM(GB)'])

    # Using high-end modern defaults for unverifiable stats like clock and bandwith
    data = {
        'Laptop_Ram_GB': ram,
        'Max_Cores': cores,
        'Max_Clock(MHz)': 4500.0,
        'Memory (GB)': vram,
        'GPU_Bandwidth': 400000.0,
        'CPU_HPI': 3000.0,
        'GPU_HPI': 250000.0,
        'Min_CPU_Cores': float(game['Min_CPU_Cores']) if not pd.isna(game['Min_CPU_Cores']) else 0,
        'Min_GPU_Memory(MB)': min_gpu,
        'Min_Ram(GB)': min_ram,
        'Recom_CPU_Cores': float(game['Recom_CPU_Cores']) if not pd.isna(game['Recom_CPU_Cores']) else 0,
        'Recom_GPU_Memory(MB)': rec_gpu,
        'Recom_RAM(GB)': rec_ram,
    }
    
    df = pd.DataFrame([data])
    
    pred = model.predict(df)[0]
    classes = {0: "Cannot Run", 1: "Playable (Meets Minimum)", 2: "Optimal (Meets Recommended)"}
    result = classes.get(int(pred), "Unknown")
    
    bottlenecks = []
    if pred != 2:
        shap_vals = explainer.shap_values(df)
        if isinstance(shap_vals, list):
            class_2_shap = shap_vals[2][0]
        else:
            class_2_shap = shap_vals[0, :, 2]
            
        feature_impacts = list(zip(feature_names, class_2_shap))
        feature_impacts.sort(key=lambda x: x[1])
        
        for feat, impact in feature_impacts[:3]:
            # For dream stats, only highlight custom inputs if they bottleneck
            if impact < -0.1 and feat in ['Laptop_Ram_GB', 'Max_Cores', 'Memory (GB)']:
                val = df[feat].values[0]
                feat_name = "VRAM" if "Memory" in feat else feat
                bottlenecks.append({"feature": feat_name, "value": val, "impact": float(impact)})

    return jsonify({
        "laptop": f"Custom Dream Rig",
        "game": game['Name'],
        "prediction": result,
        "prediction_code": int(pred),
        "bottlenecks": bottlenecks
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
