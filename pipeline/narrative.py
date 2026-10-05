import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_narrative(ticker: str, metrics: dict) -> str:
    prompt = f"""You are a markets analyst writing a short internal note.
You are given the following computed risk metrics for {ticker}:

- Annualized return: {metrics['annualized_return']:.2%}
- Annualized volatility: {metrics['annualized_volatility']:.2%}
- Sharpe ratio: {metrics['sharpe_ratio']:.2f}
- Sortino ratio: {metrics['sortino_ratio']:.2f}
- Max drawdown: {metrics['max_drawdown']:.2%}
- 95% daily VaR: {metrics['var_95']:.2%}

Write a 3-4 sentence note explaining what these numbers suggest about this
stock's risk profile right now. Do not invent news events, company facts, or
causes not present in the data above. If you are uncertain of a cause, say so
explicitly rather than asserting one.

After your analysis, output the exact marker ===FINAL NOTE=== on its own
line, followed by ONLY the final 3-4 sentence note with no further commentary
after it."""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "nvidia/nemotron-3.5-lightning:free",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
            "reasoning": {"exclude": True},
        },
        timeout=120,
    )
    full_text = response.json()["choices"][0]["message"]["content"]

    def is_valid_note(text):
        text = text.strip()
        return (
            len(text) > 40
            and text[-1] in ".!?"
            and "sentence note" not in text.lower()
            and "===final note===" not in text.lower()
        )

    if "===FINAL NOTE===" in full_text:
        candidate = full_text.split("===FINAL NOTE===")[-1].strip()
        if is_valid_note(candidate):
            return candidate

    import re
    quotes = re.findall(r'"([^"]{100,})"', full_text)
    good_quotes = [q for q in quotes if any(c.isdigit() for c in q) and is_valid_note(q)]
    if good_quotes:
        return good_quotes[-1].strip()

    return "[Narrative generation incomplete for this run — model response was truncated before reaching a usable answer.]"