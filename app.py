import streamlit as st
import requests
from PIL import Image, ImageDraw
import io

# =========================
# ROBFLOW CONFIG
# =========================
API_KEY = "Ct01Fr4ZzSux9DURoieR"
MODEL_URL = "https://detect.roboflow.com/vehicle-defect/5"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Vehicle Damage Detection",
    page_icon="🚗",
    layout="wide"
)

# =========================
# TITLE
# =========================
st.title("🚗 Vehicle Damage Detection & Cost Estimator")
st.markdown("Upload a damaged vehicle image to detect dents and scratches.")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Upload Car Image",
    type=["jpg", "jpeg", "png"]
)

# =========================
# COST ESTIMATION LOGIC
# =========================
def estimate_cost(predictions):
    total_cost = 0

    for p in predictions:
        width = p["width"]
        height = p["height"]
        area = width * height

        # Dent cost
        if p["class"] == "dent":
            if area < 10000:
                total_cost += 3000
            elif area < 30000:
                total_cost += 6000
            else:
                total_cost += 10000

        # Scratch cost
        elif p["class"] == "scratch":
            if area < 8000:
                total_cost += 1500
            elif area < 20000:
                total_cost += 3000
            else:
                total_cost += 5000

    return total_cost

# =========================
# DAMAGE LEVEL
# =========================
def get_damage_level(area):
    if area < 10000:
        return "Small"
    elif area < 30000:
        return "Medium"
    else:
        return "Severe"

# =========================
# PROCESS IMAGE
# =========================
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")
        st.image(image, use_container_width=True)

    # Convert image to bytes
    img_bytes = uploaded_file.getvalue()

    # API Request
    response = requests.post(
        f"{MODEL_URL}?api_key={API_KEY}",
        files={"file": img_bytes}
    )

    result = response.json()
    predictions = result.get("predictions", [])

    # Draw bounding boxes
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)

    for p in predictions:
        x = p["x"]
        y = p["y"]
        width = p["width"]
        height = p["height"]

        x1 = x - width / 2
        y1 = y - height / 2
        x2 = x + width / 2
        y2 = y + height / 2

        label = p["class"]

        if label == "dent":
            color = "red"
        else:
            color = "yellow"

        draw.rectangle([x1, y1, x2, y2], outline=color, width=5)
        draw.text((x1, y1 - 20), label, fill=color)

    with col2:
        st.subheader("Detected Damage")
        st.image(draw_image, use_container_width=True)

    # =========================
    # RESULTS
    # =========================

    st.markdown("---")
    st.subheader("📊 Detection Results")

    if len(predictions) == 0:
        st.warning("No damage detected")

    else:
        total_cost = estimate_cost(predictions)

        dent_count = 0
        scratch_count = 0

        for p in predictions:
            if p["class"] == "dent":
                dent_count += 1
            elif p["class"] == "scratch":
                scratch_count += 1

        # Summary Cards
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Dent Count", dent_count)

        with c2:
            st.metric("Scratch Count", scratch_count)

        with c3:
            st.metric("Estimated Cost", f"₹{total_cost}")

        st.markdown("---")

        # Detailed Predictions
        st.subheader("🔍 Detailed Damage Analysis")

        for idx, p in enumerate(predictions, start=1):
            confidence = round(p["confidence"] * 100, 2)
            area = p["width"] * p["height"]
            severity = get_damage_level(area)

            st.markdown(f"""
            ### Damage {idx}
            - **Type:** {p['class'].upper()}
            - **Confidence:** {confidence}%
            - **Severity:** {severity}
            """)

        # Final Cost Box
        st.success(f"💰 Total Estimated Repair Cost: ₹{total_cost}")
