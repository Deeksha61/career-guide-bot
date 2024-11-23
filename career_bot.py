import streamlit as st
import google.generativeai as genai

# Configure the page
st.set_page_config(
    page_title="Career Guide Bot",
    page_icon="👩‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini API (replace with your valid API key)
genai.configure(api_key="AIzaSyAP2ojlQRASt0Vl4lou3fwSj6Ls5tQTD3M")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": """
        👋 Welcome to the Career Guide Bot! 

        I can help you explore career options and guide your path after 12th grade.

        You can ask me about:
        - 🎓 Streams like Science, Commerce, and Arts
        - 📚 Courses and colleges
        - 💼 Career opportunities and salaries
        - 📝 Entrance exams and preparation tips

        How can I help you today?
        """}
    ]

# Define career-related keywords
CAREER_KEYWORDS = [
    "career", "job", "course", "college", "stream", 
    "exam", "salary", "opportunity", "guidance", "12", "12th"
]

# Function to get response from Gemini AI or a fallback
def get_response(user_input):
    """
    Generate a response from Gemini AI if input contains career-related keywords.
    Otherwise, return a fallback message.
    """
    if any(keyword in user_input.lower() for keyword in CAREER_KEYWORDS):
        try:
            # Query Gemini AI
            gemini_response = model.generate_content(user_input)
            return gemini_response.text  # Return the AI-generated response
        except Exception as e:
            return f"⚠️ Sorry, I couldn't process your request due to an error: {str(e)}"
    else:
        # Return a fallback message for non-career-related queries
        return "🔍 I'm here to help with career-related queries. Please ask me about courses, exams, or job opportunities!"

# Function to save chat history
def save_chat_history():
    """
    Save the current chat history to a downloadable text file using UTF-8 encoding.
    """
    chat_history = ""
    for message in st.session_state.messages:
        role = "You" if message["role"] == "user" else "Bot"
        chat_history += f"{role}: {message['content']}\n\n"

    # Write chat history to a file with UTF-8 encoding
    file_path = "chat_history.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(chat_history)

    return file_path

# Main chat layout
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🎓 Career Guide Bot")
    st.markdown("Your friendly AI assistant for career guidance and planning.")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about career options..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate bot response
        response = get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

with col2:
    st.sidebar.header("Quick Access 🚀")
    st.sidebar.subheader("Useful Resources")
    st.sidebar.markdown("""
    📚 **Popular Courses:**
    - Engineering (B.Tech/B.E.)
    - Medical (MBBS/BDS)
    - Commerce (B.Com/BBA)
    - Arts (BA/BFA)
    
    🎯 **Major Entrance Exams:**
    - JEE (Engineering)
    - NEET (Medical)
    - CLAT (Law)
    - CAT (Management)
    """)

    # Save Chat History Button
    if st.sidebar.button("💾 Save Chat History"):
        file_path = save_chat_history()
        with open(file_path, "rb") as file:
            st.sidebar.download_button(
                label="Download Chat History",
                data=file,
                file_name="chat_history.txt",
                mime="text/plain"
            )

    # Clear chat history button
    if st.sidebar.button("🔄 Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": """
            👋 Welcome to the Career Guide Bot! 

            I can help you explore career options and guide your path after 12th grade.

            You can ask me about:
            - 🎓 Streams like Science, Commerce, and Arts
            - 📚 Courses and colleges
            - 💼 Career opportunities and salaries
            - 📝 Entrance exams and preparation tips

            How can I help you today?
            """}
        ]
        st.rerun()
