
from datetime import datetime

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

from tools import search_tool, wiki_tool, save_tool


# Load environment variables from .env
load_dotenv()


# Define the expected research response structure
class ResearchResponse(BaseModel):
    topic: str = Field(description="The topic being researched")
    summary: str = Field(description="A detailed summary of the findings")
    sources: list[str] = Field(
        description="Names or URLs of sources used for research"
    )
    tools_used: list[str] = Field(
        description="Names of tools used during research"
    )


# Initialize the language model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Initialize the structured output parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)


# Create the system prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI research assistant that helps users research topics
using web search and Wikipedia.

The current year is {current_year}.

Follow these instructions carefully:

1. Understand the user's research question before searching.
2. For trending topics, technology, tourism, news, and other topics
   that change over time, search for information relevant to the
   current year.
3. Do not deliberately search for 2023 or another past year unless
   the user specifically asks about that year.
4. Prefer recent sources and verify publication dates when available.
5. Do not describe old search results as current trends.
6. Use Wikipedia for background information and web search for
   additional information.
7. Summarize findings accurately. Do not invent facts or sources.
8. If recent information cannot be verified, clearly mention that
   limitation in the summary.
9. Use the save_text_to_file tool when the user asks to save the
   research findings.
10. Return the final response in the required structured format.
11. Return no extra text outside the structured response.

{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(
    format_instructions=parser.get_format_instructions(),
    current_year=str(datetime.now().year),
)


# Register the tools
tools = [search_tool, wiki_tool, save_tool]


# Create the tool-calling agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)


# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=6,
)


# Ask the user for a research topic
query = input("What can I help you research? ").strip()

if not query:
    print("Please enter a research topic.")
else:
    try:
        raw_response = agent_executor.invoke({"query": query})

        # AgentExecutor returns its final output as a string
        output = raw_response["output"]

        # Convert the JSON response into a Pydantic model
        structured_response = parser.parse(output)

        print("\n========== RESEARCH RESULTS ==========\n")
        print(structured_response.model_dump_json(indent=2))

    except Exception as e:
        print("\nAn error occurred while researching.")
        print("Error:", str(e))
