---
name: confirm-form
description: 生成结构化的确认表单，以收集用户对多个问题的反馈。适用于需要用户审核的工作、需要批量确认多个问题的情况，或者当用户需要在详细上下文中选择选项时。触发条件包括：审核、确认、批量问题处理、多选题处理，以及需要用户对多个项目进行输入的情况。
---

# 确认表单

生成用于用户确认的HTML表单，将其上传到GitHub Gist，并解析用户的回复。

## 快速入门

### 1. 准备问题数据（JSON格式）

```json
[
  {
    "title": "Question title",
    "context": "Background: what I was working on",
    "uncertainty": "What specifically I cannot decide alone",
    "findings": [
      { "content": "Finding 1", "source": "Source A" },
      { "content": "Finding 2", "source": "Source B" }
    ],
    "judgment": "My recommendation and reasoning",
    "options": [
      { "label": "Option A", "basis": "Rationale for A" },
      { "label": "Option B", "basis": "Rationale for B【我的推荐】" },
      { "label": "Need more info", "basis": "If none of the above fits" }
    ]
  }
]
```

### 2. 生成表单

```bash
node scripts/generate.js questions.json
```

输出内容包括：
- 本地HTML文件
- GitHub Gist的URL
- 预览链接（htmlpreview.github.io）

### 3. 将链接发送给用户

将预览链接发送给用户。用户填写表单并将填写后的JSON数据返回。

### 4. 解析用户回复

用户回复的结构如下：
```json
{
  "formId": "form-20260130-180000",
  "timestamp": "...",
  "globalFeedback": "all_ok|need_more_info|discuss|null",
  "globalComment": "Overall feedback",
  "summary": { "total": 3, "answered": 3, "agreedWithAI": 2 },
  "answers": [
    {
      "question": "Question title",
      "selectedLabel": "Option B",
      "customAnswer": "User's custom input if any",
      "agreedWithMyJudgment": true
    }
  ]
}
```

## 问题设计指南

### 必填字段
- `title`：清晰、简洁的问题标题
- `options`：至少2个选项，每个选项都应包含`label`（标签）

### 推荐字段
- `context`：背景信息——我当时正在处理什么任务
- `uncertainty`：我需要询问的原因——是什么阻碍了我的决策
- `findings`：带有来源的证据——展示原始文本，而不仅仅是摘要
- `judgment`：我的建议及理由

### 选项设计
- 为每个选项添加`basis`（理由）
- 用「**我的推荐**」标记推荐的选项
- 提供「需要更多信息」作为备用选项

### 质量原则
1. **提供完整背景**——展示原始文本，而不仅仅是提取的数字
2. **解释不确定性**——为什么我不能独自做出决定？
3. **引用来源**——每个发现的信息来自哪里？
4. **说明推荐理由**——我为什么倾向于这个选择？

## 工作流程集成

### CC任务集成

当CC完成需要用户确认的任务时，在CC提示中包含以下内容：

```
如果有需要主人确认的问题，在任务最后生成 questions.json 文件，格式：
[{"title":"问题","context":"背景","uncertainty":"不确定点","findings":[...],"judgment":"判断","options":[...]}]
```

CC完成任务后，检查`questions.json`文件，如果存在则生成表单。

### 回复归档

收到用户回复后，将其保存到归档文件中：
```
~/clawd/records/confirm-form/YYYY-MM-DD_<formId>.json
```

归档格式：
```json
{
  "formId": "...",
  "createdAt": "...",
  "respondedAt": "...",
  "questions": [...],
  "response": {...}
}
```

归档文件用于：回顾过去的决策、追踪确认模式。

## 文件列表
- `scripts/generate.js`：表单生成脚本
- `assets/template.html`：HTML表单模板（可复制粘贴使用）
- `assets/template-v2.html`：HTML表单模板（自动通知功能，处于测试阶段）
- `assets/examples/sample.json`：示例问题数据