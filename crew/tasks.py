from crewai import Task
from .agents import strategia_checker, zakres_checker, jednostka_checker
from rag.qa_chain import qa_chain
from rag.tool_qa import QueryStrategyTool

query_tool = QueryStrategyTool()
# zakładamy, że masz funkcję rag jako narzędzie

# Zadanie 1: Czy dokument to strategia rozwoju?

strategia_task = Task(
    description=(
        "Odpowiedz na pytanie: czy dokument PDF jest strategią rozwoju gminy lub miasta? "
        "Nie uznawaj za strategię dokumentów typu: plan działań, raport diagnostyczny, plan sektorowy (np. transportowy), "
        "ani dokumentów bez wyraźnych celów strategicznych. "
        "Uwzględnij obecność takich elementów jak: wizja, cele strategiczne, analiza SWOT, kierunki działań, plan wdrażania. "
        "Jeśli dokument zawiera wszystkie te elementy, uznaj go za strategię i uzasadnij decyzję."
    ),
    expected_output=(
        "Odpowiedź TAK lub NIE, oraz krótkie uzasadnienie decyzji na podstawie dokumentu."
    ),
    agent=strategia_checker,
    tools=[query_tool]
)

# Zadanie 2: Zakres czasowy dokumentu
zakres_task = Task(
    description=(
        "Odszukaj, jakiego okresu dotyczy dokument. Znajdź dokładny zakres lat np. 2014–2020, 2021–2030 lub "
        "formę otwartą np. 2018–... jeśli data końcowa nie jest określona. "
        "Pomiń daty niepowiązane z okresem obowiązywania strategii (np. daty publikacji, konsultacji, itp.)."
    ),
    expected_output="Zakres lat w formacie: RRRR–RRRR lub RRRR–...",
    agent=zakres_checker,
    tools=[query_tool]
)

# Zadanie 3: Jakiej jednostki dotyczy dokument?
jednostka_task = Task(
    description=(
        "Ustal, jakiej jednostki samorządu dotyczy dokument. Odpowiedz jednoznacznie, np.: "
        "Gmina Wólka, Miasto Lublin, Powiat lubelski, Województwo lubelskie. "
        "Jeśli w dokumencie występuje kilka nazw — wybierz główną, dla której dokument został sporządzony."
    ),
    expected_output="Nazwa jednostki w formacie: Gmina X, Miasto Y, Powiat Z, itp.",
    agent=jednostka_checker,
    tools=[query_tool]
)
