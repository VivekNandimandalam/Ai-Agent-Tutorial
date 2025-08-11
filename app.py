

import streamlit as st
from main import create_agent_executor, process_response

# Set page config for better performance
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"    
)

# Cache the heavy agent creation
@st.cache_resource
def get_agent_and_parser():
    """Cache the agent executor and parser to avoid recreating on each run"""
    return create_agent_executor()

# Main UI
st.markdown(
    "<h2 style='text-align: center;'>🔍 AI Research Assistant</h2>",
    unsafe_allow_html=True
)

# Initialize session state for query history (optional)
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
        agent_executor, parser = get_agent_and_parser()
    
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
        # Optional: Show query history or tips
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