---
name: ms-todo-oauth
description: >
  A robust CLI skill to manage Microsoft To Do tasks via Microsoft Graph API.
  Supports full task lifecycle management including lists, tasks with priorities,
  due dates, reminders, recurrence patterns, views, search, and data export.
  Includes comprehensive test suite for reliability.
  THIS IS A REVISED OAUTH2-BASED VERSION OF ms-todo-sync with AI ASSISTANCE.
  ALL CREDITS TO THE ORIGINAL AUTHOR.
metadata:
  version: 1.0.3
  author: yalonghan@gmaill.com
  license: MIT License
  tags: [productivity, task-management, microsoft-todo, cli, graph-api, tested]
  category: productivity
  tested: true
  test_coverage: 29 comprehensive tests
---
# ms-todo-oauth

这是一个经过全面测试的Microsoft To Do命令行客户端，用于通过Microsoft Graph API管理任务和列表。

## ⚠️ 本脚本基于OAuth2认证。其中包含生成的Azure客户端ID和密钥

如果您担心隐私问题，可以考虑在`scripts\ms-todo-oauth.py`中将它们替换为您自己的信息。只需查找以下内容：

`client_id="ca6ec244……`  
`client_secret="TwQ8Q……`

## ✨ 主要功能

- ✅ **任务管理**：创建、完成、删除和搜索任务  
- 🗂️ **列表管理**：创建和管理多个任务列表  
- ⏰ **丰富的任务选项**：优先级、截止日期、提醒、描述、标签  
- 🔄 **重复任务**：每日、每周、每月的循环模式  
- 📊 **多种视图**：今日任务、逾期任务、待办任务、统计信息  
- 🔍 **强大的搜索功能**：在所有列表中查找任务  
- 💾 **数据导出**：将所有任务导出为JSON格式  
- 🧪 **全面测试**：包含29个自动化测试  
- 🌐 **支持Unicode**：完全支持中文字符和表情符号  

## 先决条件

1. 必须安装Python 3.9或更高版本  
2. 所有命令必须从包含此SKILL.md文件的目录（即工作目录）执行  
3. 需要互联网连接以访问Microsoft Graph API  
4. 拥有Microsoft账户（Hotmail、Outlook.com）或工作/学校账户  
5. 首次使用时需要通过浏览器进行OAuth2登录。详见[认证](#authentication)部分  
   - **令牌缓存**：`~/.mstodo_token_cache.json`（在会话间持久保存，自动刷新）  

## 安装与设置

### 首次使用前的设置

在首次使用此工具之前，需要安装以下依赖项：

```bash
# Navigate to skill directory
cd <path-to-ms-todo-oauth>

# Create a venv in the project (creates '.venv' folder)
python3 -m venv .venv
# Activate the venv choose based on platforms:
#- Bash/Zsh: 
source .venv/bin/activate
# - Fish: 
source .venv/bin/activate.fish
#  - Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt

# Alternative (global python env, not recommended):
# pip install -r requirements.txt
```

**依赖项：**  
- `msal`（Microsoft认证库）  
- `requests`（用于API请求的HTTP客户端）  
- 详见`requirements.txt`文件  

### 环境验证

安装完成后，请验证设置是否正确：

```bash

# If using native venv (activate as above):
python3 scripts/ms-todo-oauth.py --help

# Expected: Command help text should be displayed
```

## 故障排除

- 如果找不到Python，请从https://python.org安装Python 3.9或更高版本  

### 测试（可选但推荐）

验证所有功能是否正常工作：

```bash
# Run comprehensive automated test suite (29 tests)
python3 test_ms_todo_oauth.py

# Expected: All tests pass (100% pass rate)
```

详情请参阅[测试](#testing)部分。  

## 安全注意事项

- 通过Microsoft的`msal`库使用官方Microsoft Graph API  
- 所有代码均为纯Python（.py文件），易于阅读和审计  
- 令牌存储在本地文件`~/.mstodo_token_cache.json`中  
- 所有API请求直接发送到graph.microsoft.com  
- 遵循OAuth2标准认证流程  
- 不涉及任何第三方服务  

## 命令参考

所有命令遵循以下格式：  

```
python3 scripts/ms-todo-oauth.py [GLOBAL_OPTIONS] <command> [COMMAND_OPTIONS]
```

### 全局选项

| 选项            | 描述                                                                                                                         |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `-v, --verbose` | 显示详细信息（包括ID、日期、备注）。**必须放在子命令之前**                                       |
| `--debug`       | 启用调试模式，显示API请求和响应。有助于故障排除。**必须放在子命令之前** |
| `--reauth`      | 通过清除令牌缓存并重新登录来强制重新认证                                                        |

> ⚠️ **重要提示**：全局选项必须放在子命令之前。  
> - 示例用法：`python3 scripts/ms-todo-oauth.py -v lists`  
> - 示例用法：`python3 scripts/ms-todo-oauth.py --debug add "Task"`  
> - 错误用法：`python3 scripts/ms-todo-oauth.py lists -v`  

---

### 认证

该工具使用OAuth2认证流程，适用于交互式和自动化环境。

#### `login get` — 获取OAuth2授权码  

```bash
python3 scripts/ms-todo-oauth.py login get
```

**输出示例：**  
（此处应显示获取授权码的URL和提示信息）  

**操作步骤：**  
1. 在浏览器中打开提供的URL  
2. 使用您的Microsoft账户登录  
3. 根据提示授予权限  
4. 您将被重定向到类似以下内容的URL：`http://localhost:8000/callback?code=M.R3_BAY.abc123...`  
5. 复制`code=`后面的整个字符串（通常以`M.R3_BAY.`开头）  

**代理行为**：  
向用户展示该URL，并告知他们需要：  
1. 访问该URL  
2. 完成登录  
3. 从回调URL中复制授权码  
4. 将授权码提供给代理  

#### `login verify` — 使用授权码完成登录  

```bash
python3 scripts/ms-todo-oauth.py login verify <authorization_code>
```

**示例：**  
（此处应显示登录界面和输入授权码的提示）  

**成功输出：**  
（此处应显示登录成功后的信息）  

**失败输出：**  
（此处应显示登录失败的原因）  

**退出代码**：  
成功时返回0，失败时返回1。  

**重要提示：**  
- 每个授权码仅可使用一次  
- 如果验证失败，需要再次运行`login get`以获取新的授权码  
- 成功登录后，令牌会被缓存，除非执行`logout`、`--reauth`或令牌过期，否则无需重新登录  

#### `logout` — 清除保存的登录信息  

```bash
python3 scripts/ms-todo-oauth.py logout
```

**输出：**  
“✓ 登录信息已清除”  

仅在用户明确要求切换账户或清除登录信息时使用此命令。通常情况下，令牌会被缓存，登录是自动完成的。  

---

### 列表管理

#### `lists` — 列出所有任务列表  

```bash
python3 scripts/ms-todo-oauth.py lists
python3 scripts/ms-todo-oauth.py -v lists  # with IDs and creation dates
```

**输出示例：**  
（列出所有任务列表）  

#### `create-list` — 创建新列表  

```bash
python3 scripts/ms-todo-oauth.py create-list "<name>"
```

| 参数          | 是否必填 | 描述                                                                                                 |
| -------------- | -------- | ------------------------- |
| `name`         | 是      | 新列表的名称（支持Unicode/中文）                                                                                                 |

**示例：**  
`python3 scripts/ms-todo-oauth.py create-list "项目A"`  
**输出：**  
“✓ 列表创建：项目A”  

#### `delete-list` — 删除列表  

```bash
python3 scripts/ms-todo-oauth.py delete-list "<name>" [-y]
```

| 参数          | 是否必填 | 描述                                                                                                 |
| -------------- | ------------------------- |
| `name`         | 是      | 要删除的列表名称                                                                                                 |
| `-y, --yes`       | 否       | 省略确认提示                                                                                                 |

> ⚠️ **注意**：此操作具有破坏性。如果不使用`-y`参数，系统会提示确认。删除重要列表前请务必询问用户。  
**输出：**  
“✓ 列表已删除：<名称>”  

**退出代码**：  
列表未找到时返回1，删除成功时返回0。  

---

### 任务操作

#### `add` — 添加新任务  

```bash
python3 scripts/ms-todo-oauth.py add "<title>" [options]
```

| 选项          | 是否必填 | 默认值        | 描述                                                                                                      |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `title`         | 是      | 任务标题（支持Unicode/中文/表情符号）                                                                                                 |
| `-l, --list`       | 否       | 目标列表名称（如果未指定，使用默认列表）                                                                                                 |
| `-p, --priority`    | 是否必填 | 优先级（`low`, `normal`, `high`）                                                                                                 |
| `-d, --due`       | 是否必填 | 截止日期（例如`3`表示3天后，`2026-02-15`表示具体日期）                                                                                                 |
| `-r, --reminder`    | 是否必填 | 提醒时间（格式示例：`3h`表示3小时后，`2d`表示2天后）                                                                                                 |
| `-R, --recurrence`   | 是否必填 | 重复模式（例如`daily`表示每天，`weekly`表示每周）                                                                                                 |
| `-D, --description` | 是否必填 | 任务描述/备注（支持多行内容）                                                                                                 |
| `-t, --tags`       | 是否必填 | 逗号分隔的标签（例如`"工作,紧急"`）                                                                                                 |
| `--create-list`     | 是否必填 | 如果列表不存在，则创建新列表（已弃用，现在会自动创建列表）                                                                                                 |

**示例：**  
`python3 scripts/ms-todo-oauth.py add "购买牛奶, 完成报告, 约见牙医"`  
**输出：**  
“✓ 任务已添加：购买牛奶, 完成报告, 约见牙医”  

**带有重复设置的示例：**  
（此处应显示包含重复设置的命令示例）  

#### `complete` — 将任务标记为已完成  

```bash
python3 scripts/ms-todo-oauth.py complete "<title>" [-l "<list>"]
```

| 选项          | 是否必填 | 默认值        | 描述                                                                                                      |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `title`         | 是      | 任务标题                                                                                                 |
| `-l, --list`       | 是否必填 | 任务所属列表名称（默认使用默认列表）                                                                                                 |

**注意**：  
- 使用`-l`参数时，必须提供任务所属列表的名称。  
- 确保输入的标题与列表名称完全匹配。  

**输出：**  
“✓ 任务已完成：购买牛奶”  

**退出代码**：  
任务未找到时返回1，删除成功时返回0。  

#### `delete` — 删除任务  

```bash
python3 scripts/ms-todo-oauth.py delete "<title>" [-l "<list>"] [-y]
```

| 选项          | 是否必填 | 默认值        | 描述                                                                                                      |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `title`         | 是      | 任务标题                                                                                                 |
| `-l, --list`       | 是否必填 | 任务所属列表名称（默认使用默认列表）                                                                                                 |
| `-y, --yes`       | 是否必填 | 省略确认提示                                                                                                 |

> ⚠️ **注意**：此操作具有破坏性。如果不使用`-y`参数，系统会提示确认。  
**输出：**  
“✓ 任务已删除：购买牛奶”  

**退出代码**：  
任务未找到时返回1，删除成功时返回0。  

---

### 任务查看

#### `tasks` — 查看特定列表中的任务  

```bash
python3 scripts/ms-todo-oauth.py tasks "<list>" [-a]
```

| 选项          | 是否必填 | 描述                                                                                                 |
| -------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `list`         | 是      | 列表名称（必须完全匹配）                                                                                                 |
| `-a, --all`       | 是否必填 | 是否包含已完成的任务（默认仅显示未完成的任务）                                                                                                 |

**示例：**  
`python3 scripts/ms-todo-oauth.py tasks lists`  
**输出：**  
（列出所有任务，已完成的任务会标记为已完成）  

#### `pending` — 查看所有列表中的未完成任务  

```bash
python3 scripts/ms-todo-oauth.py pending [-g]
```

| 选项          | 是否必填 | 描述                                                                                                 |
| -------------- | -------- | ------------------------- |
| `-g, --group`     | 是否必填 | 是否按列表分组显示结果                                                                                                 |

**示例：**  
`python3 scripts/ms-todo-oauth.py pending`  
**输出：**  
（按列表分组显示未完成任务）  

**不使用`-g`参数时：**  
（仅列出所有任务）  

#### `today` — 查看今日到期的任务  

```bash
python3 scripts/ms-todo-oauth.py today
```

**输出示例：**  
（列出今日到期的任务）  

**如果没有到期任务：**  
“📅 今日没有到期任务”  

#### `overdue` — 查看逾期任务  

```bash
python3 scripts/ms-todo-oauth.py overdue
```

**输出示例：**  
（列出逾期未完成的任务）  

**如果没有逾期任务：**  
“✓ 无逾期任务”  

#### `detail` — 查看任务详细信息  

```bash
python3 scripts/ms-todo-oauth.py detail "<title>" [-l "<list>"]
```

| 选项          | 是否必填 | 描述                                                                                                 |
| -------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `title`         | 是否必填 | 任务标题（支持部分/模糊匹配）                                                                                                 |
| `-l, --list`       | 是否必填 | 任务所属列表名称（默认使用默认列表）                                                                                                 |

**匹配规则：**  
- 支持部分匹配和模糊匹配  
- 在多个匹配的任务中，优先显示未完成的任务  
- 返回最近修改的任务  

**示例：**  
（列出未完成的任务）  

#### `search` — 按关键词搜索任务  

```bash
python3 scripts/ms-todo-oauth.py search "<keyword>"
```

**搜索范围**：  
在所有列表中搜索任务标题和描述（不区分大小写）。  

**输出示例：**  
（列出匹配的任务）  

#### `stats` — 查看任务统计信息  

```bash
python3 scripts/ms-todo-oauth.py stats
```

**输出示例：**  
（显示所有任务的统计信息）  

#### `export` — 将所有任务导出为JSON  

```bash
python3 scripts/ms-todo-oauth.py export [-o "<filename>"]
```

| 选项          | 是否必填 | 默认值        | 描述                                                                                                 |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `-o, --output` | 是否必填 | 输出文件路径（默认为`todo_export.json`）                                                                                                 |

**输出示例：**  
“✓ 任务已导出至：<文件路径>`  
（输出文件内容：所有任务的JSON格式）  

---

## 错误处理

### 出错代码  

| 代码          | 含义                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `0`         | 成功                                                                                                 |
| `1`         | 失败（未登录、API错误、参数无效、资源未找到）                                                                                                 |
| `2`         | 参数错误                                                                                                 |

### 常见错误信息及解决方法  

| 错误信息            | 原因                                      | 解决方法                                                                                                 |
| ----------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `❌ 未登录`         | 令牌未缓存或已过期                                 | 先运行`login get`，然后运行`login verify <授权码>`                                                                                   |
| `ModuleNotFoundError`     | 未安装依赖项                                 | 运行`pip install -r requirements.txt`                                                                                   |
| `❌ 列表未找到`        | 指定的列表不存在                                 | 使用`lists`命令检查列表名称（需完全匹配）                                                                                   |
| `❌ 任务未找到`        | 任务标题不匹配                                 | 使用`search`查找任务标题，或使用`tasks "<列表名称>"列出所有任务                                                                                   |
| `❌ 错误：无效的ISO格式字符串`    | 时间格式解析错误                                   | 应在v1.1.0及以上版本中不会出现此问题；如有问题请报告                                                                                   |
| `❌ 错误：不支持的HTTP方法`     | API内部错误                                   | 应在v1.1.0及以上版本中不会出现此问题；如有问题请报告                                                                                   |
| `❌ 错误：<API错误信息>`     | Microsoft Graph API错误                                 | 重试；检查网络连接；使用`--debug`查看详细信息                                                                                   |
| `Network error`     | 无法连接网络或API不可达                                 | 检查网络连接；确认能否访问graph.microsoft.com                                                                                   |

## 测试

该工具包含一个全面的测试套件以确保可靠性。

### 自动化测试

运行完整的测试套件：  
**命令：** `python3 scripts/ms-todo-oauth.py test`  

**前提条件：**  
- 必须先登录  
- 需要互联网连接  
- 测试耗时约2-3分钟  

**测试覆盖范围：**  
- ✅ 认证（登录/登出）  
- ✅ 列表管理（创建、删除、列出）  
- ✅ 基本任务操作（添加、完成、删除、列出）  
- ✅ 任务选项（优先级、截止日期、提醒、描述、标签）  
- ✅ 重复任务（每日、每周、每周、每月）  
- ✅ 任务视图（今日、逾期、待办、搜索、统计）  
- ✅ 数据导出和验证  
- ✅ 错误处理（资源不存在）  
- ✅ Unicode支持（中文字符、表情符号）  

**预期输出：**  
（测试结果示例）  

### 手动测试

有关手动测试的详细步骤和预期结果，请参阅`MANUAL_TEST_CHECKLIST.txt`。  

### 测试清理

自动化测试套件会：  
- 创建临时测试列表  
- 单独运行所有测试  
- 测试完成后删除临时列表  
- 清理临时文件  

如果测试中断，可能需要手动删除剩余的测试列表。  

## 代理使用指南

### 关键规则

1. 在运行命令之前，务必切换到包含此SKILL.md文件的目录。  
2. 在首次使用或遇到导入错误时，确保已安装所有依赖项。  
3. 在执行任何操作之前，先检查认证状态：  
   如果显示“未登录”错误（退出代码1），请先进行登录。  

**添加任务时的操作流程：**  
- 首先运行`lists`查看可用列表  
- 如果用户未指定列表，任务将添加到默认列表（通常为“Tasks”或“任务”）  
- 智能地将任务分类到相应的列表中：  
  - 工作任务 → “工作”列表  
  - 个人事务 → “个人”列表  
  - 购物任务 → “购物”列表  
  - 项目相关任务 → 使用项目名称作为列表名称  
- 如果列表不存在，系统会自动创建  
- 支持中文列表名称和Unicode字符  

**删除操作注意事项：**  
- `delete`和`delete-list`命令默认会提示确认  
- 仅在用户明确要求不显示确认提示时使用`-y`参数  
- 如果删除操作明确且得到确认，否则返回退出代码1  
- 如果操作失败，返回退出代码1（表示资源未找到）  

### 全局选项的使用规则  

- `-v`, `--debug`, `--reauth`必须放在子命令之前  
- 示例用法：`python3 scripts/ms-todo-oauth.py -v lists`  
- 错误用法：`python3 scripts/ms-todo-oauth.py lists -v`  

**登录流程：**  
- 在用户确认完成浏览器登录之前，切勿调用`login verify`  
- 每个授权码仅可使用一次  
- 如果验证失败，需再次运行`login get`以获取新的授权码  

### 错误处理建议：  
- 检查退出代码：0表示成功，1表示失败，2表示参数无效  
- 解析错误信息以提供帮助  
- 使用`--debug`参数排查API问题  

### 建议的工作流程  

- 使用`search`先查找任务标题，确保完全匹配后再执行`complete`或`delete`等操作  

**示例工作流程：**  
（描述用户任务请求和代理的执行步骤）  

## 常见工作流程  

- **每日任务回顾**  
- **添加不同类型的任务**  
- **完成任务**  
- **数据管理**  

## 更新日志  

### 版本说明  

### 版本1.1.0（当前版本）  
- 修复了日期时间解析错误  
- 修复了HTTP方法参数顺序的问题  
- 修复了`create_task()`函数中缺少`start_date`参数的问题  
- 修复了`complete_task()`函数的问题  
- 修复了错误退出代码的问题  
- 添加了全面的测试套件（29个自动化测试）  
- 改进了错误信息和故障排除机制  
- 改进了OAuth2认证流程的文档  
- 改进了Unicode和表情符号的支持文档  
- 改进了代理使用指南  

### 版本1.0.2（之前的版本）  
- 首次发布，支持OAuth2认证  
- 基本的任务和列表管理功能  
- 支持重复任务  
- 提供多种任务视图  
- 支持数据导出功能  

## 故障排除指南  

### 常见问题及解决方法  

- **登录问题**：  
  - 如果显示“未登录”，请运行`login get`，完成登录流程，然后运行`login verify <授权码>`  
- 如果提示“获取令牌失败：invalid_grant”，可能是授权码已使用或过期，请重新运行`login get`获取新授权码  
- 如果登录成功后再次显示“未登录”，可能是令牌已过期，请运行`--reauth`强制重新登录  

### 依赖项/导入问题  

- 如果出现`ModuleNotFoundError: No module named 'msal'`，请运行`pip install -r requirements.txt`安装依赖项  

### API/网络问题  

- 检查网络连接是否正常  
- 可以在浏览器中访问`https://graph.microsoft.com`吗？  
- 使用`--debug`参数查看完整的API请求和响应  

### 任务/列表未找到问题  

- 如果提示“任务未找到”，请使用`search`查找任务标题  
- `complete`和`delete`命令要求任务标题完全匹配  
- 如果提示“列表未找到”，请使用`lists`命令查看列表名称（列表名称区分大小写）  

### 测试失败原因  

- 如果测试失败，请确保已应用v1.1.0版本的修复措施  
- 确保`_parse_ms_datetime()`辅助函数存在  

- 如果测试失败，请确保已登录：  
  - 运行`login get`进行认证  

## 其他资源  

- **测试套件**：`test_ms_todo_oauth.py`（自动化测试脚本）  
- **手动测试指南**：`MANUAL_TEST_CHECKLIST.txt`  
- **快速参考**：`QUICK_REFERENCE.txt`  
- **错误修复记录**：`COMPLETE_FIXPATCH.txt`（包含v1.1.0版本的修复内容）  

## 支持与贡献  

- 报告问题时，请提供错误信息和使用的命令  
- 如适用，请附上`--debug`参数的输出结果  
- 请注明使用的Python版本（例如`python3 --version`）和操作系统（Windows/Mac/Linux）  

**新功能测试：**  
- 在修改代码后务必运行测试套件  
- 为新功能添加到`test_ms_todo_oauth.py`中  
- 更新`MANUAL_TEST_CHECKLIST.txt`中的手动测试步骤  

## 许可证  

本工具采用MIT许可证，详细信息请参阅`LICENSE`文件。  

**版本：** 1.1.0  
**更新时间：** 2026-02-13  
**状态：** 已通过全面测试，可投入生产使用