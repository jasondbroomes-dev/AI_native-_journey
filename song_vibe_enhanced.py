import json
import random
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Mood(Enum):
    """Enumeration of available moods with emoji representations"""
    CHILL = "😌 chill"
    HYPE = "⚡ hype"
    SAD = "💔 sad"
    STUDY = "📖 study"
    DANCE = "🕺 dance"
    HAPPY = "😄 happy"
    ROMANTIC = "💘 romantic"
    MOTIVATIONAL = "💪 motivational"
    PARTY = "🎊 party"
    CALM = "🧘 calm"
    MELANCHOLY = "🌧️ melancholy"
    ANXIOUS = "😰 anxious"
    HOPEFUL = "⭐ hopeful"
    ANGRY = "😤 angry"
    REFLECTIVE = "🤔 reflective"
    FUN = "🎈 fun"
    SLEEPY = "😴 sleepy"
    NOSTALGIC = "📷 nostalgic"

@dataclass
class Song:
    """Data class representing a song with metadata"""
    title: str
    artist: str
    link: str
    mood: Mood
    energy_level: int  # 1-10 scale
    tempo: str  # slow, medium, fast
    genre: str
    year: Optional[int] = None
    
    def __str__(self):
        return f"{self.title} by {self.artist} ({self.mood.value})"

class SongLibrary:
    """Advanced song library using data structures for efficient storage and retrieval"""
    
    def __init__(self):
        self.songs: List[Song] = []
        self.mood_index: Dict[Mood, List[Song]] = defaultdict(list)
        self.artist_index: Dict[str, List[Song]] = defaultdict(list)
        self.genre_index: Dict[str, List[Song]] = defaultdict(list)
        self.energy_index: Dict[int, List[Song]] = defaultdict(list)
        self.tempo_index: Dict[str, List[Song]] = defaultdict(list)
        
    def add_song(self, song: Song):
        """Add a song to the library and update all indices"""
        self.songs.append(song)
        self.mood_index[song.mood].append(song)
        self.artist_index[song.artist].append(song)
        self.genre_index[song.genre].append(song)
        self.energy_index[song.energy_level].append(song)
        self.tempo_index[song.tempo].append(song)
    
    def get_songs_by_mood(self, mood: Mood) -> List[Song]:
        """Get all songs for a specific mood"""
        return self.mood_index.get(mood, [])
    
    def get_random_song_by_mood(self, mood: Mood) -> Optional[Song]:
        """Get a random song for a specific mood"""
        songs = self.get_songs_by_mood(mood)
        return random.choice(songs) if songs else None

class MoodAnalyzer:
    """Advanced mood analysis using natural language processing concepts"""
    
    def __init__(self):
        # Keyword to mood mapping with weights
        self.keyword_weights = {
            # High energy keywords
            "energized": (Mood.HYPE, 0.9), "pump": (Mood.HYPE, 0.8), "excited": (Mood.HYPE, 0.7),
            "powerful": (Mood.MOTIVATIONAL, 0.8), "strong": (Mood.MOTIVATIONAL, 0.7),
            
            # Low energy keywords
            "relax": (Mood.CHILL, 0.9), "peaceful": (Mood.CALM, 0.8), "serene": (Mood.CALM, 0.7),
            "lofi": (Mood.CHILL, 0.8), "chill": (Mood.CHILL, 0.7),
            
            # Emotional keywords
            "happy": (Mood.HAPPY, 0.9), "joy": (Mood.HAPPY, 0.8), "cheerful": (Mood.HAPPY, 0.7),
            "sad": (Mood.SAD, 0.9), "heartbroken": (Mood.SAD, 0.8), "cry": (Mood.SAD, 0.7),
            "angry": (Mood.ANGRY, 0.9), "furious": (Mood.ANGRY, 0.8), "mad": (Mood.ANGRY, 0.7),
            
            # Activity keywords
            "study": (Mood.STUDY, 0.9), "focus": (Mood.STUDY, 0.8), "concentration": (Mood.STUDY, 0.7),
            "dance": (Mood.DANCE, 0.9), "move": (Mood.DANCE, 0.8), "groove": (Mood.DANCE, 0.7),
            "party": (Mood.PARTY, 0.9), "celebrate": (Mood.PARTY, 0.8), "wild": (Mood.PARTY, 0.7),
            
            # Relationship keywords
            "love": (Mood.ROMANTIC, 0.9), "romantic": (Mood.ROMANTIC, 0.8), "affection": (Mood.ROMANTIC, 0.7),
            
            # Mental state keywords
            "worried": (Mood.ANXIOUS, 0.9), "nervous": (Mood.ANXIOUS, 0.8), "tense": (Mood.ANXIOUS, 0.7),
            "hopeful": (Mood.HOPEFUL, 0.9), "optimistic": (Mood.HOPEFUL, 0.8), "bright": (Mood.HOPEFUL, 0.7),
            "thoughtful": (Mood.REFLECTIVE, 0.9), "pensive": (Mood.REFLECTIVE, 0.8), "introspective": (Mood.REFLECTIVE, 0.7),
            
            # Physical state keywords
            "tired": (Mood.SLEEPY, 0.9), "drowsy": (Mood.SLEEPY, 0.8), "sleepy": (Mood.SLEEPY, 0.7),
            
            # Fun keywords
            "fun": (Mood.FUN, 0.9), "playful": (Mood.FUN, 0.8), "jolly": (Mood.FUN, 0.7),
            
            # Nostalgic keywords
            "memories": (Mood.NOSTALGIC, 0.9), "remember": (Mood.NOSTALGIC, 0.8), "wistful": (Mood.NOSTALGIC, 0.7),
        }
    
    def analyze_text(self, text: str) -> Tuple[Mood, float]:
        """Analyze text and return the most likely mood with confidence score"""
        words = text.lower().split()
        mood_scores = defaultdict(float)
        
        for word in words:
            if word in self.keyword_weights:
                mood, weight = self.keyword_weights[word]
                mood_scores[mood] += weight
        
        if not mood_scores:
            return Mood.CHILL, 0.5  # Default mood
        
        # Find the mood with highest score
        best_mood = max(mood_scores, key=mood_scores.get)
        confidence = min(mood_scores[best_mood] / len(words), 1.0)
        
        return best_mood, confidence

class RecommendationEngine:
    """Advanced recommendation engine using multiple algorithms"""
    
    def __init__(self, song_library: SongLibrary):
        self.library = song_library
        self.user_history = []  # Track user's song history
        self.mood_preferences = Counter()  # Track mood preferences
    
    def get_recommendation(self, mood: Mood, algorithm: str = "random") -> Optional[Song]:
        """Get song recommendation using specified algorithm"""
        if algorithm == "random":
            return self._random_recommendation(mood)
        elif algorithm == "energy_based":
            return self._energy_based_recommendation(mood)
        elif algorithm == "diversity_based":
            return self._diversity_based_recommendation(mood)
        elif algorithm == "personalized":
            return self._personalized_recommendation(mood)
        else:
            return self._random_recommendation(mood)
    
    def _random_recommendation(self, mood: Mood) -> Optional[Song]:
        """Simple random recommendation"""
        return self.library.get_random_song_by_mood(mood)
    
    def _energy_based_recommendation(self, mood: Mood) -> Optional[Song]:
        """Recommend based on energy level preferences"""
        songs = self.library.get_songs_by_mood(mood)
        if not songs:
            return None
        
        # Calculate average energy preference from history
        if self.user_history:
            avg_energy = sum(song.energy_level for song in self.user_history[-10:]) / len(self.user_history[-10:])
            # Find songs closest to preferred energy level
            songs.sort(key=lambda s: abs(s.energy_level - avg_energy))
            return songs[0]
        else:
            return random.choice(songs)
    
    def _diversity_based_recommendation(self, mood: Mood) -> Optional[Song]:
        """Recommend diverse songs avoiding recent artists"""
        songs = self.library.get_songs_by_mood(mood)
        if not songs:
            return None
        
        # Get recent artists to avoid
        recent_artists = {song.artist for song in self.user_history[-5:]}
        
        # Filter out recent artists
        diverse_songs = [s for s in songs if s.artist not in recent_artists]
        
        if diverse_songs:
            return random.choice(diverse_songs)
        else:
            return random.choice(songs)  # Fallback to any song
    
    def _personalized_recommendation(self, mood: Mood) -> Optional[Song]:
        """Personalized recommendation based on user history"""
        songs = self.library.get_songs_by_mood(mood)
        if not songs or not self.user_history:
            return random.choice(songs) if songs else None
        
        # Calculate user preferences
        genre_preferences = Counter(song.genre for song in self.user_history)
        tempo_preferences = Counter(song.tempo for song in self.user_history)
        
        # Score songs based on preferences
        scored_songs = []
        for song in songs:
            score = 0
            score += genre_preferences[song.genre] * 2
            score += tempo_preferences[song.tempo] * 1.5
            scored_songs.append((score, song))
        
        # Return highest scored song
        scored_songs.sort(reverse=True)
        return scored_songs[0][1] if scored_songs else random.choice(songs)
    
    def record_play(self, song: Song):
        """Record that a song was played"""
        self.user_history.append(song)
        self.mood_preferences[song.mood] += 1
        
        # Keep history manageable
        if len(self.user_history) > 50:
            self.user_history.pop(0)

class EnhancedSongVibeRecommender:
    """Main class that orchestrates the enhanced song vibe recommender"""
    
    def __init__(self):
        self.library = SongLibrary()
        self.analyzer = MoodAnalyzer()
        self.recommender = RecommendationEngine(self.library)
        self._initialize_library()
    
    def _initialize_library(self):
        """Initialize the song library with sample data"""
        sample_songs = [
            Song("Blinding Lights", "The Weeknd", "https://youtu.be/4NRXx6U8ABQ", Mood.CHILL, 6, "medium", "pop", 2020),
            Song("Power", "Kanye West", "https://youtu.be/L53gjP-TtGE", Mood.HYPE, 9, "fast", "hip-hop", 2010),
            Song("Someone Like You", "Adele", "https://youtu.be/hLQl3WQQoQ0", Mood.SAD, 3, "slow", "pop", 2011),
            Song("Clair de Lune", "Debussy", "https://youtu.be/CvFH_6DNRCY", Mood.STUDY, 2, "slow", "classical", 1905),
            Song("Uptown Funk", "Mark Ronson ft. Bruno Mars", "https://youtu.be/OPf0YbXqDm0", Mood.DANCE, 8, "fast", "funk", 2014),
            Song("Happy", "Pharrell Williams", "https://youtu.be/ZbZSe6N_BXs", Mood.HAPPY, 8, "medium", "pop", 2013),
            Song("All of Me", "John Legend", "https://youtu.be/450p7goxZqg", Mood.ROMANTIC, 5, "slow", "R&B", 2013),
            Song("Eye of the Tiger", "Survivor", "https://youtu.be/btPJPFnesV4", Mood.MOTIVATIONAL, 9, "fast", "rock", 1982),
            Song("Party Rock Anthem", "LMFAO", "https://youtu.be/KQ6zr6kCPj8", Mood.PARTY, 9, "fast", "electronic", 2011),
            Song("Weightless", "Marconi Union", "https://youtu.be/UfcAVejslrU", Mood.CALM, 1, "slow", "ambient", 2011),
            Song("Mad World", "Gary Jules", "https://youtu.be/4N3N1MlvVc4", Mood.MELANCHOLY, 2, "slow", "alternative", 2003),
            Song("Breathe Me", "Sia", "https://youtu.be/GCFJeS1vjqg", Mood.ANXIOUS, 3, "slow", "pop", 2004),
            Song("Count on Me", "Bruno Mars", "https://youtu.be/6k8cpUkKK8c", Mood.HOPEFUL, 7, "medium", "pop", 2010),
            Song("In The End", "Linkin Park", "https://youtu.be/eVTXPUF4Oz4", Mood.ANGRY, 8, "fast", "rock", 2000),
            Song("The Scientist", "Coldplay", "https://youtu.be/RB-RcX5DS5A", Mood.REFLECTIVE, 4, "slow", "alternative", 2002),
            Song("Call Me Maybe", "Carly Rae Jepsen", "https://youtu.be/fWNaR-rxAic", Mood.FUN, 7, "medium", "pop", 2011),
            Song("River Flows In You", "Yiruma", "https://youtu.be/7maJOI3QMu0", Mood.SLEEPY, 1, "slow", "piano", 2001),
            Song("Wonderwall", "Oasis", "https://youtu.be/bx1Bh8ZvH84", Mood.NOSTALGIC, 5, "medium", "rock", 1995),
        ]
        
        for song in sample_songs:
            self.library.add_song(song)
    
    def get_recommendation(self, text: str, algorithm: str = "random") -> Tuple[Optional[Song], Mood, float]:
        """Get song recommendation based on text input"""
        mood, confidence = self.analyzer.analyze_text(text)
        song = self.recommender.get_recommendation(mood, algorithm)
        return song, mood, confidence
    
    def get_mood_statistics(self) -> Dict[Mood, int]:
        """Get statistics about available songs per mood"""
        return {mood: len(songs) for mood, songs in self.library.mood_index.items()}
    
    def get_user_preferences(self) -> Dict[str, int]:
        """Get user's mood preferences based on history"""
        return dict(self.recommender.mood_preferences)
    
    def add_custom_song(self, title: str, artist: str, link: str, mood: Mood, 
                       energy_level: int, tempo: str, genre: str, year: Optional[int] = None):
        """Add a custom song to the library"""
        song = Song(title, artist, link, mood, energy_level, tempo, genre, year)
        self.library.add_song(song)
        return song

def main():
    """Main function to demonstrate the enhanced song vibe recommender"""
    print("🎵 Enhanced Song Vibe Recommender with Data Structures 🎵")
    print("=" * 60)
    
    # Initialize the recommender
    recommender = EnhancedSongVibeRecommender()
    
    # Display available moods
    print("\n📊 Available Moods and Song Counts:")
    stats = recommender.get_mood_statistics()
    for mood, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {mood.value}: {count} songs")
    
    # Interactive recommendation demo
    print("\n🎯 Interactive Recommendation Demo:")
    print("Type 'quit' to exit")
    
    while True:
        user_input = input("\nHow are you feeling? (describe your mood): ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        if not user_input:
            continue
        
        # Get recommendation
        song, mood, confidence = recommender.get_recommendation(user_input, "personalized")
        
        if song:
            print(f"\n🎵 Based on '{user_input}' (confidence: {confidence:.2f})")
            print(f"🎭 Detected mood: {mood.value}")
            print(f"🎶 Recommendation: {song}")
            print(f"📊 Energy: {song.energy_level}/10 | Tempo: {song.tempo} | Genre: {song.genre}")
            
            # Record the play
            recommender.recommender.record_play(song)
        else:
            print("❌ Sorry, no recommendation found for that mood.")
    
    # Show user preferences at the end
    print("\n📈 Your Mood Preferences:")
    preferences = recommender.get_user_preferences()
    if preferences:
        for mood, count in preferences.most_common():
            print(f"  {mood.value}: {count} plays")
    else:
        print("  No preferences yet. Keep exploring!")
    
    print("\n👋 Thanks for using the Enhanced Song Vibe Recommender!")

if __name__ == "__main__":
    main()
