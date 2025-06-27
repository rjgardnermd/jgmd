import logging

SUCCESS_LEVEL_NUM = 25
SUCCESS_LEVEL_NAME = "SUCCESS"
SUCCESS_COLOR = "green"


def add_success_log_level():
    if not hasattr(logging, SUCCESS_LEVEL_NAME):
        logging.addLevelName(SUCCESS_LEVEL_NUM, SUCCESS_LEVEL_NAME)

        def success(self, message, *args, **kws):
            if self.isEnabledFor(SUCCESS_LEVEL_NUM):
                self._log(SUCCESS_LEVEL_NUM, message, args, **kws)

        logging.Logger.success = success

    # Patch coloredlogs to support the new level
    try:
        import coloredlogs

        if SUCCESS_LEVEL_NAME not in coloredlogs.DEFAULT_LEVEL_STYLES:
            coloredlogs.DEFAULT_LEVEL_STYLES[SUCCESS_LEVEL_NAME] = {
                "color": SUCCESS_COLOR
            }
    except ImportError:
        pass
