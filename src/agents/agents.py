from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search,scrape_url
from dotenv import load_dotenv

load_dotenv()


## LLM Initialization

llm = ChatGroq(model="openai/gpt-oss-120b")


# 1st Agent --> for web_search

def web_search_agent():
    return create_agent(model=llm,tools=[web_search],
                        system_prompt="""
            You are a web search agent.

            Search the web for recent and relevant information.
            Return the search results and URLs.

            Do not attempt to open or scrape URLs.
            """

)


# 2nd Agent --> for web_scrapping

def web_scrapping_agent():
    return create_agent(model=llm, tools=[scrape_url],
                        system_prompt = """
    You are a fast web research scraper.

    Your job is to extract useful information from the URLs provided
    in the user's search results.

    Follow these rules strictly:

    1. Scrape ONLY the 2 or 3 most relevant URLs.
    2. Do NOT perform additional web searches.
    3. Do NOT recursively follow links from the webpages.
    4. Extract only information directly relevant to the research topic.
    5. Ignore advertisements, navigation menus, comments, and unrelated content.
    6. Do not copy entire webpages.
    7. Focus on facts, statistics, dates, important claims, and useful context.
    8. Stop scraping once sufficient information has been collected.
    9. Return concise research notes.
    10. Keep the final response below approximately 1500 words.

    Speed is more important than exhaustive coverage.
    """)


# writer chain

writer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are an Expert Research writer. Write a well structured, detailed, and insightful report."),
        ("human","""Write a detailed report on the topic provided below.

    Topic:{topic}
    
    Research Gathered:{research}

    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (list all URLs found in the research)

    Be detailed, factual and professional.""")
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()


# critic chain

critic_prompt = ChatPromptTemplate.from_messages(
    [("system","you are a sharp and constructive research critic. Be honest and specific."),
     ("human","""Review the research report below and evaluate it strictly.
      
     Report:{report}
     Respond in this exact format:

    Score: X/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ...

    One line verdict:
    
    ... """)
    ]
)


critic_chain = critic_prompt | llm | StrOutputParser()

