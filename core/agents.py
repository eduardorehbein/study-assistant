import asyncio
from pathlib import Path
from google.adk.agents import Agent as AdkAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types as genai_types


def load_prompt(prompt_file_path: str) -> str:
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading prompt from {prompt_file_path}: {e}")
        return ""

class ContentPlannerAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.prompt_template = load_prompt(str(Path('prompts') / 'content_planner.md'))
        self.agent = AdkAgent(
            name="content_planner_agent",
            model=LiteLlm(model="gemini/gemini-flash"),
            description="Generates a content/teaching plan for a given topic.",
            instructions=self.prompt_template
        )
        self.session_service = InMemorySessionService()
        self.runner = Runner(session_service=self.session_service)

    async def generate_plan_async(self, topic: str) -> str:
        prompt = f"{self.prompt_template}\n#### Tema: {topic}"
        session_id = f"content_planner_{topic}"
        full_response = ""
        try:
            async for event in self.runner.run_async(
                agent=self.agent,
                session_id=session_id,
                message=genai_types.Content(parts=[genai_types.Part.from_text(prompt)]),
            ):
                if event.is_llm_response():
                    full_response += event.data["text"]
                if event.is_final_response():
                    return full_response.strip() or event.data.get("text", "")
                elif event.is_error():
                    print(f"Error: {event.data['message']}")
                    return "[Error generating teaching plan]"
        except Exception as e:
            print(f"Error generating teaching plan: {e}")
            return "[Error generating teaching plan]"

    def generate_plan(self, topic: str) -> str:
        return asyncio.run(self.generate_plan_async(topic))

class CalendarPlannerAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.prompt_template = load_prompt(str(Path('prompts') / 'calendar_planner.md'))
        self.agent = AdkAgent(
            name="calendar_planner_agent",
            model=LiteLlm(model="gemini/gemini-flash"),
            description="Generates a study calendar based on a teaching plan and available time per session.",
            instructions=self.prompt_template
        )
        self.session_service = InMemorySessionService()
        self.runner = Runner(session_service=self.session_service)

    async def generate_calendar_async(self, teaching_plan: str, available_time_per_session: str) -> str:
        prompt = (
            f"{self.prompt_template}\n#### Plano de ensino:\n{teaching_plan}\n#### Tempo disponível por seção: {available_time_per_session}"
        )
        session_id = f"calendar_planner_{hash(teaching_plan)}"
        full_response = ""
        try:
            async for event in self.runner.run_async(
                agent=self.agent,
                session_id=session_id,
                message=genai_types.Content(parts=[genai_types.Part.from_text(prompt)]),
            ):
                if event.is_llm_response():
                    full_response += event.data["text"]
                if event.is_final_response():
                    return full_response.strip() or event.data.get("text", "")
                elif event.is_error():
                    print(f"Error: {event.data['message']}")
                    return "[Error generating study calendar]"
        except Exception as e:
            print(f"Error generating study calendar: {e}")
            return "[Error generating study calendar]"

    def generate_calendar(self, teaching_plan: str, available_time_per_session: str) -> str:
        return asyncio.run(self.generate_calendar_async(teaching_plan, available_time_per_session))
