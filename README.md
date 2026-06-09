# 🧠 Brain Tumor MRI Classification System

An AI-powered Brain Tumor Classification System that analyzes MRI scans and classifies them into four categories: **Glioma, Meningioma, Pituitary Tumor, and No Tumor**. The project utilizes **EfficientNet-based Transfer Learning**, a **FastAPI backend**, a **Streamlit frontend**, and **Grad-CAM Explainability** to provide interpretable predictions.

---

##  Overview

Brain tumors are among the most critical neurological disorders requiring early diagnosis and treatment. Manual MRI analysis can be time-consuming and requires expert radiologists. This project aims to assist diagnosis by automatically classifying MRI scans using Deep Learning techniques.

The system provides:

* Tumor classification from MRI images
* Prediction confidence scores
* Class-wise probability distribution
* Grad-CAM visual explanations highlighting important regions influencing model predictions

---

##  Features

* ✅ Brain Tumor Classification using Deep Learning
* ✅ Four-Class Classification

  * Glioma
  * Meningioma
  * Pituitary
  * No Tumor
* ✅ EfficientNet Transfer Learning
* ✅ FastAPI Backend
* ✅ Streamlit Frontend
* ✅ Grad-CAM Explainability
* ✅ Real-Time Prediction
* ✅ Probability Scores for All Classes
* ✅ User-Friendly Interface

---

##  System Architecture

```text
MRI Image
    │
    ▼
Image Preprocessing
(Cropping + Resizing)
    │
    ▼
EfficientNet Model
    │
    ├── Prediction
    │
    └── Grad-CAM
            │
            ▼
Visual Explanation
    │
    ▼
FastAPI Backend
    │
    ▼
Streamlit Frontend
```

---

##  Model Details

### Base Model

* EfficientNet (Transfer Learning)
* TensorFlow / Keras

### Training Strategy

The model was trained using a two-phase transfer learning approach:

#### Phase 1: Feature Extraction

* Pretrained EfficientNet layers frozen
* Only classification head trained

#### Phase 2: Fine-Tuning

* Selected EfficientNet layers unfrozen
* Entire model fine-tuned on Brain MRI dataset

This approach improved generalization while reducing training time.

---

##  Classes

| Class      | Description                            |
| ---------- | -------------------------------------- |
| Glioma     | Tumor originating from glial cells     |
| Meningioma | Tumor arising from meninges            |
| Pituitary  | Tumor occurring in the pituitary gland |
| No Tumor   | Normal MRI scan                        |

---

## 🔍 Explainable AI with Grad-CAM

To improve model interpretability, Grad-CAM (Gradient-weighted Class Activation Mapping) was integrated into the system.

Grad-CAM generates heatmaps highlighting image regions that contributed most to the model's prediction.

Benefits:

* Increased transparency
* Improved trust in predictions
* Better understanding of model behavior
* Useful visual explanation during diagnosis

---

##  Tech Stack

### Machine Learning

* TensorFlow
* Keras
* NumPy
* OpenCV
* Scikit-Learn

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit

### Explainability

* Grad-CAM

---

##  Project Structure

```text
Brain-Tumor-MRI-Classification/
│
├── backend/
│   ├── app.py
│   ├── gradcam.py
│   ├── brain_tumor_model.keras
│   ├── uploads/
│   └── gradcam_outputs/
│
├── frontend/
│   └── streamlit_app.py
│
├── notebooks/
│   └── final-model.ipynb
│
├── screenshots/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

##  Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Brain-Tumor-Detection.git

cd Brain-Tumor-Detection
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Run Backend

```bash
cd backend

uvicorn app:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

##  Run Frontend

Open a new terminal:

```bash
cd frontend

streamlit run streamlit_app.py
```

Frontend runs at:

```text
http://localhost:8501
```

---

##  Sample Output

### Prediction Result

```text
Prediction: Pituitary
Confidence: 99.87%
```

### Class Probabilities

```text
Glioma      : 0.01%
Meningioma  : 0.03%
Pituitary   : 99.87%
No Tumor    : 0.09%
```

### Grad-CAM Visualization

The application displays:

* Original MRI Scan
* Grad-CAM Heatmap
* Visual Explanation of Prediction

---


##  Future Improvements

* Docker Containerization
* Cloud Deployment
* Advanced Explainability Methods
* Support for Additional MRI Datasets
* Medical Report Generation
* Multi-Language Support

---

##  Authors

**Nishant Singh Bisht**

---

## Disclaimer

This project is developed for educational and research purposes only.

It is not intended to replace professional medical diagnosis or clinical decision-making.
