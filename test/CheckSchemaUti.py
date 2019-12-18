import json
import re
import time

# 正整数
INTEGER_REGEX = "^[1-9]\d*$"

ERR_LIST = []


def log_error(msg, data, schema, is_common=False):
    """
    打印错误日志
    """
    err_log = "%s,数据:【%s】,校验规则: %s" % (str(msg), str(data) + " type of " + str(type(data).__name__), str(schema))

    ERR_LIST.append(err_log)
    print("=================================================")
    print(err_log)
    print("=================================================")


def check_schema(schema):
    # 关键字判断

    pass


if __name__ == '__main__':
    with open('../schema/MySchema.json', encoding='utf8') as f:
        my_schema = json.load(f)

    check_schema(schema=my_schema)
