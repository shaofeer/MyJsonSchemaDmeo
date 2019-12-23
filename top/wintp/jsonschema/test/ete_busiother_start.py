import json

from top.wintp.jsonschema.utils.CheckDataUtil import check_data

if __name__ == '__main__':
    with open('../schema/ete_busiother_schema.json', encoding='utf8') as f:
        my_schema = json.load(f)

    # json数据：
    with open('../data/ete_busiother_schema.json', encoding='utf8') as f:
        arr = f.readlines()

    for item in arr:
        json_data = json.loads(item)

        check_data(my_schema, json_data)
    # print(ERR_LIST)
