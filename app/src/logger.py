import sys
import logging


class StdFormatter(logging.Formatter):
    _enable_exceptions: bool = False

    def format(self, record):

        color = {
            logging.CRITICAL: (31, 31),
            logging.ERROR: (31, 31),
            logging.FATAL: (31, 31),
            logging.WARNING: (33, 33),
            logging.DEBUG: (36, 36),
            logging.INFO: (32, 32)
        }.get(record.levelno, 0)

        self._style._fmt = (f"\033[37m[%(asctime)s]\033[0m "
                            f"\033[{color[0]}m%(levelname)-8s\033[0m "
                            f"\033[37m[%(filename)s/%(funcName)s:%(lineno)s]\033[0m "
                            f"\033[{color[1]}m%(message)s\033[0m")

        formatted_log = super().format(record)

        sp = ' ' * (8 - len(record.levelname))
        prefix = f'[{record.asctime}] {record.levelname}{sp} [{record.filename}/{record.funcName}:{record.lineno}] '

        return formatted_log.replace('\n', '\n' + ' '*len(prefix))

    def set_exceptions_enabled(self, enable: bool):
        self._enable_exceptions = enable

    def formatException(self, exc_info) -> str:
        if self._enable_exceptions:
            return super().formatException(exc_info)
        return ''


def get_std_handler(level: int, enable_exc: bool) -> logging.StreamHandler:
    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.set_name('STD_HANDLER')
    std_handler.setLevel(level)
    std_formatter = StdFormatter()
    std_formatter.set_exceptions_enabled(enable_exc)
    std_handler.setFormatter(std_formatter)
    return std_handler


def set_lib_log(level: int):
    logging.getLogger("requests").setLevel(level)
    logging.getLogger("databases").setLevel(level)
    logging.getLogger("urllib3").setLevel(level)
    logging.getLogger('asyncio').setLevel(level)


def set_logger(std_level: int = logging.INFO, enable_std_exceptions: bool = False) -> logging.Logger:
    set_lib_log(logging.WARNING)
    logger = logging.getLogger()
    handlers = logger.handlers
    for handler in handlers:
        logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_std_handler(std_level, enable_std_exceptions))
    return logging.getLogger()
