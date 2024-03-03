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
