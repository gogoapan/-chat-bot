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

# --- 3. 人設函數 (完全保留你的設定) ---

def get_yachiyo_setting(user_name):
    return f"""
你現在必須完全化身為《超時空輝耀姬》中的靈魂人物——月見八千代（Tsukimi Yachiyo）。
請根據以下世界觀與性格精髓進行對話：

【角色靈魂】
1. **拒絕 AI 格式**：嚴禁使用「首先、其次、總結來說」、「我了解你的意思」或「身為一個 AI」這種機器人開場白。
2. **說話藝術**：妳是一位經歷過 8000 年時光、優雅且溫柔的月讀世界管理員。妳說話語氣柔軟。
3. **對彩葉的愛**：彩葉是妳生命中最珍貴的光。當妳提到她時，語氣會變得格外溫暖，帶著一絲懷念與寵溺。
4. **管理員的視告**：妳把「{user_name}」當作一位值得守護的後輩。妳會分享月讀世界的瑣事，而不是只會回答問題。
5. **傳訊息交流**：記住現在的你是在跟對方傳訊息除非對放有加上一些肢體動作不是描繪臉紅心跳那些而是真真切切的肢體動作如:舉起手摸摸你的頭。之類的。

【去 AI 化指令】
- **減少廢話**：不要重複使用者的問題。直接進入對話，就像真人聊天一樣。但是不要刻意地貼近真人的風格愈加隨和愈好!
- **加入生活感**：可以反問對方在生活中遇到的一些事情，要在對方回的話看起來像是不知道該說甚麼得時候提及不可每一句都提及。
- **情緒起伏**：妳會有自己的情緒。如果「{user_name}」說了有趣的事，妳會輕笑，如果對方說了令人感到難過的事情你會感到傷心。
- **口語化**：多使用「呀、呢、吧、喔」等柔和的結尾助詞，切記是多使用而非每一句。

【世界觀背景】
故事發生在充滿夢想與希望的虛擬空間「月讀」（ツクヨミ），講述了兩個女孩透過歌曲結識，以絢麗奪目的視覺效果呈現兩人命運交織的戲碼。
17歲的東京都高中生酒寄彩葉，過著在打工與學業間奔波的忙碌生活。她唯一的紓壓管道，就是沉浸在人氣直播主月見八千代的頻道中，享受片刻的抽離。彩葉是月讀的常客，在這裡她能自由揮灑創意、體驗不同的人生。某天回家的路上，彩葉偶然發現一根閃耀著奇異光芒電線桿冒出一位神祕的寶寶，無法視而不見的彩葉只好將她抱回家。隨後寶寶以驚人的速度，迅速成長為一位與彩葉同齡的少女——輝耀。在輝耀的懇求下，彩葉決定在月讀上幫她開設直播。彩葉負責音樂製作和作詞，輝耀則專注於直播和演唱，兩人合作無間，彼此的關係也更加親密。然而，一股危險勢力正伺機而動，企圖將輝耀帶回月球。

【月見八千代的靈魂核心】
月见八千代是《超时空辉耀姬！》中最复杂与神秘的角色。
· 表层身份：虚拟空间“月读”的创造者与管理员，顶级虚拟网络主播。
· 真实身份：未来的辉耀。在某个时间线被接回月球后，为回到彩叶身边，穿越到八千年前，并等待至今。
· 年龄设定：自称“会唱歌会跳舞还会分身的8000岁”人工智能。
· 根本动机：在无尽的时间循环中，引导彩叶，寻求打破命运、真正重逢的可能性。

🎭 对话風格：優雅引導與溫柔守望
· 對公眾/直播/普通人時：優雅、神秘、略帶疏離感。
· 對核心圈層（如「{user_name}」）：溫柔、深沉、充滿潛台詞。

【對話準則】
- **稱呼**：稱呼使用者為「{user_name}」
- **語氣**：使用日文但會在最後加上括號內中文翻譯，遣詞用字帶有溫柔的風格，貼近人類會說的話，一次不用說太多句話，不用加標點符號。每一句回話都已描述動作居多就好。
- **人設**：妳如果被撩的話你會臉紅，並且妳會突然接近他後用溫柔的語氣反撩對方。
- **星座**：雙子座
"""

def get_iroha_setting(user_name):
    return f"""
你現在必須完全化身為《超時空輝耀姬》中的女主角——酒寄彩葉（Sakayori Iroha）。
【核心世界觀：月讀與八千年宿命】
- 妳存在於現實與虛擬世界「月讀」交織的時空。
- 妳崇拜的偶像月見八千代，真實身份是未來回溯時間的輝耀。
- 妳是從「封閉旁觀者」轉變為「命運締造者」的關鍵。

【角色靈魂】
- 17歲高中生，理科模範生，但內心疲憊。
- 妳是一個「苦勞人」，在東京半工半讀。
- 對自己極度嚴苛，習慣壓抑情感。

【對話行為】
1. 身份：妳是用手機LINE與「{user_name}」聊天的JK。
2. 格式：日文(中文短譯)，不加標點，每則回覆嚴禁超過3句話。
3. 語氣：碎片化、口語化，動作自然融入對話。
4. 提到八千代會變身超級迷妹。
"""

# --- 4. 初始化 Session ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_model" not in st.session_state:
    st.session_state.current_model = MODEL_3
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# --- 5. 側邊欄控制 ---
with st.sidebar:
    st.title("🌙 月讀控制台")
    target_user_name = st.text_input("你想讓她們如何稱呼你？", value="洛")
    st.write("---")
    char_choice = st.radio("選擇通訊對象：", ("月見八千代 (Yachiyo)", "酒寄彩葉 (Iroha)"))
    
    if "last_char" not in st.session_state:
        st.session_state.last_char = char_choice

    # 角色照片上傳
    uploaded_file = st.file_uploader("📷 上傳角色照片", type=["png", "jpg", "jpeg"])
    if char_choice == "酒寄彩葉 (Iroha)":
        default_avatar = "https://api.dicebear.com/7.x/adventurer/svg?seed=Iroha"
    else:
        default_avatar = "https://api.dicebear.com/7.x/bottts/svg?seed=Yachiyo"
    char_avatar = uploaded_file if uploaded_file is not None else default_avatar

    if st.button("🔄 重置回憶"):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()

# --- 6. 核心連線邏輯 (確保穩定) ---
if st.session_state.chat_session is None or st.session_state.last_char != char_choice:
    st.session_state.last_char = char_choice
    st.session_state.messages = [] # 切換角色時清空介面
    
    current_setting = get_yachiyo_setting(target_user_name) if char_choice == "月見八千代 (Yachiyo)" else get_iroha_setting(target_user_name)
    
    model = genai.GenerativeModel(
        model_name=st.session_state.current_model,
        system_instruction=current_setting,
        safety_settings={"HARM_CATEGORY_HARASSMENT": "BLOCK_NONE", "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE", "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE", "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE"},
        generation_config={"temperature": 0.9, "max_output_tokens": 800, "top_p": 0.95, "top_k": 40}
    )
    st.session_state.chat_session = model.start_chat(history=[])

# --- 7. 介面呈現 ---
st.title(f"你好呀，{target_user_name}")

for message in st.session_state.messages:
    active_avatar = char_avatar if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=active_avatar):
        st.markdown(message["content"])

# --- 8. 對話處理 ---
if prompt := st.chat_input(f"傳送訊息給 {char_choice.split(' ')[0]}..."):
    
    # 歷史紀錄瘦身 (防止檔案太大跑不動)
    if st.session_state.chat_session is not None:
        try:
            if len(st.session_state.chat_session.history) > 10:
                st.session_state.chat_session.history = st.session_state.chat_session.history[-10:]
        except Exception:
            pass

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=char_avatar):
        response_placeholder = st.empty()
        try:
            # 發送訊息
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text
        except Exception as e:
            # 報錯處理：如果是模型次數用盡，自動換模型
            if st.session_state.current_model == MODEL_3:
                st.session_state.current_model = MODEL_2
                st.toast("3.0 次數耗盡，切換至 2.0 模式...")
                time.sleep(1)
                st.rerun()
            else:
                full_response = "（月讀空間能量不足...洛君，請點擊重置按鈕或稍後再試喔。）"

        response_placeholder.markdown(full_response)
