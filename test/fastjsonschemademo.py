# 导入验证器
import json
import fastjsonschema

# 读取schema
with open('../schema/oneof-schema.json', encoding='utf8') as f:
    my_schema = json.load(f)

# json数据：
with open('../data/test.json', encoding='utf8') as f:
    json_data = json.load(f)

# 验证：
fastjsonschema.validate(my_schema, json_data)
