import streamlit as st
import requests
import os
import google.generativeai as genai
import config as config
from component import session_state
from component import utils
import pandas as pd

session_state.session_management()

# Set API keys securely

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get weather data from OpenWeatherMap and store in session state
def get_weather(city):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data['name'],
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "description": data['weather'][0]['description']
        }
        st.session_state['weather_info'] = weather_info  # Store in session state for future use
        return weather_info
    else:
        st.error("Sorry, couldn't retrieve weather information.")
        return None
    

def get_weather_forecast(city):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=14"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extract necessary weather information
        forecasts = []
        for forecast in data['list']:
            forecasts.append({
                "Date": forecast['dt_txt'],
                "Temperature (°C)": forecast['main']['temp'],
                "Humidity (%)": forecast['main']['humidity'],
                "Description": forecast['weather'][0]['description']
            })
        weather_info = {
            "City": data['city']['name'],
            "Forecasts": forecasts
        }
        st.session_state['weather_info'] = weather_info  # Store in session state for future use
        return weather_info
    else:
        st.error("Sorry, couldn't retrieve weather information.")
        return None

# Function to get response from Gemini model
# def get_gemini_response(input_text, language, city, weather_prompt):
#     try:
#         # Define language-specific prompts
#         prompts = {
#             "Hindi": (
#                 f"आप भारतीय कृषि में विशेषज्ञ हैं और विभिन्न खेती की प्रथाओं, फसलों, मिट्टी प्रबंधन, कीट नियंत्रण, सिंचाई तकनीकों, जलवायु परिस्थितियों, कृषि नीतियों आदि के बारे में व्यापक ज्ञान रखते हैं। आपका उद्देश्य भारत में खेती से संबंधित प्रश्नों के लिए विस्तृत, सटीक और व्यावहारिक उत्तर प्रदान करना है।\n\n"
#                 f"{weather_prompt}\n"
#                 f"उत्तर देते समय निम्नलिखित पहलुओं पर विचार करें:\n"
#                 f"- फसल का प्रकार (जैसे गेहूं, चावल, दालें, सब्जियां, फल आदि)\n"
#                 f"- {city} क्षेत्र और जलवायु\n"
#                 f"- मिट्टी के प्रकार और उनका प्रबंधन\n"
#                 f"- फसलों की बुवाई, वृद्धि और कटाई के लिए सर्वोत्तम प्रथाएं\n"
#                 f"- जैविक और अजैविक उर्वरीकरण तकनीकें\n"
#                 f"- कीट और रोग नियंत्रण के उपाय\n"
#                 f"- आधुनिक सिंचाई प्रणालियाँ और जल प्रबंधन\n"
#                 f"- किसानों के लिए उपलब्ध सरकारी योजनाएँ और सब्सिडी\n"
#                 f"- कृषि उत्पादों के लिए बाजार के रुझान और मूल्य निर्धारण\n"
#                 f"- टिकाऊ और पर्यावरण के अनुकूल खेती के तरीके\n\n"
#                 f"कृपया अपना विस्तृत उत्तर Hindi में प्रदान करें।\n\n"
#                 f"प्रश्न: {input_text}\n"
#                 f"उत्तर:"
#             ),
#             "English": (
#                 f"You are an expert in Indian agriculture with extensive knowledge about various farming practices, crops, soil management, pest control, irrigation techniques, climate conditions, agricultural policies, and more. Your goal is to provide detailed, accurate, and practical answers to questions related to farming in India.\n\n"
#                 f"{weather_prompt}\n"
#                 f"When answering, consider the following aspects:\n"
#                 f"- The type of crop (e.g., wheat, rice, pulses, vegetables, fruits, etc.)\n"
#                 f"- {city} region and climate\n"
#                 f"- Soil types and their management\n"
#                 f"- Best practices for sowing, growing, and harvesting crops\n"
#                 f"- Organic and inorganic fertilization techniques\n"
#                 f"- Pest and disease control methods\n"
#                 f"- Modern irrigation systems and water management\n"
#                 f"- Government schemes and subsidies available to farmers\n"
#                 f"- Market trends and pricing for agricultural products\n"
#                 f"- Sustainable and eco-friendly farming methods\n\n"
#                 f"Please provide your detailed response in English.\n\n"
#                 f"Question: {input_text}\n"
#                 f"Answer:"
#             )
#         }

#         # Generate response using the Gemini model
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(prompts[language])
#         return response.text
#     except Exception as e:
#         st.error(f"Error occurred: {e}")
#         return ""

        # prompts = {
        #     "Hindi": (
        #         f"आप भारतीय कृषि में विशेषज्ञ हैं और विभिन्न खेती की प्रथाओं, फसलों, मिट्टी प्रबंधन, कीट नियंत्रण, सिंचाई तकनीकों, जलवायु परिस्थितियों, कृषि नीतियों आदि के बारे में व्यापक ज्ञान रखते हैं। आपका उद्देश्य भारत में खेती से संबंधित प्रश्नों के लिए विस्तृत, सटीक और व्यावहारिक उत्तर प्रदान करना है।\n\n"
        #         f"{weather_prompt}\n"
        #         f"उत्तर देते समय निम्नलिखित पहलुओं पर विचार करें:\n"
        #         f"- फसल का प्रकार (जैसे गेहूं, चावल, दालें, सब्जियां, फल आदि)\n"
        #         f"- {city} क्षेत्र और जलवायु\n"
        #         f"- मिट्टी के प्रकार और उनका प्रबंधन\n"
        #         f"- फसलों की बुवाई, वृद्धि और कटाई के लिए सर्वोत्तम प्रथाएं\n"
        #         f"- जैविक और अजैविक उर्वरीकरण तकनीकें\n"
        #         f"- कीट और रोग नियंत्रण के उपाय\n"
        #         f"- आधुनिक सिंचाई प्रणालियाँ और जल प्रबंधन\n"
        #         f"- किसानों के लिए उपलब्ध सरकारी योजनाएँ और सब्सिडी\n"
        #         f"- कृषि उत्पादों के लिए बाजार के रुझान और मूल्य निर्धारण\n"
        #         f"- टिकाऊ और पर्यावरण के अनुकूल खेती के तरीके\n\n"
        #         f"कृपया अपना विस्तृत उत्तर Hindi में प्रदान करें।\n\n"
        #         f"प्रश्न: {input_text}\n"
        #         f"उत्तर:"
        #     ),
        #     "English": (
        #         f"You are an expert in Indian agriculture with extensive knowledge about various farming practices, crops, soil management, pest control, irrigation techniques, climate conditions, agricultural policies, and more. Your goal is to provide detailed, accurate, and practical answers to questions related to farming in India.\n\n"
        #         f"{weather_prompt}\n"
        #         f"When answering, consider the following aspects:\n"
        #         f"- The type of crop (e.g., wheat, rice, pulses, vegetables, fruits, etc.)\n"
        #         f"- {city} region and climate\n"
        #         f"- Soil types and their management\n"
        #         f"- Best practices for sowing, growing, and harvesting crops\n"
        #         f"- Organic and inorganic fertilization techniques\n"
        #         f"- Pest and disease control methods\n"
        #         f"- Modern irrigation systems and water management\n"
        #         f"- Government schemes and subsidies available to farmers\n"
        #         f"- Market trends and pricing for agricultural products\n"
        #         f"- Sustainable and eco-friendly farming methods\n\n"
        #         f"Please provide your detailed response in English.\n\n"
        #         f"Question: {input_text}\n"
        #         f"Answer:"
        #     )
        # }

# Streamlit app initialization and UI components
utils.page_config()

# Apply custom CSS
utils.page_design()

# Title with a symbol and styling
st.markdown("<h1 class='header-title'>Krishi Sahayak (कृषि सहायक) 🌾</h1>", unsafe_allow_html=True)
st.markdown("<p class='question-prompt'>आपके कृषि संबंधित प्रश्नों के उत्तर!</p>", unsafe_allow_html=True)

language = utils.language_selection()

state_label = "Select a state"
city_label = "Select a city"

# Use the selectbox to choose a state
state = st.sidebar.selectbox(label=state_label, options=utils.state())

# Only show the city selectbox if a state is selected
if state:
    cities = utils.cities(state)
    city = st.sidebar.selectbox(label=city_label, options=cities)

# Weather info retrieval and display
if st.button("Get Weather / मौसम प्राप्त करें", key="weather_button"):
    weather_info = get_weather(city)
    if weather_info:
        if language == "Hindi":
            st.write(f"शहर: {weather_info['city']}, तापमान: {weather_info['temperature']}°C, आर्द्रता: {weather_info['humidity']}%, विवरण: {weather_info['description']}")
        else:
            st.write(f"City: {weather_info['city']}, Temperature: {weather_info['temperature']}°C, Humidity: {weather_info['humidity']}%, Description: {weather_info['description']}")
    else:
        if language == "Hindi":
            st.error("मौसम की जानकारी उपलब्ध नहीं है")
        else:
            st.error("Weather information unavailable.")

    weather_info = get_weather_forecast(city)
        # Display weather forecast for selected city in tabular format
    if st.session_state.get('weather_info'):
        weather_info = st.session_state['weather_info']
        if language == "Hindi":
            st.write(f"शहर: {weather_info['City']}")
            st.write("मौसम अनुमान नीचे दिए गए हैं:")
            weather_df = pd.DataFrame(weather_info['Forecasts'])
            st.table(weather_df)
        else:
            st.write(f"City: {weather_info['City']}")
            st.write("Weather forecasts for the next 2 weeks:")
            weather_df = pd.DataFrame(weather_info['Forecasts'])
            st.table(weather_df)

# # User input for agriculture-related queries
# input_text = st.text_area(f"Enter your agriculture-related question / अपने कृषि संबंधित प्रश्न दर्ज करें ({language})", "")

# # Button to generate response
# if st.button("Get Response / उत्तर प्राप्त करें"):
#     # Get weather prompt from session state
#     if 'weather_info' in st.session_state:
#         if language == "Hindi":
#             weather_prompt = f"मौसम: {st.session_state['weather_info']['temperature']}°C, {st.session_state['weather_info']['description']}"
#         else:
#             weather_prompt = f"Weather: {st.session_state['weather_info']['temperature']}°C, {st.session_state['weather_info']['description']}"
#     else:
#         if language == "Hindi":
#             weather_prompt = "मौसम जानकारी उपलब्ध नहीं है"
#         else:
#             weather_prompt = "Weather information not available."

#     # Call function to generate response
#     response = get_gemini_response(input_text, language, city, weather_prompt)
#     st.write(response)
