---
name: feishu-pm
description: **Feishu Bitables的项目管理功能**：您可以直接通过代理工具添加任务、列出记录并跟踪项目进度。
tags: [feishu, bitable, pm, project, task]
---

# Feishu 项目管理员（Project Manager, PM）

通过命令行界面（CLI）直接在 Feishu Bitables 中管理任务和项目记录。

## 先决条件

- 首先安装 `feishu-common`。
- 该功能依赖于 `../feishu-common/index.js` 文件，用于处理令牌（token）和 API 认证。

## 使用方法

### 列出任务

```bash
node skills/feishu-pm/index.js list --app <BITABLE_TOKEN> --table <TABLE_ID>
```

选项：
- `--view <id>`：按视图 ID 过滤任务。
- `--limit <n>`：限制显示的记录数量（默认为 20 条）。
- `--json`：以原始 JSON 格式输出任务信息，而不是Markdown 表格。

### 添加任务

```bash
node skills/feishu-pm/index.js add --app <BITABLE_TOKEN> --table <TABLE_ID> --title "Fix Bug #123" --priority "High"
```

选项：
- `--desc <text>`：任务描述。
- `--priority <text>`：任务优先级（例如：“高”、“中”、“低”）。

## 注意事项

- 该功能目前针对“Iter 11”项目结构进行了优化（包含“需求”、“需求详述”和“优先级”字段）。
- 如需为其他项目自定义字段映射，请编辑 `index.js` 文件。