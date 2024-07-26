import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
import config as config
from component import session_state
from component import utils

session_state.session_management()

# Set the page configuration
utils.page_config()

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS for styling
utils.page_design()

# Streamlit App Initialization
st.markdown('<div class="main">', unsafe_allow_html=True)

language = utils.language_selection()

# Title and Instructions based on language selection
if language == "Hindi":
    title_text = "🌾 कृषि सहायक - फसल स्वास्थ्य ऐप 🌱"
    instructions_text = """
    <div class="instructions">
    <p>कृपया अपनी फसल की स्पष्ट छवि अपलोड करें और अपनी चिंताओं को निर्दिष्ट करें। बेहतर विश्लेषण के लिए आप अतिरिक्त जानकारी भी प्रदान कर सकते हैं।</p>
    </div>
    """
    user_input_placeholder = "आपकी फसल के स्वास्थ्य के बारे में क्या जानना चाहेंगे?"
    upload_text = "अपनी फसल की छवि अपलोड करें..."
    analyze_button_text = "फसल स्वास्थ्य का विश्लेषण करें"
else:
    title_text = "🌾 Krishi Sahayak - Crop Health App 🌱"
    instructions_text = """
    <div class="instructions">
    <p>Please upload a clear image of your crop and specify your concerns. You can also provide additional details for a better analysis.</p>
    </div>
    """
    user_input_placeholder = "What would you like to know about your crop's health?"
    upload_text = "Upload an image of your crop..."
    analyze_button_text = "Analyze Crop Health"

st.markdown(f'<h1 class="header-title">{title_text}</h1>', unsafe_allow_html=True)
st.markdown(instructions_text, unsafe_allow_html=True)

# Input fields
user_input = st.text_input(user_input_placeholder, key="user_input")
uploaded_file = st.file_uploader(upload_text, type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Crop Image.", use_column_width=True)

submit = st.button(analyze_button_text, key="analyze_button")

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(user_input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([user_input, image[0], prompt])
    return response.text

# Default prompt to guide user input
if language == "Hindi":
    default_prompt = """
    आप एक प्रसिद्ध कृषि चिकित्सक और फसल स्वास्थ्य में विशेषज्ञ हैं, जिन्हें फसल रोगों, पोषक तत्वों की कमी, कीट नियंत्रण और सतत कृषि प्रथाओं के बारे में व्यापक ज्ञान है। आपका उद्देश्य अपलोड की गई फसल की छवि के आधार पर फसल स्वास्थ्य समस्याओं का निदान करने और उचित उपचार सुझाने के लिए विस्तृत, सटीक और व्यावहारिक सलाह प्रदान करना है।
    
    उत्तर देते समय निम्नलिखित पहलुओं पर विचार करें:
    - फसल का प्रकार (जैसे गेहूं, चावल, दालें, सब्जियां, फल आदि)
    - फसल को प्रभावित करने वाले दृश्य लक्षण और कीट
    - पोषक तत्वों की कमी के लक्षण और उनका उपचार
    - रोग रोकथाम और कीट नियंत्रण के सर्वोत्तम तरीके
    - जैविक और अजैविक उपचार विधियाँ
    - फसल स्वास्थ्य और उपज में सुधार के लिए सिफारिशें
    - टिकाऊ और पर्यावरण के अनुकूल खेती के तरीके
    
    कृपया छवि का विश्लेषण करें और अपना विस्तृत उत्तर हिंदी में प्रदान करें, महत्वपूर्ण बिंदुओं को बुलेट पॉइंट के साथ और प्रमुख जानकारी को बोल्ड करके हाइलाइट करें।
    
    प्रश्न: {user_input}
    उत्तर:
    """
else:
    default_prompt = """
    You are a renowned agricultural doctor and expert in crop health with extensive knowledge of crop diseases, nutrient deficiencies, pest control, and sustainable farming practices. Your goal is to provide detailed, accurate, and practical advice for diagnosing crop health issues and suggesting appropriate remedies based on the uploaded image of the crop.
    
    When answering, consider the following aspects:
    - The type of crop (e.g., wheat, rice, pulses, vegetables, fruits, etc.)
    - Visible symptoms of diseases and pests affecting the crop
    - Symptoms of nutrient deficiencies and their treatments
    - Best practices for disease prevention and pest control
    - Organic and inorganic treatment methods
    - Recommendations for improving crop health and yield
    - Sustainable and eco-friendly farming practices
    
    Please analyze the image and provide your detailed response in English, highlighting important points with bullet points and making key information bold.
    
    Question: {user_input}
    Answer:
    """

# If submit button is clicked
if submit:
    user_input_prompt = default_prompt.format(user_input=user_input.strip() if user_input.strip() else "No specific query provided.")
    image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
    response = get_gemini_response(user_input_prompt, image_data, user_input)
    st.subheader("Crop Health Analysis:")
    st.write(response)

st.markdown('</div>', unsafe_allow_html=True)