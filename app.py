import streamlit as st
import requests
from PIL import Image, ImageDraw


API_KEY = "9PU75Z9tiNgXhZlgx5cW"

MODEL_URL = "https://detect.roboflow.com/car_dent_scratch_detection-1-mczqd/1"


st.set_page_config(
    page_title="Smart Vehicle Inspector",
    page_icon="🚗",
    layout="wide"
)


st.title("🚗 Smart Vehicle Inspector")
st.write("Upload a damaged vehicle image to detect dents and scratches.")


uploaded_file = st.file_uploader(
    "Upload Car Image",
    type=["jpg", "jpeg", "png"]
)


def estimate_cost(predictions):
    total_cost = 0

    for p in predictions:
        damage_class = p["class"]

        if damage_class == "dent":
            total_cost += 3000

        elif damage_class == "scratch":
            total_cost += 1500

        else:
            total_cost += 2000

    return total_cost


if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Uploaded Image", use_container_width=True)

    try:
        # Send image to Roboflow
        response = requests.post(
            f"{MODEL_URL}?api_key={API_KEY}",
            files={"file": uploaded_file.getvalue()}
        )

        result = response.json()

        predictions = result.get("predictions", [])

        # Draw detections
        draw = ImageDraw.Draw(image)

        for p in predictions:

            x = p["x"]
            y = p["y"]
            width = p["width"]
            height = p["height"]

            x1 = x - width / 2
            y1 = y - height / 2
            x2 = x + width / 2
            y2 = y + height / 2

            damage_class = p["class"]
            confidence = p["confidence"]

            # Draw rectangle
            draw.rectangle(
                [x1, y1, x2, y2],
                outline="red",
                width=4
            )

            # Draw label
            label = f"{damage_class} ({confidence:.2f})"

            draw.text(
                (x1, y1 - 20),
                label,
                fill="red"
            )

        # Show result image
        st.image(
            image,
            caption="Detected Damage",
            use_container_width=True
        )

        # Show details
        st.subheader("Detection Results")

        if len(predictions) == 0:
            st.warning("No damage detected.")

        else:
            for i, p in enumerate(predictions, start=1):

                st.write(
                    f"{i}. {p['class']} "
                    f"(Confidence: {p['confidence']:.2f})"
                )

            # Cost estimation
            total_cost = estimate_cost(predictions)

            st.success(
                f"Estimated Repair Cost: ₹{total_cost}"
            )

    except Exception as e:
        st.error(f"Error: {e}")
