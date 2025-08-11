import streamlit as st
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Check for API key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("🚨 GOOGLE_API_KEY not found in environment variables!")
    st.info("Please add your Google API Key in the Streamlit Cloud secrets or environment variables.")
    st.stop()

# Import heavy dependencies only when needed
@st.cache_resource
def get_agent_and_parser():
    """Cache the agent executor and parser to avoid recreating on each run"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain.output_parsers import PydanticOutputParser
        from langchain.agents import create_tool_calling_agent, AgentExecutor
        from langchain.prompts import ChatPromptTemplate
        from tools import search_tool, wiki_tool, save_tool
        
        class ResearchResponse(BaseModel):
            topic: str
            summary: str
            sources: list[str]
            tools_used: list[str]

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=os.getenv("GOOGLE_API_KEY")
        )   

        parser = PydanticOutputParser(pydantic_object=ResearchResponse)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful research assistant. You will help the user with their research topic."
             "Answer the user query and use necessary tools."
             "wrap the output in this format and provide no other text\n{format_instructions}"),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]).partial(format_instructions=parser.get_format_instructions())
             
        tools = [search_tool, wiki_tool, save_tool]   
        agent = create_tool_calling_agent(
            llm=llm,    
            prompt=prompt,
            tools=tools
        )
        
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,    
            verbose=True,
        )
        
        return agent_executor, parser
        
    except ImportError as e:
        st.error(f"Import error: {e}")
        st.info("Please check that all required packages are installed.")
        st.stop()
    except Exception as e:
        st.error(f"Error creating agent: {e}")
        st.stop()

def process_response(raw_response, parser):
    """Process and parse the agent response"""
    output = raw_response["output"].strip()
    
    if output.startswith("```json"):
        output = output.removeprefix("```json").removesuffix("```").strip()
    elif output.startswith("```"):
        output = output.removeprefix("```").removesuffix("```").strip()

    try:
        structured_response = parser.parse(output)
        return structured_response, None
    except Exception as e:
        return None, f"Error parsing response: {e}"

# Main UI
st.markdown(
    "<h2 style='text-align: center;'>🔍 AI Research Assistant</h2>",
    unsafe_allow_html=True
)

# Initialize session state
if "queries" not in st.session_state:
    st.session_state.queries = []

# Input form
with st.form("research_form"):
    query = st.text_input(
        "Please enter your research question:", 
        placeholder="What can I help you with?",
        help="Enter your research topic or question here"
    )
    submitted = st.form_submit_button("🚀 Research", use_container_width=True)

# Process the query
if submitted and query:
    # Load cached agent and parser
    with st.spinner("Loading research tools..."):
        try:
            agent_executor, parser = get_agent_and_parser()
        except Exception as e:
            st.error(f"Failed to initialize research tools: {e}")
            st.stop()
    
    # Add query to history
    st.session_state.queries.append(query)
    
    st.write(f"**Researching:** {query}")
    
    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.spinner("🔍 Researching... This may take a moment"):
            try:
                # Execute the research
                raw_response = agent_executor.invoke({"query": query})
                
                # Process the response
                structured_response, error = process_response(raw_response, parser)
                
                if structured_response:
                    # Display results in a nice format
                    st.success("✅ Research completed!")
                    
                    # Summary section
                    st.subheader("📝 Summary")
                    st.write(structured_response.summary)
                    
                    # Sources section
                    st.subheader("📚 Sources")
                    if structured_response.sources:
                        for i, source in enumerate(structured_response.sources, 1):
                            st.write(f"{i}. {source}")
                    else:
                        st.write("No specific sources provided")
                    
                    # Tools used section  
                    st.subheader("🛠️ Tools Used")
                    if structured_response.tools_used:
                        st.write(", ".join(structured_response.tools_used))
                    else:
                        st.write("No specific tools mentioned")
                        
                else:
                    st.error(f"❌ {error}")
                    with st.expander("Raw Response (for debugging)"):
                        st.write(raw_response)
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.write("Please try again with a different query.")
    
    with col2:
        # Show query history
        if len(st.session_state.queries) > 1:
            st.subheader("Recent Queries")
            for i, past_query in enumerate(reversed(st.session_state.queries[-5:]), 1):
                st.caption(f"{i}. {past_query}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by LangChain & Streamlit</p>", 
    unsafe_allow_html=True
)