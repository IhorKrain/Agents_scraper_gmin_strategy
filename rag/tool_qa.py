from rag.qa_chain import qa_chain
from crewai.tools import tool


@tool("query_strategy_tool")
def query_strategy_tool(query: str | dict) -> str:
    """
    Narzędzie do odpowiadania na pytania dotyczące strategii na podstawie danych z RAG.
    :param query: pytanie w formie tekstu
    :return: odpowiedź na podstawie kontekstu
    """
    if isinstance(query, dict):
        query = query.get("description", "")  # Попробуй вытащить текст
    return qa_chain(query)

