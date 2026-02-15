---
name: questions-form
description: >
  Present multiple clarifying questions as an interactive Telegram form using
  inline buttons. Use when the agent needs to ask the user 2 or more clarifying
  questions before proceeding with a task, and wants to present them all at once
  in a structured form layout with selectable options and an "Other" free-text
  escape hatch. Triggers when: gathering multi-faceted requirements, onboarding
  flows, preference collection, or any scenario requiring structured
  multi-question input from the user via Telegram.
---

# 问题表单

通过 Telegram 的内联按钮形式展示多个澄清性问题。所有问题会同时显示；用户可以按任意顺序回答，然后提交。

## 使用场景

- 在继续之前，需要用户回答 2 个或更多澄清性问题。
- 问题具有可枚举的选项（并提供可选的自由文本回答选项）。
- 该表单用于 Telegram 频道。

**请勿** 将此模式用于简单的“是/否”问题——只需发送一条包含相应按钮的消息即可。

## 表单协议

### 第 1 步：构建表单

将每个问题内部定义为一个对象：

```
{ id: "type",     text: "What type of project?", options: ["Web App", "Mobile", "API"] }
{ id: "timeline", text: "What is your timeline?", options: ["This week", "This month", "No rush"] }
{ id: "budget",   text: "Budget range?",          options: ["< $1k", "$1k-5k", "$5k-10k", "> $10k"] }
```

初始化内部跟踪状态：

```
form_state = { type: null, timeline: null, budget: null }
awaiting_freetext = null
form_submitted = false
```

### 第 2 步：发送表单介绍信息

发送一条不含按钮的纯文本消息，作为表单的引入：

```json
{
  "action": "send",
  "channel": "telegram",
  "message": "**I have a few questions before we proceed.**\nPlease answer each one by tapping a button, then tap Submit when done."
}
```

### 第 3 步：发送每个问题

对于每个问题，发送一条包含内联按钮的独立消息。将可选选项按 2-3 个按钮的行进行排列。务必将“其他”选项放在最后一行。

**回调数据** 必须遵循以下格式：`form:<question_id>:<value>`

示例：

```json
{
  "action": "send",
  "channel": "telegram",
  "message": "**1. What type of project is this?**",
  "buttons": [
    [
      { "text": "Web App", "callback_data": "form:type:web" },
      { "text": "Mobile", "callback_data": "form:type:mobile" },
      { "text": "API", "callback_data": "form:type:api" }
    ],
    [
      { "text": "Other (type your answer)", "callback_data": "form:type:other" }
    ]
  ]
}
```

```json
{
  "action": "send",
  "channel": "telegram",
  "message": "**2. What is your timeline?**",
  "buttons": [
    [
      { "text": "This week", "callback_data": "form:timeline:this_week" },
      { "text": "This month", "callback_data": "form:timeline:this_month" },
      { "text": "No rush", "callback_data": "form:timeline:no_rush" }
    ],
    [
      { "text": "Other (type your answer)", "callback_data": "form:timeline:other" }
    ]
  ]
}
```

```json
{
  "action": "send",
  "channel": "telegram",
  "message": "**3. Budget range?**",
  "buttons": [
    [
      { "text": "< $1k", "callback_data": "form:budget:lt_1k" },
      { "text": "$1k-5k", "callback_data": "form:budget:1k_5k" }
    ],
    [
      { "text": "$5k-10k", "callback_data": "form:budget:5k_10k" },
      { "text": "> $10k", "callback_data": "form:budget:gt_10k" }
    ],
    [
      { "text": "Other (type your answer)", "callback_data": "form:budget:other" }
    ]
  ]
}
```

### 第 4 步：发送提交/取消按钮

在所有问题都提交后，发送提交或取消的消息：

```json
{
  "action": "send",
  "channel": "telegram",
  "message": "**When you've answered all questions above, tap Submit.**",
  "buttons": [
    [{ "text": "\u2713 Submit All Answers", "callback_data": "form:submit" }],
    [{ "text": "\u2717 Cancel", "callback_data": "form:cancel" }]
  ]
}
```

### 第 5 步：处理回调

当收到以 `form:` 开头的回调时：

**常规选项**（`form:<qid>:<value>`，其中 `value` 不为“其他”）：
- 记录答案：`form_state[qid] = value`
- 回复用户：`收到您的回答 -- <问题标签>：**<选中的选项>**`

**“其他”选项**（`form:<qid>:other`）：
- 发送提示：`请输入 <问题文本> 的答案`
- 设置 `awaiting_freetext = qid`
- 用户的下一条纯文本消息即为他们的自由文本答案
- 记录答案：`form_state[qid] = <用户的文本>`
- 回复用户：`收到您的回答 -- <问题标签>：**<用户的文本>**
- 清除 `awaiting_freetext`

**提交**（`form:submit`）：
- 检查 `form_state` 中是否有未填写的答案
- 如果未完成：发送提示：`您还需要回答：<未回答的问题列表>`
- 如果所有问题都已完成：设置 `form_submitted = true`，并继续处理收集到的答案

**取消**（`form:cancel`）：
- 删除 `form_state` 中的所有数据
- 发送提示：`表单已取消。请告知我您希望如何继续。`

### 第 6 步：使用收集到的答案

表单提交后，可以将这些答案作为结构化数据使用，并据此继续执行后续操作：

```
Collected: { type: "mobile", timeline: "End of March", budget: "1k_5k" }
```

现在，根据这些澄清后的要求继续执行原始任务。

## 更改答案

用户可以在提交前随时点击不同的问题按钮来更改答案。只需覆盖之前的答案并给予确认即可：

`答案已更新 -- <问题标签>：**<新答案>**`

## 回调数据格式规范

- 所有的表单回调都必须使用 `form:` 前缀
- 格式：`form:<question_id>:<value>`
- 问题 ID 应尽量简短（2-8 个字符）——Telegram 对回调数据的长度有限制（64 字节）
- 值也应尽量简短，并使用下划线代替空格
- 代理通过检查收到的消息是否以 `form:` 开头来识别表单回调

## 按钮布局规则

- 每行最多放置 2-3 个按钮，以保证页面显示清晰
- 按钮标签的长度应控制在 20 个字符以内
- 选项标签应使用大写
- “其他”按钮的文本始终为：“其他（请输入您的答案）”
- “其他”按钮始终单独放在最后一行
- 提交按钮包含勾选标记：`"\u2713 提交所有答案"`
- 取消按钮包含 X 标记：`"\u2717 取消"`

## 边缘情况与高级模式

有关以下内容的详细信息，请参阅 [references/form-patterns.md]：
- 处理超时和未完成的表单
- 依赖性问题（只有在问题 A 被回答后才会显示问题 B）
- 选项数量较多（超过 6 个选项）
- 多选问题（切换模式）
- 自由文本的解析
- 恢复中断的表单操作