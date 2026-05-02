import streamlit as st
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

# ===============================
# CONFIG
# ===============================
MODEL_PATH = "model.tflite"
IMG_SIZE = (224, 224)
CLASSES = ["Dent", "Scratch", "Major Damage"]

# ===============================
# LOAD MODEL (CACHED)
# ===============================
@st.cache_resource
def load_model():
    interpreter = tflite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    return interpreter

interpreter = load_model()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ===============================
# PREPROCESS IMAGE
# ===============================
def preprocess_image(image):
    image = image.resize(IMG_SIZE)
    img_array = np.array(image, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# ===============================
# PREDICT FUNCTION
# ===============================
def predict(img_array):
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    return output

# ===============================
# DAMAGE LOGIC
# ===============================
def get_damage_level(conf):
    if conf > 0.8:
        return "🚨 High Damage"
    elif conf > 0.5:
        return "⚠️ Moderate Damage"
    else:
        return "✅ Minor Damage"

def estimate_cost(idx):
    if idx == 2:
        return "₹15,000 - ₹50,000"
    elif idx == 1:
        return "₹5,000 - ₹15,000"
    else:
        return "₹1,000 - ₹5,000"

# ===============================
# UI
# ===============================
st.set_page_config(page_title="Vehicle Detection", layout="wide")

st.markdown("<h1 style='text-align:center;color:#00ADB5'>🚗 Vehicle Damage Detection</h1>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("Upload Vehicle Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)

    img_array = preprocess_image(image)

    with st.spinner("Analyzing..."):
        prediction = predict(img_array)
        idx = np.argmax(prediction)
        conf = float(np.max(prediction))

    with col2:
        st.subheader("Prediction Result")

        st.success(CLASSES[idx])
        st.progress(conf)
        st.write(f"Confidence: {conf*100:.2f}%")

        st.warning(get_damage_level(conf))
        st.info(f"Estimated Cost: {estimate_cost(idx)}")
