# 🏨 Hotel Reservation Prediction System

> Production-ready end-to-end machine learning system for predicting hotel reservation cancellations with automated CI/CD deployment to Google Cloud Platform.

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7.2-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)



---

## 📑 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [ML Pipeline](#-ml-pipeline)
- [Installation Guide](#-installation-guide)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Model Performance](#-model-performance)
- [Monitoring & Logging](#-monitoring--logging)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

A comprehensive machine learning solution that predicts hotel reservation cancellations with **75%+ accuracy**. The system combines modern ML practices with production-grade DevOps to deliver real-time predictions through both a web interface and REST API.

### What Makes This Project Special?

✅ **End-to-End ML Pipeline**: From data ingestion to model deployment  
✅ **Production-Grade Code**: Modular, testable, and maintainable  
✅ **Automated CI/CD**: GitHub → Jenkins → Cloud Build → Cloud Run  
✅ **Scalable Architecture**: Serverless deployment with auto-scaling  
✅ **Real-Time Predictions**: Sub-second inference latency  
✅ **Experiment Tracking**: MLflow for reproducible experiments  
✅ **Cloud-Native**: Fully deployed on Google Cloud Platform  

---

## 📌 Problem Statement

Hotel reservation cancellations pose significant challenges to the hospitality industry:

- **Revenue Loss**: Empty rooms due to last-minute cancellations
- **Operational Inefficiency**: Difficulty in resource planning
- **Pricing Challenges**: Inability to implement dynamic pricing
- **Customer Experience**: Overbooking leading to dissatisfaction

### Our Solution

A binary classification model that predicts cancellation probability **before** check-in, enabling proactive decision-making.

**ML Task**: Binary Classification  
**Target Variable**: `booking_status`
- **0** = Canceled
- **1** = Not Canceled

**Model Output**:
- Binary prediction (Canceled/Not Canceled)
- Probability score (0-100%)
- Confidence threshold: **65.28%**

---

## ✨ Key Features

### 🤖 Machine Learning Pipeline
- Automated data ingestion and preprocessing
- Multi-model evaluation (RandomForest, XGBoost, LightGBM, etc.)
- MLflow-based experiment tracking
- Smart model selection based on business metrics
- Threshold optimization for precision-recall balance

### 🌐 Web Application
- Modern responsive UI
- Client & server-side validation
- Comprehensive error handling
- Mobile-friendly interface

### 🔌 REST API
- RESTful JSON endpoints
- Pydantic schema validation
- Health checks & metadata endpoints

### 🚀 DevOps & Infrastructure
- Dockerized runtime
- Jenkins + Cloud Build CI/CD
- Google Cloud Run deployment
- Google Cloud Storage model artifacts
- Auto scaling (0 → 100 instances)

---

## 🏗 System Architecture

```
User/UI
  ↓
Flask Web App + REST API
  ↓
Preprocessing Pipeline
  ↓
Trained Model (Best Model)
  ↓
Prediction Output
```

---

## 🧰 Technology Stack

- **Language**: Python  
- **Data Processing**: Pandas, NumPy  
- **Modeling**: Scikit-learn, XGBoost, LightGBM  
- **Experiment Tracking**: MLflow  
- **Pipeline Orchestration**: Custom Python pipeline  
- **Web Framework**: Flask  
- **Deployment**: Docker, Google Cloud Run  
- **CI/CD**: Jenkins, Cloud Build  

---

## 📁 Project Structure

```
PROJECT/
├── artifacts/
├── config/
│   ├── __init__.py
│   ├── config.yaml
│   ├── model_params.py
│   └── paths_config.py
├── custom_jenkins/
│   └── Dockerfile
├── Logs/
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
├── .gitignore
├── application.py
├── cloudbuild.yaml
├── Dockerfile
├── Jenkinsfile
├── README.md
├── requirement-train.txt
├── requirements.txt
└── setup.py
```

---

## 🧠 ML Pipeline

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

## ⚙️ Configuration

All pipeline settings are driven through configuration files in `config/`, keeping the system portable and environment‑agnostic.

---

## 🚫 Ignored Artifacts

Generated folders and files are excluded from version control:

```
artifacts/
models/
Logs/
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd Hotel-Management-System
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux 
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run the Training Pipeline
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