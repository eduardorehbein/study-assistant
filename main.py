import os
from dotenv import load_dotenv
from core.planner_pipeline import PlannerPipeline

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return
    print("Welcome to Study Assistant!")
    topic = input("Enter the study topic: ")
    available_time = input("Enter your available time per study session (e.g., '60 minutes'): ")
    pipeline = PlannerPipeline(api_key)
    print("\nGenerating study calendar...\n")
    study_calendar = pipeline.run(topic, available_time)
    print("\n--- Study Calendar ---\n")
    print(study_calendar)

if __name__ == "__main__":
    main()
