import streamlit as st
import asyncio
import json
from mcp_server import ProfileServer

st.set_page_config(page_title="Luise AI Assistant", page_icon="🤖")

st.title("🤖 Luise Profile AI Assistant")
st.write("Ask me anything about Luise's profile, skills, talks, or projects!")

# Initialize MCP server
@st.cache_resource
def get_mcp_server():
    return ProfileServer()

server = get_mcp_server()

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about Luise's profile..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process query and get response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Simple keyword matching to tool calls
        async def process_query():
            if any(word in prompt.lower() for word in ["profile", "about", "bio"]):
                result = await server.call_tool("get_profile", {})
                return f"Here's Luise's profile:\n\n{result.content[0].text}"
            
            elif any(word in prompt.lower() for word in ["skills", "skill"]):
                result = await server.call_tool("search_skills", {})
                return f"Here are Luise's skills:\n\n{result.content[0].text}"
            
            elif any(word in prompt.lower() for word in ["talks", "speaking", "presentations"]):
                result = await server.call_tool("get_talks", {})
                return f"Here are Luise's talks:\n\n{result.content[0].text}"
            
            elif any(word in prompt.lower() for word in ["projects", "work"]):
                result = await server.call_tool("get_projects", {})
                return f"Here are Luise's projects:\n\n{result.content[0].text}"
            
            elif "quote" in prompt.lower():
                topic = "general"
                if "python" in prompt.lower():
                    topic = "python"
                elif "ai" in prompt.lower():
                    topic = "ai"
                
                result = await server.call_tool("get_quote", {"topic": topic})
                return f"Here's a quote for you:\n\n{result.content[0].text}"
            
            else:
                return "I can help you with information about:\n- 👤 Profile & Bio\n- 💼 Skills\n- 🎤 Talks & Presentations\n- 🚀 Projects\n- 💭 Inspirational Quotes\n\nWhat would you like to know?"
        
        try:
            response = asyncio.run(process_query())
        except Exception as e:
            response = f"Sorry, I encountered an error: {str(e)}"
        
        response_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with available tools
with st.sidebar:
    st.header("🛠️ Available Tools")
    st.write("- 👤 Get Profile")
    st.write("- 💭 Get Quote")
    st.write("- 💼 Search Skills")
    st.write("- 🎤 Get Talks")
    st.write("- 🚀 Get Projects")
    st.write("- ❓ Submit Question")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()