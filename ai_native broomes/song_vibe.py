"""
Song Vibe Recommender

A Python application that recommends songs based on user mood or vibe.
Features mood-based recommendations, custom mood creation, and favorite song management.
"""

import random
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ===== ENHANCED DATA STRUCTURES =====

class Song:
    """Represents a song with enhanced metadata"""
    def __init__(self, title: str, artist: str, link: str, genre: str = "", year: int = None):
        self.title = title
        self.artist = artist
        self.link = link
        self.genre = genre
        self.year = year
        self.added_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self) -> dict:
        """Convert song to dictionary for JSON serialization"""
        return {
            "title": self.title,
            "artist": self.artist,
            "link": self.link,
            "genre": self.genre,
            "year": self.year,
            "added_date": self.added_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Song':
        """Create song from dictionary"""
        return cls(
            title=data["title"],
            artist=data["artist"],
            link=data["link"],
            genre=data.get("genre", ""),
            year=data.get("year")
        )
    
    def __str__(self) -> str:
        return f"'{self.title}' by {self.artist}"
    
    def __repr__(self) -> str:
        return f"Song('{self.title}', '{self.artist}', '{self.link}')"

class MoodCategory:
    """Represents a mood category with songs and metadata"""
    def __init__(self, name: str, emoji: str, description: str = ""):
        self.name = name
        self.emoji = emoji
        self.description = description
        self.songs: List[Song] = []
        self.created_date = datetime.now().strftime("%Y-%m-%d")
    
    def add_song(self, song: Song) -> None:
        """Add a song to this mood category"""
        self.songs.append(song)
    
    def remove_song(self, song_title: str) -> bool:
        """Remove a song by title"""
        for i, song in enumerate(self.songs):
            if song.title.lower() == song_title.lower():
                del self.songs[i]
                return True
        return False
    
    def get_random_song(self) -> Optional[Song]:
        """Get a random song from this category"""
        return random.choice(self.songs) if self.songs else None
    
    def to_dict(self) -> dict:
        """Convert mood category to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "emoji": self.emoji,
            "description": self.description,
            "songs": [song.to_dict() for song in self.songs],
            "created_date": self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MoodCategory':
        """Create mood category from dictionary"""
        mood = cls(
            name=data["name"],
            emoji=data["emoji"],
            description=data.get("description", "")
        )
        mood.songs = [Song.from_dict(song_data) for song_data in data.get("songs", [])]
        mood.created_date = data.get("created_date", datetime.now().strftime("%Y-%m-%d"))
        return mood

class SongVibeManager:
    """Main manager class for the Song Vibe Recommender"""
    def __init__(self):
        self.mood_categories: Dict[str, MoodCategory] = {}
        self.keyword_map: Dict[str, str] = {}
        self.favorites: List[dict] = []
        self.stats = {
            "total_recommendations": 0,
            "favorites_saved": 0,
            "moods_created": 0,
            "songs_added": 0
        }
        self.load_data()
    
    def initialize_builtin_moods(self) -> None:
        """Initialize the built-in mood categories with songs"""
        builtin_data = {
            "😌 chill": {
                "description": "Relaxing, peaceful vibes for unwinding",
                "songs": [
                    ("Lo-Fi Beats", "Chillhop Music", "https://youtu.be/5qap5aO4i9A", "Lo-Fi", 2020),
                    ("Weightless", "Marconi Union", "https://open.spotify.com/track/5c1O1WlU9fK3VQoZ9LrF2G", "Ambient", 2011),
                    ("Coffee", "Beabadoobee", "https://youtu.be/fM3O-WDqSNA", "Indie", 2020)
                ]
            },
            "⚡ hype": {
                "description": "High energy, pump-up music",
                "songs": [
                    ("Power", "Kanye West", "https://youtu.be/L53gjP-TtGE", "Hip-Hop", 2010),
                    ("Can't Hold Us", "Macklemore & Ryan Lewis", "https://youtu.be/2zNSgSzhBfM", "Hip-Hop", 2012),
                    ("Eye of the Tiger", "Survivor", "https://youtu.be/btPJPFnesV4", "Rock", 1982)
                ]
            },
            "💔 sad": {
                "description": "Emotional, heartbreak songs",
                "songs": [
                    ("Someone Like You", "Adele", "https://youtu.be/hLQl3WQQoQ0", "Pop", 2011),
                    ("Skinny Love", "Bon Iver", "https://youtu.be/ssdgFoHLwnk", "Indie", 2008),
                    ("The Night We Met", "Lord Huron", "https://youtu.be/KtlgYxa6BMU", "Indie", 2015)
                ]
            },
            "📖 study": {
                "description": "Focus and concentration music",
                "songs": [
                    ("Clair de Lune", "Debussy", "https://youtu.be/CvFH_6DNRCY", "Classical", 1905),
                    ("Merry Christmas Mr. Lawrence", "Ryuichi Sakamoto", "https://youtu.be/J--TDEHizVA", "Classical", 1983),
                    ("Study Session", "Brain.fm", "https://www.youtube.com/watch?v=qWZGtLZaBBc", "Ambient", 2020)
                ]
            },
            "🕺 dance": {
                "description": "Upbeat dance and party music",
                "songs": [
                    ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "https://youtu.be/OPf0YbXqDm0", "Pop", 2014),
                    ("Don't Start Now", "Dua Lipa", "https://youtu.be/oygrmJFKYZY", "Pop", 2019),
                    ("Dancing Queen", "ABBA", "https://youtu.be/xFrGuyw1V8s", "Pop", 1976)
                ]
            },
            "💘 romantic": {
                "description": "Love and romance songs",
                "songs": [
                    ("All of Me", "John Legend", "https://youtu.be/450p7goxZqg", "R&B", 2013),
                    ("Perfect", "Ed Sheeran", "https://youtu.be/2Vv-BfVoq4g", "Pop", 2017),
                    ("Adore You", "Harry Styles", "https://youtu.be/yezDEWako8U", "Pop", 2019)
                ]
            },
            "💪 motivational": {
                "description": "Inspirational and empowering music",
                "songs": [
                    ("Lose Yourself", "Eminem", "https://youtu.be/_Yhyp-_hX2s", "Hip-Hop", 2002),
                    ("Stronger", "Kanye West", "https://youtu.be/Pi5PntUju_E", "Hip-Hop", 2007),
                    ("Fight Song", "Rachel Platten", "https://youtu.be/XsX3ATc3FbA", "Pop", 2015)
                ]
            },
            "😄 happy": {
                "description": "Joyful and cheerful music",
                "songs": [
                    ("Happy", "Pharrell Williams", "https://youtu.be/ZbZSe6N_BXs", "Pop", 2013),
                    ("Can't Stop The Feeling!", "Justin Timberlake", "https://youtu.be/ru0K8uYEZWw", "Pop", 2016),
                    ("Walking on Sunshine", "Katrina & The Waves", "https://youtu.be/iPUmE-tne5U", "Pop", 1983)
                ]
            },
            "🌧️ melancholy": {
                "description": "Thoughtful and introspective music",
                "songs": [
                    ("Fix You", "Coldplay", "https://youtu.be/k4V3Mo61fJM", "Alternative", 2005),
                    ("Everybody Hurts", "R.E.M.", "https://youtu.be/jWZsXfFuC7Y", "Alternative", 1992),
                    ("Tears in Heaven", "Eric Clapton", "https://youtu.be/JxPj3GAYYZ0", "Rock", 1992)
                ]
            },
            "🎊 party": {
                "description": "Celebration and party music",
                "songs": [
                    ("24K Magic", "Bruno Mars", "https://youtu.be/UqyT8IEBkvY", "Pop", 2016),
                    ("I Gotta Feeling", "Black Eyed Peas", "https://youtu.be/uSD4vsh1zDA", "Pop", 2009),
                    ("Party Rock Anthem", "LMFAO", "https://youtu.be/KQ6zr6kCPj8", "Pop", 2011)
                ]
            },
            "🧘 calm": {
                "description": "Peaceful and serene music",
                "songs": [
                    ("River Flows In You", "Yiruma", "https://youtu.be/7maJOI3QMu0", "Classical", 2001),
                    ("Weightless", "Marconi Union", "https://youtu.be/UfcAVejslrU", "Ambient", 2011),
                    ("Sunset Lover", "Petit Biscuit", "https://youtu.be/0z0Qzn0gf1I", "Electronic", 2015)
                ]
            },
            "📷 nostalgic": {
                "description": "Memories and retro vibes",
                "songs": [
                    ("Summer of '69", "Bryan Adams", "https://youtu.be/eFjjO_lhf9c", "Rock", 1984),
                    ("Take On Me", "a-ha", "https://youtu.be/djV11Xbc914", "Pop", 1984),
                    ("Yesterday", "The Beatles", "https://youtu.be/NrgmdOz227I", "Rock", 1965)
                ]
            },
            "😰 anxious": {
                "description": "Calming music for anxious moments",
                "songs": [
                    ("Breathe Me", "Sia", "https://youtu.be/ghPcYqn0p4Y", "Pop", 2004),
                    ("Creep", "Radiohead", "https://youtu.be/XFkzRNyygfk", "Alternative", 1992),
                    ("Everybody's Got To Learn Sometime", "Beck", "https://youtu.be/yy5WnK6YhMQ", "Alternative", 2004)
                ]
            },
            "⭐ hopeful": {
                "description": "Optimistic and uplifting music",
                "songs": [
                    ("Here Comes The Sun", "The Beatles", "https://youtu.be/KQetemT1sWc", "Rock", 1969),
                    ("Dog Days Are Over", "Florence + The Machine", "https://youtu.be/iWOyfLBYtuU", "Indie", 2009),
                    ("Good Life", "OneRepublic", "https://youtu.be/jZhQOvvV45w", "Pop", 2010)
                ]
            },
            "😤 angry": {
                "description": "Intense and powerful music",
                "songs": [
                    ("Break Stuff", "Limp Bizkit", "https://youtu.be/ZpUYjpKg9KY", "Rock", 1999),
                    ("Killing In The Name", "Rage Against The Machine", "https://youtu.be/bWXazVhlyxQ", "Rock", 1992),
                    ("You Oughta Know", "Alanis Morissette", "https://youtu.be/NPcyTyilmYY", "Rock", 1995)
                ]
            },
            "🤔 reflective": {
                "description": "Deep and contemplative music",
                "songs": [
                    ("The Sound of Silence", "Simon & Garfunkel", "https://youtu.be/4zLfCnGVeL4", "Folk", 1964),
                    ("Hallelujah", "Jeff Buckley", "https://youtu.be/y8AWFf7EAc4", "Folk", 1994),
                    ("Fast Car", "Tracy Chapman", "https://youtu.be/uTIB10eQnA0", "Folk", 1988)
                ]
            },
            "🎈 fun": {
                "description": "Playful and entertaining music",
                "songs": [
                    ("Happy", "Pharrell Williams", "https://youtu.be/ZbZSe6N_BXs", "Pop", 2013),
                    ("Shake It Off", "Taylor Swift", "https://youtu.be/nfWlot6h_JM", "Pop", 2014),
                    ("Can't Stop The Feeling", "Justin Timberlake", "https://youtu.be/ru0K8uYEZWw", "Pop", 2016)
                ]
            },
            "😴 sleepy": {
                "description": "Gentle music for relaxation and sleep",
                "songs": [
                    ("Night Owl", "Galimatias", "https://youtu.be/8-SxHJ0ayN8", "Electronic", 2015),
                    ("Holocene", "Bon Iver", "https://youtu.be/TapN6N8OYMI", "Indie", 2011),
                    ("Sunset Lover", "Petit Biscuit", "https://youtu.be/0z0Qzn0gf1I", "Electronic", 2015)
                ]
            }
        }
        
        # Create mood categories from builtin data
        for mood_name, mood_data in builtin_data.items():
            mood = MoodCategory(mood_name, mood_name.split()[0], mood_data["description"])
            for song_data in mood_data["songs"]:
                song = Song(*song_data)
                mood.add_song(song)
            self.mood_categories[mood_name] = mood
    
    def initialize_keyword_map(self) -> None:
        """Initialize the keyword mapping for flexible mood input"""
        self.keyword_map = {
            "relax": "😌 chill", "peaceful": "🧘 calm", "lofi": "😌 chill",
            "energized": "⚡ hype", "happy": "😄 happy", "joy": "😄 happy", "pump": "⚡ hype",
            "focused": "📖 study", "bored": "📖 study", "concentration": "📖 study",
            "down": "💔 sad", "heartbroken": "💔 sad", "cry": "💔 sad",
            "party": "🎊 party", "move": "🕺 dance", "groove": "🕺 dance",
            "love": "💘 romantic", "affection": "💘 romantic", "sweet": "💘 romantic",
            "inspired": "💪 motivational", "pump up": "💪 motivational", "drive": "💪 motivational",
            "cheerful": "😄 happy", "bright": "😄 happy",
            "sadness": "🌧️ melancholy", "blue": "🌧️ melancholy", "heartache": "🌧️ melancholy",
            "celebrate": "🎊 party",
            "relaxing": "🧘 calm", "serene": "🧘 calm",
            "memories": "📷 nostalgic", "remember": "📷 nostalgic", "wistful": "📷 nostalgic",
            "worried": "😰 anxious", "nervous": "😰 anxious", "tense": "😰 anxious",
            "optimistic": "⭐ hopeful", "bright future": "⭐ hopeful", "expectation": "⭐ hopeful",
            "mad": "😤 angry", "furious": "😤 angry", "frustrated": "😤 angry",
            "thoughtful": "🤔 reflective", "pensive": "🤔 reflective", "introspective": "🤔 reflective",
            "playful": "🎈 fun", "jolly": "🎈 fun", "lighthearted": "🎈 fun",
            "tired": "😴 sleepy", "drowsy": "😴 sleepy", "relaxed": "😴 sleepy"
        }
    
    def load_data(self) -> None:
        """Load all data from files"""
        self.initialize_builtin_moods()
        self.initialize_keyword_map()
        self.load_custom_moods()
        self.load_favorites()
        self.load_stats()
    
    def save_data(self) -> None:
        """Save all data to files"""
        self.save_custom_moods()
        self.save_favorites()
        self.save_stats()
    
    def load_custom_moods(self) -> None:
        """Load custom mood categories from JSON file"""
        if os.path.exists("custom_moods.json"):
            try:
                with open("custom_moods.json", "r") as f:
                    data = json.load(f)
                    for mood_data in data.values():
                        mood = MoodCategory.from_dict(mood_data)
                        self.mood_categories[mood.name] = mood
            except json.JSONDecodeError:
                print("⚠️ Error loading custom moods file. Starting fresh.")
    
    def save_custom_moods(self) -> None:
        """Save custom mood categories to JSON file"""
        custom_moods = {}
        for name, mood in self.mood_categories.items():
            if name not in ["😌 chill", "⚡ hype", "💔 sad", "📖 study", "🕺 dance", 
                           "💘 romantic", "💪 motivational", "😄 happy", "🌧️ melancholy", 
                           "🎊 party", "🧘 calm", "📷 nostalgic", "😰 anxious", "⭐ hopeful", 
                           "😤 angry", "🤔 reflective", "🎈 fun", "😴 sleepy"]:
                custom_moods[name] = mood.to_dict()
        
        with open("custom_moods.json", "w") as f:
            json.dump(custom_moods, f, indent=2)
    
    def load_favorites(self) -> None:
        """Load favorites from JSON file"""
        if os.path.exists("favorites.json"):
            try:
                with open("favorites.json", "r") as f:
                    self.favorites = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Error loading favorites file. Starting fresh.")
    
    def save_favorites(self) -> None:
        """Save favorites to JSON file"""
        with open("favorites.json", "w") as f:
            json.dump(self.favorites, f, indent=2)
    
    def load_stats(self) -> None:
        """Load statistics from JSON file"""
        if os.path.exists("stats.json"):
            try:
                with open("stats.json", "r") as f:
                    self.stats = json.load(f)
            except json.JSONDecodeError:
                pass
    
    def save_stats(self) -> None:
        """Save statistics to JSON file"""
        with open("stats.json", "w") as f:
            json.dump(self.stats, f, indent=2)
    
    def get_mood_by_keyword(self, keyword: str) -> Optional[str]:
        """Get mood category by keyword"""
        return self.keyword_map.get(keyword.lower(), keyword.lower())
    
    def get_recommendation(self, vibe_input: str) -> Optional[Tuple[Song, str]]:
        """Get a song recommendation for the given vibe"""
        matched_vibe = self.get_mood_by_keyword(vibe_input)
        
        if matched_vibe in self.mood_categories:
            mood = self.mood_categories[matched_vibe]
            song = mood.get_random_song()
            if song:
                self.stats["total_recommendations"] += 1
                return song, matched_vibe
        
        return None
    
    def add_favorite(self, song: Song, mood: str) -> bool:
        """Add a song to favorites"""
        favorite_entry = {
            "song": song.to_dict(),
            "mood": mood,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Check for duplicates
        for existing in self.favorites:
            if (existing["song"]["title"] == song.title and 
                existing["song"]["artist"] == song.artist):
                return False
        
        self.favorites.append(favorite_entry)
        self.stats["favorites_saved"] += 1
        return True
    
    def create_mood(self, name: str, emoji: str, description: str = "") -> bool:
        """Create a new mood category"""
        if name in self.mood_categories:
            return False
        
        mood = MoodCategory(name, emoji, description)
        self.mood_categories[name] = mood
        self.stats["moods_created"] += 1
        return True
    
    def add_song_to_mood(self, mood_name: str, song: Song) -> bool:
        """Add a song to a mood category"""
        if mood_name in self.mood_categories:
            self.mood_categories[mood_name].add_song(song)
            self.stats["songs_added"] += 1
            return True
        return False
    
    def get_all_mood_names(self) -> List[str]:
        """Get list of all mood category names"""
        return list(self.mood_categories.keys())
    
    def get_mood_info(self, mood_name: str) -> Optional[dict]:
        """Get information about a mood category"""
        if mood_name in self.mood_categories:
            mood = self.mood_categories[mood_name]
            return {
                "name": mood.name,
                "emoji": mood.emoji,
                "description": mood.description,
                "song_count": len(mood.songs),
                "created_date": mood.created_date
            }
        return None
    
    def get_stats(self) -> dict:
        """Get application statistics"""
        return {
            **self.stats,
            "total_moods": len(self.mood_categories),
            "total_favorites": len(self.favorites),
            "total_songs": sum(len(mood.songs) for mood in self.mood_categories.values())
        }

# ===== MAIN APPLICATION =====

def main():
    """Main application function"""
    print("🎵 Welcome to the Enhanced Song Vibe Recommender!")
    print("=" * 50)
    
    # Initialize the manager
    manager = SongVibeManager()
    
    while True:
        print(f"\n📊 Stats: {manager.stats['total_recommendations']} recommendations, "
              f"{manager.stats['favorites_saved']} favorites, "
              f"{len(manager.mood_categories)} moods")
        
        vibe_input = input(
            "\n🎧 What's your vibe today? "
            "(type a mood, 'favorites', 'add', 'stats', 'moods', or 'q' to quit): "
        ).lower()

        if vibe_input == 'q':
            print("👋 Goodbye! Keep the good vibes going.")
            manager.save_data()
            break
        
        elif vibe_input == 'favorites':
            show_favorites(manager)
        
        elif vibe_input == 'add':
            add_new_mood(manager)
        
        elif vibe_input == 'stats':
            show_stats(manager)
        
        elif vibe_input == 'moods':
            show_all_moods(manager)
        
        else:
            # Get recommendation
            result = manager.get_recommendation(vibe_input)
            if result:
                song, mood = result
                print(f"\n🎶 You might like: {song}")
                print(f"🎭 Mood: {mood}")
                if song.genre:
                    print(f"🎵 Genre: {song.genre}")
                if song.year:
                    print(f"📅 Year: {song.year}")
                print(f"🔗 Listen: {song.link}")

                save = input("💾 Save to favorites? (yes/no): ").lower()
                if save in ['yes', 'y']:
                    if manager.add_favorite(song, mood):
                        print("✅ Saved to favorites!")
                    else:
                        print("⚠️ Already in favorites!")
            else:
                print("😕 I couldn't match that vibe. Try moods like 😌 chill, ⚡ hype, 💔 sad, 📖 study, 🕺 dance.")
                print("💡 Available moods:", ", ".join(manager.get_all_mood_names()[:5]) + "...")

def show_favorites(manager: SongVibeManager) -> None:
    """Display user's favorite songs"""
    if not manager.favorites:
        print("\n📭 No favorites saved yet.")
        return
    
    print(f"\n💖 Your Favorite Songs ({len(manager.favorites)} total):")
    for i, fav in enumerate(manager.favorites, 1):
        song_data = fav["song"]
        print(f"  {i}. '{song_data['title']}' by {song_data['artist']}")
        print(f"     🎭 Mood: {fav['mood']} | 📅 Added: {fav['added_date']}")

def add_new_mood(manager: SongVibeManager) -> None:
    """Add a new mood category with songs"""
    print("\n🆕 Creating a new mood category...")
    
    name = input("Mood name: ").strip()
    emoji = input("Emoji (optional): ").strip() or "🎵"
    description = input("Description (optional): ").strip()
    
    if not name:
        print("⚠️ Mood name is required!")
        return
    
    if manager.create_mood(name, emoji, description):
        print(f"✅ Created mood: {emoji} {name}")
        
        print(f"🎶 Let's add songs to '{name}'. Type 'done' when finished.")
        while True:
            title = input("Song title (or 'done'): ").strip()
            if title.lower() == 'done':
                break
            
            artist = input("Artist: ").strip()
            link = input("Link (YouTube/Spotify): ").strip()
            genre = input("Genre (optional): ").strip()
            year_str = input("Year (optional): ").strip()
            
            year = int(year_str) if year_str.isdigit() else None
            
            song = Song(title, artist, link, genre, year)
            if manager.add_song_to_mood(name, song):
                print(f"✅ Added: {song}")
            else:
                print("❌ Failed to add song!")
        
        mood = manager.mood_categories[name]
        print(f"🎉 Mood '{name}' created with {len(mood.songs)} song(s)!")
    else:
        print("⚠️ That mood already exists!")

def show_stats(manager: SongVibeManager) -> None:
    """Display application statistics"""
    stats = manager.get_stats()
    print("\n📊 Song Vibe Recommender Statistics:")
    print("=" * 40)
    print(f"🎵 Total Songs: {stats['total_songs']}")
    print(f"🎭 Total Moods: {stats['total_moods']}")
    print(f"💖 Total Favorites: {stats['total_favorites']}")
    print(f"🎯 Total Recommendations: {stats['total_recommendations']}")
    print(f"🆕 Moods Created: {stats['moods_created']}")
    print(f"➕ Songs Added: {stats['songs_added']}")
    print(f"💾 Favorites Saved: {stats['favorites_saved']}")

def show_all_moods(manager: SongVibeManager) -> None:
    """Display all available mood categories"""
    print("\n🎭 Available Mood Categories:")
    print("=" * 40)
    
    for name in manager.get_all_mood_names():
        info = manager.get_mood_info(name)
        if info:
            print(f"{info['emoji']} {info['name']}")
            print(f"   📝 {info['description']}")
            print(f"   🎵 {info['song_count']} songs | 📅 Created: {info['created_date']}")
            print()

if __name__ == "__main__":
    main()
