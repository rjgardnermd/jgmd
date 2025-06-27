from enum import Enum


class Icons(Enum):
    """Emoji icons for use in log messages."""

    # Success/Completion
    SUCCESS = "✅"
    COMPLETE = "🎉"
    DONE = "✨"
    CHECK = "✓ "

    # Information
    INFO = "ℹ️ "
    NOTE = "📝"
    BULB = "💡"
    BOOK = "📚"

    # Warning
    WARNING = "⚠️ "
    ALERT = "🚨"
    BELL = "🔔"

    # Error/Failure
    ERROR = "❌"
    FAIL = "💥"
    BUG = "🪲 "
    CRASH = "💀"

    # Processing/Progress
    LOADING = "⏳"
    SPINNER = "🔄"
    GEAR = "⚙️ "
    ROCKET = "🚀"

    # Data/Storage
    DATABASE = "🗄️ "
    FILE = "📁"
    FOLDER = "📂"
    DISK = "��"
    TABLE = "📊"

    # Network/Communication
    NETWORK = "🌐"
    WIFI = "📶"
    EMAIL = "📧"
    PHONE = "📞"

    # Time
    CLOCK = "⏰"
    TIMER = "⏱️ "
    CALENDAR = "📅"

    # User/Action
    USER = "👤"
    TEAM = "👥"
    HAND = "👋"
    THUMBS_UP = "👍"
    THUMBS_DOWN = "👎"

    # Development
    CODE = "💻"
    TERMINAL = "🖥️ "
    DEBUG = "🔍"
    TEST = "🧪"

    # Business
    MONEY = "💰"
    CHART = "📊"
    GRAPH = "📈"
    TARGET = "🎯"

    # Fun/Misc
    PARTY = "🎊"
    GIFT = "🎁"
    STAR = "⭐"
    HEART = "❤️ "
    FIRE = "🔥"
    COOL = "😎"

    # @classmethod
    # def get_icon(cls, icon_name: str, use_icons: bool = None) -> str:
    #     """
    #     Get an icon with optional fallback to text for cloud logging compatibility.

    #     Args:
    #         icon_name: Name of the icon (e.g., 'SUCCESS', 'ERROR')
    #         use_icons: Whether to use emoji icons. If None, checks JGMD_USE_ICONS env var.
    #                   If True, uses emojis. If False, uses text alternatives.

    #     Returns:
    #         Icon string (emoji or text alternative)
    #     """
    #     if use_icons is None:
    #         use_icons = os.getenv("JGMD_USE_ICONS", "true").lower() == "true"

    #     if not use_icons:
    #         # Text alternatives for cloud logging compatibility
    #         text_alternatives = {
    #             "SUCCESS": "[SUCCESS]",
    #             "COMPLETE": "[COMPLETE]",
    #             "DONE": "[DONE]",
    #             "CHECK": "[CHECK]",
    #             "INFO": "[INFO]",
    #             "NOTE": "[NOTE]",
    #             "BULB": "[IDEA]",
    #             "BOOK": "[DOC]",
    #             "WARNING": "[WARN]",
    #             "ALERT": "[ALERT]",
    #             "BELL": "[BELL]",
    #             "ERROR": "[ERROR]",
    #             "FAIL": "[FAIL]",
    #             "BUG": "[BUG]",
    #             "CRASH": "[CRASH]",
    #             "LOADING": "[LOADING]",
    #             "SPINNER": "[PROCESSING]",
    #             "GEAR": "[CONFIG]",
    #             "ROCKET": "[LAUNCH]",
    #             "DATABASE": "[DB]",
    #             "FILE": "[FILE]",
    #             "FOLDER": "[FOLDER]",
    #             "DISK": "[DISK]",
    #             "TABLE": "[TABLE]",
    #             "NETWORK": "[NET]",
    #             "WIFI": "[WIFI]",
    #             "EMAIL": "[EMAIL]",
    #             "PHONE": "[PHONE]",
    #             "CLOCK": "[TIME]",
    #             "TIMER": "[TIMER]",
    #             "CALENDAR": "[DATE]",
    #             "USER": "[USER]",
    #             "TEAM": "[TEAM]",
    #             "HAND": "[WAVE]",
    #             "THUMBS_UP": "[OK]",
    #             "THUMBS_DOWN": "[FAIL]",
    #             "CODE": "[CODE]",
    #             "TERMINAL": "[TERM]",
    #             "DEBUG": "[DEBUG]",
    #             "TEST": "[TEST]",
    #             "MONEY": "[MONEY]",
    #             "CHART": "[CHART]",
    #             "GRAPH": "[GRAPH]",
    #             "TARGET": "[TARGET]",
    #             "PARTY": "[CELEBRATE]",
    #             "GIFT": "[GIFT]",
    #             "STAR": "[STAR]",
    #             "HEART": "[LOVE]",
    #             "FIRE": "[HOT]",
    #             "COOL": "[COOL]",
    #         }
    #         return text_alternatives.get(icon_name, f"[{icon_name}]")

    #     # Use emoji icons
    #     try:
    #         return cls[icon_name].value
    #     except KeyError:
    #         return f"[{icon_name}]"
