import time
import uuid
import streamlit as st
from dotenv import load_dotenv

# MUST run before importing anything from src — web_tools reads env at import time.
load_dotenv()

from src.agent import DRA_agent
from src.utils import _coerce_text

st.set_page_config(
    page_title="Deep Research",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)


# ---------- Session state ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{role, answer, elapsed}]


# ---------- Theme CSS ----------
COMMON_CSS = """
<style>
/* Hide only the Deploy button and main menu — keep the sidebar toggle usable */
#MainMenu, footer, [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppDeployButton"],
.stDeployButton, [data-testid="stAppHeader"] button[kind="header"] {
    display: none !important;
    visibility: hidden !important;
}

/* Make sure the re-open-sidebar arrow stays visible when sidebar is collapsed */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    z-index: 999 !important;
}

/* Typography */
html, body, .stApp, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter",
                 Roboto, "Helvetica Neue", Arial, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* Constrain reading column — wider so closed-sidebar view doesn't feel empty */
[data-testid="stMainBlockContainer"] {
    max-width: 1000px !important;
    padding-top: 2.5rem !important;
    padding-bottom: 6rem !important;
}

/* Align the chat input with the content column */
[data-testid="stBottomBlockContainer"],
[data-testid="stBottom"] > div {
    max-width: 1000px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
</style>
"""

LIGHT_CSS = COMMON_CSS + """
<style>
.stApp, [data-testid="stAppViewContainer"] { background: #FBFBFD !important; }
[data-testid="stHeader"] { background: #FBFBFD !important; }
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #EAECEF !important;
}

/* Empty state */
.empty-state { text-align: center; margin: 2.5rem auto 1.5rem; }
.empty-state h1 {
    margin: 0; font-size: 1.75rem; font-weight: 600;
    color: #0F172A; letter-spacing: -0.02em;
}
.empty-state p {
    margin: 0.5rem auto 0; color: #475569; font-size: 0.95rem; max-width: 560px;
    line-height: 1.5;
}

/* Global body text contrast */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li { color: #1E293B !important; line-height: 1.6 !important; }
[data-testid="stChatMessage"] strong { color: #0F172A !important; }

/* Captions in sidebar */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #64748B !important; }

/* Chat bubbles — clean, no shadow */
[data-testid="stChatMessage"] {
    background: transparent !important; border: none !important;
    padding: 0.25rem 0 !important; box-shadow: none !important;
    margin-bottom: 0.5rem !important;
    gap: 0.75rem !important;
}
[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
    background: #FFFFFF !important; border: 1px solid #EAECEF !important;
    border-radius: 12px !important; padding: 14px 18px !important;
}
/* Pad heading/list spacing inside answers */
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 { margin-top: 1em !important; margin-bottom: 0.4em !important; }
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol { margin: 0.4em 0 0.6em !important; }

/* Sticky bottom — kill all wrappers so the input looks elevated, not boxed */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stBottomBlockContainer"] > div,
[data-testid="stBottomBlockContainer"] > div > div,
div[class*="stBottom"], div[class*="BottomBlock"],
section.main > footer, .stApp > footer {
    background: #FBFBFD !important;
    background-color: #FBFBFD !important;
    border: none !important;
    box-shadow: none !important;
}

/* Chat input — full pill shape, compact height */
[data-testid="stChatInput"] {
    border: 1px solid #D1D5DB !important;
    border-radius: 9999px !important;
    background: #FFFFFF !important;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.06),
                0 1px 3px rgba(15, 23, 42, 0.04) !important;
    padding: 4px 4px 4px 18px !important;
    overflow: hidden !important;
}
/* Inner wrappers transparent so they don't paint past the pill */
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] textarea {
    padding: 4px 0 !important;
    min-height: 24px !important;
    max-height: 140px !important;
    line-height: 1.4 !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.18),
                0 0 0 3px rgba(99, 102, 241, 0.08) !important;
}
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    background: #FFFFFF !important;
    border: none !important;
}
[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important; color: #0F172A !important;
    border: none !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #94A3B8 !important; }

/* Send button — circular indigo with an injected up-arrow icon (light). */
[data-testid="stChatInput"] button {
    background: #4F46E5 !important;
    background-color: #4F46E5 !important;
    background-image: none !important;
    border: none !important;
    border-radius: 50% !important;
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    min-height: 34px !important;
    padding: 0 !important;
    margin: 0 !important;
    opacity: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: background-color 0.15s ease !important;
}
[data-testid="stChatInput"] button:hover:not([disabled]) {
    background: #4338CA !important;
    background-color: #4338CA !important;
}
[data-testid="stChatInput"] button[disabled] {
    background: #E2E8F0 !important;
    background-color: #E2E8F0 !important;
    cursor: not-allowed !important;
}
/* Hide Streamlit's built-in icon (it renders as a square in 1.56). */
[data-testid="stChatInput"] button svg { display: none !important; }
/* Inject our own up-arrow via a white-colored CSS mask. */
[data-testid="stChatInput"] button::after {
    content: "" !important;
    display: block !important;
    width: 18px !important;
    height: 18px !important;
    background-color: #FFFFFF !important;
    -webkit-mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M12 19V5'/><path d='m5 12 7-7 7 7'/></svg>") no-repeat center / 18px 18px !important;
    mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M12 19V5'/><path d='m5 12 7-7 7 7'/></svg>") no-repeat center / 18px 18px !important;
}
[data-testid="stChatInput"] button[disabled]::after {
    background-color: #94A3B8 !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF !important; color: #0F172A !important;
    border: 1px solid #EAECEF !important; border-radius: 10px !important;
    font-weight: 500 !important; transition: all 0.15s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #6366F1 !important; color: #4338CA !important;
}

/* Brand mark */
.brand { display: flex; align-items: center; gap: 12px; margin: 0.25rem 0 0.5rem; }
.brand-mark {
    width: 30px; height: 30px; border-radius: 8px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 14px; letter-spacing: -0.02em;
}
.brand-name { font-size: 1rem; font-weight: 600; color: #0F172A; letter-spacing: -0.01em; line-height: 1.2; }
.brand-tag { font-size: 0.7rem; color: #94A3B8; letter-spacing: 0.08em; text-transform: uppercase; }

/* Sidebar section labels */
.sidebar-label {
    font-size: 0.72rem; color: #94A3B8;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin: 1rem 0 0.5rem;
}

/* Inline code */
code {
    background: #F1F5F9 !important; color: #4338CA !important;
    padding: 2px 6px !important; border-radius: 4px !important;
    font-size: 0.85em !important;
}

/* Links inside answers */
[data-testid="stChatMessage"] a { color: #4F46E5 !important; text-decoration: none; }
[data-testid="stChatMessage"] a:hover { text-decoration: underline; }
</style>
"""

DARK_CSS = COMMON_CSS + """
<style>
html, body { background: #0B0F1A !important; }
.stApp, [data-testid="stAppViewContainer"] { background: #0B0F1A !important; color: #E5E7EB !important; }
[data-testid="stHeader"] { background: #0B0F1A !important; }
[data-testid="stMain"], [data-testid="stMainBlockContainer"] { background: #0B0F1A !important; }
[data-testid="stSidebar"] {
    background: #0F172A !important;
    border-right: 1px solid #1E293B !important;
}

[data-testid="stMarkdownContainer"], .stMarkdown,
p, li, h1, h2, h3, h4, h5, h6, label, span { color: #E5E7EB !important; }
small, [data-testid="stCaptionContainer"] { color: #94A3B8 !important; }

.empty-state { text-align: center; margin: 2.5rem auto 1.5rem; }
.empty-state h1 {
    margin: 0; font-size: 1.75rem; font-weight: 600;
    color: #F3F4F6 !important; letter-spacing: -0.02em;
}
.empty-state p {
    margin: 0.5rem auto 0; color: #94A3B8 !important;
    font-size: 0.95rem; max-width: 540px;
}

[data-testid="stChatMessage"] {
    background: transparent !important; border: none !important;
    padding: 0.25rem 0 !important; box-shadow: none !important;
    margin-bottom: 0.5rem !important;
    gap: 0.75rem !important;
}
[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
    background: #111827 !important; border: 1px solid #1E293B !important;
    border-radius: 12px !important; padding: 14px 18px !important;
}
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 { margin-top: 1em !important; margin-bottom: 0.4em !important; }
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol { margin: 0.4em 0 0.6em !important; }

/* Sticky bottom — force every wrapper to page bg so no white leaks through */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stBottomBlockContainer"] > div,
[data-testid="stBottomBlockContainer"] > div > div,
div[class*="stBottom"], div[class*="BottomBlock"],
section.main > footer, .stApp > footer {
    background: #0B0F1A !important;
    background-color: #0B0F1A !important;
    border: none !important;
    box-shadow: none !important;
}

/* Chat input — full pill shape, dark fill, compact height */
[data-testid="stChatInput"] {
    border: 1px solid #334155 !important;
    border-radius: 9999px !important;
    background: #1E293B !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35),
                0 1px 3px rgba(0, 0, 0, 0.2) !important;
    padding: 4px 4px 4px 18px !important;
    overflow: hidden !important;
}
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] textarea {
    padding: 4px 0 !important;
    min-height: 24px !important;
    max-height: 140px !important;
    line-height: 1.4 !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 4px 24px rgba(99, 102, 241, 0.25),
                0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    background: #1E293B !important;
    border: none !important;
}
[data-testid="stChatInput"] textarea {
    background: #1E293B !important; color: #F3F4F6 !important; border: none !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #94A3B8 !important; }

/* Send button — circular indigo with injected up-arrow (dark). */
[data-testid="stChatInput"] button {
    background: #6366F1 !important;
    background-color: #6366F1 !important;
    background-image: none !important;
    border: none !important;
    border-radius: 50% !important;
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    min-height: 34px !important;
    padding: 0 !important;
    margin: 0 !important;
    opacity: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: background-color 0.15s ease !important;
}
[data-testid="stChatInput"] button:hover:not([disabled]) {
    background: #818CF8 !important;
    background-color: #818CF8 !important;
}
[data-testid="stChatInput"] button[disabled] {
    background: #334155 !important;
    background-color: #334155 !important;
    cursor: not-allowed !important;
}
[data-testid="stChatInput"] button svg { display: none !important; }
[data-testid="stChatInput"] button::after {
    content: "" !important;
    display: block !important;
    width: 18px !important;
    height: 18px !important;
    background-color: #FFFFFF !important;
    -webkit-mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M12 19V5'/><path d='m5 12 7-7 7 7'/></svg>") no-repeat center / 18px 18px !important;
    mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M12 19V5'/><path d='m5 12 7-7 7 7'/></svg>") no-repeat center / 18px 18px !important;
}
[data-testid="stChatInput"] button[disabled]::after {
    background-color: #64748B !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: #111827 !important; color: #E5E7EB !important;
    border: 1px solid #1E293B !important; border-radius: 10px !important;
    font-weight: 500 !important; transition: all 0.15s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #6366F1 !important; color: #A5B4FC !important;
}

.brand { display: flex; align-items: center; gap: 12px; margin: 0.25rem 0 0.5rem; }
.brand-mark {
    width: 30px; height: 30px; border-radius: 8px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 14px; letter-spacing: -0.02em;
}
.brand-name { font-size: 1rem; font-weight: 600; color: #F3F4F6 !important; letter-spacing: -0.01em; line-height: 1.2; }
.brand-tag { font-size: 0.7rem; color: #64748B !important; letter-spacing: 0.08em; text-transform: uppercase; }

.sidebar-label {
    font-size: 0.72rem; color: #64748B;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin: 1rem 0 0.5rem;
}

code {
    background: #1E293B !important; color: #C7D2FE !important;
    padding: 2px 6px !important; border-radius: 4px !important;
    font-size: 0.85em !important;
}

[data-testid="stChatMessage"] a { color: #A5B4FC !important; text-decoration: none; }
[data-testid="stChatMessage"] a:hover { text-decoration: underline; }
</style>
"""

st.markdown(DARK_CSS if st.session_state.dark_mode else LIGHT_CSS, unsafe_allow_html=True)


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">DR</div>
            <div>
                <div class="brand-name">Deep Research</div>
                <div class="brand-tag">Research assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    if st.button("＋  New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.markdown('<div class="sidebar-label">Appearance</div>', unsafe_allow_html=True)
    new_dark = st.toggle("Dark mode", value=st.session_state.dark_mode, key="theme_toggle")
    if new_dark != st.session_state.dark_mode:
        st.session_state.dark_mode = new_dark
        st.rerun()

    # Bottom session info
    st.markdown('<div style="height: 1.5rem"></div>', unsafe_allow_html=True)
    st.divider()
    st.caption(f"Thread · `{st.session_state.thread_id[:8]}`")
    msg_count = len(st.session_state.messages)
    st.caption(f"{msg_count} message{'s' if msg_count != 1 else ''}")


@st.cache_resource
def get_agent():
    return DRA_agent


agent = get_agent()


# ---------- Streaming sink ----------
class StreamSink:
    def __init__(self, answer_box):
        self.answer_box = answer_box
        self.answer_text = ""
        self._in_think_tag = False

    def feed(self, content):
        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text":
                    self._feed_string(_coerce_text(block.get("text")))
        else:
            self._feed_string(_coerce_text(content))

    def _feed_string(self, s: str):
        # Strip any stray <think>...</think> content silently — we don't surface it.
        while s:
            if self._in_think_tag:
                end = s.find("</think>")
                if end == -1:
                    return
                self._in_think_tag = False
                s = s[end + len("</think>"):]
            else:
                start = s.find("<think>")
                if start == -1:
                    self._add_answer(s)
                    return
                self._add_answer(s[:start])
                self._in_think_tag = True
                s = s[start + len("<think>"):]

    def _add_answer(self, s: str):
        if not s:
            return
        self.answer_text += s
        self.answer_box.markdown(self.answer_text)


def build_history() -> list[dict]:
    out = []
    for m in st.session_state.messages:
        content = (m.get("answer") or "").strip()
        if not content:
            continue
        out.append({"role": m["role"], "content": content})
    return out


def stream_answer(messages: list[dict], answer_box) -> str:
    sink = StreamSink(answer_box)

    for chunk in agent.stream(
        {"messages": messages},
        stream_mode=["messages"],
        subgraphs=True,
        version="v2",
    ):
        if chunk["type"] != "messages":
            continue

        token, _meta = chunk["data"]

        if getattr(token, "type", None) == "tool":
            continue
        if getattr(token, "tool_call_chunks", None):
            continue

        if getattr(token, "content", None):
            sink.feed(token.content)

    return sink.answer_text.strip()


# ---------- Empty state ----------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="empty-state">
            <h1>What do you want to research?</h1>
            <p>Ask a question — the agent searches the web, arXiv, and recent news, then synthesizes a cited answer.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- New message ----------
# Append any new user input BEFORE rendering history so it shows up in order.
query = st.chat_input("Ask a research question…")
if query:
    st.session_state.messages.append({"role": "user", "answer": query})


# ---------- Chat history ----------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m.get("answer", ""))


# ---------- Run agent if the last message is still awaiting a reply ----------
# Covers both a brand-new query AND an interrupted stream (e.g. user toggled
# dark mode mid-research, which forces a rerun and kills the in-flight stream).
needs_reply = (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
)

if needs_reply:
    history = [
        {"role": m["role"], "content": (m.get("answer") or "").strip()}
        for m in st.session_state.messages
        if (m.get("answer") or "").strip()
    ]

    with st.chat_message("assistant"):
        answer_box = st.empty()
        t0 = time.perf_counter()
        try:
            with st.spinner("Researching…"):
                answer = stream_answer(history, answer_box)
        except Exception as e:
            # Record a failed reply so we don't loop on the same orphaned user message.
            st.session_state.messages.append({
                "role": "assistant",
                "answer": f"_Error: {e}_",
                "elapsed": time.perf_counter() - t0,
            })
            st.error(str(e))
            st.stop()

        elapsed = time.perf_counter() - t0
        if not answer:
            answer_box.markdown("_(empty response)_")

        st.session_state.messages.append({
            "role": "assistant",
            "answer": answer,
            "elapsed": elapsed,
        })
