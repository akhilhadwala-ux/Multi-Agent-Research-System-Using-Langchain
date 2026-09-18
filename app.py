import streamlit as st

from src.agents.agents import (
    web_search_agent,
    web_scrapping_agent,
    writer_chain,
    critic_chain,
)


st.title("🔎 AI Research Assistant")

topic = st.text_input(
    "Enter a topic",
    placeholder="e.g. Artificial Intelligence in Healthcare"
)


if st.button("Run Research"):

    if not topic:
        st.warning("Please enter a topic.")
        st.stop()

    # Step 1: Web Search
    with st.spinner("Searching the web..."):
        search_agent = web_search_agent()

        search_result = search_agent.invoke({
            "messages": [
                (
                    "user",
                    f"find recent, relevant, and detailed information about the {topic}"
                )
            ]
        })

        search_results = search_result["messages"][-1].content

    st.subheader("🔎 Search Results")
    st.write(search_results)


   # Step 2: Web Scraping
    with st.spinner("Scraping relevant websites..."):

        scrapper_agent = web_scrapping_agent()

        scrapper_result = scrapper_agent.invoke({
            "messages": [
                (
                    "user",
                    f"""
                    You are performing focused web research for this topic:

                    {topic}

                    Search Results:
                    {['search_results'][:800]}

                    Instructions:

                    1. Select ONLY the 2 most relevant URLs from the search results.
                    2. Scrape ONLY those 2 URLs.
                    3. Do NOT perform another web search.
                    4. Do NOT follow links from those pages.
                    5. Do NOT open additional URLs.
                    6. Do NOT scrape the same URL more than once.
                    7. Ignore advertisements, navigation, menus, comments,
                    cookie notices and unrelated content.
                    8. Extract only information relevant to the topic.
                    9. Prioritize facts, statistics, dates, findings and
                    important details.
                    10. Do not copy entire webpages.
                    11. Stop after the 2 URLs have been processed.
                    12. Return concise research notes.

                    Output format:

                    SOURCE 1:
                    URL:
                    Key findings:

                    SOURCE 2:
                    URL:
                    Key findings:
                    """
                )
            ]
        })

        scrapped_content = (
            scrapper_result["messages"][-1].content
        )



    # Step 3: Writer
    with st.spinner("Writing the report..."):
        research_combined = (
            f"web search result:\n{search_results}\n\n"
            f"web scrapper result:\n{scrapped_content}"
        )

        report_draft = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })

        if hasattr(report_draft, "content"):
            report_draft = report_draft.content

    st.subheader("📝 Report")
    st.write(report_draft)


    # Step 4: Critic
    with st.spinner("Reviewing the report..."):
        feedback = critic_chain.invoke({
            "report": report_draft
        })

        if hasattr(feedback, "content"):
            feedback = feedback.content

    st.subheader("💡 Critic Feedback")
    st.write(feedback)

    st.success("Research completed!")