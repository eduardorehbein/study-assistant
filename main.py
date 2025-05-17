import os
import csv
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

    # Salvar resultado em CSV na pasta 'results'
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    filename = os.path.join(results_dir, f"{topic}.csv")
    # Supondo que study_calendar seja uma string CSV ou lista de listas
    if isinstance(study_calendar, str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(study_calendar)
    elif isinstance(study_calendar, list):
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(study_calendar)
    print(f"\nCalendário salvo em: {filename}")

if __name__ == "__main__":
    main()
