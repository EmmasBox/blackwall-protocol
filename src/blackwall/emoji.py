
import random

from blackwall.settings import get_user_setting

emoji_allowed = get_user_setting(section="display",setting="emojis")

def get_emoji(emoji: str | list[str]) -> str:
    if emoji_allowed is not False:
        if emoji is type(str):
            return emoji
        else:
            return random.choice(emoji)
    else:
        return ""