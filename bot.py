from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from typing import Final
from database import DatabaseManager
from telegram.ext import ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from agent import GroqClient


# Load the bot token from the config file
with open("config.json", "r") as f:
    config = json.load(f)
TOKEN: Final = config["BOT_TOKEN"]


# Start database manager and agent client
groq_client = GroqClient()
db_manager = DatabaseManager()


# Define conversation states
WORD, MEANING = range(2)
SHOW_WORDS, SHOW_EXAMPLES, SHOW_PARAGRAPH = range(3, 6)









async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    username = update.effective_user.username
    user_exists = db_manager.fetch_all('users', where_clause='telegram_id', where_args=[user_id])
    if not user_exists:
        db_manager.add_instance('users', columns=['telegram_id', 'username'], new_vals=[user_id, username])
        text = f"Hello @{username}! \nWelcome to Vocab Buddy! You have been registered."
    else:
        text = f"Hello @{username}! \nWelcome back to Vocab Buddy!"

    await update.message.reply_text(text)


    

async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the word you want to add:")
    return WORD

async def receive_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, translation, cefr_level = groq_client.get_word_info(update.message.text).split(" - ")
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

        await update.message.reply_text(
            f"⚠️ <b>The word</b> <i>'{db_word_text}'</i> <b>already exists in the database.</b>\n"
            f"💡 <b>Meaning:</b> <i>{db_translation}</i>\n"
            f"🎯 <b>Level:</b> <i>{db_cefr_level}</i>\n\n"
            f"Do you want to add it to your list of words?",
            reply_markup=markup,
            parse_mode="HTML"
        )
        return ConversationHandler.END

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
    
    # Handle review conversation callbacks
    if query.data == "continue_examples":
        return await show_examples(update, context)
    elif query.data == "continue_paragraph":
        return await show_paragraph(update, context)
    elif query.data == "complete_review":
        return await complete_review(update, context)
    
    # Only handle yes/no callbacks for word confirmation
    if query.data not in ["yes", "no"]:
        return
    
    if query.data == "no":
        await query.edit_message_text("Please start over by sending /add_word.", reply_markup=None)
        return
    
    # If user chose "yes", save the word
    word = context.user_data['word']
    translation = context.user_data['translation']
    cefr_level = context.user_data['cefr_level']
    user_id = update.effective_user.id
    
    if context.user_data['word_exists']:
        # Word exists in words table, get its ID
        word_id = context.user_data['word_id']
    else:
        # Word doesn't exist, add it to words table
        db_manager.add_instance('words', columns=['word', 'translation','cefr_level'], new_vals=[word, translation, cefr_level])
        # Get the newly created word's ID
        word_id = db_manager.fetch_all('words', where_clause='word', where_args=[word])[0][0]
    
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
        await query.edit_message_text(
            f"⚠️ <b>You already have the word</b> <i>'{word}'</i> <b>in your vocabulary!</b> ✨\n\nTry adding a new word or use /add_word again.",
            reply_markup=None,
            parse_mode="HTML"
        )
        return
    else:
        # Add word to user's collection
        db_manager.add_instance('words_users', columns=['user_id', 'word_id'], new_vals=[user_id, word_id])
        await query.edit_message_text(
            f"🎉 Great! The word <b>'{word}'</b> with translation <b>'{translation}'</b> has been added to your vocabulary! 🚀\n\nKeep learning! 📚",
            reply_markup=None,
            parse_mode="HTML"
        )


async def review_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_words = db_manager.fetch_all('words_users', where_clause='user_id', where_args=[user_id])
    if len(user_words) < 5:
        await update.message.reply_text(
            "🚦 <b>Not enough words!</b>\n\n"
            "You need at least <b>5 words</b> in your vocabulary to start a review session. "
            "Add more words using <b>/add_word</b> and come back soon! 💪📚",
            parse_mode="HTML"
        )
        return ConversationHandler.END
    
    words_df = db_manager.choose_words(user_id)
    words_df = words_df.sort_values(by='prob', ascending=False).head(5)
    
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
    reply_text += f"<b>English: </b> <i>{paragraph[2].strip()}</i>\n\n"
    
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
    await update.callback_query.edit_message_text(
        "🎉 <b>Excellent work!</b> 🌟\n\n"
        "You've successfully completed your vocabulary review session! "
        "Keep practicing regularly to improve your language skills. 💪📚\n\n"
        "Use /review_words again anytime to practice more!",
        reply_markup=None,
        parse_mode="HTML"
    )
    return ConversationHandler.END







def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Add conversation handlers first (more specific)
    add_word_conv = ConversationHandler(
        entry_points=[CommandHandler("add_word", add_word)],
        states={
            WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_word)],
        },
        fallbacks=[],
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

    app.add_handler(add_word_conv)
    app.add_handler(review_conv)
    
    # Add general callback handler last (less specific)
    app.add_handler(CallbackQueryHandler(button_callback))





    app.run_polling()

if __name__ == "__main__":
    main()