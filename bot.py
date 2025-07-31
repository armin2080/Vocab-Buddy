from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from typing import Final
from database import DatabaseManager
from telegram.ext import ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from agent import GroqClient
from datetime import datetime
import logging
import os


# Load the bot token from the config file
with open("config.json", "r") as f:
    config = json.load(f)
TOKEN: Final = config["BOT_TOKEN"]
ADMIN_ID: Final = config.get("ADMIN_ID", None)  # Optional admin ID

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('vocab_buddy.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Log startup
logger.info("🚀 Vocab Buddy Bot Starting Up...")
logger.info("📊 Loading configuration and initializing components...")
if ADMIN_ID:
    logger.info(f"👑 Admin functionality enabled for user ID: {ADMIN_ID}")
else:
    logger.info("⚠️ No admin ID configured - admin features disabled")

# Start database manager and agent client
groq_client = GroqClient()
db_manager = DatabaseManager()

logger.info("✅ Database Manager and Groq Client initialized successfully")


# Define conversation states
WORD, MEANING = range(2)
SHOW_WORDS, SHOW_EXAMPLES, SHOW_PARAGRAPH = range(3, 6)
MANAGE_VOCAB = range(6, 7)
ADMIN_MESSAGE = range(7, 8)

# Helper function to check if user is admin
def is_admin(user_id):
    """Check if the user is an admin"""
    return ADMIN_ID is not None and user_id == ADMIN_ID









async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"👋 START command from user {username} (ID: {user_id})")
    
    user_exists = db_manager.fetch_all('users', where_clause='telegram_id', where_args=[user_id])
    if not user_exists:
        db_manager.add_instance('users', columns=['telegram_id', 'username'], new_vals=[user_id, username])
        text = f"Hello @{username}! \nWelcome to Vocab Buddy! You have been registered."
        logger.info(f"✅ New user registered: {username} (ID: {user_id})")
    else:
        text = f"Hello @{username}! \nWelcome back to Vocab Buddy!"
        logger.info(f"🔄 Returning user: {username} (ID: {user_id})")

    await update.message.reply_text(text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show comprehensive help information about bot commands and features"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"❓ HELP command from user {username} (ID: {user_id})")
    
    help_text = """
🤖 <b>Vocab Buddy - Your German Learning Assistant</b>

Welcome to Vocab Buddy! Here's everything you need to know to get started with improving your German vocabulary:

📚 <b>MAIN COMMANDS:</b>

🆕 <b>/add_word</b> - Add new German words to your vocabulary
   • Simply type the command and follow the prompts
   • Only German words/phrases are accepted
   • The bot will automatically provide translations and CEFR levels
   • Confirm if the information is correct to add it to your collection

📖 <b>/review_words</b> - Practice with your vocabulary (minimum 5 words needed)
   • Reviews 5 words selected based on spaced repetition algorithm
   • Shows word list → example sentences → contextual paragraph
   • Tracks your review progress automatically

📚 <b>/my_words</b> - View and manage your vocabulary collection
   • See all your words organized by CEFR levels (A1-C2)
   • View review statistics for each word
   • Remove words you no longer want to study

📊 <b>/top_words</b> - See most popular words across all users
   • Discover trending vocabulary by difficulty level
   • See what other learners are studying most

❓ <b>/help</b> - Show this help message

🎯 <b>HOW TO GET STARTED:</b>

1️⃣ Use <b>/add_word</b> to build your vocabulary (aim for at least 5 words)
2️⃣ Practice with <b>/review_words</b> to reinforce learning
3️⃣ Check your progress with <b>/my_words</b>
4️⃣ Discover new words with <b>/top_words</b>

📈 <b>LEARNING FEATURES:</b>

🔄 <b>Spaced Repetition:</b> Words are reviewed based on how well you know them
🎯 <b>CEFR Levels:</b> Words are categorized from A1 (beginner) to C2 (advanced)
📝 <b>Contextual Learning:</b> See words in example sentences and paragraphs
📊 <b>Progress Tracking:</b> Monitor your review history and learning stats

💡 <b>TIPS FOR SUCCESS:</b>

• Add words regularly to build a diverse vocabulary
• Review consistently to improve retention
• Read the example sentences and paragraphs carefully
• Don't rush - take time to understand each word in context
• Remove words you've mastered to focus on challenging ones

🎓 <b>CEFR LEVEL GUIDE:</b>
🟢 A1 - Beginner (basic everyday words)
🔵 A2 - Elementary (common phrases and expressions)
🟡 B1 - Intermediate (familiar topics and situations)
🟠 B2 - Upper-Intermediate (complex texts and ideas)
🔴 C1 - Advanced (sophisticated vocabulary)
🟣 C2 - Proficient (near-native level expressions)

Ready to start learning? Try <b>/add_word</b> to add your first German word! 🚀

<i>Need more help? Feel free to explore the commands and see how they work!</i>
"""
    
    # Add admin section if user is admin
    if is_admin(user_id):
        help_text += """

👑 <b>ADMIN COMMANDS:</b>
You have administrative access! Use these commands:
• <b>/admin_help</b> - Show admin command help
• <b>/admin_users</b> - List all users
• <b>/admin_stats</b> - Show bot statistics
"""
    
    await update.message.reply_text(help_text, parse_mode="HTML")


    

async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"📝 ADD_WORD command from user {username} (ID: {user_id})")
    
    await update.message.reply_text("Please enter the word you want to add:")
    return WORD

async def receive_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    input_word = update.message.text
    
    logger.info(f"🔍 Processing word '{input_word}' for user {username} (ID: {user_id})")
    
    try:
        ai_response = groq_client.get_word_info(input_word)
        logger.info(f"🤖 AI response: {ai_response}")
        
        # Check if the word is not German
        if ai_response.strip().lower() == "not german":
            logger.warning(f"⚠️ Non-German word detected: '{input_word}' from user {username}")
            await update.message.reply_text(
                "🇩🇪 <b>Please enter a German word!</b>\n\n"
                f"The word/phrase <i>'{input_word}'</i> doesn't appear to be German. "
                "This bot is designed to help you learn German vocabulary.\n\n"
                "Please try again with a German word! 🔄",
                parse_mode="HTML"
            )
            return ConversationHandler.END 
        
        word, translation, cefr_level = ai_response.split(" - ")
        logger.info(f"✅ Word info received: {word} - {translation} - {cefr_level}")
    except ValueError as e:
        logger.error(f"❌ Error parsing AI response for '{input_word}': {e} | Response: {ai_response}")
        await update.message.reply_text(
            "❌ <b>Sorry, I couldn't process that word properly.</b>\n\n"
            "Please try again with a different German word.",
            parse_mode="HTML"
        )
        return WORD  # Keep the conversation active for retry
    except Exception as e:
        logger.error(f"❌ Error getting word info for '{input_word}': {e}")
        await update.message.reply_text(
            "❌ <b>Sorry, there was an error processing your word.</b>\n\n"
            "Please try again.",
            parse_mode="HTML"
        )
        return WORD  # Keep the conversation active for retry
    context.user_data['word'] = word
    context.user_data['translation'] = translation
    context.user_data['cefr_level'] = cefr_level

    # Only show glass-style buttons when asking for confirmation
    reply_keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="yes"),
            InlineKeyboardButton("No", callback_data="no")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)

    context.user_data['word_exists'] = False

    existing_word = db_manager.fetch_all('words', where_clause='word', where_args=[context.user_data['word']])
    if existing_word:
        db_word = existing_word[0]
        db_word_id = db_word[0]  # assuming columns: id, word, translation, cefr_level
        db_word_text = db_word[1]  # assuming columns: id, word, translation, cefr_level
        db_translation = db_word[2]
        db_cefr_level = db_word[3]

        context.user_data['word_exists'] = True
        context.user_data['word_id'] = db_word_id
        
        logger.info(f"🔍 Word '{word}' already exists in database (ID: {db_word_id})")

        await update.message.reply_text(
            f"⚠️ <b>The word</b> <i>'{db_word_text}'</i> <b>already exists in the database.</b>\n"
            f"💡 <b>Meaning:</b> <i>{db_translation}</i>\n"
            f"🎯 <b>Level:</b> <i>{db_cefr_level}</i>\n\n"
            f"Do you want to add it to your list of words?",
            reply_markup=markup,
            parse_mode="HTML"
        )
        return ConversationHandler.END

    logger.info(f"🆕 New word '{word}' will be added to database")
    
    await update.message.reply_text(
        f"✨ <b>Word:</b> <i>{word}</i>\n"
        f"💡 <b>Meaning:</b> <i>{translation}</i>\n"
        f"🎯 <b>Estimated Level:</b> <i>{cefr_level}</i>\n\n"
        f"Is this correct?",
        reply_markup=markup,
        parse_mode="HTML"
    )
    return ConversationHandler.END


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    username = update.effective_user.username
    callback_data = query.data
    
    logger.info(f"🔘 Button callback '{callback_data}' from user {username} (ID: {user_id})")
    
    # Handle admin broadcast callbacks
    if query.data in ["send_broadcast", "cancel_broadcast"]:
        return await admin_handle_broadcast_callback(update, context)
    
    # Handle review conversation callbacks
    if query.data == "continue_examples":
        logger.info(f"📚 User {username} continuing to examples")
        return await show_examples(update, context)
    elif query.data == "continue_paragraph":
        logger.info(f"📖 User {username} continuing to paragraph")
        return await show_paragraph(update, context)
    elif query.data == "complete_review":
        logger.info(f"✅ User {username} completing review")
        return await complete_review(update, context)
    
    # Only handle yes/no callbacks for word confirmation
    if query.data not in ["yes", "no"]:
        return
    
    if query.data == "no":
        logger.info(f"❌ User {username} declined word addition")
        await query.edit_message_text("Please start over by sending /add_word.", reply_markup=None)
        return
    
    # If user chose "yes", save the word
    word = context.user_data['word']
    translation = context.user_data['translation']
    cefr_level = context.user_data['cefr_level']
    
    logger.info(f"✅ User {username} confirmed word addition: '{word}'")
    
    if context.user_data['word_exists']:
        # Word exists in words table, get its ID
        word_id = context.user_data['word_id']
        logger.info(f"🔄 Using existing word ID: {word_id}")
    else:
        # Word doesn't exist, add it to words table
        db_manager.add_instance('words', columns=['word', 'translation','cefr_level'], new_vals=[word, translation, cefr_level])
        # Get the newly created word's ID
        word_id = db_manager.fetch_all('words', where_clause='word', where_args=[word])[0][0]
        logger.info(f"🆕 Created new word in database with ID: {word_id}")
    
    # Now check if user already has this word in their collection
    user_word_exists = db_manager.fetch_all('words_users', 
                                           where_clause='user_id', 
                                           where_args=[user_id])
    
    user_has_word = False

    for row in user_word_exists:
        # Adjust the index based on your actual table schema; typically, word_id is at index 1 if columns are (id, user_id, word_id)
        if len(row) > 2 and row[2] == word_id:
            user_has_word = True
            break

        
    if user_has_word:
        logger.warning(f"⚠️ User {username} already has word '{word}' in vocabulary")
        await query.edit_message_text(
            f"⚠️ <b>You already have the word</b> <i>'{word}'</i> <b>in your vocabulary!</b> ✨\n\nTry adding a new word or use /add_word again.",
            reply_markup=None,
            parse_mode="HTML"
        )
        return
    else:
        # Add word to user's collection
        db_manager.add_instance('words_users', columns=['user_id', 'word_id'], new_vals=[user_id, word_id])
        logger.info(f"🎉 Successfully added word '{word}' to user {username}'s vocabulary")
        await query.edit_message_text(
            f"🎉 Great! The word <b>'{word}'</b> with translation <b>'{translation}'</b> has been added to your vocabulary! 🚀\n\nKeep learning! 📚",
            reply_markup=None,
            parse_mode="HTML"
        )


async def review_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"📖 REVIEW_WORDS command from user {username} (ID: {user_id})")
    
    user_words = db_manager.fetch_all('words_users', where_clause='user_id', where_args=[user_id])
    logger.info(f"📊 User {username} has {len(user_words)} words in vocabulary")
    
    if len(user_words) < 5:
        logger.warning(f"⚠️ User {username} has insufficient words for review ({len(user_words)} < 5)")
        await update.message.reply_text(
            "🚦 <b>Not enough words!</b>\n\n"
            "You need at least <b>5 words</b> in your vocabulary to start a review session. "
            "Add more words using <b>/add_word</b> and come back soon! 💪📚",
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    words_df = db_manager.choose_words(user_id)
    words_df = words_df.sort_values(by='prob', ascending=False).head(5)
    
    logger.info(f"🎯 Selected 5 words for review for user {username}")
    
    words_info = []
    for _, row in words_df.iterrows():
        word_id = row['word_id'] if 'word_id' in row else row[0]
        word_data = db_manager.fetch_all('words', where_clause='id', where_args=[word_id])
        if word_data:
            word, translation, cefr_level = word_data[0][1], word_data[0][2], word_data[0][3]
            if any(info[0] == word for info in words_info):
                continue
            words_info.append((word, translation, cefr_level))

    # Store the words info in context for later use
    context.user_data['review_words_info'] = words_info
    context.user_data['word_list'] = [word for word, _, _ in words_info]
    
    selected_words = [word for word, _, _ in words_info]
    logger.info(f"📝 Review words for {username}: {selected_words}")

    reply_text = "📝 <b>Your review words:</b>\n\n"
    for idx, (word, translation, cefr_level) in enumerate(words_info, 1):
        reply_text += f"{idx}. <b>{word}</b> - <i>{translation}</i> (Level: {cefr_level})\n"
    
    # Add confirmation button
    reply_keyboard = [
        [InlineKeyboardButton("✅ Continue to Examples", callback_data="continue_examples")]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    
    await update.message.reply_text(
        reply_text + "\n\n📖 <b>Take your time to review these words. Click continue when you're ready to see example sentences!</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )
    return SHOW_EXAMPLES

async def show_examples(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word_list = context.user_data['word_list']
    
    examples = groq_client.write_example(word_list).split('\n')
    reply_text = "💡 <b>Example Sentences:</b>\n\n"
    
    display_idx = 1
    for example in examples:
        if example.strip():
            reply_text += f"<b>{display_idx}.</b> <i>{example.strip()}</i>\n\n"
            display_idx += 1
    
    # Add confirmation button
    reply_keyboard = [
        [InlineKeyboardButton("✅ Continue to Paragraph", callback_data="continue_paragraph")]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    
    await update.callback_query.edit_message_text(
        reply_text + "\n\n📚 <b>Study these examples carefully. Click continue when you're ready to see the paragraph!</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )
    return SHOW_PARAGRAPH

async def show_paragraph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word_list = context.user_data['word_list']
    
    paragraph = groq_client.write_paragraph(word_list).split('\n')
    reply_text = "📝 <b>Paragraph using your words:</b>\n\n"
    reply_text += f"<b>German: </b> <i>{paragraph[0].strip()}</i>\n\n"
    try:
        reply_text += f"<b>English: </b> <i>{paragraph[2].strip()}</i>\n\n"
    except IndexError:
        reply_text += f"<b>English: </b> <i>{paragraph[1].strip()}</i>\n\n"
    
    # Add completion button
    reply_keyboard = [
        [InlineKeyboardButton("🎉 Complete Review", callback_data="complete_review")]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    
    await update.callback_query.edit_message_text(
        reply_text + "\n\n🎯 <b>Great job! Read through this paragraph to see your words in context. Click complete when you're done!</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )
    return ConversationHandler.END

async def complete_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the user ID and the words that were reviewed
    user_id = update.effective_user.id
    word_list = context.user_data.get('word_list', [])
    
    # Update review count and last_reviewed for each word
    for word in word_list:
        # Get the word_id from the words table
        word_data = db_manager.fetch_all('words', where_clause='word', where_args=[word])
        if word_data:
            word_id = word_data[0][0]  # Get the word ID
            
            # Get current review data for this user-word combination
            current_data = db_manager.fetch_all('words_users', 
                                              columns='review_count', 
                                              where_clause='user_id = ? AND word_id = ?', 
                                              where_args=[user_id, word_id])
            
            if current_data:
                current_review_count = current_data[0][0]
                new_review_count = current_review_count + 1
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Update the record
                db_manager.edit_instance('words_users',
                                       columns=['review_count', 'last_reviewed'],
                                       new_vals=[new_review_count, current_time],
                                       where_clause='user_id = ? AND word_id = ?',
                                       where_args=[user_id, word_id])
    
    await update.callback_query.edit_message_text(
        "🎉 <b>Excellent work!</b> 🌟\n\n"
        "You've successfully completed your vocabulary review session! "
        "Keep practicing regularly to improve your language skills. 💪📚\n\n"
        "Use /review_words again anytime to practice more!",
        reply_markup=None,
        parse_mode="HTML"
    )
    return ConversationHandler.END

async def top_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top words by CEFR level based on total review count across all users"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"📊 TOP_WORDS command from user {username} (ID: {user_id})")
    
    top_words_by_level = db_manager.get_top_words_by_level(limit_per_level=5)
    
    if not top_words_by_level:
        logger.info("📭 No word statistics available yet")
        await update.message.reply_text(
            "📊 <b>No word statistics available yet!</b>\n\n"
            "Start adding and reviewing words to see the most popular vocabulary! 📚",
            parse_mode="HTML"
        )
        return
    
    logger.info(f"📈 Displaying top words statistics to user {username}")
    
    # Define level order and emojis
    level_order = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    level_emojis = {
        'A1': '🟢',
        'A2': '🔵', 
        'B1': '🟡',
        'B2': '🟠',
        'C1': '🔴',
        'C2': '🟣'
    }
    
    current_date = datetime.now().strftime("%B %d, %Y")
    reply_text = f"📊 <b>Top Words by CEFR Level - {current_date}</b>\n"
    reply_text += "<i>Most reviewed words across all users</i>\n\n"
    
    for level in level_order:
        if level in top_words_by_level:
            emoji = level_emojis.get(level, '⭐')
            reply_text += f"{emoji} <b>{level} Level:</b>\n"
            
            for idx, (word, translation, total_reviews) in enumerate(top_words_by_level[level], 1):
                reply_text += f"  {idx}. <b>{word}</b> - <i>{translation}</i> ({total_reviews} reviews)\n"
            
            reply_text += "\n"
    
    reply_text += "💡 <i>Keep practicing to contribute to these statistics!</i>"
    
    await update.message.reply_text(reply_text, parse_mode="HTML")

async def my_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's vocabulary list with option to remove words"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"📚 MY_WORDS command from user {username} (ID: {user_id})")
    
    user_words = db_manager.fetch_all('words_users', where_clause='user_id', where_args=[user_id])
    logger.info(f"📊 User {username} has {len(user_words)} words in vocabulary")
    
    if not user_words:
        logger.info(f"📭 User {username} has empty vocabulary")
        await update.message.reply_text(
            "📚 <b>Your vocabulary is empty!</b>\n\n"
            "Start adding words using <b>/add_word</b> to build your vocabulary! 💪📖",
            parse_mode="HTML"
        )
        return
    
    # Get word details for each word in user's collection
    words_info = []
    for user_word in user_words:
        word_id = user_word[2]  # Assuming columns: id, user_id, word_id, review_count, last_reviewed
        word_data = db_manager.fetch_all('words', where_clause='id', where_args=[word_id])
        if word_data:
            word_db_row = word_data[0]
            word_text = word_db_row[1]  # word
            translation = word_db_row[2]  # translation
            cefr_level = word_db_row[3]  # cefr_level
            review_count = user_word[3] if len(user_word) > 3 else 0  # review_count
            words_info.append((word_id, word_text, translation, cefr_level, review_count))
    
    # Sort by word alphabetically
    words_info.sort(key=lambda x: x[1].lower())
    
    reply_text = f"📚 <b>Your Vocabulary ({len(words_info)} words)</b>\n\n"
    
    # Group by CEFR level
    level_groups = {}
    for word_info in words_info:
        level = word_info[3]
        if level not in level_groups:
            level_groups[level] = []
        level_groups[level].append(word_info)
    
    # Define level order and emojis
    level_order = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    level_emojis = {
        'A1': '🟢',
        'A2': '🔵', 
        'B1': '🟡',
        'B2': '🟠',
        'C1': '🔴',
        'C2': '🟣'
    }
    
    for level in level_order:
        if level in level_groups:
            emoji = level_emojis.get(level, '⭐')
            reply_text += f"{emoji} <b>{level} Level:</b>\n"
            
            for word_info in level_groups[level]:
                word_id, word_text, translation, cefr_level, review_count = word_info
                reply_text += f"  • <b>{word_text}</b> - <i>{translation}</i> (reviewed {review_count} times)\n"
            
            reply_text += "\n"
    
    # Add management buttons
    reply_keyboard = [
        [InlineKeyboardButton("🗑️ Remove Words", callback_data="manage_vocab")]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    
    reply_text += "💡 <i>Click 'Remove Words' to manage your vocabulary list.</i>"
    
    await update.message.reply_text(reply_text, reply_markup=markup, parse_mode="HTML")

async def manage_vocabulary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show vocabulary management interface with remove options"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user_words = db_manager.fetch_all('words_users', where_clause='user_id', where_args=[user_id])
    
    if not user_words:
        await query.edit_message_text(
            "📚 <b>Your vocabulary is empty!</b>\n\n"
            "Start adding words using <b>/add_word</b> to build your vocabulary! 💪📖",
            reply_markup=None,
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    # Get word details for each word in user's collection
    words_info = []
    for user_word in user_words:
        word_id = user_word[2]  # Assuming columns: id, user_id, word_id, review_count, last_reviewed
        word_data = db_manager.fetch_all('words', where_clause='id', where_args=[word_id])
        if word_data:
            word_db_row = word_data[0]
            word_text = word_db_row[1]  # word
            translation = word_db_row[2]  # translation
            cefr_level = word_db_row[3]  # cefr_level
            words_info.append((word_id, word_text, translation, cefr_level))
    
    # Sort by word alphabetically
    words_info.sort(key=lambda x: x[1].lower())
    
    reply_text = f"🗑️ <b>Remove Words from Your Vocabulary</b>\n\n"
    reply_text += "<i>Click on a word to remove it from your vocabulary:</i>\n\n"
    
    # Create buttons for each word (max 20 to avoid hitting button limits)
    buttons = []
    for i, (word_id, word_text, translation, cefr_level) in enumerate(words_info[:20]):
        button_text = f"❌ {word_text} ({cefr_level})"
        callback_data = f"remove_word_{word_id}"
        buttons.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    # Add back button
    buttons.append([InlineKeyboardButton("⬅️ Back to My Words", callback_data="back_to_words")])
    
    if len(words_info) > 20:
        reply_text += f"\n<i>Showing first 20 words out of {len(words_info)} total words.</i>"
    
    markup = InlineKeyboardMarkup(buttons)
    
    await query.edit_message_text(reply_text, reply_markup=markup, parse_mode="HTML")
    return MANAGE_VOCAB

async def handle_word_removal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle word removal from user's vocabulary"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    if query.data == "back_to_words":
        logger.info(f"⬅️ User {username} navigating back to word list")
        # Call my_words function but adapt for callback query instead of message
        user_words = db_manager.fetch_all('words_users', where_clause='user_id', where_args=[user_id])
        
        if not user_words:
            await query.edit_message_text(
                "📚 <b>Your vocabulary is empty!</b>\n\n"
                "Start adding words using <b>/add_word</b> to build your vocabulary! 💪📖",
                reply_markup=None,
                parse_mode="HTML"
            )
            return ConversationHandler.END
        
        # Get word details for each word in user's collection
        words_info = []
        for user_word in user_words:
            word_id = user_word[2]
            word_data = db_manager.fetch_all('words', where_clause='id', where_args=[word_id])
            if word_data:
                word_db_row = word_data[0]
                word_text = word_db_row[1]
                translation = word_db_row[2]
                cefr_level = word_db_row[3]
                review_count = user_word[3] if len(user_word) > 3 else 0
                words_info.append((word_id, word_text, translation, cefr_level, review_count))
        
        words_info.sort(key=lambda x: x[1].lower())
        reply_text = f"📚 <b>Your Vocabulary ({len(words_info)} words)</b>\n\n"
        
        # Group by CEFR level
        level_groups = {}
        for word_info in words_info:
            level = word_info[3]
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(word_info)
        
        level_order = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        level_emojis = {
            'A1': '🟢', 'A2': '🔵', 'B1': '🟡',
            'B2': '🟠', 'C1': '🔴', 'C2': '🟣'
        }
        
        for level in level_order:
            if level in level_groups:
                emoji = level_emojis.get(level, '⭐')
                reply_text += f"{emoji} <b>{level} Level:</b>\n"
                for word_info in level_groups[level]:
                    word_id, word_text, translation, cefr_level, review_count = word_info
                    reply_text += f"  • <b>{word_text}</b> - <i>{translation}</i> (reviewed {review_count} times)\n"
                reply_text += "\n"
        
        reply_keyboard = [
            [InlineKeyboardButton("🗑️ Remove Words", callback_data="manage_vocab")]
        ]
        markup = InlineKeyboardMarkup(reply_keyboard)
        reply_text += "💡 <i>Click 'Remove Words' to manage your vocabulary list.</i>"
        
        await query.edit_message_text(reply_text, reply_markup=markup, parse_mode="HTML")
        return MANAGE_VOCAB
    
    if query.data.startswith("remove_word_"):
        word_id = int(query.data.replace("remove_word_", ""))
        
        logger.info(f"🗑️ User {username} attempting to remove word ID: {word_id}")
        
        # Get word details before removing
        word_data = db_manager.fetch_all('words', where_clause='id', where_args=[word_id])
        if word_data:
            word_text = word_data[0][1]
            
            # Remove word from user's collection using DatabaseManager methods
            # First, get the record ID from words_users table
            user_word_record = db_manager.fetch_all('words_users', 
                                                   where_clause='user_id = ? AND word_id = ?', 
                                                   where_args=[user_id, word_id])
            
            if user_word_record:
                record_id = user_word_record[0][0]  # Get the ID of the words_users record
                
                # Delete the record using the delete_instance method
                db_manager.delete_instance('words_users', where_clause='id = ?', where_args=[record_id])
                
                logger.info(f"✅ Successfully removed word '{word_text}' from user {username}'s vocabulary")
                
                await query.edit_message_text(
                    f"✅ <b>Word Removed Successfully!</b>\n\n"
                    f"The word <b>'{word_text}'</b> has been removed from your vocabulary.\n\n"
                    f"You can add it back anytime using <b>/add_word</b>.",
                    reply_markup=None,
                    parse_mode="HTML"
                )
            else:
                logger.warning(f"⚠️ Word ID {word_id} not found in user {username}'s vocabulary")
                await query.edit_message_text(
                    f"❌ <b>Error!</b>\n\n"
                    f"Could not find the word in your vocabulary. It may have already been removed.",
                    reply_markup=None,
                    parse_mode="HTML"
                )
            return ConversationHandler.END
    
    return ConversationHandler.END


# ADMIN COMMANDS
async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to list all users"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"👑 ADMIN_USERS command from user {username} (ID: {user_id})")
    
    # Check if user is admin
    if not is_admin(user_id):
        logger.warning(f"🚫 Unauthorized admin access attempt from user {username} (ID: {user_id})")
        await update.message.reply_text(
            "🚫 <b>Access Denied</b>\n\n"
            "You don't have permission to use admin commands.",
            parse_mode="HTML"
        )
        return
    
    # Get all users from database
    all_users = db_manager.fetch_all('users')
    
    if not all_users:
        await update.message.reply_text(
            "👑 <b>Admin - User List</b>\n\n"
            "📭 No users found in the database.",
            parse_mode="HTML"
        )
        return
    
    logger.info(f"👑 Admin {username} requested user list - {len(all_users)} users found")
    
    # Format user list
    reply_text = f"👑 <b>Admin - User List ({len(all_users)} users)</b>\n\n"
    
    for idx, user in enumerate(all_users, 1):
        user_db_id = user[0]  # Database ID
        telegram_id = user[1]  # Telegram ID
        db_username = user[2] if user[2] else "No username"  # Username
        created_at = user[3] if len(user) > 3 else "Unknown"  # Created timestamp
        
        # Get user's word count
        user_words = db_manager.fetch_all('words_users', where_clause='user_id', where_args=[telegram_id])
        word_count = len(user_words)
        
        reply_text += f"<b>{idx}.</b> @{db_username}\n"
        reply_text += f"   📱 Telegram ID: <code>{telegram_id}</code>\n"
        reply_text += f"   📚 Words: {word_count}\n"
        
        # Format the created_at date safely
        if created_at and created_at != 'Unknown':
            try:
                # Handle different timestamp formats
                if len(created_at) > 10:
                    join_date = created_at[:10]  # Take only the date part
                else:
                    join_date = created_at
            except (TypeError, IndexError):
                join_date = "Unknown"
        else:
            join_date = "Unknown"
            
        reply_text += f"   📅 Joined: {join_date}\n\n"
        
        # Split message if it gets too long (Telegram limit is 4096 characters)
        if len(reply_text) > 3500:
            await update.message.reply_text(reply_text, parse_mode="HTML")
            reply_text = f"👑 <b>Admin - User List (continued)</b>\n\n"
    
    if reply_text.strip() != f"👑 <b>Admin - User List (continued)</b>\n\n":
        await update.message.reply_text(reply_text, parse_mode="HTML")

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to show bot statistics"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"👑 ADMIN_STATS command from user {username} (ID: {user_id})")
    
    # Check if user is admin
    if not is_admin(user_id):
        logger.warning(f"🚫 Unauthorized admin access attempt from user {username} (ID: {user_id})")
        await update.message.reply_text(
            "🚫 <b>Access Denied</b>\n\n"
            "You don't have permission to use admin commands.",
            parse_mode="HTML"
        )
        return
    
    # Get statistics
    all_users = db_manager.fetch_all('users')
    all_words = db_manager.fetch_all('words')
    all_user_words = db_manager.fetch_all('words_users')
    
    # Calculate total reviews
    total_reviews = sum(row[3] if len(row) > 3 and row[3] else 0 for row in all_user_words)
    
    # Get active users (users with at least 1 word)
    active_users = set()
    for user_word in all_user_words:
        active_users.add(user_word[1])  # user_id
    
    logger.info(f"👑 Admin {username} requested bot statistics")
    
    reply_text = f"👑 <b>Admin - Bot Statistics</b>\n\n"
    reply_text += f"👥 <b>Total Users:</b> {len(all_users)}\n"
    reply_text += f"🟢 <b>Active Users:</b> {len(active_users)}\n"
    reply_text += f"📚 <b>Total Words in Database:</b> {len(all_words)}\n"
    reply_text += f"🔗 <b>Total User-Word Connections:</b> {len(all_user_words)}\n"
    reply_text += f"📖 <b>Total Reviews Completed:</b> {total_reviews}\n\n"
    
    # Average words per active user
    if len(active_users) > 0:
        avg_words = len(all_user_words) / len(active_users)
        reply_text += f"📊 <b>Average Words per Active User:</b> {avg_words:.1f}\n"
    
    # Average reviews per word connection
    if len(all_user_words) > 0:
        avg_reviews = total_reviews / len(all_user_words)
        reply_text += f"📈 <b>Average Reviews per Word:</b> {avg_reviews:.1f}\n"
    
    reply_text += f"\n⏰ <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    await update.message.reply_text(reply_text, parse_mode="HTML")

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to show available admin commands"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"👑 ADMIN_HELP command from user {username} (ID: {user_id})")
    
    # Check if user is admin
    if not is_admin(user_id):
        logger.warning(f"🚫 Unauthorized admin access attempt from user {username} (ID: {user_id})")
        await update.message.reply_text(
            "🚫 <b>Access Denied</b>\n\n"
            "You don't have permission to use admin commands.",
            parse_mode="HTML"
        )
        return
    
    help_text = """
👑 <b>Admin Commands - Vocab Buddy</b>

Welcome to the admin panel! Here are the available admin commands:

📋 <b>USER MANAGEMENT:</b>
• <b>/admin_users</b> - List all registered users with statistics
• <b>/admin_stats</b> - Show comprehensive bot statistics

📢 <b>COMMUNICATION:</b>
• <b>/admin_broadcast</b> - Send announcement to all users

❓ <b>HELP:</b>
• <b>/admin_help</b> - Show this admin help message

📊 <b>STATISTICS AVAILABLE:</b>
• Total and active user counts
• Word database size
• Review completion statistics
• User engagement metrics

🔒 <b>SECURITY:</b>
All admin commands are logged and require proper authorization.
Only the configured admin can access these features.

💡 <b>TIPS:</b>
• Use /admin_stats for quick overview
• Use /admin_users for detailed user information
• All commands provide comprehensive logging

<i>More admin features will be added in future updates!</i>
"""
    
    await update.message.reply_text(help_text, parse_mode="HTML")

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to start broadcasting a message to all users"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    logger.info(f"👑 ADMIN_BROADCAST command from user {username} (ID: {user_id})")
    
    # Check if user is admin
    if not is_admin(user_id):
        logger.warning(f"🚫 Unauthorized admin access attempt from user {username} (ID: {user_id})")
        await update.message.reply_text(
            "🚫 <b>Access Denied</b>\n\n"
            "You don't have permission to use admin commands.",
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        "📢 <b>Admin Broadcast Message</b>\n\n"
        "Please type the message you want to send to all users.\n\n"
        "💡 <b>Tips:</b>\n"
        "• Use HTML formatting if needed (<b>bold</b>, <i>italic</i>)\n"
        "• Keep it concise and informative\n"
        "• Type /cancel to abort\n\n"
        "✍️ <i>Enter your message:</i>",
        parse_mode="HTML"
    )
    return ADMIN_MESSAGE

async def admin_receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and confirm admin broadcast message"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text
    
    logger.info(f"👑 Admin {username} composed broadcast message")
    
    # Store the message in context
    context.user_data['broadcast_message'] = message_text
    
    # Show preview with confirmation buttons
    reply_keyboard = [
        [
            InlineKeyboardButton("✅ Send to All Users", callback_data="send_broadcast"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_broadcast")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    
    preview_text = f"📢 <b>Broadcast Message Preview</b>\n\n"
    preview_text += f"📝 <b>Message:</b>\n{message_text}\n\n"
    preview_text += "🔍 <b>This message will be sent to ALL users.</b>\n"
    preview_text += "Are you sure you want to proceed?"
    
    await update.message.reply_text(
        preview_text,
        reply_markup=markup,
        parse_mode="HTML"
    )
    return ConversationHandler.END

async def admin_handle_broadcast_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle broadcast confirmation callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    if query.data == "cancel_broadcast":
        logger.info(f"👑 Admin {username} cancelled broadcast")
        await query.edit_message_text(
            "❌ <b>Broadcast Cancelled</b>\n\n"
            "The message was not sent to users.",
            reply_markup=None,
            parse_mode="HTML"
        )
        return
    
    elif query.data == "send_broadcast":
        broadcast_message = context.user_data.get('broadcast_message')
        if not broadcast_message:
            await query.edit_message_text(
                "❌ <b>Error</b>\n\n"
                "No message found. Please try again.",
                reply_markup=None,
                parse_mode="HTML"
            )
            return
        
        logger.info(f"👑 Admin {username} confirmed broadcast - starting delivery")
        
        # Update the message to show broadcasting status
        await query.edit_message_text(
            "📡 <b>Broadcasting Message...</b>\n\n"
            "Please wait while the message is being sent to all users.",
            reply_markup=None,
            parse_mode="HTML"
        )
        
        # Get all users
        all_users = db_manager.fetch_all('users')
        
        if not all_users:
            await query.edit_message_text(
                "📭 <b>No Users Found</b>\n\n"
                "There are no users in the database to send the message to.",
                reply_markup=None,
                parse_mode="HTML"
            )
            return
        
        # Send message to all users
        success_count = 0
        failed_count = 0
        
        # Format the broadcast message with admin header
        formatted_message = f"📢 <b>Announcement from Vocab Buddy</b>\n\n{broadcast_message}\n\n<i>— Admin Team</i>"
        
        for user in all_users:
            telegram_id = user[1]  # Telegram ID
            db_username = user[2] if user[2] else "Unknown"
            
            try:
                # Send message to user
                await context.bot.send_message(
                    chat_id=telegram_id,
                    text=formatted_message,
                    parse_mode="HTML"
                )
                success_count += 1
                logger.info(f"📤 Broadcast delivered to user {db_username} (ID: {telegram_id})")
                
            except Exception as e:
                failed_count += 1
                logger.warning(f"📤 Failed to deliver broadcast to user {db_username} (ID: {telegram_id}): {e}")
        
        # Report results
        total_users = len(all_users)
        logger.info(f"👑 Broadcast completed: {success_count}/{total_users} delivered, {failed_count} failed")
        
        result_text = f"✅ <b>Broadcast Complete!</b>\n\n"
        result_text += f"📊 <b>Delivery Report:</b>\n"
        result_text += f"👥 Total Users: {total_users}\n"
        result_text += f"✅ Successfully Delivered: {success_count}\n"
        result_text += f"❌ Failed Deliveries: {failed_count}\n\n"
        
        if failed_count > 0:
            result_text += f"<i>Failed deliveries may be due to users blocking the bot or deactivated accounts.</i>\n\n"
        
        result_text += f"📝 <b>Message Sent:</b>\n{broadcast_message}"
        
        await query.edit_message_text(
            result_text,
            reply_markup=None,
            parse_mode="HTML"
        )


def main():
    logger.info("🔧 Initializing Telegram Bot Application...")
    
    # Create application
    app = ApplicationBuilder().token(TOKEN).build()
    
    logger.info("🎯 Setting up command handlers...")
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("top_words", top_words))
    app.add_handler(CommandHandler("my_words", my_words))
    
    # Add admin command handlers
    if ADMIN_ID:
        app.add_handler(CommandHandler("admin_users", admin_users))
        app.add_handler(CommandHandler("admin_stats", admin_stats))
        app.add_handler(CommandHandler("admin_help", admin_help))
        
        # Admin broadcast conversation handler
        admin_broadcast_conv = ConversationHandler(
            entry_points=[CommandHandler("admin_broadcast", admin_broadcast)],
            states={
                ADMIN_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_receive_message)],
            },
            fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)],
        )
        app.add_handler(admin_broadcast_conv)
        
        logger.info("👑 Admin command handlers registered")
    
    logger.info("🔄 Setting up conversation handlers...")
    
    # Add conversation handlers first (more specific)
    add_word_conv = ConversationHandler(
        entry_points=[CommandHandler("add_word", add_word)],
        states={
            WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_word)],
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)],
    )

    review_conv = ConversationHandler(
        entry_points=[CommandHandler("review_words", review_words)],
        states={
            SHOW_EXAMPLES: [CallbackQueryHandler(button_callback, pattern="^continue_examples$")],
            SHOW_PARAGRAPH: [CallbackQueryHandler(button_callback, pattern="^continue_paragraph$")],
        },
        fallbacks=[],
        per_message=False,
    )

    vocab_manage_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(manage_vocabulary, pattern="^manage_vocab$")],
        states={
            MANAGE_VOCAB: [
                CallbackQueryHandler(handle_word_removal, pattern="^(remove_word_|back_to_words)"),
            ],
        },
        fallbacks=[],
        per_message=False,
    )

    app.add_handler(add_word_conv)
    app.add_handler(review_conv)
    app.add_handler(vocab_manage_conv)
    
    # Add general callback handler last (less specific)
    app.add_handler(CallbackQueryHandler(button_callback))

    logger.info("✅ All handlers registered successfully")
    logger.info("🚀 Starting bot polling...")
    
    try:
        app.run_polling()
    except Exception as e:
        logger.error(f"❌ Critical error in bot execution: {e}")
        raise

if __name__ == "__main__":
    logger.info("🌟 Vocab Buddy Bot Application Starting...")
    main()