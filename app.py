# ============================================
# CHAT WITH PDF - AI Powered App
# ============================================

import streamlit as st
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
import os

# API Key load karo
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Model setup karo
model = genai.GenerativeModel('gemini-1.5-flash')

# ---- PDF Se Text Nikalne Ka Function ----
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# ---- AI Se Jawab Lene Ka Function ----
def get_answer(pdf_text, question):
    prompt = f"""
    Neeche ek PDF ka content diya gaya hai.
    Is content ke basis par question ka jawab do.
    Agar jawab PDF mein nahi hai toh likho: 
    "Ye information PDF mein nahi hai."
    
    PDF Content:
    {pdf_text}
    
    Question: {question}
    
    Jawab Hindi ya English mein do:
    """
    response = model.generate_content(prompt)
    return response.text

# ============================================
# WEB APP DESIGN
# ============================================

# Page Setup
st.set_page_config(
    page_title="Chat With PDF",
    page_icon="📄",
    layout="centered"
)

# Custom Style
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .answer-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📄 Chat With PDF")
st.markdown("### Apna PDF upload karo aur koi bhi sawaal pucho!")
st.markdown("---")

# Chat history initialize karo
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# PDF Upload Section
st.markdown("### 📁 Step 1: PDF Upload Karo")
uploaded_file = st.file_uploader(
    "Apni PDF file yahan drop karo",
    type=['pdf'],
    help="Sirf PDF files supported hain"
)

if uploaded_file is not None:
    with st.spinner("📖 PDF padh raha hai..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.session_state.pdf_text = pdf_text

    st.success(f"✅ PDF successfully load ho gayi!")
    st.info(f"📊 Total characters: {len(pdf_text):,}")

    # PDF preview
    with st.expander("👁️ PDF Content Preview"):
        st.text(pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text)

    st.markdown("---")

    # Chat Section
    st.markdown("### 💬 Step 2: Sawaal Pucho")

    # Purane messages dikhao
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**🧑 Aapka Sawaal:** {message['content']}")
        else:
            st.markdown(f"""
            <div class='answer-box'>
            🤖 <b>AI Ka Jawab:</b><br>{message['content']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("")

    # Question Input
    question = st.text_input(
        "❓ Apna sawaal yahan likho:",
        placeholder="Example: Is PDF ka main topic kya hai?"
    )

    col1, col2 = st.columns([1, 4])

    with col1:
        ask_button = st.button("🔍 Pucho", use_container_width=True)

    with col2:
        if st.button("🗑️ Chat Clear Karo", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Answer Generate Karo
    if ask_button and question:
        if st.session_state.pdf_text == "":
            st.warning("⚠️ Pehle PDF upload karo!")
        else:
            with st.spinner("🤖 AI soch raha hai..."):
                answer = get_answer(st.session_state.pdf_text, question)

            # Messages save karo
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
            st.rerun()

    elif ask_button and not question:
        st.warning("⚠️ Pehle koi sawaal likho!")

else:
    # PDF upload nahi hui
    st.info("👆 Upar se apni PDF upload karo")

    # Example questions
    st.markdown("---")
    st.markdown("### 💡 Aap Aisa Sawaal Pooch Sakte Ho:")
    col1, col2 = st.columns(2)
    with col1:
        st.code("Is PDF ka summary kya hai?")
        st.code("Main points kya hain?")
        st.code("Chapter 1 ke baare mein batao")
    with col2:
        st.code("Writer ka naam kya hai?")
        st.code("Conclusion kya hai?")
        st.code("Important dates kaunsi hain?")

# Footer
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ using Python, Streamlit & Google Gemini AI</center>",
    unsafe_allow_html=True
)