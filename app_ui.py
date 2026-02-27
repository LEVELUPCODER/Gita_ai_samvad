
import streamlit as st
import base64
import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Gita-Ai samvad", page_icon="🪷", layout="wide")

# --- 2. BRAIN INITIALIZATION ---
@st.cache_resource
def load_brain():
    # RAG pipeline using ChromaDB
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory="gita_db", embedding_function=embeddings)

vector_db = load_brain()

# Initialize Session States
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 3. LOAD LOCAL IMAGES ---
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

local_img = get_base64('krishna_bg.jpg')
bg_css = f"url(data:image/png;base64,{local_img})" if local_img else ""
feather_base64 = get_base64('download.png')
feather_data = f"data:image/png;base64,{feather_base64}" if feather_base64 else ""

# --- 4. ADVANCED CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), {bg_css} !important;
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
    }}
    @keyframes divineDrift {{
        0% {{ transform: translate(85vw, 85vh) rotate(0deg) scale(0.1); opacity: 0; }}
        10% {{ opacity: 1; }}
        50% {{ transform: translate(30vw, 15vh) rotate(30deg) scale(1.8); filter: drop-shadow(0 0 25px rgba(186, 85, 211, 0.8)); }}
        100% {{ transform: translate(-20vw, -20vh) rotate(60deg) scale(1); opacity: 0; }}
    }}
    .feather-anim {{
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 280px; 
        z-index: 99999 !important; /* Critical fix for visibility */
        pointer-events: none; 
        animation: divineDrift 6.5s ease-in-out forwards;
    }}
    .stChatMessage div, .stMarkdown p {{ font-size: 22px !important; line-height: 1.6 !important; }}
    .stChatInput textarea {{ font-size: 24px !important; }}
    @keyframes radheGlow {{
        0% {{ color: #FFD700; text-shadow: 0 0 10px #FF69B4; transform: scale(1); }}
        50% {{ color: #FF69B4; text-shadow: 0 0 30px #FFD700; transform: scale(1.1); }}
        100% {{ color: #FFD700; text-shadow: 0 0 10px #FF69B4; transform: scale(1); }}
    }}
    .radhe-loader {{ font-size: 55px; font-weight: bold; display: inline-block; animation: radheGlow 2s infinite ease-in-out; }}
    .stChatMessage {{ background: rgba(255, 255, 255, 0.07) !important; backdrop-filter: blur(15px); border-radius: 15px !important; }}
    [data-testid="stSidebar"] {{ background-color: rgba(15, 15, 15, 0.95) !important; }}
    .dev-footer {{ text-align: center; font-size: 20px; color: rgba(255, 255, 255, 0.9); margin-top: 50px; padding: 20px; font-style: italic; }}
    
    /* Scale UI to 75% and center */
    .main .block-container,
    [data-testid="stMainBlockContainer"] {{
        max-width: 100% !important;
        margin: 0 !important;
        margin-left: 0 !important;
        padding-left: 2rem !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}
    .stChatMessage div, .stMarkdown p {{ font-size: 16px !important; line-height: 1.5 !important; }}
    .stChatInput textarea {{ font-size: 18px !important; }}
    .radhe-loader {{ font-size: 42px; }}
    .feather-anim {{ width: 210px; }}
    .dev-footer {{ font-size: 15px; margin-top: 30px; padding: 15px; }}
    h1 {{ font-size: 2rem !important; }}
    h4 {{ font-size: 1rem !important; }}
    [data-testid="stSidebar"] {{
        width: 180px !important;
        min-width: 180px !important;
    }}
    [data-testid="stSidebar"] > div {{
        width: 180px !important;
    }}
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {{ font-size: 13px !important; }}
    [data-testid="stSidebar"] h1 {{ font-size: 1.2rem !important; }}
    
    /* Make sidebar fixed (always visible, no collapse) */
    [data-testid="stSidebar"][aria-expanded="false"] {{
        display: block !important;
        visibility: visible !important;
        transform: none !important;
        margin-left: 0 !important;
    }}
    [data-testid="stSidebarCollapsedControl"] {{
        display: none !important;
    }}
    
    /* Hide Fork, GitHub, Settings */
    .stDeployButton,
    #MainMenu,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stHeader"] {{
        visibility: hidden !important;
        display: none !important;
        height: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)





# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("📜 DASHBOARD")
    with st.expander("⭐ Saved Guidance", expanded=True):
        if st.session_state.favorites:
            for idx, fav in enumerate(st.session_state.favorites):
                c1, c2, c3 = st.columns([0.6, 0.2, 0.2])
                c1.caption(f"{fav[:30]}...")
                if c2.button("👁️", key=f"v_{idx}"):
                    st.session_state.chat_history.append({"role": "assistant", "content": f"✨ **Reflected Wisdom:**\n\n{fav}"})
                    st.rerun()
                if c3.button("🗑️", key=f"d_{idx}"):
                    st.session_state.favorites.pop(idx)
                    st.rerun()
    st.markdown("---")
    reply_format = st.radio("Response Depth:", ["Short & Direct", "Detailed Explanation"])
    if st.button("➕ New Samvad"):
        st.session_state.chat_history = []
        st.rerun()

# --- 6. MAIN INTERFACE ---
st.title("🪷 Gita-Ai samvad")
st.markdown("#### *Strategic Wisdom and Guidance for Parth from the Bhagavad Gita*")

for i, msg in enumerate(st.session_state.chat_history):
    with st.chat_message(msg["role"], avatar="🪷" if msg["role"]=="assistant" else "👤"):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "Reflected Wisdom" not in msg["content"]:
            if st.button("⭐ Save", key=f"f_{i}"):
                if msg["content"] not in st.session_state.favorites:
                    st.session_state.favorites.append(msg["content"])
                    st.toast("Saved!")

# --- 7. INPUT & LOGIC ---
if prompt := st.chat_input("Ask Your Life Related Doubts...(here, Parth!)"):
    if feather_data: 
        st.markdown(f'<img src="{feather_data}" class="feather-anim">', unsafe_allow_html=True)
    
    with st.chat_message("user", avatar="👤"): 
        st.markdown(prompt)

    docs = vector_db.similarity_search(prompt, k=2)
    context = "\n".join([d.page_content for d in docs])
    depth = "Short and direct guidance." if reply_format == "Short & Direct" else "A detailed philosophical Samvad."
    
    with st.chat_message("assistant", avatar="🪷"):
        loader = st.empty()
        loader.markdown('<div class="radhe-loader">राधे राधे</div>', unsafe_allow_html=True)
        
        try:
            # SECURE: Using st.secrets for key management
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Using the production model confirmed by your ListModels check
            model = genai.GenerativeModel('gemini-2.5-flash') 
            
            full_prompt = f"You are Lord Krishna. {depth} Context: {context}. Always address the user as 'Parth' in your reply. Parth asks: {prompt}"
            
            response = model.generate_content(full_prompt)
            loader.empty()
            answer = response.text
            st.markdown(answer)
            
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
            
        except Exception as e:
            loader.empty()
            st.error(f"Divine Error: {str(e)}")

# --- 8. FOOTER ---
st.markdown('<div class="dev-footer">Developed by <b>Amit Chanchal</b> | NIT Jamshedpur</div>', unsafe_allow_html=True)