from src.agents.agents import web_search_agent,web_scrapping_agent,writer_chain,critic_chain

def run_web_search_pipeline(topic:str)->dict:

    # step:1 web search agent working 

    state ={}
    search_agent = web_search_agent()

    search_result = search_agent.invoke({
    "messages":[("user",f"find recent, relevant, and detailed information about the {topic}")]
    })

    state['search_results'] = search_result['messages'][-1].content
    print("\n search result ",state['search_results'])

    # step:2 web scrapping agent working

    scrapper_agent = web_scrapping_agent()
    scrapper_result = scrapper_agent.invoke({

        "messages": [("user",
            f"""
            Topic: {topic}

            From the search results below, select ONLY the
            2 most relevant URLs and scrape them.

            Do not search for additional sources.
            Do not follow links from those pages.

            Return concise research notes containing:
            - Key facts
            - Important statistics
            - Dates
            - Main findings
            - Source URL

            Search Results:
            {state['search_results'][:800]}""")]
    })

    state['scrapped_content'] = scrapper_result['messages'][-1].content
    print("\n scrapper result ",state['scrapped_content'])


    # step:3  writer agent working

    research_combined = (
        f"web search result:\n {state['search_results']}\n\n"
        f"web scrapper result:\n {state['scrapped_content']}")

    state["report_draft"] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined})

    print("\n Draft Report: \n",state['report_draft'])


    # step:4 

    state["feedback"] = critic_chain.invoke({
        "report":state['report_draft']})

    print("\n critic report \n",state["feedback"])

    return state