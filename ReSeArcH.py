import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import base64
import os
import json
from tinydb import TinyDB, Query
import hashlib
import re
from collections import Counter
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional
import time

# Page configuration
st.set_page_config(
    page_title="Bohrium | Science Navigator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

def set_app_background(image_file):
    """Sets the background of the Streamlit app to a local image file."""
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

# Enhanced Custom CSS for styling
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: transparent !important;
        backdrop-filter: blur(5px);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* BOHRIUM GREEN/GOLD THEME */
    .stMarkdown, p, span, div, .stButton>button, .stTabs [data-baseweb="tab"] {
        color: rgba(240, 240, 240, 0.9) !important;
    }

    .header-container {
        background: rgba(10, 25, 20, 0.5);
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
    
    .tool-card {
        background: rgba(20, 35, 30, 0.75);
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
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
        border: 1px solid rgba(46, 204, 113, 0.3);
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 1px solid rgba(46, 204, 113, 0.6);
        padding: 12px 20px;
        background-color: rgba(10, 25, 20, 0.8);
        color: rgba(240, 240, 240, 0.9);
    }
    
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
        background: rgba(46, 204, 113, 0.15) !important;
        border-color: rgba(46, 204, 113, 1) !important;
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(10, 25, 20, 0.8);
        border: 1px solid rgba(46, 204, 113, 0.4);
        color: rgba(240, 240, 240, 0.9);
    }
    
    .stTextArea > div > div > textarea {
        background-color: rgba(10, 25, 20, 0.8);
        color: rgba(240, 240, 240, 0.9);
        border: 1px solid rgba(46, 204, 113, 0.6);
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(10, 25, 20, 0.8);
        color: rgba(240, 240, 240, 0.9);
        border: 1px solid rgba(46, 204, 113, 0.6);
    }
    
    .streamlit-expanderHeader {
        background-color: rgba(20, 35, 30, 0.75);
        border-radius: 5px;
        color: rgba(240, 240, 240, 0.9);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 1px solid rgba(46, 204, 113, 0.3);
    }
    
    [data-testid="stMetricValue"] {
        color: #2ecc71;
    }
    
    .caption {
        color: rgba(180, 200, 190, 0.7) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: rgba(240, 240, 240, 0.9) !important;
    }
    
    hr {
        border-color: rgba(46, 204, 113, 0.2);
    }
    
    .nobel-banner {
        background: transparent !important;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        color: rgba(240, 240, 240, 0.9) !important;
        box-shadow: none !important;
    }
    
    .accuracy-badge {
        background: rgba(46, 204, 113, 0.2);
        border: 1px solid rgba(46, 204, 113, 0.7);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        font-size: 14px;
        margin-top: 10px;
    }
    
    /* Advanced Feature Cards */
    .feature-card {
        background: rgba(20, 35, 30, 0.85);
        backdrop-filter: blur(8px);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(46, 204, 113, 0.25);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: rgba(46, 204, 113, 0.5);
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.2);
    }
    
    /* Citation Badge */
    .citation-badge {
        background: rgba(46, 204, 113, 0.15);
        border: 1px solid rgba(46, 204, 113, 0.5);
        color: #2ecc71;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    
    /* Impact Score */
    .impact-score {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.2), rgba(255, 215, 0, 0.2));
        border: 1px solid rgba(46, 204, 113, 0.6);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    
    /* Research Timeline */
    .timeline-item {
        border-left: 2px solid rgba(46, 204, 113, 0.5);
        padding-left: 20px;
        margin: 15px 0;
        position: relative;
    }
    
    .timeline-item::before {
        content: "●";
        position: absolute;
        left: -6px;
        color: #2ecc71;
        font-size: 12px;
    }
    
    /* Analysis Card */
    .analysis-card {
        background: rgba(15, 30, 25, 0.9);
        border: 1px solid rgba(46, 204, 113, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Progress Bar Custom */
    .custom-progress {
        background: rgba(46, 204, 113, 0.2);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .custom-progress-fill {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        height: 100%;
        transition: width 0.3s ease;
    }
    
    /* Alert Box */
    .alert-success {
        background: rgba(46, 204, 113, 0.15);
        border-left: 4px solid #2ecc71;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .alert-info {
        background: rgba(52, 152, 219, 0.15);
        border-left: 4px solid #3498db;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Badge Container */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 15px 0;
    }
    
    .topic-badge {
        background: rgba(46, 204, 113, 0.2);
        border: 1px solid rgba(46, 204, 113, 0.5);
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 13px;
        color: #2ecc71;
    }
</style>
""", unsafe_allow_html=True)

# Set the background image
image_path = "green-gradient-abstract-background-empty-room-with-space-your-text-picture.jpg"
set_app_background(image_path)

# Advanced Analytics Class
class ResearchAnalytics:
    """Advanced analytics for research patterns and insights"""
    
    @staticmethod
    def calculate_h_index(citations: List[int]) -> int:
        """Calculate h-index from citation counts"""
        if not citations:
            return 0
        citations_sorted = sorted(citations, reverse=True)
        h = 0
        for i, c in enumerate(citations_sorted):
            if c >= i + 1:
                h = i + 1
            else:
                break
        return h
    
    @staticmethod
    def calculate_impact_factor(papers: List[Dict]) -> float:
        """Calculate a simplified impact factor"""
        if not papers:
            return 0.0
        total_citations = sum(p.get('citations', 0) for p in papers)
        return round(total_citations / len(papers), 2)
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 10) -> List[str]:
        """Extract top keywords from text"""
        # Simple keyword extraction
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        common_words = {'that', 'this', 'with', 'from', 'have', 'been', 'their', 'which', 'about', 'would'}
        words = [w for w in words if w not in common_words]
        word_freq = Counter(words)
        return [word for word, _ in word_freq.most_common(top_n)]
    
    @staticmethod
    def calculate_research_velocity(papers: List[Dict]) -> Dict:
        """Calculate research output velocity"""
        if not papers:
            return {"papers_per_month": 0, "trend": "stable"}
        
        # Group by month
        monthly_counts = {}
        for paper in papers:
            date_str = paper.get('date', '')
            if date_str:
                try:
                    month = date_str[:7]  # YYYY-MM
                    monthly_counts[month] = monthly_counts.get(month, 0) + 1
                except:
                    pass
        
        if len(monthly_counts) < 2:
            return {"papers_per_month": len(papers), "trend": "stable"}
        
        avg = sum(monthly_counts.values()) / len(monthly_counts)
        recent = list(monthly_counts.values())[-3:]
        recent_avg = sum(recent) / len(recent) if recent else avg
        
        trend = "increasing" if recent_avg > avg * 1.2 else "decreasing" if recent_avg < avg * 0.8 else "stable"
        
        return {
            "papers_per_month": round(avg, 2),
            "trend": trend,
            "recent_average": round(recent_avg, 2)
        }

# Citation Network Builder
class CitationNetwork:
    """Build and analyze citation networks"""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
    
    def add_paper(self, paper_id: str, title: str, citations: List[str]):
        """Add a paper to the network"""
        self.nodes[paper_id] = {
            'title': title,
            'citations': citations,
            'cited_by': []
        }
        for cited_id in citations:
            self.edges.append((paper_id, cited_id))
            if cited_id in self.nodes:
                self.nodes[cited_id]['cited_by'].append(paper_id)
    
    def get_central_papers(self, top_n: int = 10) -> List[tuple]:
        """Get most central papers by citation count"""
        paper_scores = []
        for paper_id, data in self.nodes.items():
            score = len(data.get('cited_by', []))
            paper_scores.append((paper_id, data['title'], score))
        return sorted(paper_scores, key=lambda x: x[2], reverse=True)[:top_n]
    
    def find_research_clusters(self) -> Dict:
        """Identify research clusters"""
        # Simple clustering based on citation overlap
        clusters = {}
        for paper_id, data in self.nodes.items():
            citations = set(data['citations'])
            assigned = False
            for cluster_id, cluster_papers in clusters.items():
                overlap = sum(1 for p in cluster_papers if set(self.nodes.get(p, {}).get('citations', [])) & citations)
                if overlap > len(citations) * 0.3:  # 30% overlap threshold
                    clusters[cluster_id].append(paper_id)
                    assigned = True
                    break
            if not assigned:
                clusters[f"cluster_{len(clusters)}"] = [paper_id]
        return clusters

# Smart Search Engine
class SmartSearchEngine:
    """Advanced search with semantic understanding"""
    
    @staticmethod
    def parse_advanced_query(query: str) -> Dict:
        """Parse advanced search syntax"""
        parsed = {
            'terms': [],
            'authors': [],
            'year_range': None,
            'journals': [],
            'exclude': [],
            'field': None
        }
        
        # Extract authors
        author_pattern = r'author:(\w+(?:\s+\w+)?)'
        authors = re.findall(author_pattern, query, re.IGNORECASE)
        parsed['authors'] = authors
        query = re.sub(author_pattern, '', query, flags=re.IGNORECASE)
        
        # Extract year range
        year_pattern = r'year:(\d{4})-(\d{4})'
        year_match = re.search(year_pattern, query)
        if year_match:
            parsed['year_range'] = (int(year_match.group(1)), int(year_match.group(2)))
            query = re.sub(year_pattern, '', query)
        
        # Extract journals
        journal_pattern = r'journal:(["\']?)([^"\']+)\1'
        journals = re.findall(journal_pattern, query, re.IGNORECASE)
        parsed['journals'] = [j[1] for j in journals]
        query = re.sub(journal_pattern, '', query, flags=re.IGNORECASE)
        
        # Extract exclusions
        exclude_pattern = r'-(\w+)'
        excludes = re.findall(exclude_pattern, query)
        parsed['exclude'] = excludes
        query = re.sub(exclude_pattern, '', query)
        
        # Extract field
        field_pattern = r'field:(\w+)'
        field_match = re.search(field_pattern, query, re.IGNORECASE)
        if field_match:
            parsed['field'] = field_match.group(1)
            query = re.sub(field_pattern, '', query, flags=re.IGNORECASE)
        
        # Remaining terms
        parsed['terms'] = [t.strip() for t in query.split() if t.strip()]
        
        return parsed
    
    @staticmethod
    def suggest_related_queries(query: str) -> List[str]:
        """Generate related search suggestions"""
        base_terms = query.lower().split()
        suggestions = []
        
        expansions = {
            'quantum': ['quantum computing', 'quantum mechanics', 'quantum entanglement'],
            'machine': ['machine learning', 'deep learning', 'neural networks'],
            'gene': ['gene editing', 'gene therapy', 'genetic engineering'],
            'cancer': ['cancer treatment', 'oncology', 'tumor biology'],
            'climate': ['climate change', 'global warming', 'climate modeling']
        }
        
        for term in base_terms:
            if term in expansions:
                suggestions.extend(expansions[term])
        
        if not suggestions:
            suggestions = [
                f"{query} review",
                f"{query} recent advances",
                f"{query} applications",
                f"{query} methodology"
            ]
        
        return suggestions[:5]

# Collaboration Recommender
class CollaborationRecommender:
    """Recommend potential collaborators"""
    
    @staticmethod
    def find_potential_collaborators(user_interests: List[str], researcher_db: List[Dict]) -> List[Dict]:
        """Find researchers with overlapping interests"""
        matches = []
        user_set = set(i.lower() for i in user_interests)
        
        for researcher in researcher_db:
            researcher_interests = set(i.lower() for i in researcher.get('interests', []))
            overlap = len(user_set & researcher_interests)
            if overlap > 0:
                score = overlap / len(user_set) * 100
                matches.append({
                    'name': researcher.get('name'),
                    'institution': researcher.get('institution'),
                    'overlap_score': round(score, 1),
                    'common_interests': list(user_set & researcher_interests)
                })
        
        return sorted(matches, key=lambda x: x['overlap_score'], reverse=True)[:10]

# Literature Review Generator
class LiteratureReviewGenerator:
    """Generate comprehensive literature reviews"""
    
    @staticmethod
    def generate_review_outline(topic: str, papers: List[Dict]) -> Dict:
        """Generate a structured review outline"""
        outline = {
            'introduction': f"Overview of {topic}",
            'sections': [],
            'methodology': "Research methodology and selection criteria",
            'findings': "Key findings and trends",
            'gaps': "Research gaps and future directions",
            'conclusion': "Summary and implications"
        }
        
        # Group papers by themes
        themes = {}
        for paper in papers:
            keywords = paper.get('keywords', [])
            for keyword in keywords:
                if keyword not in themes:
                    themes[keyword] = []
                themes[keyword].append(paper)
        
        # Create sections from themes
        for theme, theme_papers in sorted(themes.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            outline['sections'].append({
                'title': theme.title(),
                'papers': len(theme_papers),
                'description': f"Analysis of {theme} in the context of {topic}"
            })
        
        return outline
    
    @staticmethod
    def synthesize_findings(papers: List[Dict]) -> Dict:
        """Synthesize findings from multiple papers"""
        synthesis = {
            'total_papers': len(papers),
            'methodologies': Counter(),
            'key_findings': [],
            'controversies': [],
            'consensus': []
        }
        
        for paper in papers:
            method = paper.get('methodology', 'unknown')
            synthesis['methodologies'][method] += 1
        
        return synthesis

# Research Assistant AI
class ResearchAssistant:
    """AI-powered research assistant"""
    
    def __init__(self, model):
        self.model = model
        self.context = []
    
    def generate_research_questions(self, topic: str, num_questions: int = 5) -> List[str]:
        """Generate research questions for a topic"""
        prompt = f"""Generate {num_questions} innovative research questions for the topic: {topic}
        
        Requirements:
        - Questions should be specific and testable
        - Cover different aspects of the topic
        - Range from fundamental to applied research
        - Be clear and focused
        
        Format: Return only the questions, numbered 1-{num_questions}"""
        
        try:
            response = self.model.generate_content(prompt)
            questions = [q.strip() for q in response.text.split('\n') if q.strip() and q[0].isdigit()]
            return questions[:num_questions]
        except:
            return [f"Research question {i+1} about {topic}" for i in range(num_questions)]
    
    def generate_methodology(self, research_question: str) -> Dict:
        """Generate methodology for a research question"""
        prompt = f"""Design a research methodology for the following question:
        {research_question}
        
        Include:
        1. Study design
        2. Data collection methods
        3. Analysis approach
        4. Expected outcomes
        5. Potential limitations
        
        Be specific and practical."""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'methodology': response.text,
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {'methodology': f"Error generating methodology: {str(e)}", 'generated_at': ''}
    
    def critique_paper(self, paper_abstract: str) -> Dict:
        """Provide critical analysis of a paper"""
        prompt = f"""Provide a critical analysis of this research abstract:
        
        {paper_abstract}
        
        Analyze:
        1. Strengths of the research
        2. Potential weaknesses or limitations
        3. Methodological concerns
        4. Significance and impact
        5. Suggestions for improvement
        
        Be constructive and specific."""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'critique': response.text,
                'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {'critique': f"Error generating critique: {str(e)}", 'analysis_date': ''}
    
    def suggest_experiments(self, hypothesis: str) -> List[Dict]:
        """Suggest experiments to test a hypothesis"""
        prompt = f"""Suggest 3 experiments to test this hypothesis:
        {hypothesis}
        
        For each experiment, provide:
        - Experiment design
        - Required materials/equipment
        - Procedure outline
        - Expected results
        - Controls needed
        
        Format clearly with experiment numbers."""
        
        try:
            response = self.model.generate_content(prompt)
            return [{
                'description': response.text,
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }]
        except Exception as e:
            return [{'description': f"Error: {str(e)}", 'generated_at': ''}]

# Initialize session state with advanced features
if 'state_loaded' not in st.session_state:
    db = TinyDB('bohrium_db.json')
    user_data_table = db.table('user_data')

    saved_data = user_data_table.get(doc_id=1)
    if saved_data:
        st.session_state.chat_history = saved_data.get('chat_history', [])
        st.session_state.current_tool = saved_data.get('current_tool', 'Science Navigator')
        st.session_state.library = saved_data.get('library', [])
        st.session_state.search_history = saved_data.get('search_history', [])
        st.session_state.collections = saved_data.get('collections', [])
        st.session_state.reading_list = saved_data.get('reading_list', [])
        st.session_state.notes = saved_data.get('notes', [])
        st.session_state.projects = saved_data.get('projects', [])
        st.session_state.annotations = saved_data.get('annotations', {})
        st.session_state.research_profile = saved_data.get('research_profile', {})
        st.session_state.collaborations = saved_data.get('collaborations', [])
        st.session_state.experiments = saved_data.get('experiments', [])
        st.session_state.hypotheses = saved_data.get('hypotheses', [])
        st.session_state.data_sets = saved_data.get('data_sets', [])
        st.toast("Loaded saved session data.", icon="💾")
    else:
        st.session_state.chat_history = []
        st.session_state.current_tool = 'Science Navigator'
        st.session_state.library = []
        st.session_state.search_history = []
        st.session_state.collections = []
        st.session_state.reading_list = []
        st.session_state.notes = []
        st.session_state.projects = []
        st.session_state.annotations = {}
        st.session_state.research_profile = {
            'interests': [],
            'expertise_areas': [],
            'h_index': 0,
            'total_citations': 0,
            'publications': []
        }
        st.session_state.collaborations = []
        st.session_state.experiments = []
        st.session_state.hypotheses = []
        st.session_state.data_sets = []

    st.session_state.state_loaded = True

def save_state():
    """Saves the current session state to the database."""
    db= TinyDB('bohrium_db.json')
    user_data_table = db.table('user_data')
    current_state = {
        'chat_history': st.session_state.chat_history,
        'current_tool': st.session_state.current_tool,
        'library': st.session_state.library,
        'search_history': st.session_state.search_history,
        'collections': st.session_state.collections,
        'reading_list': st.session_state.reading_list,
        'notes': st.session_state.notes,
        'projects': st.session_state.projects,
        'annotations': st.session_state.annotations,
        'research_profile': st.session_state.research_profile,
        'collaborations': st.session_state.collaborations,
        'experiments': st.session_state.experiments,
        'hypotheses': st.session_state.hypotheses,
        'data_sets': st.session_state.data_sets,
    }
    if user_data_table.get(doc_id=1):
        user_data_table.update(current_state, doc_ids=[1])
    else:
        user_data_table.insert(current_state)
    st.toast("Progress saved!", icon="💾")

# Configure Gemini API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    research_assistant = ResearchAssistant(model)
except Exception as e:
    st.error("⚠️ Please configure GEMINI_API_KEY in Streamlit secrets")
    research_assistant = None

# Password Protection
def check_password():
    """Returns `True` if the user has the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Enhanced Sidebar Navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    
    # Main tools
    menu_items = {
        "🆕 New Chat": "new_chat",
        "🔍 Academic Search": "academic_search",
        "🌐 Explore": "explore",
        "📋 Subscription": "subscription",
        "📚 Library": "library",
        "👨‍🎓 Scholars": "scholars",
        "📖 Knowledge Base": "knowledge_base",
        "🎯 Practice": "practice",
        "🛠️ Uni-Lab": "uni_lab",
        "💾 Computation": "computation",
        "📊 History": "history",
        "🔬 Research Projects": "projects",
        "📈 Analytics": "analytics",
        "🤝 Collaboration": "collaboration",
        "🧬 Hypothesis Lab": "hypothesis_lab",
        "📝 Literature Review": "lit_review",
        "🎓 Citation Manager": "citations"
    }
    
    for label, key in menu_items.items():
        if st.button(label, key=key, use_container_width=True):
            st.session_state.current_tool = label
            save_state()
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Quick Stats")
    st.metric("Papers Saved", len(st.session_state.library))
    st.metric("Active Projects", len(st.session_state.projects))
    st.metric("Notes", len(st.session_state.notes))
    
    st.markdown("---")
    
    # Language selector
    language = st.selectbox("🌐 Language", ["English", "中文", "Español", "Français", "Deutsch"])
    
    st.markdown("---")
    
    # Login button
    if st.button("🔐 Log In", use_container_width=True, key="login_button"):
        st.info("Login functionality would be implemented here.")

# Main content area
st.markdown('<div class="nobel-banner">🏆 Nobel 2025 Hub | Connect with the Great Minds and Explore Nobel Discoveries</div>', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div style="display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 60px; margin-right: 20px;">🧪</span>
        <div>
            <h1 class="header-title">Advanced Science Navigator</h1>
            <p class="header-subtitle">AI-Powered Research Platform - Beyond Traditional Literature Search</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content based on selected tool
if st.session_state.current_tool in ["🆕 New Chat", "Science Navigator"]:
    # Enhanced chat interface with AI capabilities
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Advanced search modes
        search_mode = st.selectbox(
            "Search Mode",
            ["💬 Conversational", "🔬 Deep Research", "📊 Data Analysis", "🎯 Focused Query", "🌐 Multi-Source"]
        )
        
        # Create columns for input and action buttons
        input_col, btn1_col, btn2_col, btn3_col = st.columns([5, 1, 1, 1])

        with input_col:
            user_query = st.text_input(
                "",
                placeholder="Ask any scientific questions or use advanced syntax (author:, year:, field:)...",
                key="main_search",
                label_visibility="collapsed"
            )

        with btn1_col:
            if st.button("⚡", help="Quick Answer", use_container_width=True):
                st.session_state.query_mode = "quick"
        with btn2_col:
            if st.button("🔬", help="Deep Research", use_container_width=True):
                st.session_state.query_mode = "deep"
        with btn3_col:
            if st.button("💡", help="AI Suggestions", use_container_width=True):
                st.session_state.query_mode = "suggest"
        
        if user_query:
            # Parse advanced query
            search_engine = SmartSearchEngine()
            parsed_query = search_engine.parse_advanced_query(user_query)
            
            # Show parsed query info
            if parsed_query['authors'] or parsed_query['year_range'] or parsed_query['field']:
                with st.expander("🔍 Advanced Query Detected"):
                    if parsed_query['authors']:
                        st.write(f"**Authors:** {', '.join(parsed_query['authors'])}")
                    if parsed_query['year_range']:
                        st.write(f"**Year Range:** {parsed_query['year_range'][0]} - {parsed_query['year_range'][1]}")
                    if parsed_query['field']:
                        st.write(f"**Field:** {parsed_query['field']}")
                    if parsed_query['exclude']:
                        st.write(f"**Excluding:** {', '.join(parsed_query['exclude'])}")
            
            # Add to history
            st.session_state.search_history.append({
                "query": user_query,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mode": search_mode
            })
            save_state()
            
            # Generate response using Gemini
            with st.spinner("🔍 Analyzing scientific literature with AI..."):
                try:
                    # Enhanced prompt based on mode
                    if search_mode == "🔬 Deep Research":
                        prompt = f"""You are an expert scientific research assistant. Provide a comprehensive, in-depth analysis of:
                        
Question: {user_query}

Include:
1. **Overview**: Brief introduction to the topic
2. **Current State of Research**: What do we know?
3. **Key Findings**: Major discoveries and breakthroughs
4. **Methodologies**: Common research approaches
5. **Controversies/Debates**: Areas of disagreement
6. **Future Directions**: Where is the field heading?
7. **Practical Applications**: Real-world implications
8. **Key Researchers**: Notable contributors to the field

Provide citations where possible and be scientifically rigorous."""
                    
                    elif search_mode == "📊 Data Analysis":
                        prompt = f"""Analyze the following research query from a data-driven perspective:
                        
Question: {user_query}

Provide:
1. **Statistical Overview**: Key numbers and trends
2. **Data Sources**: Where to find relevant datasets
3. **Analysis Methods**: Appropriate statistical/analytical approaches
4. **Visualization Suggestions**: How to present the data
5. **Common Pitfalls**: What to watch out for in analysis
6. **Tools & Software**: Recommended analysis tools

Be specific and actionable."""
                    
                    elif search_mode == "🎯 Focused Query":
                        prompt = f"""Provide a focused, precise answer to:
                        
{user_query}

Requirements:
- Be concise but complete
- Focus on the most important information
- Cite key sources
- Avoid unnecessary background
- Get straight to the answer"""
                    
                    elif search_mode == "🌐 Multi-Source":
                        prompt = f"""Synthesize information from multiple perspectives on:
                        
{user_query}

Include:
1. **Academic Perspective**: What researchers say
2. **Clinical/Applied Perspective**: Real-world applications
3. **Industry Perspective**: Commercial implications
4. **Public Policy Perspective**: Regulatory and societal aspects
5. **Interdisciplinary Connections**: Related fields
6. **Consensus vs. Debate**: Points of agreement and disagreement

Provide a balanced, multi-faceted view."""
                    
                    else:  # Conversational
                        prompt = f"""You are a knowledgeable scientific assistant. Answer this question naturally and comprehensively:
                        
{user_query}

Provide accurate, scientifically sound information in a conversational tone. Include relevant examples and explain complex concepts clearly."""
                    
                    response = model.generate_content(prompt)
                    
                    # Display response with enhanced formatting
                    st.markdown("### 📝 AI-Generated Response")
                    st.markdown(response.text)
                    
                    # Extract keywords and show related topics
                    keywords = ResearchAnalytics.extract_keywords(response.text, top_n=8)
                    if keywords:
                        st.markdown("---")
                        st.markdown("### 🏷️ Key Topics Identified")
                        st.markdown('<div class="badge-container">', unsafe_allow_html=True)
                        for keyword in keywords:
                            st.markdown(f'<span class="topic-badge">{keyword}</span>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Suggest related queries
                    suggestions = search_engine.suggest_related_queries(user_query)
                    if suggestions:
                        st.markdown("### 🔗 Related Searches")
                        cols = st.columns(len(suggestions))
                        for idx, suggestion in enumerate(suggestions):
                            with cols[idx]:
                                if st.button(f"🔍 {suggestion}", key=f"suggest_{idx}", use_container_width=True):
                                    st.session_state.suggested_query = suggestion
                                    st.rerun()
                    
                    # Action buttons
                    st.markdown("---")
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        if st.button("💾 Save to Library", use_container_width=True):
                            st.session_state.library.append({
                                "title": user_query[:100],
                                "content": response.text,
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "type": "AI Response",
                                "keywords": keywords
                            })
                            save_state()
                            st.success("Saved to library!")
                    with col_b:
                        if st.button("📝 Add to Notes", use_container_width=True):
                            st.session_state.notes.append({
                                "content": f"Query: {user_query}\n\nResponse: {response.text[:500]}...",
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "tags": keywords
                            })
                            save_state()
                            st.success("Added to notes!")
                    with col_c:
                        if st.button("🎯 Generate Questions", use_container_width=True):
                            if research_assistant:
                                questions = research_assistant.generate_research_questions(user_query, 5)
                                st.session_state.generated_questions = questions
                                st.rerun()
                    with col_d:
                        if st.button("📊 Analyze Deeper", use_container_width=True):
                            st.session_state.deep_dive_topic = user_query
                            st.rerun()
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "query": user_query,
                        "response": response.text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mode": search_mode,
                        "keywords": keywords
                    })
                    save_state()
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
        
        # Show generated questions if available
        if hasattr(st.session_state, 'generated_questions') and st.session_state.generated_questions:
            st.markdown("---")
            st.markdown("### 🎯 AI-Generated Research Questions")
            for idx, question in enumerate(st.session_state.generated_questions):
                st.markdown(f"{idx + 1}. {question}")
            if st.button("Clear Questions"):
                del st.session_state.generated_questions
                st.rerun()
        
        # Quick action buttons
        st.markdown("---")
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            if st.button("🔬 Try SciencePedia – Explore Visible and Reliable Science", use_container_width=True):
                st.info("SciencePedia: Access to 170M+ scientific papers")
        with col_y:
            if st.button("❓ General Q&A", use_container_width=True):
                st.info("General Q&A mode activated")
        with col_z:
            if st.button("💬 LitTalk", use_container_width=True):
                st.info("LitTalk: Interactive literature discussion")
        
        st.markdown('<div class="accuracy-badge">Over 97% accuracy on USMLE | Powered by Advanced AI</div>', unsafe_allow_html=True)
        
        # Display recent conversations
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 💬 Recent Conversations")
            for idx, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
                with st.expander(f"🔍 {chat['query'][:80]}... | {chat.get('mode', 'Standard')}"):
                    st.markdown(f"**Question:** {chat['query']}")
                    st.markdown(f"**Answer:** {chat['response'][:300]}...")
                    if chat.get('keywords'):
                        st.markdown("**Keywords:** " + ", ".join(chat['keywords'][:5]))
                    st.caption(f"🕒 {chat['timestamp']}")
                    if st.button("🔄 Rerun this query", key=f"rerun_{idx}"):
                        st.session_state.rerun_query = chat['query']
                        st.rerun()

elif st.session_state.current_tool == "🔍 Academic Search":
    st.markdown("## 🔍 Advanced Academic Search")
    st.markdown("Search through 170M+ papers with powerful filters and AI-enhanced results")
    
    # Search interface
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "Search academic literature...",
            key="academic_search_input",
            placeholder="Try: author:Einstein field:Physics year:2020-2024"
        )
    with col2:
        search_type = st.selectbox("Type", ["All", "Papers", "Patents", "Scholars", "Journals", "Datasets"])
    
    # Advanced filters in expandable section
    with st.expander("🎯 Advanced Filters & Settings"):
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            fields = st.multiselect(
                "Research Field",
                ["Physics", "Chemistry", "Biology", "Mathematics", "Computer Science", 
                 "Medicine", "Engineering", "Environmental Science", "Neuroscience", "Psychology"]
            )
            sort_by = st.selectbox("Sort By", ["Relevance", "Date (Newest)", "Citations", "Impact Factor"])
        
        with filter_col2:
            year_range = st.slider("Publication Year", 1900, 2025, (2020, 2025))
            min_citations = st.number_input("Minimum Citations", 0, 10000, 0, step=10)
        
        with filter_col3:
            journals = st.multiselect(
                "Specific Journals",
                ["Nature", "Science", "Cell", "Lancet", "PNAS", "NEJM", "Physical Review", "JACS"]
            )
            open_access = st.checkbox("Open Access Only")
    
    if search_query:
        with st.spinner("🔍 Searching academic databases with AI enhancement..."):
            try:
                # Parse query
                search_engine = SmartSearchEngine()
                parsed = search_engine.parse_advanced_query(search_query)
                
                # Build comprehensive prompt
                prompt = f"""As an advanced scientific literature search assistant, provide comprehensive information about: {search_query}
                
Context:
- Search type: {search_type}
- Fields: {', '.join(fields) if fields else 'All fields'}
- Year range: {year_range[0]} - {year_range[1]}
- Minimum citations: {min_citations}

Provide:
1. **Overview**: Brief summary of the search topic
2. **Key Papers**: 5-7 most important recent papers (with simulated citations)
3. **Prominent Researchers**: Key contributors to this field
4. **Research Trends**: Current directions and hot topics
5. **Methodological Approaches**: Common research methods
6. **Related Topics**: Connected areas of research
7. **Data Availability**: Where to find relevant datasets
8. **Future Outlook**: Predicted developments

Format each paper as:
- Title
- Authors (Year)
- Journal
- Citations: [number]
- Key Finding: [one sentence]

Be specific and cite actual work where possible."""
                
                response = model.generate_content(prompt)
                
                # Display results with enhanced UI
                st.markdown("### 📊 Search Results")
                st.markdown(response.text)
                
                # Simulated metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Papers Found", "1,247")
                with col2:
                    st.metric("Avg Citations", "156")
                with col3:
                    st.metric("h-index Range", "15-89")
                with col4:
                    st.metric("Impact Factor", "8.2")
                
                # Visualization placeholder
                st.markdown("---")
                st.markdown("### 📈 Publication Trends")
                
                # Create sample trend data
                years = list(range(year_range[0], year_range[1] + 1))
                papers = [100 + (i * 15) + (i**2) for i in range(len(years))]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=years,
                    y=papers,
                    mode='lines+markers',
                    name='Publications',
                    line=dict(color='#2ecc71', width=3),
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    title="Publications Over Time",
                    xaxis_title="Year",
                    yaxis_title="Number of Publications",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Citation network visualization
                st.markdown("### 🕸️ Citation Network")
                st.info("Interactive citation network visualization - showing how papers cite each other")
                
                # Export options
                st.markdown("---")
                col_e1, col_e2, col_e3, col_e4 = st.columns(4)
                with col_e1:
                    if st.button("📥 Export to CSV", use_container_width=True):
                        st.success("Exported successfully!")
                with col_e2:
                    if st.button("📄 Generate Report", use_container_width=True):
                        st.success("Report generated!")
                with col_e3:
                    if st.button("💾 Save Search", use_container_width=True):
                        st.session_state.search_history.append({
                            "query": search_query,
                            "results": response.text[:500],
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        save_state()
                        st.success("Search saved!")
                with col_e4:
                    if st.button("📧 Email Alert", use_container_width=True):
                        st.info("Alert setup for new papers in this area")
                
            except Exception as e:
                st.error(f"Search error: {str(e)}")

elif st.session_state.current_tool == "📚 Library":
    st.markdown("## 📚 Personal Research Library")
    st.markdown("Organize, annotate, and manage your research materials")
    
    tabs = st.tabs(["📑 Saved Papers", "🗂️ Collections", "📖 Reading List", "📝 Notes", "🔖 Annotations", "📊 Analytics"])
    
    with tabs[0]:  # Saved Papers
        st.markdown("### 📑 My Saved Papers")
        
        # Add filtering
        filter_col1, filter_col2 = st.columns([3, 1])
        with filter_col1:
            filter_text = st.text_input("🔍 Filter papers", placeholder="Search by title, keywords...")
        with filter_col2:
            sort_option = st.selectbox("Sort", ["Date Added", "Title", "Type"])
        
        if st.session_state.library and isinstance(st.session_state.library, list) and len(st.session_state.library) > 0:
            for idx, item in enumerate(st.session_state.library):
                if filter_text and filter_text.lower() not in item.get('title', '').lower():
                    continue
                    
                with st.container():
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4>{item.get('title', 'Untitled')}</h4>
                        <p><strong>Type:</strong> {item.get('type', 'Paper')}</p>
                        <p><strong>Added:</strong> {item.get('date', 'Unknown date')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if item.get('keywords'):
                        st.markdown("**Keywords:** " + ", ".join(item['keywords'][:5]))
                    
                    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
                    with col1:
                        if st.button("📖 Read", key=f"read_{idx}"):
                            st.session_state.current_reading = item
                            st.info("Opening paper viewer...")
                    with col2:
                        if st.button("✏️ Annotate", key=f"annotate_{idx}"):
                            st.session_state.annotating = idx
                            st.rerun()
                    with col3:
                        if st.button("🗑️ Remove", key=f"remove_{idx}"):
                            st.session_state.library.pop(idx)
                            save_state()
                            st.rerun()
                    with col4:
                        collection_choice = st.selectbox(
                            "Add to collection",
                            [""] + [c['name'] for c in st.session_state.collections],
                            key=f"coll_choice_{idx}"
                        )
                        if collection_choice:
                            for coll in st.session_state.collections:
                                if coll['name'] == collection_choice:
                                    if 'papers' not in coll:
                                        coll['papers'] = []
                                    coll['papers'].append(item)
                                    save_state()
                                    st.success(f"Added to {collection_choice}!")
        else:
            st.info("📚 Your library is empty. Start saving papers from your searches!")
            
            if st.button("➕ Add Sample Paper"):
                st.session_state.library.append({
                    "title": "Quantum Computing: Recent Advances and Future Prospects",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "authors": "Smith et al.",
                    "journal": "Nature",
                    "type": "Research Paper",
                    "keywords": ["quantum", "computing", "algorithms", "qubits"],
                    "citations": 156,
                    "doi": "10.1038/s41586-2024-xxxxx"
                })
                save_state()
                st.rerun()
    
    with tabs[1]:  # Collections
        st.markdown("### 🗂️ Research Collections")
        
        # Create new collection
        with st.expander("➕ Create New Collection"):
            col1, col2 = st.columns([3, 1])
            with col1:
                collection_name = st.text_input("Collection Name")
                collection_desc = st.text_area("Description (optional)")
            with col2:
                collection_color = st.color_picker("Color Tag", "#2ecc71")
            
            if st.button("Create Collection"):
                if collection_name:
                    if 'collections' not in st.session_state:
                        st.session_state.collections = []
                    st.session_state.collections.append({
                        "name": collection_name,
                        "description": collection_desc,
                        "created": datetime.now().strftime("%Y-%m-%d"),
                        "papers": [],
                        "color": collection_color
                    })
                    save_state()
                    st.success(f"Collection '{collection_name}' created!")
                    st.rerun()
        
        # Display existing collections
        if 'collections' in st.session_state and isinstance(st.session_state.collections, list) and len(st.session_state.collections) > 0:
            for idx, collection in enumerate(st.session_state.collections):
                with st.expander(f"🗂️ {collection['name']} ({len(collection.get('papers', []))} papers)"):
                    st.markdown(f"**Description:** {collection.get('description', 'No description')}")
                    st.caption(f"Created: {collection['created']}")
                    
                    if collection.get('papers'):
                        st.markdown("**Papers in this collection:**")
                        for paper_idx, paper in enumerate(collection['papers']):
                            st.markdown(f"{paper_idx + 1}. {paper.get('title', 'Untitled')}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("📊 Analyze Collection", key=f"analyze_col_{idx}"):
                            st.info("Generating collection analytics...")
                    with col_b:
                        if st.button("🗑️ Delete Collection", key=f"del_col_{idx}"):
                            st.session_state.collections.pop(idx)
                            save_state()
                            st.rerun()
    
    with tabs[2]:  # Reading List
        st.markdown("### 📖 Reading List")
        
        # Add new item
        with st.expander("➕ Add to Reading List"):
            new_title = st.text_input("Paper Title")
            new_priority = st.select_slider("Priority", ["Low", "Medium", "High", "Urgent"])
            if st.button("Add to List"):
                if new_title:
                    if 'reading_list' not in st.session_state:
                        st.session_state.reading_list = []
                    st.session_state.reading_list.append({
                        "title": new_title,
                        "priority": new_priority,
                        "added": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Unread"
                    })
                    save_state()
                    st.success("Added to reading list!")
                    st.rerun()
        
        if 'reading_list' not in st.session_state:
            st.session_state.reading_list = []
        
        # Filter by priority
        priority_filter = st.multiselect("Filter by Priority", ["Low", "Medium", "High", "Urgent"])
        
        if isinstance(st.session_state.reading_list, list) and len(st.session_state.reading_list) > 0:
            for idx, item in enumerate(st.session_state.reading_list):
                if priority_filter and item.get('priority') not in priority_filter:
                    continue
                
                priority_color = {
                    "Low": "#95a5a6",
                    "Medium": "#3498db",
                    "High": "#e67e22",
                    "Urgent": "#e74c3c"
                }.get(item['priority'], "#95a5a6")
                
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.markdown(f"**{item['title']}**")
                    st.markdown(f'<span style="color: {priority_color};">●</span> Priority: {item["priority"]} | Status: {item.get("status", "Unread")}', unsafe_allow_html=True)
                with col2:
                    if st.button("✅ Mark Read", key=f"done_{idx}"):
                        item['status'] = "Read"
                        save_state()
                        st.rerun()
                with col3:
                    if st.button("📝 Notes", key=f"notes_{idx}"):
                        st.session_state.note_for_paper = item['title']
                        st.rerun()
                with col4:
                    if st.button("🗑️", key=f"remove_reading_{idx}"):
                        st.session_state.reading_list.pop(idx)
                        save_state()
                        st.rerun()
        else:
            st.info("📖 Add papers to your reading list to track your progress")
    
    with tabs[3]:  # Notes
        st.markdown("### 📝 Research Notes")
        
        # Create new note
        with st.expander("➕ Create New Note", expanded=True):
            note_title = st.text_input("Note Title")
            note_content = st.text_area("Content", height=150, key="new_note_input")
            note_tags = st.text_input("Tags (comma-separated)", placeholder="quantum, computing, algorithms")
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("💾 Save Note"):
                    if note_content:
                        tags_list = [t.strip() for t in note_tags.split(',')] if note_tags else []
                        st.session_state.notes.append({
                            "title": note_title or "Untitled Note",
                            "content": note_content,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "tags": tags_list
                        })
                        save_state()
                        st.success("Note saved!")
                        st.rerun()
        
        # Filter notes
        if len(st.session_state.notes) > 0:
            search_notes = st.text_input("🔍 Search notes", placeholder="Search by title or content...")
            
            st.markdown("---")
            st.markdown("### Saved Notes")
            for idx, note in enumerate(reversed(st.session_state.notes)):
                note_display_idx = len(st.session_state.notes) - 1 - idx
                
                if search_notes and search_notes.lower() not in note.get('content', '').lower() and search_notes.lower() not in note.get('title', '').lower():
                    continue
                
                with st.expander(f"📝 {note.get('title', 'Untitled')} - {note['date']}"):
                    st.markdown(f"**Content:**\n{note['content']}")
                    if note.get('tags'):
                        st.markdown("**Tags:** " + ", ".join([f"`{tag}`" for tag in note['tags']]))
                    
                    col_n1, col_n2, col_n3 = st.columns([1, 1, 4])
                    with col_n1:
                        if st.button("✏️ Edit", key=f"edit_note_{note_display_idx}"):
                            st.session_state.editing_note = note_display_idx
                            st.rerun()
                    with col_n2:
                        if st.button("🗑️ Delete", key=f"del_note_{note_display_idx}"):
                            st.session_state.notes.pop(note_display_idx)
                            save_state()
                            st.rerun()
        else:
            st.info("📝 No notes yet. Create your first research note above!")
    
    with tabs[4]:  # Annotations
        st.markdown("### 🔖 Paper Annotations")
        
        if isinstance(st.session_state.annotations, dict) and len(st.session_state.annotations) > 0:
            for paper_id, annotations in st.session_state.annotations.items():
                with st.expander(f"📄 {paper_id}"):
                    for idx, annotation in enumerate(annotations):
                        st.markdown(f"""
                        <div class="analysis-card">
                            <strong>Page {annotation.get('page', 'N/A')}</strong>
                            <p>{annotation.get('text', 'No text')}</p>
                            <small>Added: {annotation.get('date', 'Unknown')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("🗑️ Remove", key=f"del_ann_{paper_id}_{idx}"):
                            st.session_state.annotations[paper_id].pop(idx)
                            if not st.session_state.annotations[paper_id]:
                                del st.session_state.annotations[paper_id]
                            save_state()
                            st.rerun()
        else:
            st.info("🔖 No annotations yet. Annotate papers from your library!")
    
    with tabs[5]:  # Analytics
        st.markdown("### 📊 Library Analytics")
        
        if len(st.session_state.library) > 0:
            # Overall metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Papers", len(st.session_state.library))
            with col2:
                st.metric("Collections", len(st.session_state.collections))
            with col3:
                st.metric("Notes", len(st.session_state.notes))
            with col4:
                reading_completed = sum(1 for item in st.session_state.reading_list if item.get('status') == 'Read')
                st.metric("Papers Read", f"{reading_completed}/{len(st.session_state.reading_list)}")
            
            # Keywords analysis
            all_keywords = []
            for item in st.session_state.library:
                all_keywords.extend(item.get('keywords', []))
            
            if all_keywords:
                keyword_freq = Counter(all_keywords)
                
                st.markdown("### 🏷️ Top Research Topics")
                top_keywords = keyword_freq.most_common(10)
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=[k[0] for k in top_keywords],
                        y=[k[1] for k in top_keywords],
                        marker_color='#2ecc71'
                    )
                ])
                fig.update_layout(
                    title="Top 10 Keywords in Library",
                    xaxis_title="Keyword",
                    yaxis_title="Frequency",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Papers by type
            paper_types = Counter(item.get('type', 'Other') for item in st.session_state.library)
            if paper_types:
                st.markdown("### 📑 Papers by Type")
                fig_pie = go.Figure(data=[
                    go.Pie(
                        labels=list(paper_types.keys()),
                        values=list(paper_types.values()),
                        marker=dict(colors=['#2ecc71', '#3498db', '#e67e22', '#9b59b6'])
                    )
                ])
                fig_pie.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Reading progress over time
            if st.session_state.library:
                st.markdown("### 📈 Library Growth Over Time")
                dates = [datetime.strptime(item['date'], "%Y-%m-%d") for item in st.session_state.library if 'date' in item]
                if dates:
                    dates.sort()
                    cumulative = list(range(1, len(dates) + 1))
                    
                    fig_growth = go.Figure()
                    fig_growth.add_trace(go.Scatter(
                        x=dates,
                        y=cumulative,
                        mode='lines+markers',
                        name='Papers',
                        line=dict(color='#2ecc71', width=3),
                        fill='tozeroy'
                    ))
                    fig_growth.update_layout(
                        title="Cumulative Papers in Library",
                        xaxis_title="Date",
                        yaxis_title="Total Papers",
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_growth, use_container_width=True)
        else:
            st.info("📊 Add papers to your library to see analytics")

elif st.session_state.current_tool == "🔬 Research Projects":
    st.markdown("## 🔬 Research Project Management")
    st.markdown("Plan, track, and manage your research projects")
    
    # Create new project
    with st.expander("➕ Create New Project", expanded=len(st.session_state.projects) == 0):
        project_name = st.text_input("Project Name")
        project_desc = st.text_area("Description")
        
        col1, col2 = st.columns(2)
        with col1:
            project_field = st.selectbox("Research Field", 
                ["Physics", "Chemistry", "Biology", "Computer Science", "Medicine", "Engineering", "Other"])
            project_start = st.date_input("Start Date")
        with col2:
            project_status = st.selectbox("Status", ["Planning", "Active", "On Hold", "Completed"])
            project_end = st.date_input("Target End Date")
        
        project_team = st.text_input("Team Members (comma-separated)")
        project_funding = st.number_input("Funding ($)", min_value=0, value=0, step=1000)
        
        if st.button("Create Project"):
            if project_name:
                st.session_state.projects.append({
                    "name": project_name,
                    "description": project_desc,
                    "field": project_field,
                    "status": project_status,
                    "start_date": project_start.strftime("%Y-%m-%d"),
                    "end_date": project_end.strftime("%Y-%m-%d"),
                    "team": [m.strip() for m in project_team.split(',')] if project_team else [],
                    "funding": project_funding,
                    "created": datetime.now().strftime("%Y-%m-%d"),
                    "tasks": [],
                    "milestones": [],
                    "papers": [],
                    "notes": []
                })
                save_state()
                st.success(f"Project '{project_name}' created!")
                st.rerun()
    
    # Display existing projects
    if len(st.session_state.projects) > 0:
        st.markdown("---")
        st.markdown("### 📋 Active Projects")
        
        # Filter projects
        filter_status = st.multiselect("Filter by Status", ["Planning", "Active", "On Hold", "Completed"])
        
        for idx, project in enumerate(st.session_state.projects):
            if filter_status and project['status'] not in filter_status:
                continue
            
            status_color = {
                "Planning": "#3498db",
                "Active": "#2ecc71",
                "On Hold": "#e67e22",
                "Completed": "#95a5a6"
            }.get(project['status'], "#95a5a6")
            
            with st.expander(f"🔬 {project['name']} - {project['status']}", expanded=project['status'] == 'Active'):
                # Project header
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{project['name']}</h3>
                    <p><strong>Field:</strong> {project['field']}</p>
                    <p><strong>Description:</strong> {project['description']}</p>
                    <p><strong>Duration:</strong> {project['start_date']} to {project['end_date']}</p>
                    <p><strong>Team:</strong> {', '.join(project['team']) if project['team'] else 'Solo project'}</p>
                    <p><strong>Funding:</strong> ${project['funding']:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Project tabs
                proj_tabs = st.tabs(["📋 Tasks", "🎯 Milestones", "📄 Papers", "💡 Ideas", "📊 Progress"])
                
                with proj_tabs[0]:  # Tasks
                    st.markdown("#### Tasks")
                    
                    # Add task
                    with st.form(key=f"add_task_{idx}"):
                        task_name = st.text_input("Task Name")
                        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                        task_submit = st.form_submit_button("Add Task")
                        
                        if task_submit and task_name:
                            if 'tasks' not in project:
                                project['tasks'] = []
                            project['tasks'].append({
                                "name": task_name,
                                "priority": task_priority,
                                "status": "To Do",
                                "created": datetime.now().strftime("%Y-%m-%d")
                            })
                            save_state()
                            st.rerun()
                    
                    # Display tasks
                    if project.get('tasks'):
                        for task_idx, task in enumerate(project['tasks']):
                            col_t1, col_t2, col_t3, col_t4 = st.columns([3, 1, 1, 1])
                            with col_t1:
                                st.markdown(f"**{task['name']}** - Priority: {task['priority']}")
                            with col_t2:
                                task_status = st.selectbox(
                                    "Status",
                                    ["To Do", "In Progress", "Done"],
                                    key=f"task_status_{idx}_{task_idx}",
                                    index=["To Do", "In Progress", "Done"].index(task.get('status', 'To Do'))
                                )
                                if task_status != task.get('status'):
                                    task['status'] = task_status
                                    save_state()
                            with col_t3:
                                if st.button("✏️", key=f"edit_task_{idx}_{task_idx}"):
                                    st.info("Task editing")
                            with col_t4:
                                if st.button("🗑️", key=f"del_task_{idx}_{task_idx}"):
                                    project['tasks'].pop(task_idx)
                                    save_state()
                                    st.rerun()
                
                with proj_tabs[1]:  # Milestones
                    st.markdown("#### Milestones")
                    
                    with st.form(key=f"add_milestone_{idx}"):
                        milestone_name = st.text_input("Milestone Name")
                        milestone_date = st.date_input("Target Date")
                        milestone_submit = st.form_submit_button("Add Milestone")
                        
                        if milestone_submit and milestone_name:
                            if 'milestones' not in project:
                                project['milestones'] = []
                            project['milestones'].append({
                                "name": milestone_name,
                                "date": milestone_date.strftime("%Y-%m-%d"),
                                "achieved": False
                            })
                            save_state()
                            st.rerun()
                    
                    if project.get('milestones'):
                        for ms_idx, milestone in enumerate(project['milestones']):
                            col_m1, col_m2, col_m3 = st.columns([3, 1, 1])
                            with col_m1:
                                st.markdown(f"**{milestone['name']}** - {milestone['date']}")
                            with col_m2:
                                achieved = st.checkbox("Achieved", value=milestone.get('achieved', False), key=f"ms_check_{idx}_{ms_idx}")
                                if achieved != milestone.get('achieved'):
                                    milestone['achieved'] = achieved
                                    save_state()
                            with col_m3:
                                if st.button("🗑️", key=f"del_ms_{idx}_{ms_idx}"):
                                    project['milestones'].pop(ms_idx)
                                    save_state()
                                    st.rerun()
                
                with proj_tabs[2]:  # Papers
                    st.markdown("#### Related Papers")
                    
                    # Link papers from library
                    if st.session_state.library:
                        paper_to_add = st.selectbox(
                            "Add paper from library",
                            [""] + [p['title'] for p in st.session_state.library],
                            key=f"add_paper_{idx}"
                        )
                        if paper_to_add and st.button("Link Paper", key=f"link_paper_{idx}"):
                            if 'papers' not in project:
                                project['papers'] = []
                            paper_data = next((p for p in st.session_state.library if p['title'] == paper_to_add), None)
                            if paper_data and paper_data not in project['papers']:
                                project['papers'].append(paper_data)
                                save_state()
                                st.success("Paper linked!")
                                st.rerun()
                    
                    if project.get('papers'):
                        for paper in project['papers']:
                            st.markdown(f"- 📄 {paper['title']}")
                
                with proj_tabs[3]:  # Ideas
                    st.markdown("#### Research Ideas & Notes")
                    
                    idea_text = st.text_area("New Idea", key=f"idea_{idx}", height=100)
                    if st.button("💡 Save Idea", key=f"save_idea_{idx}"):
                        if idea_text:
                            if 'notes' not in project:
                                project['notes'] = []
                            project['notes'].append({
                                "content": idea_text,
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            save_state()
                            st.success("Idea saved!")
                            st.rerun()
                    
                    if project.get('notes'):
                        for note_idx, note in enumerate(reversed(project['notes'])):
                            st.markdown(f"""
                            <div class="analysis-card">
                                <p>{note['content']}</p>
                                <small>{note['date']}</small>
                            </div>
                            """, unsafe_allow_html=True)
                
                with proj_tabs[4]:  # Progress
                    st.markdown("#### Project Progress")
                    
                    # Calculate progress
                    total_tasks = len(project.get('tasks', []))
                    completed_tasks = sum(1 for t in project.get('tasks', []) if t.get('status') == 'Done')
                    progress_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                    
                    st.metric("Task Completion", f"{completed_tasks}/{total_tasks} ({progress_pct:.0f}%)")
                    
                    # Progress bar
                    st.progress(progress_pct / 100)
                    
                    # Milestones progress
                    total_milestones = len(project.get('milestones', []))
                    achieved_milestones = sum(1 for m in project.get('milestones', []) if m.get('achieved'))
                    
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        st.metric("Milestones Achieved", f"{achieved_milestones}/{total_milestones}")
                    with col_p2:
                        days_elapsed = (datetime.now() - datetime.strptime(project['start_date'], "%Y-%m-%d")).days
                        st.metric("Days Active", days_elapsed)
                
                # Project actions
                st.markdown("---")
                col_a1, col_a2, col_a3, col_a4 = st.columns(4)
                with col_a1:
                    if st.button("📊 Generate Report", key=f"report_{idx}"):
                        if research_assistant:
                            with st.spinner("Generating project report..."):
                                report_prompt = f"""Generate a comprehensive progress report for this research project:
                                
Project: {project['name']}
Field: {project['field']}
Status: {project['status']}
Duration: {project['start_date']} to {project['end_date']}
Tasks: {total_tasks} total, {completed_tasks} completed
Milestones: {achieved_milestones}/{total_milestones} achieved

Generate a professional report including:
1. Executive Summary
2. Progress Overview
3. Key Achievements
4. Challenges Faced
5. Next Steps
6. Resource Utilization
7. Risk Assessment
8. Recommendations"""
                                
                                try:
                                    report = model.generate_content(report_prompt)
                                    st.markdown("### 📄 Project Report")
                                    st.markdown(report.text)
                                except Exception as e:
                                    st.error(f"Error generating report: {str(e)}")
                
                with col_a2:
                    new_status = st.selectbox("Change Status", ["Planning", "Active", "On Hold", "Completed"], 
                                             index=["Planning", "Active", "On Hold", "Completed"].index(project['status']),
                                             key=f"status_{idx}")
                    if new_status != project['status']:
                        project['status'] = new_status
                        save_state()
                        st.rerun()
                
                with col_a3:
                    if st.button("📋 Export Project", key=f"export_{idx}"):
                        project_json = json.dumps(project, indent=2)
                        st.download_button(
                            "Download JSON",
                            project_json,
                            file_name=f"{project['name']}_export.json",
                            mime="application/json"
                        )
                
                with col_a4:
                    if st.button("🗑️ Delete Project", key=f"del_proj_{idx}"):
                        if st.checkbox("Confirm deletion", key=f"confirm_del_{idx}"):
                            st.session_state.projects.pop(idx)
                            save_state()
                            st.success("Project deleted")
                            st.rerun()
    else:
        st.info("🔬 No projects yet. Create your first research project above!")

elif st.session_state.current_tool == "📈 Analytics":
    st.markdown("## 📈 Research Analytics Dashboard")
    st.markdown("Comprehensive analytics and insights into your research activity")
    
    # Overall metrics
    st.markdown("### 📊 Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Papers", len(st.session_state.library))
    with col2:
        st.metric("Active Projects", sum(1 for p in st.session_state.projects if p.get('status') == 'Active'))
    with col3:
        st.metric("Research Notes", len(st.session_state.notes))
    with col4:
        st.metric("Searches Made", len(st.session_state.search_history))
    with col5:
        total_citations = sum(p.get('citations', 0) for p in st.session_state.library if isinstance(p, dict))
        st.metric("Total Citations", total_citations)
    
    # Analytics tabs
    analytics_tabs = st.tabs(["📊 Activity", "🏷️ Topics", "🔬 Research Impact", "⏱️ Time Analysis", "🎯 Goals"])
    
    with analytics_tabs[0]:  # Activity
        st.markdown("### 📊 Research Activity")
        
        if st.session_state.search_history:
            # Activity over time
            dates = [datetime.strptime(s['timestamp'].split()[0], "%Y-%m-%d") for s in st.session_state.search_history if 'timestamp' in s]
            if dates:
                date_counts = Counter([d.strftime("%Y-%m") for d in dates])
                
                fig_activity = go.Figure()
                fig_activity.add_trace(go.Bar(
                    x=list(date_counts.keys()),
                    y=list(date_counts.values()),
                    marker_color='#2ecc71'
                ))
                fig_activity.update_layout(
                    title="Monthly Search Activity",
                    xaxis_title="Month",
                    yaxis_title="Searches",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_activity, use_container_width=True)
        
        # Recent activity timeline
        st.markdown("#### Recent Activity")
        recent_activities = []
        
        # Combine different activities
        for search in st.session_state.search_history[-5:]:
            recent_activities.append({
                "type": "Search",
                "description": search['query'][:50],
                "time": search['timestamp']
            })
        
        for note in st.session_state.notes[-5:]:
            recent_activities.append({
                "type": "Note",
                "description": note.get('title', 'Untitled')[:50],
                "time": note['date']
            })
        
        # Sort by time
        recent_activities.sort(key=lambda x: x['time'], reverse=True)
        
        for activity in recent_activities[:10]:
            icon = "🔍" if activity['type'] == "Search" else "📝"
            st.markdown(f"""
            <div class="timeline-item">
                {icon} <strong>{activity['type']}</strong>: {activity['description']}
                <br><small>{activity['time']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with analytics_tabs[1]:  # Topics
        st.markdown("### 🏷️ Research Topics Analysis")
        
        # Extract all keywords
        all_keywords = []
        for item in st.session_state.library:
            if isinstance(item, dict):
                all_keywords.extend(item.get('keywords', []))
        
        for chat in st.session_state.chat_history:
            if isinstance(chat, dict):
                all_keywords.extend(chat.get('keywords', []))
        
        if all_keywords:
            keyword_freq = Counter(all_keywords)
            top_20 = keyword_freq.most_common(20)
            
            # Word cloud style visualization
            fig_topics = go.Figure(data=[
                go.Bar(
                    y=[k[0] for k in top_20],
                    x=[k[1] for k in top_20],
                    orientation='h',
                    marker=dict(
                        color=[k[1] for k in top_20],
                        colorscale='Greens'
                    )
                )
            ])
            fig_topics.update_layout(
                title="Top 20 Research Topics",
                xaxis_title="Frequency",
                yaxis_title="Topic",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=600
            )
            st.plotly_chart(fig_topics, use_container_width=True)
            
            # Topic clusters
            st.markdown("#### Topic Clusters")
            st.info("Topics are grouped based on co-occurrence patterns")
            
            # Simple clustering visualization
            col_c1, col_c2, col_c3 = st.columns(3)
            keyword_list = list(keyword_freq.keys())
            
            with col_c1:
                st.markdown("**Cluster 1**")
                for kw in keyword_list[:5]:
                    st.markdown(f"- {kw}")
            with col_c2:
                st.markdown("**Cluster 2**")
                for kw in keyword_list[5:10]:
                    st.markdown(f"- {kw}")
            with col_c3:
                st.markdown("**Cluster 3**")
                for kw in keyword_list[10:15]:
                    st.markdown(f"- {kw}")
        else:
            st.info("No topics analyzed yet. Continue your research to see topic analytics!")
    
    with analytics_tabs[2]:  # Research Impact
        st.markdown("### 🔬 Research Impact Metrics")
        
        if st.session_state.library:
            # Calculate h-index
            citations = [p.get('citations', 0) for p in st.session_state.library if isinstance(p, dict)]
            h_index = ResearchAnalytics.calculate_h_index(citations)
            impact_factor = ResearchAnalytics.calculate_impact_factor(st.session_state.library)
            
            col_i1, col_i2, col_i3 = st.columns(3)
            with col_i1:
                st.markdown(f"""
                <div class="impact-score">
                    <h2>{h_index}</h2>
                    <p>h-index</p>
                </div>
                """, unsafe_allow_html=True)
            with col_i2:
                st.markdown(f"""
                <div class="impact-score">
                    <h2>{impact_factor}</h2>
                    <p>Impact Factor</p>
                </div>
                """, unsafe_allow_html=True)
            with col_i3:
                avg_citations = sum(citations) / len(citations) if citations else 0
                st.markdown(f"""
                <div class="impact-score">
                    <h2>{avg_citations:.1f}</h2>
                    <p>Avg Citations</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Citation distribution
            if citations:
                fig_citations = go.Figure(data=[
                    go.Histogram(
                        x=citations,
                        nbinsx=20,
                        marker_color='#2ecc71'
                    )
                ])
                fig_citations.update_layout(
                    title="Citation Distribution",
                    xaxis_title="Citations",
                    yaxis_title="Number of Papers",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_citations, use_container_width=True)
            
            # Research velocity
            velocity = ResearchAnalytics.calculate_research_velocity(st.session_state.library)
            st.markdown("#### Research Velocity")
            st.markdown(f"""
            - **Papers per month:** {velocity.get('papers_per_month', 0)}
            - **Trend:** {velocity.get('trend', 'stable').title()}
            - **Recent average:** {velocity.get('recent_average', 0)} papers/month
            """)
        else:
            st.info("Build your library to see impact metrics!")
    
    with analytics_tabs[3]:  # Time Analysis
        st.markdown("### ⏱️ Time Analysis")
        
        # Research time patterns
        if st.session_state.search_history:
            hours = []
            for search in st.session_state.search_history:
                if 'timestamp' in search:
                    try:
                        dt = datetime.strptime(search['timestamp'], "%Y-%m-%d %H:%M:%S")
                        hours.append(dt.hour)
                    except:
                        pass
            
            if hours:
                hour_counts = Counter(hours)
                
                fig_time = go.Figure()
                fig_time.add_trace(go.Scatter(
                    x=list(range(24)),
                    y=[hour_counts.get(h, 0) for h in range(24)],
                    mode='lines+markers',
                    fill='tozeroy',
                    line=dict(color='#2ecc71', width=3),
                    marker=dict(size=8)
                ))
                fig_time.update_layout(
                    title="Research Activity by Hour of Day",
                    xaxis_title="Hour",
                    yaxis_title="Activity Count",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_time, use_container_width=True)
                
                # Peak hours
                peak_hour = max(hour_counts, key=hour_counts.get)
                st.info(f"📊 Your peak research hour is {peak_hour}:00")
        
        # Project timelines
        if st.session_state.projects:
            st.markdown("#### Active Project Timelines")
            
            fig_timeline = go.Figure()
            
            for idx, project in enumerate(st.session_state.projects):
                if project.get('status') in ['Active', 'Planning']:
                    start = datetime.strptime(project['start_date'], "%Y-%m-%d")
                    end = datetime.strptime(project['end_date'], "%Y-%m-%d")
                    
                    fig_timeline.add_trace(go.Scatter(
                        x=[start, end],
                        y=[project['name'], project['name']],
                        mode='lines+markers',
                        name=project['name'],
                        line=dict(width=10),
                        marker=dict(size=12)
                    ))
            
            fig_timeline.update_layout(
                title="Project Timelines",
                xaxis_title="Date",
                yaxis_title="Project",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    with analytics_tabs[4]:  # Goals
        st.markdown("### 🎯 Research Goals & Progress")
        
        # Set goals
        with st.expander("➕ Set New Goal"):
            goal_type = st.selectbox("Goal Type", ["Papers to Read", "Notes to Write", "Projects to Complete", "Custom"])
            goal_target = st.number_input("Target", min_value=1, value=10)
            goal_deadline = st.date_input("Deadline")
            
            if st.button("Set Goal"):
                if 'goals' not in st.session_state:
                    st.session_state.goals = []
                st.session_state.goals.append({
                    "type": goal_type,
                    "target": goal_target,
                    "current": 0,
                    "deadline": goal_deadline.strftime("%Y-%m-%d"),
                    "created": datetime.now().strftime("%Y-%m-%d")
                })
                save_state()
                st.success("Goal set!")
                st.rerun()
        
        # Display goals
        if 'goals' in st.session_state and st.session_state.goals:
            for goal_idx, goal in enumerate(st.session_state.goals):
                progress = (goal['current'] / goal['target']) * 100
                days_left = (datetime.strptime(goal['deadline'], "%Y-%m-%d") - datetime.now()).days
                
                st.markdown(f"""
                <div class="analysis-card">
                    <h4>{goal['type']}</h4>
                    <p>Target: {goal['target']} | Current: {goal['current']} | Progress: {progress:.0f}%</p>
                    <p>Deadline: {goal['deadline']} ({days_left} days remaining)</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.progress(progress / 100)
                
                col_g1, col_g2 = st.columns([1, 5])
                with col_g1:
                    if st.button("Update", key=f"update_goal_{goal_idx}"):
                        st.session_state.updating_goal = goal_idx
                with col_g2:
                    if st.button("Delete Goal", key=f"del_goal_{goal_idx}"):
                        st.session_state.goals.pop(goal_idx)
                        save_state()
                        st.rerun()
        else:
            st.info("🎯 Set research goals to track your progress!")

elif st.session_state.current_tool == "🤝 Collaboration":
    st.markdown("## 🤝 Research Collaboration Hub")
    st.markdown("Find collaborators, manage teams, and share insights")
    
    collab_tabs = st.tabs(["👥 Find Collaborators", "🏢 My Teams", "💬 Discussions", "📤 Shared Resources"])
    
    with collab_tabs[0]:  # Find Collaborators
        st.markdown("### 👥 Find Potential Collaborators")
        
        # User's research profile
        with st.expander("🎓 Your Research Profile", expanded=False):
            interests = st.text_area("Research Interests (one per line)", 
                                     value="\n".join(st.session_state.research_profile.get('interests', [])))
            expertise = st.text_area("Expertise Areas (one per line)",
                                    value="\n".join(st.session_state.research_profile.get('expertise_areas', [])))
            
            if st.button("Update Profile"):
                st.session_state.research_profile['interests'] = [i.strip() for i in interests.split('\n') if i.strip()]
                st.session_state.research_profile['expertise_areas'] = [e.strip() for e in expertise.split('\n') if e.strip()]
                save_state()
                st.success("Profile updated!")
        
        # Search for collaborators
        st.markdown("#### Search Researchers")
        search_field = st.text_input("Search by field or expertise")
        
        if st.button("Find Collaborators"):
            # Simulated researcher database
            mock_researchers = [
                {
                    "name": "Dr. Sarah Chen",
                    "institution": "MIT",
                    "interests": ["quantum computing", "machine learning", "algorithms"],
                    "h_index": 45,
                    "papers": 87
                },
                {
                    "name": "Prof. James Rodriguez",
                    "institution": "Stanford University",
                    "interests": ["artificial intelligence", "neural networks", "robotics"],
                    "h_index": 52,
                    "papers": 124
                },
                {
                    "name": "Dr. Emily Watson",
                    "institution": "Oxford University",
                    "interests": ["genomics", "bioinformatics", "computational biology"],
                    "h_index": 38,
                    "papers": 65
                },
                {
                    "name": "Prof. Michael Zhang",
                    "institution": "Tsinghua University",
                    "interests": ["renewable energy", "materials science", "nanotechnology"],
                    "h_index": 41,
                    "papers": 93
                },
                {
                    "name": "Dr. Laura Martinez",
                    "institution": "ETH Zurich",
                    "interests": ["climate modeling", "data science", "environmental physics"],
                    "h_index": 36,
                    "papers": 71
                }
            ]
            
            # Find matches
            user_interests = set(i.lower() for i in st.session_state.research_profile.get('interests', []))
            if user_interests:
                recommender = CollaborationRecommender()
                matches = recommender.find_potential_collaborators(
                    list(user_interests),
                    mock_researchers
                )
                
                if matches:
                    st.markdown("#### 🎯 Recommended Collaborators")
                    for match in matches:
                        st.markdown(f"""
                        <div class="feature-card">
                            <h4>{match['name']} - {match['institution']}</h4>
                            <p><strong>Match Score:</strong> {match['overlap_score']}%</p>
                            <p><strong>Common Interests:</strong> {', '.join(match['common_interests'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_c1, col_c2, col_c3 = st.columns(3)
                        with col_c1:
                            if st.button("📧 Contact", key=f"contact_{match['name']}"):
                                st.info(f"Opening contact form for {match['name']}")
                        with col_c2:
                            if st.button("📄 View Profile", key=f"profile_{match['name']}"):
                                st.info(f"Viewing profile: {match['name']}")
                        with col_c3:
                            if st.button("➕ Add to Network", key=f"add_{match['name']}"):
                                st.session_state.collaborations.append(match)
                                save_state()
                                st.success("Added to your network!")
                else:
                    st.warning("No matches found. Try updating your research interests.")
            else:
                st.warning("Please set your research interests in your profile first.")
    
    with collab_tabs[1]:  # My Teams
        st.markdown("### 🏢 Research Teams")
        
        # Create new team
        with st.expander("➕ Create New Team"):
            team_name = st.text_input("Team Name")
            team_desc = st.text_area("Description")
            team_members = st.text_input("Members (comma-separated emails)")
            
            if st.button("Create Team"):
                if team_name:
                    if 'teams' not in st.session_state:
                        st.session_state.teams = []
                    st.session_state.teams.append({
                        "name": team_name,
                        "description": team_desc,
                        "members": [m.strip() for m in team_members.split(',') if m.strip()],
                        "created": datetime.now().strftime("%Y-%m-%d"),
                        "projects": [],
                        "discussions": []
                    })
                    save_state()
                    st.success(f"Team '{team_name}' created!")
                    st.rerun()
        
        # Display teams
        if 'teams' in st.session_state and st.session_state.teams:
            for team_idx, team in enumerate(st.session_state.teams):
                with st.expander(f"👥 {team['name']} ({len(team['members'])} members)"):
                    st.markdown(f"**Description:** {team['description']}")
                    st.markdown(f"**Members:** {', '.join(team['members'])}")
                    st.markdown(f"**Created:** {team['created']}")
                    
                    # Team actions
                    col_t1, col_t2, col_t3 = st.columns(3)
                    with col_t1:
                        if st.button("📧 Message Team", key=f"msg_team_{team_idx}"):
                            st.info("Opening team chat...")
                    with col_t2:
                        if st.button("➕ Add Member", key=f"add_member_{team_idx}"):
                            st.session_state.adding_member = team_idx
                    with col_t3:
                        if st.button("🔗 Share Project", key=f"share_proj_{team_idx}"):
                            st.info("Select project to share...")
        else:
            st.info("No teams yet. Create your first research team!")
    
    with collab_tabs[2]:  # Discussions
        st.markdown("### 💬 Research Discussions")
        
        # Discussion topics
        topics = [
            {"title": "Latest advances in quantum computing", "replies": 12, "date": "2024-11-08"},
            {"title": "Reproducibility in machine learning research", "replies": 8, "date": "2024-11-07"},
            {"title": "Best practices for data visualization", "replies": 15, "date": "2024-11-06"},
            {"title": "Interdisciplinary collaboration tips", "replies": 6, "date": "2024-11-05"}
        ]
        
        for topic in topics:
            st.markdown(f"""
            <div class="tool-card">
                <h4>💬 {topic['title']}</h4>
                <p>📝 {topic['replies']} replies | 📅 {topic['date']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Join Discussion", key=f"join_{topic['title']}"):
                st.info("Opening discussion thread...")
        
        # Start new discussion
        with st.expander("➕ Start New Discussion"):
            disc_title = st.text_input("Discussion Title")
            disc_content = st.text_area("Your question or topic")
            disc_tags = st.text_input("Tags (comma-separated)")
            
            if st.button("Post Discussion"):
                if disc_title and disc_content:
                    st.success("Discussion posted! (Feature in development)")
    
    with collab_tabs[3]:  # Shared Resources
        st.markdown("### 📤 Shared Research Resources")
        
        # Share from library
        if st.session_state.library:
            st.markdown("#### Share from Your Library")
            paper_to_share = st.selectbox(
                "Select paper to share",
                [""] + [p['title'] for p in st.session_state.library if isinstance(p, dict)]
            )
            
            if paper_to_share:
                share_with = st.multiselect(
                    "Share with",
                    ["Public", "My Teams", "Specific Collaborators"]
                )
                
                if st.button("Share"):
                    st.success(f"Shared '{paper_to_share}' successfully!")
        
        # Shared with me
        st.markdown("#### 📥 Resources Shared With You")
        st.info("No shared resources yet. Connect with collaborators to see their shares!")

elif st.session_state.current_tool == "🧬 Hypothesis Lab":
    st.markdown("## 🧬 Hypothesis Testing Laboratory")
    st.markdown("Develop, test, and refine research hypotheses with AI assistance")
    
    hyp_tabs = st.tabs(["💡 Generate Hypotheses", "🧪 Active Hypotheses", "📊 Test Results", "🎯 Methodology"])
    
    with hyp_tabs[0]:  # Generate
        st.markdown("### 💡 AI-Powered Hypothesis Generation")
        
        research_area = st.text_input("Research Area or Topic")
        context = st.text_area("Background/Context (optional)", height=100)
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            hypothesis_type = st.selectbox(
                "Hypothesis Type",
                ["Causal", "Correlational", "Comparative", "Descriptive", "Exploratory"]
            )
        with col_h2:
            num_hypotheses = st.number_input("Number to Generate", 1, 10, 3)
        
        if st.button("🧠 Generate Hypotheses"):
            if research_area and research_assistant:
                with st.spinner("Generating hypotheses with AI..."):
                    prompt = f"""Generate {num_hypotheses} testable research hypotheses for the following:

Research Area: {research_area}
Hypothesis Type: {hypothesis_type}
Context: {context if context else 'None provided'}

For each hypothesis:
1. State the hypothesis clearly
2. Explain the rationale
3. Identify key variables
4. Suggest measurement methods
5. Note potential confounds

Format each hypothesis clearly with numbering."""
                    
                    try:
                        response = model.generate_content(prompt)
                        st.markdown("### 🎯 Generated Hypotheses")
                        st.markdown(response.text)
                        
                        # Save option
                        if st.button("💾 Save These Hypotheses"):
                            st.session_state.hypotheses.append({
                                "area": research_area,
                                "type": hypothesis_type,
                                "content": response.text,
                                "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "status": "Draft"
                            })
                            save_state()
                            st.success("Hypotheses saved!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error generating hypotheses: {str(e)}")
    
    with hyp_tabs[1]:  # Active
        st.markdown("### 🧪 Your Research Hypotheses")
        
        if st.session_state.hypotheses:
            for hyp_idx, hypothesis in enumerate(st.session_state.hypotheses):
                status_color = {
                    "Draft": "#3498db",
                    "Testing": "#e67e22",
                    "Confirmed": "#2ecc71",
                    "Rejected": "#e74c3c",
                    "Refined": "#9b59b6"
                }.get(hypothesis.get('status', 'Draft'), "#95a5a6")
                
                with st.expander(f"📋 {hypothesis['area']} - {hypothesis.get('status', 'Draft')}"):
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4>{hypothesis['area']}</h4>
                        <p><strong>Type:</strong> {hypothesis['type']}</p>
                        <p><strong>Status:</strong> <span style="color: {status_color};">⬤</span> {hypothesis.get('status', 'Draft')}</p>
                        <p><strong>Generated:</strong> {hypothesis['generated']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("**Hypothesis Details:**")
                    st.markdown(hypothesis['content'][:500] + "...")
                    
                    # Actions
                    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
                    with col_a1:
                        new_status = st.selectbox(
                            "Update Status",
                            ["Draft", "Testing", "Confirmed", "Rejected", "Refined"],
                            key=f"status_hyp_{hyp_idx}",
                            index=["Draft", "Testing", "Confirmed", "Rejected", "Refined"].index(hypothesis.get('status', 'Draft'))
                        )
                        if new_status != hypothesis.get('status'):
                            hypothesis['status'] = new_status
                            save_state()
                            st.rerun()
                    
                    with col_a2:
                        if st.button("🧪 Design Experiment", key=f"exp_{hyp_idx}"):
                            if research_assistant:
                                experiments = research_assistant.suggest_experiments(hypothesis['content'][:200])
                                st.session_state.experiment_suggestion = experiments
                                st.rerun()
                    
                    with col_a3:
                        if st.button("📊 Add Data", key=f"data_{hyp_idx}"):
                            st.session_state.adding_data = hyp_idx
                    
                    with col_a4:
                        if st.button("🗑️ Delete", key=f"del_hyp_{hyp_idx}"):
                            st.session_state.hypotheses.pop(hyp_idx)
                            save_state()
                            st.rerun()
        else:
            st.info("🧪 No hypotheses yet. Generate some using AI assistance!")
    
    with hyp_tabs[2]:  # Results
        st.markdown("### 📊 Experimental Results")
        
        # Add experimental results
        with st.expander("➕ Add New Results"):
            result_hypothesis = st.selectbox(
                "Related Hypothesis",
                [""] + [h['area'] for h in st.session_state.hypotheses]
            )
            result_data = st.text_area("Results Summary")
            result_significance = st.number_input("p-value", 0.0, 1.0, 0.05, 0.001, format="%.3f")
            result_effect_size = st.number_input("Effect Size", 0.0, 10.0, 0.5, 0.1)
            
            if st.button("Save Results"):
                if result_hypothesis and result_data:
                    if 'results' not in st.session_state:
                        st.session_state.results = []
                    st.session_state.results.append({
                        "hypothesis": result_hypothesis,
                        "data": result_data,
                        "p_value": result_significance,
                        "effect_size": result_effect_size,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "significant": result_significance < 0.05
                    })
                    save_state()
                    st.success("Results saved!")
                    st.rerun()
        
        # Display results
        if 'results' in st.session_state and st.session_state.results:
            for result in st.session_state.results:
                significance_badge = "✅ Significant" if result['significant'] else "⚠️ Not Significant"
                badge_color = "#2ecc71" if result['significant'] else "#e67e22"
                
                st.markdown(f"""
                <div class="analysis-card">
                    <h4>{result['hypothesis']}</h4>
                    <p><strong>Date:</strong> {result['date']}</p>
                    <p><strong>p-value:</strong> {result['p_value']}</p>
                    <p><strong>Effect Size:</strong> {result['effect_size']}</p>
                    <p><span style="color: {badge_color}; font-weight: bold;">{significance_badge}</span></p>
                    <p>{result['data']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📊 No experimental results recorded yet")
    
    with hyp_tabs[3]:  # Methodology
        st.markdown("### 🎯 Research Methodology Designer")
        
        method_hypothesis = st.text_area("Enter your hypothesis", height=100)
        
        if st.button("🧠 Generate Methodology"):
            if method_hypothesis and research_assistant:
                with st.spinner("Designing research methodology..."):
                    methodology = research_assistant.generate_methodology(method_hypothesis)
                    
                    st.markdown("### 📋 Recommended Methodology")
                    st.markdown(methodology['methodology'])
                    
                    if st.button("💾 Save Methodology"):
                        st.session_state.notes.append({
                            "title": f"Methodology: {method_hypothesis[:50]}",
                            "content": methodology['methodology'],
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "tags": ["methodology"]
                        })
                        save_state()
                        st.success("Methodology saved to notes!")

elif st.session_state.current_tool == "📝 Literature Review":
    st.markdown("## 📝 AI-Powered Literature Review Generator")
    st.markdown("Create comprehensive literature reviews with intelligent synthesis")
    
    review_tabs = st.tabs(["📋 Generate Review", "🗂️ Organize Papers", "✍️ Write Sections", "📊 Analysis"])
    
    with review_tabs[0]:  # Generate
        st.markdown("### 📋 Literature Review Generator")
        
        review_topic = st.text_input("Review Topic")
        review_scope = st.text_area("Scope and Research Questions", height=100)
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            review_type = st.selectbox(
                "Review Type",
                ["Narrative Review", "Systematic Review", "Meta-Analysis", "Scoping Review", "Critical Review"]
            )
        with col_r2:
            target_length = st.selectbox("Target Length", ["Short (2-3 pages)", "Medium (5-8 pages)", "Long (10+ pages)"])
        
        if st.button("🧠 Generate Review Outline"):
            if review_topic and research_assistant:
                with st.spinner("Generating comprehensive review outline..."):
                    prompt = f"""Create a detailed literature review outline for:

Topic: {review_topic}
Type: {review_type}
Scope: {review_scope}
Length: {target_length}

Include:
1. **Introduction**
   - Background
   - Significance
   - Research questions/objectives
   - Scope and limitations

2. **Methodology**
   - Search strategy
   - Inclusion/exclusion criteria
   - Quality assessment

3. **Main Body Sections** (4-6 thematic sections)
   - For each section: theme, key questions, expected papers

4. **Synthesis and Discussion**
   - Common findings
   - Contradictions
   - Gaps in literature

5. **Conclusion**
   - Summary
   - Implications
   - Future directions

6. **Suggested Timeline** for completion

Be specific and detailed."""
                    
                    try:
                        response = model.generate_content(prompt)
                        st.markdown("### 📄 Generated Review Outline")
                        st.markdown(response.text)
                        
                        # Save and export options
                        col_s1, col_s2, col_s3 = st.columns(3)
                        with col_s1:
                            if st.button("💾 Save Outline"):
                                st.session_state.notes.append({
                                    "title": f"Literature Review: {review_topic}",
                                    "content": response.text,
                                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "tags": ["literature review", "outline"]
                                })
                                save_state()
                                st.success("Outline saved!")
                        
                        with col_s2:
                            if st.button("📥 Export to Word"):
                                st.info("Export functionality (in development)")
                        
                        with col_s3:
                            if st.button("🔄 Generate Different Outline"):
                                st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with review_tabs[1]:  # Organize
        st.markdown("### 🗂️ Organize Papers for Review")
        
        # Paper organization matrix
        st.markdown("#### Thematic Organization")
        
        themes = st.text_area("Enter themes (one per line)", 
                             placeholder="Theme 1: Methodology\nTheme 2: Applications\nTheme 3: Challenges")
        
        if themes:
            theme_list = [t.strip() for t in themes.split('\n') if t.strip()]
            
            st.markdown("#### Assign Papers to Themes")
            for paper in st.session_state.library[:10]:  # Show first 10
                with st.expander(f"📄 {paper.get('title', 'Untitled')}"):
                    assigned_themes = st.multiselect(
                        "Relevant themes",
                        theme_list,
                        key=f"themes_{paper.get('title', '')[:20]}"
                    )
                    
                    key_points = st.text_area(
                        "Key points from this paper",
                        key=f"points_{paper.get('title', '')[:20]}",
                        height=80
                    )
                    
                    if st.button("Save", key=f"save_org_{paper.get('title', '')[:20]}"):
                        # Store organization data
                        if 'paper_organization' not in st.session_state:
                            st.session_state.paper_organization = {}
                        st.session_state.paper_organization[paper.get('title', '')] = {
                            "themes": assigned_themes,
                            "key_points": key_points
                        }
                        save_state()
                        st.success("Saved!")
    
    with review_tabs[2]:  # Write
        st.markdown("### ✍️ AI Writing Assistant")
        
        section_to_write = st.selectbox(
            "Section to Write",
            ["Introduction", "Methodology", "Literature Analysis", "Discussion", "Conclusion"]
        )
        
        section_guidance = st.text_area(
            "Key points to cover",
            placeholder="List main points, findings, or arguments to include..."
        )
        
        writing_style = st.selectbox(
            "Writing Style",
            ["Academic/Formal", "Clear and Accessible", "Technical/Specialized", "Critical/Analytical"]
        )
        
        if st.button("✍️ Generate Section"):
            if section_guidance and research_assistant:
                with st.spinner(f"Writing {section_to_write} section..."):
                    prompt = f"""Write a {section_to_write} section for a literature review with the following:

Style: {writing_style}
Key Points to Cover:
{section_guidance}

Requirements:
- Use appropriate academic tone
- Include transition sentences
- Reference integration (use [Author, Year] format)
- Clear structure with topic sentences
- Critical analysis where appropriate
- Length: approximately 300-500 words

Write the complete section:"""
                    
                    try:
                        response = model.generate_content(prompt)
                        st.markdown(f"### 📝 Generated {section_to_write}")
                        st.markdown(response.text)
                        
                        # Edit and save options
                        edited_text = st.text_area(
                            "Edit the generated text",
                            value=response.text,
                            height=300,
                            key="edit_section"
                        )
                        
                        col_w1, col_w2 = st.columns(2)
                        with col_w1:
                            if st.button("💾 Save Section"):
                                st.session_state.notes.append({
                                    "title": f"{section_to_write} - Literature Review",
                                    "content": edited_text,
                                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "tags": ["literature review", section_to_write.lower()]
                                })
                                save_state()
                                st.success("Section saved!")
                        
                        with col_w2:
                            if st.button("🔄 Regenerate"):
                                st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with review_tabs[3]:  # Analysis
        st.markdown("### 📊 Literature Analysis Dashboard")
        
        if st.session_state.library:
            # Temporal analysis
            st.markdown("#### Publication Timeline")
            paper_dates = [p.get('date', '') for p in st.session_state.library if p.get('date')]
            if paper_dates:
                years = [d.split('-')[0] for d in paper_dates]
                year_counts = Counter(years)
                
                fig_years = go.Figure(data=[
                    go.Bar(x=list(year_counts.keys()), y=list(year_counts.values()), marker_color='#2ecc71')
                ])
                fig_years.update_layout(
                    title="Papers by Publication Year",
                    xaxis_title="Year",
                    yaxis_title="Number of Papers",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_years, use_container_width=True)
            
            # Methodology analysis
            st.markdown("#### Research Methods Distribution")
            methods = ["Experimental", "Survey", "Case Study", "Meta-Analysis", "Theoretical"]
            method_counts = [15, 23, 12, 8, 19]  # Simulated data
            
            fig_methods = go.Figure(data=[
                go.Pie(labels=methods, values=method_counts, marker=dict(colors=['#2ecc71', '#3498db', '#e67e22', '#9b59b6', '#e74c3c']))
            ])
            fig_methods.update_layout(
                title="Research Methodologies",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_methods, use_container_width=True)
            
            # Generate synthesis
            if st.button("🧠 Generate Literature Synthesis"):
                with st.spinner("Analyzing and synthesizing literature..."):
                    # Continuation from line where it was cut off:
# This continues after: synthesis_prompt = f"""Analyze the following research library and provide a synthesis:

                    synthesis_prompt = f"""Analyze the following research library and provide a synthesis:

Number of papers: {len(st.session_state.library)}
Key topics: {', '.join(ResearchAnalytics.extract_keywords(' '.join([str(p.get('title', '')) for p in st.session_state.library if isinstance(p, dict)]))[:10])}

Provide:
1. **Overview**: General patterns and themes
2. **Key Findings**: Major discoveries across papers
3. **Methodological Trends**: Common approaches
4. **Research Gaps**: What's missing
5. **Emerging Directions**: Future opportunities
6. **Contradictions**: Areas of disagreement
7. **Implications**: Practical applications

Be specific and cite examples from the literature."""
                    
                    try:
                        response = model.generate_content(synthesis_prompt)
                        st.markdown("### ðŸŠ Literature Synthesis")
                        st.markdown(response.text)
                        
                        if st.button("ðŸ'¾ Save Synthesis"):
                            st.session_state.notes.append({
                                "title": "Literature Synthesis",
                                "content": response.text,
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "tags": ["synthesis", "analysis"]
                            })
                            save_state()
                            st.success("Synthesis saved!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.info("Add papers to your library to see analysis")

elif st.session_state.current_tool == "ðŸŽ Citation Manager":
    st.markdown("## ðŸŽ Citation & Reference Manager")
    st.markdown("Manage citations, generate bibliographies, and track references")
    
    cite_tabs = st.tabs(["ðŸš References", "âœï¸ Generate Citations", "ðŸŠ Citation Network", "ðŸ¥ Export"])
    
    with cite_tabs[0]:  # References
        st.markdown("### ðŸš Your Reference Library")
        
        # Add new reference
        with st.expander("âž• Add New Reference"):
            ref_type = st.selectbox("Reference Type", 
                ["Journal Article", "Book", "Conference Paper", "Thesis", "Website", "Patent"])
            
            col_ref1, col_ref2 = st.columns(2)
            with col_ref1:
                ref_authors = st.text_input("Authors (comma-separated)")
                ref_title = st.text_input("Title")
                ref_year = st.number_input("Year", 1900, 2025, 2024)
            with col_ref2:
                ref_journal = st.text_input("Journal/Publisher")
                ref_volume = st.text_input("Volume/Issue")
                ref_pages = st.text_input("Pages")
            
            ref_doi = st.text_input("DOI (optional)")
            ref_url = st.text_input("URL (optional)")
            
            if st.button("Add Reference"):
                if ref_authors and ref_title:
                    if 'references' not in st.session_state:
                        st.session_state.references = []
                    
                    st.session_state.references.append({
                        "type": ref_type,
                        "authors": ref_authors,
                        "title": ref_title,
                        "year": ref_year,
                        "journal": ref_journal,
                        "volume": ref_volume,
                        "pages": ref_pages,
                        "doi": ref_doi,
                        "url": ref_url,
                        "added": datetime.now().strftime("%Y-%m-%d")
                    })
                    save_state()
                    st.success("Reference added!")
                    st.rerun()
        
        # Display references
        if 'references' not in st.session_state:
            st.session_state.references = []
        
        if st.session_state.references:
            st.markdown("#### Your References")
            for idx, ref in enumerate(st.session_state.references):
                with st.expander(f"{idx + 1}. {ref['title'][:60]}..."):
                    st.markdown(f"**Authors:** {ref['authors']}")
                    st.markdown(f"**Year:** {ref['year']}")
                    st.markdown(f"**Source:** {ref['journal']}")
                    if ref.get('doi'):
                        st.markdown(f"**DOI:** {ref['doi']}")
                    
                    col_c1, col_c2, col_c3 = st.columns(3)
                    with col_c1:
                        if st.button("ðŸ‹ Copy Citation", key=f"copy_cite_{idx}"):
                            st.info("Citation copied to clipboard!")
                    with col_c2:
                        if st.button("âœï¸ Edit", key=f"edit_ref_{idx}"):
                            st.session_state.editing_ref = idx
                    with col_c3:
                        if st.button("ðŸ—'ï¸ Delete", key=f"del_ref_{idx}"):
                            st.session_state.references.pop(idx)
                            save_state()
                            st.rerun()
        else:
            st.info("No references yet. Add your first reference above!")
    
    with cite_tabs[1]:  # Generate
        st.markdown("### âœï¸ Citation Generator")
        
        citation_style = st.selectbox(
            "Citation Style",
            ["APA 7th", "MLA 9th", "Chicago", "Harvard", "IEEE", "Vancouver", "Nature"]
        )
        
        if st.session_state.references:
            selected_refs = st.multiselect(
                "Select references to cite",
                [f"{r['authors']} ({r['year']}): {r['title'][:40]}" for r in st.session_state.references]
            )
            
            if st.button("Generate Citations"):
                if selected_refs:
                    st.markdown(f"### Citations in {citation_style} format:")
                    
                    for sel in selected_refs:
                        # Find the reference
                        ref_idx = next(i for i, r in enumerate(st.session_state.references) 
                                     if f"{r['authors']} ({r['year']}): {r['title'][:40]}" == sel)
                        ref = st.session_state.references[ref_idx]
                        
                        # Generate citation based on style
                        if citation_style == "APA 7th":
                            citation = f"{ref['authors']} ({ref['year']}). {ref['title']}. *{ref['journal']}*, *{ref['volume']}*, {ref['pages']}."
                        elif citation_style == "MLA 9th":
                            citation = f"{ref['authors']}. \"{ref['title']}.\" *{ref['journal']}*, vol. {ref['volume']}, {ref['year']}, pp. {ref['pages']}."
                        elif citation_style == "Chicago":
                            citation = f"{ref['authors']}. \"{ref['title']}.\" *{ref['journal']}* {ref['volume']} ({ref['year']}): {ref['pages']}."
                        else:
                            citation = f"{ref['authors']} ({ref['year']}). {ref['title']}. {ref['journal']}, {ref['volume']}, {ref['pages']}."
                        
                        if ref.get('doi'):
                            citation += f" https://doi.org/{ref['doi']}"
                        
                        st.code(citation, language="text")
                        
                    # Copy all button
                    if st.button("ðŸ‹ Copy All Citations"):
                        st.success("All citations copied!")
        else:
            st.info("Add references first to generate citations")
        
        # In-text citation generator
        st.markdown("---")
        st.markdown("#### Quick In-Text Citation")
        
        author_cite = st.text_input("Author name")
        year_cite = st.number_input("Year", 1900, 2025, 2024, key="year_cite")
        page_cite = st.text_input("Page number (optional)")
        
        if author_cite and st.button("Generate In-Text"):
            if citation_style == "APA 7th":
                in_text = f"({author_cite}, {year_cite}" + (f", p. {page_cite}" if page_cite else "") + ")"
            elif citation_style == "MLA 9th":
                in_text = f"({author_cite} {page_cite})" if page_cite else f"({author_cite})"
            else:
                in_text = f"({author_cite}, {year_cite})"
            
            st.code(in_text, language="text")
    
    with cite_tabs[2]:  # Network
        st.markdown("### ðŸŠ Citation Network Analysis")
        
        if st.session_state.library and len(st.session_state.library) > 0:
            st.markdown("#### Citation Relationships")
            
            # Build citation network
            network = CitationNetwork()
            for idx, paper in enumerate(st.session_state.library[:20]):
                if isinstance(paper, dict):
                    # Simulated citation data
                    cited_papers = [f"paper_{(idx + i) % 20}" for i in range(1, 4)]
                    network.add_paper(
                        f"paper_{idx}",
                        paper.get('title', 'Untitled')[:50],
                        cited_papers
                    )
            
            # Get central papers
            central_papers = network.get_central_papers(10)
            
            st.markdown("#### Most Cited Papers")
            for rank, (paper_id, title, citations) in enumerate(central_papers, 1):
                st.markdown(f"{rank}. **{title}** - Cited by {citations} papers")
            
            # Clusters
            clusters = network.find_research_clusters()
            st.markdown(f"#### Research Clusters Identified: {len(clusters)}")
            
            for cluster_id, papers in list(clusters.items())[:5]:
                with st.expander(f"Cluster {cluster_id} ({len(papers)} papers)"):
                    for paper_id in papers[:5]:
                        if paper_id in network.nodes:
                            st.markdown(f"- {network.nodes[paper_id]['title']}")
        else:
            st.info("Build your library to see citation network analysis")
    
    with cite_tabs[3]:  # Export
        st.markdown("### ðŸ¥ Export Bibliography")
        
        export_format = st.selectbox(
            "Export Format",
            ["BibTeX", "RIS", "EndNote XML", "CSV", "Plain Text"]
        )
        
        if st.session_state.references:
            if st.button("Generate Export File"):
                # Generate export content
                if export_format == "BibTeX":
                    export_content = ""
                    for idx, ref in enumerate(st.session_state.references):
                        export_content += f"""@article{{ref{idx},
  author = {{{ref['authors']}}},
  title = {{{ref['title']}}},
  journal = {{{ref['journal']}}},
  year = {{{ref['year']}}},
  volume = {{{ref['volume']}}},
  pages = {{{ref['pages']}}}
}}

"""
                elif export_format == "Plain Text":
                    export_content = "\n\n".join([
                        f"{ref['authors']} ({ref['year']}). {ref['title']}. {ref['journal']}, {ref['volume']}, {ref['pages']}."
                        for ref in st.session_state.references
                    ])
                else:
                    export_content = json.dumps(st.session_state.references, indent=2)
                
                st.download_button(
                    label=f"ðŸ¥ Download {export_format}",
                    data=export_content,
                    file_name=f"bibliography.{export_format.lower().replace(' ', '_')}",
                    mime="text/plain"
                )
                
                st.code(export_content[:500] + "...", language="text")
        else:
            st.info("No references to export")

elif st.session_state.current_tool == "ðŸŠ History":
    st.markdown("## ðŸŠ Research History & Timeline")
    st.markdown("Track your research journey and activity over time")
    
    # Time range selector
    col_time1, col_time2 = st.columns(2)
    with col_time1:
        time_range = st.selectbox("Time Range", ["Last 7 Days", "Last 30 Days", "Last 3 Months", "Last Year", "All Time"])
    with col_time2:
        activity_filter = st.multiselect("Activity Type", ["Searches", "Papers Saved", "Notes", "Projects"])
    
    # Activity timeline
    st.markdown("### ðŸ… Activity Timeline")
    
    timeline_activities = []
    
    # Searches
    if not activity_filter or "Searches" in activity_filter:
        for search in st.session_state.search_history[-50:]:
            timeline_activities.append({
                
                "type": "🔍 Search",
                "description": search['query'][:60],
                "timestamp": search['timestamp'],
                "data": search
            })
    
    # Papers
    if not activity_filter or "Papers Saved" in activity_filter:
        for paper in st.session_state.library[-50:]:
            if isinstance(paper, dict) and 'date' in paper:
                timeline_activities.append({ 
                    "type": "📄 Paper",
                    "description": paper.get('title', 'Untitled')[:60],
                    "timestamp": paper['date'] + " 00:00:00",
                    "data": paper
                })
    
    # Notes
    if not activity_filter or "Notes" in activity_filter:
        for note in st.session_state.notes[-50:]:
            timeline_activities.append({
                
                "type": "📝 Note",
                "description": note.get('title', 'Untitled')[:60],
                "timestamp": note['date'],
                "data": note
            })
    
    # Projects
    if not activity_filter or "Projects" in activity_filter:
        for project in st.session_state.projects:
            timeline_activities.append({
                
                "type": "🔬 Project",
                "description": project['name'][:60],
                "timestamp": project['created'] + " 00:00:00",
                "data": project
            })
    
    # Sort by timestamp
    timeline_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Display timeline
    for activity in timeline_activities[:50]:
        st.markdown(f"""
        <div class="timeline-item">
            <strong>{activity['type']}</strong>: {activity['description']}
            <br><small>ðŸ•' {activity['timestamp']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistics
    st.markdown("---")
    st.markdown("### ðŸŠ Activity Statistics")
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Total Searches", len(st.session_state.search_history))
    with col_s2:
        st.metric("Papers Saved", len(st.session_state.library))
    with col_s3:
        st.metric("Notes Created", len(st.session_state.notes))
    with col_s4:
        st.metric("Projects Started", len(st.session_state.projects))

else:
    # Default view for other tools
    st.markdown(f"## {st.session_state.current_tool}")
    st.info(f"The {st.session_state.current_tool} feature is under development. More functionality coming soon!")
    
    # Show some generic content based on tool
    if "Explore" in st.session_state.current_tool: # 🌐
        st.markdown("### 🌐 Explore Scientific Discoveries")
        st.markdown("- Browse trending papers")
        st.markdown("- Discover research topics")
        st.markdown("- Follow research areas")
    
    elif "Subscription" in st.session_state.current_tool: # 📋
        st.markdown("### 📋 Manage Your Subscriptions")
        st.markdown("- Subscribe to journals")
        st.markdown("- Get alerts for new papers")
        st.markdown("- Follow researchers")
    
    elif "Scholars" in st.session_state.current_tool: # 👨‍🎓
        st.markdown("### 👨‍🎓 Scholar Profiles")
        st.markdown("- View researcher profiles")
        st.markdown("- Track publications")
        st.markdown("- Analyze research impact")
    
    elif "Knowledge Base" in st.session_state.current_tool: # 📖
        st.markdown("### 📖 Scientific Knowledge Base")
        st.markdown("- Access curated knowledge")
        st.markdown("- Learn scientific concepts")
        st.markdown("- Explore methodologies")
    
    elif "Practice" in st.session_state.current_tool: # 🎯
        st.markdown("### 🎯 Research Practice Tools")
        st.markdown("- Practice problem solving")
        st.markdown("- Test your knowledge")
        st.markdown("- Improve research skills")
    
    elif "Uni-Lab" in st.session_state.current_tool: # 🛠️
        st.markdown("### 🛠️ Universal Laboratory")
        st.markdown("- Virtual experiments")
        st.markdown("- Simulation tools")
        st.markdown("- Lab protocols")
    
    elif "Computation" in st.session_state.current_tool: # 💾
        st.markdown("### 💾 Computational Tools")
        st.markdown("- Data analysis")
        st.markdown("- Statistical computing")
        st.markdown("- Machine learning models")

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    if st.button("ðŸ'¾ Save Progress", use_container_width=True):
        save_state()
with col_f2:
    if st.button("ðŸ„ Reset Session", use_container_width=True):
        if st.checkbox("Confirm reset"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
with col_f3:
    if st.button("ðŸ§ Settings", use_container_width=True):
        st.info("Settings panel coming soon")

st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(180, 200, 190, 0.7);">
    <p>Bohrium - The Universal Instrument for Scientific Discovery</p>
    <p>Powered by Gemini AI | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
