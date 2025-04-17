# rag/tool_qa.py

from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel
from rag.qa_chain import qa_chain

class QueryInput(BaseModel):
    question: str

class QueryStrategyTool(BaseTool):
    name = "query_strategy_tool"
    description = "Odpowiada na pytania dotyczące strategii na podstawie danych z RAG"
    args_schema: Type[BaseModel] = QueryInput

    def _run(self, question: str) -> str:
        return qa_chain(question)

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Nie obsługuję trybu asynchronicznego.")
