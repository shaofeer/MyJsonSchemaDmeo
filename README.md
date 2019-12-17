# 本文目录
   * [JsonSchmea用法](#jsonschmea用法)
      * [简介](#简介)
      * [关键字及其描述](#关键字及其描述)
      * [JSON Schema关键字详解](#json-schema关键字详解)
      * [type的常用取值](#type的常用取值)
      * [关键字详解](#关键字详解)
         * [最外层type为object时](#最外层type为object时)
         * [最外层type为array时](#最外层type为array时)
         * [当type的值为integer或者number时](#当type的值为integer或者number时)
         * [当type取值为string时](#当type取值为string时)
         * [全类型可用](#全类型可用)
         * [type关键字](#type关键字)
         * [dependencies关键字](#dependencies关键字)
         * [$ref关键字](#ref关键字)
         * [if-then-else 关键字](#if-then-else-关键字)

# JsonSchmea用法

## 简介
JSON Schema是基于JSON格式，用于定义JSON数据结构以及校验JSON数据内容。
JSON Schema官网地址：[http://json-schema.org/](http://json-schema.org/)

> 个人观点：JsonSchema类似于xml的schema和DTD的作用，主要是用来规范json的格式。


## 关键字及其描述

|关键字|描述|
|-|-|
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


## JSON Schema关键字详解

JsonSchema代码：
```json

{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "TestInfo",
    "description": "some information about test",
    "type": "object",
    "properties": {
        "name": {
            "description": "Name of the test",
            "type": "string"
        },
        "age": {
            "description": "age of test",
            "type": "integer"
        }
    },
    "required": [
        "name"
    ]
}
```
详细解释：
- $schema:用于指定JSONSchema的版本信息，该值由官方提供，不可乱写。该关键字可以省略。
- title：当前schema的标题信息。可以省略
- description：当前节点的描述
- type：当前节点的类型，最外层type代表json的最外层是什么样的类型。例如上方的例子中，符合该JsonSchema的json数据必需是一个JsonObject而不能是一个JsonArray
- properties：代表当前节点的子节点信息。例如上方的例子中，符合该JsonSchema的json数据的信息可以存在“name”节点和“age”节点。按照上面的配置required信息来看，name是必需要有的，而age是非必需的。
- required： 是一个数组类型，代表当前节点下必需的节点key。例如上方例子中，规定了json的格式必需要有name节点。

符合上述JsonSchema的json数据如下：

第一种（不含有age节点，只含有name一个节点或者name及其若干个节点）：
```json
{
  "name": "upuptop"
}

```
第二种（含有age节点，age节点的值必需为integer类型）：
```json
{
  "name": "upuptop",
  "age": 123,
  "create_time": "2019-12-12"
}
```

## type的常用取值

|  type取值  | 	对应的python数据类型 |
| ---------- | -------------------- |
| object     | 	Object              |
| array	     | List                 |
| integer    | 	int                |
| number	 | float或int           |
| null       | 	None                |
| boolean    | Boolean              |
| string	 | String               |


## 关键字详解
### 最外层type为object时

- properties
>该关键字的值是一个对象。

用于指定JSON对象中的各种不同key应该满足的校验逻辑，如果待校验JSON对象中所有值都能够通过该关键字值中定义的对应key的校验逻辑，
**每个key对应的值，都是一个JSON Schema**，则待校验JSON对象通过校验。
从这里，我们可以看到，只要待校验JSON对象的所有key分别都通过对应的JSON Schema的校验检测，这个对象才算是通过校验。

```json

"properties": {
    "name": {
      "description": "姓名必须由2-3个字组成",
      "type": "string",
      "maxLength": 3,
      "minLength": 2
    },
    "age": {
      "description": "年龄必须大于18岁。并且不能超过60岁",
      "type": "integer",
      "minimum": 18,
      "maximum": 60
    }
  }

```

解释：**每个key对应的值，都是一个JSON Schema:**例如上方例子中，每一个key(name/age)对应的值都是一个JSONSchema，JSONSchema中的关键字及描述都可以使用。

- required
> 该关键字的值是一个数组，而数组中的元素必须是字符串，而且必须是唯一的。

该关键字限制了JSON对象中必须包含哪些一级key。
如果一个JSON对象中含有required关键字所指定的所有一级key，则该JSON对象能够通过校验。

```json
"required": ["id","name","price"]
```

- minProperties、maxProperties
> 这两个关键字的值都是非负整数。规定最多节点个数与最少节点个数。

指定了待校验JSON对象中一级key的个数限制，minProperties指定了待校验JSON对象可以接受的最少一级key的个数，而maxProperties指定了待校验JSON对象可以接受的最多一级key的个数。

另外，需要注意的是，省略minProperties关键字和该关键字的值为0，具有相同效果。而，如果省略maxProperties关键字则表示对一级key的最大个数没有限制。例如，如果限制一个JSON对象的一级key的最大个数为5，最小个数为1，则JSON Schema如下：

```json
"minProperties": 1,
"maxProperties": 5
```

- patternProperties
> 该关键字的值是一个对象，该JSON对象的每一个一级key都是一个正则表达式，value都是一个JSON Schema。
> 指定符合正则表达式的key的规则。
>只有待校验JSON对象中的一级key，通过与之匹配的patternProperties中的一级正则表达式，
>对应的JSON Schema的校验，才算通过校验。例如，如果patternProperties对应的值如下

```json
"patternProperties": {
        "^a": {
            "type": "number"
        },
        "^b": {
            "type": "string"
        }
}
```
上面的JSON Schema表示，待校验JSON对象中，所有以a开头的一级key的value都必须是number，所有以b开头的一级key的value都必须是string。

- additionalProperties
> 该关键字的值是一个JSON Schema。

如果待校验JSON对象中存在，既没有在properties中被定义，又没有在patternProperties中被定义，那么这些一级key必须通过additionalProperties的校验。



### 最外层type为array时
- items:
>该关键字的值是一个有效的JSON Schema或者一组有效的JSON Schema。

当该关键字的值是一个有效的JSON Schema时，只有待校验JSON数组中的所有元素均通过校验，整个数组才算通过校验。例如，如果items关键字的具体定义如下：
```json
{
   "type": "array",
   "items": {
     "type": "string",
     "minLength": 5 
   }
}
```
上面的JSON Schema的意思是，待校验JSON数组的元素都是string类型，且最小可接受长度是5。那么下面这个JSON数组明显是符合要求的，具体内容如下：
```json
["myhome", "green"]
```
那么下面这个JSON数据则是不符合要求，因为第一个元素的长度小于5，具体内容如下：

```json
["home", "green"]
```
以上对于items的介绍是对于所有元素来规定的。

**注意**
下面对items的详解，趋向于每一个元素的规则。

这里需要注意的是，如果items定义的有效的JSON Schema的数量和待校验JSON数组中元素的数量不一致，那么就要采用**“取小原则”**。即，如果items定义了3个JSON Schema，但是待校验JSON数组只有2个元素，这时，只要待校验JSON数组的前两个元素能够分别通过items中的前两个JSON Schema的校验，那么，我们认为待校验JSON数组通过了校验。而，如果待校验JSON数组有4个元素，这时，只要待校验JSON数组的前三个元素能够通过items中对应的JSON Schema的校验，我们就认为待校验JSON数组通过了校验。


例如，如果items的值如下：

```json

{
    "type": "array",
    "items": [
        {
            "type": "string",
            "minLength": 5
        },
        {
            "type": "number",
            "minimum": 10
        },
        {
            "type": "string"
        }
    ]
}
```
上面的JSON Schema指出了待校验JSON数组应该满足的条件，数组的第一个元素是string类型，且最小可接受长度为5，数组的第二个元素是number类型，最小可接受的值为10，数组的第三个元素是string类型。那么下面这两个JSON数组明显是符合要求的，具体内容如下：

```
["green", 10, "good"]
["helloworld", 11]
```
下面这两个JSON数组却是不符合要求的，具体内容如下：

```
["green", 9, "good"]
["good", 12]
```

- additionalItems
> 该关键字的值是一个有效的JSON Schema。主要规定除了items内部规定的元素之外的元素规则。只有在items是一个schema数组的时候才可以使用。


需要**注意**的是，该关键字只有在items关键字的值为一组有效的JSON Schema的时候，才可以使用，用于规定超出items中JSON Schema总数量之外的待校验JSON数组中的剩余的元素应该满足的校验逻辑。当然了，只有这些剩余的所有元素都满足additionalItems的要求时，待校验JSON数组才算通过校验。

其实，你可以这么理解，当items的值为一组有效的JOSN Schema的时候，一般可以和additionalItems关键字组合使用，items用于规定对应位置上应该满足的校验逻辑，而additionalItems用于规定超出items校验范围的所有剩余元素应该满足的条件。如果二者同时存在，那么只有待校验JSON数组同时通过二者的校验，才算真正地通过校验。

另外，需要注意的是，如果items只是一个有效的JSON Schema，那么就不能使用additionalItems，原因也很简单，因为items为一个有效的JSON Schema的时候，其规定了待校验JSON数组所有元素应该满足的校验逻辑。additionalItems已经没有用武之地了。

如果一个additionalItems的值如下：
```json

{
    "type": "array",
    "items": [
        {
            "type": "string",
            "minLength": 5
        },
        {
            "type": "number",
            "minimum": 10
        }
    ],
    "additionalItems": {
        "type": "string",
        "minLength": 2
    }
}
```

上面的JSON Schema的意思是，待校验JSON数组第一个元素是string类型，且可接受的最短长度为5个字符，第二个元素是number类型，且可接受的最小值为10，剩余的其他元素是string类型，且可接受的最短长度为2。那么，下面三个JSON数组是能够通过校验的，具体内容如下：
```

["green", 10, "good"]
["green", 11]
["green", 10, "good", "ok"]
```
下面JSON数组是无法通过校验的，具体内容如下：
```

["green", 10, "a"]
["green", 10, "ok", 2]
```



- minItems、maxItems
> 这两个关键字的值都是非负整数。
>指定了待校验JSON数组中元素的个数限制，minItems指定了待校验JSON数组可以接受的最少元素个数，而maxItems指定了待校验JSON数组可以接受的最多元素个数。

另外，需要注意的是，省略minItems关键字和该关键字的值为0，具有相同效果。而，如果省略maxItems关键字则表示对元素的最大个数没有限制。

例如，如果限制一个JSON数组的元素的最大个数为5，最小个数为1，则JSON Schema如下：

```
"minItems": 1,
"maxItems": 5
```


- uniqueItems
> 该关键字的值是一个布尔值，即boolean（true、false）。

当该关键字的值为true时，只有待校验JSON数组中的所有元素都具有**唯一性**时，才能通过校验。当该关键字的值为false时，任何待校验JSON数组都能通过校验。
另外，需要注意的是，省略该关键字和该关键字的值为false时，具有相同的效果。例如：

```json
"uniqueItems": true
```


### 当type的值为integer或者number时

> integer和number的区别，integer相当于python中的int类型，而number相当于python中的int或float类型

- multipleOf
> 该关键字的值是一个大于0的number，即可以是大于0的int，也可以是大于0的float。只有待校验的值能够被该关键字的值**整除**，才算通过校验。


如果含有该关键字的JSON Schema如下：
```json

{
    "type": "integer",
    "multipleOf": 2
}
```
> 那么，2、4、6都是可以通过校验的，但是，3、5、7都是无法通过校验的，当然了，2.0、4.0也是无法通过校验的，但是，并不是因为multipleOf关键字，而是因为type关键字。

如果含有multipleOf关键字的JSON Schema如下：

```json
{
    "type": "number",
    "multipleOf": 2.0
}
```

> 那么，2、2.0、4、4.0都是可以通过校验的，但是，3、3.0、3、3.0都是无法通过校验的。

- maximum 、exclusiveMaximum

> `maximum`该关键字的值是一个number，即可以是int，也可以是float。该关键字规定了待校验元素可以通过校验的最大值。即传入的值必须小于maximum。
> `exclusiveMaximum`该关键字和`maximum`一样，规定了待校验元素可以通过校验的最大值，不同的是待校验元素可以等于exclusiveMaximum指定的值。即比maximum多了一个他自身这个边界值.

```
{
    "type": "number",
#  设定 maximum 为12.3 则传入值必须小于12.3
#    "maximum": 12.3,
#  设定 exclusiveMaximum为12.3 则传入值是小于等于12.3
    "exclusiveMaximum": 12.3
}

```

- minimum、exclusiveMinimum
> `minimum`、`exclusiveMinimum`关键字的用法和含义与`maximum`、`exclusiveMaximum`相似。唯一的区别在于，一个约束了待校验元素的最小值，一个约束了待校验元素的最大值。

### 当type取值为string时


- maxLength
>该关键字的值是一个非负整数。该关键字规定了待校验JSON元素可以通过校验的最大长度，即待校验JSON元素的最大长度必须小于或者等于该关键字的值。


- minLength
>该关键字的值是一个非负整数。该关键字规定了待校验JSON元素可以通过校验的最小长度，即待校验JSON元素的最小长度必须大于或者等于该关键字的值。

- pattern
> 该关键字的值是一个正则表达式。只有待校验JSON元素符合该关键字指定的正则表达式，才算通过校验。

- format
>该关键字的值可以是以下取值：`date`、`date-time`（时间格式）、`email`（邮件格式）、`hostname`（网站地址格式）、`ipv4`、`ipv6`、`uri`等等。

```

{
    "type": "string",
    "format": "email"
}
```
使用format关键字时，**在实例化validator时必须给它传`format_checker`参数,fromat_checker参数的值即使各种版本的JSON模式规范的验证器类**，如：

[Draft7Validator](https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft7Validator)
[Draft6Validator](https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft6Validator)
[Draft4Validator](https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft4Validator)



当你实例化validator时,如果没有给它传format_checker参数, jsonschema是不会自动校验schema中的format关键字的.因此,你需要做以下步骤:
1.额外导入JSON Schema某个版本的模式规范如：from jsonschema import draft7_format_checker
2.实例化validator时传入：validate(instance=json_data, schema=my_schema, format_checker=draft7_format_checker)


### 全类型可用


- enum
> 该关键字的值是一个数组，该数组至少要有一个元素，且数组内的每一个元素都是唯一的。
> 如果待校验的JSON元素和数组中的某一个元素相同，则通过校验。否则，无法通过校验。

**注意：**该数组中的元素值可以是任何值，包括null。省略该关键字则表示无须对待校验元素进行该项校验。例如：
```json

{
    "type": "number",
    "enum": [2, 3, null, "hello"]
}
```

- const
> 该关键字的值可以是任何值，包括null。如果待校验的JSON元素的值和该关键字指定的值相同，则通过校验。否则，无法通过校验。


- allOf
>该关键字的值是一个非空数组，数组里面的每个元素都必须是一个有效的JSON Schema。
>只有待校验JSON元素通过数组中**所有的**JSON Schema校验，才算真正通过校验。

- anyOf
>该关键字的值是一个非空数组，数组里面的每个元素都必须是一个有效的JSON Schema。
>如果待校验JSON元素能够通过数组中的**任何一个**~~~~JSON Schema校验，就算通过校验。

- oneOf
>该关键字的值是一个非空数组，数组里面的每个元素都必须是一个有效的JSON Schema。
>如果待校验JSON元素**能且只能**通过数组中的**某一个**JSON Schema校验，才算真正通过校验。**不能通过任何一个校验和能通过两个及以上的校验**，都**不算真正**通过校验。

- not
>该关键字的值是一个JSON Schema。只有待校验JSON元素**不能通过**该关键字指定的JSON Schema校验的时候，待校验元素才算通过校验。

- default
>该关键字的值是没有任何要求的。该关键字常常用来指定待校验JSON元素的默认值，当然，这个默认值最好是符合要求的，即能够通过相应的JSON Schema的校验。
>另外，需要注意的是，该关键字除了**提示作用**外，并不会产生任何实质性的影响。

### type关键字
>需要特别注意的是，type关键字的值可以是一个string，也可以是一个数组。
>如果type的值是一个string，则其值只能是以下几种：null、boolean、object、array、number、string、integer。
>如果type的值是一个数组，则数组中的元素都必须是string，且其取值依旧被限定为以上几种。**只要带校验JSON元素是其中的一种**，则通过校验。



**注意，**以上JSON Schema只是为了展示部分关键字的用法，可能和实际应用略有不同。

### dependencies关键字
> 依赖关系



```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  
  "properties": {
  },
  "dependencies": {
    "age": [
      "name"
    ]
  },
 
}

```
> 上述schema表示，age依赖于name，如果age出现，name必须出现


### $ref关键字

使用该关键字可以引用一个规范

```json

"warehouseLocation": {
      "description": "Coordinates of the warehouse where the product is located.",
      "$ref": "https://example.com/geographical-location.schema.json"
    }

```

### if-then-else 关键字



```json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "foo": {
      "type": "string"
    },
    "bar": {
      "type": "string"
    }
  },
  "if": {
    "properties": {
      "foo": {
        "enum": [
          "bar",
          "123"
        ]
      }
    },
    "required": [
      "foo"
    ]
  },
  "then": {
    "required": [
      "bar"
    ]
  },
  "else": {
    "required": [
      "cc"
    ]
  }
}


```

符合上述规则的json（最简单的两种方式）：
```json
{
  "foo": "bar22",
  "cc": 123
}


{
  "foo": "bar",
  "bar": "123"
}

```

概述：

```
if条件为：key为foo的值是bar或者123 返回true，否则返回false
if返回true执行then：
    then的规则，bar必须存在
if返回false执行else
    else规则，cc必须存在
```



>官方的参考文档如下：
>[http://json-schema.org/latest/json-schema-validation.html](http://json-schema.org/latest/json-schema-validation.html)
>[https://json-schema.org/implementations.html](https://json-schema.org/implementations.html)

> 本文参考：[https://www.cnblogs.com/ChangAn223/articles/11234348.htm](https://www.cnblogs.com/ChangAn223/articles/11234348.htm)


<div style="width: 96px;height: 96px;float: right">
<a href='https://github.com/upuptop/MyJsonSchemaDmeo#jsonschmea%E7%94%A8%E6%B3%95'><img width='96' height='96' style='float:right' src='./img/top.png'></a>
</div>



# 本文目录
   * [JsonSchmea用法](#jsonschmea用法)
      * [简介](#简介)
      * [关键字及其描述](#关键字及其描述)
      * [JSON Schema关键字详解](#json-schema关键字详解)
      * [type的常用取值](#type的常用取值)
      * [关键字详解](#关键字详解)
         * [最外层type为object时](#最外层type为object时)
         * [最外层type为array时](#最外层type为array时)
         * [当type的值为integer或者number时](#当type的值为integer或者number时)
         * [当type取值为string时](#当type取值为string时)
         * [全类型可用](#全类型可用)
         * [type关键字](#type关键字)
         * [dependencies关键字](#dependencies关键字)
         * [$ref关键字](#ref关键字)
         * [if-then-else 关键字](#if-then-else-关键字)














