import streamlit as st
import datetime
from component import session_state
from component import utils

session_state.session_management()

# Define the content in both languages
content = {
    "English": {
        "title": "Krishi Expert Consultation Scheduling 🌾",
        "subtitle": "Check our availability and book the date and time that works for you",
        "select_date": "Select a Date",
        "availability": "Available Time Slots",
        "service_details": "Service Details",
        "consultation": "Expert Consultation - ₹500",
        "book": "Book Appointment",
        "success": "Your appointment is booked for {date} at {time_slot} with the agriculture domain expert.",
        "no_availability": "No availability"
    },
    "Hindi": {
        "title": "कृषि विशेषज्ञ परामर्श अनुसूची 🌾",
        "subtitle": "हमारी उपलब्धता देखें और अपने लिए उपयुक्त दिन और समय बुक करें",
        "select_date": "दिनांक चुनें",
        "availability": "उपलब्ध समय स्लॉट",
        "service_details": "सेवा विवरण",
        "consultation": "विशेषज्ञ परामर्श - ₹500",
        "book": "नियुक्ति बुक करें",
        "success": "आपकी नियुक्ति {date} को {time_slot} पर कृषि विशेषज्ञ के साथ बुक की गई है।",
        "no_availability": "कोई उपलब्धता नहीं"
    }
}


# Set the page configuration
utils.page_config()
utils.language_selection()

# Mapping language selection to content dictionary keys
lang = "English" if st.session_state.language == "English" else "Hindi"

# Style adjustments
utils.page_design()

# Title of the application
st.markdown(f"<h1 class='header-title'>{content[lang]['title']}</h1>", unsafe_allow_html=True)

# Subtitle
st.markdown(f"<h3 class='subtitle'>{content[lang]['subtitle']}</h3>", unsafe_allow_html=True)

# Selecting the date
date = st.date_input(content[lang]["select_date"], datetime.date.today(), min_value=datetime.date.today())

# Simulated available time slots (this should be dynamically fetched in a real application)
available_slots = {
    "09:00 - 10:00 AM": True,
    "10:00 - 11:00 AM": True,
    "11:00 - 12:00 PM": False,
    "02:00 - 03:00 PM": True,
    "03:00 - 04:00 PM": True,
    "04:00 - 05:00 PM": True,
}

# Display available time slots for the selected date
st.markdown(f"<h3 class='section-title'>{content[lang]['availability']}</h3>", unsafe_allow_html=True)
time_slots = [slot for slot, available in available_slots.items() if available]
if time_slots:
    time_slot = st.radio("", time_slots)
else:
    st.write(f"**{content[lang]['no_availability']}**")

# Expert consultation details
st.markdown(f"<h3 class='section-title'>{content[lang]['service_details']}</h3>", unsafe_allow_html=True)
st.markdown(f"<div class='service-details'>{content[lang]['consultation']}</div>", unsafe_allow_html=True)

# Booking button
if st.button(content[lang]["book"]):
    if time_slots:
        st.success(content[lang]["success"].format(date=date, time_slot=time_slot))
    else:
        st.error(content[lang]["no_availability"])