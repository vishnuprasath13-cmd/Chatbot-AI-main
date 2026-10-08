import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
<style>
    :root {
        --primary-color: #4F46E5;
        --secondary-color: #06B6D4;
        --success-color: #10B981;
        --danger-color: #EF4444;
        --dark-bg: #0F172A;
        --light-bg: #F8FAFC;
        --border-color: #E2E8F0;
    }

    * { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }

    .main {
        padding: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    h1 {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    h2 {
        color: #1E293B;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        color: #1E293B !important;
    }

    .stTextInput > div > div > input::placeholder { color: #94A3B8 !important; }

    .stTextInput > div > div > input:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        color: #1E293B !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4F46E5, #06B6D4) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 12px 24px !important;
        border: none !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
    }

    .stButton > button:active { transform: translateY(0) !important; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B, #0F172A) !important;
    }

    [data-testid="stSidebar"] h2 { color: #F1F5F9 !important; }
    [data-testid="stSidebar"] p { color: #CBD5E1 !important; }

    .stAlert { border-radius: 10px !important; border: none !important; }

    .response-container {
        background: white !important;
        border-radius: 12px !important;
        padding: 24px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07) !important;
        margin-top: 20px !important;
        line-height: 1.8;
        font-size: 1.05rem;
        color: #1E293B !important;
    }

    .response-container * { color: #1E293B !important; }

    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        color: #1E293B !important;
    }

    .feature-card b { color: #4F46E5 !important; }

    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15);
        border-color: #4F46E5;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #64748B;
        font-weight: 500;
    }

    hr {
        border: none;
        height: 1px;
        background: #E2E8F0;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


def get_ai_response(query):
    if not query or query.strip() == "":
        return "Please enter a question."

    try:
        api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        if not api_key:
            return "ERROR: Key not found in secrets at all."

        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": query}],
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            stream=False,
            stop=None
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings & Info")
    st.markdown("---")
    st.markdown("### 🤖 About This App")
    st.markdown("""
    **AI Assistant** powered by Meta's **Llama 3.3 70B** via Groq.

    - ⚡ Lightning-fast responses
    - 💡 High-quality AI
    - 🆓 Completely free
    - 🔒 No billing required
    """)

    st.markdown("---")
    st.markdown("### 📚 What You Can Do")
    features = [
        ("💬", "Chat & Q&A"),
        ("📝", "Creative Writing"),
        ("💻", "Code Generation"),
        ("🧠", "Problem Solving"),
        ("🌍", "Translation"),
        ("📊", "Data Analysis"),
    ]
    for emoji, feature in features:
        st.markdown(f"**{emoji} {feature}**")

    st.markdown("---")
    st.markdown("### 🚀 Quick Tips")
    st.markdown("""
    1. Be specific in your questions
    2. Ask follow-up questions
    3. Request code or explanations
    4. Try creative prompts
    """)
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")


# Main Content
st.markdown("## ✨ AI Assistant")
st.markdown('<p class="subtitle">Powered by Llama 3.3 70B via Groq — Fast & Free</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([3, 1], gap="large")

with col1:
    st.markdown("### 💭 Ask Me Anything")
    user_input = st.text_input(
        "Your question or prompt:",
        key="input",
        placeholder="Type your question here... (e.g., 'Write a Python function to sort a list')"
    )

    button_col1, button_col2, button_col3 = st.columns(3, gap="small")
    with button_col1:
        submit = st.button("🚀 Submit", use_container_width=True)
    with button_col2:
        clear = st.button("🔄 Clear", use_container_width=True)
    with button_col3:
        st.markdown("")

with col2:
    st.markdown("### 📊 Status")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #4F46E5, #06B6D4);
                border-radius: 10px; padding: 20px; color: white; text-align: center;'>
    <div style='font-size: 2rem; margin-bottom: 10px;'>🟢</div>
    <div style='font-weight: 600; margin-bottom: 5px;'>Ready</div>
    <div style='font-size: 0.9rem; opacity: 0.9;'>Connected & Active</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

if clear:
    st.rerun()

if submit:
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a question first!")
    else:
        with st.spinner("🤔 Thinking... Processing your request..."):
            response = get_ai_response(user_input)

        if response.startswith("ERROR:"):
            st.error(f"❌ {response}")
        else:
            st.success("✅ Response generated successfully!")
            st.markdown(f"""
            <div class="response-container">
            {response}
            </div>
            """, unsafe_allow_html=True)

# Example queries
st.markdown("---")
st.markdown("### 💡 Example Queries")

example_col1, example_col2, example_col3 = st.columns(3, gap="medium")

with example_col1:
    st.markdown("""
    <div class="feature-card">
    <b>💻 Code Generation</b><br>
    "Write a Python function that checks if a number is prime"
    </div>
    """, unsafe_allow_html=True)

with example_col2:
    st.markdown("""
    <div class="feature-card">
    <b>📚 Learning</b><br>
    "Explain machine learning in simple terms"
    </div>
    """, unsafe_allow_html=True)

with example_col3:
    st.markdown("""
    <div class="feature-card">
    <b>✍️ Creative</b><br>
    "Write a funny poem about programming"
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; font-size: 0.9rem; padding: 20px;'>
<p>⚡ Powered by <b>Llama 3.3 70B</b> via <b>Groq</b> | Built with <b>Streamlit</b></p>
<p>Free • Fast • Reliable | No Billing Required</p>
</div>
""", unsafe_allow_html=True)
