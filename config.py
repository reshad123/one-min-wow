"""
Central config for the daily Shorts automation.
Edit TOPICS to add/remove niches. The bot rotates through them
so you get variety instead of the same niche every day.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

TOPICS = [
    {
        "niche": "food_science",
        "prompt_hint": (
            "one surprising, verifiable fact about everyday food or cooking "
            "science -- why something happens when you cook, freeze, or eat "
            "a common food (bread, chocolate, coffee, fruit, spices, etc). "
            "Make it feel like a kitchen secret most people never learned."
        ),
        "visual_keywords": [
            "cooking closeup",
            "food preparation",
            "kitchen closeup",
            "fresh ingredients",
            "coffee pour",
        ],
        "hashtags": "#foodfacts #curiosity #wow #facts #shorts",
    },
    {
        "niche": "nature_weather",
        "prompt_hint": (
            "one surprising, verifiable fact about weather, nature, or the "
            "outdoors -- clouds, storms, oceans, forests, rivers, or seasons. "
            "Something people see all the time but never understood why it "
            "happens."
        ),
        "visual_keywords": [
            "storm clouds",
            "ocean waves",
            "forest nature",
            "rain closeup",
            "sunset landscape",
        ],
        "hashtags": "#naturefacts #curiosity #wow #facts #shorts",
    },
    {
        "niche": "everyday_objects",
        "prompt_hint": (
            "one surprising, verifiable fact about a common everyday object "
            "or material -- glass, metal, paper, plastic, fabric, or a "
            "household item. Something that sounds impossible but is "
            "scientifically true."
        ),
        "visual_keywords": [
            "glass closeup",
            "metal texture",
            "fabric closeup",
            "paper texture",
            "household items",
        ],
        "hashtags": "#didyouknow #curiosity #wow #facts #shorts",
    },
]


VIDEOS_PER_DAY = 3

# Uploads and reports must target this channel.
SILENTVISION_CHANNEL_ID = "UCOuRLbO73RGZktBUP0zoEjg"
SILENTVISION_CHANNEL_TITLE = "One Min WOW"

# One Short per window so uploads are spaced, not dumped at once.
# Times are UTC (US Eastern/EDT: 8am / 3pm / 9pm).
POST_WINDOWS = (
    {"name": "morning", "utc_hour": 12},
    {"name": "afternoon", "utc_hour": 19},
    {"name": "night", "utc_hour": 1},
)
SLOT_NAMES = {window["name"]: index for index, window in enumerate(POST_WINDOWS)}


def slot_for_now(name: str | None = None) -> int:
    """
    Map a window name or the current UTC hour to slot 0, 1, or 2.
    """
    if name:
        key = name.strip().lower()
        if key.isdigit():
            return max(0, min(VIDEOS_PER_DAY - 1, int(key)))
        if key in SLOT_NAMES:
            return SLOT_NAMES[key]

    from datetime import datetime, timezone

    hour = datetime.now(timezone.utc).hour
    if hour < 1:
        return 2
    if hour < 12:
        return 2
    if hour < 19:
        return 0
    return 1


def pick_topic_for_slot(slot: int = 0):
    """
    Each daily window posts one niche. Slot 0, 1, 2 rotate through
    TOPICS, shifted by day-of-year so the order changes.
    """
    import datetime

    day_index = datetime.date.today().timetuple().tm_yday
    return TOPICS[(day_index + int(slot)) % len(TOPICS)]


def pick_topic_for_today():
    return pick_topic_for_slot(slot_for_now())


# ---- Video settings ----
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # vertical, for Shorts
TARGET_DURATION_SECONDS = 45
MIN_DURATION_SECONDS = 40
MAX_DURATION_SECONDS = 55
# Spoken at the end of every Short. Captions follow the voice.
END_CTA = "Subscribe to One Min Wow for more surprising facts."
FONT_SIZE = 60
CAPTION_COLOR = "white"
CAPTION_HIGHLIGHT_COLOR = "#FFD700"

# TTS voice (edge-tts). Full list: `edge-tts --list-voices`
TTS_VOICE = "en-US-GuyNeural"

# Output paths
WORKDIR = "workdir"
