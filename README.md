🚗 Vehicle Damage Detection & Cost Estimator
🔍 Overview

An AI-powered web application that detects vehicle dents and scratches from uploaded car images and estimates the repair cost automatically using a trained YOLOv11 object detection model.

Built using:

🐍 Python
🎯 Roboflow YOLOv11
🌐 Streamlit
🖼️ Computer Vision
✨ Features

✅ Detects Dents and Scratches
✅ Draws Bounding Boxes on damaged areas
✅ Displays Confidence Scores
✅ Estimates Repair Cost Automatically
✅ Supports Multiple Damages in one image
✅ Professional Web UI using Streamlit
✅ Severity Analysis (Small / Medium / Severe)

🧠 How It Works
User uploads a damaged vehicle image
Image is sent to the trained Roboflow model
Model detects damage regions
Bounding boxes are drawn on detected areas
Repair cost is estimated based on damage size and type
Results are displayed in a clean dashboard
🛠️ Tech Stack
Technology	Purpose
Python	Backend Logic
Streamlit	Web Application
Roboflow	Model Training & API
YOLOv11	Object Detection
Pillow	Image Processing
Requests	API Communication
📂 Project Structure
vehicle-damage-detection/
│
├── app.py
├── requirements.txt
└── README.md
