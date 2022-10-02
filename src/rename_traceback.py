import traceback
import sys


class NestRaiser:

    def __init__(self, error_msg: str = "Errorが発生"):

        self.cnt = 0
        self.error_msg = error_msg

    def __call__(self, max_iter: int = 5):
        self.cnt += 1

        if self.cnt == max_iter:
            raise ValueError(self.error_msg)
        else:
            self()

    def reset(self):
        self.cnt = 1


if __name__ == "__main__":
    nest_raiser = NestRaiser()

    # tracebackを取得する
    try:
        nest_raiser(max_iter=3)
    except ValueError as e:
        # exception情報を取得
        # exc_tracebackはtracebackモジュールと合わせて使う
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("===== sys.exc_info()")
        print("exc_type : ", type(exc_type), exc_type)
        print("exc_value : ", type(exc_value), exc_value)
        print("exc_traceback : ", type(exc_traceback), exc_traceback)
        print("===== traceback.format_exc()")
        print("Type : ", type(traceback.format_exc()))
        print(traceback.format_exc())
        print("===== traceback.format_stack()")
        print("Type : ", type(traceback.format_stack()))
        print(traceback.format_stack())
        print("===== traceback.extract_tb()")
        print(traceback.extract_tb(exc_traceback))
        print("===== ===== about FrameSummary object")
        temp_frame_summary = traceback.extract_tb(exc_traceback)[0]
        attr_list = ["line", "lineno", "filename", "name"]
        for attr in attr_list:
            print(f"{attr} : ", getattr(temp_frame_summary, attr))

