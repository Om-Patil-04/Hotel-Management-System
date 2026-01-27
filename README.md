# 🏨 Hotel Reservation Prediction – End-to-End ML Pipeline

A production-ready machine learning pipeline that predicts hotel reservation cancellations using clean, modular code and reproducible workflows.

---

## 🛠 Tech Stack

- **Language**: Python  
- **Data Processing**: Pandas, NumPy  
- **Modeling**: Scikit-learn, XGBoost, LightGBM  
- **Experiment Tracking**: MLflow  
- **Pipeline Orchestration**: Custom Python pipeline  
- **Logging**: Python `logging`  

---

## 📌 Problem Statement

Hotel reservation cancellations create operational and revenue risks.  
This system predicts whether a reservation will be canceled, helping hotels:

- Reduce overbooking losses  
- Improve pricing strategies  
- Optimize room allocation  

**ML Task**: Binary Classification  
**Target**: booking_status (Canceled / Not_Canceled)

---

## 🧠 ML Workflow

```
Raw Data
   ↓
Data Ingestion
   ↓
Data Preprocessing
   ↓
Feature Selection
   ↓
Model Training & Selection
   ↓
MLflow Tracking
   ↓
Best Model Saved
```

---

## 📁 Project Structure

```
PROJECT/
├── artifacts/
├── build/
├── config/
│   ├── __init__.py
│   ├── config.yaml
│   ├── model_params.py
│   └── paths_config.py
├── custom_jenkins/
│   └── Dockerfile
├── HotelReservationIO.egg-info/
├── Logs/
├── mlruns/
├── models/
│   ├── best_model/
│   │   └── model.pkl
│   └── selection_candidates/
│       └── xgboost_model_artifact.joblib
├── notebooks/
│   └── model_selection_and_training.ipynb
├── pipeline/
│   ├── __init__.py
│   └── training_pipeline.py
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── logger.py
│   └── exceptions.py
├── templates/
│   └── index.html
├── utils/
├── venv/
├── .gitignore
├── application.py
├── Dockerfile
├── Jenkinsfile
├─�� mlflow.db
├── README.md
├── requirement-train.txt
├── requirements.txt
└── setup.py
```

---

## ⚙️ Configuration

All pipeline settings are driven through configuration files in `config/`.  
This keeps the system portable and environment-agnostic.

---

## 🚫 Ignored Artifacts

Generated folders and files are excluded from version control:

```
artifacts/
models/
mlruns/
Logs/
build/
*.egg-info/
mlflow.db
venv/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd Hotel-Management-System
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Run the Training Pipeline

```bash
python pipeline/training_pipeline.py
```

This will:

- Load raw data  
- Preprocess features  
- Train candidate models  
- Track experiments with MLflow  
- Save the best model  

---

## 📊 MLflow UI

```bash
mlflow ui
```

Open:

```
http://localhost:5000
```

---

## 🧪 Model Development

Optional exploration is available in:

```
notebooks/model_selection_and_training.ipynb
```

The pipeline runs independently of notebooks.

---

## ✅ Engineering Highlights

- Modular architecture  
- Clean separation of concerns  
- Centralized logging & exception handling  
- Reproducible training  
- MLflow integration  
- Production-ready pipeline structure  

---

## 📄 License

MIT License