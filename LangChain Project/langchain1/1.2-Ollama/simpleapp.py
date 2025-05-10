import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tracers.langchain import wait_for_all_tracers

load_dotenv()

# Set environment variables
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


# prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Please respond to the questions asked.",
        ),
        ("user", "Question:{question}"),
    ]
)

# Create LLM and Chain outside the button
llm = Ollama(model="gemma:2b", temperature=0.5)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Streamlit UI
st.title("Advanced Chat Assistant")
st.chat_message("assistant").write("How can I help you today?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("Your message:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(chain.stream({"question": prompt}))
    st.session_state.messages.append({"role": "assistant", "content": response})

# Make sure all traces are sent before app ends
wait_for_all_tracers()
