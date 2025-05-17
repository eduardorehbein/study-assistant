import os
from dotenv import load_dotenv
from core.planner_pipeline import PlannerPipeline

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada nas variáveis de ambiente.")
        return
    print("Bem-vindo ao Assistente de Estudos!")
    topic = input("Digite o tema de estudo: ")
    available_time = input("Informe o tempo disponível por sessão de estudo (ex: '60 minutos'): ")
    pipeline = PlannerPipeline(api_key)
    study_calendar = pipeline.run(topic, available_time)
    print("--- Calendário de Estudos ---\n")
    print(study_calendar)
    print("---")

if __name__ == "__main__":
    main()
