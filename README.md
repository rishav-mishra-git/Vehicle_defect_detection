# 🚗 Vehicle Defect Detection 

An advanced AI-powered web application that detects vehicle damage types (**Dent, Scratch, Major Damage**) from images using Deep Learning and provides **confidence scores, severity analysis, and cost estimation**.

---

## 📌 Project Overview

This project is built to automate vehicle damage assessment using Computer Vision. It allows users to upload an image of a damaged vehicle and instantly receive:

* 🔍 Damage Classification (Dent / Scratch / Major Damage)
* 📊 Confidence Score
* ⚠️ Damage Severity Level
* 💰 Estimated Repair Cost

---

## 🧠 Tech Stack

* **Frontend/UI:** Streamlit
* **Model:** TensorFlow / Keras
* **Architecture:** EfficientNetB0 (Transfer Learning)
* **Libraries:** NumPy, Pillow, OpenCV, Matplotlib

---

## 📂 Project Structure

```
Vehicle_Detection/
│
├── dataset/
│   ├── train/
│   └── val/
│
├── model/
│   └── model_advanced.h5
│
├── train.py
├── app.py
├── utils.py
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

The dataset consists of vehicle images categorized into:

* Dent
* Scratch
* Major Damage

> ⚠️ Important: Dataset must be organized in folder structure:

```
dataset/train/dent
dataset/train/scratch
dataset/train/damage
```

---

## ⚙️ Installation

###  Install Dependencies

```
pip install -r requirements.txt
```

---

## 🧠 Model Training

Run the training script:

```
python train.py
```

This will:

* Train EfficientNet model
* Save trained model in `/model` folder

---

## 🚀 Run Application

Start Streamlit app:

```
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 🎯 Features

* ✔️ Deep Learning-based image classification
* ✔️ Transfer learning (EfficientNetB0)
* ✔️ Real-time prediction
* ✔️ Clean and interactive UI
* ✔️ Damage severity detection
* ✔️ Repair cost estimation

---

## 📸 Demo Workflow

1. Upload vehicle image
2. Model processes image
3. Displays:

   * Damage type
   * Confidence score
   * Severity level
   * Estimated cost

---

## 🔥 Future Enhancements

* 🔴 Grad-CAM (highlight damaged area)
* 🎥 Video damage detection
* 🌐 Full-stack integration (React + API)
* ☁️ Cloud deployment (AWS / GCP)
* 📊 Analytics dashboard

---

## ⚠️ Limitations

* Model accuracy depends on dataset quality
* Limited performance on unseen damage types
* Requires more diverse training data

---

## 👨‍💻 Author

**Rishav**
CSE (AI/ML) Student
Haldia Institute of Technology
