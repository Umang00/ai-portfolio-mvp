import os, asyncio, gradio as gr
from dotenv import load_dotenv
from retriever import TinyRetriever
from providers import llm_groq, llm_openrouter

load_dotenv()
PROVIDER = os.getenv("PROVIDER", "groq")
LINKEDIN_URL = os.getenv("LINKEDIN_URL", "https://linkedin.com")
CALENDLY_URL = os.getenv("CALENDLY_URL", "https://calendly.com/yourlink")

SYSTEM = """You are Umang’s AI Portfolio Assistant.

Style:
- Be concise, confident, specific. Prefer short paragraphs and bullets.
- Do not invent facts. If context is insufficient, say so briefly and ask one focused follow-up.
- Only use retrieved snippets when relevant; otherwise ignore them.
- Suggest next steps by referring to the buttons below (LinkedIn, Book a Call). Do NOT print bracket tokens.

Output format:
1) Summary — 1–2 sentences.
2) Evidence — 2–5 bullets grounded in the provided context.
"""

retriever = TinyRetriever("content")

async def generate_reply(user_text: str):
    # retrieve local context
    ctxs = retriever.topk(user_text, k=3)
    context = "\n\n".join([f"[{c['source']}]\n{c['text']}" for c in ctxs]) \
              or "About Umang: Builder PM working on GenAI projects."

    messages = [
        {"role": "system", "content": SYSTEM + f"\n\nContext:\n{context}"},
        {"role": "user", "content": user_text}
    ]

    if PROVIDER == "openrouter":
        reply = await llm_openrouter(messages)
    else:
        reply = await llm_groq(messages)

    return reply


def build_ui():
    # Custom modern theme
    theme = gr.themes.Default(
        primary_hue="blue",
        secondary_hue="gray",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter"),
        font_mono=[gr.themes.GoogleFont("JetBrains Mono")]
    )
    
    # Enhanced CSS for modern UI with better chat interface
    custom_css = """
    /* Main container styling */
    .gradio-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding: 20px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        min-height: 100vh !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Header styling */
    .header-section {
        text-align: center !important;
        margin-bottom: 30px !important;
        padding: 40px 30px !important;
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 24px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .header-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 15px !important;
        letter-spacing: -0.02em !important;
    }
    
    .header-subtitle {
        font-size: 1.3rem !important;
        color: #64748b !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 24px !important;
        padding: 30px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        margin-bottom: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Enhanced Chatbot styling - Clean and modern */
    .chatbot {
        border: none !important;
        border-radius: 20px !important;
        background: #ffffff !important;
        min-height: 600px !important;
        max-height: 600px !important;
        padding: 0 !important;
        box-shadow: none !important;
        overflow-y: auto !important;
    }
    
    /* Remove default chatbot styling */
    .chatbot .message-wrap {
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        background: none !important;
    }
    
    /* Custom message styling */
    .chatbot .message {
        margin: 20px 0 !important;
        padding: 0 !important;
        border: none !important;
        background: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }
    
    /* User message styling */
    .chatbot .message.user {
        display: flex !important;
        justify-content: flex-end !important;
        margin-bottom: 20px !important;
    }
    
    .chatbot .message.user .message-content {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        padding: 16px 20px !important;
        border-radius: 20px !important;
        border-bottom-right-radius: 6px !important;
        max-width: 70% !important;
        word-wrap: break-word !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        margin-left: 20px !important;
    }
    
    /* Assistant message styling */
    .chatbot .message.assistant {
        display: flex !important;
        justify-content: flex-start !important;
        margin-bottom: 20px !important;
    }
    
    .chatbot .message.assistant .message-content {
        background: #f8fafc !important;
        color: #334155 !important;
        padding: 16px 20px !important;
        border-radius: 20px !important;
        border-bottom-left-radius: 6px !important;
        max-width: 70% !important;
        word-wrap: break-word !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        margin-right: 20px !important;
    }
    
    /* Hide avatars for cleaner design */
    .chatbot .avatar {
        display: none !important;
    }
    
    /* Input area */
    .input-container {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 24px !important;
        padding: 30px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        margin-bottom: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Better input field styling */
    .textbox, .modern-input {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        background: #ffffff !important;
        font-family: inherit !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
        resize: none !important;
    }
    
    .textbox:focus, .modern-input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
        background: #ffffff !important;
        outline: none !important;
    }
    
    .textbox::placeholder, .modern-input::placeholder {
        color: #94a3b8 !important;
        font-style: italic !important;
    }
    
    /* Modern input container */
    .modern-input {
        min-height: 56px !important;
        max-height: 120px !important;
        overflow-y: auto !important;
    }
    
    /* Input row styling */
    .input-container .gr-row {
        gap: 12px !important;
        align-items: flex-end !important;
    }
    
    /* Enhanced buttons */
    .send-button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 28px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        cursor: pointer !important;
        min-width: 100px !important;
    }
    
    .send-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .send-button:active {
        transform: translateY(0) !important;
    }
    
    /* CTA buttons */
    .cta-container {
        display: flex !important;
        gap: 20px !important;
        justify-content: center !important;
    }
    
    .cta-button {
        flex: 1 !important;
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 20px 28px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3) !important;
        text-decoration: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
    }
    
    .cta-button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
    }
    
    .linkedin-button {
        background: linear-gradient(135deg, #0077b5, #005885) !important;
        box-shadow: 0 6px 20px rgba(0, 119, 181, 0.3) !important;
    }
    
    .linkedin-button:hover {
        box-shadow: 0 8px 25px rgba(0, 119, 181, 0.4) !important;
    }
    
    /* Animations */
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        display: inline-block !important;
        width: 20px !important;
        height: 20px !important;
        border: 3px solid #f3f3f3 !important;
        border-top: 3px solid #667eea !important;
        border-radius: 50% !important;
        animation: spin 1s linear infinite !important;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        padding: 18px 24px !important;
        background: #f8fafc !important;
        border-radius: 20px !important;
        border-bottom-left-radius: 6px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid #e2e8f0 !important;
        max-width: 70% !important;
    }
    
    .typing-dot {
        width: 8px !important;
        height: 8px !important;
        border-radius: 50% !important;
        background: #667eea !important;
        animation: pulse 1.4s infinite !important;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s !important;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .gradio-container {
            padding: 15px !important;
        }
        
        .header-title {
            font-size: 2.2rem !important;
        }
        
        .header-subtitle {
            font-size: 1.1rem !important;
        }
        
        .cta-container {
            flex-direction: column !important;
        }
        
        .chatbot .message.user .message-content,
        .chatbot .message.assistant .message-content {
            max-width: 85% !important;
            padding: 14px 18px !important;
        }
        
        .chatbot {
            min-height: 500px !important;
            max-height: 500px !important;
        }
    }
    
    /* Scrollbar styling */
    .chatbot::-webkit-scrollbar {
        width: 6px !important;
    }
    
    .chatbot::-webkit-scrollbar-track {
        background: #f1f1f1 !important;
        border-radius: 3px !important;
    }
    
    .chatbot::-webkit-scrollbar-thumb {
        background: #c1c1c1 !important;
        border-radius: 3px !important;
    }
    
    .chatbot::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8 !important;
    }
    
    /* Remove unwanted elements */
    .chatbot .copy-button {
        display: none !important;
    }
    
    .chatbot .clear-button {
        display: none !important;
    }
    
    /* Additional improvements */
    .chatbot .message-wrap:first-child {
        margin-top: 0 !important;
    }
    
    .chatbot .message-wrap:last-child {
        margin-bottom: 0 !important;
    }
    
    /* Better spacing for message content */
    .chatbot .message-content p {
        margin: 0 0 8px 0 !important;
    }
    
    .chatbot .message-content p:last-child {
        margin-bottom: 0 !important;
    }
    
    /* Improve list styling */
    .chatbot .message-content ul,
    .chatbot .message-content ol {
        margin: 8px 0 !important;
        padding-left: 20px !important;
    }
    
    .chatbot .message-content li {
        margin: 4px 0 !important;
    }
    
    /* Better button styling */
    .send-button:disabled {
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }
    
    /* Loading state for input */
    .input-container.loading .textbox {
        opacity: 0.7 !important;
        pointer-events: none !important;
    }
    
    /* Improved focus states */
    .send-button:focus {
        outline: 2px solid #667eea !important;
        outline-offset: 2px !important;
    }
    """
    
    with gr.Blocks(
        title="AI Portfolio Assistant — Umang's Professional Assistant", 
        theme=theme, 
        css=custom_css
    ) as demo:
        
        # Header section
        with gr.Column(elem_classes=["header-section"]):
            gr.HTML("""
                <div class="header-title">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; vertical-align: middle; margin-right: 15px;">
                        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="url(#gradient)" stroke-width="2" stroke-linejoin="round"/>
                        <path d="M2 17L12 22L22 17" stroke="url(#gradient)" stroke-width="2" stroke-linejoin="round"/>
                        <path d="M2 12L12 17L22 12" stroke="url(#gradient)" stroke-width="2" stroke-linejoin="round"/>
                        <defs>
                            <linearGradient id="gradient" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#667eea"/>
                                <stop offset="1" stop-color="#764ba2"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    AI Portfolio Assistant
                </div>
                <div class="header-subtitle">Discover Umang's expertise, projects, and professional journey</div>
            """)
        
        # Chat container
        with gr.Column(elem_classes=["chat-container"]):
            # Chat history state
            history = gr.State([])
            
            # Enhanced chatbot with proper avatars and clean interface
            chatbot = gr.Chatbot(
                label="",
                height=600,
                show_copy_button=False,
                type="messages",
                show_label=False,
                container=True,
                show_share_button=False
            )
        
        # Input container
        with gr.Column(elem_classes=["input-container"]):
            with gr.Row():
                user_box = gr.Textbox(
                    lines=1, 
                    label="", 
                    placeholder="Ask me anything about Umang's experience, projects, or skills...",
                    show_label=False,
                    scale=4,
                    max_lines=3,
                    elem_classes=["modern-input"]
                )
                send = gr.Button(
                    "Send", 
                    elem_classes=["send-button"],
                    scale=1,
                    variant="primary"
                )
        
        # CTA buttons
        with gr.Column(elem_classes=["cta-container"]):
            with gr.Row():
                gr.Button(
                    "🔗 View LinkedIn Profile", 
                    link=LINKEDIN_URL,
                    elem_classes=["cta-button", "linkedin-button"]
                )
                gr.Button(
                    "📅 Book a Call", 
                    link=CALENDLY_URL,
                    elem_classes=["cta-button"]
                )

        # Welcome message
        welcome_message = [
            {
                "role": "assistant", 
                "content": "👋 Hello! I'm Umang's AI Portfolio Assistant. I can help you learn about his professional experience, projects, and skills. Feel free to ask me anything!"
            }
        ]
        
        # Handler with loading state
        def on_send(u, h):
            if not u.strip():
                return h, "", h
            
            # Add user message to history
            h = h + [{"role": "user", "content": u}]
            
            # Generate reply
            reply = asyncio.run(generate_reply(u))
            
            # Add assistant reply to history
            h = h + [{"role": "assistant", "content": reply}]
            
            return h, "", h

        # Initialize chatbot with welcome message
        chatbot.value = welcome_message
        history.value = welcome_message
        
        # Wire events
        send.click(on_send, [user_box, history], [chatbot, user_box, history])
        user_box.submit(on_send, [user_box, history], [chatbot, user_box, history])

    return demo


if __name__ == "__main__":
    import socket
    
    def find_free_port():
        """Find a free port starting from 7860"""
        for port in range(7860, 7890):  # Check more ports
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))  # Use localhost instead of 0.0.0.0
                    return port
            except OSError:
                continue
        return None  # No free port found
    
    demo = build_ui()
    free_port = find_free_port()
    
    if free_port:
        print(f"🚀 Starting AI Portfolio Assistant on port {free_port}")
        print(f"📱 Local URL: http://localhost:{free_port}")
        print(f"🌐 Public URL will be available after startup")
        
        demo.launch(
            server_name="127.0.0.1",  # Use localhost for better compatibility
            server_port=free_port,
            show_error=True,
            inbrowser=True,
            quiet=False
        )
    else:
        print("❌ No free ports available in range 7860-7889")
        print("🔄 Letting Gradio find an available port...")
        demo.launch(
            server_name="127.0.0.1",
            show_error=True,
            inbrowser=True,
            quiet=False
        )
