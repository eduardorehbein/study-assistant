import os
from flask import Flask, render_template, request, session, redirect, url_for, make_response # Added make_response
from dotenv import load_dotenv
from core.planner_pipeline import PlannerPipeline
import re # For sanitizing filename

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure a secret key for session management
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev_fallback_secret_key')

# Load Google API Key
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    print("CRITICAL: GOOGLE_API_KEY not found in environment variables. The application may not work correctly.")

@app.route('/')
@app.route('/index')
def index():
    # Pass error message from session if redirected from /generate
    error_message = session.pop('error_message', None)
    return render_template('index.html', error_message=error_message)

@app.route('/generate', methods=['POST'])
def generate():
    study_theme = request.form.get('study_theme')
    study_time_days_str = request.form.get('study_time')

    if not study_theme or not study_time_days_str:
        session['error_message'] = "Ambos os campos são obrigatórios."
        return redirect(url_for('index'))

    try:
        study_time_days = int(study_time_days_str)
        if study_time_days <= 0:
            session['error_message'] = "O tempo disponível deve ser um número positivo."
            return redirect(url_for('index'))
    except ValueError:
        session['error_message'] = "O tempo disponível deve ser um número válido."
        return redirect(url_for('index'))

    # Construct the time_available string for the pipeline.
    # The pipeline's CalendarPlannerAgent expects a string describing session duration.
    # For now, we'll adapt the "days" input. This might need refinement based on agent's prompt.
    # Example: "10 days total" or adapt to "X hours per day if total days is Y"
    # For simplicity, let's assume the agent can interpret "N days" as total duration for planning.
    time_available_string = f"{study_time_days} dias"

    try:
        pipeline = PlannerPipeline()
        # The pipeline now returns two values: syllabus and calendar_csv_string
        syllabus, calendar_csv_string = pipeline.run(study_theme, time_available_string)

        session['calendar_csv_data'] = calendar_csv_string
        session['study_theme'] = study_theme # For naming the CSV file

        # For displaying on results.html, we might need to parse the CSV string
        # For now, pass it directly. The template will handle presentation.
        return render_template('results.html', syllabus=syllabus, calendar_data=calendar_csv_string, study_theme=study_theme)

    except Exception as e:
        print(f"Error during pipeline execution: {e}") # Log the error server-side
        session['error_message'] = f"Ocorreu um erro ao gerar o plano: {str(e)}"
        return redirect(url_for('index'))

@app.route('/download_csv')
def download_csv():
    calendar_csv_data = session.get('calendar_csv_data')
    study_theme = session.get('study_theme', 'estudo') # Default theme if not in session

    if calendar_csv_data:
        # Sanitize the study_theme to create a safe filename
        safe_theme_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', study_theme)
        if not safe_theme_filename: # Handle case where theme was all non-alphanumeric
            safe_theme_filename = "estudo"

        filename = f"{safe_theme_filename}_calendar.csv"

        response = make_response(calendar_csv_data)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        # Optional: Add an error message for the user
        session['error_message'] = "Nenhum calendário para baixar. Por favor, gere um plano primeiro."
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
