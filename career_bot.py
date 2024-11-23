import streamlit as st
import google.generativeai as genai

# Configure the page
st.set_page_config(
    page_title="Career Guide Bot",
    page_icon="👩‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini API
genai.configure(api_key="AIzaSyAP2ojlQRASt0Vl4lou3fwSj6Ls5tQTD3M")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session states
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

# Resource information dictionary
RESOURCE_INFO = {
    "Engineering (B.Tech/B.E.)": """
        Engineering is a popular career choice that offers various specializations:
        - Computer Science Engineering
        - Mechanical Engineering
        - Electrical Engineering
        - Civil Engineering
        
        Key aspects:
        - Duration: 4 years
        - Entrance exams: JEE Main, JEE Advanced
        - Average starting salary: ₹3-8 LPA
        - Top colleges: IITs, NITs, BITS
    """,
    "Medical (MBBS/BDS)": """
        Medical education leads to becoming a doctor:
        - MBBS: 5.5 years (including internship)
        - BDS: 5 years
        
        Key aspects:
        - Entrance exam: NEET-UG
        - Extensive practical training
        - Various specializations available
        - Top colleges: AIIMS, JIPMER, GMCs
    """,
    "Commerce (B.Com/BBA)": """
        Commerce offers various career opportunities:
        - Accounting & Finance
        - Business Management
        - Banking & Insurance
        
        Key aspects:
        - Duration: 3 years
        - Options for professional courses: CA, CS
        - Average starting salary: ₹3-6 LPA
        - Top colleges: SRCC, Christ University
    """,
    "Arts (BA/BFA)": """
        Arts stream offers diverse career paths:
        - Literature
        - Psychology
        - Economics
        - Fine Arts
        
        Key aspects:
        - Duration: 3 years
        - Flexible career options
        - Creative opportunities
        - Research possibilities
    """,
    "JEE (Engineering)": """
        Joint Entrance Examination:
        - Two levels: JEE Main & JEE Advanced
        - Topics: Physics, Chemistry, Mathematics
        - Conducted multiple times a year
        - Required for IITs, NITs, and other top engineering colleges
    """,
    "NEET (Medical)": """
        National Eligibility cum Entrance Test:
        - Single window entrance for medical courses
        - Topics: Physics, Chemistry, Biology
        - Conducted once a year
        - Mandatory for MBBS/BDS admission
    """,
    "CLAT (Law)": """
        Common Law Admission Test:
        - For 5-year integrated law programs
        - Topics: Legal aptitude, reasoning, English
        - Conducted once a year
        - Required for National Law Universities
    """,
    "CAT (Management)": """
        Common Admission Test:
        - For MBA/PGDM programs
        - Topics: VARC, DILR, Quantitative Ability
        - Conducted once a year
        - Required for IIMs and top B-schools
    """
}

def get_response(user_input):
    """Generate a response from Gemini AI if input contains career-related keywords."""
    try:
        gemini_response = model.generate_content(user_input)
        return gemini_response.text
    except Exception as e:
        return f"⚠️ Sorry, I couldn't process your request due to an error: {str(e)}"

def save_chat_history():
    """Save the current chat history to a downloadable text file."""
    chat_history = ""
    for message in st.session_state.messages:
        role = "You" if message["role"] == "user" else "Bot"
        chat_history += f"{role}: {message['content']}\n\n"
    
    file_path = "chat_history.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(chat_history)
    return file_path

# Custom CSS for sticky input and better styling
st.markdown("""
    <style>
        .stTextInput {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem;
            background-color: white;
            z-index: 1000;
        }
        .resource-button {
            width: 100%;
            margin: 5px 0;
            padding: 10px;
            border-radius: 5px;
            background-color: #f0f2f6;
            border: none;
            text-align: left;
            cursor: pointer;
        }
        .resource-button:hover {
            background-color: #e0e2e6;
        }
    </style>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🎓 Career Guide Bot")
    st.markdown("Your friendly AI assistant for career guidance and planning.")
    
    # Chat container with some bottom padding for the fixed input
    chat_container = st.container()
    st.markdown("<div style='height: 100px'></div>", unsafe_allow_html=True)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

with col2:
    st.sidebar.header("Quick Access 🚀")
    
    # Courses Section
    st.sidebar.subheader("📚 Popular Courses")
    courses = ["Engineering (B.Tech/B.E.)", "Medical (MBBS/BDS)", 
              "Commerce (B.Com/BBA)", "Arts (BA/BFA)"]
    
    for course in courses:
        if st.sidebar.button(course, key=f"btn_{course}", 
                           help=f"Click to learn more about {course}"):
            response = RESOURCE_INFO[course]
            st.session_state.messages.append(
                {"role": "user", "content": f"Tell me about {course}"}
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()

    # Exams Section
    st.sidebar.subheader("🎯 Major Entrance Exams")
    exams = ["JEE (Engineering)", "NEET (Medical)", 
            "CLAT (Law)", "CAT (Management)"]
    
    for exam in exams:
        if st.sidebar.button(exam, key=f"btn_{exam}", 
                           help=f"Click to learn more about {exam}"):
            response = RESOURCE_INFO[exam]
            st.session_state.messages.append(
                {"role": "user", "content": f"Tell me about {exam}"}
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()

    # Chat Management Buttons
    st.sidebar.markdown("---")
    if st.sidebar.button("💾 Save Chat History"):
        file_path = save_chat_history()
        with open(file_path, "rb") as file:
            st.sidebar.download_button(
                label="Download Chat History",
                data=file,
                file_name="chat_history.txt",
                mime="text/plain"
            )

    if st.sidebar.button("🔄 Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": """
            👋 Welcome back! How can I help you with your career planning today?
            """}
        ]
        st.rerun()

# Fixed position chat input at the bottom
with st.container():
    if prompt := st.chat_input("Ask me anything about career options...", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()