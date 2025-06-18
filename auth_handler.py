from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# ইন-মেমোরি ডাটাবেস
user_db = {}

ASK_NAME = 1

# সাইনআপ শুরু
async def auth_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("📝 দয়া করে আপনার নাম লিখুন:")
    return ASK_NAME

# নাম সংরক্ষণ
async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.message.text
    username = update.effective_user.username or "NoUsername"

    user_db[user_id] = {
        "name": name,
        "username": username
    }

    await update.message.reply_text(
        f"✅ ধন্যবাদ {name}!\nআপনার একাউন্টটি সফলভাবে তৈরি হয়েছে!"
    )

    return ConversationHandler.END  # ✅ conversation properly ends
