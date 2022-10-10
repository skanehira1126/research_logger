from logging import Formatter, StreamHandler, Filter, getLogger
from logging import DEBUG


class CustomFilter(Filter):
    """[hidden]から始まるメッセージを表示しない"""
    def filter(self, record):
        message = record.getMessage()
        return not message.startswith("[hidden]")


def main():
    # ===== formatter
    # logの出力形式を設定する
    fmt = "[%(levelname)s][%(filename)s]%(module)s - %(funcName)s - %(lineno)d : %(message)s"
    formatter = Formatter(fmt)

    # ===== Filter
    my_filter = CustomFilter()

    # ===== handler
    # logの出力について管理する
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(formatter)
    handler.addFilter(my_filter)

    # ===== loggerの生成
    logger = getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(DEBUG)

    # まずは基本
    logger.debug("debug log")
    logger.info("info log")
    logger.warning("warning log")
    logger.error("error log")
    try:
        assert False
    except AssertionError as e:
        logger.exception("exception log")

    # ====== hiddenをつける
    logger.info("[hidden] This is hidden message")  # 出力されない


if __name__ == "__main__":
    main()
