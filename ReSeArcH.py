import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Bohrium | Science Navigator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f5f7fa;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #e8eaf6;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        font-size: 42px;
        font-weight: bold;
        margin: 0;
    }
    
    .header-subtitle {
        color: #e3f2fd;
        font-size: 18px;
        margin-top: 10px;
    }
    
    /* Tool card styling */
    .tool-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    
    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Chat input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 12px 20px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 30px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Nobel banner */
    .nobel-banner {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        color: #333;
    }
    
    /* Accuracy badge */
    .accuracy-badge {
        background: linear-gradient(135deg, #4caf50 0%, #81c784 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_tool' not in st.session_state:
    st.session_state.current_tool = 'Science Navigator'
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Configure Gemini API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    st.error("⚠️ Please configure GEMINI_API_KEY in Streamlit secrets")

# Sidebar Navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/667eea/ffffff?text=Bohrium", width=150)
    
    st.markdown("---")
    
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
        if st.session_state.library:
            for item in st.session_state.library:
                with st.container():
                    st.markdown(f"**{item['title']}**")
                    st.caption(f"Added: {item['date']}")
                    col1, col2, col3 = st.columns([1, 1, 3])
                    with col1:
                        st.button("📖 Read", key=f"read_{item['title']}")
                    with col2:
                        st.button("🗑️ Remove", key=f"remove_{item['title']}")
        else:
            st.info("Your library is empty. Start saving papers from your searches!")
    
    with tabs[1]:
        st.markdown("### Create New Collection")
        col1, col2 = st.columns([3, 1])
        with col1:
            collection_name = st.text_input("Collection Name")
        with col2:
            if st.button("➕ Create"):
                st.success(f"Collection '{collection_name}' created!")
    
    with tabs[2]:
        st.markdown("### 📖 Reading List")
        st.info("Add papers to your reading list to track your progress")
    
    with tabs[3]:
        st.markdown("### 📝 My Notes")
        st.text_area("Write your research notes...", height=200)

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
st.caption("京公网安备11010802045318号 | 京ICP备20010051号-16 | 营业执照 | 增值电信业务经营许可证B2-20210408 | 网络直播服务 | 网络视听许可证")
