import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent,AgentExecutor
from langchain.prompts import ChatPromptTemplate
from tools import search_tool,wiki_tool,save_tool


load_dotenv()

class ResearchRespone(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used :list[str]



# llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatGoogleGenerativeAI   (
    model="gemini-2.0-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)   

parser = PydanticOutputParser(pydantic_object=ResearchRespone)

prompt = ChatPromptTemplate.from_messages(
    [   ("system", "You are a helpful research assistant. You will help the user with their research topic."
         "Answer the user query and use necessary tools."
         "wrap the output in this formant and provide no other text\n{format_instructions}"),

    ("placeholder", "{chat_history}"),
    ("human","{query}"),
    ("placeholder","{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())
     
tools = [search_tool, wiki_tool,save_tool]   
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

query = input("What can I help you with? ")

raw_response = agent_executor.invoke({"query": query})
output = raw_response["output"].strip()
if output.startswith("```json"):
    output = output.removeprefix("```json").removesuffix("```").strip()
elif output.startswith("```"):
    output = output.removeprefix("```").removesuffix("```").strip()



# structured_response = parser.parse(raw_response["output"]) 

try:
    structured_response = parser.parse(output)
    print(structured_response)
except Exception as e:
    print(f"Error parsing response", e, "Raw response:", raw_response)
    
