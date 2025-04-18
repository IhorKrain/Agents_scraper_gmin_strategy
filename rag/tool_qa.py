from crewai.tools import tool, BaseTool
from rag.qa_chain import qa_chain

@tool("query_strategy_tool")
def qa_tool(question: str) -> str:
    """Odpowiada na pytania dotyczące strategii na podstawie danych z RAG"""
    return qa_chain(question)