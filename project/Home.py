import streamlit as st
import base64
from PIL import Image

import streamlit as st
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="AgriGenius 🌾",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to read image file and encode it to base64
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Sidebar background image
side_bg = 'component\image\Firefly generate modern agriculture farmer image 72490.jpg'
side_bg_ext = 'png'

# Main background image
bg_image_path = "Firefly background image for Agribot for indian farmers 95903 (1) copy.jpg"
bg_image_base64 = get_img_as_base64(bg_image_path)

# Sidebar CSS
sidebar_styles = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
    background: url(data:image/{side_bg_ext};base64,{get_img_as_base64(side_bg)});
    background-size: cover;
    background-position: center;
}}
</style>
"""

# Main page CSS
page_styles = f"""
<style>
:root {{
    --main-font: 'Arial', sans-serif;
    --text-color: #333333;
    --bg-color: #f0f8ff; /* Light blue background */
    --header-font-size: 30px;
    --content-font-size: 20px;
    --line-height: 1.6;
}}

body {{
    font-family: var(--main-font);
    color: var(--text-color);
    background-color: var(--bg-color);
}}

[data-testid="stAppViewContainer"] > .main {{
    background-color: var(--bg-color);
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    padding: 20px;
}}

.stHeader {{
    font-size: var(--header-font-size);
    color: darkgreen;
    margin-bottom: 20px;
}}

.stMarkdown {{
    font-size: var(--content-font-size);
    line-height: var(--line-height);
    margin-bottom: 20px;
}}

.stPlotly {{
    margin-top: 20px;
}}

h1, h2, h3 {{
    color: darkgreen;
    text-align: center;
}}

hr {{
    border: 1px solid darkgreen;
}}
</style>
"""

# Apply styles to the page
st.markdown(page_styles, unsafe_allow_html=True)
st.markdown(sidebar_styles, unsafe_allow_html=True)

# Title and introduction
st.markdown("<h1>Krishi Chatbot: A Smart Solution for Agriculture🌾</h1>", unsafe_allow_html=True)
st.markdown("<h2>Welcome to the Farming ChatBot! 🚜🌾</h2>", unsafe_allow_html=True)

# Introduction section
st.markdown("<h2>Introduction</h2>", unsafe_allow_html=True)
st.markdown(
    """
    The Farming ChatBot is your digital companion for all things agriculture. Whether you're a seasoned farmer or just getting started, our chatbot is here to assist you with a wide range of farming queries and tasks.
    """
)

# Features section
st.markdown("<h2>Features</h2>", unsafe_allow_html=True)

# Simple ChatBot feature
st.markdown("<h3>🌾 Krishi Chatbot</h3>", unsafe_allow_html=True)
st.markdown(
    """
    Krishibot is an AI-powered agricultural assistant designed for text-based interactions. It provides real-time solutions and advice on farming queries, ensuring farmers receive accurate and timely information for better crop management.
    """
)

# Advanced ChatBot feature
st.markdown("<h3>🌾 Krishi Vigyanik</h3>", unsafe_allow_html=True)
st.markdown(
    """
    Krishi Vigyanik connects farmers with expert agronomists for personalized consultations. It offers tailored advice and solutions, enhancing crop productivity and addressing specific agricultural challenges.
    """
)

# Advanced ChatBot feature
st.markdown("<h3>🌾 Krishi Mitra</h3>", unsafe_allow_html=True)
st.markdown(
    """
    Krishi Mitra is a multimodal agribot that supports both text and voice interactions. It provides comprehensive farming solutions, combining advanced AI insights with user-friendly communication for enhanced agricultural support.
    """
)

# Advanced ChatBot feature
st.markdown("<h3>🌾 Krishi Sahayak</h3>", unsafe_allow_html=True)
st.markdown(
    """
    Krishi Sahayak is an AI-driven crop health assistant that diagnoses plant diseases and pests. It provides actionable insights and recommendations to maintain healthy crops and improve yields.
    """
)

# How to Use section
st.markdown("<h2>How to Use</h2>", unsafe_allow_html=True)
st.markdown(
    """
    1. **Enter your query**: Provide detailed information about your farming issue or question.
    2. **Select the type of response**: Choose between simple or advanced chatbot.
    3. **Receive tailored advice**: Get solutions and recommendations specific to your needs.
    """
)

# Contact Us section
st.markdown("<h2>Contact Us</h2>", unsafe_allow_html=True)
st.markdown(
    """
    If you have any questions or need further assistance, please reach out to us:
    - Email: support@farmingchatbot.com
    - Phone: +91 7721815296
    """
)

# Images section (crops, tools, farmlands)
st.markdown("<h2>Future of Farming</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    image1 = Image.open("Firefly crop_image for Agribot for indian farmers 40768.jpg")
    st.image(image1, caption='Healthy Crops', use_column_width=True)

with col2:
    image2 = Image.open("Firefly farming_tools image for Agribot for indian farmers 95903.jpg")
    st.image(image2, caption='Modern Farming Tools', use_column_width=True)

with col3:
    image3 = Image.open("Firefly farmland_image image for Agribot for indian farmers 95903.jpg")
    st.image(image3, caption='Vast Farmlands', use_column_width=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h4>© 2024 Krishi ChatBot | Empowering Farmers with Technology</h4>", unsafe_allow_html=True)



