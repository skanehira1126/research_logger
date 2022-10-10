import sys
from logging import getLogger, StreamHandler, Formatter
from logging import INFO, ERROR
from logging import LoggerAdapter


def make_logger(name, fmt):
    logger = getLogger(name)
    logger.setLevel(INFO)
    logger.handlers = []

    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter(fmt))
    handler.setLevel(INFO)

    logger.addHandler(handler)

    return logger


class CustomLoggerAdapter(LoggerAdapter):
    """
    This class can hides logging message manually.
    """

    def __init__(self, logger, extra=None):
        super(CustomLoggerAdapter, self).__init__(logger, extra)
        self.is_hidden = False

    def process(self, msg, kwargs):
        """kwargs has arguments of logging function."""
        is_hidden = kwargs.pop("is_hidden", self.is_hidden)
        if is_hidden:
            msg = "******"

        return msg, kwargs

    def custom_error(self, msg, *args, **kwargs):
        """
        custom error method
        """
        self.log(ERROR, msg, *args, **kwargs)


def main():
    fmt = (
        "[%(levelname)s][%(filename)s]%(module)s - %(funcName)s - %(lineno)d : %(message)s"
        "[%(extra_msg)s]"
    )
    logger = make_logger("logger", fmt)
    extra = {"extra_msg": "Extra message"}

    # default logger
    print("This is default logger. 'extra' must be set at each times of logging.")
    logger.info("logger_adapter info log", extra=extra)
    logger.warning("logger_adapter warning log", extra=extra)
    logger.error("logger_adapter error log", extra=extra)
    print("")

    # logger adapter
    """
    process関数がlogger adapterがもつextra変数をkwargsに入れる。
    kwargs["extra"]はLogRecordクラスに渡され、Formatter中の変数の置換する値として利用できる
    -> つまりFormatterにextraの'key'を指定しておくとそこを埋めることができる
    -> 辞書Likeなオブジェクトなら渡すことができる

    Note
    -----
    default process function
    https://github.com/python/cpython/blob/29f1b0bb1ff73dcc28f0ca7e11794141b6de58c9/Lib/logging/__init__.py#L1898-L1909
    """
    print("This is logger adapter. 'extra' must be set when logger adapter is created.")
    _logger = make_logger("logger_adapter", fmt)
    logger_adapter = LoggerAdapter(_logger, extra=extra)
    logger_adapter.info("logger_adapter info log")
    logger_adapter.warning("logger_adapter warning log")
    logger_adapter.error("logger_adapter error log")
    print("")

    # custom logger adapter
    print("This is custom logger adapter. This logger can hidden message.")
    fmt = (
        "[%(levelname)s][%(filename)s]%(module)s - %(funcName)s - %(lineno)d : %(message)s"
    )
    _logger = make_logger("custom_logger", fmt)
    custom_logger = CustomLoggerAdapter(_logger)
    custom_logger.info("info")
    custom_logger.warning("warning")
    custom_logger.error("error")
    # 自前で作った関数はlinenoが関数定義内でlog関数を読んでいる場所の行数になる
    custom_logger.custom_error("Custom error function")
    custom_logger.error("error with is_hidden", is_hidden=True)
    try:
        assert False
    except AssertionError as e:
        custom_logger.exception("exception.")
    print("")


if __name__ == "__main__":
    main()



