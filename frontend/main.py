import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Deep Learning Image Classifier", layout="centered")

st.title("🧠 End-to-End Deep Learning Classifier")
st.write("Upload an image below to get real-time predictions from our PyTorch backend API.")

BACKEND_URL = "http://127.0.0.1:8001/predict"

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Run Deep Learning Model"):
        with st.spinner("Analyzing image..."):
            try:
                buf = io.BytesIO()
                image.save(buf, format="JPEG")
                byte_im = buf.getvalue()

                files = {"file": ("image.jpg", byte_im, "image/jpeg")}
                response = requests.post(BACKEND_URL, files=files)

                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete!")
                    st.subheader("Top Predictions:")

                    for item in data["predictions"]:
                        label = item["label"].title()
                        confidence = item["confidence"]
                        st.write(f"**{label}**: {confidence}%")
                        st.progress(int(confidence))
                else:
                    st.error(f"Backend Error: {response.text}")

            except Exception as e:
                st.error(f"Failed to connect to backend server: {e}")