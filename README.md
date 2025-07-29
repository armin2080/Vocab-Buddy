# 🇩🇪 Vocab Buddy - German Vocabulary Learning Bot

A smart Telegram bot designed to help users learn German vocabulary through spaced repetition, interactive review sessions, and community-driven word statistics.

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
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 Core Functionality
- **Smart Word Addition**: AI-powered word analysis with automatic CEFR level classification
- **Spaced Repetition Algorithm**: Intelligent word selection based on review frequency and performance
- **Interactive Review Sessions**: Step-by-step vocabulary practice with examples and contextual paragraphs
- **Vocabulary Management**: Personal word list with easy removal and organization by CEFR levels

### 📊 Analytics & Community
- **Community Statistics**: View most popular words across all users by CEFR level
- **Personal Progress Tracking**: Monitor review counts and learning progress
- **Usage Analytics**: Comprehensive logging system for performance monitoring

### 🤖 AI Integration
- **Groq AI Integration**: Automatic word translation and CEFR level estimation
- **Context Generation**: AI-generated example sentences and paragraphs using learned vocabulary
- **Smart Word Processing**: Handles various input formats and provides accurate translations

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
  "GROQ_API_KEY": "your_groq_api_key_here"
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

## 📖 Usage

### Getting Started

1. Start a conversation with your bot on Telegram
2. Send `/start` to register and get welcome message
3. Use `/add_word` to begin building your vocabulary
4. Practice with `/review_words` when you have 5+ words
5. Manage your vocabulary with `/my_words`
6. Check community stats with `/top_words`

### Typical Workflow

```
1. Add words → 2. Review regularly → 3. Track progress → 4. Expand vocabulary
```

## 🤖 Bot Commands

| Command | Description | Requirements |
|---------|-------------|--------------|
| `/start` | Register/welcome message | None |
| `/add_word` | Add new word to vocabulary | None |
| `/review_words` | Start interactive review session | 5+ words in vocabulary |
| `/my_words` | View and manage personal vocabulary | None |
| `/top_words` | View community word statistics | None |

### Interactive Features

- **Button-based confirmations** for word additions
- **Step-by-step review process** with examples and paragraphs
- **Vocabulary management interface** with easy word removal
- **CEFR level organization** (A1, A2, B1, B2, C1, C2)

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
   - Word processing and translation
   - Content generation

### Key Algorithms

**Spaced Repetition Scoring**
```python
score = base_weight / (1 + review_count) * time_decay_factor
```

**Word Selection Strategy**
- Prioritizes less-reviewed words
- Considers time since last review
- Ensures vocabulary diversity
- Prevents duplicate selections

## 🔄 Development Workflow

### Adding New Features

1. **Database changes**: Update `database.py` and schema
2. **Bot commands**: Add handlers in `bot.py`
3. **AI integration**: Extend `agent.py` for new AI features
4. **Testing**: Test with various user scenarios
5. **Logging**: Add appropriate log statements
6. **Documentation**: Update README and comments

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

---

**Happy Learning! 🎓📚**

*Vocab Buddy - Making German vocabulary learning interactive and fun!*