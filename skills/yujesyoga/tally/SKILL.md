---
name: tally
version: 1.0.0
description: 通过 API 创建和编辑 Tally 表单。适用于编程方式构建调查问卷、反馈表单或问题表单。支持所有类型的问题，包括文本输入、单选、复选框、评分（通过变通方法实现）等。
---

# Tally Forms API

通过 REST API 可以编程方式创建和编辑 Tally.so 表单。

## 认证

```bash
TALLY_KEY=$(cat ~/.config/tally/api_key)
```

## 端点

| 操作 | 方法 | 端点 |
|--------|--------|----------|
| 列出表单 | GET | `https://api.tally.so/forms` |
| 获取表单 | GET | `https://api.tally.so/forms/{id}` |
| 更新表单 | PATCH | `https://api.tally.so/forms/{id}` |
| 获取提交记录 | GET | `https://api.tally.so/forms/{id}/submissions` |

## 表单结构

Tally 表单由多个 **块（blocks）** 组成。问题需要通过 `groupUuid` 将多个块组合在一起：

```json
{
  "uuid": "q1-title",
  "type": "TITLE",
  "groupUuid": "group-q1",
  "groupType": "QUESTION",
  "payload": {
    "safeHTMLSchema": [["Question text here", [["tag", "span"]]]]
  }
},
{
  "uuid": "q1-input",
  "type": "INPUT_TEXT",
  "groupUuid": "group-q1",
  "groupType": "QUESTION",
  "payload": {"isRequired": true}
}
```

**注意：** 标题（TITLE）块和输入（INPUT）块必须使用相同的 `groupUuid`。

## 块类型

### 结构
- `FORM_TITLE` - 表单标题和提交按钮
- `TEXT` - 段落文本
- `HEADING_1`, `HEADING_2`, `HEADING_3` - 节标题
- `TITLE` - 问题标签（位于 QUESTION 组内）
- `DIVIDER` - 分隔线

### 输入类型
- `INPUT_TEXT` - 短文本输入
- `INPUT_NUMBER` - 数字输入
- `INPUT_EMAIL` - 电子邮件输入
- `INPUT_DATE` - 日期选择器
- `INPUT_PHONE_NUMBER` - 电话号码输入
- `TEXTAREA` - 长文本输入

### 选择类型
- `MULTIPLE_CHOICE_OPTION` - 单选（groupType: MULTIPLE_CHOICE）
- `CHECKBOX` - 多选（groupType: CHECKBOXES）
- `DROPDOWN_OPTION` - 下拉菜单

### 注意：**某些类型无法通过 API 正确显示**
- `RATING` - 评分（星星）无法显示
- `LINEAR_SCALE` - 线性评分量表无法显示

**解决方法：** 使用 `MULTIPLE_CHOICE_OPTION` 并添加星星表情符号来表示评分。

## 示例

### 表单标题
```json
{
  "uuid": "title-001",
  "type": "FORM_TITLE",
  "groupUuid": "group-title",
  "groupType": "FORM_TITLE",
  "payload": {
    "title": "My Survey",
    "button": {"label": "Submit"}
  }
}
```

### 节标题
```json
{
  "uuid": "sec1-head",
  "type": "HEADING_2",
  "groupUuid": "group-sec1",
  "groupType": "TEXT",
  "payload": {
    "safeHTMLSchema": [["📊 Section Title", [["tag", "span"]]]]
  }
}
```

### 文本输入问题
```json
{
  "uuid": "q1-title",
  "type": "TITLE",
  "groupUuid": "group-q1",
  "groupType": "QUESTION",
  "payload": {
    "safeHTMLSchema": [["What is your name?", [["tag", "span"]]]]
  }
},
{
  "uuid": "q1-input",
  "type": "INPUT_TEXT",
  "groupUuid": "group-q1",
  "groupType": "QUESTION",
  "payload": {"isRequired": true}
}
```

### 单选问题
```json
{
  "uuid": "q2-title",
  "type": "TITLE",
  "groupUuid": "group-q2",
  "groupType": "QUESTION",
  "payload": {
    "safeHTMLSchema": [["How did you hear about us?", [["tag", "span"]]]]
  }
},
{
  "uuid": "q2-opt1",
  "type": "MULTIPLE_CHOICE_OPTION",
  "groupUuid": "group-q2",
  "groupType": "MULTIPLE_CHOICE",
  "payload": {"isRequired": true, "index": 0, "isFirst": true, "isLast": false, "text": "Social media"}
},
{
  "uuid": "q2-opt2",
  "type": "MULTIPLE_CHOICE_OPTION",
  "groupUuid": "group-q2",
  "groupType": "MULTIPLE_CHOICE",
  "payload": {"isRequired": true, "index": 1, "isFirst": false, "isLast": true, "text": "Friend referral"}
}
```

### 多选问题（可有多个答案）
```json
{
  "uuid": "q3-title",
  "type": "TITLE",
  "groupUuid": "group-q3",
  "groupType": "QUESTION",
  "payload": {
    "safeHTMLSchema": [["What features interest you?", [["tag", "span"]]]]
  }
},
{
  "uuid": "q3-cb1",
  "type": "CHECKBOX",
  "groupUuid": "group-q3",
  "groupType": "CHECKBOXES",
  "payload": {"index": 0, "isFirst": true, "isLast": false, "text": "Feature A"}
},
{
  "uuid": "q3-cb2",
  "type": "CHECKBOX",
  "groupUuid": "group-q3",
  "groupType": "CHECKBOXES",
  "payload": {"index": 1, "isFirst": false, "isLast": true, "text": "Feature B"}
}
```

### 评分量表（使用星星表情符号替代）
```json
{
  "uuid": "q4-title",
  "type": "TITLE",
  "groupUuid": "group-q4",
  "groupType": "QUESTION",
  "payload": {
    "safeHTMLSchema": [["How would you rate our service?", [["tag", "span"]]]]
  }
},
{
  "uuid": "q4-opt1",
  "type": "MULTIPLE_CHOICE_OPTION",
  "groupUuid": "group-q4",
  "groupType": "MULTIPLE_CHOICE",
  "payload": {"isRequired": true, "index": 0, "isFirst": true, "isLast": false, "text": "⭐ Poor"}
},
{
  "uuid": "q4-opt2",
  "type": "MULTIPLE_CHOICE_OPTION",
  "groupUuid": "group-q4",
  "groupType": "MULTIPLE_CHOICE",
  "payload": {"isRequired": true, "index": 1, "isFirst": false, "isLast": false, "text": "⭐⭐ Fair"}
},
{
  "uuid": "q4-opt3",
  "type": "MULTIPLE_CHOICE_OPTION",
  "groupUuid": "group-q4",
  "groupType": "MULTIPLE_CHOICE",
  "payload": {"isRequired": true, "index": 2, "isFirst": false, "isLast": false, "text": "⭐⭐⭐ Good"}
},
{
  "uuid": "q4-opt4",
  "type": "MULTIPLE_CHOICE_OPTION",
  "groupUuid": "group-q4",
  "groupType": "MULTIPLE_CHOICE",
  "payload": {"isRequired": true, "index": 3, "isFirst": false, "isLast": false, "text": "⭐⭐⭐⭐ Very good"}
},
{
  "uuid": "q4-opt5",
  "type": "MULTIPLE_CHOICE_OPTION",
  "groupUuid": "group-q4",
  "groupType": "MULTIPLE_CHOICE",
  "payload": {"isRequired": true, "index": 4, "isFirst": false, "isLast": true, "text": "⭐⭐⭐⭐⭐ Excellent"}
}
```

## 更新表单的命令

```bash
TALLY_KEY=$(cat ~/.config/tally/api_key)

# Backup first
curl -s "https://api.tally.so/forms/{ID}" \
  -H "Authorization: Bearer $TALLY_KEY" > /tmp/backup.json

# Update
curl -s "https://api.tally.so/forms/{ID}" \
  -X PATCH \
  -H "Authorization: Bearer $TALLY_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/form.json

# Verify
curl -s "https://api.tally.so/forms/{ID}" \
  -H "Authorization: Bearer $TALLY_KEY" | jq '.blocks | length'
```

## 最佳实践
1. **修改表单前务必备份**
2. **使用描述性的 UUID**（例如：q1-title, q1-input, sec1-head）
3. **节标题**：使用小写字母，并加上表情符号前缀（例如：📊 一般反馈）
4. **对于评分**：使用 `MULTIPLE_CHOICE` 并添加星星表情符号（⭐）代替 `RATING` 类型
5. **更新后进行验证**：确认块的数量与预期一致