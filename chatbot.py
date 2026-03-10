import streamlit as st
from groq import Groq

# --- INITIALIZATION ---
st.set_page_config(page_title="AI Study Assistant", page_icon="🤖")
st.title("💬 My AI Buddy")
st.markdown("""
    <style>
    /* Change background of the main chat area */
    .stApp {
         background: linear-gradient(135deg, #1e1e2f, #2d2d44);
    }
    /* Make the chat input look sleek */
    .stChatInput {
        border-radius: 20px;
        border: 2px solid #7b2cbf !important;
    }

    /* Style the user and assistant messages */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
        padding: 10px;
    }
    
    /* Customizing the "Assistant" avatar background */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(123, 44, 191, 0.1);
        border: 1px solid #7b2cbf;
    }
    </style>
    """, unsafe_allow_html=True)
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    st.write("**Model:** Llama 3.3 70B")
    st.write("**Task:** CSE Study Buddy")
    
    # Add a colorful slider for "Creativity" (Temperature)
    temp = st.slider("Bot Creativity", 0.0, 1.0, 0.7)
# Initialize the Groq client
client = Groq(api_key="api")

# --- MEMORY (Session State) ---
# This acts like the "conversation_history" list but stays active in the browser
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful CSE Assistant specialized in AI and Architecture."}
    ]

# --- DISPLAY CHAT HISTORY ---
# This renders the "bubbles" on the screen
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- CHAT INPUT & LOGIC ---
if prompt := st.chat_input("What are we studying today?"):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call Groq API
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                stream=True, # This makes the text "type out" like Gemini
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
            # Save assistant response to memory
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")

