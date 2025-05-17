from pathlib import Path
from typing import Optional
import google.generativeai as genai


def load_prompt(prompt_file_path: str) -> str:
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading prompt from {prompt_file_path}: {e}")
        return ""

class Agent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)

class ContentPlannerAgent(Agent):
    def __init__(self, api_key: str, search_tool):
        super().__init__(api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.search_tool = search_tool
        self.prompt_template = load_prompt(str(Path('prompts') / 'content_planner.md'))

    def generate_plan(self, topic: str) -> str:
        search_results = self.search_tool.execute_search(topic)
        prompt = f"{self.prompt_template}\n\nTopic: {topic}\n\nSearch Results: {search_results}"
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip() if hasattr(response, 'text') else str(response)
        except Exception as e:
            print(f"Error generating teaching plan: {e}")
            return "[Error generating teaching plan]"

class CalendarPlannerAgent(Agent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.prompt_template = load_prompt(str(Path('prompts') / 'calendar_planner.md'))

    def generate_calendar(self, teaching_plan: str, available_time_per_session: str) -> str:
        prompt = (
            f"{self.prompt_template}\n\nTeaching Plan:\n{teaching_plan}\n\nAvailable Time Per Session: {available_time_per_session}"
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip() if hasattr(response, 'text') else str(response)
        except Exception as e:
            print(f"Error generating study calendar: {e}")
            return "[Error generating study calendar]"
