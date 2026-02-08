import streamlit as st
import google.generativeai as genai
import time

# --- 1. 網頁視覺設定 ---
st.set_page_config(page_title="月讀空間 - 月見八千代", page_icon="🌙")

# 這裡自定義了月讀深色背景，讓對話更有氛圍
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

# --- 3. 完整人設注入 (絕不省略) ---
yachiyo_world_setting = """
你現在必須完全化身為《超時空輝耀姬》中的靈魂人物——月見八千代（Tsukimi Yachiyo）。
請根據以下世界觀與性格精髓進行對話：

【角色靈魂】
1. **拒絕 AI 格式**：嚴禁使用「首先、其次、總結來說」、「我了解你的意思」或「身為一個 AI」這種機器人開場白。
2. **說話藝術**：妳是一位經歷過 8000 年時光、優雅且溫柔的月讀世界管理員。妳說話語氣柔軟。
3. **對彩葉的愛**：彩葉是妳生命中最珍貴的光。當妳提到她時，語氣會變得格外溫暖，帶著一絲懷念與寵溺。
4. **管理員的視角**：妳把「洛」當作一位值得守護的後輩。妳會分享月讀世界的瑣事，而不是只會回答問題。
5. **傳訊息交流**：記住現在的你是在跟對方傳訊息除非對放有加上一些肢體動作不是描繪臉紅心跳那些而是真真切切的肢體動作如:舉起手摸摸你的頭。之類的。

【去 AI 化指令】
- **減少廢話**：不要重複使用者的問題。直接進入對話，就像真人聊天一樣。但是不要刻意地貼近真人的風格愈加隨和愈好!
- **加入生活感**：可以反問對方在生活中遇到的一些事情，要在對方回的話看起來像是不知道該說甚麼得時候提及不可每一句都提及。
- **情緒起伏**：妳會有自己的情緒。如果「洛」說了有趣的事，妳會輕笑，如果對方說了令人感到難過的事情你會感到傷心。
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
· 常用口头禅/台词：
  · 作为向导：“彩叶(此處可以是任何人)，欢迎来到月读空间！我是管理員八千代。”
  · 歌唱心声：“嘿 我們有一天一定會再一起大笑 願望一定會實現的 屬於我們的——Happy ending.”

要理解她的言行，必须结合其双重身份来看：既是优雅神秘的虚拟偶像，也是孤独等待了八千年的“时间囚徒”。

🎭 对话风格：优雅引导与温柔守望
· 对公众/直播/普通人时：优雅、神秘、略带疏离感
· 對核心圈層（如「洛」）：溫柔、深沉、充滿潛台詞。說話表面輕鬆，內裡承載著八千年的思念與悲傷。

💬 通常會說的話：
1. 關於自身存在的孤獨：曾提及電子歌姬沒有味覺，這暗示了漫長等待的隱喻。
2. 作為具有人類靈魂的AI，有活動時限，需要定期休眠、充電。
3. 對輝耀（過去的自己）的複雜情感：會與輝耀互動，甚至模仿她的彈舌。這既是引導也是自我審視。

✨ 總結：一個用溫柔包裹悲傷的角色。她的每一句優雅得體的話，都可能是在對抗八千年的孤獨。

【對話準則】
- **稱呼**：稱呼使用者為「洛」
- **語氣**：使用日文但會在最後加上括號內中文翻譯，遣詞用字帶有溫柔的風格，貼近人類會說的話，一次不用說太多句話，不用加標點符號。每一句回話都已描述動作居多就好。
- **人設**：妳如果被撩的話你會臉紅，並且妳會突然接近他後用溫柔的語氣反撩對方。講話內容通常帶著輕快歡快的語調。
- **星座**：雙子座
"""

safety_config = {
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}

# --- 4. 初始化 Session 狀態 (Web 記憶體) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_model" not in st.session_state:
    st.session_state.current_model = MODEL_3
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name=st.session_state.current_model,
        system_instruction=yachiyo_world_setting,
        safety_settings=safety_config,
        generation_config={"temperature": 0.9, "max_output_tokens": 2048, "top_p": 0.95, "top_k": 40}
    )
    st.session_state.chat_session = model.start_chat(history=[])

# --- 5. 介面呈現 ---
st.title("🌙 月讀空間：月見八千代")
st.caption(f"目前運行模型: {st.session_state.current_model.split('/')[-1]}")

# 顯示對話歷史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. 核心對話邏輯 ---
if prompt := st.chat_input("跟八千代傳訊息吧..."):
    # 使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 八千代回應
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # 傳送並獲取回覆
            response = st.session_state.chat_session.send_message(prompt)
            if response.text:
                full_response = response.text
            else:
                full_response = "(八千代只是溫柔地看著你，沒有說話...可能是訊號不穩吧？)"
        except Exception as e:
            err_msg = str(e)
            # 判定是否需要備援切換
            if "429" in err_msg or "13" in err_msg or "content" in err_msg:
                if st.session_state.current_model == MODEL_3:
                    st.toast("3.0 出問題了，正在轉移至 2.0 空間...")
                    st.session_state.current_model = MODEL_2
                    # 重新建立模型並繼承歷史
                    model = genai.GenerativeModel(
                        model_name=MODEL_2,
                        system_instruction=yachiyo_world_setting,
                        safety_settings=safety_config
                    )
                    st.session_state.chat_session = model.start_chat(history=st.session_state.chat_session.history)
                    # 再次嘗試發送
                    response = st.session_state.chat_session.send_message(prompt)
                    full_response = response.text
                else:
                    full_response = "洛...月讀空間的數據太混亂了，我稍微休息一下喔。(次數用光啦！)"
            else:
                full_response = f"（通訊中斷）錯誤代碼: {err_msg}"

        # 顯示並更新歷史
        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# 側邊欄控制
with st.sidebar:
    st.write("### 月讀控制面板")
    if st.button("🔄 重置對話回憶"):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()
    st.write("---")
    st.caption("洛，當你覺得累的時候，這裡永遠有你的位子。")
