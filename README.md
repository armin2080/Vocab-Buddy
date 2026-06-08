# 🇩🇪 Vocab Buddy - German Vocabulary Learning Web App

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://djangoproject.com)
[![Groq AI](https://img.shields.io/badge/AI-Groq-green.svg)](https://groq.com)
[![PWA](https://img.shields.io/badge/PWA-Ready-blueviolet.svg)](#pwa-support)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Turn German words you recognize into German you can actually use.**

Vocab Buddy is a personal, AI-assisted German learning workspace. Add any German word and the app turns it into a useful learning card with its meaning, CEFR level, examples, grammatical forms, and review history. Then move beyond memorization in **Practice Lab**, where an AI writing coach challenges you to use difficult words in context and gives detailed, conversational feedback.

Instead of giving every learner the same fixed lesson, Vocab Buddy builds practice around **your vocabulary**, **your mistakes**, and **your progress**.

> Add words you care about. Review the ones you are likely to forget. Practice using them. Get feedback. Improve.

## 📋 Table of Contents

- [Features](#-features)
- [How Vocab Buddy Helps](#-how-vocab-buddy-helps)
- [AI Practice Coach](#-ai-practice-coach)
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

### Build a Useful Personal Dictionary
- Add a German word, phrase, conjugated verb, or noun without an article.
- Let AI validate the input and normalize it into a useful dictionary form.
- Receive an English translation, CEFR difficulty level, and contextual example sentences.
- See present, past, and perfect conjugations for verbs.
- See singular, plural, masculine, and feminine noun forms when they exist.
- Open any saved word to edit its information, retrieve fresh AI metadata, or remove it.

### Remember More With Focused Review
- Review vocabulary with interactive flashcards instead of passively reading a list.
- See examples and grammatical forms while reviewing.
- Prioritize words based on difficulty, mistakes, review frequency, and time since the last review.
- Track reviews, correct answers, accuracy, mastered words, weekly activity, and study streaks.

### Turn Vocabulary Into Active German
- Enter Practice Lab and receive a challenge built from five difficult words in your own collection.
- Write a German paragraph that uses all five words naturally.
- Get structured feedback on word usage, grammar, spelling, and natural phrasing.
- Compare your paragraph with an improved German version.
- Revise your work, ask follow-up questions, and continue the conversation with an AI coach that remembers the active session.

### Learn Anywhere
- Use a responsive interface designed for phones, tablets, and desktops.
- Install Vocab Buddy as a Progressive Web App.
- Keep every account's vocabulary, progress, and practice sessions separate.

---

## 🎓 How Vocab Buddy Helps

Many vocabulary tools stop after showing a translation. Vocab Buddy supports the full learning loop:

| Step | What Vocab Buddy Does | Why It Matters |
|------|------------------------|----------------|
| **Discover** | Turns a word into structured, learner-friendly information | You learn more than a one-word translation |
| **Understand** | Shows examples, noun forms, verb conjugations, and CEFR level | You see how the word behaves in real German |
| **Remember** | Brings challenging and forgotten words back into review | Study time focuses on words that need attention |
| **Use** | Builds writing challenges from your own vocabulary | Passive recognition becomes active language ability |
| **Improve** | Gives corrections, explanations, and a stronger rewritten version | Mistakes become practical learning opportunities |

Your vocabulary remains editable. If AI-generated information is missing or outdated, you can correct it manually or ask Vocab Buddy to retrieve the word information again.

---

## 🤖 AI Practice Coach

Practice Lab is not a blank, generic chatbot. It begins with a clear task based on your learning history:

1. Vocab Buddy selects five words from your vocabulary, prioritizing more advanced words, frequently missed words, and words that need review.
2. You write a German paragraph using all five challenge words.
3. The coach checks whether each word was used correctly and naturally.
4. It explains important grammar, spelling, and phrasing improvements.
5. It provides an improved version and invites you to revise or ask follow-up questions.

During an open Practice Lab session, the coach receives the previous messages so it can understand revisions and continue the same conversation. When you select **Close Session**, the session and its chat history are deleted.

Practice Lab is designed as an expandable home for future exercises such as speaking practice, voice recognition, listening tasks, role-play conversations, and other guided activities.

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
Create a `.env.local` file in the project root with your Groq API key:
```bash
cp .env.local.example .env.local
```

Then edit `.env.local`:
```bash
GROQ_API_KEY=your_groq_api_key_here
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
2. **Build Your Vocabulary**: Add words you encounter in lessons, conversations, books, or media
3. **Review Intelligently**: Use Flash Cards to focus on challenging and forgotten words
4. **Practice Writing**: Open Practice Lab and write a paragraph using five selected words
5. **Track Progress**: View your "Home" dashboard for weekly progress and streak

### What Happens When You Add a Word?

Enter a German word such as `Haus`, `Lehrerin`, or a conjugated verb such as `ging`. Vocab Buddy uses AI to validate and normalize it, then builds a richer vocabulary entry containing the information that applies:

- Dictionary form and English meaning
- CEFR difficulty level
- German example sentences with translations
- Noun article, singular, plural, and gendered counterparts
- Verb infinitive, type, present tense, past tense, participle, and auxiliary

Every entry opens into a detailed page where you can inspect the information, correct fields manually, retrieve fresh AI information, or delete the word from your collection.

### What Feedback Does Practice Lab Give?

After you submit a paragraph, the AI coach returns clearly formatted feedback:

- An overall assessment of the paragraph
- A check of how each challenge word was used
- Specific grammar, spelling, and word-choice improvements
- Suggestions for more natural German phrasing
- An improved version of your paragraph
- A focused next step for revision

You can respond with an updated paragraph or ask questions such as why a correction was needed. The coach remembers the active conversation until you close the session.

### Learning Workflow
```
Register → Add German Words → Review with Flashcards → Practice Writing → Track Progress
```

### Key Pages

| Page | Description |
|------|-------------|
| **Home** | Dashboard with weekly progress chart, study streak, and learning stats |
| **Flash Cards** | Interactive spaced repetition review session with examples and verb forms |
| **Practice Lab** | Use difficult saved words in a paragraph, receive corrections, and revise with an AI coach |
| **Vocabulary** | Browse selectable word cards; inspect, edit, refresh, or delete detailed entries |
| **Add Word** | Add new German words with AI-extracted translation, CEFR level, examples, noun forms, and verb forms |

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
│   ├── views.py              # Add/list/detail/edit/refresh/delete word views
│   ├── forms.py              # Word input validation and AI parsing
│   └── urls.py
├── learning/                 # Flashcards and dashboard
│   ├── models.py             # ReviewSession model
│   ├── views.py              # Flashcard and dashboard views
│   ├── forms.py              # Review forms
│   ├── scheduler.py          # Spaced repetition algorithm
│   └── urls.py
├── practice_lab/             # AI-guided writing practice
│   ├── models.py             # Temporary practice sessions and chat messages
│   ├── services.py           # Challenge selection and coach prompts
│   ├── views.py              # Session, conversation, and close-session views
│   ├── templatetags/         # Safe formatted feedback rendering
│   └── urls.py
├── templates/                # Server-rendered HTML templates
│   ├── base.html             # Base layout with header and navigation
│   ├── home.html             # Dashboard with weekly chart and stats
│   ├── authentication/       # Login and registration
│   ├── words/                # Word list, add word forms
│   ├── learning/             # Flashcard templates
│   └── practice_lab/         # Practice challenge and chat templates
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
- **Groq LLM**: AI for German language processing, word metadata, and conversational writing feedback

### Frontend
- **Tailwind CSS**: Utility-first CSS framework
- **Vanilla JavaScript**: Interactive UI for flashcards
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

**"Practice Lab is not ready"**
- Add at least 5 words to your vocabulary
- Practice Lab selects five challenging words from your saved collection
- Close the active session when finished to delete its conversation history

**PWA not installing**
- Ensure using HTTPS (production) or localhost (development)
- Update your browser to the latest version
- Try a different browser if issues persist

---

**Happy Learning! 🎓📚**

*Vocab Buddy - Making German vocabulary learning interactive, personalized, and fun!*
