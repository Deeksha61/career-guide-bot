# frontend.py
import streamlit as st
import requests
import json
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_URL = "http://localhost:8000"
MONSTER_API_KEY = os.getenv("MONSTER_API_KEY")

class CareerChatbotUI:
    def __init__(self):
        # Initialize Streamlit config
        st.set_page_config(
            page_title="Career Guide Bot",
            page_icon="👩‍💼",
            layout="centered"
        )
        
        # Initialize session state
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hello! I'm your AI Career Guide. I can help you with:\n\n"
                    "• Career path exploration\n"
                    "• Job search and recommendations\n"
                    "• Skill analysis and development\n"
                    "• Industry insights\n\n"
                    "What would you like to explore today?"
                }
            ]

    def setup_ui(self):
        """Setup the main UI components"""
        st.title("👩‍💼 AI Career Guide")
        st.markdown("Powered by NLP and real-time job market data")
        
        # Custom CSS
        st.markdown("""
            <style>
                .stChat > div {
                    padding: 1rem;
                    border-radius: 15px;
                    margin-bottom: 1rem;
                }
                .job-card {
                    border: 1px solid #ddd;
                    padding: 1rem;
                    border-radius: 10px;
                    margin: 0.5rem 0;
                }
                .skill-tag {
                    background-color: #e8f0fe;
                    padding: 0.2rem 0.5rem;
                    border-radius: 15px;
                    margin: 0.2rem;
                    display: inline-block;
                }
            </style>
        """, unsafe_allow_html=True)

    async def get_chatbot_response(self, user_input: str, location: str = None) -> dict:
        """Get response from backend API"""
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": user_input,
                    "location": location,
                    "user_id": "test_user"  # You can implement user management later
                }
            )
            return response.json()
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")
            return None

    def display_job_listings(self, jobs):
        """Display job listings in a structured format"""
        st.subheader("📋 Related Job Opportunities")
        for job in jobs:
            with st.container():
                st.markdown(f"""
                    <div class="job-card">
                        <h4>{job['title']}</h4>
                        <p><strong>Company:</strong> {job.get('company', 'Not specified')}</p>
                        <p><strong>Location:</strong> {job.get('location', 'Not specified')}</p>
                        <p><strong>Salary:</strong> {job.get('salary', 'Not specified')}</p>
                    </div>
                """, unsafe_allow_html=True)

    def display_skill_recommendations(self, skills):
        """Display skill recommendations in a structured format"""
        st.subheader("🎯 Recommended Skills")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Technical Skills**")
            for skill in skills.get('technical_skills', {}).items():
                st.markdown(f'<span class="skill-tag">{skill[0]}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Soft Skills**")
            for skill in skills.get('soft_skills', []):
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)

    def run(self):
        """Main method to run the chatbot UI"""
        self.setup_ui()
        
        # Sidebar
        with st.sidebar:
            st.header("Settings")
            location = st.text_input("Job Search Location", "United States")
            
            st.header("Filters")
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level", "Mid Level", "Senior Level"]
            )
            
            job_type = st.selectbox(
                "Job Type",
                ["Full Time", "Part Time", "Contract", "Internship"]
            )
            
            st.header("About")
            st.markdown("""
                This AI Career Guide helps you:
                - Explore career opportunities
                - Find relevant job listings
                - Identify key skills
                - Understand industry trends
            """)

        # Main chat interface
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display additional information if available
                if "additional_data" in message:
                    data = message["additional_data"]
                    
                    if "job_listings" in data:
                        self.display_job_listings(data["job_listings"])
                    
                    if "skill_recommendations" in data:
                        self.display_skill_recommendations(data["skill_recommendations"])

        # Chat input
        if prompt := st.chat_input("Ask me about careers, jobs, or skills..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            response_data = asyncio.run(self.get_chatbot_response(prompt, location))
            
            if response_data:
                # Add bot response to chat history with additional data
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_data["message"],
                    "additional_data": {
                        "job_listings": response_data.get("job_listings", []),
                        "skill_recommendations": response_data.get("skill_recommendations", {}),
                        "career_path": response_data.get("career_path", {})
                    }
                })
                
                # Display bot response
                with st.chat_message("assistant"):
                    st.markdown(response_data["message"])
                    
                    # Display additional information
                    if response_data.get("job_listings"):
                        self.display_job_listings(response_data["job_listings"])
                    
                    if response_data.get("skill_recommendations"):
                        self.display_skill_recommendations(
                            response_data["skill_recommendations"]
                        )

if __name__ == "__main__":
    chatbot = CareerChatbotUI()
    chatbot.run()