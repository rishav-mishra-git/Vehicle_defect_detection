```python
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ===============================
# CONFIG
# ===============================
MODEL_PATH = "model/model_advanced.h5"
IMG_SIZE = (224, 224)
CLASSES = ["Dent", "Scratch", "Major Damage"]

# ===============================
# LOAD MODEL (CACHED)
# ===============================
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model(MODEL_PATH)
    return model

model = load_model()

# ===============================
# UTILITY FUNCTIONS
# ===============================
def preprocess_image(image):
    image = image.resize(IMG_SIZE)
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def get_damage_level(confidence):
    if confidence > 0.8:
        return "High Damage", "🚨"
    elif confidence > 0.5:
        return "Moderate Damage", "⚠️"
    else:
        return "Minor Damage", "✅"

def estimate_cost(class_index):
    if class_index == 2:
        return "₹15,000 - ₹50,000"
    elif class_index == 1:
        return "₹5,000 - ₹15,000"
    else:
        return "₹1,000 - ₹5,000"

# ===============================
# UI CONFIG
# ===============================
st.set_page_config(
    page_title="Vehicle Damage Detection",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #00ADB5;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# TITLE
# ===============================
st.markdown("<div class='title'>🚗 Vehicle Damage Detection Pro</div>", unsafe_allow_html=True)
st.write("---")

# ===============================
# FILE UPLOAD
# ===============================
uploaded_file = st.file_uploader(
    "📤 Upload Vehicle Image",
    type=["jpg", "jpeg", "png"]
)

# ===============================
# PREDICTION
# ===============================
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    # Show image
    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Process & Predict
    img_array = preprocess_image(image)

    with st.spinner("🔍 Analyzing damage..."):
        prediction = model.predict(img_array)
        class_index = np.argmax(prediction)
        confidence = float(np.max(prediction))

    # Show results
    with col2:
        st.subheader("📊 Prediction Result")

        st.success(f"{CLASSES[class_index]}")
        st.progress(confidence)
        st.write(f"Confidence: {confidence*100:.2f}%")

        # Damage level
        level, emoji = get_damage_level(confidence)
        st.warning(f"{emoji} {level}")

        # Cost estimation
        cost = estimate_cost(class_index)
        st.info(f"💰 Estimated Repair Cost: {cost}")
```
