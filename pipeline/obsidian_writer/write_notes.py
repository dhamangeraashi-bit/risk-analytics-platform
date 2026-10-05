from pathlib import Path
from datetime import date

VAULT_PATH = Path("C:/Users/LENOVO/Desktop/My Knowledge Vault/Analysis Log")

def write_narrative_note(ticker: str, narrative: str) -> Path:
    VAULT_PATH.mkdir(parents=True, exist_ok=True)
    filename = f"{date.today().isoformat()} - {ticker}.md"
    filepath = VAULT_PATH / filename

    content = f"""# Portfolio Analysis — {ticker}
**Date:** {date.today().isoformat()}

{narrative}

---
tags: #analytics #portfolio #{ticker.lower()}
"""
    filepath.write_text(content, encoding="utf-8")
    return filepath