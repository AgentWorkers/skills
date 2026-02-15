---
name: local-approvals
description: 本地审批系统用于管理代理权限。可通过命令行界面（CLI）来批准/拒绝请求、查看审批历史记录以及管理自动批准的分类。
---

# 本地审批技能

这是一个用于管理代理权限的本地审批系统，支持自动审批功能以及审批历史记录的跟踪。

## 快速入门

```bash
# List pending requests
python C:\Users\Shai\.openclaw\skills\local-approvals\cli.py list

# Approve a request
python C:\Users\Shai\.openclaw\skills\local-approvals\cli.py approve abc123

# Deny a request
python C:\Users\Shai\.openclaw\skills\local-approvals\cli.py deny abc123

# Show approval history
python C:\Users\Shai\.openclaw\skills\local-approvals\cli.py history

# Reset an agent's categories
python C:\Users\Shai\.openclaw\skills\local-approvals\cli.py reset assistant
```

## 命令

### approve(id)
通过ID批准一个待处理的请求。

```bash
python cli.py approve <request_id> [--learn] [--reviewer <name>]
```

**选项:**
- `--learn`: 将该类别添加到代理的自动审批列表中
- `--reviewer`: 批准者（默认值：`user`）

**示例:**
```bash
python cli.py approve abc123 --learn
```

### deny(id)
通过ID拒绝一个待处理的请求。

```bash
python cli.py deny <request_id> [--reviewer <name>]
```

**选项:**
- `--reviewer`: 拒绝者（默认值：`user`）

**示例:**
```bash
python cli.py deny abc123
```

### list_pending()
列出所有待处理的请求，可选地按代理进行过滤。

```bash
python cli.py list [--agent <agent_id>]
```

**选项:**
- `--agent`: 按代理ID过滤请求

**示例:**
```bash
python cli.py list --agent assistant
```

### show_history()
从`state.json`文件中显示审批历史记录。

```bash
python cli.py history [--limit <number>]
```

**选项:**
- `--limit`: 显示的最大条目数（默认值：20）

**示例:**
```bash
python cli.py history --limit 50
```

### reset_categories(agent)
重置代理的自动审批类别列表。

```bash
python cli.py reset <agent_id>
```

**示例:**
```bash
python cli.py reset assistant
```

## 其他命令

### categories
显示一个或多个代理的自动审批类别。

```bash
python cli.py categories [--agent <agent_id>]
```

**选项:**
- `--agent`: 为特定代理显示类别

**示例:**
```bash
python cli.py categories --agent planner
```

## 状态文件

该技能在`state`目录下维护两个JSON文件：

- **state.json**: 自动审批列表和审批历史记录
- **pending.json**: 待处理的审批请求

**位置**: `~/.openclaw/skills/local-approvals/`

## 核心功能

`core.py`模块提供了以下核心功能：

- `check_auto_approve(agent, category)` - 检查某个类别是否被自动批准
- `submit_request(agent, category, operation, reasoning)` - 提交一个待处理的请求
- `learn_category(agent, category)` - 将类别添加到自动审批列表中
- `get_request(request_id)` - 根据ID检索请求
- `update_request(request_id, decision, reviewer)` - 更新请求的状态
- `list_pending(agent)` - 列出待处理的请求
- `get_agent_approvals(agent)` - 获取代理的自动审批类别

## 最佳实践

1. **审批前审核**: 在批准之前务必检查操作内容和理由。
2. **谨慎使用自动学习功能**: 只将`--learn`选项用于那些你希望自动批准的受信任的类别。
3. **定期查看历史记录**: 定期查看审批历史记录以了解审批模式。
4. **必要时重置**: 如果怀疑有问题，使用`reset`命令清除代理的自动审批列表。

## 示例

### 完整工作流程

```bash
# 1. Check what's pending
python cli.py list

# 2. Review the request details (output shows agent, category, operation, reasoning)
# ID: abc123
#   Agent:     assistant
#   Category:  file_write
#   Operation: Create config file
#   Reasoning: Setting up new environment

# 3. Approve and auto-learn this category for future
python cli.py approve abc123 --learn

# 4. Verify it was approved
python cli.py list  # Should show no pending requests

# 5. Check history
python cli.py history

# 6. View auto-approved categories
python cli.py categories
```

### 管理类别

```bash
# View all auto-approved categories
python cli.py categories

# View categories for a specific agent
python cli.py categories --agent assistant

# Reset an agent's categories (clear all auto-approvals)
python cli.py reset assistant
```

## 集成

该命令行界面（CLI）既可用于交互式操作，也可用于编程式调用。退出代码说明：
- `0`: 成功
- `1`: 错误（例如：请求未找到、代理未找到等）

## 文件

- `cli.py` - 命令行接口（本文件）
- `core.py` - 核心审批功能模块
- `schemas/` - JSON模式定义文件
- `schemas/state.json` - 状态数据结构模板
- `schemas/pending.json` - 待处理请求数据结构模板