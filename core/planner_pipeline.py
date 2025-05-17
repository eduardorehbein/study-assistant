from core.agents import ContentPlannerAgent, CalendarPlannerAgent

class PlannerPipeline:
    def __init__(self, api_key: str):
        self.content_planner_agent = ContentPlannerAgent(api_key)
        self.calendar_planner_agent = CalendarPlannerAgent(api_key)

    def run(self, topic: str, available_time_per_session: str) -> str:
        print("\nGerando plano de estudos...")
        teaching_plan = self.content_planner_agent.generate_plan(topic)
        print("Plano de estudos gerado.\n")
        print("--- Plano de Estudos ---\n")
        print(teaching_plan)
        print("---")
        print("\nGerando calendário de estudos...")
        study_calendar = self.calendar_planner_agent.generate_calendar(teaching_plan, available_time_per_session)
        print("Calendário de estudos gerado.\n")
        return study_calendar
