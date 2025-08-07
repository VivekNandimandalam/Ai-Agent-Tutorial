# import streamlit as st
# from main import agent_executor, parser

# st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="centered")

# # Initialize chat history in session state
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Hey! I am your research assistant. How can I help you today?"}
#     ]

# st.markdown(
#     """
#     <style>
#     .stChatMessage {text-align: left;}
#     .stChatInput {position: fixed; bottom: 2rem; width: 50vw;}
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.title("AI Research Assistant", anchor=False)

# # Display chat history
# for msg in st.session_state.messages:
#     if msg["role"] == "user":
#         st.chat_message("user").write(msg["content"])
#     else:
#         st.chat_message("assistant").write(msg["content"])

# # Input box at the bottom
# user_input = st.chat_input("Type your research question here...")

# if user_input:
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     with st.spinner("Thinking..."):
#         raw_response = agent_executor.invoke({"query": user_input})
#         output = raw_response["output"].strip()
#         if output.startswith("```json"):
#             output = output.removeprefix("```json").removesuffix("```").strip()
#         elif output.startswith("```"):
#             output = output.removeprefix("```").removesuffix("```").strip()
#         try:
#             structured_response = parser.parse(output)
#             response_text = (
#                 f"**Summary:** {structured_response.summary}\n\n"
#                 f"**Sources:** {', '.join(structured_response.sources)}\n\n"
#                 f"**Tools Used:** {', '.join(structured_response.tools_used)}"
#             )
#         except Exception as e:
#             response_text = f"Error parsing response: {e}\n\nRaw response: {raw_response}"

#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response_text})
#     st.experimental_rerun()




# import streamlit as st

# st.write ("Hello, I am Your AI Research Assistant")

import streamlit as st
from main import agent_executor, parser

st.markdown(
    "<h2 style='text-align: center;'>Hello, I am Your AI Research Assistant</h2>",
    unsafe_allow_html=True
)

query = st.text_input("Please enter your research question:", placeholder="What can I help you with?")


if st.button("Submit") and query:
    with st.spinner("Researching..."):
        raw_response = agent_executor.invoke({"query": query})
        output = raw_response["output"].strip()
        if output.startswith("```json"):
            output = output.removeprefix("```json").removesuffix("```").strip()
        elif output.startswith("```"):
            output = output.removeprefix("```").removesuffix("```").strip()
        try:
            structured_response = parser.parse(output)
            st.subheader("Summary")
            st.write(structured_response.summary)
            st.subheader("Sources")
            st.write(structured_response.sources)
            st.subheader("Tools Used")
            st.write(structured_response.tools_used)
        except Exception as e:
            st.error(f"Error parsing response: {e}")
            st.write("Raw response:", raw_response)