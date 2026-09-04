"""
Cara jalanin:

streamlit run app.py
"""

import streamlit as st

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="My ChatBot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
    ===================================================== */

    .stApp {
        background-color: #f4f7f5;
    }


    .block-container {
        max-width: 760px;
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 7rem;
    }


    /* Hilangkan menu/footer bawaan jika diperlukan */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* =====================================================
       HEADER
    ===================================================== */

    .chat-header {
        text-align: center;
        margin-bottom: 2rem;
    }


    .chat-logo {
        width: 64px;
        height: 64px;

        display: flex;
        align-items: center;
        justify-content: center;

        margin: 0 auto 12px auto;

        border-radius: 20px;

        background: linear-gradient(
            135deg,
            #16a34a,
            #22c55e
        );

        font-size: 32px;

        box-shadow:
            0 10px 25px
            rgba(22, 163, 74, 0.25);
    }


    .chat-title {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 6px;
    }


    .chat-subtitle {
        color: #6b7280;
        font-size: 14px;
    }


    /* =====================================================
       SECTION TITLE
    ===================================================== */

    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 1rem;
    }


    /* =====================================================
       BUTTON
    ===================================================== */

    .stButton button {

        width: 100%;

        background-color: #16a34a;

        color: white;

        border: none;

        border-radius: 12px;

        min-height: 44px;

        font-weight: 600;

        transition: all 0.2s ease;

    }


    .stButton button:hover {

        background-color: #15803d;

        color: white;

        transform: translateY(-1px);

        box-shadow:
            0 8px 20px
            rgba(22, 163, 74, 0.25);

    }


    /* =====================================================
       TEXT INPUT
    ===================================================== */

    .stTextInput input {

        border-radius: 12px !important;

        border: 1px solid #d1d5db !important;

        min-height: 44px;

    }


    .stTextInput input:focus {

        border-color: #22c55e !important;

        box-shadow:
            0 0 0 2px
            rgba(34, 197, 94, 0.15) !important;

    }


    /* =====================================================
       CHAT MESSAGE
    ===================================================== */

    # [data-testid="stChatMessage"] {

    #     background-color: white;

    #     border: 1px solid #e5e7eb;

    #     border-radius: 16px;

    #     padding: 0.7rem;

    #     margin-bottom: 0.8rem;

    }
    
    /* =====================================================
   CHAT MESSAGE
===================================================== */

[data-testid="stChatMessage"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 0.7rem;
    margin-bottom: 0.8rem;
}


/* =====================================================
   CHAT MESSAGE TEXT COLOR
===================================================== */

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] div {
    color: #111827 !important;
}

[data-testid="stChatMessageContent"] {
    color: #111827 !important;
}

[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li,
[data-testid="stChatMessageContent"] strong,
[data-testid="stChatMessageContent"] em {
    color: #111827 !important;
}

[data-testid="stChatMessageContent"] code {
    color: #111827 !important;
}


    /* =====================================================
       CHAT INPUT
    ===================================================== */

    [data-testid="stChatInput"] {

        border-top: none;

    }


    [data-testid="stChatInput"] textarea {

        border-radius: 18px;

        border: 1px solid #d1d5db;

    }


    [data-testid="stChatInput"] textarea:focus {

        border-color: #22c55e;

        box-shadow:
            0 0 0 2px
            rgba(34, 197, 94, 0.15);

    }


    /* =====================================================
       MOBILE
    ===================================================== */

    @media (max-width: 600px) {

        .block-container {

            padding-top: 1.2rem;

            padding-left: 0.8rem;

            padding-right: 0.8rem;

            padding-bottom: 6rem;

        }


        .chat-logo {

            width: 58px;

            height: 58px;

            font-size: 28px;

        }


        .chat-title {

            font-size: 24px;

        }


        .chat-subtitle {

            font-size: 13px;

        }


        [data-testid="stChatMessage"] {

            border-radius: 14px;

            font-size: 14px;

        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

# st.markdown(
#     """
#     <div class="chat-header">

#         <div class="chat-logo">
#             🤖
#         </div>

#         <div class="chat-title">
#             My ChatBot
#         </div>

#         <div class="chat-subtitle">
#             Your smart AI assistant powered by Groq
#         </div>

#     </div>
#     """,
#     unsafe_allow_html=True,
    
# =========================================================
# HEADER
# =========================================================

st.markdown(
"""
<div class="chat-header">
    <div class="chat-logo">
        🤖
    </div>
    <div class="chat-title">
        My ChatBot
    </div>
    <div class="chat-subtitle">
        Your smart AI assistant powered by Groq
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE API KEY
# =========================================================

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""


# =========================================================
# API KEY FORM
# =========================================================

if st.session_state["api_key"] == "":

    st.markdown(
        '<div class="section-title">🔐 Connect Your Groq API</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Masukkan Groq API Key untuk mulai menggunakan AI ChatBot."
    )

    col1, col2 = st.columns([4, 1])

    with col1:

        input_api_key = st.text_input(
            "API Key",
            type="password",
            label_visibility="collapsed",
            placeholder="Masukkan Groq API Key...",
        )

    with col2:

        is_api_key_submitted = st.button(
            "Connect",
            use_container_width=True,
        )

    if is_api_key_submitted:

        if input_api_key.strip():

            st.session_state["api_key"] = input_api_key

            st.rerun()

        else:

            st.warning(
                "Silakan masukkan API Key terlebih dahulu."
            )


if st.session_state["api_key"] == "":
    st.stop()


# =========================================================
# GROQ CLIENT
# =========================================================

client = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=st.session_state["api_key"],
)


# =========================================================
# CHAT HISTORY
# =========================================================

if "chat_history" not in st.session_state:

    st.session_state["chat_history"] = [

        SystemMessage(
            "You are a comedian, but smart. "
            "Always reply with a joke."
        )

    ]


chat_history = st.session_state["chat_history"]


# =========================================================
# CHAT HEADER + CLEAR BUTTON
# =========================================================

col1, col2 = st.columns([4, 1])

with col1:

    st.markdown(
        '<div class="section-title">💬 Conversation</div>',
        unsafe_allow_html=True,
    )


with col2:

    if st.button("Clear"):

        st.session_state["chat_history"] = [

            SystemMessage(
                "You are a comedian, but smart. "
                "Always reply with a joke."
            )

        ]

        st.rerun()


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for chat_msg in chat_history:

    if isinstance(chat_msg, HumanMessage):

        role = "user"

    elif isinstance(chat_msg, AIMessage):

        role = "assistant"

    else:

        continue

    with st.chat_message(role):

        st.markdown(chat_msg.content)


# =========================================================
# CHAT INPUT
# =========================================================

user_prompt = st.chat_input(
    "Ask anything..."
)


if not user_prompt:
    st.stop()


# =========================================================
# USER MESSAGE
# =========================================================

chat_history.append(
    HumanMessage(user_prompt)
)


with st.chat_message("user"):

    st.markdown(user_prompt)


# =========================================================
# AI RESPONSE
# =========================================================

with st.chat_message("assistant"):

    with st.spinner("AI sedang berpikir... 🤔"):

        response = client.invoke(
            chat_history
        )

        st.markdown(
            response.content
        )


# =========================================================
# SAVE RESPONSE
# =========================================================

chat_history.append(response)