import random
import os
import json

# Built-in song library (hardcoded)
builtin_song_library = {
    "chill": [
        ("Lo-Fi Beats", "Chillhop Music", "https://youtu.be/5qap5aO4i9A"),
        ("Weightless", "Marconi Union", "https://open.spotify.com/track/5c1O1WlU9fK3VQoZ9LrF2G"),
        ("Coffee", "Beabadoobee", "https://youtu.be/fM3O-WDqSNA")
    ],
    "hype": [
        ("Power", "Kanye West", "https://youtu.be/L53gjP-TtGE"),
        ("Can’t Hold Us", "Macklemore & Ryan Lewis", "https://youtu.be/2zNSgSzhBfM"),
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
        ("Don’t Start Now", "Dua Lipa", "https://youtu.be/oygrmJFKYZY"),
        ("Dancing Queen", "ABBA", "https://youtu.be/xFrGuyw1V8s")
    ]
}

# Keyword matcher for flexible mood input
keyword_map = {
    "relax": "chill",
    "peaceful": "chill",
    "lofi": "chill",
    "energized": "hype",
    "happy": "hype",
    "pump": "hype",
    "focused": "study",
    "bored": "study",
    "concentration": "study",
    "down": "sad",
    "heartbroken": "sad",
    "cry": "sad",
    "party": "dance",
    "move": "dance",
    "groove": "dance"
}

CUSTOM_VIBES_FILE = "custom_vibes.json"
FAVORITES_FILE = "favorite_songs.txt"

def load_custom_vibes():
    if os.path.exists(CUSTOM_VIBES_FILE):
        with open(CUSTOM_VIBES_FILE, "r") as f:
            data = json.load(f)
        return {k: [tuple(song) for song in v] for k,v in data.items()}
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
            print(f"✅ Added: “{title}” by {artist}")

        if song_library[new_vibe]:
            print(f"\n🎉 New mood '{new_vibe}' added with {len(song_library[new_vibe])} song(s)!")
            # Save custom vibes separately
            custom_song_library[new_vibe] = song_library[new_vibe]
            save_custom_vibes(custom_song_library)
        else:
            del song_library[new_vibe]
            print("⚠️ No songs were added. Mood was discarded.")
        continue

    # Match mood exactly or through keyword map
    if vibe_input in song_library:
        matched_vibe = vibe_input
    elif vibe_input in keyword_map:
        matched_vibe = keyword_map[vibe_input]
        print(f"🔍 Interpreted your vibe as: {matched_vibe}")
    else:
        print("😕 I couldn't match that vibe. Try moods like chill, hype, sad, study, dance.")
        continue

    # Pick a random song from matched vibe
    song = random.choice(song_library[matched_vibe])
    print(f"\n🎶 You might like: “{song[0]}” by {song[1]}\n🔗 Listen: {song[2]}")

    save = input("💾 Save to favorites? (yes/no): ").lower()
    if save in ['yes', 'y']:
        save_favorite(song, matched_vibe)

    again = input("\n🔁 Try another? (yes to continue, anything else to quit): ").lower()
    if again != 'yes':
        print("👋 Thanks for vibing with the Song Vibe Recommender!")
        break
