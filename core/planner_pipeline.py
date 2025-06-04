from core.agents import ContentPlannerAgent, CalendarPlannerAgent

class PlannerPipeline:
    def __init__(self, ):
        self.content_planner_agent = ContentPlannerAgent()
        self.calendar_planner_agent = CalendarPlannerAgent()

    def run(self, topic: str, available_time_per_session: str) -> tuple[str, str]:
        # Optionally, keep a log for server-side information
        print(f"Gerando plano de estudos para o tema: '{topic}'...")
        teaching_plan = self.content_planner_agent.generate_plan(topic)
        print(f"Plano de estudos gerado para o tema: '{topic}'.")

        print(f"Gerando calendário de estudos para o tema: '{topic}'...")
        study_calendar = self.calendar_planner_agent.generate_calendar(teaching_plan, available_time_per_session)
        print(f"Calendário de estudos gerado para o tema: '{topic}'.")

        return teaching_plan, study_calendar
