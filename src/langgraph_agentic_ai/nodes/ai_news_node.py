from src.langgraph_agentic_ai.state.state import State
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self, llm):
        self.tavily = TavilyClient()
        self.llm = llm
        self.state = {}

    def fetch_news(self, state:dict)->dict:
        frequency = state["messages"][0].content.lower()
        time_range_map = {"daily": 'd',
                          "weekly": 'w',
                          "monthly": 'm',
                          "yearly": 'y'}
        days_map = {"daily": 1,
                    "weekly":7,
                    "monthly":30,
                    "year":366}
        print("fetch news worked well !")
        response = self.tavily.search(
            query="Top Artificial Intelligence news India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
        )
        state["news_data"] = response.get('results',[])
        self.state["news_data"] = state["news_data"]
        self.state["frequency"] = frequency
        print("fetch news worked well")
        return self.state
    
    def summarize_news(self, state:dict)->dict:
        news_data = self.state["news_data"]
        prompt_template = ChatPromptTemplate.from_messages([
            ("system",
             """Summarize AI news articles in markdown format,
                Make sure it doesn't include charmap codec characters,
                For each item include
                - Date in **YYYY-MM-DD*** format in IST timezone
                - Concise sentences summary for latest news, It should have atleast two lines of text
                - Sort news by date wise (latest first)
                - Source url as link
                Use format:
                 [Date]
                [Summary](URL)
             """),
             ("user", "Articles:\n{articles}")]
        )
        articles_str = "\n\n".join([
                f"Content: {item.get('content','')}\n URL:{item.get('url', '')}\n Date:{item.get('published_date','')}"
                for item in news_data
            ]
        )
        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state["summary"]=response.content
        self.state["summary"]=state["summary"]
        print("summarize worked well")
        return self.state
    
    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        # Write as ASCII, replacing problematic characters
        with open(filename, 'w', encoding='ascii', errors='replace') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename']=filename
        print("save result worked well")
        return self.state