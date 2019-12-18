import json

from dist_.CheckDataUti import check_data

if __name__ == '__main__':
    with open('../schema/MySchema.json', encoding='utf8') as f:
        my_schema = json.load(f)

    # json数据：
    with open('../data/cece.json', encoding='utf8') as f:
        json_data = json.load(f)

    check_data(my_schema, json_data)
    # print(ERR_LIST)
