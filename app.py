import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image_data):
    # Create a generative model instance
    model = genai.GenerativeModel('gemini-pro-vision')
    # Generate content using the model
    response = model.generate_content([input_prompt, image_data])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Nutritionist GenAI App", layout="wide")

# App title and description with custom colors and spacing
st.markdown("""
    <style>
        .main-header {
            font-size: 48px;
            color: #4CAF50;
            text-align: center;
            margin-top: 50px;
            margin-bottom: 20px;
        }
        .sub-header {
            font-size: 20px;
            color: #555555;
            text-align: center;
            margin-bottom: 40px;
        }
        .footer {
            font-size: 16px;
            color: #888888;
            text-align: center;
            margin-top: 50px;
            margin-bottom: 10px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
        }
        .uploader-label {
            font-size: 18px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        }
        .uploader {
            margin-bottom: 30px;
        }
        .response-header {
            font-size: 24px;
            color: #4CAF50;
            margin-top: 40px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Nutritionist GenAI App</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Welcome! Upload an image of your meal, and our AI will analyze the food items, calculate the total calories, and provide detailed nutritional information.</div>', unsafe_allow_html=True)

# File uploader with custom styling
st.markdown('<div class="uploader-label">Choose an image...</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="uploader")

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.markdown('<div style="margin-bottom: 30px;"></div>', unsafe_allow_html=True)

# Prompt for AI model
input_prompt = """
You are an expert in nutrition. See the food items from the image and calculate the total calories. 
Also, provide the details of every food item with calories intake in the format below:

1. Item 1 = number of calories
2. Item 2 = number of calories
---
---

Finally, mention whether the food is healthy or not. Also mention the percentage split of the ratio
of carbohydrates, fats, fibers, sugar, and other important nutrients required in our diet.
"""

# Submit button
if st.button("Tell me about the total calories"):
    if uploaded_file is not None:
        with st.spinner("Analyzing the image..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data)
                st.success("Analysis complete!")
                st.markdown('<div class="response-header">The Response is</div>', unsafe_allow_html=True)
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an image to proceed.")

# Footer
st.markdown('<div class="footer">© 2024 Nutritionist GenAI App. All rights reserved.</div>', unsafe_allow_html=True)
