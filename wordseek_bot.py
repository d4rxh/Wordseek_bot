"""
╔══════════════════════════════════════════════════╗
║           🔤 WORDSEEKBOT - COMPLETE              ║
║     Daily Wordle-style Telegram Game Bot         ║
╚══════════════════════════════════════════════════╝
Features:
  ✅ Daily Word Challenge
  ✅ Multiplayer Group Mode
  ✅ Hints System
  ✅ Score & Leaderboard
  ✅ Streak System
  ✅ Timer (120 second rounds)
  ✅ Aesthetic /start interface
  ✅ Private + Group support
"""

import logging
import json
import os
import random
import asyncio
from datetime import datetime, date, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# ─────────────────────────────────────────────────
# 📦 IMPORT CONFIGURATION
# ─────────────────────────────────────────────────
import config

# Configuration variables (imported from config.py)
BOT_TOKEN = config.BOT_TOKEN
GAME_TIMEOUT = config.GAME_TIMEOUT
MAX_ATTEMPTS = config.MAX_ATTEMPTS
DATA_FILE = config.DATA_FILE
START_IMAGE_URL = config.START_IMAGE_URL

# Emojis
EMOJI_CORRECT = config.EMOJI_CORRECT
EMOJI_WRONG_POS = config.EMOJI_WRONG_POS
EMOJI_NOT_IN_WORD = config.EMOJI_NOT_IN_WORD
EMOJI_EMPTY = config.EMOJI_EMPTY

# Scoring
SCORE_MAP = config.SCORE_MAP
DAILY_BONUS = config.DAILY_BONUS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, config.LOG_LEVEL)
)

# ─────────────────────────────────────────────────
# 📚 WORD LIST (500+ common 5-letter words)
# ─────────────────────────────────────────────────
WORDS = [
    "about","above","abuse","actor","acute","admit","adopt","adult","after","again",
    "agent","agree","ahead","alarm","album","alert","alike","alive","allow","alone",
    "along","angel","anger","angle","angry","ankle","apart","apple","apply","apron",
    "arena","armor","aroma","arose","array","arrow","arson","aside","atlas","atone",
    "audio","audit","avail","avoid","awake","award","aware","awful","bacon","badge",
    "badly","bagel","banal","banjo","basic","basil","basis","batch","beach","beard",
    "beast","began","begin","being","belly","below","bench","berry","bible","birth",
    "bison","black","blade","blame","bland","blank","blast","blaze","bleak","blend",
    "bless","blind","bliss","block","blood","bloom","board","boast","bonus","bound",
    "boxer","brace","braid","brain","brand","brave","bread","break","breed","brick",
    "bride","brief","brine","bring","brisk","brook","broth","brown","brush","built",
    "bulge","bully","bunch","burst","buyer","camel","cameo","canal","candy","canny",
    "cargo","carry","carve","catch","cause","cease","chain","chair","chalk","chaos",
    "charm","chart","chase","cheap","cheat","cheek","chess","chest","chief","child",
    "chili","chill","choir","chord","civil","claim","clamp","clash","clasp","class",
    "clean","clear","clerk","click","cliff","climb","cling","cloak","clock","clone",
    "close","cloth","cloud","clown","coast","cobra","comet","comic","coral","could",
    "count","court","cover","craft","crash","crawl","crazy","cream","creek","creep",
    "crest","crime","crisp","cross","crowd","crown","cruel","crush","crust","cubic",
    "curve","cycle","daily","dairy","daisy","dance","datum","dealt","debut","decay",
    "denim","depot","depth","digit","disco","ditch","diver","dizzy","dodge","doubt",
    "dough","draft","drain","drama","drape","drawl","dread","dream","dress","dried",
    "drift","drink","drive","drone","drove","drown","drums","dryer","dwarf","dwell",
    "dying","eagle","early","earth","eight","elite","empty","enjoy","enter","entry",
    "equal","error","essay","ethic","event","every","exact","exist","extra","fable",
    "faith","false","fancy","fatal","fault","feast","fence","feral","ferry","fetch",
    "fever","fiber","field","fifth","fifty","fight","final","first","fixed","flame",
    "flare","flash","flask","fleet","flesh","flock","flood","floor","flour","fluid",
    "flute","focus","force","forge","forth","forum","found","frame","frank","fraud",
    "fresh","front","frost","fruit","fungi","funny","fuzzy","ghost","girth","given",
    "gland","glare","glass","glide","gloom","gloss","glove","grace","grade","grain",
    "grand","grant","graph","grasp","grass","grave","great","greed","green","grief",
    "grind","groan","groom","gross","group","grove","grown","guard","guide","guild",
    "gusto","habit","happy","harsh","haste","haven","heart","heavy","hence","herbs",
    "hippo","hoist","holly","honey","honor","horse","hotel","hound","house","human",
    "humor","hurry","ideal","image","inner","input","inter","intro","irate","irony",
    "issue","ivory","jelly","jewel","judge","juice","juicy","jumbo","kayak","khaki",
    "knack","kneel","knife","knock","knoll","known","label","lance","laser","latch",
    "later","lathe","latte","layer","learn","lease","least","ledge","legal","lemon",
    "level","light","linen","liner","liver","lodge","logic","loose","lotus","lover",
    "lower","loyal","lucky","lunar","lyric","magic","major","maker","manor","maple",
    "march","marry","match","mayor","media","mercy","merit","metal","meter","might",
    "minor","minus","mirth","model","money","month","moral","motor","motto","mourn",
    "mouth","movie","music","musty","naive","nasty","naval","nerve","night","noble",
    "noise","notch","noted","novel","nurse","occur","ocean","offer","often","olive",
    "onset","opera","orbit","order","otter","outer","oxide","ozone","paint","panel",
    "panic","paper","party","pasta","patch","pause","peace","pearl","pedal","penny",
    "perch","peril","phase","phone","photo","piano","pilot","pinch","pixel","pizza",
    "place","plain","plane","plant","plate","plaza","plead","pluck","plumb","plume",
    "point","polar","power","press","price","pride","prime","print","prior","prize",
    "probe","prone","proof","prose","proud","prove","pulse","punch","purse","queen",
    "query","quest","quick","quiet","quota","quote","radar","radio","rainy","rally",
    "ranch","range","rapid","raven","reach","ready","realm","rebel","reign","relax",
    "relay","reply","resin","revel","rider","ridge","rifle","right","rigid","risky",
    "rival","river","robot","rocky","rough","round","route","royal","rugby","ruler",
    "rumor","rusty","saint","salad","sandy","sauce","savvy","scale","scare","scarf",
    "scene","scent","scope","score","scout","seize","sense","serum","serve","setup",
    "seven","shade","shaft","shake","shame","shape","share","shark","sharp","shear",
    "sheen","sheet","shelf","shell","shift","shine","shirt","shock","shore","short",
    "shout","shove","shown","siege","sight","sigma","silly","since","sixth","sixty",
    "skill","skull","slant","slash","sleep","slice","slide","slope","sloth","small",
    "smart","smash","smile","smirk","smoke","snake","snare","sneak","snore","solar",
    "solid","solve","sorry","south","space","spare","spark","spawn","speak","speed",
    "spell","spend","spice","spill","spine","spite","split","spoke","spoon","sport",
    "spray","squad","squat","squid","stack","staff","stain","stair","stake","stale",
    "stamp","stand","stark","start","state","steam","steel","steep","steer","stern",
    "stick","stiff","still","sting","stock","stomp","stone","store","storm","story",
    "stout","stove","strap","straw","stray","strip","study","stump","style","sugar",
    "suite","sunny","super","surge","swamp","swarm","swear","sweat","sweep","sweet",
    "swift","swipe","swirl","sword","syrup","table","talon","tango","taste","taunt",
    "teach","tease","tempo","tense","tenth","tepid","thorn","three","throw","tiger",
    "tight","timer","tired","title","today","token","torso","total","touch","tough",
    "towel","tower","toxic","trace","track","trade","trail","train","trait","trash",
    "tread","treat","trend","trial","tribe","trick","tried","troop","trove","truce",
    "truck","truly","trunk","trust","truth","tulip","tumor","tweak","twice","twist",
    "ulcer","ultra","unify","union","unite","unity","until","upper","upset","urban",
    "usage","utter","valve","vapor","vault","verse","video","vigor","viral","virus",
    "vista","vital","vivid","vocal","vodka","voice","voter","vowel","wager","waltz",
    "watch","water","weary","weave","wedge","weird","whale","wheat","wheel","witch",
    "woman","world","worse","worst","worth","would","wound","wrath","write","wrote",
    "yacht","yearn","yield","young","youth","zebra","zesty",
]

WORD_LIST = list(set([w.lower() for w in WORDS if len(w) == 5]))

# Hints for common words
HINTS = {
    "about": ["Means approximately", "Related to a topic", "Common preposition"],
    "brain": ["Inside your head", "Organ for thinking", "Controls your body"],
    "crane": ["A bird or machine", "Construction equipment", "Lifts heavy things"],
    "dance": ["Movement to music", "Ballroom activity", "Fun with rhythm"],
    "earth": ["Our planet", "Soil or ground", "Third from the sun"],
    "flame": ["Fire produces this", "Burns bright", "Hot and orange"],
    "grace": ["Elegance", "Smooth movement", "Also a name"],
    "heart": ["Body organ", "Symbol of love ❤️", "Pumps blood"],
    "image": ["A picture", "Visual representation", "Photo or drawing"],
    "judge": ["In a courtroom", "Makes decisions", "Wears a robe"],
    "knife": ["Kitchen tool", "Has a sharp blade", "Used for cutting"],
    "light": ["Opposite of dark", "Illumination", "Comes from sun"],
    "music": ["Sound and rhythm", "Songs and melodies", "Art of sound"],
    "night": ["Opposite of day", "Dark time", "Stars visible"],
    "ocean": ["Large body of water", "Salty water", "Has waves and tides"],
    "piano": ["Musical instrument", "Black and white keys", "Classical instrument"],
    "queen": ["Female ruler", "Chess piece", "Wears a crown"],
    "river": ["Flowing water", "Runs to sea", "Has banks"],
    "storm": ["Bad weather", "Thunder and rain", "Strong winds"],
    "tiger": ["Wild cat", "Has stripes", "Lives in jungle"],
    "ultra": ["Beyond extreme", "Prefix meaning beyond", "Super intense"],
    "virus": ["Causes illness", "Microscopic organism", "Needs a host"],
    "world": ["The Earth", "Our planet", "Where we live"],
    "yacht": ["Luxury boat", "Sailing vessel", "Rich person's boat"],
    "zebra": ["Striped animal", "Black and white", "Lives in Africa"],
}

DEFAULT_HINTS = ["It's a 5-letter English word", "Think carefully! 🤔", "You can do it! 💪"]


# ─────────────────────────────────────────────────
# 💾 DATA MANAGEMENT
# ─────────────────────────────────────────────────

def load_data():
    """Load game data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "games": {},       # active games per chat
        "scores": {},      # user scores
        "streaks": {},     # user streaks
        "daily": {},       # daily word per date
        "daily_played": {} # who played daily today
    }

def save_data(data):
    """Save game data to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_daily_word():
    """Get today's daily word (same for everyone)"""
    today = str(date.today())
    data = load_data()
    if today not in data["daily"]:
        data["daily"][today] = random.choice(WORD_LIST)
        save_data(data)
    return data["daily"][today]


# ─────────────────────────────────────────────────
# 🎮 GAME LOGIC
# ─────────────────────────────────────────────────

def check_guess(guess, secret):
    """
    Returns list of (letter, color) tuples
    🟩 green = correct position
    🟨 yellow = wrong position
    🟥 red = not in word
    """
    result = []
    secret_list = list(secret)
    guess_list = list(guess)
    colors = [EMOJI_NOT_IN_WORD] * 5

    # First pass: mark greens
    for i in range(5):
        if guess_list[i] == secret_list[i]:
            colors[i] = EMOJI_CORRECT
            secret_list[i] = None
            guess_list[i] = None

    # Second pass: mark yellows
    for i in range(5):
        if guess_list[i] is not None:
            if guess_list[i] in secret_list:
                colors[i] = EMOJI_WRONG_POS
                secret_list[secret_list.index(guess_list[i])] = None

    for i in range(5):
        result.append((guess[i].upper(), colors[i]))
    return result

def build_board(attempts):
    """Build the game board display"""
    board = ""
    for guess_word, result in attempts:
        emojis = "".join([e for _, e in result])
        letters = " ".join([l for l, _ in result])
        board += f"`{letters}` {emojis}\n"
    
    # Add empty rows
    empty_emoji = EMOJI_EMPTY * 5
    for _ in range(MAX_ATTEMPTS - len(attempts)):
        board += f"`_ _ _ _ _` {empty_emoji}\n"
    
    return board


# ─────────────────────────────────────────────────
# 📩 BOT COMMANDS
# ─────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with game info"""
    user = update.effective_user

    caption = (
        f"✨ *Welcome {user.first_name} to WordSeekBot!* ✨\n\n"
        "🔤 *The Ultimate Word Guessing Game*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎮 *HOW TO PLAY:*\n"
        "Guess the secret 5-letter word in 6 tries!\n\n"
        "🟩 = Right letter, right place\n"
        "🟨 = Right letter, wrong place\n"
        "🟥 = Letter not in word\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📜 *COMMANDS:*\n"
        "▸ /play — Start new game\n"
        "▸ /daily — Daily challenge\n"
        "▸ /hint — Get a hint\n"
        "▸ /score — Your stats\n"
        "▸ /top — Leaderboard\n"
        "▸ /streak — Daily streak\n"
        "▸ /endgame — End game\n"
        "▸ /help — Instructions\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏆 *SCORING:*\n"
        "• Win in 1 guess = 10 pts\n"
        "• Win in 2 guesses = 8 pts\n"
        "• Win in 3 guesses = 6 pts\n"
        "• Win in 4 guesses = 4 pts\n"
        "• Win in 5 guesses = 2 pts\n"
        "• Win in 6 guesses = 1 pt\n"
        "• Daily bonus = +3 pts\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 *Ready to play?* Type /play"
    )

    keyboard = [
        [InlineKeyboardButton("🎮 Play Now", callback_data="play"),
         InlineKeyboardButton("📅 Daily", callback_data="daily")],
        [InlineKeyboardButton("🏆 Leaderboard", callback_data="top"),
         InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(caption, parse_mode="Markdown", reply_markup=reply_markup)


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a new random word game"""
    chat_id = str(update.effective_chat.id)
    data = load_data()

    # Check if game already active
    if chat_id in data["games"] and data["games"][chat_id].get("active"):
        attempts_done = len(data["games"][chat_id]["attempts"])
        await update.message.reply_text(
            f"⚠️ *Game already running!*\n"
            f"📊 Attempts: *{attempts_done}/{MAX_ATTEMPTS}*\n\n"
            f"Keep guessing or /endgame to stop.",
            parse_mode="Markdown"
        )
        return

    # Start new game
    word = random.choice(WORD_LIST)
    
    data["games"][chat_id] = {
        "active": True,
        "word": word,
        "attempts": [],
        "start_time": datetime.now().isoformat(),
        "daily": False,
        "hints_given": 0
    }
    save_data(data)

    # Auto-end game after timeout
    asyncio.create_task(auto_end_game(chat_id, context, word))

    keyboard = [[InlineKeyboardButton("💡 Get Hint", callback_data=f"hint_{chat_id}")]]

    await update.message.reply_text(
        f"🎮 *New Game Started!*\n\n"
        f"🔤 Guess the *5-letter* word!\n"
        f"⏱️ Time limit: *{GAME_TIMEOUT//60} minutes*\n"
        f"🎯 Max attempts: *{MAX_ATTEMPTS}*\n\n"
        f"🟩 = Correct position\n"
        f"🟨 = Wrong position\n"
        f"🟥 = Not in word\n\n"
        f"*Type your 5-letter guess!* ✍️",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start daily word challenge"""
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    today = str(date.today())
    data = load_data()

    # Check if already played today
    played_key = f"{user_id}_{today}"
    if played_key in data.get("daily_played", {}):
        await update.message.reply_text(
            "✅ *You've already completed today's challenge!*\n"
            "🌅 Come back tomorrow for a new word!\n\n"
            "Try /play for a random game instead! 🎮",
            parse_mode="Markdown"
        )
        return

    # Check if game active
    if chat_id in data["games"] and data["games"][chat_id].get("active"):
        await update.message.reply_text(
            "⚠️ Finish current game first!\nUse /endgame to stop.",
            parse_mode="Markdown"
        )
        return

    # Start daily challenge
    word = get_daily_word()

    data["games"][chat_id] = {
        "active": True,
        "word": word,
        "attempts": [],
        "start_time": datetime.now().isoformat(),
        "daily": True,
        "hints_given": 0
    }
    save_data(data)

    asyncio.create_task(auto_end_game(chat_id, context, word))

    await update.message.reply_text(
        f"📅 *Daily Word Challenge!*\n"
        f"🗓️ {datetime.now().strftime('%B %d, %Y')}\n\n"
        f"🔤 Guess today's secret word!\n"
        f"⏱️ Time limit: *{GAME_TIMEOUT//60} minutes*\n"
        f"🎯 Max attempts: *{MAX_ATTEMPTS}*\n"
        f"🏆 *+3 bonus points* for completing!\n\n"
        f"*Type your 5-letter guess!* ✍️",
        parse_mode="Markdown"
    )


async def hint_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Give a hint for current game"""
    chat_id = str(update.effective_chat.id)
    data = load_data()

    if chat_id not in data["games"] or not data["games"][chat_id].get("active"):
        await update.message.reply_text("❌ No active game! Start with /play")
        return

    game = data["games"][chat_id]
    word = game["word"]
    hint_num = game.get("hints_given", 0)

    # Get hints for this word
    hints_list = HINTS.get(word, DEFAULT_HINTS)

    if hint_num >= len(hints_list):
        msg = (
            f"💡 *No more hints available!*\n\n"
            f"📝 Word has *{len(set(word))}* unique letters\n"
            f"🔤 First letter: *{word[0].upper()}*"
        )
    else:
        hint_text = hints_list[hint_num]
        data["games"][chat_id]["hints_given"] = hint_num + 1
        save_data(data)
        
        attempts_done = len(game["attempts"])
        msg = (
            f"💡 *Hint #{hint_num + 1}:*\n"
            f"_{hint_text}_\n\n"
            f"🔤 First letter: *{word[0].upper()}*\n"
            f"📊 Attempts: *{attempts_done}/{MAX_ATTEMPTS}*"
        )

    await update.message.reply_text(msg, parse_mode="Markdown")


async def score_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user stats and scores"""
    user = update.effective_user
    uid = str(user.id)
    data = load_data()

    scores = data.get("scores", {})
    streaks = data.get("streaks", {})

    user_score = scores.get(uid, {"total": 0, "wins": 0, "games": 0})
    user_streak = streaks.get(uid, {"current": 0, "best": 0, "last_date": None})

    win_rate = 0
    if user_score.get("games", 0) > 0:
        win_rate = round((user_score.get("wins", 0) / user_score["games"]) * 100)

    await update.message.reply_text(
        f"📊 *{user.first_name}'s Stats*\n\n"
        f"⭐ Total Score: *{user_score.get('total', 0)} pts*\n"
        f"🎮 Games Played: *{user_score.get('games', 0)}*\n"
        f"✅ Games Won: *{user_score.get('wins', 0)}*\n"
        f"📈 Win Rate: *{win_rate}%*\n\n"
        f"🔥 Current Streak: *{user_streak.get('current', 0)} days*\n"
        f"🏆 Best Streak: *{user_streak.get('best', 0)} days*\n\n"
        f"Keep playing to improve! 💪",
        parse_mode="Markdown"
    )


async def top_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show global leaderboard"""
    data = load_data()
    scores = data.get("scores", {})

    if not scores:
        await update.message.reply_text("📊 No scores yet! Start playing with /play")
        return

    # Sort by total score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1].get("total", 0), reverse=True)
    
    leaderboard = "🏆 *LEADERBOARD - Top 10*\n"
    leaderboard += "━━━━━━━━━━━━━━━━━━━━━━\n\n"

    for i, (uid, score_data) in enumerate(sorted_scores[:10], 1):
        try:
            user = await context.bot.get_chat(int(uid))
            name = user.first_name or "Unknown"
        except:
            name = "User"
        
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        
        leaderboard += (
            f"{medal} *{name}*\n"
            f"   ⭐ {score_data.get('total', 0)} pts | "
            f"🎮 {score_data.get('wins', 0)}/{score_data.get('games', 0)} wins\n\n"
        )

    await update.message.reply_text(leaderboard, parse_mode="Markdown")


async def streak_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's daily streak"""
    user = update.effective_user
    uid = str(user.id)
    data = load_data()

    streaks = data.get("streaks", {})
    user_streak = streaks.get(uid, {"current": 0, "best": 0, "last_date": None})

    current = user_streak.get("current", 0)
    best = user_streak.get("best", 0)
    
    fire_emojis = "🔥" * min(current, 10)

    await update.message.reply_text(
        f"🔥 *Daily Streak Status*\n\n"
        f"{fire_emojis}\n\n"
        f"🔥 Current Streak: *{current} days*\n"
        f"🏆 Best Streak: *{best} days*\n\n"
        f"Play /daily every day to maintain your streak! 📅",
        parse_mode="Markdown"
    )


async def endgame_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """End current game"""
    chat_id = str(update.effective_chat.id)
    data = load_data()

    if chat_id not in data["games"] or not data["games"][chat_id].get("active"):
        await update.message.reply_text("❌ No active game to end!")
        return

    word = data["games"][chat_id]["word"]
    attempts = len(data["games"][chat_id]["attempts"])
    
    data["games"][chat_id]["active"] = False
    save_data(data)

    await update.message.reply_text(
        f"🛑 *Game Ended!*\n\n"
        f"The word was: *{word.upper()}*\n"
        f"Attempts used: *{attempts}/{MAX_ATTEMPTS}*\n\n"
        f"Better luck next time! Start a new game with /play 🎮",
        parse_mode="Markdown"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    help_text = (
        "❓ *HOW TO PLAY WORDSEEK*\n\n"
        "🎯 *Goal:* Guess the 5-letter word in 6 tries\n\n"
        "📝 *How it works:*\n"
        "• Type any 5-letter word as your guess\n"
        "• Get feedback after each guess:\n"
        "  🟩 = Correct letter, correct position\n"
        "  🟨 = Correct letter, wrong position\n"
        "  🟥 = Letter not in word\n\n"
        "🎮 *Game Modes:*\n"
        "• /play — Random word game\n"
        "• /daily — Same word for everyone today\n\n"
        "💡 *Tips:*\n"
        "• Use /hint for clues\n"
        "• Start with common letters (A, E, I, O, U)\n"
        "• Pay attention to the colored feedback\n"
        "• Try different letter positions\n\n"
        "🏆 *Scoring:*\n"
        "Fewer guesses = more points!\n"
        "Daily challenges give bonus points\n\n"
        "Good luck! 🍀"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


# ─────────────────────────────────────────────────
# 🎯 MESSAGE HANDLER (for guesses)
# ─────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle word guesses"""
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name
    text = update.message.text.strip().lower()
    
    data = load_data()

    # Check if game is active
    if chat_id not in data["games"] or not data["games"][chat_id].get("active"):
        return  # Ignore non-game messages

    game = data["games"][chat_id]
    word = game["word"]

    # Validate guess
    if len(text) != 5:
        await update.message.reply_text("⚠️ Please enter exactly 5 letters!")
        return

    if not text.isalpha():
        await update.message.reply_text("⚠️ Only letters allowed!")
        return

    if text not in WORD_LIST:
        await update.message.reply_text("⚠️ Not a valid English word! Try again.")
        return

    # Check guess
    result = check_guess(text, word)
    game["attempts"].append((text, result))
    attempts_count = len(game["attempts"])

    # Build board display
    board = build_board(game["attempts"])

    # Check if won
    if text == word:
        # Calculate score
        points = SCORE_MAP.get(attempts_count, 1)
        
        if game.get("daily"):
            points += DAILY_BONUS  # Daily bonus

        # Update user score
        if user_id not in data["scores"]:
            data["scores"][user_id] = {"total": 0, "wins": 0, "games": 0}
        
        data["scores"][user_id]["total"] += points
        data["scores"][user_id]["wins"] += 1
        data["scores"][user_id]["games"] += 1

        # Update streak for daily
        if game.get("daily"):
            today = str(date.today())
            played_key = f"{user_id}_{today}"
            data["daily_played"][played_key] = True
            
            update_streak(data, user_id)

        game["active"] = False
        save_data(data)

        celebration = ["🎉", "🎊", "🏆", "✨", "🌟"][attempts_count % 5]
        
        await update.message.reply_text(
            f"{celebration} *WINNER!* {celebration}\n\n"
            f"{board}\n"
            f"🎯 Word: *{word.upper()}*\n"
            f"📊 Solved in: *{attempts_count}/{MAX_ATTEMPTS}* attempts\n"
            f"⭐ Points earned: *+{points}*\n"
            f"🏆 Total score: *{data['scores'][user_id]['total']}*\n\n"
            f"Excellent work, {user_name}! 🎊",
            parse_mode="Markdown"
        )
        return

    # Check if lost
    if attempts_count >= MAX_ATTEMPTS:
        # Update games played
        if user_id not in data["scores"]:
            data["scores"][user_id] = {"total": 0, "wins": 0, "games": 0}
        data["scores"][user_id]["games"] += 1

        game["active"] = False
        save_data(data)

        await update.message.reply_text(
            f"😔 *Game Over!*\n\n"
            f"{board}\n"
            f"❌ No attempts remaining\n"
            f"🎯 The word was: *{word.upper()}*\n\n"
            f"Better luck next time! Try /play for a new game 🎮",
            parse_mode="Markdown"
        )
        return

    # Continue game
    save_data(data)
    
    keyboard = [[InlineKeyboardButton("💡 Get Hint", callback_data=f"hint_{chat_id}")]]
    
    await update.message.reply_text(
        f"📊 *Attempt {attempts_count}/{MAX_ATTEMPTS}*\n\n"
        f"{board}\n"
        f"Keep guessing! {MAX_ATTEMPTS - attempts_count} attempts left ✍️",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def update_streak(data, user_id):
    """Update daily streak for user"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    if user_id not in data["streaks"]:
        data["streaks"][user_id] = {"current": 0, "best": 0, "last_date": None}
    
    streak = data["streaks"][user_id]
    last_date_str = streak.get("last_date")
    
    if last_date_str:
        last_date = date.fromisoformat(last_date_str)
        
        if last_date == yesterday:
            # Continue streak
            streak["current"] += 1
        elif last_date < yesterday:
            # Streak broken
            streak["current"] = 1
        # If last_date == today, already played (shouldn't happen)
    else:
        # First time
        streak["current"] = 1
    
    streak["last_date"] = str(today)
    
    # Update best streak
    if streak["current"] > streak.get("best", 0):
        streak["best"] = streak["current"]


# ─────────────────────────────────────────────────
# ⏰ AUTO-END GAME AFTER TIMEOUT
# ─────────────────────────────────────────────────

async def auto_end_game(chat_id, context, word):
    """Auto-end game after timeout"""
    await asyncio.sleep(GAME_TIMEOUT)
    
    data = load_data()
    
    if chat_id in data["games"] and data["games"][chat_id].get("active"):
        attempts = len(data["games"][chat_id]["attempts"])
        data["games"][chat_id]["active"] = False
        save_data(data)
        
        await context.bot.send_message(
            chat_id=int(chat_id),
            text=(
                f"⏱️ *Time's Up!*\n\n"
                f"The word was: *{word.upper()}*\n"
                f"Attempts used: *{attempts}/{MAX_ATTEMPTS}*\n\n"
                f"Start a new game with /play! 🎮"
            ),
            parse_mode="Markdown"
        )


# ─────────────────────────────────────────────────
# 🔘 BUTTON CALLBACKS
# ─────────────────────────────────────────────────

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "play":
        # Simulate /play command
        update.message = query.message
        await play(update, context)
    
    elif data == "daily":
        update.message = query.message
        await daily(update, context)
    
    elif data == "top":
        update.message = query.message
        await top_cmd(update, context)
    
    elif data == "help":
        update.message = query.message
        await help_cmd(update, context)
    
    elif data.startswith("hint_"):
        chat_id = data.split("_")[1]
        await give_hint_callback(update, context, chat_id)


async def give_hint_callback(update, context, chat_id):
    """Give hint via callback"""
    data = load_data()

    if chat_id not in data["games"] or not data["games"][chat_id].get("active"):
        await context.bot.send_message(
            chat_id=int(chat_id),
            text="❌ No active game!"
        )
        return

    game = data["games"][chat_id]
    word = game["word"]
    hint_num = game.get("hints_given", 0)

    hints_list = HINTS.get(word, DEFAULT_HINTS)

    if hint_num >= len(hints_list):
        msg = (
            f"💡 *No more hints!*\n\n"
            f"📝 Word has *{len(set(word))}* unique letters\n"
            f"🔤 First letter: *{word[0].upper()}*"
        )
    else:
        hint_text = hints_list[hint_num]
        data["games"][chat_id]["hints_given"] = hint_num + 1
        save_data(data)
        
        attempts_done = len(game["attempts"])
        msg = (
            f"💡 *Hint #{hint_num + 1}:*\n"
            f"_{hint_text}_\n\n"
            f"🔤 First letter: *{word[0].upper()}*\n"
            f"📊 Attempts: *{attempts_done}/{MAX_ATTEMPTS}*"
        )

    await context.bot.send_message(
        chat_id=int(chat_id),
        text=msg,
        parse_mode="Markdown"
    )


# ─────────────────────────────────────────────────
# 🚀 MAIN FUNCTION
# ─────────────────────────────────────────────────

def main():
    """Start the bot"""
    print("🔤 WordSeekBot starting...")
    
    # Create application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("hint", hint_cmd))
    application.add_handler(CommandHandler("score", score_cmd))
    application.add_handler(CommandHandler("top", top_cmd))
    application.add_handler(CommandHandler("streak", streak_cmd))
    application.add_handler(CommandHandler("endgame", endgame_cmd))
    application.add_handler(CommandHandler("help", help_cmd))
    
    # Message handler for guesses
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Button callback handler
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()
