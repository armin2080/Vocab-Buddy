# 🇩🇪 Vocab Buddy - German Vocabulary Learning Web App

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://djangoproject.com)
[![Groq AI](https://img.shields.io/badge/AI-Groq-green.svg)](https://groq.com)
[![PWA](https://img.shields.io/badge/PWA-Ready-blueviolet.svg)](#pwa-support)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern Django web application designed to help users learn German vocabulary through spaced repetition, interactive flashcard review, AI-powered language validation, personalized quizzes, and a responsive mobile-first interface with PWA support.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [PWA Support](#-pwa-support)
- [Deployment](#-deployment)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Learning Features
- **Smart Word Addition**: Add German words with AI-powered metadata extraction
- **German Language Validation**: AI ensures only authentic German words are accepted
- **Automatic CEFR Classification**: Words categorized by proficiency level (A1–C2)
- **Example Sentences**: AI-generated contextual examples for each word
- **Verb Conjugations**: Automatic parsing and storage of all verb forms (present, past, perfect)
- **Interactive Flashcards**: Flip-based card system with examples and verb conjugations
- **Spaced Repetition Algorithm**: Intelligent word selection based on mastery level and review frequency
- **Multiple-Choice Quizzes**: Test knowledge with randomized questions and instant feedback

### 📊 Dashboard & Analytics
- **Weekly Progress Chart**: Visual bar chart showing words added each day over the past week
- **Study Streak**: Track consecutive days of vocabulary practice
- **Learning Statistics**: Total words, mastered words, and words due for review
- **Personal Vocabulary List**: Browse, search, and manage your word collection

### 📱 User Interface
- **Responsive Design**: Mobile-first layout that works on all devices
- **Tailwind CSS Styling**: Modern, accessible interface matching the original frontend theme
- **Server-Rendered Templates**: Fast, SEO-friendly Django templates (no JS framework required)
- **Keyboard-Friendly**: Full keyboard navigation support for accessibility

### 🌐 PWA Support
- **Install as App**: Save the web app to your home screen on mobile and desktop
- **Offline Support**: Service worker caches core assets for offline functionality
- **Web Manifest**: Installable Progressive Web App with custom icons and theme colors
- **Native App Experience**: Standalone display mode with app-like feel

### 🤖 AI Integration
- **Groq LLM**: Fast, cost-effective AI via Groq's language models
- **Language Detection**: Validates German vs. non-German input
- **Structured Parsing**: Extracts word metadata (translation, CEFR level, examples, verb forms)
- **Fallback Verb Detection**: Automatic retry with enhanced prompts for verb forms
- **Persistence**: AI-generated data stored at creation time for reliable rendering

### 🔐 Authentication & Personalization
- **User Accounts**: Secure registration and login system
- **Per-User Vocabulary**: Each user maintains their own word list and progress
- **Session Management**: Stateful sessions with automatic timeout
- **Personalized Stats**: Dashboard tailored to each user's learning journey

---

## 🔧 Prerequisites

- **Python 3.12+**
- **Django 6.0+**
- **SQLite** (included with Python)
- **Groq API Key** (for AI word processing)
- **Pillow** (for icon generation; included in requirements)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/armin2080/Vocab-Buddy.git
cd Vocab-Buddy
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .env

# macOS/Linux
source .env/bin/activate

# Windows
.env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the project root with your Groq API key:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Or add it to `Vocab_Buddy/settings.py`:
```python
GROQ_API_KEY = "your_groq_api_key_here"
```

### 5. Initialize the Database
```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional, for Django Admin)
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

---

## 🏃 Running the Application

### Development Server
```bash
python manage.py runserver
```

The app will be available at `http://localhost:8000`

### Production Deployment
See [FRONTEND_DEPLOYMENT.md](FRONTEND_DEPLOYMENT.md) for detailed production setup instructions including:
- Gunicorn configuration
- Nginx reverse proxy setup
- WhiteNoise static file serving
- HTTPS/SSL configuration
- PWA installability requirements

---

## ⚙️ Configuration

### Environment Variables
```bash
GROQ_API_KEY          # Required: Groq API key for AI features
DEBUG                 # Optional: Set to False for production
ALLOWED_HOSTS         # Optional: Comma-separated list of allowed hosts
SECRET_KEY            # Optional: Django secret key (auto-generated if missing)
```

### Django Settings
Edit `Vocab_Buddy/settings.py` to customize:
- Database backend
- Static file storage
- Email configuration
- CORS settings
- API keys

### Getting a Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Generate an API key in your dashboard
4. Add to environment or settings as shown above

---

## 📖 Usage

### Getting Started
1. **Create Account**: Register with username and password
2. **Add Words**: Click "Add Word" and enter German words
3. **Review Vocabulary**: Use "Flash Cards" to review words with spaced repetition
4. **Take Quizzes**: Test knowledge with "Quiz" mode
5. **Track Progress**: View your "Home" dashboard for weekly progress and streak

### Typical Learning Workflow
```
Register → Add German Words → Review with Flashcards → Take Quizzes → Track Progress
```

### Key Pages

| Page | Description |
|------|-------------|
| **Home** | Dashboard with weekly progress chart, study streak, and learning stats |
| **Flash Cards** | Interactive spaced repetition review session with examples and verb forms |
| **Quiz** | Multiple-choice questions from your vocabulary (4+ words required) |
| **Vocabulary** | Browse, search, and manage your word collection |
| **Add Word** | Add new German words (AI extracts translation, CEFR level, examples, verb forms) |

---

## 📁 Project Structure

```
Vocab-Buddy/
├── Vocab_Buddy/              # Django project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # URL routing
│   ├── middleware.py         # Authentication middleware
│   ├── context_processors.py # Template context helpers
│   ├── streaks.py            # Study streak calculation
│   └── pwa.py                # PWA manifest and service worker
├── authentication/           # User registration and login
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── words/                    # Vocabulary management
│   ├── models.py             # Word and UserWord models
│   ├── views.py              # Add/list/delete word views
│   ├── forms.py              # Word input validation and AI parsing
│   └── urls.py
├── learning/                 # Flashcards, quizzes, dashboard
│   ├── models.py             # ReviewSession and QuizResult models
│   ├── views.py              # Flashcard, quiz, and dashboard views
│   ├── forms.py              # Review and quiz forms
│   ├── scheduler.py          # Spaced repetition algorithm
│   └── urls.py
├── templates/                # Server-rendered HTML templates
│   ├── base.html             # Base layout with header and navigation
│   ├── home.html             # Dashboard with weekly chart and stats
│   ├── authentication/       # Login and registration
│   ├── words/                # Word list, add word forms
│   └── learning/             # Flashcard and quiz templates
├── static/                   # CSS, JavaScript, icons
│   ├── css/
│   │   ├── fonts.css         # Font definitions
│   │   └── theme.css         # Theme variables and styling
│   ├── js/
│   │   ├── ui.js             # Flashcard interactivity
│   │   └── verb-panel.js     # Verb conjugation table rendering
│   └── icons/                # PWA app icons (generated from logo)
│       ├── icon-192.png
│       ├── icon-512.png
│       ├── icon-maskable-512.png
│       └── ...
├── ai_service.py             # Groq AI service wrapper
├── manage.py                 # Django management command
├── requirements.txt          # Python dependencies
├── db.sqlite3                # SQLite database (auto-created)
└── README.md                 # This file
```

---

## 🏗️ Technology Stack

### Backend
- **Django 6.0.5**: Web framework with authentication, ORM, and admin
- **Python 3.12**: Programming language
- **SQLite**: Lightweight relational database
- **Groq LLM**: AI for German language processing and word metadata

### Frontend
- **Tailwind CSS**: Utility-first CSS framework
- **Vanilla JavaScript**: Interactive UI (flashcards, quizzes)
- **Server-Rendered Templates**: Django template language for HTML generation
- **Responsive Design**: Mobile-first approach with flexbox and media queries

### Deployment
- **Gunicorn**: WSGI application server
- **WhiteNoise**: Static file serving (production)
- **Nginx**: Reverse proxy and load balancer (recommended)

---

## 🌐 PWA Support

Vocab Buddy is a Progressive Web App (PWA) and can be installed on mobile and desktop devices.

### Features
- **Installable**: Add to home screen on Android, iOS, and desktop browsers
- **Offline Support**: Service worker caches critical assets and pages
- **App Icon**: Custom 192×192 and 512×512 icons from your logo
- **Splash Screen**: Branded loading experience
- **Theme Color**: Custom theme color for address bar

### Installation

#### Android/Chrome
1. Open the app in Chrome
2. Tap the menu (⋮) → "Install app"
3. Confirm installation

#### iOS/Safari
1. Open the app in Safari
2. Tap Share → "Add to Home Screen"
3. Confirm and launch

#### Desktop (Chrome/Edge)
1. Open the app
2. Click the install icon in the address bar
3. Confirm installation

### HTTPS Requirement
PWA install prompts require **HTTPS** in production. Development (localhost) is exempt. For production, obtain an SSL certificate from:
- Let's Encrypt (free)
- Cloudflare (free tier available)
- Other certificate authorities

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use a strong `SECRET_KEY`
- [ ] Set up HTTPS with SSL certificate
- [ ] Run `collectstatic` to compile static files
- [ ] Use Gunicorn and Nginx
- [ ] Configure environment variables (GROQ_API_KEY, etc.)
- [ ] Set up database backups
- [ ] Enable CSRF protection

### Quick Deployment with Gunicorn & Nginx

See [FRONTEND_DEPLOYMENT.md](FRONTEND_DEPLOYMENT.md) for detailed instructions including:
- Gunicorn service configuration
- Nginx reverse proxy setup
- SSL certificate setup
- Security hardening

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Django**: Web framework powering the backend
- **Groq**: Fast, cost-effective AI language models
- **Tailwind CSS**: Modern utility-first styling
- **Pillow**: Image processing for PWA icons
- **SQLite**: Reliable embedded database

---

## 📞 Support & Feedback

For issues, questions, or suggestions:

1. Check [GitHub Issues](https://github.com/armin2080/Vocab-Buddy/issues)
2. Create a new issue with detailed description and screenshots
3. Include relevant error logs or console output

### Common Issues

**"Word not recognized as German"**
- Ensure you're entering actual German words
- Check for correct spelling and special characters (ä, ö, ü, ß)
- Try a different word to verify the system is working

**"Not enough words for review"**
- Add at least 5 words using the "Add Word" feature
- Wait a moment for AI processing to complete

**PWA not installing**
- Ensure using HTTPS (production) or localhost (development)
- Update your browser to the latest version
- Try a different browser if issues persist

---

**Happy Learning! 🎓📚**

*Vocab Buddy - Making German vocabulary learning interactive, personalized, and fun!*
