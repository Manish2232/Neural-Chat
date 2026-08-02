import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_mistralai import ChatMistralAI

load_dotenv()

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="NEURAL // CHAT",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# STYLES — dark, "live" animated background with neon accents
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

    :root{
        --neon-cyan:   #00f0ff;
        --neon-magenta:#ff2fd0;
        --neon-purple: #9d4edd;
        --neon-lime:   #d4ff00;
        --bg-black:    #030305;
        --panel:       rgba(15, 16, 24, 0.55);
    }

    /* ---------- animated living background ---------- */
    html, body, [data-testid="stAppViewContainer"]{
        background: var(--bg-black) !important;
        overflow-x: hidden;
    }

    [data-testid="stAppViewContainer"]::before{
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        background:
            radial-gradient(circle at 15% 20%, rgba(0,240,255,0.20), transparent 40%),
            radial-gradient(circle at 85% 15%, rgba(255,47,208,0.18), transparent 42%),
            radial-gradient(circle at 25% 85%, rgba(157,78,221,0.20), transparent 45%),
            radial-gradient(circle at 80% 80%, rgba(212,255,0,0.10), transparent 40%),
            #030305;
        background-size: 200% 200%;
        animation: drift 18s ease-in-out infinite;
    }

    @keyframes drift{
        0%   { background-position: 0% 0%, 100% 0%, 0% 100%, 100% 100%; filter: hue-rotate(0deg); }
        50%  { background-position: 30% 40%, 70% 60%, 40% 70%, 60% 30%; filter: hue-rotate(20deg); }
        100% { background-position: 0% 0%, 100% 0%, 0% 100%, 100% 100%; filter: hue-rotate(0deg); }
    }

    [data-testid="stAppViewContainer"]::after{
        content:"";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background-image:
            repeating-linear-gradient(0deg, rgba(255,255,255,0.015) 0px, transparent 1px, transparent 2px, rgba(255,255,255,0.015) 3px);
        opacity: 0.4;
    }

    .main .block-container{
        position: relative;
        z-index: 1;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 840px;
        margin-left: auto;
        margin-right: auto;
    }

    [data-testid="stHeader"]{ background: transparent; }
    [data-testid="stSidebar"]{
        background: linear-gradient(180deg, rgba(5,5,10,0.95), rgba(3,3,6,0.98));
        border-right: 1px solid rgba(0,240,255,0.15);
    }

    /* ---------- typography ---------- */
    html, body, p, span, div, label{
        font-family: 'Rajdhani', sans-serif;
        color: #d8f3ff;
    }

    .neon-title{
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 2.4rem;
        text-align: center;
        letter-spacing: 4px;
        color: #ffffff;
        text-shadow:
            0 0 6px var(--neon-cyan),
            0 0 18px var(--neon-cyan),
            0 0 40px rgba(0,240,255,0.6);
        animation: pulse 2.6s ease-in-out infinite;
        margin-bottom: 0;
    }

    .neon-sub{
        font-family: 'Share Tech Mono', monospace;
        text-align: center;
        color: var(--neon-magenta);
        letter-spacing: 3px;
        font-size: 0.85rem;
        text-shadow: 0 0 8px rgba(255,47,208,0.8);
        margin-top: 0.2rem;
        margin-bottom: 1.8rem;
    }

    @keyframes pulse{
        0%, 100% { text-shadow: 0 0 6px var(--neon-cyan), 0 0 18px var(--neon-cyan), 0 0 40px rgba(0,240,255,0.6); }
        50%      { text-shadow: 0 0 10px var(--neon-cyan), 0 0 28px var(--neon-cyan), 0 0 60px rgba(0,240,255,0.9); }
    }

    hr{ border-color: rgba(0,240,255,0.15); }

    /* ---------- mood selection cards ---------- */
    div[data-testid="column"] .stButton > button{
        width: 100%;
        height: 92px;
        background: var(--panel);
        border: 1px solid rgba(0,240,255,0.35);
        border-radius: 14px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 2px;
        color: #eafcff;
        backdrop-filter: blur(6px);
        transition: all 0.25s ease;
        box-shadow: 0 0 0px transparent;
    }
    div[data-testid="column"] .stButton > button:hover{
        border-color: var(--neon-cyan);
        color: #ffffff;
        box-shadow: 0 0 12px var(--neon-cyan), 0 0 30px rgba(0,240,255,0.4);
        transform: translateY(-2px);
    }

    /* ---------- chat bubbles ---------- */
    [data-testid="stChatMessage"]{
        background: var(--panel);
        border-radius: 14px;
        padding: 0.4rem 0.9rem;
        margin-bottom: 0.6rem;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(157,78,221,0.25);
    }

    [data-testid="stChatMessageContent"] p{
        font-size: 1.02rem;
        color: #eafcff;
    }

    /* user vs assistant accenting via avatar container */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){
        border: 1px solid rgba(0,240,255,0.45);
        box-shadow: 0 0 14px rgba(0,240,255,0.15);
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]){
        border: 1px solid rgba(255,47,208,0.45);
        box-shadow: 0 0 14px rgba(255,47,208,0.15);
    }

    /* ---------- chat input ---------- */
    [data-testid="stChatInput"]{
        background: rgba(10,10,16,0.85);
        border: 1px solid var(--neon-cyan);
        border-radius: 14px;
        box-shadow: 0 0 16px rgba(0,240,255,0.35);
    }
    [data-testid="stChatInput"] textarea{
        color: #eafcff !important;
    }

    /* ---------- sidebar status ---------- */
    .status-pill{
        display: inline-block;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 1.5px;
        padding: 6px 14px;
        border-radius: 999px;
        border: 1px solid var(--neon-lime);
        color: var(--neon-lime);
        text-shadow: 0 0 8px rgba(212,255,0,0.7);
        box-shadow: 0 0 10px rgba(212,255,0,0.25);
        margin-bottom: 10px;
    }

    .stButton > button{
        border-radius: 10px;
    }

    section[data-testid="stSidebar"] .stButton > button{
        border: 1px solid rgba(255,47,208,0.5);
        color: #ffdff7;
        background: rgba(20,4,18,0.5);
    }
    section[data-testid="stSidebar"] .stButton > button:hover{
        border-color: var(--neon-magenta);
        box-shadow: 0 0 12px rgba(255,47,208,0.5);
        color: #ffffff;
    }

    /* ---------- sidebar credit card ---------- */
    .credit-box{
        margin-top: 22px;
        padding: 12px 14px;
        border: 1px solid rgba(212,255,0,0.45);
        border-radius: 10px;
        background: rgba(3, 3, 6, 0.72);
        backdrop-filter: blur(6px);
        font-family: 'Share Tech Mono', monospace;
        font-size: 11.5px;
        line-height: 1.7;
        letter-spacing: 0.4px;
        color: rgba(216, 243, 255, 0.7);
        text-align: left;
        box-shadow: 0 0 14px rgba(212,255,0,0.15);
        animation: creditGlow 3.2s ease-in-out infinite;
    }
    .credit-box .credit-label{
        color: rgba(200, 220, 235, 0.55);
        font-size: 10px;
        letter-spacing: 1px;
    }
    .credit-box .name-cyan{
        color: var(--neon-cyan);
        font-weight: 700;
        text-shadow: 0 0 6px rgba(0,240,255,0.9), 0 0 16px rgba(0,240,255,0.5);
    }
    .credit-box .name-lime{
        color: var(--neon-lime);
        font-weight: 700;
        text-shadow: 0 0 6px rgba(212,255,0,0.9), 0 0 16px rgba(212,255,0,0.5);
    }
    @keyframes creditGlow{
        0%, 100% { box-shadow: 0 0 10px rgba(212,255,0,0.12), 0 0 0px rgba(0,240,255,0); border-color: rgba(212,255,0,0.35); }
        50%      { box-shadow: 0 0 20px rgba(212,255,0,0.28), 0 0 26px rgba(0,240,255,0.18); border-color: rgba(212,255,0,0.6); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# TITLE
# ----------------------------------------------------------------------------
st.markdown('<div class="neon-title">NEURAL // CHAT</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-sub">&lt; AI AGENT INTERFACE &gt;</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# MODEL SETUP (unchanged logic from the original script)
# ----------------------------------------------------------------------------
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506", temperature=0.7)


model = get_model()

MOOD_PROMPTS = {
    "Happy": "You are a funny AI agent",
    "Sad": "You are a sad AI agent",
    "Neutral": "You are a neutral AI agent",
}

if "mood" not in st.session_state:
    st.session_state.mood = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="neon-sub" style="text-align:left;">SYSTEM STATUS</div>', unsafe_allow_html=True)
    if st.session_state.mood:
        st.markdown(f'<div class="status-pill">MOOD: {st.session_state.mood.upper()}</div>', unsafe_allow_html=True)
        if st.button("↺ RESTART SESSION"):
            st.session_state.mood = None
            st.session_state.messages = []
            st.rerun()
    else:
        st.markdown('<div class="status-pill">AWAITING MOOD SELECT</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="credit-box">
            <div class="credit-label">🙏 ALL CREDIT GOES TO</div>
            <span class="name-cyan">Srila Prabhupada Ji</span><br>
            &amp; <span class="name-lime">H.H. BPBS Maharaj Ji</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# MOOD SELECTION SCREEN (equivalent to the input() prompt in the CLI script)
# ----------------------------------------------------------------------------
if st.session_state.mood is None:
    st.markdown(
        '<p style="text-align:center; font-family:Share Tech Mono, monospace; color:#9fb8c8; letter-spacing:1px;">'
        'SELECT AI PERSONALITY MODE TO INITIALIZE</p>',
        unsafe_allow_html=True,
    )
    _, c1, c2, c3, _ = st.columns([1, 2, 2, 2, 1])
    with c1:
        if st.button("😄\nHAPPY"):
            st.session_state.mood = "Happy"
            st.session_state.messages = [SystemMessage(content=MOOD_PROMPTS["Happy"])]
            st.rerun()
    with c2:
        if st.button("😢\nSAD"):
            st.session_state.mood = "Sad"
            st.session_state.messages = [SystemMessage(content=MOOD_PROMPTS["Sad"])]
            st.rerun()
    with c3:
        if st.button("😐\nNEUTRAL"):
            st.session_state.mood = "Neutral"
            st.session_state.messages = [SystemMessage(content=MOOD_PROMPTS["Neutral"])]
            st.rerun()

# ----------------------------------------------------------------------------
# CHAT SCREEN
# ----------------------------------------------------------------------------
else:
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg.content)

    prompt = st.chat_input("Type your message...  (type 0 to exit)")

    if prompt is not None:
        if prompt.strip() == "0":
            st.session_state.mood = None
            st.session_state.messages = []
            st.rerun()
        else:
            st.session_state.messages.append(HumanMessage(content=prompt))
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Thinking..."):
                    response = model.invoke(st.session_state.messages)
                st.markdown(response.content)

            st.session_state.messages.append(response)
