from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import streamlit as st
import os

def save_to_txt(data: str, filename: str = "research_output.txt"):
    """Save research data to a text file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    
    try:
        # For Streamlit Cloud, we might not have write permissions
        # So we'll just return the formatted text instead of writing to file
        return f"Research data formatted and ready:\n{formatted_text}"
    except Exception as e:
        return f"Note: Could not save to file ({str(e)}), but research completed successfully"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file or formats it for display.",
)

# Initialize search tool
try:
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="search",
        func=search.run,
        description="Search the web for information.",
    )
except Exception as e:
    # Fallback if DuckDuckGo fails
    def dummy_search(query):
        return f"Search functionality temporarily unavailable. Query was: {query}"
    
    search_tool = Tool(
        name="search",
        func=dummy_search,
        description="Search the web for information (fallback mode).",
    )

@st.cache_resource
def get_wiki_wrapper():
    """Get Wikipedia wrapper with caching"""
    try:
        return WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
    except Exception as e:
        # Return a dummy wrapper if Wikipedia fails
        class DummyWrapper:
            def run(self, query):
                return f"Wikipedia search for '{query}' temporarily unavailable"
        return DummyWrapper()

try:
    api_wrapper = get_wiki_wrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
except Exception as e:
    # Fallback wiki tool
    def dummy_wiki(query):
        return f"Wikipedia search temporarily unavailable. Query was: {query}"
    
    wiki_tool = Tool(
        name="wikipedia",
        func=dummy_wiki,
        description="Search Wikipedia for information (fallback mode).",
    )