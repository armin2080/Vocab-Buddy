# 🇩🇪 Vocab Buddy - German Vocabulary Learning Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![Groq AI](https://img.shields.io/badge/AI-Groq-green.svg)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A smart Telegram bot designed to help users learn German vocabulary through spaced repetition, interactive review sessions, and AI-powered language validation.

## 🚀 **[Try the Bot Now!](https://t.me/vocabularyBuddy_bot)**

**Ready to start learning German? Click the link above to begin your vocabulary journey!** 📚✨

Simply search for `@vocabularyBuddy_bot` on Telegram or use the direct link: https://t.me/vocabularyBuddy_bot

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Bot Commands](#-bot-commands)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Logging](#-logging)
- [Architecture](#-architecture)
- [Development](#-development-workflow)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 What's New

### ✨ Latest Updates
- 🇩🇪 **German Language Validation**: AI now ensures only authentic German words are accepted
- 📚 **Enhanced Help System**: Comprehensive `/help` command with detailed guides
- 🔧 **Improved Error Handling**: Better user feedback for invalid inputs
- 🎯 **Word Type Preservation**: Maintains correct grammatical forms (adjectives, verbs, nouns)
- 🔄 **Retry Logic**: Users can immediately correct mistakes during word addition
- 👑 **Admin Management System**: Complete admin toolkit with user management and broadcast messaging
- 📢 **Broadcast Announcements**: Admins can send announcements to all users with delivery tracking
- 🧠 **Interactive Quiz System**: New multiple-choice vocabulary quizzes with scoring and performance tracking

---

## ✨ Features

### 🎯 Core Functionality
- **Smart Word Addition**: AI-powered word analysis with automatic CEFR level classification
- **German Language Validation**: Ensures only authentic German words are accepted
- **Spaced Repetition Algorithm**: Intelligent word selection based on review frequency and performance
- **Interactive Review Sessions**: Step-by-step vocabulary practice with examples and contextual paragraphs
- **Multiple-Choice Quizzes**: Test knowledge with randomized quiz questions and instant feedback
- **Vocabulary Management**: Personal word list with easy removal and organization by CEFR levels
- **Comprehensive Help System**: Built-in `/help` command with detailed usage instructions

### 📊 Analytics & Community
- **Community Statistics**: View most popular words across all users by CEFR level
- **Personal Progress Tracking**: Monitor review counts and learning progress
- **Usage Analytics**: Comprehensive logging system for performance monitoring

### 👑 Admin & Management
- **Admin Access Control**: Secure admin-only command system with proper authorization
- **User Management**: Complete user listing with registration dates and vocabulary statistics
- **Bot Analytics**: Comprehensive statistics including active users, word counts, and review metrics
- **Broadcast Messaging**: Send announcements to all users with delivery tracking and reporting
- **Database Management**: Automatic schema upgrades and data integrity maintenance
- **Comprehensive Logging**: All admin actions logged for security and audit purposes

### 🤖 AI Integration
- **Groq AI Integration**: Automatic word translation and CEFR level estimation
- **Language Detection**: Advanced AI validation to ensure German-only vocabulary
- **Word Type Preservation**: Maintains correct grammatical forms (adjectives stay adjectives, etc.)
- **Context Generation**: AI-generated example sentences and paragraphs using learned vocabulary
- **Smart Error Handling**: Graceful handling of non-German inputs with helpful feedback

## 🔧 Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Groq API Key (for AI functionality)
- SQLite (included with Python)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/armin2080/Vocab-Buddy.git
   cd Vocab-Buddy
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   # Windows
   .\env\Scripts\activate
   # macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration** (see [Configuration](#-configuration) section)

5. **Run the bot**
   ```bash
   python bot.py
   ```

## ⚙️ Configuration

Create a `config.json` file in the project root:

```json
{
  "BOT_TOKEN": "your_telegram_bot_token_here",
  "AI_TOKEN": "your_groq_api_key_here",
  "ADMIN_ID": 123456789
}
```

### Getting API Keys

1. **Telegram Bot Token**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot with `/newbot`
   - Follow the instructions and copy the token

2. **Groq API Key**:
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up for an account
   - Generate an API key in the dashboard

3. **Admin ID (Optional)**:
   - Get your Telegram user ID to enable admin features
   - Start a chat with [@userinfobot](https://t.me/userinfobot) to find your ID
   - Add this ID to enable admin commands and broadcast functionality
   - If not set, admin features will be disabled

## 📖 Usage

### Getting Started

1. Start a conversation with your bot on Telegram
2. Send `/start` to register and get welcome message
3. Use `/help` to see all available commands and features
4. Use `/add_word` to begin building your vocabulary (German words only!)
5. Practice with `/review_words` when you have 5+ words
6. Manage your vocabulary with `/my_words`
7. Check community stats with `/top_words`

### Typical Workflow

```
1. Learn commands (/help) → 2. Add German words → 3. Review regularly → 4. Track progress → 5. Expand vocabulary
```

## 🤖 Bot Commands

| Command | Description | Requirements |
|---------|-------------|--------------|
| `/start` | Register/welcome message | None |
| `/help` | Show comprehensive command guide and usage tips | None |
| `/add_word` | Add new German word to vocabulary | German words only |
| `/review_words` | Start interactive review session | 5+ words in vocabulary |
| `/quiz` | Take vocabulary quiz with multiple-choice questions | 4+ words in vocabulary |
| `/my_words` | View and manage personal vocabulary | None |
| `/top_words` | View community word statistics | None |
| `/cancel` | Cancel current conversation (during word addition) | Active conversation |

### � Admin Commands

*Available only for configured administrators*

| Command | Description | Requirements |
|---------|-------------|--------------|
| `/admin_help` | Show admin command help and documentation | Admin access |
| `/admin_users` | List all registered users with detailed statistics | Admin access |
| `/admin_stats` | Display comprehensive bot usage analytics | Admin access |
| `/admin_broadcast` | Send announcements to all users | Admin access |

#### 📢 Admin Broadcast Features
- **Message Composition**: Interactive message creation with preview
- **HTML Formatting Support**: Rich text formatting for announcements
- **Delivery Tracking**: Real-time progress monitoring during broadcast
- **Comprehensive Reporting**: Detailed success/failure statistics
- **Professional Formatting**: Messages include admin header and signature
- **Cancellation Option**: Ability to cancel broadcast before sending
- **Error Handling**: Graceful handling of blocked users and delivery failures

### �🔥 New Features

#### 🧠 Interactive Quiz System
- **Multiple-Choice Questions**: Test knowledge with 4-option questions
- **Randomized Question Order**: Different quiz experience each time
- **Smart Wrong Answers**: Incorrect options come from user's other vocabulary words
- **Performance Scoring**: Detailed scoring with percentage and performance feedback
- **Instant Feedback**: Immediate confirmation of correct/incorrect answers
- **Question Review**: Complete review of all questions and correct answers
- **Progress Tracking**: Monitor quiz performance to identify learning gaps
- **Flexible Length**: Adaptive quiz length based on vocabulary size (up to 5 questions)

#### 🇩🇪 German Language Validation
- **Smart Detection**: AI automatically detects and rejects non-German words
- **Helpful Feedback**: Clear messages guide users to enter German vocabulary
- **Retry Logic**: Users can immediately try again with correct input
- **Examples**: Bot explains what constitutes a valid German word

#### 📚 Enhanced Help System
- **Comprehensive Guide**: Detailed explanations of all features
- **Getting Started Tutorial**: Step-by-step instructions for new users
- **CEFR Level Guide**: Understanding of difficulty levels with color coding
- **Learning Tips**: Best practices for effective vocabulary acquisition

### Interactive Features

- **Button-based confirmations** for word additions
- **German language validation** with immediate feedback
- **Step-by-step review process** with examples and paragraphs
- **Vocabulary management interface** with easy word removal
- **CEFR level organization** (A1, A2, B1, B2, C1, C2)
- **Retry functionality** for incorrect inputs
- **Comprehensive help system** accessible anytime

### 🎯 Language Learning Features

#### Word Type Preservation
- **Adjectives stay adjectives** (schnell → schnell, not Schnelligkeit)
- **Nouns include articles** (das Haus, der Mann, die Frau)
- **Verbs in infinitive form** (laufen, sprechen, haben)
- **Accurate translations** for each grammatical category

#### Learning Methodology
- **Spaced Repetition**: Words appear based on your mastery level
- **Contextual Learning**: See words in sentences and paragraphs
- **Progressive Difficulty**: CEFR levels from A1 (beginner) to C2 (advanced)
- **Community Learning**: Discover popular words other learners are studying

## 📁 Project Structure

```
Vocab-Buddy/
├── bot.py                 # Main bot application
├── database.py           # Database management and word selection algorithms
├── agent.py              # Groq AI client for word processing
├── config.json           # Configuration file (not in repo)
├── requirements.txt      # Python dependencies
├── vocab_buddy.db        # SQLite database (auto-generated)
├── vocab_buddy.log       # Application logs (auto-generated)
├── .gitignore           # Git ignore rules
├── LICENSE              # Project license
└── README.md            # This file
```

## 🗄️ Database Schema

### Tables

**users**
- `id` (INTEGER PRIMARY KEY)
- `telegram_id` (INTEGER UNIQUE)
- `username` (TEXT)
- `created_at` (TIMESTAMP)

**words**
- `id` (INTEGER PRIMARY KEY)
- `word` (TEXT UNIQUE)
- `translation` (TEXT)
- `cefr_level` (TEXT)
- `created_at` (TIMESTAMP)

**words_users**
- `id` (INTEGER PRIMARY KEY)
- `user_id` (INTEGER FOREIGN KEY)
- `word_id` (INTEGER FOREIGN KEY)
- `review_count` (INTEGER DEFAULT 0)
- `last_reviewed` (TIMESTAMP)
- `created_at` (TIMESTAMP)

## 📊 Logging

The bot includes comprehensive logging for monitoring and debugging:

### Log Features
- **File logging**: Saved to `vocab_buddy.log`
- **Console output**: Real-time monitoring
- **Structured format**: Timestamp, level, and emoji-coded messages
- **User activity tracking**: All actions with user identification
- **Error monitoring**: Detailed error reporting with context

### Log Levels
- `INFO`: Normal operations (user actions, successful operations)
- `WARNING`: Non-critical issues (insufficient words, duplicates)
- `ERROR`: Serious problems (API failures, database errors)

### Example Log Entry
```
2025-07-29 14:23:15 - __main__ - INFO - 🎉 Successfully added word 'Hund' to user john_doe's vocabulary
```

## 🏗️ Architecture

### Core Components

1. **Bot Controller** (`bot.py`)
   - Telegram API integration
   - Command and callback handling
   - User interface management

2. **Database Manager** (`database.py`)
   - SQLite operations
   - Spaced repetition algorithm
   - Word selection logic

3. **AI Agent** (`agent.py`)
   - Groq API integration
   - German language detection and validation
   - Word processing and translation with grammatical accuracy
   - Content generation for examples and paragraphs

### Key Algorithms

**German Language Validation**
```python
# AI validates input language before processing
if ai_response.strip().lower() == "not german":
    # Provide helpful feedback and retry opportunity
    return WORD  # Keep conversation active
```

**Spaced Repetition Scoring**
```python
score = base_weight / (1 + review_count) * time_decay_factor
```

**Word Selection Strategy**
- Prioritizes less-reviewed words
- Considers time since last review
- Ensures vocabulary diversity
- Prevents duplicate selections
- Maintains grammatical accuracy

## 🔄 Development Workflow

### Adding New Features

1. **Database changes**: Update `database.py` and schema
2. **Bot commands**: Add handlers in `bot.py`
3. **AI integration**: Extend `agent.py` for new AI features
4. **Language validation**: Ensure proper German language handling
5. **Testing**: Test with various user scenarios including edge cases
6. **Logging**: Add appropriate log statements for monitoring
7. **Documentation**: Update README and comments

### Code Style

- Use descriptive function names and comments
- Include logging for important operations
- Follow Python PEP 8 style guidelines
- Add error handling for external API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### Contribution Guidelines

- Ensure all new features include appropriate logging
- Add tests for new functionality
- Update documentation for user-facing changes
- Follow existing code patterns and style

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Telegram Bot API** for the excellent bot platform
- **Groq** for powerful AI language processing
- **Python-telegram-bot** library for seamless Telegram integration
- **SQLite** for reliable local data storage

## 📞 Support

For issues, questions, or feature requests:

1. Check existing [GitHub Issues](https://github.com/armin2080/Vocab-Buddy/issues)
2. Create a new issue with detailed description
3. Include relevant log entries for bug reports
4. Provide steps to reproduce problems

### 🐛 Common Issues

**"Word not recognized as German"**
- Ensure you're entering actual German words
- Try different spellings or word forms
- Check that special characters are included (ä, ö, ü, ß)

**"Not enough words for review"**
- Add at least 5 words using `/add_word`
- Each word must be confirmed and saved to your vocabulary

**Bot not responding**
- Check if the bot is online
- Try `/start` to reinitialize your session
- Contact support if issues persist

---

**Happy Learning! 🎓📚**

*Vocab Buddy - Making German vocabulary learning interactive, accurate, and fun!*