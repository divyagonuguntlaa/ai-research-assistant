# AI Research Assistant

An AI-powered research assistant built with Python and LangChain that researches user questions using web search and Wikipedia, then returns findings in a structured JSON format.

## Features

- **AI-powered research:** Uses OpenAI's language model to interpret research questions and summarize findings.
- **Web search:** Retrieves additional information through DuckDuckGo search.
- **Wikipedia integration:** Uses Wikipedia for background information.
- **Structured output:** Uses Pydantic to organize research into a consistent JSON schema.
- **File saving:** Supports saving research findings to a local text file.
- **Error handling:** Handles temporary search and Wikipedia failures.
- **Environment configuration:** Loads API credentials from a local `.env` file.

## Tech Stack

- Python
- LangChain
- OpenAI API
- DuckDuckGo Search
- Wikipedia
- Pydantic
- python-dotenv

## Project Structure

```text
ai-research-assistant/
├── main.py
├── tools.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env                 # Local only; never commit
```

## Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies
- An OpenAI API key
- Git
- A GitHub account

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-research-assistant.git
   cd ai-research-assistant
   ```

2. Create and activate a virtual environment:

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API key:

   ```text
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Replace the placeholder with your own API key. Do not share or commit this file.

## Usage

Run the application:

```bash
python main.py
```

Enter a research question when prompted, for example:

```text
What are the emerging applications of artificial intelligence in 2026?
```

The assistant uses its available research tools and returns a structured JSON response containing the topic, summary, sources, and tools used.

## Output Format

The response follows a Pydantic model with these fields:

- `topic`: Research topic
- `summary`: Summary of findings
- `sources`: Sources associated with the research
- `tools_used`: Tools used during research

## Limitations

- Search results depend on external services and network availability.
- The accuracy and freshness of findings depend on the sources retrieved.
- AI-generated summaries and source references must be verified before relying on them.
- This project is a learning and demonstration project, not a substitute for primary-source research.

## Future Improvements

- Improve source URL extraction and verification.
- Add citations linked directly to individual claims.
- Add tests and logging.
- Add a web interface and research history.
- Support additional research providers.

## Security

API keys and other secrets must be stored in environment variables and excluded from version control.

## License

This project is available under the MIT License. Add a `LICENSE` file before distributing it under that license.
