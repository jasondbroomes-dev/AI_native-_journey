from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_greeting(name):
    """
    Returns a personalized greeting based on the name.
    """
    name_lower = name.lower()
    name_display = name.capitalize()
    
    if name_lower == "jason":
        return f"Hey, it's the Marvellous AI Trainee, {name_display}!"
    elif name_lower == "alex":
        return f"Salute, Captain {name_display}!"
    elif name_lower == "maya":
        return f"{name_display} the Marvelous has arrived!"
    elif name_lower == "sophia":
        return f"Welcome, the Brilliant {name_display}!"
    else:
        return f"Hello, {name_display}! Nice to meet you."

@app.route('/')
def home():
    return render_template('hello_web.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form.get('name', '')
    if name:
        greeting = get_greeting(name)
        return jsonify({'greeting': greeting})
    return jsonify({'greeting': 'Please enter a name!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001) 