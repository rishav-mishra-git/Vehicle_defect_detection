import streamlit as st
import requests
from PIL import Image, ImageDraw
import pandas as pd

API_KEY = "9PU75Z9tiNgXhZlgx5cW"

MODEL_URL = "https://detect.roboflow.com/car_dent_scratch_detection-1-mczqd/1"


st.set_page_config(
    page_title="AI Vehicle Damage Inspector",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 AI Vehicle Damage Inspector")
st.write("Upload a vehicle image to detect damages and estimate repair cost.")


damage_costs = {

    # DENTS
    "bonnet-dent": 4500,
    "boot-dent": 4000,
    "doorouter-dent": 5000,
    "fender-dent": 3500,
    "front-bumper-dent": 6000,
    "rear-bumper-dent": 5500,
    "quarterpanel-dent": 6500,
    "roof-dent": 7000,
    "pillar-dent": 4500,
    "RunningBoard-Dent": 3000,
    "medium-Bodypanel-Dent": 5000,
    "Major-Rear-Bumper-Dent": 12000,

    # GLASS DAMAGES
    "Front-Windscreen-Damage": 15000,
    "Rear-windscreen-Damage": 12000,

    # LIGHT DAMAGES
    "Headlight-Damage": 8000,
    "Signlight-Damage": 3000,
    "Taillight-Damage": 5000,
    "Sidemirror-Damage": 3500,

    # DEFAULT
    "scratch": 2500
}


def get_severity(confidence):

    if confidence > 0.80:
        return "High"

    elif confidence > 0.55:
        return "Medium"

    else:
        return "Low"


uploaded_file = st.file_uploader(
    "Upload Vehicle Image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    try:

       
        response = requests.post(
            f"{MODEL_URL}?api_key={API_KEY}",
            files={"file": uploaded_file.getvalue()}
        )

        result = response.json()

        predictions = result.get("predictions", [])

        draw = ImageDraw.Draw(image)

        total_cost = 0

        table_data = []

       
        for p in predictions:

            confidence = p["confidence"]

            # FILTER LOW CONFIDENCE
            if confidence < 0.40:
                continue

            x = p["x"]
            y = p["y"]
            width = p["width"]
            height = p["height"]

            x1 = x - width / 2
            y1 = y - height / 2
            x2 = x + width / 2
            y2 = y + height / 2

            damage_class = p["class"]

            # GET COST
            estimated_cost = damage_costs.get(
                damage_class,
                4000
            )

            total_cost += estimated_cost

            severity = get_severity(confidence)

            # DRAW BOX
            draw.rectangle(
                [x1, y1, x2, y2],
                outline="red",
                width=4
            )

            # LABEL
            label = f"{damage_class} ({confidence:.2f})"

            draw.text(
                (x1, y1 - 20),
                label,
                fill="red"
            )

            # STORE TABLE DATA
            table_data.append({
                "Damage Type": damage_class,
                "Confidence": f"{confidence:.2f}",
                "Severity": severity,
                "Estimated Cost (₹)": estimated_cost
            })

        
        st.image(
            image,
            caption="Detected Damages",
            use_container_width=True
        )

        
        st.subheader("📋 Damage Report")

        if len(table_data) == 0:

            st.warning("No major damage detected.")

        else:

            df = pd.DataFrame(table_data)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.success(
                f"💰 Total Estimated Repair Cost: ₹{total_cost}"
            )

            
            if total_cost > 25000:

                st.error(
                    "⚠ Recommended: Insurance Claim Suggested"
                )

            elif total_cost > 10000:

                st.warning(
                    "⚠ Moderate Damage Detected"
                )

            else:

                st.info(
                    "✅ Minor Damage Detected"
                )

    except Exception as e:

        st.error(f"Error: {e}")
