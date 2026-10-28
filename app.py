import streamlit as st
import streamlit.components.v1 as components
import json
import os
from pipeline import run_pipeline

st.set_page_config(page_title="Nexus Multi-Agent Pipeline", page_icon="🚀", layout="wide")

# ==========================================
# PREMIUM FUTURISTIC UI / CSS INJECTION
# ==========================================
def inject_premium_ui():
    st.markdown("""
    <style>
    /* Hide default Streamlit header and main menu */
    header[data-testid="stHeader"] { display: none !important; }
    
    /* Make the main app background transparent to show the video */
    .stApp {
        background: transparent !important;
    }
    
    /* Glowing Glassmorphism Sticky Header */
    .glass-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 65px;
        background: rgba(5, 5, 16, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 2px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        z-index: 999999;
        display: flex;
        align-items: center;
        padding: 0 2.5rem;
    }
    
    .glass-header h2 {
        margin: 0;
        font-size: 1.5rem;
        font-family: 'Courier New', Courier, monospace;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00FFFF 0%, #FF00FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulseText 3s infinite alternate;
    }
    
    @keyframes pulseText {
        0% { text-shadow: 0 0 10px rgba(0, 255, 255, 0.5); }
        100% { text-shadow: 0 0 20px rgba(255, 0, 255, 0.8); }
    }

    /* Push container down */
    .block-container { padding-top: 6rem !important; }

    /* Futuristic Chat Messages */
    .stChatMessage {
        border-radius: 8px !important;
        border-left: 4px solid #00FFFF !important;
        background: rgba(10, 15, 30, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        padding: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 0 15px rgba(0, 201, 255, 0.1) !important;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.3), inset 0 0 10px rgba(255, 0, 255, 0.1) !important;
        border-color: #FF00FF !important;
        transform: scale(1.01);
    }
    
    /* Glowing Primary Button */
    .stButton>button {
        background: rgba(0,0,0,0.5) !important;
        backdrop-filter: blur(5px) !important;
        border: 2px solid #00FFFF !important;
        color: #00FFFF !important;
        font-weight: bold;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-radius: 4px !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2), inset 0 0 10px rgba(0, 255, 255, 0.1) !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        background: #00FFFF !important;
        color: #000 !important;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.8) !important;
    }
    
    /* System Status Badges */
    .status-badge {
        display: flex;
        align-items: center;
        padding: 10px;
        margin-bottom: 10px;
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(0,255,0,0.3);
        border-radius: 5px;
        color: #00FF00;
        font-family: monospace;
    }
    .status-badge.rag {
        border-color: rgba(255,0,255,0.5);
        color: #FF00FF;
    }
    .status-badge i {
        margin-right: 10px;
        animation: blink 1s infinite;
    }
    @keyframes blink { 0% { opacity: 0; } 50% { opacity: 1; } 100% { opacity: 0; } }
    
    /* Custom Sidebar styling for transparency */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 15, 0.6) !important;
        backdrop-filter: blur(15px) !important;
    }
    </style>
    
    <div class="glass-header">
        <h2> NEXUS Multi-Agent System </h2>
    </div>
    """, unsafe_allow_html=True)

def render_3d_cards():
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body { 
        margin: 0; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        display: flex; 
        justify-content: space-between; 
        background: transparent; 
        padding: 10px 0;
        overflow: hidden;
    }
    .card {
        background: rgba(5, 10, 20, 0.5);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 8px;
        width: 31%;
        padding: 24px;
        color: #E2E8F0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        transform-style: preserve-3d;
        transform: perspective(1000px);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #00FFFF, transparent);
    }
    .card:hover {
        border-color: rgba(255, 0, 255, 0.8);
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.3);
    }
    .card-content {
        transform: translateZ(40px); /* The 3D pop effect */
    }
    h3 { 
        margin-top: 0; 
        margin-bottom: 10px;
        font-size: 1.2rem;
        font-family: monospace;
        color: #00FFFF;
    }
    p { 
        margin: 0;
        font-size: 0.9rem; 
        line-height: 1.5;
        color: #94A3B8;
    }
    </style>
    </head>
    <body>
        <div class="card" data-tilt data-tilt-max="15" data-tilt-speed="400" data-tilt-glare data-tilt-max-glare="0.5">
            <div class="card-content">
                <h3>[01]_NODE_PLANNER</h3>
                <p>Ingests constraints and constructs a robust execution strategy tailored to the domain.</p>
            </div>
        </div>
        <div class="card" data-tilt data-tilt-max="15" data-tilt-speed="400" data-tilt-glare data-tilt-max-glare="0.5">
            <div class="card-content">
                <h3>[02]_NODE_CREATOR</h3>
                <p>Generates high-fidelity assets strictly following the architectural blueprints.</p>
            </div>
        </div>
        <div class="card" data-tilt data-tilt-max="15" data-tilt-speed="400" data-tilt-glare data-tilt-max-glare="0.5">
            <div class="card-content">
                <h3>[03]_NODE_REVIEWER</h3>
                <p>Audits output, ensures compliance with domain standards, and finalizes deliverables.</p>
            </div>
        </div>
        
        <!-- vanilla-tilt.js for 3D interactions -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.0/vanilla-tilt.min.js"></script>
    </body>
    </html>
    """, height=190)

# ==========================================
# APP LOGIC
# ==========================================

import base64

def inject_background_video(video_path):
    """Sets a local video file as a full-screen background video behind the UI."""
    if os.path.exists(video_path):
        with open(video_path, 'rb') as f:
            video_bytes = f.read()
        
        video_b64 = base64.b64encode(video_bytes).decode()
        
        video_html = f'''
            <style>
            #bg-video {{
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100vw;
                min-height: 100vh;
                width: auto;
                height: auto;
                z-index: -100;
                object-fit: cover;
                filter: brightness(0.4) blur(1px); /* Darken slightly so UI text is readable */
            }}
            </style>
            <video id="bg-video" autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        '''
        st.markdown(video_html, unsafe_allow_html=True)

# Render the Background Video if it exists
inject_background_video(os.path.join(os.path.dirname(__file__), 'intro.mp4'))

inject_premium_ui()

def load_domains():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return list(config['domains'].keys())

try:
    domains = load_domains()
except Exception as e:
    st.error(f"Failed to load configuration: {e}")
    st.stop()
    
# Render the 3D Interactive Feature Cards
st.markdown("### `// SYSTEM_ARCHITECTURE_TOPOLOGY`")
render_3d_cards()

# UI Inputs
st.sidebar.markdown("### `// CONFIGURATION_MATRIX`")
selected_domain = st.sidebar.selectbox("Target Domain Node", domains)

st.sidebar.markdown("### `// AGENT_PARAMETERS`")
agent_temperature = st.sidebar.slider(
    "Neural Creativity (Temperature)", 
    min_value=0.0, 
    max_value=1.5, 
    value=0.7, 
    step=0.1,
    help="Higher values make output more creative and random. Lower values make it more focused and deterministic."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### `// SYSTEM_DIAGNOSTICS`")
st.sidebar.markdown('<div class="status-badge"><i>█</i> VRAM_OPTIMIZER: SECURE</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="status-badge"><i>█</i> LOCAL_LLM_LINK: ACTIVE</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="status-badge rag"><i>█</i> RAG_KNOWLEDGE_BASE: MOUNTED</div>', unsafe_allow_html=True)

st.markdown(f"### `// INITIALIZATION_SEQUENCE: {selected_domain}`")
user_prompt = st.text_area("Inject Task Parameters:", height=120, placeholder="e.g., Architect a microservice for processing payment webhooks in Python...")

if st.button("EXECUTE WORKFLOW", type="primary"):
    if not user_prompt.strip():
        st.warning("⚠️ Awaiting valid prompt parameters.")
    else:
        st.markdown("### 📡 Telemetry & Execution Stream")
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        st.markdown("---")
        st.subheader("🗣️ Multi-Agent Synth-Stream")
        
        # Container to hold the real-time chat messages
        chat_container = st.container()
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(f"**Root User:**\n{user_prompt}")
                
        def update_status(msg):
            status_text.info(f"⚡ {msg}")
            if "Scanning" in msg:
                progress_bar.progress(10)
            elif "Agent 1" in msg:
                progress_bar.progress(33)
            elif "Agent 2" in msg:
                progress_bar.progress(66)
            elif "Agent 3" in msg:
                progress_bar.progress(90)
            elif "complete" in msg:
                progress_bar.progress(100)
                status_text.success("✅ " + msg)

        # Real-time UI rendering callback
        def render_agent_output(agent_num, text):
            with chat_container:
                if agent_num == 1:
                    with st.chat_message("assistant", avatar="🧠"):
                        st.markdown("**Node 01 [Planner]:** Architectural blueprint generated based on constraints and local knowledge.")
                        st.info(text)
                elif agent_num == 2:
                    with st.chat_message("assistant", avatar="✍️"):
                        st.markdown("**Node 02 [Creator]:** Execution phase complete. Initial artifact generated.")
                        st.success(text)
                elif agent_num == 3:
                    with st.chat_message("assistant", avatar="🧐"):
                        st.markdown("**Node 03 [Reviewer]:** Quality assurance audit passed. Refactoring complete.")
                        st.warning(text)

        with st.spinner("Compiling context... Check terminal for real-time logs!"):
            results = run_pipeline(
                selected_domain, 
                user_prompt, 
                temperature=agent_temperature, 
                status_callback=update_status, 
                output_callback=render_agent_output
            )
            
        if "error" in results or "Error:" in results.get("plan", ""):
            error_msg = results.get("error", results.get("plan", "Unknown Error"))
            st.error(error_msg)
        else:
            # Display the retrieved RAG context if any was found
            if results.get('rag_context'):
                with st.sidebar.expander("📚 RAG Knowledge Intercepted", expanded=True):
                    st.markdown("*The pipeline automatically retrieved this local context and injected it into Node 01:*")
                    st.code(results['rag_context'], language="markdown")
            
            st.markdown("---")
            st.subheader("💎 Final Deliverable Artifact")
            st.write(results.get("final", "No final output generated."))
