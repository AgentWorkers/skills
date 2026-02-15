---
name: blinko
description: 通过 Blinko 的 REST API 管理笔记（创建/列出/删除笔记、管理标签/分类）。当用户输入 “blinko …” 时，可以使用该 API 将笔记保存到 Blinko 中、列出/搜索最近的笔记、重新标记笔记或进行清理/整理操作。使用该 API 需要 BLINKO_API_KEY。
---

# Blinko

将 Blinko 作为笔记管理的唯一信息来源。

## 设置（仅一次）

环境变量（Gateway 环境变量也可使用）：
- `BLINKO_API_KEY`（必填）
- `BLINKO_BASE_URL`（可选；默认值为 `https://blinko.exemple.com`）

## 核心工作流程

### 1) 创建笔记
当用户输入类似以下内容时：
- “blinko: …”
- “note: …”

系统会创建一个笔记，包含：
- 使用 Markdown 格式编写的正文
- 在笔记末尾添加标签（需遵循用户的分类规则）

### 2) 列出/搜索笔记
如果用户输入 “liste mes notes” 或 “cherche …”，系统会调用相应的 API 端点，并显示：
- 笔记的 ID
- 笔记的第一行/标题
- 最相关的标签（如果有的话）

### 3) 标签规则（用户限制）
- 最多允许使用 **7** 个顶级标签。
- 每个笔记最多可以选择 **1** 个顶级标签和 **0–2** 个子标签。
- 子标签的格式为：`#Tech/dev`。

### 4) 删除/清除笔记
在执行以下操作之前，必须明确获得用户的确认（例如：“OK, vas-y”）：
- 删除笔记
- 删除标签

建议使用辅助脚本来批量处理这些操作。

## 辅助脚本

`scripts/blinko.py` 负责封装 API 请求的逻辑。

示例：
```bash
# list
BLINKO_API_KEY=... ./scripts/blinko.py list --page 1 --size 20

# create
BLINKO_API_KEY=... ./scripts/blinko.py create --title "Test" --content "Hello" --tags "#Inbox #Todo/à-faire"

# delete (destructive)
BLINKO_API_KEY=... ./scripts/blinko.py delete --yes 123 124
```

## 参考资料

请参阅 `references/blinko_api.md` 以获取 API 端点的详细信息。

## Github 仓库

https://github.com/Vellis59/openclaw-skill-blinko