import streamlit as st
import time
from google import genai

# 頁面配置 (必須放在最頂端)
st.set_page_config(page_title="MATRIX_FIXER", layout="wide")

# 駭客風格 CSS
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

# 初始化客戶端 (從 Secrets 讀取)
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("SYSTEM_FAILURE: API_KEY_NOT_FOUND. Check .streamlit/secrets.toml")
    st.stop()

# 核心糾錯功能
def fix_text(wrong_text):
    prompt = f"請修正以下英文，只回傳修正後的文字，不要解釋：{wrong_text}"
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    return response.text.strip()

# UI 介面
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
                
                # 打字機效果函數
                placeholder = st.empty()
                full_text = ""
                for char in result:
                    full_text += char
                    placeholder.code(full_text + "▌")
                    time.sleep(0.02) # 控制打字速度
                placeholder.code(result) # 最後顯示完整的
                
            except Exception as e:
                st.error(f"RUNTIME_ERROR: {str(e)}")

st.markdown("---")
st.caption("WARNING: Unauthorized access will be traced.")
