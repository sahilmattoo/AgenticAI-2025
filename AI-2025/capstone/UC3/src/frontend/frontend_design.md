# Sentinela — Frontend Design Specification

**File:** `src/frontend/app.py`  
**Framework:** Streamlit  
**Version:** 1.0  
**Last Updated:** 2026-04-18

---

## 1. Purpose

This document captures the design decisions, layout specification, component inventory, UX rationale, and future upgrade path for the Sentinela AI Customer Support Agent's Streamlit frontend. It is intended to be a living reference for the project team throughout the capstone build.

---

## 2. Design Goals

| Goal | Description |
|------|-------------|
| **User Journey Coverage** | The UI must surface all three user journeys (UJ1, UJ2, UJ3) naturally — without requiring the customer to know intent categories |
| **Transparency** | Agent reasoning must be viewable (trace expander) to support evaluation and trust |
| **Safety Visibility** | Escalation events must be visually distinct and surfaced to the human agent with a structured ticket |
| **Simplicity First** | Chatbot interface is familiar to e-commerce customers; no onboarding required |
| **Eval-Friendly** | Session stats, reasoning traces, and citation pills make it easy to score agent quality during evaluation |

---

## 3. Technology Choice

**Streamlit** was selected as the primary UI framework for the following reasons:

- Zero frontend infrastructure — runs as a Python script alongside the agent backend
- Native Python data types — agent responses (dicts, lists) render directly with no serialisation layer
- `st.form` + `st.rerun()` provides stateful chat without a separate state server
- Compatible with both Variation 1 (LangChain) and Variation 2 (LangGraph) backends — only `call_agent()` needs to change
- Rapid iteration matches the capstone's two-variation evaluation approach

> **Future path:** If the project requires a persistent, multi-user deployment, migrate the backend to FastAPI and replace this Streamlit app with a Next.js or React frontend consuming the REST API.

---

## 4. Layout Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  SIDEBAR (260px fixed)         │  MAIN AREA (remaining width)   │
│                                │                                 │
│  🛡️ Sentinela header           │  🛡️ Sentinela + tagline         │
│  ─────────────────────         │                                 │
│  🧑 Customer Context           │  ┌──────┐ ┌──────┐ ┌──────┐   │
│     Order ID (input)           │  │ UJ1  │ │ UJ2  │ │ UJ3  │   │
│     Email (input)              │  │ card │ │ card │ │ card │   │
│  ─────────────────────         │  └──────┘ └──────┘ └──────┘   │
│  📊 Session Stats              │                                 │
│     Queries metric             │  ── Chat history ──────────── │
│     Escalated metric           │  [user bubble]                  │
│     Containment progress       │  [intent badge]                 │
│  ─────────────────────         │  [agent bubble]                 │
│  ⚡ Quick-Start Journeys       │    [citation pills]             │
│     UJ1 button                 │    [escalation ticket expander] │
│     UJ2 button                 │    [reasoning trace expander]   │
│     UJ3 button                 │  [user bubble]                  │
│  ─────────────────────         │  ...                            │
│  🔬 Dev Options                │                                 │
│     Trace toggle               │  ── Input row ───────────────  │
│     Clear conversation         │  [ text input ........... ] [➤] │
│  ─────────────────────         │                                 │
│  version / stack footer        │                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Component Inventory

### 5.1 Sidebar Components

| Component | ID / Key | Type | Purpose |
|-----------|----------|------|---------|
| Order ID input | `order_id_input` | `st.text_input` | Optional pre-fill for API tool lookups |
| Email input | `email_input` | `st.text_input` | Optional session context (not logged/persisted) |
| Queries metric | — | `st.metric` | Session query count |
| Escalated metric | — | `st.metric` | Count of HITL-triggered responses |
| Containment progress bar | — | `st.progress` | `resolved / total` as a percentage |
| UJ1 quick-start button | — | `st.button` | Pre-fills input with UJ1 sample query |
| UJ2 quick-start button | — | `st.button` | Pre-fills input with UJ2 sample query |
| UJ3 quick-start button | — | `st.button` | Pre-fills input with UJ3 sample query |
| Reasoning trace toggle | — | `st.toggle` | Shows/hides agent trace expanders in chat |
| Clear conversation | — | `st.button` | Resets session state and chat history |

### 5.2 Main Area Components

| Component | Type | Purpose |
|-----------|------|---------|
| UJ intent strip (3 cards) | Custom HTML + `st.columns` | Visual overview of supported journeys |
| Chat history container | `st.container` + HTML bubbles | Scrollable conversation display |
| User bubble | Custom HTML div `.user-bubble` | Right-aligned blue gradient bubble |
| Agent bubble | Custom HTML div `.agent-bubble` | Left-aligned dark bubble with blue left border |
| Escalation bubble | Custom HTML div `.escalation-bubble` | Red-tinted bubble for HITL responses |
| Intent badge | Custom HTML `<span class='badge'>` | Colour-coded label per response |
| Citation pills | Custom HTML `<span class='citation'>` | Inline policy document references |
| Escalation ticket expander | `st.expander` | Collapsible structured ticket for human agent |
| Reasoning trace expander | `st.expander` | Collapsible ReAct step-by-step trace |
| Chat input form | `st.form('chat_form')` | Text input + send button; clears on submit |

---

## 6. User Journey → UI Flow Mapping

### UJ1 — Order Status & Tracking

```
Customer types: "Where is my order?"
  ↓
[order_id_input] pre-fills API call (or agent asks clarifying question)
  ↓
Agent bubble: 📦 UJ1 badge + status message + ETA
  ↓
Citation pill: shipping_sla.md §1
  ↓
[Trace expander]: order_status_tool → rag_policy_tool → reasoning → response
```

**Key UI states:**
- No order ID → agent asks clarification (clarification_tool output displayed in bubble)
- Order found, within SLA → informational bubble, no escalation
- Order not found → graceful error bubble + escalation offer button (future)

---

### UJ2 — Return & Refund Initiation

```
Customer types: "I want to return my shoes"
  ↓
Agent bubble: ↩️ UJ2 badge + eligibility verdict + refund amount
  ↓
Red escalation bubble: HITL gate triggered (refund > $50)
  ↓
Citation pills: return_policy.md + refund_guidelines.md
  ↓
[Escalation Ticket expander]: structured ticket visible in UI
  ↓
[Trace expander]: order lookup → rag → eligibility check → guardrail → escalation
```

**Key UI states:**
- Within window + below threshold → green eligibility, no escalation
- Within window + above threshold → escalation bubble + ticket expander (HITL gate)
- Outside 30-day window → refusal bubble + policy citation

---

### UJ3 — Shipping Dispute Resolution

```
Customer types: "My package says delivered but I never got it"
  ↓
Agent bubble: 🚚 UJ3 badge + delivery timestamp + claim window guidance
  ↓
Citation pill: shipping_sla.md §3
  ↓
Optional: "Escalate to support team?" → [Escalate] button (future)
  ↓
[Trace expander]: order lookup → rag → reasoning → response
```

**Key UI states:**
- Within 7-day claim window → advisory bubble, escalation offer
- Outside claim window → policy refusal + redirect to team
- Wrong item → eligibility check for replacement + HITL gate

---

## 7. Visual Design System

### 7.1 Colour Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-deep` | `#0f0f1a` | App background gradient start |
| `--bg-mid` | `#1a1a2e` | App background gradient mid |
| `--bg-card` | `#1a1f2e` | Bubble / card backgrounds |
| `--border` | `#30363d` | Dividers, input borders, card borders |
| `--text-primary` | `#e8eaf6` | Main text |
| `--text-muted` | `#8b949e` | Subtitles, timestamps, captions |
| `--accent-blue` | `#4f8ef7` | Agent bubble border, UJ1, citations |
| `--accent-green` | `#81c784` | UJ2 / return journey |
| `--accent-amber` | `#ffb74d` | UJ3 / shipping journey |
| `--accent-red` | `#ff6b6b` | Escalation / HITL events |
| `--accent-purple` | `#9575cd` | Out-of-scope badge |

### 7.2 Typography

- **Font:** Inter (Google Fonts, loaded via CSS `@import`)
- **Body:** 0.92rem / line-height 1.5–1.6
- **Badges:** 0.72rem / weight 600 / letter-spacing 0.04em
- **Trace box:** `Courier New` monospace, 0.78rem

### 7.3 Intent Badge Colours

| Intent | Badge Class | Text Colour | Border |
|--------|-------------|-------------|--------|
| `order_status` | `.badge-order` | `#4fc3f7` (cyan) | cyan |
| `return_refund` | `.badge-return` | `#81c784` (green) | green |
| `shipping_dispute` | `.badge-shipping` | `#ffb74d` (amber) | amber |
| `escalation` | `.badge-escalate` | `#ef5350` (red) | red |
| `out_of_scope` | `.badge-scope` | `#9575cd` (purple) | purple |

---

## 8. Session State Schema

All state is stored in `st.session_state`. No data is persisted beyond the browser session.

```python
{
    "messages":          list[dict],   # chat history: {role, content, intent, trace, citations, escalated}
    "order_id":          str,          # from sidebar input
    "customer_email":    str,          # from sidebar input (never logged)
    "session_resolved":  int,          # count of non-escalated responses
    "session_escalated": int,          # count of HITL-triggered responses
    "session_queries":   int,          # total queries in session
    "show_trace":        bool,         # controls trace expander visibility
    "_prefill":          str,          # transient: quick-start button pre-fill value
}
```

> **PII Note:** `customer_email` and `order_id` exist only in `st.session_state` for the duration of the session. They are not written to disk, logs, or sent anywhere beyond the agent call stub.

---

## 9. Backend Integration Points

The frontend connects to the agent backend via a **single function call**: `call_agent(user_query, order_id)`.

To switch from the mock stub to the real backend:

### Variation 1 — LangChain AgentExecutor

```python
# In app.py, replace call_agent() with:
from langchain.agents import AgentExecutor

def call_agent(user_query: str, order_id: str) -> dict:
    response = agent_executor.invoke({"input": user_query, "order_id": order_id})
    return parse_agent_output(response)   # map to {intent, response, citations, trace, escalated}
```

### Variation 2 — LangGraph StateGraph

```python
# In app.py, replace call_agent() with:
from backend.graph import sentinela_graph

def call_agent(user_query: str, order_id: str) -> dict:
    state = sentinela_graph.invoke({
        "user_query": user_query,
        "order_id": order_id,
    })
    return {
        "intent":            state["intent"],
        "response":          state["response"],
        "citations":         state["citations"],
        "trace":             state["reasoning_trace"],
        "escalated":         state["escalation_required"],
        "escalation_ticket": state.get("escalation_ticket", ""),
    }
```

The frontend rendering logic **does not change** between variations — only `call_agent()` is swapped.

---

## 10. Running the App

```bash
# From the project root
cd src/frontend
pip install streamlit
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 11. Known Limitations & Future Improvements

| Limitation | Future Fix |
|-----------|-----------|
| Mock `call_agent()` stub — no real agent | Wire in LangChain / LangGraph backend |
| No multi-turn memory across sessions | Add `ConversationBufferMemory` or LangGraph persistent state |
| Escalation is UI-only — no real ticket system | Integrate Zendesk / ServiceNow API |
| No authentication — any user can enter any order ID | Add session token or customer auth flow |
| Streamlit re-renders full page on each message | Migrate to FastAPI + React for production scale |
| Containment rate is session-only | Log to backend for aggregate evaluation metrics |

---

## 12. File Structure

```
src/
└── frontend/
    ├── app.py                  ← Main Streamlit application (this file)
    └── frontend_design.md      ← This design specification document
```
