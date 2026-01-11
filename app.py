import streamlit as st
from streamlit_mic_recorder import mic_recorder
from medical_swarm import run_smart_ai, get_file_content, encode_image

# Ye code footer aur menu ko gayab kar dega
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title="Smart Vision Agent", layout="wide")

# --- URDU READABILITY CSS ---
st.markdown("""
    <style>
    /* Chat bubbles ko bada aur clear banane ke liye */
    .stMarkdown p {
        font-size: 22px !important; /* Font size bada kar diya */
        line-height: 1.8 !important; /* Lines ke darmiyan gap */
        font-family: 'Jameel Noori Nastaleeq', 'Noto Sans Arabic', sans-serif;
        direction: auto; /* Urdu ko right-to-left auto karega */
    }
    /* User aur Assistant ki messages ki background styling */
    [data-testid="stChatMessage"] {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ SmartScan AI ")

# Sidebar: PDF, CSV, Image, GIF Support
st.sidebar.header("📁 Data & Image Center")
uploaded_file = st.sidebar.file_uploader("Upload PDF, CSV, Image or GIF", type=["pdf", "csv", "png", "jpg", "jpeg", "gif"])

if "context" not in st.session_state: st.session_state.context = ""
if "img_base64" not in st.session_state: st.session_state.img_base64 = None

if uploaded_file:
    with st.sidebar:
        if uploaded_file.type in ["image/png", "image/jpeg", "image/gif"]:
            st.session_state.img_base64 = encode_image(uploaded_file)
            st.image(uploaded_file, caption="Image Ready!")
        else:
            st.session_state.context = get_file_content(uploaded_file)
            st.success("Document Data Loaded!")

# Chat History
if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# Input Section
st.write("---")
col1, col2 = st.columns([1, 6])
with col1:
    mic_recorder(start_prompt="🎤 Voice", stop_prompt="🛑 Stop", key='voice')

if prompt := st.chat_input("Ask about anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing smartly..."):
            res = run_smart_ai(prompt, st.session_state.context, st.session_state.img_base64)
            st.markdown(res)

            st.session_state.messages.append({"role": "assistant", "content": res})


