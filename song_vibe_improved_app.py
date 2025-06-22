from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

# --- Data Files ---
SONG_LIBRARY_FILE = 'song_library.json'
FAVORITES_FILE = 'favorites.txt'

# --- Helper Functions ---

def load_song_library(filename=SONG_LIBRARY_FILE):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_song_library(library, filename=SONG_LIBRARY_FILE):
    with open(filename, "w") as f:
        json.dump(library, f, indent=2)

def load_favorites(filename=FAVORITES_FILE):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def save_favorite(song_str, filename=FAVORITES_FILE):
    favorites = load_favorites(filename)
    if song_str not in favorites:
        with open(filename, "a") as f:
            f.write(song_str + "\n")
        return True
    return False

def match_vibe(user_input, keyword_map, song_library):
    user_input = user_input.lower()
    if user_input in song_library:
        return user_input
    elif user_input in keyword_map:
        return keyword_map[user_input]
    else:
        return None

def recommend_song(mood, song_library):
    if mood not in song_library or not song_library[mood]:
        return None
    return random.choice(song_library[mood])

# --- Initial Data ---

keyword_map = {
    "chill": "calm",
    "relax": "calm",
    "study": "focus",
    "work": "focus",
    "hype": "energetic",
    "sad": "melancholy",
    "happy": "joyful",
    "energized": "energetic",
    "peaceful": "calm",
    "focused": "focus",
    "melancholic": "melancholy",
    "joyful": "joyful",
    "cheerful": "joyful",
    "down": "melancholy",
    "upbeat": "energetic",
    "motivated": "energetic"
}

# Load or initialize song library
song_library = load_song_library()
if not song_library:
    # Default songs if none saved yet
    song_library = {
        "calm": [
            {"title": "Weightless", "artist": "Marconi Union", "link": "https://youtu.be/UfcAVejslrU"},
            {"title": "Night Owl", "artist": "Galimatias", "link": "https://youtu.be/ZFnzNfVfSNY"},
            {"title": "River Flows In You", "artist": "Yiruma", "link": "https://youtu.be/7maJOI3QMu0"}
        ],
        "focus": [
            {"title": "Clair de Lune", "artist": "Debussy", "link": "https://youtu.be/CvFH_6DNRCY"},
            {"title": "Study Music", "artist": "Various Artists", "link": "https://youtu.be/WPni755-Krg"},
            {"title": "Merry Christmas Mr. Lawrence", "artist": "Ryuichi Sakamoto", "link": "https://youtu.be/J--TDEHizVA"}
        ],
        "energetic": [
            {"title": "Eye of the Tiger", "artist": "Survivor", "link": "https://youtu.be/btPJPFnesV4"},
            {"title": "Stronger", "artist": "Kanye West", "link": "https://youtu.be/PiTn5h1t73g"},
            {"title": "Power", "artist": "Kanye West", "link": "https://youtu.be/L53gjP-TtGE"}
        ],
        "melancholy": [
            {"title": "Someone Like You", "artist": "Adele", "link": "https://youtu.be/hLQl3WQQoQ0"},
            {"title": "Everybody Hurts", "artist": "R.E.M.", "link": "https://youtu.be/ijZRCIrTgQc"},
            {"title": "Fix You", "artist": "Coldplay", "link": "https://youtu.be/k4V3Mo61fJM"}
        ],
        "joyful": [
            {"title": "Happy", "artist": "Pharrell Williams", "link": "https://youtu.be/ZbZSe6N_BXs"},
            {"title": "Good Vibrations", "artist": "The Beach Boys", "link": "https://youtu.be/Eab_beh07HU"},
            {"title": "Walking on Sunshine", "artist": "Katrina & The Waves", "link": "https://youtu.be/iPUmE-tne5U"}
        ],
    }
    save_song_library(song_library)

# --- Routes ---

@app.route('/')
def index():
    return render_template('song_vibe_improved.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    data = request.json
    user_input = data.get('vibe', '').strip().lower()
    
    if not user_input:
        return jsonify({'success': False, 'message': 'Please enter a vibe!'})
    
    mood = match_vibe(user_input, keyword_map, song_library)
    if not mood:
        return jsonify({'success': False, 'message': f"Sorry, I don't recognize '{user_input}'. Try another vibe or add it!"})
    
    song = recommend_song(mood, song_library)
    if not song:
        return jsonify({'success': False, 'message': f"No songs found for mood '{mood}'."})
    
    song_str = f"{song['title']} by {song['artist']} ({song['link']})"
    
    return jsonify({
        'success': True,
        'song': song,
        'mood': mood,
        'song_str': song_str
    })

@app.route('/save_favorite', methods=['POST'])
def save_favorite_route():
    data = request.json
    song_str = data.get('song_str', '')
    
    if save_favorite(song_str):
        return jsonify({'success': True, 'message': 'Saved to favorites!'})
    else:
        return jsonify({'success': False, 'message': 'Already in favorites!'})

@app.route('/get_favorites')
def get_favorites():
    favorites = load_favorites()
    return jsonify(favorites)

@app.route('/add_mood', methods=['POST'])
def add_mood():
    data = request.json
    mood = data.get('mood', '').strip().lower()
    songs = data.get('songs', [])
    
    if not mood or not songs:
        return jsonify({'success': False, 'message': 'Mood name and songs are required!'})
    
    if mood in song_library:
        song_library[mood].extend(songs)
        message = f"Added {len(songs)} songs to existing mood '{mood}'."
    else:
        song_library[mood] = songs
        message = f"Created new mood '{mood}' with {len(songs)} songs."
    
    save_song_library(song_library)
    return jsonify({'success': True, 'message': message})

@app.route('/get_moods')
def get_moods():
    return jsonify(list(song_library.keys()))

@app.route('/get_keywords')
def get_keywords():
    return jsonify(keyword_map)

if __name__ == '__main__':
    app.run(debug=True, port=5004) 