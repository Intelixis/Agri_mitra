import streamlit as st
import google.generativeai as genai
import os
import config as config
from component import session_state
import base64
from component import utils


utils.page_config()
utils.page_design_image()
session_state.session_management()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Sidebar background image
side_bg = 'component\image\Firefly generate image for modern farmer with agriculture robot which support farmer to suporn in th.jpg'
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



# Function to get response from Gemini model
def get_gemini_response(input_text, language):
    try:
        # Define language-specific prompts
        prompts = {
            "Hindi": (
                f"आप भारतीय कृषि में विशेषज्ञ हैं और विभिन्न खेती की प्रथाओं, फसलों, मिट्टी प्रबंधन, कीट नियंत्रण, सिंचाई तकनीकों, जलवायु परिस्थितियों, कृषि नीतियों आदि के बारे में व्यापक ज्ञान रखते हैं। आपका उद्देश्य भारत में खेती से संबंधित प्रश्नों के लिए विस्तृत, सटीक और व्यावहारिक उत्तर प्रदान करना है।\n\n"
                f"उत्तर देते समय निम्नलिखित पहलुओं पर विचार करें:\n"
                f"- फसल का प्रकार (जैसे गेहूं, चावल, दालें, सब्जियां, फल आदि)\n"
                f"- भारत के जिस विशेष क्षेत्र और जलवायु में खेती हो रही है\n"
                f"- मिट्टी के प्रकार और उनका प्रबंधन\n"
                f"- फसलों की बुवाई, वृद्धि और कटाई के लिए सर्वोत्तम प्रथाएं\n"
                f"- जैविक और अजैविक उर्वरीकरण तकनीकें\n"
                f"- कीट और रोग नियंत्रण के उपाय\n"
                f"- आधुनिक सिंचाई प्रणालियाँ और जल प्रबंधन\n"
                f"- किसानों के लिए उपलब्ध सरकारी योजनाएँ और सब्सिडी\n"
                f"- कृषि उत्पादों के लिए बाजार के रुझान और मूल्य निर्धारण\n"
                f"- टिकाऊ और पर्यावरण के अनुकूल खेती के तरीके\n\n"
                f"कृपया अपना विस्तृत उत्तर हिंदी में प्रदान करें।\n\n"
                f"प्रश्न: {input_text}\n"
                f"उत्तर:"
            ),
            "English": (
                f"You are an expert in Indian agriculture with extensive knowledge about various farming practices, crops, soil management, pest control, irrigation techniques, climate conditions, agricultural policies, and more. Your goal is to provide detailed, accurate, and practical answers to questions related to farming in India.\n\n"
                f"When answering, consider the following aspects:\n"
                f"- The type of crop (e.g., wheat, rice, pulses, vegetables, fruits, etc.)\n"
                f"- The specific climate and region in India where the farming is taking place\n"
                f"- Soil types and their management\n"
                f"- Best practices for sowing, growing, and harvesting crops\n"
                f"- Organic and inorganic fertilization techniques\n"
                f"- Pest and disease control methods\n"
                f"- Modern irrigation systems and water management\n"
                f"- Government schemes and subsidies available to farmers\n"
                f"- Market trends and pricing for agricultural products\n"
                f"- Sustainable and eco-friendly farming methods\n\n"
                f"Please provide your detailed response in English.\n\n"
                f"Question: {input_text}\n"
                f"Answer:"
            )
        }

        # Generate response using the few-shot learning technique
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompts[language])
        return response.text
    except Exception as e:
        return f"Error occurred: {e}"
    


# # Streamlit app initialization
# utils.page_config()
# utils.page_design()

language = utils.language_selection()


# Title with a symbol and styling
st.markdown("<h1 class='header-title'>Krishi Sahayak (कृषि सहायक) 🌾</h1>", unsafe_allow_html=True)  # Hindi for Agri Assistant with Wheat symbol
st.markdown("<p class='question-prompt'>शेती संबंधित प्रश्नों के उत्तर!</p>", unsafe_allow_html=True)
st.markdown(sidebar_styles, unsafe_allow_html=True)

# Display chat history if display_chat is True
if st.session_state["display_chat"]:
    for item in st.session_state["chat_history"]:
        if "user" in item:
            with st.chat_message("user", avatar= "component\image\Firefly-kisaan.jpg"):
                st.write(item["user"])
        elif "assistant" in item:
            with st.chat_message("assistant", avatar= "component\image\chat.png"):
                st.write(item["assistant"])
# User input
user_message = st.chat_input("Say something")

if user_message:

    with st.chat_message("user", avatar= "component\image\Firefly-kisaan.jpg"):
        st.write(user_message)
        
   
    st.session_state["chat_history"].append({"user": user_message})
   
    response = get_gemini_response(user_message, language)
    with st.chat_message("assistant", avatar= "component\image\chat.png"):
        st.write(response)
   
    st.session_state["chat_history"].append({"assistant": response})
   
    st.session_state["display_chat"] = True

