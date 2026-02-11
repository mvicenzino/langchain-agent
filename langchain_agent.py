import os
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from serpapi import GoogleSearch
import requests
from bs4 import BeautifulSoup
import wikipedia

# Load API keys from .env
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


# --- Tool Functions ---

def search(query: str) -> str:
    """Search the web using SerpAPI."""
    try:
        params = {
            "q": query,
            "api_key": os.environ.get("SERPAPI_API_KEY"),
            "num": 5,
        }
        results = GoogleSearch(params).get_dict()
        if "answer_box" in results:
            box = results["answer_box"]
            if "answer" in box:
                return box["answer"]
            if "snippet" in box:
                return box["snippet"]
        if "organic_results" in results:
            snippets = []
            for r in results["organic_results"][:3]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                link = r.get("link", "")
                snippets.append(f"{title}\n{snippet}\n{link}")
            return "\n\n".join(snippets)
        return "No results found."
    except Exception as e:
        return f"Search error: {e}"


def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        expr = _clean_path(expression)
        allowed = {"__builtins__": {}}
        import math
        allowed.update({k: getattr(math, k) for k in dir(math) if not k.startswith("_")})
        result = eval(expr, allowed)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def get_current_date(input: str = "") -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def wiki_lookup(query: str) -> str:
    """Look up a topic on Wikipedia."""
    try:
        page = wikipedia.page(query, auto_suggest=True)
        return page.summary[:1500]
    except wikipedia.DisambiguationError as e:
        return f"Disambiguation: did you mean one of these? {', '.join(e.options[:5])}"
    except wikipedia.PageError:
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        return f"Wikipedia error: {e}"


def fetch_webpage(url: str) -> str:
    """Fetch and extract text content from a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(_clean_input(url), headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:3000]
    except Exception as e:
        return f"Error fetching URL: {e}"


def weather(location: str) -> str:
    """Get current weather for a location using wttr.in."""
    try:
        loc = _clean_input(location)
        resp = requests.get(f"https://wttr.in/{loc}?format=j1", timeout=20)
        resp.raise_for_status()
        data = resp.json()
        current = data["current_condition"][0]
        desc = current["weatherDesc"][0]["value"]
        temp_f = current["temp_F"]
        temp_c = current["temp_C"]
        humidity = current["humidity"]
        wind_mph = current["windspeedMiles"]
        feels_f = current["FeelsLikeF"]
        area = data["nearest_area"][0]["areaName"][0]["value"]
        return f"{area}: {desc}, {temp_f}°F ({temp_c}°C), Feels like {feels_f}°F, Humidity {humidity}%, Wind {wind_mph} mph"
    except Exception as e:
        return f"Weather error: {e}"


def run_python(code: str) -> str:
    """Execute Python code and return the output."""
    try:
        cleaned = _clean_input(code)
        result = subprocess.run(
            ["python3", "-c", cleaned],
            capture_output=True, text=True, timeout=15
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            output += f"\nError: {result.stderr.strip()}"
        return output if output else "Code executed with no output."
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (15s limit)."
    except Exception as e:
        return f"Error: {e}"


def _clean_path(s: str) -> str:
    """Strip backticks, quotes, and whitespace from file paths."""
    return s.strip().strip("`").strip("'").strip('"').strip()


def _clean_input(s: str) -> str:
    """Strip backticks and matching outer quotes from inputs."""
    s = s.strip().strip("`").strip()
    # Remove matching outer quotes (single or double)
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        s = s[1:-1]
    return s


def read_file(filepath: str) -> str:
    """Read the contents of a local file."""
    try:
        path = os.path.expanduser(_clean_path(filepath))
        with open(path, "r") as f:
            content = f.read()
        if len(content) > 3000:
            return content[:3000] + "\n... (truncated)"
        return content
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(input_str: str) -> str:
    """Write content to a file. Input format: filepath|||content"""
    try:
        parts = input_str.split("|||", 1)
        if len(parts) != 2:
            return "Error: Input must be in format 'filepath|||content'"
        filepath = os.path.expanduser(_clean_path(parts[0]))
        content = parts[1]
        with open(filepath, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"


def shell_command(command: str) -> str:
    """Run a shell command and return its output."""
    try:
        cmd = _clean_input(command)
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=15
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            output += f"\nError: {result.stderr.strip()}"
        return output if output else "Command executed with no output."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out (15s limit)."
    except Exception as e:
        return f"Error: {e}"


# --- Tools ---

tools = [
    Tool(name="Search", func=search,
         description="Search the web for current information. Input: a search query."),
    Tool(name="Calculator", func=calculator,
         description="Evaluate math expressions. Supports functions like sqrt(), sin(), pi, etc. Input: a math expression."),
    Tool(name="GetDateTime", func=get_current_date,
         description="Get the current date and time. Input can be any string or empty."),
    Tool(name="Wikipedia", func=wiki_lookup,
         description="Look up a topic on Wikipedia for factual/encyclopedic info. Input: a topic name."),
    Tool(name="WebScraper", func=fetch_webpage,
         description="Fetch and read the text content of a webpage. Input: a full URL."),
    Tool(name="Weather", func=weather,
         description="Get current weather for a location. Input: city name or location."),
    Tool(name="PythonREPL", func=run_python,
         description="Execute Python code and return output. Input: Python code as a string."),
    Tool(name="ReadFile", func=read_file,
         description="Read the contents of a local file. Input: file path."),
    Tool(name="WriteFile", func=write_file,
         description="Write content to a local file. Input format: filepath|||content"),
    Tool(name="Shell", func=shell_command,
         description="Run a shell command and return its output. Input: a shell command string."),
]

# Set up the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ReAct prompt template
prompt = PromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
)

# Create the agent
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=25)

# Interactive loop
if __name__ == "__main__":
    print("LangChain Agent Ready!")
    print("Tools: Search, Calculator, GetDateTime, Wikipedia, WebScraper, Weather, PythonREPL, ReadFile, WriteFile, Shell")
    print("Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        response = executor.invoke({"input": user_input})
        print(f"\nAgent: {response['output']}\n")
