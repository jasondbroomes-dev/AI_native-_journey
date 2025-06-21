from flask import Flask, render_template, request, jsonify
import random
import os
import json

app = Flask(__name__)

# --- Data Management ---
BUILTIN_SONG_LIBRARY_FILE = 'builtin_songs.json'
CUSTOM_VIBES_FILE = 'custom_vibes.json'
FAVORITES_FILE = 'favorite_songs.json'

def load_json(filename, default_data={}):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default_data
    return default_data

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize data files
builtin_song_library = load_json(BUILTIN_SONG_LIBRARY_FILE, {
    "chill": [("Lo-Fi Beats", "Chillhop Music", "https://youtu.be/5qap5aO4i9A")],
    "hype": [("Power", "Kanye West", "https://youtu.be/L53gjP-TtGE")],
    "sad": [("Someone Like You", "Adele", "https://youtu.be/hLQl3WQQoQ0")],
    "study": [("Clair de Lune", "Debussy", "https://youtu.be/CvFH_6DNRCY")],
    "dance": [("Uptown Funk", "Mark Ronson ft. Bruno Mars", "https://youtu.be/OPf0YbXqDm0")]
})
save_json(BUILTIN_SONG_LIBRARY_FILE, builtin_song_library)

custom_song_library = load_json(CUSTOM_VIBES_FILE)
favorites = load_json(FAVORITES_FILE, [])

keyword_map = {
    "relax": "chill", "peaceful": "calm", "lofi": "chill",
    "energized": "hype", "happy": "happy", "joy": "happy", "pump": "hype",
    "focused": "study", "bored": "study", "concentration": "study",
    "down": "sad", "heartbroken": "sad", "cry": "sad",
    "party": "party", "move": "dance", "groove": "dance",
    "love": "romantic", "affection": "romantic", "sweet": "romantic",
    "inspired": "motivational", "pump up": "motivational", "drive": "motivational",
    "cheerful": "happy", "bright": "happy",
    "sadness": "melancholy", "blue": "melancholy", "heartache": "melancholy",
    "celebrate": "party",
    "relaxing": "calm", "serene": "calm",
    "memories": "nostalgic", "remember": "nostalgic", "wistful": "nostalgic",
    "worried": "anxious", "nervous": "anxious", "tense": "anxious",
    "optimistic": "hopeful", "bright future": "hopeful", "expectation": "hopeful",
    "mad": "angry", "furious": "angry", "frustrated": "angry",
    "thoughtful": "reflective", "pensive": "reflective", "introspective": "reflective",
    "playful": "fun", "jolly": "fun", "lighthearted": "fun",
    "tired": "sleepy", "drowsy": "sleepy", "relaxed": "sleepy"
}

def get_full_library():
    # Combine built-in and custom libraries for recommendations
    library = builtin_song_library.copy()
    for vibe, songs in custom_song_library.items():
        if vibe in library:
            library[vibe].extend(songs)
        else:
            library[vibe] = songs
    return library

# --- Routes ---

@app.route('/')
def index():
    return render_template('song_vibe.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    vibe_input = request.json.get('vibe', '').lower()
    full_library = get_full_library()
    
    matched_vibe = keyword_map.get(vibe_input, vibe_input)
    
    if matched_vibe in full_library and full_library[matched_vibe]:
        song = random.choice(full_library[matched_vibe])
        return jsonify({
            'success': True, 
            'song': {'title': song[0], 'artist': song[1], 'link': song[2]},
            'vibe': matched_vibe
        })
    else:
        return jsonify({'success': False, 'message': "I couldn't match that vibe. Try something else!"})

@app.route('/add_vibe', methods=['POST'])
def add_vibe():
    data = request.json
    vibe = data.get('vibe', '').lower()
    title = data.get('title')
    artist = data.get('artist')
    link = data.get('link')

    if not all([vibe, title, artist, link]):
        return jsonify({'success': False, 'message': 'All fields are required.'})

    if vibe not in custom_song_library:
        custom_song_library[vibe] = []
    
    custom_song_library[vibe].append((title, artist, link))
    save_json(CUSTOM_VIBES_FILE, custom_song_library)
    
    return jsonify({'success': True, 'message': f"Added '{title}' to the '{vibe}' vibe!"})

@app.route('/get_favorites')
def get_favorites():
    return jsonify(favorites)

@app.route('/save_favorite', methods=['POST'])
def save_favorite():
    song_data = request.json.get('song')
    if song_data not in favorites:
        favorites.append(song_data)
        save_json(FAVORITES_FILE, favorites)
        return jsonify({'success': True, 'message': 'Saved to favorites!'})
    return jsonify({'success': False, 'message': 'Already in favorites.'})

@app.route('/get_vibes')
def get_vibes():
    return jsonify(list(get_full_library().keys()))

if __name__ == '__main__':
    app.run(debug=True, port=5002) 