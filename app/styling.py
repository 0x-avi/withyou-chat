chat_interface = """
<style>
    /* Hide Streamlit branding and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* User message - RIGHT SIDE */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 1rem 0;
        width: 100%;
    }
    
    .user-message-content {
        display: flex;
        align-items: flex-end;
        flex-direction: row-reverse;
        max-width: 70%;
        gap: 10px;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 5px 18px;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
    }
    
    /* Bot message - LEFT SIDE */
    .bot-message {
        display: flex;
        justify-content: flex-start;
        margin: 1rem 0;
        width: 100%;
    }
    
    .bot-message-content {
        display: flex;
        align-items: flex-end;
        flex-direction: row;
        max-width: 70%;
        gap: 10px;
    }
    
    .bot-bubble {
        background: #f8f9fa;
        color: #333;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 5px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
    }
    
    /* Avatar styling */
    .user-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }
    
    .bot-avatar {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }
    
    /* Chat header */
    .chat-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    .chat-header h1 {
        margin: 0;
        font-size: 1.8em;
    }
    
    .chat-header p {
        margin: 5px 0 0 0;
        opacity: 0.9;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e9ecef;
        padding: 12px 20px;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
    }
    
    /* Chat container */
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #e9ecef;
        border-radius: 15px;
        background: white;
        margin-bottom: 20px;
    }
    
    /* Timestamp */
    .timestamp {
        font-size: 0.7em;
        color: #6c757d;
        margin-top: 5px;
        text-align: right;
    }
    
    .bot-timestamp {
        text-align: left;
    }
</style>
"""