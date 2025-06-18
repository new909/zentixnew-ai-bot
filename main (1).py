import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Load environment variables
from auth_handler import auth_handler, save_name, ASK_NAME
from telegram.ext import ConversationHandler
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # 🛡️ এখানে টোকেন ENV থেকে আসবে

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📦 মেনু"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "🌟 স্বাগতম *Zentix Ai Bot* -এ!\n\n"
        "🤖 আমি আপনার ব্যক্তিগত AI সহকারী।\n\n"
        "📦 মেনু দেখতে নিচের '📦 মেনু' বাটনে ক্লিক করুন —\n"
        "নতুন প্রযুক্তির সাথে যুক্ত হোন এক ক্লিকে।",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Menu Command
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_page(update, context, 1)

# Menu Pagination
async def send_page(update, context, page):
    if update.callback_query:
        chat_id = update.callback_query.message.chat.id
        await update.callback_query.answer()
    else:
        chat_id = update.message.chat.id

    if page == 1:
        keyboard = [
            [InlineKeyboardButton("🔑 সাইনআপ / সাইনইন", callback_data="auth")],
            [InlineKeyboardButton("🎬 ভিডিও এডিট", callback_data="video_edit")],
            [InlineKeyboardButton("🖼️ ফটো এডিট", callback_data="photo_edit")],
            [InlineKeyboardButton("📼 CapCut/Remini Pro", callback_data="capcut")],
            [InlineKeyboardButton("🛠️ ওয়েব/সফটওয়্যার অর্ডার", callback_data="web_order")],
            [InlineKeyboardButton("➡️ পরের পেজ", callback_data="page_2")]
        ]
    elif page == 2:
        keyboard = [
            [InlineKeyboardButton("📱 SMM সার্ভিস", callback_data="smm")],
            [InlineKeyboardButton("🤖 ওয়াজিফা AI", callback_data="wazifa_ai")],
            [InlineKeyboardButton("🧠 Nur AI", callback_data="nur_ai")],
            [InlineKeyboardButton("📞 কাস্টমার কেয়ার", callback_data="customer_care")],
            [InlineKeyboardButton("⬅️ পেছনের পেজ", callback_data="page_1"), InlineKeyboardButton("➡️ পেজ ৩", callback_data="page_3")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("📲 টেলিকম প্যাক", callback_data="telecom")],
            [InlineKeyboardButton("🔥 গেম টপআপ", callback_data="topup")],
            [InlineKeyboardButton("💳 ব্যালেন্স", callback_data="balance")],
            [InlineKeyboardButton("⬅️ পেছনের পেজ", callback_data="page_2")]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text="📦 নিচে থেকে আপনার প্রয়োজনীয় সার্ভিস বেছে নিন:",
        reply_markup=reply_markup
    )

# Callback handler
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data.startswith("page_"):
        page_num = int(data.split("_")[1])
        await send_page(update, context, page_num)
    elif data == "auth":
        await auth_handler(update, context)
    else:
        await update.callback_query.answer("🚧 ফিচারটি এখনো তৈরি হচ্ছে!")

# Run Bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(handle_callback))

# ✅ যেকোনো 'মেনু' লিখলেই বাটন আসবে
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"মেনু"), menu))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"(মেনু|📦 মেনু)"), menu))
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(auth_handler, pattern="^auth$")],
    states={ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)]},
    fallbacks=[],
)
app.add_handler(conv_handler)
