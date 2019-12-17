# 语法
|关键字|描述|
|---|---|
|$schema|表示该JSON Schema文件遵循的规范|
|title|为该JSON Schema文件提供一个标题|
|description|关于该JSON Schema文件的描述信息|
|type|表示待校验元素的类型（例如，最外层的type表示待校验的是一个JSON对象，内层type分别表示待校验的元素类型为，整数，字符串，数字）|
|properties|定义待校验的JSON对象中，各个key-value对中value的限制条件|
|requiredv|定义待校验的JSON对象中，必须存在的key|
|minimum|用于约束取值范围，表示取值范围应该大于或等于minimum|
|exclusiveMinimum|如果minimum和exclusiveMinimum同时存在，且exclusiveMinimum的值为true，则表示取值范围只能大于minimum
|maximum|用于约束取值范围，表示取值范围应该小于或等于maximum|
|exclusiveMaximum|如果maximum和exclusiveMaximum同时存在，且exclusiveMaximum的值为true，则表示取值范围只能小于maximum|
|multipleOf|用于约束取值，表示取值必须能够被multipleOf所指定的值整除|
|maxLength|字符串类型数据的最大长度|
|minLength|字符串类型数据的最小长度|
|pattern|使用正则表达式约束字符串类型数据|


# 使用方法


```json

{
  "title": "测试",
  "description": "测试",
  "type": "object",
  "properties": {
    "error": {
      "description": "Name of the test",
      "type": "boolean"
    },
    "results": {
      "description": "age of test",
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "_id"
        ]
      }
    }
  },
  "required": [
    "error",
    "results"
  ]
}


```
