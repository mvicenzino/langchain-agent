# LangChain ReAct Agent

An interactive AI agent built with LangChain and GPT-4o-mini with 28 tools across search, AI, data, productivity, and developer categories.

## Tools (28)

### Core (10)

| Tool | Description |
|------|-------------|
| **Search** | Web search via SerpAPI |
| **Calculator** | Math expressions with full `math` library (sqrt, sin, pi, etc.) |
| **GetDateTime** | Returns current date and time |
| **Wikipedia** | Encyclopedia lookups |
| **WebScraper** | Fetches and extracts text from any webpage |
| **Weather** | Live weather for any location via wttr.in |
| **PythonREPL** | Executes Python code and returns output |
| **ReadFile** | Reads contents of local files |
| **WriteFile** | Writes content to local files |
| **Shell** | Runs shell commands |

### AI / LLM (4)

| Tool | Description |
|------|-------------|
| **Summarize** | Summarize any block of text using GPT |
| **Translate** | Translate text to any language |
| **Sentiment** | Analyze sentiment (Positive/Negative/Neutral/Mixed) |
| **Rewrite** | Rewrite text in a style (formal, casual, concise, persuasive, technical) |

### Data (5)

| Tool | Description |
|------|-------------|
| **StockPrice** | Live stock prices, market cap, volume, and daily change |
| **CurrencyConvert** | Convert between 150+ currencies with live rates |
| **ParseCSV** | Parse and summarize CSV files or raw CSV data |
| **ParseJSON** | Parse and summarize JSON files or raw JSON data |
| **APIRequest** | Make HTTP requests (GET, POST, PUT, DELETE) to any API |

### Productivity (4)

| Tool | Description |
|------|-------------|
| **Todo** | Persistent todo list (add, list, done, remove) |
| **Notes** | Save, list, read, and delete named notes |
| **SendEmail** | Send emails via SMTP (requires config in .env) |
| **Timer** | Set countdown timers (up to 5 minutes) |

### Developer (5)

| Tool | Description |
|------|-------------|
| **Git** | Run any git command |
| **Regex** | Test regex patterns against text |
| **SQLite** | Execute SQL queries on SQLite databases |
| **Docker** | Run Docker commands |
| **FormatJSON** | Format and validate JSON |

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

Add your API keys:

```
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key

# Optional - for email sending
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your_email@gmail.com
# SMTP_PASS=your_app_password
```

- Get an OpenAI key at https://platform.openai.com/api-keys
- Get a SerpAPI key at https://serpapi.com/manage-api-key (free tier: 100 searches/month)

### 4. Run the agent

```bash
python3 langchain_agent.py
```

## Usage Examples

```
# Core
You: What's the weather in Miami?
You: Calculate sqrt(144) + pi
You: Search for the latest AI news
You: Look up quantum computing on Wikipedia
You: Scrape the top stories from https://news.ycombinator.com

# AI / LLM
You: Translate 'hello world' to Spanish, French, and Japanese
You: Analyze the sentiment of 'I love this product but the price is too high'
You: Rewrite 'hey the meeting is at 3pm dont be late' in a formal style
You: Summarize this article for me: [paste text]

# Data
You: What's the stock price of AAPL?
You: Convert 1000 USD to EUR
You: Parse the CSV file ~/data.csv

# Productivity
You: Add 'buy groceries' to my todo list
You: Save a note called meeting_notes with today's action items
You: Show my todo list

# Developer
You: Run git status
You: Test the regex '\d{3}-\d{4}' against '555-1234 and 123-4567'
You: Format this JSON: {"name":"test","active":true}
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
