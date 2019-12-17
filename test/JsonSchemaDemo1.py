# 导入验证器
import json

from jsonschema import validate, draft7_format_checker, SchemaError, ValidationError

if __name__ == '__main__':
    with open('../schema/MySchema.json', encoding='utf8') as f:
        my_schema = json.load(f)

    # json数据：
    with open('../data/cece.json', encoding='utf8') as f:
        json_data = json.load(f)

    # error_list = check_type(my_schema, json_data)
    # print(error_list)

    # 验证：
    try:
        validate(instance=json_data, schema=my_schema, format_checker=draft7_format_checker)
        # Draft7Validator.format_checker
    except SchemaError as serr:
        print("schema 错误 【%s】 \nschema错误" % str(serr))
    except ValidationError as verr:
        print("数据 错误 【%s】 \n数据错误" % str(verr))
