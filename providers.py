import os, httpx

def _need(name):
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing {name} in environment")
    return v

async def llm_groq(messages, model="llama-3.1-8b-instant", **kw):
    key = _need("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}"}
    payload = {
        "model": model,
        "messages": messages,
        "temperature": kw.get("temperature", 0.6),
        "max_tokens": 600,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

async def llm_openrouter(messages, model="meta-llama/llama-3.1-8b-instruct:free", **kw):
    key = _need("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "https://github.com/Umang00/ai-portfolio-mvp",
        "X-Title": "AI-Portfolio-MVP",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": kw.get("temperature", 0.6),
        "max_tokens": 600,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
