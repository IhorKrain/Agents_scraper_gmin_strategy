from crewai import Crew, Process
from .agents import strategia_checker, zakres_checker, jednostka_checker
from .tasks import strategia_task, zakres_task, jednostka_task

crew = Crew(
    agents=[
        strategia_checker,
        zakres_checker,
        jednostka_checker
    ],
    tasks=[
        strategia_task,
        zakres_task,
        jednostka_task
    ],
    process=Process.sequential,  # możesz też przetestować Process.hierarchical
    verbose=True
)
