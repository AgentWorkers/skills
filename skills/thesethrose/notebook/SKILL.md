---
name: Notebook
description: 这是一个以本地数据为中心的个人知识库，用于跟踪各种想法、项目、任务、习惯以及你自定义的任何对象类型。它基于 YAML 格式设计，且不依赖于任何云服务。
---

# 笔记本：基于对象的个人知识库

**用途：** 可以跟踪您定义的任何对象类型，例如想法、项目、任务、习惯、书籍和人物等信息。

**存储位置：** `{WORKSPACE}/skills/notebook/`

## 代理（Agent）入职流程

当系统中尚未存在任何对象类型时，指导用户完成设置。

### 第一步：建议选择第一个对象类型

```
It looks like you have not defined any object types yet.
Notebook works best when you define the types of things you want to track.

What would you like to start with?

1. Ideas for capturing thoughts and features
2. Projects for long term work with goals
3. Tasks for actionable items with due dates
4. Something custom tell me what you want to track
```

### 第二步：共同定义对象类型

- 如果用户选择预设的对象类型：
  ```
Great. Let us set up [type].

I will create it with useful fields. You can add or remove them later.

For [type], what fields do you want?
- title (text, required)
- status (select)
- priority (select)
- tags (text)
- notes (longtext)
- [custom fields]

What fields should [type] have?
```

- 如果用户希望自定义对象类型：
  ```
Tell me what you want to track and what details matter.

Example: I want to track books I read. I need title, author, status, rating, and notes.

I will translate that into a type definition.
```

### 第三步：创建第一个对象

```
Now let us add your first [type].

What do you want to track as your first [type]?

Example: The Andromeda Strain for books or Home automation for projects
```

### 第四步：展示工作流程

```
Perfect. You now have:
- Type: [typename] with [N] fields
- 1 [typename] object: [title]

What would you like to do next?

- notebook list [typename] to see all items
- notebook expand [typename] [title] to add details
- notebook add [typename] to add another
- notebook type-add [typename] to add more fields later
```

### 第五步：提供扩展功能

```
Would you like to deepen this [typename] with some questions?
Say expand and I will ask questions to add depth.
```

## 快速参考

### 定义对象类型

```
notebook type-add typename field1:text field2:select(a|b|c) field3:number
```

- **字段类型：**
  - `text`：用于存储简短字符串
  - `longtext`：用于存储多行文本
  - `select(a|b|c)`：从列表中选择一个选项
  - `number`：用于存储数值
  - `date`：用于存储日期
  - `list`：用于存储字符串数组

### 操作对象的方法

```
notebook add typename "Title" [-t tag1,tag2 -p priority]
notebook list typename
notebook get typename title
notebook expand typename title
notebook edit typename "title" field:value
notebook link type1:title1 type2:title2
notebook delete typename title
notebook find "query"
notebook stats
```

## 示例工作流程

```
# 1. Define a type
notebook type-add idea title:text status:select(raw|expanded|archived) priority:select(high|medium|low) tags:text notes:longtext

# 2. Add your first idea
notebook add idea "Voice capture while driving" -t voice,automation -p high

# 3. Deepen it
notebook expand idea "voice capture"

# 4. Link to other objects
notebook add project "Home automation" -t household
notebook link idea:"voice capture" project:"home automation"

# 5. Update as you work
notebook edit idea "voice capture" status:expanded
```

## 数据存储位置

```
/data/notebook/
├── objects/
├── types.yaml
└── index.json
```

## 设计原则：
- **用户自定义**：用户可以自行定义所需的数据类型。
- **本地存储优先**：数据存储在本地YAML文件中，不依赖云服务或第三方软件。
- **对象间的关联**：对象之间可以相互引用。
- **可扩展性**：根据需要添加新的对象类型和字段。
- **深度思考引导**：通过智能问题引导用户更深入地思考和记录信息。