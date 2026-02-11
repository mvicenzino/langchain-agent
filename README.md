# LangChain ReAct Agent

An interactive AI agent built with LangChain and GPT-4o-mini that can search the web, run code, read/write files, check the weather, and more.

## Tools

| Tool | Description |
|------|-------------|
| **Search** | Web search via SerpAPI |
| **Calculator** | Math expressions with full `math` library support (sqrt, sin, pi, etc.) |
| **GetDateTime** | Returns current date and time |
| **Wikipedia** | Encyclopedia lookups |
| **WebScraper** | Fetches and extracts text from any webpage |
| **Weather** | Live weather for any location via wttr.in |
| **PythonREPL** | Executes Python code and returns output |
| **ReadFile** | Reads contents of local files |
| **WriteFile** | Writes content to local files |
| **Shell** | Runs shell commands |

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/mvicenzino/langchain-agent.git
cd langchain-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```bash
cp .env.example .env
```

Then add your API keys:

```
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

- Get an OpenAI key at https://platform.openai.com/api-keys
- Get a SerpAPI key at https://serpapi.com/manage-api-key (free tier: 100 searches/month)

### 4. Run the agent

```bash
python3 langchain_agent.py
```

## Usage Examples

```
You: What's the weather in Miami?
You: Calculate the hypotenuse of a triangle with sides 7 and 24
You: Search for the latest AI news
You: Look up quantum computing on Wikipedia
You: Scrape the top stories from https://news.ycombinator.com
You: Use Python to generate 10 random numbers
You: What's the current date and time?
You: Read the file ~/some_file.txt
You: Run the shell command ls -la
```

Type `quit` to exit.

## How It Works

The agent uses the [ReAct](https://arxiv.org/abs/2210.03629) (Reasoning + Acting) pattern. For each query, the LLM:

1. **Thinks** about which tool to use
2. **Acts** by calling the tool
3. **Observes** the result
4. Repeats until it has a final answer

This allows the agent to chain multiple tools together to solve complex, multi-step problems.

## License

MIT
