import streamlit as st
from streamlit_mic_recorder import mic_recorder
from medical_swarm import run_smart_ai, get_file_content, encode_image

# 1. Page Config (Must be first)
st.set_page_config(page_title="SmartScan AI", layout="wide")

# 2. Advanced Responsive CSS
def apply_expert_ui():
    style = """
    <style>
        /* 1. Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stAppDeployButton {display:none;}

        /* 2. Fix Sidebar Toggle (Desktop view mein wapis na aane wala bug) */
        section[data-testid="stSidebar"] {
            transition: all 0.3s ease-in-out;
        }
        
        /* 3. Mobile Responsive Search Bar (Fix for disappearing input) */
        @media (max-width: 768px) {
            .stChatInput {
                position: fixed;
                bottom: 20px;
                left: 0;
                right: 0;
                z-index: 9999;
                padding: 10px;
                background: white;
            }
            .main .block-container {
                padding-bottom: 100px; /* Space for fixed input */
            }
        }

        /* 4. Expert Chat Bubble Styling */
        [data-testid="stChatMessage"] {
            border-radius: 20px;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            max-width: 85%;
        }
        
        /* 5. Urdu Text Alignment & Font */
        .stMarkdown p {
            font-size: 1.2rem !important;
            line-height: 1.6;
            direction: auto;
            text-align: left;
        }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

apply_expert_ui()

# --- Rest of your logic (Session State, Sidebar, Chat) ---
# ... (Wahi code jo pehle tha)
