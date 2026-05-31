import streamlit as st
import time
import google.generativeai as genai

# 1. 頁面配置 (必須放在最頂端)
st.set_page_config(page_title="MATRIX_FIXER", layout="wide")

# 2. 駭客風格 CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #00FF41; font-family: 'Courier New', monospace; }
    .stTextArea textarea { background-color: #1a1a1a !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; font-family: 'Courier New', monospace !important; }
    div.stButton > button { background-color: #00FF41 !important; color: #000000 !important; font-weight: bold; border-radius: 0px !important; border: none; }
    h1, h2, h3, p { color: #00FF41 !important; }
    .blink { animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# 3. 初始化 Gemini (修正後的安全配置)
try:
    # 讀取 Streamlit Secrets 中的 API Key
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("SYSTEM_FAILURE: 密鑰讀取錯誤，請檢查 Streamlit Secrets 設定。")
    st.stop()

# 4. 核心糾錯功能
def fix_text(wrong_text):
    prompt = f"請修正以下英文，只回傳修正後的文字，不要解釋：{wrong_text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# 5. UI 介面
st.title("> SYSTEM: MATRIX_ENGLISH_FIXER")
st.markdown("---")
st.write("Status: Connection Established... <span class='blink'>_</span>", unsafe_allow_html=True)

user_input = st.text_area("COMMAND_INPUT:", height=150, placeholder="Type your broken English here...")

if st.button("> EXECUTE_CORRECTION"):
    if not user_input.strip():
        st.warning("ERROR: INPUT_NULL_DETECTED")
    else:
        with st.spinner('Accessing Neural Link...'):
            try:
                result = fix_text(user_input)
                st.subheader("> OUTPUT_STREAM:")
                
                # 打字機效果
                placeholder = st.empty()
                full_text = ""
                for char in result:
                    full_text += char
                    placeholder.code(full_text + "▌")
                    time.sleep(0.02)
                placeholder.code(result) 
                
            except Exception as e:
                st.error(f"RUNTIME_ERROR: {str(e)}")

st.markdown("---")
st.caption("WARNING: Unauthorized access will be traced.")
