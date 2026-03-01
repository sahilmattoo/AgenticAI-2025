from langchain_community.chat_message_histories import ChatMessageHistory

history_store = {}

def get_session_history(session_id: str):
    if session_id not in history_store:
        history_store[session_id] = ChatMessageHistory()
    return history_store[session_id]


# Expand this with
# Redis
# Postgres
# Vector DB