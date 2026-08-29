"""
Sentinela — Adaptive AI Customer Support Agent
Streamlit Frontend (Variation 1 & 2 compatible)

Entry point: streamlit run app.py
"""

import streamlit as st
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sentinela | AI Support Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Global ──────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Main background ─────────────────────────────────── */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        color: #e8eaf6;
    }

    /* ── Sidebar ─────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        border-right: 1px solid #30363d;
    }

    /* ── Chat bubbles ────────────────────────────────────── */
    .user-bubble {
        background: linear-gradient(135deg, #1e3a5f, #2d5a8e);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
        margin: 6px 0;
        max-width: 75%;
        margin-left: auto;
        color: #e8eaf6;
        font-size: 0.92rem;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .agent-bubble {
        background: linear-gradient(135deg, #1a1f2e, #252d3d);
        border-left: 3px solid #4f8ef7;
        border-radius: 4px 18px 18px 18px;
        padding: 14px 16px;
        margin: 6px 0;
        max-width: 80%;
        color: #cdd5e0;
        font-size: 0.92rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .escalation-bubble {
        background: linear-gradient(135deg, #3d1f1f, #5a2d2d);
        border-left: 3px solid #ff6b6b;
        border-radius: 4px 18px 18px 18px;
        padding: 14px 16px;
        margin: 6px 0;
        max-width: 80%;
        color: #ffd5d5;
        font-size: 0.92rem;
    }

    /* ── Intent badge ────────────────────────────────────── */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        margin-bottom: 6px;
    }
    .badge-order    { background: #0d3349; color: #4fc3f7; border: 1px solid #4fc3f7; }
    .badge-return   { background: #1b2a1b; color: #81c784; border: 1px solid #81c784; }
    .badge-shipping { background: #2a2010; color: #ffb74d; border: 1px solid #ffb74d; }
    .badge-escalate { background: #3d1010; color: #ef5350; border: 1px solid #ef5350; }
    .badge-scope    { background: #1e1e2e; color: #9575cd; border: 1px solid #9575cd; }

    /* ── Reasoning trace expander ────────────────────────── */
    .trace-box {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px 14px;
        font-family: 'Courier New', monospace;
        font-size: 0.78rem;
        color: #8b949e;
        margin-top: 8px;
    }

    /* ── Citation pill ───────────────────────────────────── */
    .citation {
        display: inline-block;
        background: #1e2d40;
        color: #64b5f6;
        border: 1px solid #1a5276;
        border-radius: 10px;
        padding: 1px 8px;
        font-size: 0.72rem;
        margin: 2px 2px;
    }

    /* ── Input area ──────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: #1a1f2e !important;
        color: #e8eaf6 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }

    /* ── Buttons ─────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #1565c0, #1976d2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976d2, #2196f3);
        box-shadow: 0 0 12px rgba(33, 150, 243, 0.4);
    }

    /* ── Metric cards ────────────────────────────────────── */
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e, #252d3d);
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
    }

    /* ── Journey quick-start cards ───────────────────────── */
    .journey-card {
        background: linear-gradient(135deg, #1a1f2e, #1e2740);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 14px;
        margin: 6px 0;
        cursor: pointer;
        transition: border-color 0.2s;
    }
    .journey-card:hover { border-color: #4f8ef7; }

    /* ── Hide Streamlit branding ─────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state init ─────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "messages": [],           # list of {role, content, intent, trace, citations, escalated}
        "order_id": "",
        "customer_email": "",
        "session_resolved": 0,
        "session_escalated": 0,
        "session_queries": 0,
        "show_trace": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ── Mock agent call (stub — replace with LangChain / LangGraph backend) ────────
def call_agent(user_query: str, order_id: str) -> dict:
    """
    Stub agent response. Replace this function body with your actual
    LangChain AgentExecutor (Variation 1) or LangGraph graph.invoke() (Variation 2) call.

    Expected return schema:
    {
        "intent":    str,          # order_status | return_refund | shipping_dispute | escalation | out_of_scope
        "response":  str,          # final customer-facing message
        "citations": list[str],    # e.g. ["return_policy.md §3", "shipping_sla.md §1"]
        "trace":     list[str],    # ReAct reasoning steps for transparency
        "escalated": bool,         # True if HITL gate was triggered
        "escalation_ticket": str,  # formatted ticket string (only if escalated=True)
    }
    """
    q = user_query.lower()

    # ── UJ1: Order Status ──────────────────────────────────────────────────────
    if any(kw in q for kw in ["where is", "track", "status", "order", "arrived", "delivery", "late"]):
        oid = order_id or "#12345"
        return {
            "intent": "order_status",
            "response": (
                f"📦 **Order {oid}** is currently **In Transit** via FedEx.\n\n"
                "- **Estimated Delivery:** Tomorrow by 8 PM\n"
                "- **Last Scan:** Distribution centre, 6 hours ago\n\n"
                "Our standard delivery window is **5–7 business days**. "
                "You're currently on day 4, well within the expected range. "
                "If it doesn't arrive by tomorrow evening, please reach out and we'll open a carrier investigation."
            ),
            "citations": ["shipping_sla.md §1 — Standard Delivery Window"],
            "trace": [
                "Thought: User is asking about order status. Need order ID.",
                f"Action: order_status_tool({oid})",
                "Observation: status=In Transit, carrier=FedEx, ETA=tomorrow",
                "Action: rag_policy_tool('standard delivery timeline')",
                "Observation: '5–7 business days from dispatch date'",
                "Thought: Order is on day 4, within SLA. Safe to report ETA without escalation.",
                "Final Answer: Compose status response with ETA and policy grounding.",
            ],
            "escalated": False,
            "escalation_ticket": "",
        }

    # ── UJ2: Return / Refund ───────────────────────────────────────────────────
    if any(kw in q for kw in ["return", "refund", "send back", "exchange", "policy"]):
        return {
            "intent": "return_refund",
            "response": (
                "✅ **Good news — your item is eligible for a return.**\n\n"
                "- **Return Window:** 30 days from purchase (you're on day 7)\n"
                "- **Condition:** Item must be unworn / unopened with original packaging\n"
                "- **Refund Amount:** $89.99 (original payment method)\n\n"
                "⚠️ Because this involves a refund of **$89.99**, I'm flagging this for a "
                "support agent to confirm and process. You'll receive a confirmation email within **24 hours**."
            ),
            "citations": ["return_policy.md §2 — 30-Day Window", "refund_guidelines.md §4 — Processing Time"],
            "trace": [
                "Thought: User wants to return an item. Need order details.",
                "Action: order_status_tool(last_order_for_customer)",
                "Observation: order #54321, purchase_date=Apr 11, item=shoes, amount=$89.99",
                "Action: rag_policy_tool('return eligibility shoes')",
                "Observation: '30-day window; must be unworn with original tags'",
                "Action: return_eligibility_tool(order_id=#54321, reason='change of mind')",
                "Observation: eligible=True, days_since_purchase=7, refund_amount=$89.99",
                "Thought: Refund $89.99 exceeds $0 but triggers HITL check (threshold $50).",
                "Guardrail: financial_flag=True → route to escalation node.",
                "Final Answer: Confirm eligibility, inform HITL gate, set 24hr expectation.",
            ],
            "escalated": True,
            "escalation_ticket": (
                "**Escalation Ticket — Return Request**\n"
                "- Order: #54321 | Customer: session user\n"
                "- Item: Shoes | Purchase Date: Apr 11\n"
                "- Eligibility: ✅ Confirmed (day 7 of 30)\n"
                "- Refund Amount: $89.99\n"
                "- Action Required: Agent to approve & process refund\n"
                f"- Raised: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            ),
        }

    # ── UJ3: Shipping Dispute ──────────────────────────────────────────────────
    if any(kw in q for kw in ["delivered but", "not received", "missing", "wrong item", "damaged", "lost", "dispute"]):
        return {
            "intent": "shipping_dispute",
            "response": (
                "🔍 **We're sorry to hear that.** Our records show your package was marked "
                "**Delivered on April 17 at 2:32 PM**.\n\n"
                "Here's what I recommend:\n"
                "1. Check with neighbours or a safe-drop location\n"
                "2. If still missing, you can file a **carrier claim within 7 days** of the delivery date\n\n"
                "Would you like me to escalate this to our support team to open a carrier investigation on your behalf?"
            ),
            "citations": ["shipping_sla.md §3 — Lost Package Claim Window"],
            "trace": [
                "Thought: User reports non-receipt of delivered package.",
                "Action: order_status_tool(last_order_for_customer)",
                "Observation: status=Delivered, timestamp=Apr 17 14:32, carrier=FedEx",
                "Action: rag_policy_tool('lost package claim process')",
                "Observation: 'File claim within 7 days of marked delivery date'",
                "Thought: Delivery was yesterday — day 1 of 7-day claim window. Can advise.",
                "Thought: No financial action needed yet. Offer escalation as next step.",
                "Final Answer: Inform delivery timestamp, explain claim window, offer escalation.",
            ],
            "escalated": False,
            "escalation_ticket": "",
        }

    # ── Out of scope ───────────────────────────────────────────────────────────
    return {
        "intent": "out_of_scope",
        "response": (
            "I'm specialised in order tracking, returns, refunds, and shipping issues. "
            "I'm not able to help with that particular request, but I can connect you with "
            "the right team. Is there anything order-related I can help you with?"
        ),
        "citations": [],
        "trace": ["Thought: Query is outside support domain.", "Final Answer: Politely redirect."],
        "escalated": False,
        "escalation_ticket": "",
    }


# ── Intent badge HTML ──────────────────────────────────────────────────────────
_BADGE_MAP = {
    "order_status":     ("badge-order",    "📦 Order Status"),
    "return_refund":    ("badge-return",   "↩️ Return & Refund"),
    "shipping_dispute": ("badge-shipping", "🚚 Shipping Dispute"),
    "escalation":       ("badge-escalate", "🚨 Escalated"),
    "out_of_scope":     ("badge-scope",    "🔒 Out of Scope"),
}

def _badge(intent: str) -> str:
    cls, label = _BADGE_MAP.get(intent, ("badge-scope", intent))
    return f'<span class="badge {cls}">{label}</span>'


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🛡️ Sentinela")
    st.markdown(
        "<p style='color:#8b949e;font-size:0.8rem;margin-top:-10px'>"
        "Adaptive AI Customer Support Agent</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Customer context ───────────────────────────────────────────────────────
    st.markdown("### 🧑 Customer Context")
    st.session_state.order_id = st.text_input(
        "Order ID (optional)",
        value=st.session_state.order_id,
        placeholder="#12345",
        key="order_id_input",
    )
    st.session_state.customer_email = st.text_input(
        "Email (optional)",
        value=st.session_state.customer_email,
        placeholder="you@example.com",
        key="email_input",
    )
    st.divider()

    # ── Session stats ──────────────────────────────────────────────────────────
    st.markdown("### 📊 Session Stats")
    col_a, col_b = st.columns(2)
    col_a.metric("Queries", st.session_state.session_queries)
    col_b.metric("Escalated", st.session_state.session_escalated)
    resolved_pct = (
        int((st.session_state.session_resolved / st.session_state.session_queries) * 100)
        if st.session_state.session_queries > 0
        else 0
    )
    st.progress(resolved_pct / 100, text=f"Containment Rate: {resolved_pct}%")
    st.divider()

    # ── Quick-start user journey buttons ──────────────────────────────────────
    st.markdown("### ⚡ Quick-Start Journeys")
    st.caption("Click to pre-fill a sample query")

    if st.button("📦 UJ1 — Track My Order", use_container_width=True):
        st.session_state["_prefill"] = "Where is my order? It hasn't arrived yet."
    if st.button("↩️  UJ2 — Return & Refund", use_container_width=True):
        st.session_state["_prefill"] = "I want to return the shoes I ordered last week and get a refund."
    if st.button("🚚 UJ3 — Shipping Dispute", use_container_width=True):
        st.session_state["_prefill"] = "My package says delivered but I never received it."
    st.divider()

    # ── Show reasoning trace toggle ────────────────────────────────────────────
    st.markdown("### 🔬 Dev Options")
    st.session_state.show_trace = st.toggle(
        "Show Agent Reasoning Trace", value=st.session_state.show_trace
    )

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_queries = 0
        st.session_state.session_resolved = 0
        st.session_state.session_escalated = 0
        st.rerun()

    st.divider()
    st.markdown(
        "<p style='color:#484f58;font-size:0.72rem;text-align:center'>"
        "Sentinela v1.0 · Capstone UC3<br>"
        "LangChain ReAct + RAG + ChromaDB</p>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ══════════════════════════════════════════════════════════════════════════════
# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center;padding:20px 0 10px 0;">
        <h1 style="font-size:2rem;font-weight:700;color:#e8eaf6;">
            🛡️ Sentinela
        </h1>
        <p style="color:#8b949e;font-size:0.9rem;margin-top:-8px;">
            Adaptive AI Customer Support · Order · Returns · Shipping
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Intent coverage strip ──────────────────────────────────────────────────────
ic1, ic2, ic3 = st.columns(3)
with ic1:
    st.markdown(
        '<div class="metric-card"><span style="font-size:1.4rem">📦</span>'
        '<br><b style="font-size:0.8rem;color:#4fc3f7">UJ1 · Order Tracking</b>'
        '<br><span style="font-size:0.72rem;color:#8b949e">Live API lookups + SLA grounding</span></div>',
        unsafe_allow_html=True,
    )
with ic2:
    st.markdown(
        '<div class="metric-card"><span style="font-size:1.4rem">↩️</span>'
        '<br><b style="font-size:0.8rem;color:#81c784">UJ2 · Returns & Refunds</b>'
        '<br><span style="font-size:0.72rem;color:#8b949e">RAG policy + HITL guardrail</span></div>',
        unsafe_allow_html=True,
    )
with ic3:
    st.markdown(
        '<div class="metric-card"><span style="font-size:1.4rem">🚚</span>'
        '<br><b style="font-size:0.8rem;color:#ffb74d">UJ3 · Shipping Disputes</b>'
        '<br><span style="font-size:0.72rem;color:#8b949e">Claim window + escalation path</span></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Chat history ───────────────────────────────────────────────────────────────
chat_area = st.container()

with chat_area:
    if not st.session_state.messages:
        st.markdown(
            """
            <div style="text-align:center;padding:40px 20px;color:#484f58;">
                <p style="font-size:2rem">💬</p>
                <p style="font-size:0.9rem">
                    Hello! I'm Sentinela, your AI support agent.<br>
                    Ask me about <b style="color:#4fc3f7">order tracking</b>, 
                    <b style="color:#81c784">returns & refunds</b>, or 
                    <b style="color:#ffb74d">shipping issues</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-bubble">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            intent = msg.get("intent", "")
            escalated = msg.get("escalated", False)
            bubble_cls = "escalation-bubble" if escalated else "agent-bubble"

            st.markdown(
                f'{_badge(intent)}<br>'
                f'<div class="{bubble_cls}">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )

            # ── Citations ──────────────────────────────────────────────────────
            if msg.get("citations"):
                pills = "".join(
                    f'<span class="citation">📄 {c}</span>' for c in msg["citations"]
                )
                st.markdown(
                    f'<div style="margin:4px 0 8px 0">{pills}</div>',
                    unsafe_allow_html=True,
                )

            # ── Escalation ticket ──────────────────────────────────────────────
            if escalated and msg.get("escalation_ticket"):
                with st.expander("🚨 View Escalation Ticket (Human Agent)", expanded=False):
                    st.markdown(msg["escalation_ticket"])

            # ── Reasoning trace ────────────────────────────────────────────────
            if st.session_state.show_trace and msg.get("trace"):
                with st.expander("🔬 Agent Reasoning Trace", expanded=False):
                    trace_html = "<br>".join(
                        f'<span style="color:#4f8ef7">▶</span> {step}'
                        for step in msg["trace"]
                    )
                    st.markdown(
                        f'<div class="trace-box">{trace_html}</div>',
                        unsafe_allow_html=True,
                    )

# ── Input row ──────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

prefill_value = st.session_state.pop("_prefill", "")

with st.form("chat_form", clear_on_submit=True):
    col_input, col_send = st.columns([8, 1])
    with col_input:
        user_input = st.text_input(
            label="Message",
            value=prefill_value,
            placeholder="e.g. Where is my order? / I want to return an item...",
            label_visibility="collapsed",
            key="user_input_field",
        )
    with col_send:
        submitted = st.form_submit_button("Send ➤", use_container_width=True)

if submitted and user_input.strip():
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    st.session_state.session_queries += 1

    # Call agent
    with st.spinner("Sentinela is thinking..."):
        result = call_agent(user_input.strip(), st.session_state.order_id)

    # Track escalations vs resolved
    if result["escalated"]:
        st.session_state.session_escalated += 1
    else:
        st.session_state.session_resolved += 1

    # Append agent message
    st.session_state.messages.append(
        {
            "role": "agent",
            "content": result["response"],
            "intent": result["intent"],
            "citations": result["citations"],
            "trace": result["trace"],
            "escalated": result["escalated"],
            "escalation_ticket": result.get("escalation_ticket", ""),
        }
    )

    st.rerun()
