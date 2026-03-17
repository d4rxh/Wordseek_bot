"""
╔══════════════════════════════════════════════════╗
║              CONFIGURATION FILE                  ║
║     Bot settings and environment variables       ║
╚══════════════════════════════════════════════════╝
"""

import os
from typing import Optional

# ─────────────────────────────────────────────────
# 🔑 BOT TOKEN (Environment Variable se)
# ─────────────────────────────────────────────────

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise ValueError(
        "❌ BOT_TOKEN not found!\n"
        "Please set BOT_TOKEN in:\n"
        "  • Replit: Secrets tab\n"
        "  • Local: .env file\n"
        "  • Terminal: export BOT_TOKEN='your_token'"
    )

# ─────────────────────────────────────────────────
# ⚙️ GAME SETTINGS
# ─────────────────────────────────────────────────

# Game Configuration
GAME_TIMEOUT: int = int(os.getenv("GAME_TIMEOUT", "120"))  # seconds
MAX_ATTEMPTS: int = int(os.getenv("MAX_ATTEMPTS", "6"))    # max guesses
WORD_LENGTH: int = 5                                        # letter count

# Timer settings
AUTO_END_ENABLED: bool = True  # Auto-end game after timeout

# ─────────────────────────────────────────────────
# 🎨 UI SETTINGS
# ─────────────────────────────────────────────────

# Emojis for feedback
EMOJI_CORRECT: str = "🟩"      # Correct position
EMOJI_WRONG_POS: str = "🟨"    # Wrong position
EMOJI_NOT_IN_WORD: str = "🟥"  # Not in word
EMOJI_EMPTY: str = "⬜"         # Empty slot

# Other emojis
EMOJI_TROPHY: str = "🏆"
EMOJI_FIRE: str = "🔥"
EMOJI_STAR: str = "⭐"
EMOJI_GAME: str = "🎮"

# ─────────────────────────────────────────────────
# 🏆 SCORING SYSTEM
# ─────────────────────────────────────────────────

# Points based on attempts
SCORE_MAP: dict = {
    1: 10,  # Perfect! First try
    2: 8,   # Excellent
    3: 6,   # Great
    4: 4,   # Good
    5: 2,   # Nice
    6: 1    # Won!
}

# Bonus points
DAILY_BONUS: int = 3    # Extra points for daily challenge
STREAK_BONUS: int = 1   # Bonus per streak day (optional)

# ─────────────────────────────────────────────────
# 💾 DATA STORAGE
# ─────────────────────────────────────────────────

DATA_FILE: str = os.getenv("DATA_FILE", "wordseek_data.json")
BACKUP_ENABLED: bool = False  # Auto-backup (set to True if needed)

# ─────────────────────────────────────────────────
# 🎯 FEATURE FLAGS
# ─────────────────────────────────────────────────

# Enable/disable features
ENABLE_DAILY_CHALLENGE: bool = True
ENABLE_HINTS: bool = True
ENABLE_LEADERBOARD: bool = True
ENABLE_STREAKS: bool = True
ENABLE_GROUPS: bool = True

# ─────────────────────────────────────────────────
# 🌐 OPTIONAL SETTINGS
# ─────────────────────────────────────────────────

# Start image URL (optional)
START_IMAGE_URL: Optional[str] = os.getenv("START_IMAGE_URL")

# Admin user IDs (comma-separated in env)
ADMIN_IDS: list = os.getenv("ADMIN_IDS", "").split(",") if os.getenv("ADMIN_IDS") else []

# Logging level
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# ─────────────────────────────────────────────────
# 📊 WORD SETTINGS
# ─────────────────────────────────────────────────

# Minimum unique letters in word
MIN_UNIQUE_LETTERS: int = 3

# Word difficulty (future feature)
DIFFICULTY_LEVELS: dict = {
    "easy": 1,
    "medium": 2,
    "hard": 3
}

# ─────────────────────────────────────────────────
# 🔧 ADVANCED SETTINGS
# ─────────────────────────────────────────────────

# Rate limiting (optional)
MAX_GAMES_PER_DAY: Optional[int] = None  # None = unlimited

# Message cleanup
AUTO_DELETE_MESSAGES: bool = False
MESSAGE_DELETE_DELAY: int = 30  # seconds

# ─────────────────────────────────────────────────
# 📝 VALIDATION
# ─────────────────────────────────────────────────

def validate_config() -> bool:
    """Validate configuration settings"""
    
    if not BOT_TOKEN:
        return False
    
    if GAME_TIMEOUT < 30:
        raise ValueError("GAME_TIMEOUT must be at least 30 seconds")
    
    if MAX_ATTEMPTS < 1 or MAX_ATTEMPTS > 10:
        raise ValueError("MAX_ATTEMPTS must be between 1 and 10")
    
    if WORD_LENGTH != 5:
        raise ValueError("WORD_LENGTH must be 5 (for now)")
    
    return True


# Run validation on import
validate_config()


# ─────────────────────────────────────────────────
# 📋 CONFIG SUMMARY (for debugging)
# ─────────────────────────────────────────────────

def print_config() -> None:
    """Print current configuration (for debugging)"""
    print("=" * 50)
    print("🔧 WORDSEEK BOT CONFIGURATION")
    print("=" * 50)
    print(f"Bot Token: {'✅ Set' if BOT_TOKEN else '❌ Missing'}")
    print(f"Game Timeout: {GAME_TIMEOUT}s")
    print(f"Max Attempts: {MAX_ATTEMPTS}")
    print(f"Word Length: {WORD_LENGTH}")
    print(f"Daily Challenge: {'✅' if ENABLE_DAILY_CHALLENGE else '❌'}")
    print(f"Hints System: {'✅' if ENABLE_HINTS else '❌'}")
    print(f"Leaderboard: {'✅' if ENABLE_LEADERBOARD else '❌'}")
    print(f"Streaks: {'✅' if ENABLE_STREAKS else '❌'}")
    print(f"Data File: {DATA_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    # Test configuration
    print_config()
