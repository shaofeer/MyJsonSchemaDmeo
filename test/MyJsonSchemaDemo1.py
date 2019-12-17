import json
import re
import time

# email 正则表达式
EMAIL_REGEX = "^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
# URL 正则表达式
URL_REGEX = "^[a-zA-z]+://[^\s]*$"
# PHONE 正则表达式
PHONE_REGEX = "^([1][3,4,5,6,7,8,9])\d{9}$"
# 身份证 正则表达式
ID_CARD_REGEX = "^((\d{18})|([0-9x]{18})|([0-9X]{18}))$"
# 邮政编码 正则表达式
ZIP_CODE_REGEX = "^[1-9]\d{5}(?!\d)$"
# IP 地址 正则表达式
IP_REGEX = "^\d+\.\d+\.\d+\.\d+$"
# 正整数
INTEGER_REGEX = "^[1-9]\d*$"

ERR_LIST = []


# 校验每一层的type
def log_error(msg, data, schema, is_any_of=False):
    """
    打印错误日志
    """
    err_log = "%s,数据:【%s】,校验规则: %s" % (str(msg), str(data) + " type of " + str(type(data).__name__), str(schema))
    ERR_LIST.append(err_log)
    if not is_any_of:
        print("=================================================")
        print(err_log)
        print("=================================================")


def check_object(data, schema, is_any_of):
    """
    校验对象格式
    【 properties、required、minProperties、maxProperties、patternProperties、additionalProperties 】
    """
    if type(data) != dict:
        log_error("当前校验的json不是一个对象格式", data, schema, is_any_of)
    else:
        # 获取当前校验数据的所有key
        keys = dict.keys(data)

        # 处理必需值
        if "required" in schema:
            required_schema = schema['required']
            for schema_key in required_schema:
                if schema_key not in keys:
                    log_error("字段【%s】必填" % schema_key, data, schema, is_any_of)

        # 处理最小key和最大key
        if "minProperties" in schema:
            min_properties = schema['minProperties']
            if len(keys) < min_properties:
                log_error("校验数据的key个数小于【%s】" % str(min_properties), data, schema, is_any_of)

        if "maxProperties" in schema:
            max_properties = schema['maxProperties']
            if len(keys) > max_properties:
                log_error("校验数据的key个数大于【%s】" % str(max_properties), data, schema, is_any_of)

        # 处理具体的key
        if "properties" in schema:
            # 处理 properties
            properties_schema = schema['properties']
            schema_keys = dict.keys(properties_schema)
            for data_key in schema_keys:
                if data_key in data:
                    check_type(properties_schema[data_key], data[data_key])

        # 处理满足正则表达式的key
        if "patternProperties" in schema:
            # 处理 properties
            pattern_properties = schema['patternProperties']
            schema_keys = dict.keys(pattern_properties)

            # 循环所有正则表达式的key
            for schema_key in schema_keys:
                # 循环当前待校验的数据key
                for data_key in keys:
                    # 仅仅处理满足正则表达式的key数据
                    if re.match(schema_key, data_key):
                        check_type(pattern_properties[schema_key], data[data_key])


def check_array(data, schema, is_any_of):
    """
    校验数组格式
    【 items、additionalItems、minItems、maxItems、uniqueItems 】
    """
    if type(data) != list:
        log_error("当前校验的json不是数组格式", data, schema, is_any_of)
    else:
        # minItems、maxItems
        # 判断最小值
        if "minItems" in schema:
            min_items = schema['minItems']
            if len(data) < min_items:
                log_error("当前校验的数据数组长度小于【%s】" % str(min_items), data, schema, is_any_of)

        # 判断最大值
        if "maxItems" in schema:
            max_properties = schema['maxItems']
            if len(data) > max_properties:
                log_error("当前校验的数据数组长度大于【%s】" % str(max_properties), data, schema, is_any_of)

        # uniqueItems true 数组元素不能重复
        if "uniqueItems" in schema:
            unique_items_schema = schema['uniqueItems']

            if unique_items_schema:
                # 数组元素不能重复
                try:
                    if len(set(data)) != len(data):
                        log_error("当前校验的数据数组元素不能重复", data, schema, is_any_of)
                except TypeError:
                    # 存在数组内部元素是dict格式
                    pass
        # 判断每一个items
        if "items" in schema:
            items_schema = schema["items"]
            # 判断items_schema 是数组还是对象
            if type(items_schema) is list:
                # 如果是数组 每一个item都是一个jsonSchema 索引对应的数组内索引的格式
                index = 0
                for item_sc in items_schema:
                    check_type(item_sc, data[index])
                    index += 1

                # additionalItems该关键字只有在items是数组的时候才会有效
                # additionalItems 除了上述规定之外的数据必需符合指定的规则
                if "additionalItems" in schema:
                    additional_items_schema = schema['additionalItems']

                    for i in range(index, len(data)):
                        check_type(additional_items_schema, data[i])

            # items如果是对象  当前schema规范了数组内所有元素的格式
            elif type(items_schema) is dict:
                for item_data in data:
                    check_type(items_schema, item_data)


def check_number(data, schema, is_any_of):
    """
    校验数字类型
    """
    if type(data) not in (int, float):
        log_error("当前校验的json不是一个数字格式", data, schema)

    else:
        # 判断最大值 maximum 如果exclusiveMaximum该关键字是True 包含本身
        if "maximum" in schema:
            maximum_schema = schema['maximum']
            if 'exclusiveMaximum' in schema and schema['exclusiveMaximum']:
                if data >= maximum_schema:
                    log_error("当前校验的数据大于等于【%s】" % maximum_schema, data, schema, is_any_of)
            else:
                if data > maximum_schema:
                    log_error("当前校验的数据大于【%s】" % maximum_schema, data, schema, is_any_of)

        # minimum、exclusiveMinimum
        if "minimum" in schema:
            minimum_schema = schema['minimum']
            if 'exclusiveMinimum' in schema and schema['exclusiveMinimum']:
                if data <= minimum_schema:
                    log_error("当前校验的数据小于等于【%s】" % minimum_schema, data, schema, is_any_of)

            else:
                if data < minimum_schema:
                    log_error("当前校验的数据小于【%s】" % minimum_schema, data, schema, is_any_of)

        # multipleOf    整除
        if "multipleOf" in schema:
            multiple_of_schema = schema['multipleOf']
            if not data % multiple_of_schema == 0:
                log_error("当前校验的数据不能被%s整除" % multiple_of_schema, data, schema, is_any_of)


def check_str(data, schema, is_any_of):
    """
    校验字符串类型
    涉及的关键字 【maxLength、minLength、pattern、format】
    """
    if type(data) != str:
        log_error("当前校验的数据不是一个字符串格式", data, schema, is_any_of)
    else:
        # maxLength
        if "maxLength" in schema:
            max_length_schema = schema['maxLength']
            if len(data) > max_length_schema:
                log_error("当前校验的数据长度大于%d" % max_length_schema, data, schema, is_any_of)

        # minLength
        if "minLength" in schema:
            min_length_schema = schema['minLength']
            if len(data) < min_length_schema:
                log_error("当前校验的数据长度小于%d" % min_length_schema, data, schema, is_any_of)

        # pattern
        if "pattern" in schema:
            pattern_schema = schema['pattern']
            if not re.match(pattern_schema, data):
                log_error("当前校验的数据不符合正则表达式规则【%s】" % pattern_schema, data, schema, is_any_of)
        # format
        if 'format' in schema:
            format_schema = schema['format']

            if format_schema == 'email' and not re.match(EMAIL_REGEX, data):
                log_error("当前校验的数据不是正确的邮箱格式", data, schema, is_any_of)

            elif format_schema == 'phone' and not re.match(PHONE_REGEX, data):
                log_error("当前校验的数据不是正确的手机号码格式", data, schema, is_any_of)

            elif format_schema == 'hostname' and not re.match(IP_REGEX, data):
                log_error("当前校验的数据不是正确的IP地址格式", data, schema, is_any_of)

            elif format_schema == 'idCard' and not re.match(ID_CARD_REGEX, data):
                log_error("当前校验的数据不是正确的身份证格式", data, schema, is_any_of)

            elif format_schema == 'date':
                format_patten = '%Y-%m-%d'
                if 'format_patten' in schema:
                    format_patten = schema['format_patten']
                try:
                    time.strptime(data, format_patten)
                except ValueError:
                    log_error("当前校验的数据不是正确的日期格式格式【%s】" % format_patten, data, schema, is_any_of)


def check_common(schema, data):
    """
    校验通用的
    """
    if "enum" in schema:
        enum_schema = schema['enum']
        if data not in enum_schema:
            log_error("当前校验的数据值不存在【%s】" % str(enum_schema), data, schema)

    if "const" in schema:
        const_schema = schema['const']
        if data == const_schema:
            log_error("当前校验数据值不等于【%s】" % str(const_schema), data, schema)

    if "allOf" in schema:
        all_of_schema = schema['allOf']
        for item_schema in all_of_schema:
            check_type(item_schema, data)
    if "anyOf" in schema:
        any_of_schema = schema['anyOf']

        begin_len = len(ERR_LIST)

        for item_schema in any_of_schema:
            check_type(item_schema, data, True)

        end_len = len(ERR_LIST)

        if end_len - begin_len == len(any_of_schema):
            log_error("")

    pass


def check_type(schema, data, is_any_of=False):
    check_common(schema, data)

    # type 默认为string
    type_name = schema['type'] if "type" in schema else 'string'

    if type_name == 'object':
        check_object(data, schema, is_any_of)
    elif type_name == 'array':
        check_array(data, schema, is_any_of)
    elif type_name in ['integer', 'number']:
        check_number(data, schema, is_any_of)
    elif type_name == 'string':
        check_str(data, schema, is_any_of)
    # type是布尔类型
    elif type_name == 'boolean':
        if type(data) != bool:
            log_error("当前校验的数据不是一个boolean格式", data, schema, is_any_of)


if __name__ == '__main__':
    with open('../schema/MySchema.json', encoding='utf8') as f:
        my_schema = json.load(f)

    # json数据：
    with open('../data/cece.json', encoding='utf8') as f:
        json_data = json.load(f)

    check_type(my_schema, json_data)
    # print(ERR_LIST)

# 验证：
# try:
#     validate(instance=json_data, schema=my_schema, format_checker=draft7_format_checker)
#     # Draft7Validator.format_checker
# except SchemaError as serr:
#     print("schema 错误 【%s】 \nschema错误" % str(serr))
# except ValidationError as verr:
#     print("数据 错误 【%s】 \n数据错误" % str(verr))
