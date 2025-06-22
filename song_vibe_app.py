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
    "chill": [
        ("Blinding Lights", "The Weeknd", "https://youtu.be/4NRXx6U8ABQ"),
        ("Stay With Me", "Calvin Harris", "https://youtu.be/3TjqjMkHZeQ"),
        ("Midnight City", "M83", "https://youtu.be/dX3k_QDnzHE"),
        ("Redbone", "Childish Gambino", "https://youtu.be/Kp7eSUU9oy8"),
        ("The Less I Know The Better", "Tame Impala", "https://youtu.be/8X8X8X8X8X8"),
        ("Lofi Beats", "Chillhop Music", "https://youtu.be/5qap5aO4i9A")
    ],
    "hype": [
        ("Power", "Kanye West", "https://youtu.be/L53gjP-TtGE"),
        ("Stronger", "Kanye West", "https://youtu.be/PsO6ZnUZI0g"),
        ("Can't Hold Us", "Macklemore & Ryan Lewis", "https://youtu.be/Sv6dMFF_yts"),
        ("Titanium", "David Guetta ft. Sia", "https://youtu.be/JRfuAukYTKg"),
        ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "https://youtu.be/OPf0YbXqDm0"),
        ("Shake It Off", "Taylor Swift", "https://youtu.be/nfWlot6h_JM")
    ],
    "sad": [
        ("Someone Like You", "Adele", "https://youtu.be/hLQl3WQQoQ0"),
        ("All of Me", "John Legend", "https://youtu.be/450p7goxZqg"),
        ("Say Something", "A Great Big World", "https://youtu.be/-2U0Ivkn2Ds"),
        ("Fix You", "Coldplay", "https://youtu.be/k4V3Mo61fJM"),
        ("Skinny Love", "Bon Iver", "https://youtu.be/8CdcCD5V-d8"),
        ("Mad World", "Gary Jules", "https://youtu.be/4N3N1MlvVc4")
    ],
    "study": [
        ("Clair de Lune", "Debussy", "https://youtu.be/CvFH_6DNRCY"),
        ("River Flows In You", "Yiruma", "https://youtu.be/7maJOI3QMu0"),
        ("Comptine d'un autre été", "Yann Tiersen", "https://youtu.be/nvHqJjW0dyY"),
        ("Experience", "Ludovico Einaudi", "https://youtu.be/hhEJJkOX0Hs"),
        ("Nuvole Bianche", "Ludovico Einaudi", "https://youtu.be/6ZdJcKvG_3k"),
        ("Weightless", "Marconi Union", "https://youtu.be/UfcAVejslrU")
    ],
    "dance": [
        ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "https://youtu.be/OPf0YbXqDm0"),
        ("Get Lucky", "Daft Punk ft. Pharrell", "https://youtu.be/5NV6Rdv1a3I"),
        ("Blurred Lines", "Robin Thicke ft. T.I.", "https://youtu.be/yyDUC1LUXSU"),
        ("We Found Love", "Rihanna ft. Calvin Harris", "https://youtu.be/0I647GU3Jsc"),
        ("Call Me Maybe", "Carly Rae Jepsen", "https://youtu.be/fWNaR-rxAic"),
        ("Party Rock Anthem", "LMFAO", "https://youtu.be/KQ6zr6kCPj8")
    ],
    "happy": [
        ("Happy", "Pharrell Williams", "https://youtu.be/ZbZSe6N_BXs"),
        ("Good Time", "Owl City & Carly Rae Jepsen", "https://youtu.be/9Sc-ir2UaGU"),
        ("Walking on Sunshine", "Katrina & The Waves", "https://youtu.be/iPUmE-tne5U"),
        ("I Gotta Feeling", "The Black Eyed Peas", "https://youtu.be/uSD4vsh1zBA"),
        ("Best Day of My Life", "American Authors", "https://youtu.be/Y66j_BUCBMY"),
        ("Count on Me", "Bruno Mars", "https://youtu.be/6k8cpUkKK8c")
    ],
    "romantic": [
        ("All of Me", "John Legend", "https://youtu.be/450p7goxZqg"),
        ("Perfect", "Ed Sheeran", "https://youtu.be/2Vv-BfVoq4g"),
        ("Just the Way You Are", "Bruno Mars", "https://youtu.be/LjhCEhWiKXk"),
        ("A Thousand Years", "Christina Perri", "https://youtu.be/rtOvBOTyX00"),
        ("Marry Me", "Train", "https://youtu.be/ghZt2cILcCU"),
        ("Thinking Out Loud", "Ed Sheeran", "https://youtu.be/lp-EO5I60KA")
    ],
    "motivational": [
        ("Eye of the Tiger", "Survivor", "https://youtu.be/btPJPFnesV4"),
        ("We Will Rock You", "Queen", "https://youtu.be/-tJYN-eG1zk"),
        ("Don't Stop Believin'", "Journey", "https://youtu.be/1k8craCGpgs"),
        ("Lose Yourself", "Eminem", "https://youtu.be/_Yhyp-_hX2s"),
        ("Hall of Fame", "The Script ft. will.i.am", "https://youtu.be/mk48xRzuNvA"),
        ("The Climb", "Miley Cyrus", "https://youtu.be/NG2zyeVRcbs")
    ],
    "party": [
        ("Party Rock Anthem", "LMFAO", "https://youtu.be/KQ6zr6kCPj8"),
        ("I Gotta Feeling", "The Black Eyed Peas", "https://youtu.be/uSD4vsh1zBA"),
        ("We Found Love", "Rihanna ft. Calvin Harris", "https://youtu.be/0I647GU3Jsc"),
        ("Call Me Maybe", "Carly Rae Jepsen", "https://youtu.be/fWNaR-rxAic"),
        ("Gangnam Style", "PSY", "https://youtu.be/9bZkp7q19f0"),
        ("Shake It Off", "Taylor Swift", "https://youtu.be/nfWlot6h_JM")
    ],
    "calm": [
        ("Weightless", "Marconi Union", "https://youtu.be/UfcAVejslrU"),
        ("Claire de Lune", "Debussy", "https://youtu.be/CvFH_6DNRCY"),
        ("River Flows In You", "Yiruma", "https://youtu.be/7maJOI3QMu0"),
        ("Experience", "Ludovico Einaudi", "https://youtu.be/hhEJJkOX0Hs"),
        ("Nuvole Bianche", "Ludovico Einaudi", "https://youtu.be/6ZdJcKvG_3k"),
        ("Comptine d'un autre été", "Yann Tiersen", "https://youtu.be/nvHqJjW0dyY")
    ],
    "melancholy": [
        ("Mad World", "Gary Jules", "https://youtu.be/4N3N1MlvVc4"),
        ("Skinny Love", "Bon Iver", "https://youtu.be/8CdcCD5V-d8"),
        ("Fix You", "Coldplay", "https://youtu.be/k4V3Mo61fJM"),
        ("Say Something", "A Great Big World", "https://youtu.be/-2U0Ivkn2Ds"),
        ("Creep", "Radiohead", "https://youtu.be/XFkzRNyygfk"),
        ("Hallelujah", "Jeff Buckley", "https://youtu.be/y8AWFf7EAc4")
    ],
    "anxious": [
        ("Breathe Me", "Sia", "https://youtu.be/GCFJeS1vjqg"),
        ("Fix You", "Coldplay", "https://youtu.be/k4V3Mo61fJM"),
        ("The Scientist", "Coldplay", "https://youtu.be/RB-RcX5DS5A"),
        ("Yellow", "Coldplay", "https://youtu.be/d020hcWA_Wg"),
        ("Clocks", "Coldplay", "https://youtu.be/d020hcWA_Wg"),
        ("Viva La Vida", "Coldplay", "https://youtu.be/d020hcWA_Wg")
    ],
    "hopeful": [
        ("Count on Me", "Bruno Mars", "https://youtu.be/6k8cpUkKK8c"),
        ("Best Day of My Life", "American Authors", "https://youtu.be/Y66j_BUCBMY"),
        ("Walking on Sunshine", "Katrina & The Waves", "https://youtu.be/iPUmE-tne5U"),
        ("Good Time", "Owl City & Carly Rae Jepsen", "https://youtu.be/9Sc-ir2UaGU"),
        ("The Climb", "Miley Cyrus", "https://youtu.be/NG2zyeVRcbs"),
        ("Hall of Fame", "The Script ft. will.i.am", "https://youtu.be/mk48xRzuNvA")
    ],
    "angry": [
        ("In The End", "Linkin Park", "https://youtu.be/eVTXPUF4Oz4"),
        ("Numb", "Linkin Park", "https://youtu.be/kXYiU_JCYtU"),
        ("Crawling", "Linkin Park", "https://youtu.be/Gd9OhYroLN0"),
        ("Breaking the Habit", "Linkin Park", "https://youtu.be/v2H4l9RpAMM"),
        ("Given Up", "Linkin Park", "https://youtu.be/8sgycukafqQ"),
        ("One Step Closer", "Linkin Park", "https://youtu.be/4qlCC1GOwFw")
    ],
    "reflective": [
        ("The Scientist", "Coldplay", "https://youtu.be/RB-RcX5DS5A"),
        ("Yellow", "Coldplay", "https://youtu.be/d020hcWA_Wg"),
        ("Clocks", "Coldplay", "https://youtu.be/d020hcWA_Wg"),
        ("Viva La Vida", "Coldplay", "https://youtu.be/d020hcWA_Wg"),
        ("Fix You", "Coldplay", "https://youtu.be/k4V3Mo61fJM"),
        ("Paradise", "Coldplay", "https://youtu.be/1G4isv_Fylg")
    ],
    "fun": [
        ("Call Me Maybe", "Carly Rae Jepsen", "https://youtu.be/fWNaR-rxAic"),
        ("Gangnam Style", "PSY", "https://youtu.be/9bZkp7q19f0"),
        ("Shake It Off", "Taylor Swift", "https://youtu.be/nfWlot6h_JM"),
        ("Party Rock Anthem", "LMFAO", "https://youtu.be/KQ6zr6kCPj8"),
        ("I Gotta Feeling", "The Black Eyed Peas", "https://youtu.be/uSD4vsh1zBA"),
        ("Good Time", "Owl City & Carly Rae Jepsen", "https://youtu.be/9Sc-ir2UaGU")
    ],
    "sleepy": [
        ("Weightless", "Marconi Union", "https://youtu.be/UfcAVejslrU"),
        ("Claire de Lune", "Debussy", "https://youtu.be/CvFH_6DNRCY"),
        ("River Flows In You", "Yiruma", "https://youtu.be/7maJOI3QMu0"),
        ("Experience", "Ludovico Einaudi", "https://youtu.be/hhEJJkOX0Hs"),
        ("Nuvole Bianche", "Ludovico Einaudi", "https://youtu.be/6ZdJcKvG_3k"),
        ("Comptine d'un autre été", "Yann Tiersen", "https://youtu.be/nvHqJjW0dyY")
    ],
    "nostalgic": [
        ("Wonderwall", "Oasis", "https://youtu.be/bx1Bh8ZvH84"),
        ("Don't Look Back in Anger", "Oasis", "https://youtu.be/r8OipmKFDeM"),
        ("Champagne Supernova", "Oasis", "https://youtu.be/tI-5v4aHqXk"),
        ("Creep", "Radiohead", "https://youtu.be/XFkzRNyygfk"),
        ("Karma Police", "Radiohead", "https://youtu.be/1uYWYWPc9HU"),
        ("No Surprises", "Radiohead", "https://youtu.be/u5CVsCnxyXg")
    ]
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