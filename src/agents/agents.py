from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search,scrape_url
from dotenv import load_dotenv

load_dotenv()


## LLM Initialization

llm = ChatGroq(model="openai/gpt-oss-120b")