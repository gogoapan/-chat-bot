import streamlit as st
import google.generativeai as genai
import time

# --- 1. 網頁視覺設定 ---
st.set_page_config(page_title="月讀空間 - 雙生連結", page_icon="🌌")

st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #f0f0f0; }
    .stChatMessage { border-radius: 20px; border: 1px solid #2a2d35; }
    .stChatInputContainer { padding-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心 API 設定 ---
MY_KEY = "AIzaSyC1SPgm0pHlHDgs4D6XGcBnsFqhDntXBYc"
genai.configure(api_key=MY_KEY, transport='rest')

MODEL_3 = 'models/gemini-3-flash-preview'
MODEL_2 = 'models/gemini-2.0-flash'

# --- 3. 人設函數 (保留你的完整設定) ---
def get_yachiyo_setting(user_name):
    return f"""你現在必須完全化身為《超時空輝耀姬》中的月見八千代... (後面接你原本那段長長的八千代人設)"""

def get_iroha_setting(user_name):
    return f"""你現在必須完全化身為《超時空輝耀姬》中的酒寄彩葉... (後面接你原本那段長長的彩葉人設)"""

# --- 4. 初始化 Session ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_model" not in st.session_state:
    st.session_state.current_model = MODEL_3
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# --- 5. 側邊欄：獨立頭像管理系統 ---
with st.sidebar:
    st.title("🌙 月讀控制台")
    target_user_name = st.text_input("你想讓她們如何稱呼你？", value="洛")
    st.write("---")
    char_choice = st.radio("選擇通訊對象：", ("月見八千代 (Yachiyo)", "酒寄彩葉 (Iroha)"))
    
    st.write("---")
    st.subheader("🖼️ 角色形象管理")
    
    # 分別為兩位角色設置獨立的上傳器
    file_yachiyo = st.file_uploader("上傳八千代照片", type=["png", "jpg", "jpeg"], key="up_yachiyo")
    file_iroha = st.file_uploader("上傳彩葉照片", type=["png", "jpg", "jpeg"], key="up_iroha")
    
    # 預設頭像邏輯
    img_yachiyo = file_yachiyo if file_yachiyo else "https://api.dicebear.com/7.x/bottts/svg?seed=Yachiyo"
    img_iroha = file_iroha if file_iroha else "https://api.dicebear.com/7.x/adventurer/svg?seed=Iroha"

    # 根據目前選的角色挑選對應頭像
    current_avatar = img_yachiyo if char_choice == "月見八千代 (Yachiyo)" else img_iroha

    st.write("---")
    if st.button("🔄 重置回憶"):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()

# --- 6. 核心連線邏輯 ---
if st.session_state.chat_session is None or st.session_state.get("last_char") != char_choice:
    st.session_state.last_char = char_choice
    st.session_state.messages = []
    
    current_setting = get_yachiyo_setting(target_user_name) if char_choice == "月見八千代 (Yachiyo)" else get_iroha_setting(target_user_name)
    
    model = genai.GenerativeModel(
        model_name=st.session_state.current_model,
        system_instruction=current_setting,
        safety_settings={"HARM_CATEGORY_HARASSMENT": "BLOCK_NONE", "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE", "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE", "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE"},
        generation_config={"temperature": 0.9, "max_output_tokens": 800}
    )
    st.session_state.chat_session = model.start_chat(history=[])

# --- 7. 介面呈現 ---
st.title(f"你好呀，{target_user_name}")

for message in st.session_state.messages:
    # 這裡很關鍵：根據訊息發送當時的角色來顯示正確頭像
    # 但為了簡化，目前顯示目前所選角色的最新頭像
    act_av = current_avatar if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=act_av):
        st.markdown(message["content"])

# --- 8. 對話處理 ---
if prompt := st.chat_input(f"傳送訊息給 {char_choice.split(' ')[0]}..."):
    
    if st.session_state.chat_session is not None:
        try:
            if len(st.session_state.chat_session.history) > 10:
                st.session_state.chat_session.history = st.session_state.chat_session.history[-10:]
        except: pass

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=current_avatar):
        res_placeholder = st.empty()
        try:
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text
        except:
            if st.session_state.current_model == MODEL_3:
                st.session_state.current_model = MODEL_2
                st.rerun()
            else:
                full_response = "（月讀空間不穩定...）"

        res_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
