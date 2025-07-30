# Group 4 - English Listening Service

A Django microservice for English listening comprehension practice and testing, featuring text-to-speech audio generation and interactive quiz functionality.

## 🎯 Overview

This microservice provides an interactive English listening practice platform with two main modes:
- **Practice Mode**: Learn at your own pace with unlimited attempts
- **Quiz Mode**: Timed assessments with immediate feedback

## ✨ Features

### 🔊 Audio Generation
- **Text-to-Speech**: Microsoft Edge-TTS integration
- **Multiple Accents**: US English (AriaNeural) and UK English (SoniaNeural)
- **Smart Sentence Splitting**: Handles abbreviations (Dr., Mr., etc.) and ordinal numbers
- **Timestamp Synchronization**: Precise word-level timing for audio navigation

### 📚 Content Management
- **CEFR Difficulty Levels**: A1, A2, B1, B2, C1, C2
- **Categorized Content**: Organized by topics and themes
- **Interactive Transcripts**: Show/hide transcript functionality
- **Multiple Question Types**: Multiple choice, true/false, fill-in-the-blank, short answer

### 🎮 Interactive Features
- **Accent Selection**: Choose between American and British pronunciation
- **Timer System**: Configurable test duration (3x audio length)
- **Real-time Results**: Immediate feedback with detailed explanations
- **Client-side Processing**: Fast, offline-capable quiz evaluation

## 🏗️ Architecture

### Models
- **Reading**: Core content model with difficulty levels and categories
- **Question**: Associated quiz questions with multiple types
- **ReadingCategory**: Content organization and theming
- **ReadingTag**: Flexible content tagging system

### Views Structure
```
views.py
├── Main Pages (HTML Templates)
│   ├── home() - Landing page
│   ├── practice_selection() - Practice mode selection
│   └── quiz_selection() - Quiz mode selection
├── Reading Views
│   ├── reading_list_practice() - Browse practice content
│   ├── practice_mode() - Interactive practice interface
│   ├── reading_list_quiz() - Browse quiz content
│   └── quiz_mode() - Timed quiz interface
└── API Endpoints
    └── generate_audio() - TTS audio generation
```

### Templates
- `group4.html` - Main landing page
- `practice_level_selection.html` - Practice difficulty selection
- `practice_view.html` - Interactive practice interface with audio player
- `quiz_view.html` - Timed quiz interface with client-side evaluation
- `test_level_selection.html` - Quiz difficulty selection
- `search_readings.html` - Content browsing and search

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 4.x
- MySQL database
- Required Python packages (see `group4/requirements.txt`)

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup**
* If you run on linux
   ```bash
   bash group4/scripts/linux/startup.sh
   ```
* If you run on windows
  ```bash
  .\group4\scripts\windows\startup.bat
  ```

3. **Initialize db with data**
* Note: this will require a set of .json files located at `group4/scripts/data/`
  ```bash
  python group4/scripts/initialize_test_data.py
  ```

Now you're all set up and ready to go :)

## 🔧 Configuration

### Environment Variables
The application uses the following database configuration from `.env`:
```properties
DATABASE_HOST=127.0.0.1
DATABASE_NAME=software-database
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_PORT=3307
```

### TTS Configuration
The Edge-TTS integration supports multiple voices:
- **US English**: `en-US-AriaNeural`
- **UK English**: `en-GB-SoniaNeural`

## 📁 Project Structure

```
group4/
├── admin.py              # Django admin configuration
├── apps.py               # App configuration
├── models.py             # Data models (Reading, Question, etc.)
├── views.py              # View controllers and API endpoints
├── urls.py               # URL routing configuration
├── requirements.txt      # Python dependencies
├── migrations/           # Database migrations
├── static/group4/        # Static assets (CSS, JS, images)
├── templates/            # HTML templates
├── scripts/              # Utility scripts
└── tests.py              # Unit tests
```

## 🎮 Usage Guide

### Practice Mode
1. Select difficulty level (A1-C2)
2. Choose a reading passage
3. Select accent preference (US/UK)
4. Listen to generated audio
5. Practice with interactive transcript
6. No time limits or restrictions

### Quiz Mode
1. Select difficulty level
2. Choose quiz content
3. Select accent for audio generation
4. Complete timed assessment
5. Receive immediate feedback
6. View detailed results and corrections

### Audio Features
- **Play/Pause Controls**: Standard audio player interface
- **Speed Adjustment**: Variable playback speed
- **Sentence Navigation**: Jump to specific sentences
- **Transcript Sync**: Highlight current audio position

## 🐛 Known Issues & Limitations

1. **Audio Generation**: Requires internet connection for Edge-TTS
2. **Browser Compatibility**: Modern browsers required for audio features
3. **Mobile Responsiveness**: Some UI elements may need mobile optimization

## 📝 API Documentation

### Audio Generation Endpoint
```
POST /group4/api/readings/<int:reading_id>/generate/
Content-Type: application/json

{
    "voice": "en-US-AriaNeural"  // or "en-GB-SoniaNeural"
}

Response:
{
    "audio_url": "data:audio/mp3;base64,<base64_audio>",
    "duration": 120.5,
    "timestamps": [...]
}
```
---

**Group 4 - Software Engineering Course 1403-02**  
*English Listening Comprehension Microservice*
