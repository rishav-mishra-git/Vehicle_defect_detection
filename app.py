import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import time
from utils import estimate_cost, damage_level

# Load model
model = tf.keras.models.load_model("model/model_advanced.h5")
classes = ["Dent", "Scratch", "Major Damage"]

# Page config
st.set_page_config(page_title="Vehicle Detection Pro", layout="wide")

# Styling
st.markdown("""
<style>
body { background-color: #0E1117; color: white; }
.title { text-align:center; font-size:42px; color:#00ADB5; font-weight:bold; }
.card { background-color:#1E1E1E; padding:20px; border-radius:10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚗 Vehicle Damage Detection Pro</div>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader("📤 Upload Vehicle Image", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_resized = image.resize((224,224))

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Original Image", use_column_width=True)

    with st.spinner("🔍 Analyzing..."):
        time.sleep(1)

        img_array = np.array(img_resized)/255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        idx = np.argmax(prediction)
        conf = float(np.max(prediction))

    with col2:
        st.subheader("📊 Prediction Result")
        st.success(classes[idx])

        st.progress(conf)

        st.write(f"Confidence: {conf*100:.2f}%")

        # Damage Level
        level = damage_level(conf)
        st.warning(level)

        # Cost Estimation
        cost = estimate_cost(idx)
        st.info(f"💰 Estimated Cost: {cost}")