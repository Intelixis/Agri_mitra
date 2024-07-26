import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder, speech_to_text
import config as config
from component import session_state
from component import utils


session_state.session_management()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page configuration as the first Streamlit command
utils.page_config()


lang_data = {
    "English": {
        "app_title": "AgriMitra",
        "subtitle": "Krishi Mitra is a multimodal agribot that supports both text and voice interactions",
        "ask_question": "Kindly ask your agricultural question:",
        "submit_button": "Ask",
        "clear_button": "Clear",
        "chat_tab": "🌱 Chat",
        "speech_tab": "🎤 Speech to Text",
        "chat_with_agrimitra": "Chat with AgriMitra",
        "response": "Response",
        "history": "Chat History",
        "convert_speech": "Convert Speech to Text",
        "received_texts": "Received Texts",
        "generating_content": "Generating content...",
        "bot_response": "Expert's Response",
        "footer": "Powered by Streamlit & Google Generative AI",
        "getting_response": "Getting response...",
        "options": "Options",
        "chat_instructions": "Please enter your question about agriculture or farming.",
        "example_questions_label": "Example Questions:",
        "sample_questions_label": "Sample Questions:",
        "select_question_label": "Select a question",
        "example_questions": [
            "What are some effective pest control methods for tomato plants?",
            "How can I improve soil fertility for better crop yield?",
            "What is the ideal temperature range for growing strawberries?",
            "Can you suggest organic fertilizers for promoting plant growth?"
        ]
    },
    "Hindi": {
        "app_title": "एग्रीमित्रा",
        "subtitle": "कृषि मित्र एक मल्टीमॉडल एग्रीबॉट है जो टेक्स्ट और वॉयस इंटरैक्शन दोनों का समर्थन करता है।",
        "ask_question": "कृपया अपना कृषि संबंधी प्रश्न पूछें:",
        "submit_button": "पूछें",
        "clear_button": "साफ करें",
        "chat_tab": "🌱 चैट",
        "speech_tab": "🎤 वाक्-से-पाठ",
        "chat_with_agrimitra": "एग्रीमित्रा के साथ चैट करें",
        "response": "प्रतिक्रिया",
        "history": "चैट इतिहास",
        "convert_speech": "वाक् को पाठ में बदलें",
        "received_texts": "प्राप्त पाठ",
        "generating_content": "सामग्री उत्पन्न की जा रही है...",
        "bot_response": "विशेषज्ञ की प्रतिक्रिया",
        "footer": "Streamlit & Google Generative AI द्वारा संचालित",
        "getting_response": "प्रतिक्रिया प्राप्त की जा रही है...",
        "options": "विकल्प",
        "chat_instructions": "कृपया अपना कृषि संबंधी प्रश्न दर्ज करें।",
        "example_questions_label": "उदाहरण प्रश्न:",
        "sample_questions_label": "नमूना प्रश्न:",
        "select_question_label": "प्रश्न चुनें",
        "example_questions": [
            "टमाटर पौधों के लिए कुशल कीट प्रबंधन विधियां क्या हैं?",
            "बेहतर फसल उत्पादन के लिए मृदा पौष्टिकता को कैसे सुधारें?",
            "स्ट्रॉबेरी उगाने के लिए आदर्श तापमान सीमा क्या है?",
            "पौधों के विकास को बढ़ावा देने के लिए जैविक उर्वरक का सुझाव दें।"
        ]
    }
}



language = utils.language_selection()

# Mapping language selection to content dictionary keys
lang = "English" if st.session_state.language == "English" else "Hindi"
# Load environment variables
load_dotenv()

utils.page_design()

# Title of the application
st.markdown(f"<h1 class='header-title'>{lang_data[lang]['app_title']}</h1>", unsafe_allow_html=True)
# Subtitle
st.markdown(f"<h3 class='subtitle'>{lang_data[lang]['subtitle']}</h3>", unsafe_allow_html=True)
# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question, language):
    with st.spinner(lang_data[language]["getting_response"]):
        response = chat.send_message(question, stream=True)
    return response



# Add header image and title
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
# with header_col2:
#     st.markdown(f"<h1 class='header'>{lang_data[st.session_state.language]['app_title']}</h1>", unsafe_allow_html=True)

# Main content area with tabs
tab1, tab2 = st.tabs([lang_data[language]["chat_tab"], lang_data[language]["speech_tab"]])

with tab1:
    st.markdown(f"### {lang_data[language]['chat_with_agrimitra']}")
    st.markdown(f"{lang_data[language]['chat_instructions']}")
    
    text_input_label = lang_data[language]["select_question_label"]
    selected_question = st.selectbox(text_input_label, [""] + lang_data[language]["example_questions"], key="example_question")
    
    if selected_question:
        user_input = st.text_input(
            lang_data[language]["ask_question"], value=selected_question, key=f"user_input_{st.session_state.input_key}"
        )
    else:
        user_input = st.text_input(
            lang_data[language]["ask_question"], key=f"user_input_{st.session_state.input_key}"
        )
    
    st.markdown(f"#### {lang_data[language]['example_questions_label']}")
    for q in lang_data[language]["example_questions"]:
        st.markdown(f"- {q}")

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        submit = st.button(lang_data[language]["submit_button"], use_container_width=True)
    with col4:
        clear = st.button(lang_data[language]["clear_button"], use_container_width=True)

    if submit and user_input:
        st.session_state.history.append(("User", user_input))
        with st.spinner(lang_data[language]["getting_response"]):
            response = get_gemini_response(user_input, st.session_state.language)
        st.subheader(lang_data[language]["response"])
        with st.expander(lang_data[language]["bot_response"]):
            full_response = "".join([chunk.text for chunk in response])
            st.markdown(f"<div class='chat-bubble'>{full_response}</div>", unsafe_allow_html=True)
            st.session_state.history.append(("Bot", full_response))

    st.markdown(f"### {lang_data[language]['history']}")
    for sender, message in st.session_state.history:
        if sender == "Bot":
            st.markdown(f"<div class='chat-bubble'>{message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble user-bubble'>{message}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown(f"### {lang_data[language]['convert_speech']}")
    
    text = speech_to_text(
        language="Hindi" if language == "Hindi" else "en", use_container_width=True, just_once=True, key="STT"
    )
    if text:
        st.session_state.text_received.append(text)
    ask_speech = st.button(lang_data[language]["submit_button"], key="ask_speech")
    if ask_speech and st.session_state.text_received:
        question = st.session_state.text_received[-1]
        st.session_state.history.append(("User", question))
        with st.spinner(lang_data[language]["getting_response"]):
            response = get_gemini_response(question, st.session_state.language)
        st.markdown(f"#### {lang_data[language]['response']}")
        with st.expander(lang_data[language]["bot_response"]):
            full_response = "".join([chunk.text for chunk in response])
            st.markdown(f"<div class='chat-bubble'>{full_response}</div>", unsafe_allow_html=True)
            st.session_state.history.append(("Bot", full_response))
    
    st.markdown(f"#### {lang_data[language]['example_questions_label']}")
    for q in lang_data[language]["example_questions"]:
        st.markdown(f"- {q}")

    st.markdown(f"### {lang_data[language]['received_texts']}")
    for i, t in enumerate(st.session_state.text_received):
        st.write(f"{i + 1}: {t}")
