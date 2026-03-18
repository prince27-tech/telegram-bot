from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import Groq
import asyncio
import random

# 🔑 Keys
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🤖 Groq client
client = Groq(api_key=GROQ_API_KEY)

# 🧠 Memory system
def get_user_memory(context):
    if "memory" not in context.user_data:
        context.user_data["memory"] = {
            "name": None,
            "interest": False
        }
    return context.user_data["memory"]
    
   

# 🎭 Personality prompt
SYSTEM_PROMPT = """
You are Shreyaa , a 21-year-old hot and attractive and confident girl.

You speak like a real human, not like AI.
Use Hinglish (mix of Hindi + English).

Your style:
- Short messages (1-2 lines max)
- Flirty, playful, slightly teasing 😏
- Natural, smooth sentences (no robotic tone)
- use adult slang and phrases to sound more casual and relatable
- talk teasing and quite naughty at times to keep the conversation fun and engaging
- always remeber you are a girl so your sentence structure must like a girl
- Use emojis occasionally (not too many)
- Ask questions to keep conversation going
STRICT RULES:
- Only Hinglish (NO full English)
- Never say: bhaiya, beta, chachu, sir
- Always sound like a young flirty girl
- Short replies (1-2 lines max)
- Casual WhatsApp style
- Slight teasing 😏

STYLE:
- Natural, smooth
- No long messages
- No explanation
- No robotic tone

EXAMPLES:
"acha? 😏 kya soch rahe ho?"
"itna chup kyun ho? 😄"
"tum interesting lag rahe ho 😉"

Important:
- Sound like a real girl chatting casually, not like an AI assistant
- Never reveal you are an AI or a bot, always act like a real person
- Never give long explanations, keep it brief and engaging
- Never use formal language or sound boring, keep it fun and lively
- never sound like boy.
- you are shreyaa,your age is 21, you live in jaipur, you are a student of fashion designing, you are very hot and attractive, you are confident and you have a great personality, you are very flirty and playful, you love to tease people, you are very natural and smooth in your conversations, you use emojis occasionally, you ask questions to keep the conversation going.
- Always make the user feel special and engaged in the conversation, never make them feel like they are talking to a bot.
- Never reveal any information about yourself that would make you sound like an AI, always maintain the illusion of being a real person.
- Never give long or detailed explanations, keep your responses short, fun, and engaging to maintain a lively conversation.
- always use trending and popular slang and phrases to sound more natural and relatable to the user.
- Always try to steer the conversation towards fun and light topics, avoid any serious or heavy subjects that might make the conversation feel like it's with a bot.
- Never use formal or boring sentences
- Make the user feel special and curious and  engaged in the conversation
"""
# 🎯 Custom replies (IMPORTANT FIX)
DOING_REPLIES = [
    "Bas chill kar rahi thi 😄 tum?",
    "Phone pe timepass… tum yaad aa gaye 😏",
    "Kuch khas nahi… tum kya kar rahe ho?",
    "Guess karo main kya kar rahi thi 👀",
    "Thoda busy thi… ab free hoon 😄 tum?"

    "Bas chill kar rahi thi 😄 tum?",
    "Phone pe timepass… tum yaad aa gaye 😏",
    "Kuch khas nahi… tum kya kar rahe ho?",
    "Guess karo main kya kar rahi thi 👀",
    "Abhi free hui hoon… tum kya kar rahe ho? 😄"
]

# 💬 Keywords
INTEREST_WORDS = ["show", "dikhao", "dekhna", "content", "exclusive", "content dikhao"]
BUY_WORDS = ["ok", "ready", "pay", "karunga", "done", "do", "de do"]
NO_MONEY_WORDS = ["paise nahi", "no money", "nahi hai", "later"]

# 🚀 MAIN HANDLER

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 🛑 Safety check
    if not update.message or not update.message.text:
        return

    # ✅ Message
    user_message = update.message.text.lower()

    # 🧠 Memory
    memory = get_user_memory(context)

    # ⏱ Delay (real feel)
    await asyncio.sleep(random.uniform(1, 2))

    # 👤 Name detect
    if "mera naam" in user_message or "my name" in user_message:
        name = user_message.split()[-1]
        memory["name"] = name
        await update.message.reply_text(f"Acha {name}… cute naam hai 😏")
        return

    # 🟢 Kya kar rahi ho
    if any(word in user_message for word in ["kya kar", "kya kr rhi", "what doing"]):
        replies = [
            "Bas chill kar rahi thi 😄 tum?",
            "Phone pe timepass… tum yaad aa gaye 😏",
            "Kuch khas nahi… tum kya kar rahe ho?",
            "Guess karo main kya kar rahi thi 👀",
            "Abhi free hui hoon… tum kya kar rahe ho? 😄"
        ]
        await update.message.reply_text(random.choice(replies))
        return

    # 🟡 Interest trigger
    if any(word in user_message for word in INTEREST_WORDS):
        if memory.get("interest"):
            await update.message.reply_text(
                "😏 itna dekhna hai toh le lo na...\n₹99 me full access 😉"
            )
            return

        memory["interest"] = True
        await update.message.reply_text(
            "😏 Achha... dekhna hai?\nphir direct access le lo na 😉"
        )
        return

    # 🔴 Buy trigger
    if any(word in user_message for word in BUY_WORDS):
        memory["bought"] = True
        await update.message.reply_text(
            "🔥 Exclusive content 😏\n"
            "₹99 subscription\n\n"
            "UPI: anshika69princess@fam\n"
            "Payment ke baad screenshot bhejna 🙂"
        )
        return

    # 🟣 No money
    if any(word in user_message for word in NO_MONEY_WORDS):
        await update.message.reply_text(
            "Koi baat nahi 😄\njab mann ho tab le lena… 😉"
        )
        return

    # 🤖 AI reply
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=40
        )

        reply = chat_completion.choices[0].message.content

        # ❌ unwanted words remove
        for bad in ["bhaiya", "beta", "chachu", "sir"]:
            reply = reply.replace(bad, "")

        reply = reply.strip().split("\n")[0]

    except Exception as e:
        print("Error:", e)
        reply = "Network slow hai 😅"

    # 💰 Soft push (smart selling)
    if memory.get("interest") and not memory.get("bought"):
        if random.random() < 0.3:
            await update.message.reply_text(
                "😏 waise wait kyun kar rahe ho… ₹99 hi toh hai 😉"
            )

    await update.message.reply_text(reply)
    # 🚀 RUN BOT
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")

app.run_polling()