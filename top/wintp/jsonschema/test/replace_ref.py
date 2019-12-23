import json


def replace_all(my_schema):
    my_schema_str = str(my_schema)
    print(my_schema_str)

    my_schema_str.index(my_schema_str,0,len(my_schema_str))

    if "${" in my_schema_str:
        print(True)
        pass


if __name__ == '__main__':
    with open('../schema/MySchema.json', encoding='utf8') as f:
        my_schema = json.load(f)

    replace_all(my_schema)
