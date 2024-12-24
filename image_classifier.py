import streamlit as st
from transformers import pipeline
from PIL import Image

# Load the classification pipeline
@st.cache_resource
def load_pipeline(model_name):
    return pipeline("image-classification", model=model_name)

# Title and Description
st.title("📷 Hugging Face Image Classifier")
st.write("Classify objects in images using a pre-trained model from Hugging Face.")
st.markdown("---")

# Model Input Section
st.subheader("🔧 Select Model")
st.write("Enter the Hugging Face model identifier to use for image classification.")
model_name = st.text_input(
    "Model Name", "NonoBru/leaf-classifier", help="Enter the Hugging Face model identifier (e.g., 'google/vit-base-patch16-224')."
)

# Load the selected model
if model_name:
    with st.spinner("Loading model..."):
        try:
            classifier = load_pipeline(model_name)
            st.success(f"Model '{model_name}' loaded successfully!")
        except Exception as e:
            st.error(f"Failed to load model: {e}")
            st.stop()

st.markdown("---")

# Input Method Selector
st.subheader("📤 Upload or Take an Image")
input_method = st.radio(
    "Choose an input method:",
    ("Upload an Image", "Take a Photo"),
    horizontal=True
)

st.markdown("---")

# Dynamic Content Based on Input Method
if input_method == "Take a Photo":
    st.subheader("📸 Capture a Photo")
    st.write("Use your webcam to take a picture.")
    image_data = st.camera_input("Take a picture")

    if image_data:
        with st.spinner("Processing your image..."):
            image = Image.open(image_data)
            st.image(image, caption="Captured Photo", use_container_width=True)

            # Perform classification
            predictions = classifier(image)

        # Display Results
        st.markdown("### 🌟 Predictions:")
        for pred in predictions:
            st.markdown(f"<span style='color:green;font-size:18px;'>✔️ **{pred['label']}**</span>: {pred['score']:.4f}", unsafe_allow_html=True)
else:
    st.subheader("📁 Upload an Image")
    st.write("Select an image file from your device.")
    uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        with st.spinner("Processing your image..."):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)

            # Perform classification
            predictions = classifier(image)

        # Display Results
        st.markdown("### 🌟 Predictions:")
        for pred in predictions:
            st.markdown(f"<span style='color:green;font-size:18px;'>✔️ **{pred['label']}**</span>: {pred['score']:.4f}", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;">
        <small>Created with ❤️</small>
    </div>
    """,
    unsafe_allow_html=True
)
