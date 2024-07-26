import streamlit as st
import us
import geopy
from geopy.geocoders import Nominatim
import config as config
from .session_state import session_management
import pandas as pd
import gtts
from gtts import gTTS
import os
import base64


session_management()

def page_config():
    st.set_page_config(page_title="Krishi Sahayak (कृषि सहायक)", page_icon="🌾", layout="centered")


import streamlit as st

def page_design():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    :root {
        --main-font: 'Arial', sans-serif;
        --text-color: #333333;
        --bg-color: #f0f8ff;
        --header-font-size: 30px;
        --content-font-size: 20px;
        --line-height: 1.6;
    }

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f7fdf5;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        font-size: 32px;
        color: #ffffff;
        text-align: center;
        background-color: #2e7d32;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .css-1d391kg {
        font-size: 20px;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 20px;
    }
    .css-1y4p8pa {
        font-size: 18px;
        color: #388e3c;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton button {
        background-color: #2e7d32;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #1b5e20;
    }
    .css-2trqyj {
        font-size: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    .css-1awozwy {
        font-size: 18px;
        color: #d32f2f;
        text-align: center;
        margin-bottom: 20px;
    }
    .question-prompt {
        font-size: 22px;
        color: #1b5e20;
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        font-size: 14px;
        color: #6d6d6d;
        text-align: center;
        margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

def print_directory_contents(directory):
    try:
        files = os.listdir(directory)
        st.write(f"Contents of directory '{directory}': {files}")
    except Exception as e:
        st.error(f"Error accessing directory: {e}")

def page_design_image():
    # Path to the background image
    bg_image_path = "component\image\ear-wheat-close-up-field.jpg"

    # Encode the image to Base64
    bg_image_base64 = get_img_as_base64(bg_image_path)

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body {{
        font-family: 'Roboto', sans-serif;
        background-color: #f7fdf5;
    }}
    .main {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-image: url(data:image/jpg;base64,{bg_image_base64});
        background-size: cover;
        background-position: center;
    }}
    .header-title {{
        font-size: 32px;
        color: #ffffff;
        text-align: center;
        background-color: #2e7d32;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    .css-1d391kg {{
        font-size: 20px;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 20px;
    }}
    .css-1y4p8pa {{
        font-size: 18px;
        color: #388e3c;
        text-align: center;
        margin-bottom: 20px;
    }}
    .stButton button {{
        background-color: #2e7d32;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }}
    .stButton button:hover {{
        background-color: #1b5e20;
    }}
    .css-2trqyj {{
        font-size: 16px;
        text-align: center;
        margin-bottom: 20px;
    }}
    .css-1awozwy {{
        font-size: 18px;
        color: #d32f2f;
        text-align: center;
        margin-bottom: 20px;
    }}
    .question-prompt {{
        font-size: 22px;
        color: #1b5e20;
        text-align: center;
        margin-bottom: 20px;
    }}
    .footer {{
        font-size: 14px;
        color: #6d6d6d;
        text-align: center;
        margin-top: 40px;
    }}
    /* Styling for chat input bar */
    .stTextInput {{
        background-color: #ffffff; /* Change this to your desired color */
        border: 1px solid #2e7d32; /* Optional: Border color */
        border-radius: 5px; /* Optional: Rounded corners */
        padding: 10px; /* Optional: Padding inside the input bar */
        font-size: 16px; /* Optional: Font size */
    }}
    .stTextInput input {{
        color: #2e7d32; /* Text color inside input */
    }}
    </style>
    """, unsafe_allow_html=True)



def language_selection():
    language = st.sidebar.selectbox("भाषा चुनें | Choose Language", ["English", "Hindi"])
    st.session_state.language = language
    return st.session_state.language


df = pd.read_csv("component\data\Indian Cities Database.csv")


def state():
    df = pd.read_csv("component\data\Indian Cities Database.csv")

    state = df["State"].unique()
    return state


def cities(State):
    df = pd.read_csv("component\data\Indian Cities Database.csv")
   
    cities = df[df['State'] == State]
    return cities["City"].to_list()



def text_to_audio(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    audio_file = "output.mp3"
    tts.save(audio_file)
    print(f"Audio saved as {audio_file}")



