# 🏨 Hotel Reservation Prediction – End-to-End ML Pipeline

An end-to-end machine learning project that predicts hotel reservation outcomes using a clean, modular, and reproducible pipeline. Built with production practices—not notebook spaghetti.

---

## 🛠 Tech Stack

- **Language**: Python  
- **Data Processing**: Pandas, NumPy  
- **Modeling**: Scikit-learn, XGBoost  
- **Experiment Tracking**: MLflow  
- **Pipeline Orchestration**: Custom Python pipeline  
- **Logging**: Python `logging` module  

---

## 📌 Problem Statement

Hotel cancellations significantly impact revenue and operations.  
This system predicts whether a reservation will be fulfilled or canceled, enabling hotels to:

- Reduce overbooking losses  
- Improve dynamic pricing strategies  
- Optimize room allocation  

**ML Task**: Binary Classification  
**Target**: Reservation Canceled (Yes / No)

---

## 🧠 ML Workflow Overview

```
Raw Data
   ↓
Data Ingestion
   ↓
Data Preprocessing
   ↓
Feature Engineering
   ↓
Model Training & Selection
   ↓
Experiment Tracking (MLflow)
   ↓
Best Model Serialization
```

Everything is code-driven. No manual steps.

---

## 📁 Project Structure (Tracked Files Only)

```
PROJECT/
├── pipeline/
│   ├── __init__.py
│   └── training_pipeline.py     # Main pipeline entry point
│
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py        # Reads raw data
│   ├── data_preprocessing.py    # Cleaning & feature engineering
│   ├── model_training.py        # Training & evaluation
│   ├── logger.py                # Centralized logging
│   └── exceptions.py            # Custom exception handling
│
├── notebooks/
│   └── model_selection_and_training.ipynb
│
├── templates/
│   └── index.html               # Optional frontend placeholder
│
├── config/                      # Configuration files (if any)
├── utils/                       # Shared utilities
│
├── setup.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Configuration Management

All paths, hyperparameters, and pipeline settings are controlled via configuration files.  
This avoids hard-coded values and makes the pipeline environment-agnostic.

---

## 🔁 Reproducibility

- All datasets are reprocessed from raw sources  
- Models are retrained deterministically  
- No artifacts are committed to version control  
- Results can be regenerated using a single command  

---

## 🚫 Ignored During Version Control

The following are intentionally excluded and regenerated automatically:

```
artifacts/
models/
mlruns/
Logs/
build/
*.egg-info/
```

This keeps the repository:

- Lightweight  
- Reproducible  
- Reviewer-friendly  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd hotel-reservation-ml
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

## 🚀 Running the Training Pipeline

Single command. No excuses.

```bash
python pipeline/training_pipeline.py
```

This will:

- Load raw data  
- Preprocess features  
- Train candidate models  
- Track experiments via MLflow  
- Save the best model locally  

All outputs are generated automatically in ignored directories.

---

## 📊 Experiment Tracking (MLflow)

MLflow is used to track:

- Parameters  
- Metrics  
- Models  

To view experiments:

```bash
mlflow ui
```

Then open:  
**http://localhost:5000**

---

## 🧪 Model Development

Exploratory analysis and model comparison are available in:

```
notebooks/model_selection_and_training.ipynb
```

This notebook is optional — the pipeline does **not** depend on it.

---

## 🧱 Engineering Highlights

✔ Modular architecture  
✔ Clean separation of concerns  
✔ Centralized logging & exception handling  
✔ Reproducible training  
✔ MLflow integration  
✔ Production-ready pipeline pattern  

This is how ML systems are built in real teams, not Kaggle demos.

---

## 📄 License

This project is licensed under the MIT License.