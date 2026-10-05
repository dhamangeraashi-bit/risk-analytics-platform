import requests
import streamlit as st

def ask_about_data(question: str, context_data: dict) -> str:
    api_key = st.secrets.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return "API key not configured yet."
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "nvidia/nemotron-3.5-lightning:free",
                "max_tokens": 600,
                "messages": [
                    {"role": "system", "content": (
                        "You answer questions about the specific financial data "
                        "provided below only. You have no other tools or memory. "
                        "If the answer isn't derivable from the data, say so. "
                        "Answer in 2-3 sentences, no preamble, no visible reasoning."
                    )},
                    {"role": "user", "content": f"Data: {context_data}\n\nQuestion: {question}"},
                ],
                "reasoning": {"exclude": True},
            },
            timeout=60,
        )
        text = response.json()["choices"][0]["message"]["content"]
        return text.strip()
    except Exception as e:
        return f"Couldn't get an answer right now ({e}). Try again shortly."