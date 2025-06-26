# AI Native Journey

Welcome to my AI and Python programming journey! This repository contains various projects showcasing different programming concepts and technologies.

## 🐕 Dog Park Finder React App

A beautiful React application to find the best dog parks in NYC.

### Features:
- **Modern React 18** with functional components
- **Tailwind CSS** for beautiful styling
- **Responsive design** for all devices
- **Interactive cards** with hover effects
- **Real dog park data** from NYC

### To run the Dog Park Finder:

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser** and go to `http://localhost:3000`

## 🌐 Hello World Web Application

A Flask web application showcasing your Python greeting program.

### To run the Hello World web app:

1. **Install Flask:**
   ```bash
   pip3 install Flask
   ```

2. **Start the server:**
   ```bash
   python3 hello_web.py
   ```

3. **Open your browser** and go to `http://localhost:5001`

## 📁 Project Structure

- `src/components/DogParkFinder.js` - Main React component
- `hello_web.py` - Flask web application
- `Hello_World.py` - Original Python greeting script
- `budget_calculator.py` - Personal finance tool
- `number_guessing_game.py` - Interactive game
- `greeting_by_time.py` - Time-based greetings

## 🚀 Technologies Used

- **Python** - Backend logic and scripts
- **Flask** - Web framework
- **React** - Frontend framework
- **Tailwind CSS** - Styling
- **HTML/CSS/JavaScript** - Web technologies

## 🎶 Song Vibe Recommender

## About This Project

The **Song Vibe Recommender** is a fun, interactive web application designed to instantly recommend music based on your current mood. Whether you're happy 😊, sad 😢, hyped 🔥, or calm 🌙, this app helps you quickly discover the perfect song that matches your vibe. It's built to provide an engaging experience without complicated playlists or logins.

## How It Works

The app's core logic, created with AI assistance, revolves around matching user-selected moods to songs:

- **Mood Selection:** Users pick a mood using intuitive emoji buttons.
- **Song Recommendation:** A random song that matches the chosen mood is selected from a predefined, structured song library, filtering by mood category and year.
- **Interactive Playback:** Each recommended song includes an embedded YouTube preview directly within the app.
- **Favorites Management:** Users can save favorite songs during their session, and the app ensures no duplicates are added.

## Features

### 🎯 **Core Features**
- **18 Different Moods** - From 😌 chill to ⚡ hype to 💔 sad
- **Smart Text Analysis** - Type how you're feeling and get recommendations
- **Word-Based Recommendations** - Use noun/verb/adjective combinations
- **Personalized Suggestions** - Learns from your listening history
- **Beautiful Web Interface** - Modern glass morphism design

### 🚀 **Advanced Features**
- **Multiple Algorithms** - Random, energy-based, diversity-based, personalized
- **User History Tracking** - Remembers your preferences
- **Energy Level Matching** - Finds songs matching your energy
- **Artist Diversity** - Avoids recommending the same artists repeatedly
- **Confidence Scoring** - Shows how sure the AI is about mood detection

## Project Structure

```
AI_native-_journey/
├── song_vibe_app.py              # Main Flask web application
├── song_vibe_enhanced.py         # Advanced version with data structures
├── templates/
│   ├── song_vibe.html           # Beautiful web interface
│   └── song_vibe_improved.html  # Enhanced web interface
├── builtin_songs.json           # Song library database
├── custom_vibes.json            # User-added songs
├── favorite_songs.json          # User favorites
└── ai_native broomes/
    └── song_vibe.py             # Personal version
```

## How to Run It

### Prerequisites

- Python 3.7 or higher
- Flask (install via `pip install flask`)

### Setup

1. Clone or download the project repository:

```sh
git clone https://github.com/jasondbroomes-dev/AI_native-_journey.git
cd AI_native-_journey
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Run the web application:

```sh
python3 song_vibe_app.py
```

4. Open your browser and go to: **http://127.0.0.1:5002**

### Alternative: Enhanced Version

For the advanced command-line version with data structures:

```sh
python3 song_vibe_enhanced.py
```

## Usage Examples

### Web Interface
1. **Visit** http://127.0.0.1:5002
2. **Choose a mood** by clicking emoji buttons or typing your feelings
3. **Get recommendations** instantly with YouTube links
4. **Save favorites** for later listening
5. **Add custom songs** to the library

### Text Input Examples
- "I'm feeling happy and energetic"
- "I need something calm to study"
- "I'm sad and want to cry"
- "I want to party and dance"

### Word-Based Recommendations
- **Noun:** "music" + **Verb:** "dance" + **Adjective:** "happy"
- **Noun:** "heart" + **Verb:** "love" + **Adjective:** "romantic"

## Technical Details

### Data Structures Used
- **Enums** - `Mood` enum with 18 different mood types
- **Data Classes** - `Song` class with comprehensive metadata
- **Multiple Indexes** - Efficient lookup by mood, artist, genre, energy, tempo
- **Counters** - Track user preferences and mood history
- **DefaultDict** - Automatic list creation for new moods

### Algorithms
- **Natural Language Processing** - Analyzes text input to detect mood
- **Personalized Recommendations** - Learns from your listening history
- **Energy-based Matching** - Finds songs matching your energy preferences
- **Diversity Algorithm** - Avoids recommending the same artists repeatedly

### Web Technologies
- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Glass morphism design with gradients
- **Icons:** Font Awesome and emoji support

## API Endpoints

- `GET /` - Main web interface
- `POST /get_recommendation` - Get song based on mood
- `POST /get_word_recommendation` - Get song based on words
- `GET /get_vibes` - Get all available moods
- `GET /get_favorites` - Get user's favorite songs
- `POST /save_favorite` - Save a song to favorites
- `POST /add_vibe` - Add custom song to library

## Contributing

Feel free to contribute to this project by:
- Adding new songs to the library
- Improving the mood detection algorithms
- Enhancing the web interface
- Adding new features

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with AI assistance for learning and development
- Song recommendations curated for various moods and activities
- YouTube integration for instant music preview
- Modern web design principles for optimal user experience

---

**Happy listening! 🎵✨**

---

*Built with ❤️ during my AI Native Journey*
