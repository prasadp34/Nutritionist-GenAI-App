import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv() ##loading all the env variables
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
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

## Initialize Streamlit app

st.set_page_config(page_title="Nutritionist GenAI APP")

# Custom CSS
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

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert in nutritionist where you need to 
see the food items from the image and calculate the 
total calories, also provide the deatils of every 
food items with calories intake
in below format

1.Item 1=no of calories
2.Item 2=no of calories
---
---

Finally you can also mention whether the food is healthy 
or not and also mention the percentage split of the ratio
if carbohydrates,fats,fibers,sugar and other important things 
required in our diet
"""

if submit:
    if uploaded_file is not None:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            st.markdown('<div class="response-header">The Response is</div>', unsafe_allow_html=True)
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an image to proceed.")

st.markdown('<div class="footer">© 2024 Nutritionist GenAI App. All rights reserved.</div>', unsafe_allow_html=True)
