"""
Mini Project Definition Document

Project Title:
Song Vibe Recommender

Project Purpose:
Create an interactive Python application that recommends songs based on a user's mood or vibe.
The app lets users choose from preset moods or add their own custom moods and songs.
It also saves favorite songs for easy access later.

Project Objectives:
- Provide personalized song recommendations based on mood input.
- Support flexible mood recognition using keyword mapping.
- Allow users to add new mood categories with custom songs (title, artist, link).
- Persist user-added moods and favorites between sessions using JSON and text files.
- Enable users to view and manage their favorite songs.

Target Users:
- Music lovers and casual listeners seeking mood-based music discovery.
- Users comfortable running simple Python scripts or command-line apps.
- People who want to save and revisit favorite songs easily.

Inputs:
- User mood or vibe text input.
- User commands: add mood, view favorites, quit.
- New mood name and multiple song entries (title, artist, link).
- Save confirmation for favorite songs.

Processing:
- Match user input to built-in or custom mood categories (exact or keyword match).
- Randomly select a song from the matched mood category.
- Save custom moods and favorites to files for persistence.
- Check for duplicates when saving favorites.

Outputs:
- Display song recommendations with title, artist, and streaming link.
- Confirmation messages for saved favorites and added moods.
- List of saved favorite songs upon user request.
- Informative error or guidance messages for unmatched moods or invalid input.

Features:
- Built-in moods with curated song lists.
- AI-inspired keyword matching for flexible input recognition.
- User-defined mood creation and immediate usage.
- Persistent storage of custom moods and favorite songs.
- Duplicate detection for favorites.
- Command-line interface for easy interaction.

Technology Stack:
- Python 3.x
- JSON for data persistence
- Text files for storing favorites

Success Criteria:
- User can get relevant song recommendations by typing moods or keywords.
- User can add new moods with songs and retrieve recommendations from them.
- User's custom moods and favorites persist across program runs.
- User can view and manage their favorite songs.
- The app handles invalid inputs gracefully.
"""

import random
import os
import json

# Built-in song library (expanded with new moods)
builtin_song_library = {
    "chill": [
        ("Lo-Fi Beats", "Chillhop Music", "https://youtu.be/5qap5aO4i9A"),
        ("Weightless", "Marconi Union", "https://open.spotify.com/track/5c1O1WlU9fK3VQoZ9LrF2G"),
        ("Coffee", "Beabadoobee", "https://youtu.be/fM3O-WDqSNA")
    ],
    "hype": [
        ("Power", "Kanye West", "https://youtu.be/L53gjP-TtGE"),
        ("Can't Hold Us", "Macklemore & Ryan Lewis", "https://youtu.be/2zNSgSzhBfM"),
        ("Eye of the Tiger", "Survivor", "https://youtu.be/btPJPFnesV4")
    ],
    "sad": [
        ("Someone Like You", "Adele", "https://youtu.be/hLQl3WQQoQ0"),
        ("Skinny Love", "Bon Iver", "https://youtu.be/ssdgFoHLwnk"),
        ("The Night We Met", "Lord Huron", "https://youtu.be/KtlgYxa6BMU")
    ],
    "study": [
        ("Clair de Lune", "Debussy", "https://youtu.be/CvFH_6DNRCY"),
        ("Merry Christmas Mr. Lawrence", "Ryuichi Sakamoto", "https://youtu.be/J--TDEHizVA"),
        ("Study Session", "Brain.fm", "https://www.youtube.com/watch?v=qWZGtLZaBBc")
    ],
    "dance": [
        ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "https://youtu.be/OPf0YbXqDm0"),
        ("Don't Start Now", "Dua Lipa", "https://youtu.be/oygrmJFKYZY"),
        ("Dancing Queen", "ABBA", "https://youtu.be/xFrGuyw1V8s")
    ],
    "romantic": [
        ("All of Me", "John Legend", "https://youtu.be/450p7goxZqg"),
        ("Perfect", "Ed Sheeran", "https://youtu.be/2Vv-BfVoq4g"),
        ("Adore You", "Harry Styles", "https://youtu.be/yezDEWako8U")
    ],
    "motivational": [
        ("Lose Yourself", "Eminem", "https://youtu.be/_Yhyp-_hX2s"),
        ("Stronger", "Kanye West", "https://youtu.be/Pi5PntUju_E"),
        ("Fight Song", "Rachel Platten", "https://youtu.be/XsX3ATc3FbA")
    ],
    "happy": [
        ("Happy", "Pharrell Williams", "https://youtu.be/ZbZSe6N_BXs"),
        ("Can't Stop The Feeling!", "Justin Timberlake", "https://youtu.be/ru0K8uYEZWw"),
        ("Walking on Sunshine", "Katrina & The Waves", "https://youtu.be/iPUmE-tne5U")
    ],
    "melancholy": [
        ("Fix You", "Coldplay", "https://youtu.be/k4V3Mo61fJM"),
        ("Everybody Hurts", "R.E.M.", "https://youtu.be/jWZsXfFuC7Y"),
        ("Tears in Heaven", "Eric Clapton", "https://youtu.be/JxPj3GAYYZ0")
    ],
    "party": [
        ("24K Magic", "Bruno Mars", "https://youtu.be/UqyT8IEBkvY"),
        ("I Gotta Feeling", "Black Eyed Peas", "https://youtu.be/uSD4vsh1zDA"),
        ("Party Rock Anthem", "LMFAO", "https://youtu.be/KQ6zr6kCPj8")
    ],
    "calm": [
        ("River Flows In You", "Yiruma", "https://youtu.be/7maJOI3QMu0"),
        ("Weightless", "Marconi Union", "https://youtu.be/UfcAVejslrU"),
        ("Sunset Lover", "Petit Biscuit", "https://youtu.be/0z0Qzn0gf1I")
    ],
    "nostalgic": [
        ("Summer of '69", "Bryan Adams", "https://youtu.be/eFjjO_lhf9c"),
        ("Take On Me", "a-ha", "https://youtu.be/djV11Xbc914"),
        ("Yesterday", "The Beatles", "https://youtu.be/NrgmdOz227I")
    ],
    "anxious": [
        ("Breathe Me", "Sia", "https://youtu.be/ghPcYqn0p4Y"),
        ("Creep", "Radiohead", "https://youtu.be/XFkzRNyygfk"),
        ("Everybody's Got To Learn Sometime", "Beck", "https://youtu.be/yy5WnK6YhMQ")
    ],
    "hopeful": [
        ("Here Comes The Sun", "The Beatles", "https://youtu.be/KQetemT1sWc"),
        ("Dog Days Are Over", "Florence + The Machine", "https://youtu.be/iWOyfLBYtuU"),
        ("Good Life", "OneRepublic", "https://youtu.be/jZhQOvvV45w")
    ],
    "angry": [
        ("Break Stuff", "Limp Bizkit", "https://youtu.be/ZpUYjpKg9KY"),
        ("Killing In The Name", "Rage Against The Machine", "https://youtu.be/bWXazVhlyxQ"),
        ("You Oughta Know", "Alanis Morissette", "https://youtu.be/NPcyTyilmYY")
    ],
    "reflective": [
        ("The Sound of Silence", "Simon & Garfunkel", "https://youtu.be/4zLfCnGVeL4"),
        ("Hallelujah", "Jeff Buckley", "https://youtu.be/y8AWFf7EAc4"),
        ("Fast Car", "Tracy Chapman", "https://youtu.be/uTIB10eQnA0")
    ],
    "fun": [
        ("Happy", "Pharrell Williams", "https://youtu.be/ZbZSe6N_BXs"),
        ("Shake It Off", "Taylor Swift", "https://youtu.be/nfWlot6h_JM"),
        ("Can't Stop The Feeling", "Justin Timberlake", "https://youtu.be/ru0K8uYEZWw")
    ],
    "sleepy": [
        ("Night Owl", "Galimatias", "https://youtu.be/8-SxHJ0ayN8"),
        ("Holocene", "Bon Iver", "https://youtu.be/TapN6N8OYMI"),
        ("Sunset Lover", "Petit Biscuit", "https://youtu.be/0z0Qzn0gf1I")
    ]
}

# Keyword matcher for flexible mood input
keyword_map = {
    "relax": "chill",
    "peaceful": "calm",
    "lofi": "chill",
    "energized": "hype",
    "happy": "happy",
    "joy": "happy",
    "pump": "hype",
    "focused": "study",
    "bored": "study",
    "concentration": "study",
    "down": "sad",
    "heartbroken": "sad",
    "cry": "sad",
    "party": "party",
    "move": "dance",
    "groove": "dance",
    "love": "romantic",
    "affection": "romantic",
    "sweet": "romantic",
    "inspired": "motivational",
    "pump up": "motivational",
    "drive": "motivational",
    "cheerful": "happy",
    "bright": "happy",
    "sadness": "melancholy",
    "blue": "melancholy",
    "heartache": "melancholy",
    "celebrate": "party",
    "dance": "party",
    "fun": "fun",
    "peaceful": "calm",
    "relaxing": "calm",
    "serene": "calm",
    "memories": "nostalgic",
    "remember": "nostalgic",
    "wistful": "nostalgic",
    "worried": "anxious",
    "nervous": "anxious",
    "tense": "anxious",
    "optimistic": "hopeful",
    "bright future": "hopeful",
    "expectation": "hopeful",
    "mad": "angry",
    "furious": "angry",
    "frustrated": "angry",
    "thoughtful": "reflective",
    "pensive": "reflective",
    "introspective": "reflective",
    "playful": "fun",
    "jolly": "fun",
    "lighthearted": "fun",
    "tired": "sleepy",
    "drowsy": "sleepy",
    "relaxed": "sleepy"
}

CUSTOM_VIBES_FILE = "custom_vibes.json"
FAVORITES_FILE = "favorite_songs.txt"

def load_custom_vibes():
    if os.path.exists(CUSTOM_VIBES_FILE):
        with open(CUSTOM_VIBES_FILE, "r") as f:
            try:
                data = json.load(f)
                return {k: [tuple(song) for song in v] for k,v in data.items()}
            except json.JSONDecodeError:
                return {}
    return {}

def save_custom_vibes(custom_vibes):
    serializable = {k: [list(song) for song in v] for k,v in custom_vibes.items()}
    with open(CUSTOM_VIBES_FILE, "w") as f:
        json.dump(serializable, f, indent=2)

def save_favorite(song, vibe):
    entry = f"{song[0]} by {song[1]} - vibe: {vibe}\n"
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as file:
            if entry in file.readlines():
                print("⚠️ Already saved in favorites.")
                return
    with open(FAVORITES_FILE, "a") as file:
        file.write(entry)
    print("✅ Saved to favorite_songs.txt!")

def show_favorites():
    if not os.path.exists(FAVORITES_FILE):
        print("\n📭 No favorites saved yet.")
        return
    with open(FAVORITES_FILE, "r") as file:
        favorites = file.readlines()
    if favorites:
        print("\n💖 Your Favorite Songs:")
        for song in favorites:
            print(f"  - {song.strip()}")
    else:
        print("\n📭 Your favorites list is empty.")

# Load custom vibes on startup
custom_song_library = load_custom_vibes()

# Combine built-in + custom vibes
song_library = {**builtin_song_library, **custom_song_library}

while True:
    vibe_input = input(
        "\n🎧 What's your vibe today? (type a mood, 'favorites', 'add' to create your own, or 'q' to quit): "
    ).lower()

    if vibe_input == 'q':
        print("👋 Goodbye! Keep the good vibes going.")
        break
    elif vibe_input == 'favorites':
        show_favorites()
        continue
    elif vibe_input == 'add':
        new_vibe = input("🆕 What's the name of your new mood category? ").lower()
        if new_vibe in song_library:
            print("⚠️ That vibe already exists. Try recommending from it instead.")
            continue

        song_library[new_vibe] = []
        print(f"🎶 Let's add songs to '{new_vibe}'. Type 'done' when finished.")

        while True:
            title = input("Song title (or 'done'): ")
            if title.lower() == 'done':
                break
            artist = input("Artist: ")
            link = input("Link (YouTube/Spotify): ")
            song_library[new_vibe].append((title, artist, link))
            print(f"✅ Added: '{title}' by {artist}")

        if song_library[new_vibe]:
            print(f"🎉 New mood '{new_vibe}' added with {len(song_library[new_vibe])} song(s)!")
            custom_song_library[new_vibe] = song_library[new_vibe]
            save_custom_vibes(custom_song_library)
        else:
            del song_library[new_vibe]
            print("⚠️ No songs were added. Mood was discarded.")
        continue

    # Match mood exactly or through keyword map
    matched_vibe = keyword_map.get(vibe_input, vibe_input)

    if matched_vibe in song_library and song_library[matched_vibe]:
        song = random.choice(song_library[matched_vibe])
        print(f"\n🎶 You might like: '{song[0]}' by {song[1]}\n🔗 Listen: {song[2]}")

        save = input("💾 Save to favorites? (yes/no): ").lower()
        if save in ['yes', 'y']:
            save_favorite(song, matched_vibe)
    else:
        print("😕 I couldn't match that vibe. Try moods like chill, hype, sad, study, dance.")
        continue

    again = input("\n🔁 Try another? (yes to continue, anything else to quit): ").lower()
    if again != 'yes':
        print("👋 Thanks for vibing with the Song Vibe Recommender!")
        break
