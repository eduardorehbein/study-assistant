import asyncio
from pathlib import Path
from google.adk.agents import Agent as AdkAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types as genai_types
from google.adk.tools import google_search


def load_prompt(prompt_file_path: str) -> str:
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading prompt from {prompt_file_path}: {e}")
        return ""


class ContentPlannerAgent:
    def __init__(self):
        self.prompt_template = load_prompt(
            str(Path('prompts') / 'content_planner.md'))
        self.agent = AdkAgent(
            name="content_planner_agent",
            model="gemini-2.0-flash",
            description="Generates a content/teaching plan for a given topic.",
            instruction=self.prompt_template,
            tools=[google_search]
        )

    async def generate_plan_async(self, topic: str) -> str:
        prompt = f"\n\n#### Tema\n\n{topic}"
        user_and_session_id = f"content_planner_{topic}"

        session_service = InMemorySessionService()
        await session_service.create_session(
            app_name=self.agent.name,
            user_id=user_and_session_id,
            session_id=user_and_session_id)
        runner = Runner(
            agent=self.agent,
            app_name=self.agent.name,
            session_service=session_service
        )
        content = genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=prompt)])

        full_response = ""
        try:
            async for event in runner.run_async(
                user_id=user_and_session_id,
                session_id=user_and_session_id,
                new_message=content,
            ):
                if event.is_final_response():
                    for part in event.content.parts:
                        if part.text is not None:
                            full_response += part.text
                            full_response += "\n"
        except Exception as e:
            print(f"Error in generate_plan_async for topic '{topic}': {e}")
            return "[Error generating teaching plan]"
        return full_response.strip()

    def generate_plan(self, topic: str) -> str:
        return asyncio.run(self.generate_plan_async(topic))


class CalendarPlannerAgent:
    def __init__(self):
        self.prompt_template = load_prompt(
            str(Path('prompts') / 'calendar_planner.md'))
        self.agent = AdkAgent(
            name="calendar_planner_agent",
            model="gemini-2.0-flash",
            description="Generates a study calendar based on a teaching plan and available time per session.",
            instruction=self.prompt_template
        )

    async def generate_calendar_async(self, teaching_plan: str, available_time_per_session: str) -> str:
        prompt = (
            f"\n\n#### Plano de ensino:\n\n{teaching_plan}\n\n#### Tempo disponível por seção:\n\n{available_time_per_session}"
        )
        user_and_session_id = f"calendar_planner_{hash(teaching_plan)}"

        session_service = InMemorySessionService()
        await session_service.create_session(
            app_name=self.agent.name,
            user_id=user_and_session_id,
            session_id=user_and_session_id)
        runner = Runner(
            agent=self.agent,
            app_name=self.agent.name,
            session_service=session_service
        )
        content = genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=prompt)])

        full_response = ""
        try:
            async for event in runner.run_async(
                user_id=user_and_session_id,
                session_id=user_and_session_id,
                new_message=content,
            ):
                if event.is_final_response():
                    for part in event.content.parts:
                        if part.text is not None:
                            full_response += part.text
                            full_response += "\n"
        except Exception as e:
            print(f"Error in generate_calendar_async: {e}")
            return "[Error generating study calendar]"
        return full_response.strip()

    def generate_calendar(self, teaching_plan: str, available_time_per_session: str) -> str:
        return asyncio.run(self.generate_calendar_async(teaching_plan, available_time_per_session))
