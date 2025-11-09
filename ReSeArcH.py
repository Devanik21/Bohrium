import streamlit as st
import google.generativeai as genai
from datetime import datetime
import base64
import os
import json
from tinydb import TinyDB, Query

# Page configuration
st.set_page_config(
    page_title="Bohrium | Science Navigator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

def set_app_background(image_file):
    """
    Sets the background of the Streamlit app to a local image file.
    """
    if not os.path.exists(image_file):
        st.error(f"Background image not found at '{image_file}'")
        return

    with open(image_file, "rb") as f:
        img_bytes = f.read()
    
    base64_img = base64.b64encode(img_bytes).decode()
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: transparent !important;
        backdrop-filter: blur(5px); /* A bit more blur for readability */
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }
    
    /* Make the main app header transparent */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* --- BOHRIUM GREEN/GOLD THEME --- */

    /* General Text Color */
    .stMarkdown, p, span, div, .stButton>button, .stTabs [data-baseweb="tab"] {
        color: rgba(240, 240, 240, 0.9) !important;
    }

    /* Header Container */
    .header-container {
        background: rgba(10, 25, 20, 0.5); /* Semi-transparent dark green */
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid rgba(46, 204, 113, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        color: #ffffff;
        font-size: 42px;
        font-weight: bold;
        margin: 0;
    }
    
    .header-subtitle {
        color: rgba(220, 230, 225, 0.85);
        font-size: 18px;
        margin-top: 10px;
    }
    
    /* Tool Cards */
    .tool-card {
        background: rgba(20, 35, 30, 0.75); /* Darker semi-transparent green */
        backdrop-filter: blur(5px);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(46, 204, 113, 0.15);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        margin-bottom: 15px;
        transition: transform 0.2s;
        color: rgba(240, 240, 240, 0.9);
    }
    
    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3); /* Green glow */
        border: 1px solid rgba(46, 204, 113, 0.3);
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 1px solid rgba(46, 204, 113, 0.6);
        padding: 12px 20px;
        background-color: rgba(10, 25, 20, 0.8);
        color: rgba(240, 240, 240, 0.9);
    }
    
    /* Main Action Buttons */
    .stButton > button {
        border-radius: 25px;
        background: transparent !important;
        border: 1px solid rgba(46, 204, 113, 0.7) !important;
        color: rgba(240, 240, 240, 0.9) !important;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: rgba(46, 204, 113, 0.15) !important; /* Subtle green glow on hover */
        border-color: rgba(46, 204, 113, 1) !important;
        color: #ffffff !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: rgba(10, 25, 20, 0.8);
        border: 1px solid rgba(46, 204, 113, 0.4);
        color: rgba(240, 240, 240, 0.9);
    }
    
    /* Text Area */
    .stTextArea > div > div > textarea {
        background-color: rgba(10, 25, 20, 0.8);
        color: rgba(240, 240, 240, 0.9);
        border: 1px solid rgba(46, 204, 113, 0.6);
    }
    
    /* Number Input */
    .stNumberInput > div > div > input {
        background-color: rgba(10, 25, 20, 0.8);
        color: rgba(240, 240, 240, 0.9);
        border: 1px solid rgba(46, 204, 113, 0.6);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(20, 35, 30, 0.75);
        border-radius: 5px;
        color: rgba(240, 240, 240, 0.9);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 1px solid rgba(46, 204, 113, 0.3);
    }
    
    /* Metric Value */
    [data-testid="stMetricValue"] {
        color: #2ecc71; /* Bright green */
    }
    
    /* Caption Text */
    .caption {
        color: rgba(180, 200, 190, 0.7) !important;
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] * {
        color: rgba(240, 240, 240, 0.9) !important;
    }
    
    /* Divider color */
    hr {
        border-color: rgba(46, 204, 113, 0.2);
    }
    
    /* Nobel Banner */
    .nobel-banner {
        background: transparent !important;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        color: rgba(240, 240, 240, 0.9) !important; /* Light text for visibility */
        box-shadow: none !important;
    }
    
    /* Accuracy Badge */
    .accuracy-badge {
        background: rgba(46, 204, 113, 0.2); /* Subtle green background */
        border: 1px solid rgba(46, 204, 113, 0.7);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        font-size: 14px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Set the background image
image_path = "green-gradient-abstract-background-empty-room-with-space-your-text-picture.jpg"
set_app_background(image_path)

# Initialize session state
if 'state_loaded' not in st.session_state:
    # --- Database Setup for Persistence ---
    db = TinyDB('bohrium_db.json')
    user_data_table = db.table('user_data')

    # Load previous state if available
    saved_data = user_data_table.get(doc_id=1)
    if saved_data:
        st.session_state.chat_history = saved_data.get('chat_history', [])
        st.session_state.current_tool = saved_data.get('current_tool', 'Science Navigator')
        st.session_state.library = saved_data.get('library', [])
        st.session_state.search_history = saved_data.get('search_history', [])
        st.session_state.collections = saved_data.get('collections', [])
        st.session_state.reading_list = saved_data.get('reading_list', [])
        st.session_state.notes = saved_data.get('notes', [])
        st.toast("Loaded saved session data.", icon="💾")
    else:
        # Initialize if no saved data
        st.session_state.chat_history = []
        st.session_state.current_tool = 'Science Navigator'
        st.session_state.library = []
        st.session_state.search_history = []
        st.session_state.collections = []
        st.session_state.reading_list = []
        st.session_state.notes = []

    st.session_state.state_loaded = True

# Function to save state to TinyDB
def save_state():
    """Saves the current session state to the database."""
    db = TinyDB('bohrium_db.json')
    user_data_table = db.table('user_data')
    current_state = {
        'chat_history': st.session_state.chat_history,
        'current_tool': st.session_state.current_tool,
        'library': st.session_state.library,
        'search_history': st.session_state.search_history,
        'collections': st.session_state.collections,
        'reading_list': st.session_state.reading_list,
        'notes': st.session_state.notes,
    }
    if user_data_table.get(doc_id=1):
        user_data_table.update(current_state, doc_ids=[1])
    else:
        user_data_table.insert(current_state)
    st.toast("Progress saved!", icon="💾")

# Configure Gemini API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    st.error("⚠️ Please configure GEMINI_API_KEY in Streamlit secrets")

# --- Password Protection ---
def check_password():
    """Returns `True` if the user has the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Sidebar Navigation
with st.sidebar:
    # Main Navigation
    menu_items = {
        "🆕 New Chat": "new_chat",
        "🔍 Academic Search": "academic_search",
        "🌐 Explore": "explore",
        "🔔 Subscription": "subscription",
        "📚 Library": "library",
        "👨‍🎓 Scholars": "scholars",
        "📖 Knowledge Base": "knowledge_base",
        "🎯 Practice": "practice",
        "🛠️ Uni-Lab": "uni_lab",
        "💾 Computation": "computation",
        "📊 History": "history"
    }
    
    st.markdown("### 🧭 Navigation")
    for label, key in menu_items.items():
        if st.button(label, key=key, use_container_width=True):
            st.session_state.current_tool = label
            save_state()
    
    st.markdown("---")
    
    # Language selector
    language = st.selectbox("🌍 Language", ["English", "中文", "Español", "Français", "Deutsch"])
    
    st.markdown("---")
    
    # Login button
    if st.button("🔐 Log In", use_container_width=True):
        st.info("Login functionality would be implemented here")

# Main content area
st.markdown('<div class="nobel-banner">🏆 Nobel 2025 Hub | Connect with the Great Minds and Explore Nobel Discoveries</div>', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div style="display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 60px; margin-right: 20px;">🧪</span>
        <div>
            <h1 class="header-title">Science Navigator</h1>
            <p class="header-subtitle">AI Literature Assistant for Scientists - Solving Scientific Problems</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content based on selected tool
if st.session_state.current_tool in ["🆕 New Chat", "Science Navigator"]:
    # Main chat interface
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Search input
        user_query = st.text_input(
            "",
            placeholder="Ask any scientific questions...",
            key="main_search",
            label_visibility="collapsed"
        )
        
        # Action buttons
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            if st.button("⚡ Quick Answer"):
                st.session_state.mode = "quick"
        with col_b:
            if st.button("🔬 Deep Research"):
                st.session_state.mode = "deep"
        with col_c:
            if st.button("📊 Data Analysis"):
                st.session_state.mode = "analysis"
        with col_d:
            if st.button("💡 More..."):
                st.session_state.mode = "more"
        
        if user_query:
            # Add to history
            st.session_state.search_history.append({
                "query": user_query,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_state()
            
            # Generate response using Gemini
            with st.spinner("🔍 Searching scientific literature..."):
                try:
                    # Create a scientific research prompt
                    prompt = f"""You are a scientific research assistant. Answer the following question with accuracy and cite relevant scientific sources when possible:
                    
Question: {user_query}

Provide a comprehensive, scientifically accurate answer."""
                    
                    response = model.generate_content(prompt)
                    
                    # Display response
                    st.markdown("### 📝 Answer")
                    st.markdown(response.text)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "query": user_query,
                        "response": response.text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_state()
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
        
        # Quick action buttons
        st.markdown("---")
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            if st.button("🔬 Try SciencePedia — Explore Visible and Reliable Science", use_container_width=True):
                st.info("SciencePedia: Access to 170M+ scientific papers")
        with col_y:
            if st.button("❓ General Q&A", use_container_width=True):
                st.info("General Q&A mode activated")
        with col_z:
            if st.button("💬 LitTalk", use_container_width=True):
                st.info("LitTalk: Interactive literature discussion")
        
        st.markdown('<div class="accuracy-badge">Over 97% accuracy on USMLE</div>', unsafe_allow_html=True)
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 💬 Recent Conversations")
            for idx, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
                with st.expander(f"Q: {chat['query'][:100]}..."):
                    st.markdown(f"**Question:** {chat['query']}")
                    st.markdown(f"**Answer:** {chat['response']}")
                    st.caption(f"🕒 {chat['timestamp']}")

elif st.session_state.current_tool == "🔍 Academic Search":
    st.markdown("## 🔍 Academic Search")
    st.markdown("Search through 170M+ papers, 160M+ patents, and 20M+ scholar profiles")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search academic literature...", key="academic_search_input")
    with col2:
        search_type = st.selectbox("Type", ["Papers", "Patents", "Scholars", "Journals"])
    
    if search_query:
        with st.spinner("Searching academic databases..."):
            try:
                prompt = f"""As a scientific literature search assistant, provide relevant information about: {search_query}
                
Include:
1. Key research papers and findings
2. Important researchers in this field
3. Recent developments
4. Relevant journals and publications

Format the response clearly with sections."""
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Search error: {str(e)}")
    
    # Filters
    with st.expander("🎯 Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.multiselect("Field", ["Physics", "Chemistry", "Biology", "Mathematics", "Computer Science", "Medicine"])
        with col2:
            st.slider("Publication Year", 1900, 2025, (2020, 2025))
        with col3:
            st.multiselect("Journal", ["Nature", "Science", "Cell", "Lancet", "PNAS"])

elif st.session_state.current_tool == "📚 Library":
    st.markdown("## 📚 My Library")
    
    tabs = st.tabs(["Saved Papers", "Collections", "Reading List", "Notes"])
    
    with tabs[0]:
        if st.session_state.library and isinstance(st.session_state.library, list) and len(st.session_state.library) > 0:
            for idx, item in enumerate(st.session_state.library):
                with st.container():
                    st.markdown(f"**{item.get('title', 'Untitled')}**")
                    st.caption(f"Added: {item.get('date', 'Unknown date')}")
                    col1, col2, col3 = st.columns([1, 1, 3])
                    with col1:
                        st.button("📖 Read", key=f"read_{idx}")
                    with col2:
                        if st.button("🗑️ Remove", key=f"remove_{idx}"):
                            st.session_state.library.pop(idx)
                            save_state()
                            st.rerun()
        else:
            st.info("Your library is empty. Start saving papers from your searches!")
            
            # Add sample paper button
            if st.button("➕ Add Sample Paper"):
                st.session_state.library.append({
                    "title": "Quantum Computing Advances in 2025",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "authors": "Smith et al.",
                    "journal": "Nature"
                })
                save_state()
                st.rerun()
    
    with tabs[1]:
        st.markdown("### Create New Collection")
        col1, col2 = st.columns([3, 1])
        with col1:
            collection_name = st.text_input("Collection Name")
        with col2:
            if st.button("➕ Create"):
                if collection_name:
                    if 'collections' not in st.session_state:
                        st.session_state.collections = []
                    st.session_state.collections.append({
                        "name": collection_name,
                        "created": datetime.now().strftime("%Y-%m-%d"),
                        "papers": []
                    })
                    save_state()
                    st.success(f"Collection '{collection_name}' created!")
        
        # Display existing collections
        if 'collections' in st.session_state and isinstance(st.session_state.collections, list) and len(st.session_state.collections) > 0:
            st.markdown("### Your Collections")
            for idx, collection in enumerate(st.session_state.collections):
                with st.expander(f"📁 {collection['name']} ({len(collection['papers'])} papers)"):
                    st.caption(f"Created: {collection['created']}")
                    if st.button("🗑️ Delete Collection", key=f"del_col_{idx}"):
                        st.session_state.collections.pop(idx)
                        save_state()
                        st.rerun()
    
    with tabs[2]:
        st.markdown("### 📖 Reading List")
        
        if 'reading_list' not in st.session_state:
            st.session_state.reading_list = []
        
        if isinstance(st.session_state.reading_list, list) and len(st.session_state.reading_list) > 0:
            for idx, item in enumerate(st.session_state.reading_list):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{item['title']}**")
                    st.caption(f"Priority: {item['priority']}")
                with col2:
                    if st.button("✅ Done", key=f"done_{idx}"):
                        st.session_state.reading_list.pop(idx)
                        save_state()
                        st.rerun()
                with col3:
                    if st.button("🗑️", key=f"remove_reading_{idx}"):
                        st.session_state.reading_list.pop(idx)
                        save_state()
                        st.rerun()
        else:
            st.info("Add papers to your reading list to track your progress")
            
            # Add sample to reading list
            if st.button("➕ Add Sample to Reading List"):
                st.session_state.reading_list.append({
                    "title": "Introduction to Machine Learning",
                    "priority": "High",
                    "added": datetime.now().strftime("%Y-%m-%d")
                })
                save_state()
                st.rerun()
    
    with tabs[3]:
        st.markdown("### 📝 My Notes")
        
        if 'notes' not in st.session_state:
            st.session_state.notes = []
        
        note_content = st.text_area("Write your research notes...", height=200, key="new_note_input")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("💾 Save Note"):
                if note_content:
                    st.session_state.notes.append({
                        "content": note_content,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_state()
                    st.success("Note saved!")
                    st.rerun()
        
        if len(st.session_state.notes) > 0:
            st.markdown("---")
            st.markdown("### Saved Notes")
            for idx, note in enumerate(reversed(st.session_state.notes)):
                note_display_idx = len(st.session_state.notes) - 1 - idx
                with st.expander(f"📄 Note from {note.get('date', 'Unknown')}"):
                    st.markdown(note.get('content', ''))
                    if st.button("🗑️ Delete", key=f"delete_note_{note_display_idx}"):
                        st.session_state.notes.pop(note_display_idx)
                        save_state()
                        st.rerun()

elif st.session_state.current_tool == "🎯 Practice":
    st.markdown("## 🎯 Practice & Learning Tools")
    
    practice_tools = {
        "🧮 Problem Solver": "Solve complex scientific and mathematical problems",
        "📊 Data Analysis": "Analyze datasets and generate insights",
        "🔬 Lab Simulator": "Virtual laboratory experiments",
        "📝 Quiz Generator": "Generate practice quizzes on any topic",
        "🎓 Study Guide Creator": "Create comprehensive study guides",
        "💡 Concept Explainer": "Break down complex concepts",
        "🔍 Research Planner": "Plan your research projects",
        "📈 Progress Tracker": "Track your learning progress"
    }
    
    cols = st.columns(2)
    for idx, (tool, desc) in enumerate(practice_tools.items()):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"### {tool}")
                st.markdown(desc)
                if st.button("Launch", key=f"practice_{idx}"):
                    st.session_state.active_practice_tool = tool
    
    if hasattr(st.session_state, 'active_practice_tool'):
        st.markdown("---")
        st.markdown(f"## {st.session_state.active_practice_tool}")
        
        if "Problem Solver" in st.session_state.active_practice_tool:
            problem = st.text_area("Enter your problem:")
            if st.button("Solve"):
                with st.spinner("Solving..."):
                    try:
                        response = model.generate_content(f"Solve this problem step by step: {problem}")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        elif "Quiz Generator" in st.session_state.active_practice_tool:
            topic = st.text_input("Enter topic:")
            num_questions = st.slider("Number of questions:", 5, 20, 10)
            if st.button("Generate Quiz"):
                with st.spinner("Generating quiz..."):
                    try:
                        prompt = f"Generate {num_questions} multiple choice questions about {topic} with answers"
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

elif st.session_state.current_tool == "👨‍🎓 Scholars":
    st.markdown("## 👨‍🎓 Scholar Network")
    st.markdown("Connect with 20M+ active researchers worldwide")
    
    search_scholar = st.text_input("Search for scholars, institutions, or research groups...")
    
    if search_scholar:
        with st.spinner("Searching scholar database..."):
            try:
                prompt = f"""Provide information about researchers, institutions, or research groups related to: {search_scholar}
                
Include:
1. Notable researchers and their contributions
2. Key institutions and departments
3. Research areas and specializations
4. Recent publications and achievements"""
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Scholars", "20M+")
    with col2:
        st.metric("Institutions", "10K+")
    with col3:
        st.metric("Research Groups", "50K+")

elif st.session_state.current_tool == "📖 Knowledge Base":
    st.markdown("## 📖 Knowledge Base")
    st.markdown("Access comprehensive scientific knowledge across all disciplines")
    
    tabs = st.tabs(["Browse by Field", "Concepts", "Methodologies", "Protocols"])
    
    with tabs[0]:
        fields = ["Physics", "Chemistry", "Biology", "Mathematics", "Computer Science", 
                 "Medicine", "Engineering", "Environmental Science", "Neuroscience"]
        
        cols = st.columns(3)
        for idx, field in enumerate(fields):
            with cols[idx % 3]:
                if st.button(f"🔬 {field}", key=f"field_{field}", use_container_width=True):
                    with st.spinner(f"Loading {field} knowledge base..."):
                        try:
                            prompt = f"Provide an overview of key concepts, recent developments, and important research areas in {field}"
                            response = model.generate_content(prompt)
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
    
    with tabs[1]:
        concept_search = st.text_input("Search for a scientific concept...")
        if concept_search:
            with st.spinner("Searching..."):
                try:
                    prompt = f"Explain the scientific concept: {concept_search}. Include definition, applications, and related concepts."
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif st.session_state.current_tool == "🛠️ Uni-Lab":
    st.markdown("## 🛠️ Uni-Lab - Virtual Laboratory")
    st.markdown("Conduct virtual experiments and simulations")
    
    lab_tools = {
        "⚗️ Chemistry Lab": ["Titration", "Synthesis", "Spectroscopy"],
        "🔬 Biology Lab": ["Microscopy", "PCR", "Cell Culture"],
        "⚛️ Physics Lab": ["Mechanics", "Optics", "Electromagnetism"],
        "🧬 Molecular Lab": ["Protein Analysis", "DNA Sequencing", "CRISPR"]
    }
    
    selected_lab = st.selectbox("Select Laboratory", list(lab_tools.keys()))
    
    st.markdown(f"### {selected_lab}")
    experiment = st.selectbox("Choose Experiment", lab_tools[selected_lab])
    
    st.markdown("#### Experiment Setup")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Sample Name")
        st.number_input("Temperature (°C)", 20.0, 100.0, 25.0)
    with col2:
        st.number_input("Concentration (M)", 0.0, 10.0, 1.0)
        st.selectbox("Duration", ["5 min", "10 min", "30 min", "1 hour"])
    
    if st.button("🚀 Run Experiment"):
        with st.spinner("Running simulation..."):
            st.success("Experiment completed! View results below.")
            st.line_chart([1, 2, 3, 4, 5, 4, 3, 2, 1])

elif st.session_state.current_tool == "💾 Computation":
    st.markdown("## 💾 High-Performance Computing")
    st.markdown("Access cloud computing resources for intensive scientific calculations")
    
    tabs = st.tabs(["Job Manager", "Resources", "Datasets", "Results"])
    
    with tabs[0]:
        st.markdown("### Create New Job")
        job_name = st.text_input("Job Name")
        job_type = st.selectbox("Job Type", ["Molecular Dynamics", "Quantum Chemistry", "Machine Learning", "Data Analysis"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("CPU Cores", [4, 8, 16, 32, 64])
            st.selectbox("Memory (GB)", [16, 32, 64, 128, 256])
        with col2:
            st.selectbox("GPU", ["None", "1x V100", "2x V100", "4x V100"])
            st.number_input("Max Runtime (hours)", 1, 72, 24)
        
        if st.button("Submit Job"):
            st.success(f"Job '{job_name}' submitted successfully!")
    
    with tabs[1]:
        st.markdown("### Resource Usage")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CPU Hours Used", "245.6")
        with col2:
            st.metric("GPU Hours Used", "89.3")
        with col3:
            st.metric("Storage (TB)", "2.4")

elif st.session_state.current_tool == "📊 History":
    st.markdown("## 📊 Search & Activity History")
    
    tabs = st.tabs(["Search History", "Chat History", "Downloads", "Activity Timeline"])
    
    with tabs[0]:
        st.markdown("### Recent Searches")
        if st.session_state.search_history:
            for idx, item in enumerate(reversed(st.session_state.search_history[-20:])):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"🔍 {item['query']}")
                with col2:
                    st.caption(item['timestamp'])
                with col3:
                    if st.button("↻", key=f"repeat_{idx}"):
                        st.session_state.current_tool = "Science Navigator"
                        save_state()
                        st.rerun()
        else:
            st.info("No search history yet")
    
    with tabs[1]:
        st.markdown("### Chat History")
        if st.session_state.chat_history:
            for idx, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"💬 {chat['query'][:80]}... - {chat['timestamp']}"):
                    st.markdown(f"**Q:** {chat['query']}")
                    st.markdown(f"**A:** {chat['response'][:500]}...")
        else:
            st.info("No chat history yet")
    
    with tabs[2]:
        st.markdown("### Downloads")
        st.info("Downloaded papers and data will appear here")
    
    with tabs[3]:
        st.markdown("### Activity Timeline")
        st.info("Your complete activity timeline will be displayed here")

elif st.session_state.current_tool == "🌐 Explore":
    st.markdown("## 🌐 Explore Scientific Frontiers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔥 Trending Topics")
        trending = ["Quantum Computing", "CRISPR Gene Editing", "AI in Drug Discovery", 
                   "Climate Modeling", "Fusion Energy"]
        for topic in trending:
            if st.button(topic, key=f"trend_{topic}"):
                st.info(f"Exploring {topic}...")
    
    with col2:
        st.markdown("### 📈 Recent Breakthroughs")
        st.markdown("- New exoplanet discovered")
        st.markdown("- Cancer immunotherapy advance")
        st.markdown("- Quantum entanglement record")
    
    with col3:
        st.markdown("### 🏆 Nobel Laureates")
        st.markdown("- Physics: Attosecond pulses")
        st.markdown("- Chemistry: Quantum dots")
        st.markdown("- Medicine: mRNA vaccines")

else:
    st.markdown(f"## {st.session_state.current_tool}")
    st.info("This feature is under development. Stay tuned for updates!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📊 170M+ Papers")
with col2:
    st.caption("🔬 26 Disciplines")
with col3:
    st.caption("🌍 Global Research Network")

st.markdown("---")
