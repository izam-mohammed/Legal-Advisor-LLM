import streamlit as st

st.title("Legal Advisor 📚")

# Sidebar for selecting the chatbot
selected_chatbot = st.sidebar.radio("Select Chatbot", ("OpenAI", "Llama 2"))
if selected_chatbot == "OpenAI":
    from src import openai_call
elif selected_chatbot == "Llama 2":
    st.warning(
        "It might take some time to get response becuase of the size of Llama 2 model ⚠️"
    )
    from src import llama_call

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
st.info("""
**Legal Advisor Bot:**
- **Objective:** Develop a conversational AI chatbot to provide legal advice and assistance. 🤖💼
- **Technology Stack:** Utilizes Streamlit for the user interface, integrates with external chatbot APIs (such as OpenAI and Llama 2) for natural language processing. 🖥️📡
- **Features:**
  - Allows users to select between different chatbot models for varied responses. 🔄
  - Provides a chat history feature to track user interactions. 📝
  - Displays loading spinner while fetching responses from the selected chatbot. ⏳
  - Offers a user-friendly interface for asking legal questions. 💬
- **Emphasis:** Focuses on simplicity, efficiency, and accessibility in delivering legal information and support through conversational AI. 🎯
        """)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask something about law"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Add a loading spinner while waiting for response
    with st.spinner("Thinking ✨..."):
        if selected_chatbot == "Llama 2":
            response = llama_call(prompt)
        elif selected_chatbot == "OpenAI":
            response = openai_call(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
