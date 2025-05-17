from core.agents import ContentPlannerAgent, CalendarPlannerAgent
from tools.search_tool import SearchTool

class PlannerPipeline:
    def __init__(self, api_key: str):
        self.search_tool = SearchTool()
        self.content_planner_agent = ContentPlannerAgent(api_key, self.search_tool)
        self.calendar_planner_agent = CalendarPlannerAgent(api_key)

    def run(self, topic: str, available_time_per_session: str) -> str:
        print("Generating teaching plan...")
        teaching_plan = self.content_planner_agent.generate_plan(topic)
        print("Teaching plan generated.\n")
        print("Generating study calendar...")
        study_calendar = self.calendar_planner_agent.generate_calendar(teaching_plan, available_time_per_session)
        print("Study calendar generated.\n")
        return study_calendar
