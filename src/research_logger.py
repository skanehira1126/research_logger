from logging import getLogger, setLoggerClass, getLogRecordFactory, setLogRecordFactory
from logging import Formatter, StreamHandler, getLogger
from logging import INFO

"""
やりたいこと
-----
logger.xxx()をカスタムしたい.
    * Levelに合わせて文字列を付与するとか 

手段
-----
1. LoggerAdapterを使う : pythonのloggerの行けてないところでlineno変数がおかしくなる
2. CustomLoggerを使う : 同上 
3. Filterを利用する : ログレコードに属性を付与するような使い方ができる. ただ、あまり直感的じゃないかも？
4. LogRecordFactoryを使う : いいかも？
"""


def setup_logger(name: str, fmt: str):

    formatter = Formatter(fmt)
    handler = StreamHandler()
    handler.setLevel(INFO)
    handler.setFormatter(formatter)

    _logger = getLogger(name)
    _logger.addHandler(handler)
    _logger.setLevel(INFO)

    return _logger


current_factory = getLogRecordFactory()


def record_factory(*args, **kwargs):
    """new_attrという属性を追加する"""
    record = current_factory(*args, **kwargs)
    record.new_attr = "new_attributes"
    return record


def main():
    fmt = "[%(levelname)s][%(filename)s]%(module)s - %(funcName)s - %(lineno)d : %(message)s"
    logger = setup_logger("basic", fmt)
    # まずは基本
    logger.info("basic log")
    logger.warning("basic log")
    logger.error("basic log")

    # record factoryを利用してみる
    fmt = "[%(levelname)s][%(filename)s]%(module)s - %(funcName)s - %(lineno)d : %(message)s"
    fmt += "- %(new_attr)s"
    logger = setup_logger("record_factory", fmt)
    setLogRecordFactory(record_factory)
    # まずは基本
    logger.info("factory log")
    logger.warning("factory log")
    logger.error("factory log")



if __name__ == "__main__":
    main()
