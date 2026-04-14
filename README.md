# 💻 Laptop Gaming Performance Predictor

An advanced Machine Learning platform built to determine if your specific laptop hardware can run heavily demanding video games, featuring a full-stack Flask/Vanilla JS Web Application and SHAP-powered Bottleneck Analytics.

![Platform Screenshot](./static/css/screenshot-placeholder.png) <!-- Replace with an actual screenshot later -->

## 🔥 Core Features

- **XGBoost Pipeline**: A highly accurate multi-class prediction model (`0`: Cannot Run, `1`: Playable, `2`: Optimal) that learns complex architectural limits across different generations of laptop tech.
- **SHAP Bottleneck Detection**: If a laptop is predicted as unable to optimally run a game, the system parses the predictive matrix using `SHAP (SHapley Additive exPlanations)` to explicitly output exactly *why* it failed (e.g., "Your CPU Cores are bottlenecking this game").
- **Massive Normalized Dataset**: Developed by NLP-fuzzy matching over 1,200 unique laptops against performance specifications spanning 7,000+ distinct videogames.
- **Dream Builder Interface**: A custom "What If" testbed allowing users to drag sliders to build modern, hypothetical 2024-era setups (such as RTX 4090s and Core i9 configurations) and instantly check their capabilities without buying the hardware.
- **Glassmorphism Web UI**: A blazing fast frontend built dynamically connected to the deployed Flask backend.

## ⚙️ Architecture

The backend synthesizes a feature matrix containing deeply engineered indices (Hardware Performance Indices - **HPI**, Theoretical Memory Bandwidth interpolations) instead of relying solely on raw clock speeds. 

**Technologies Used**: 
- *Machine Learning Backend*: Python, XGBoost, Scikit-learn, SHAP, Pandas.
- *Web Server Deployment Base*: Flask, Gunicorn.
- *Frontend Implementation*: Vanilla HTML5, CSS3 (Custom Glass UI), JavaScript.

## 🚀 How to Run Locally

You can run this full machine-learning backend and the web app completely locally. 

### Prerequisites
Make sure you have Python 3.9+ installed and clone the repository.
```bash
git clone https://github.com/adityapulad/Laptop-Performance-Predictor.git
cd Laptop-Performance-Predictor
```

### Installation
Install all backend dependencies via standard PIP.
```bash
pip install -r requirements.txt
```

### Launch the Application
Start the Flask application server.
```bash
python app.py
```
Open a browser and navigate to exactly `http://127.0.0.1:5000` to interact with your local platform.

---

## ☁️ Deployment instructions
This repository is optimized automatically for deployment on hosting platforms like **Render**, **Heroku**, or **PythonAnywhere**. It includes a generated `requirements.txt` and a `Procfile` mapping cleanly to `gunicorn app:app`. Just link your GitHub repository to Render as a "Web Service" and it will deploy for free!
