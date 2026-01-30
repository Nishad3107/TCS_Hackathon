"""
Travel Itinerary AI Agent - Streamlit Web Application
A beautiful, interactive web interface for generating personalized travel itineraries.
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import time

# CRITICAL: Load .env BEFORE importing anything else
from dotenv import load_dotenv
load_dotenv()

# Verify environment is loaded
if not os.getenv("GOOGLE_API_KEY"):
    st.error("⚠️ GOOGLE_API_KEY not found in .env file!")
    st.stop()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent import TravelAgent
from schemas import ItineraryRequest, TravelItinerary
from utils.formatting import format_itinerary_to_markdown, export_to_pdf
from validation import validate_itinerary_activities, format_validation_report
from image_service import get_destination_hero_image, get_activity_image

# Page Configuration
st.set_page_config(
    page_title="Travel Itinerary AI Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    with open('assets/styles/custom.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css()
except:
    pass  # CSS file not found, continue without custom styles

# Initialize Session State
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None
if 'request_data' not in st.session_state:
    st.session_state.request_data = None
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = TravelAgent()
    except Exception as e:
        st.error(f"Failed to initialize AI agent: {e}")
        st.stop()

# Hero Section
def render_hero():
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🌍 Travel Itinerary AI Agent</h1>
        <p class="hero-subtitle">Your Personal AI Travel Planner - Create Amazing Trips in Seconds</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/clouds/200/000000/globe.png", width=150)
        st.markdown("### 🎯 Quick Guide")
        st.markdown("""
        1. 📝 Fill in trip details
        2. 🤖 Let AI plan your trip
        3. ✅ Validate activities (optional)
        4. 📥 Download your itinerary
        """)
        
        st.markdown("---")
        st.markdown("### 🌟 Features")
        st.markdown("""
        - 🧠 Smart AI Planning
        - 🔍 Real Attraction Search
        - 🌤️ Weather Integration
        - ✅ Activity Validation
        - 📄 PDF/Markdown Export
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Example Destinations")
        example_destinations = ["Paris, France", "Tokyo, Japan", "New York, USA", 
                                "Bali, Indonesia", "Rome, Italy", "Dubai, UAE"]
        for dest in example_destinations:
            st.markdown(f"🗺️ {dest}")

# Main Input Form
def render_input_form():
    st.markdown("## 📝 Plan Your Perfect Trip")
    
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.text_input(
            "🗺️ Destination",
            placeholder="e.g., Paris, Tokyo, New York",
            help="Where do you want to go?"
        )
        
        duration = st.number_input(
            "📅 Duration (Days)",
            min_value=1,
            max_value=30,
            value=3,
            help="How many days will you stay?"
        )
        
        budget = st.select_slider(
            "💰 Budget Level",
            options=["Low", "Medium", "High", "Luxury"],
            value="Medium",
            help="Select your budget range"
        )
    
    with col2:
        interests = st.multiselect(
            "🎨 Interests",
            ["Food", "Culture", "Adventure", "Nature", "History", 
             "Shopping", "Nightlife", "Art", "Beach", "Museums"],
            default=["Food", "Culture"],
            help="What are you interested in?"
        )
        
        travelers = st.selectbox(
            "👥 Traveling As",
            ["Solo", "Couple", "Family", "Friends", "Business"],
            help="Who's traveling?"
        )
        
        start_date = st.date_input(
            "📆 Start Date",
            value=datetime.now() + timedelta(days=7),
            help="When does your trip start?"
        )
    
    st.markdown("---")
    
    # Additional preferences
    with st.expander("⚙️ Advanced Options (Optional)"):
        col3, col4 = st.columns(2)
        with col3:
            pace = st.radio(
                "Trip Pace",
                ["Relaxed", "Moderate", "Fast-paced"],
                index=1
            )
        with col4:
            accommodation = st.selectbox(
                "Accommodation Preference",
                ["Budget Hostel", "Mid-range Hotel", "Luxury Hotel", "Boutique", "Airbnb"]
            )
    
    return {
        "destination": destination,
        "duration": duration,
        "budget": budget,
        "interests": interests,
        "travelers": travelers,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "pace": pace if 'pace' in locals() else "Moderate",
        "accommodation": accommodation if 'accommodation' in locals() else "Mid-range Hotel"
    }

# Generate Itinerary
def generate_itinerary(form_data):
    if not form_data["destination"]:
        st.warning("⚠️ Please enter a destination!")
        return None
    
    # Create request
    request_data = ItineraryRequest(
        destination=form_data["destination"],
        duration_days=form_data["duration"],
        budget=form_data["budget"],
        interests=form_data["interests"],
        travelers=form_data["travelers"],
        start_date=form_data["start_date"]
    )
    
    # Generate itinerary with progress
    with st.spinner("🔮 Understanding your request..."):
        time.sleep(0.5)
    
    st.success("✅ Request understood!")
    
    with st.spinner("🔍 Searching for attractions and checking weather..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
    
    st.success("✅ Information gathered!")
    
    with st.spinner("🎨 Creating your perfect itinerary..."):
        itinerary = st.session_state.agent.create_itinerary(request_data)
        time.sleep(0.5)
    
    if not itinerary:
        st.error("❌ Failed to generate itinerary.")
        st.warning("💡 **Most Common Issue: API Quota Exceeded**")
        st.info("""
        **Your API key has likely exceeded its free quota.**
        
        **Solution:** Get a fresh API key from https://aistudio.google.com/app/apikey
        
        Then update your `.env` file and restart the app.
        
        **Other possible issues:**
        - Network connectivity
        - Invalid API configuration
        
        Check the terminal where you ran `streamlit run app.py` for detailed error logs.
        """)
        return None
    
    st.balloons()
    st.success("🎉 Your itinerary is ready!")
    
    return itinerary, request_data

# Display Itinerary
def display_itinerary(itinerary: TravelItinerary):
    st.markdown("---")
    st.markdown(f"# {itinerary.title}")
    
    # Summary Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-number">{len(itinerary.days)}</div>
            <div class="stats-label">Days</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-number">{itinerary.request.destination.split(',')[0]}</div>
            <div class="stats-label">Destination</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-number">{itinerary.request.budget}</div>
            <div class="stats-label">Budget</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-number">{len(itinerary.request.interests)}</div>
            <div class="stats-label">Interests</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Destination Hero Image (smaller, centered)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        hero_image = get_destination_hero_image(itinerary.request.destination)
        st.image(hero_image, caption=f"📍 {itinerary.request.destination}", use_container_width=True)
    
    st.markdown("---")
    
    # Overview
    with st.expander("📋 Trip Overview", expanded=True):
        st.markdown(f"**Summary:** {itinerary.summary}")
        st.markdown(f"**Estimated Cost:** {itinerary.total_estimated_cost}")
        st.markdown(f"**Travelers:** {itinerary.request.travelers}")
        st.markdown(f"**Interests:** {', '.join(itinerary.request.interests)}")
    
    # Day by Day Itinerary
    st.markdown("## 📅 Daily Itinerary")
    
    for day in itinerary.days:
        # Use container with custom CSS class
        with st.container():
            # Day header
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #162838 0%, #0d1b2a 100%); 
                 border: 1px solid rgba(66, 165, 245, 0.3); border-left: 5px solid #42a5f5; 
                 border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                 box-shadow: 0 3px 15px rgba(0, 150, 255, 0.2);">
                <div style="font-size: 1.8rem; font-weight: 700; color: #42a5f5; 
                     text-shadow: 0 0 10px rgba(66, 165, 245, 0.5); margin-bottom: 0.5rem;">
                    Day {day.day_number}
                </div>
                <p style="color: #90caf9; margin-bottom: 1.5rem;">📆 {day.date}</p>
            """, unsafe_allow_html=True)
            
            # Get image for the day's main activity (smaller, in columns)
            img_col1, img_col2 = st.columns([1, 2])
            with img_col1:
                day_image = get_activity_image(day.morning_activity, itinerary.request.destination)
                st.image(day_image, caption=f"Day {day.day_number}", use_container_width=True)
            
            # Morning
            st.markdown('<div style="font-weight: 600; color: #64b5f6; margin-top: 1rem;">☀️ MORNING</div>', unsafe_allow_html=True)
            st.write(day.morning_activity)
            
            # Afternoon
            st.markdown('<div style="font-weight: 600; color: #64b5f6; margin-top: 1rem;">🌤️ AFTERNOON</div>', unsafe_allow_html=True)
            st.write(day.afternoon_activity)
            
            # Evening
            st.markdown('<div style="font-weight: 600; color: #64b5f6; margin-top: 1rem;">🌙 EVENING</div>', unsafe_allow_html=True)
            st.write(day.evening_activity)
            
            st.markdown('</div>', unsafe_allow_html=True)

# Main App
def main():
    render_hero()
    render_sidebar()
    
    # Main content
    form_data = render_input_form()
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        generate_btn = st.button("🚀 Generate Itinerary", type="primary", use_container_width=True)
    with col2:
        if st.session_state.itinerary:
            clear_btn = st.button("🔄 Start Over", use_container_width=True)
            if clear_btn:
                st.session_state.itinerary = None
                st.session_state.request_data = None
                st.rerun()
    
    if generate_btn:
        result = generate_itinerary(form_data)
        if result:
            st.session_state.itinerary, st.session_state.request_data = result
    
    # Display existing itinerary
    if st.session_state.itinerary:
        display_itinerary(st.session_state.itinerary)
        
        st.markdown("---")
        
        # Action Buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ Validate Activities"):
                with st.spinner("Validating activities..."):
                    validation_results = validate_itinerary_activities(
                        st.session_state.itinerary, 
                        sample_validation=True
                    )
                    report = format_validation_report(validation_results)
                    st.markdown(report)
        
        with col2:
            # Export to Markdown
            markdown_content = format_itinerary_to_markdown(st.session_state.itinerary)
            st.download_button(
                label="📄 Download Markdown",
                data=markdown_content,
                file_name=f"itinerary_{form_data['destination'].replace(' ', '_')}.md",
                mime="text/markdown"
            )
        
        with col3:
            # Export to PDF
            if st.button("📕 Generate PDF"):
                with st.spinner("Creating PDF..."):
                    pdf_path = f"output/itinerary_{form_data['destination'].replace(' ', '_')}.pdf"
                    os.makedirs("output", exist_ok=True)
                    success = export_to_pdf(markdown_content, pdf_path)
                    if success:
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="📥 Download PDF",
                                data=f,
                                file_name=f"itinerary_{form_data['destination'].replace(' ', '_')}.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.error("Failed to generate PDF. Please check reportlab installation.")
        
        with col4:
            if st.button("📧 Share (Coming Soon)"):
                st.info("🚀 Email sharing feature coming soon!")
    
    # Spacer to push footer to bottom
    st.markdown("<div style='min-height: 5vh;'></div>", unsafe_allow_html=True)
    
    # Footer Section - At the very bottom
    st.markdown("""
    <div style="background: linear-gradient(135deg, #001e3c 0%, #0a1929 100%); 
         border-top: 2px solid #42a5f5; padding: 1.5rem 2rem; margin-top: auto;
         border-radius: 0; position: relative; bottom: 0; left: 0; right: 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div style="color: #90caf9; font-size: 0.9rem;">
                © 2026 Travel Itinerary AI
            </div>
            <div style="color: #90caf9; font-size: 0.9rem; text-align: center; flex: 1;">
                🌍 AI-Powered Travel Planning | <span style="color: #64b5f6;">About • Privacy • Terms • Contact</span>
            </div>
            <div style="color: #64b5f6; font-size: 0.9rem;">
                ✨ Powered by AI
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
