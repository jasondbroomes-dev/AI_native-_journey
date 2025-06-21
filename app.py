from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Project data
projects = [
    {
        'name': 'Hello World',
        'filename': 'Hello_World.py',
        'description': 'Interactive greeting script with personalized messages',
        'features': ['User input handling', 'Personalized greetings', 'Name validation'],
        'category': 'Basic Python'
    },
    {
        'name': 'Budget Calculator',
        'filename': 'budget_calculator.py',
        'description': 'Personal finance management tool',
        'features': ['Income tracking', 'Expense management', 'Budget analysis'],
        'category': 'Finance'
    },
    {
        'name': 'Number Guessing Game',
        'filename': 'number_guessing_game.py',
        'description': 'Interactive number guessing game with hints',
        'features': ['Random number generation', 'User feedback', 'Score tracking'],
        'category': 'Games'
    },
    {
        'name': 'Greeting by Time',
        'filename': 'greeting_by_time.py',
        'description': 'Time-based greeting system',
        'features': ['Time detection', 'Contextual greetings', 'Dynamic messages'],
        'category': 'Utilities'
    },
    {
        'name': 'Dog Park',
        'filename': 'dog_park.py',
        'description': 'Dog park management simulation',
        'features': ['Object-oriented programming', 'Pet management', 'Interactive simulation'],
        'category': 'Simulation'
    }
]

@app.route('/')
def home():
    return render_template('index.html', projects=projects)

@app.route('/project/<filename>')
def view_project(filename):
    project = next((p for p in projects if p['filename'] == filename), None)
    if project:
        try:
            with open(filename, 'r') as f:
                code = f.read()
            return render_template('project.html', project=project, code=code)
        except FileNotFoundError:
            return render_template('project.html', project=project, code="File not found")
    return "Project not found", 404

@app.route('/api/projects')
def api_projects():
    return jsonify(projects)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 