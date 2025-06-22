import random
import json
import os

# --- Helper Functions ---

def get_user_words():
    noun = input("Enter a noun: ")
    verb = input("Enter a verb: ")
    adjective = input("Enter an adjective: ")
    return noun, verb, adjective

def get_custom_mood_and_songs():
    mood = input("Enter the new mood name: ").strip().lower()
    songs = []
    print("Enter songs for this mood (title, artist, link). Type 'done' when finished.")
    while True:
        title = input("Song title: ").strip()
        if title.lower() == "done":
            break
        artist = input("Artist: ").strip()
        link = input("Link: ").strip()
        songs.append({"title": title, "artist": artist, "link": link})
    return mood, songs

def load_song_library(filename="song_library.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_song_library(library, filename="song_library.json"):
    with open(filename, "w") as f:
        json.dump(library, f, indent=2)

def load_favorites(filename="favorites.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return set(line.strip() for line in f)
    return set()

def save_favorite(song_str, filename="favorites.txt"):
    favorites = load_favorites(filename)
    if song_str not in favorites:
        with open(filename, "a") as f:
            f.write(song_str + "\n")
        print(f"Saved '{song_str}' to favorites.")
    else:
        print(f"'{song_str}' is already in favorites.")

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
    # Add more mappings as needed
}

# Load or initialize song library
song_library = load_song_library()
if not song_library:
    # Default songs if none saved yet
    song_library = {
        "calm": [
            {"title": "Weightless", "artist": "Marconi Union", "link": "https://youtu.be/UfcAVejslrU"},
            {"title": "Night Owl", "artist": "Galimatias", "link": "https://youtu.be/ZFnzNfVfSNY"}
        ],
        "focus": [
            {"title": "Clair de Lune", "artist": "Debussy", "link": "https://youtu.be/CvFH_6DNRCY"},
            {"title": "Study Music", "artist": "Various Artists", "link": "https://youtu.be/WPni755-Krg"}
        ],
        "energetic": [
            {"title": "Eye of the Tiger", "artist": "Survivor", "link": "https://youtu.be/btPJPFnesV4"},
            {"title": "Stronger", "artist": "Kanye West", "link": "https://youtu.be/PiTn5h1t73g"}
        ],
        "melancholy": [
            {"title": "Someone Like You", "artist": "Adele", "link": "https://youtu.be/hLQl3WQQoQ0"},
            {"title": "Everybody Hurts", "artist": "R.E.M.", "link": "https://youtu.be/ijZRCIrTgQc"}
        ],
        "joyful": [
            {"title": "Happy", "artist": "Pharrell Williams", "link": "https://youtu.be/ZbZSe6N_BXs"},
            {"title": "Good Vibrations", "artist": "The Beach Boys", "link": "https://youtu.be/Eab_beh07HU"}
        ],
    }

favorites_file = "favorites.txt"

# --- Main Program Loop ---

def main():
    print("Welcome to the Song Vibe Recommender!")
    print("Type 'q' to quit, 'favorites' to see saved songs, or 'add' to add a new mood and songs.")

    while True:
        user_input = input("\nWhat's your vibe today? ").strip().lower()

        if user_input == "q":
            print("Goodbye! Enjoy your music!")
            break
        elif user_input == "favorites":
            favorites = load_favorites(favorites_file)
            if favorites:
                print("\nYour favorite songs:")
                for fav in favorites:
                    print(f"- {fav}")
            else:
                print("You have no favorites saved yet.")
        elif user_input == "add":
            new_mood, new_songs = get_custom_mood_and_songs()
            if new_mood in song_library:
                print(f"Adding to existing mood '{new_mood}'.")
                song_library[new_mood].extend(new_songs)
            else:
                song_library[new_mood] = new_songs
            save_song_library(song_library)
            print(f"Added {len(new_songs)} songs under mood '{new_mood}'.")
        else:
            mood = match_vibe(user_input, keyword_map, song_library)
            if not mood:
                print("Sorry, I don't recognize that vibe. Try another or add it with 'add'.")
                continue

            song = recommend_song(mood, song_library)
            if not song:
                print(f"No songs found for mood '{mood}'.")
                continue

            song_str = f"{song['title']} by {song['artist']} ({song['link']})"
            print(f"Here's a {mood} song for you: {song_str}")

            save = input("Save to favorites? (y/n): ").strip().lower()
            if save == "y":
                save_favorite(song_str, favorites_file)

if __name__ == "__main__":
    main() 