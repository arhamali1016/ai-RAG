import streamlit as st
from streamlit_mic_recorder import mic_recorder
from medical_swarm import run_smart_ai, get_file_content, encode_image

# 1. ZAROORI: Ye hamesha sab se upar hona chahiye warna error aayega
st.set_page_config(
    page_title="Smart Vision Agent | AI Expert", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. EXPERT LEVEL UI/UX (Custom CSS)
def local_css():
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .stAppDeployButton {display:none;}
                [data-testid="stStatusWidget"] {display:none;}
                
                /* Chat Container ki styling */
                .stChatMessage {
                    border-radius: 15px;
                    padding: 20px;
                    margin: 10px 0px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                
                /* Urdu aur English Readability */
                .stMarkdown p {
                    font-size: 20px !important;
                    line-height: 1.7 !important;
                    font-family: 'Jameel Noori Nastaleeq', 'Noto Sans Arabic', 'Segoe UI', sans-serif;
                }
                
                /* Responsive Sidebar */
                [data-testid="stSidebar"] {
                    background-color: #f8f9fa;
                }
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

local_css()

# 3. SESSION STATE MANAGEMENT (Expert Level)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""
if "img_base64" not in st.session_state:
    st.session_state.img_base64 = None

# 4. SIDEBAR - DATA CENTER
with st.sidebar:
    st.title("📁 AI Control Center")
    st.info("Upload documents or images for deep analysis.")
    uploaded_file = st.file_uploader("Drop PDF, CSV, or Images", type=["pdf", "csv", "png", "jpg", "jpeg", "gif"])
    
    if uploaded_file:
        with st.status("Processing data...", expanded=False):
            if uploaded_file.type in ["image/png", "image/jpeg", "image/gif"]:
                st.session_state.img_base64 = encode_image(uploaded_file)
                st.image(uploaded_file, caption="Vision Analysis Ready")
            else:
                st.session_state.context = get_file_content(uploaded_file)
                st.success("Context Loaded Successfully")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 5. MAIN CHAT INTERFACE
st.title("🎙️ SmartScan AI Expert")
st.caption("Advanced Vision & Document Intelligence Agent")

# History Display
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 6. INPUT SECTION (Responsive Layout)
st.divider()
input_col, mic_col = st.columns([8, 1])

with mic_col:
    # Mic widget
    mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='voice_input')

if prompt := st.chat_input("Explain this document or ask anything..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                res = run_smart_ai(prompt, st.session_state.context, st.session_state.img_base64)
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Analysis Error: {str(e)}")
