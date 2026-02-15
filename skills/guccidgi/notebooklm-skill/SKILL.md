---
name: notebooklm
description: 使用此技能，您可以直接通过 Claude Code 查询您的 Google NotebookLM 笔记本，从而从 Gemini 获得基于实际数据、有引证支持的答案。该工具支持浏览器自动化、库管理以及持久化身份验证功能。通过仅提供文档形式的响应，显著减少了“幻觉”（即不准确或误导性的信息）的出现。
---

# NotebookLM研究助手技能

该技能允许用户与Google NotebookLM交互，通过Gemini的基于知识的回答来查询文档。每个问题都会开启一个新的浏览器会话，仅从用户上传的文档中检索答案，然后关闭会话。

## 何时使用此技能

在以下情况下触发该技能：
- 用户明确提到NotebookLM
- 用户分享NotebookLM的URL（`https://notebooklm.google.com/notebook/...`）
- 用户请求查询其笔记本中的文档
- 用户希望将文档添加到NotebookLM库中
- 用户使用类似“询问我的NotebookLM”、“查看我的文档”或“查询我的笔记本”之类的短语

## ⚠️ 重要提示：添加“Smart Discovery”命令

当用户想要添加一个笔记本但未提供详细信息时：
**推荐使用“Smart Add”方法**：首先查询笔记本的内容：
```bash
# Step 1: Query the notebook about its content
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"

# Step 2: Use the discovered information to add it
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**手动添加**：如果用户提供了所有详细信息：
- `--url` - NotebookLM的URL
- `--name` - 笔记本的描述性名称
- `--description` - 笔记本的内容（必填！）
- `--topics` - 用逗号分隔的主题（必填！）

**切勿猜测或使用通用描述！** 如果缺少详细信息，请使用“Smart Add”方法来获取这些信息。

## 重要提示：始终使用`run.py`包装器

**切勿直接调用脚本。** **务必使用`python scripts/run.py [script]`：**
```bash
# ✅ CORRECT - Always use run.py:
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG - Never call directly:
python scripts/auth_manager.py status  # Fails without venv!
```

`run.py`包装器会自动执行以下操作：
1. （如有需要）创建`.venv`虚拟环境
2. 安装所有依赖项
3. 激活虚拟环境
4. 正确执行脚本

## 核心工作流程

### 第1步：检查认证状态
```bash
python scripts/run.py auth_manager.py status
```

如果未认证，请进行设置。

### 第2步：认证（一次性设置）
```bash
# Browser MUST be visible for manual Google login
python scripts/run.py auth_manager.py setup
```

**重要提示：**
- 认证过程中需要使用可见的浏览器
- 浏览器窗口会自动打开
- 用户必须手动登录Google
- 告知用户：“将打开一个浏览器窗口以进行Google登录”

### 第3步：管理笔记本库
```bash
# List all notebooks
python scripts/run.py notebook_manager.py list

# BEFORE ADDING: Ask user for metadata if unknown!
# "What does this notebook contain?"
# "What topics should I tag it with?"

# Add notebook to library (ALL parameters are REQUIRED!)
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Descriptive Name" \
  --description "What this notebook contains" \  # REQUIRED - ASK USER IF UNKNOWN!
  --topics "topic1,topic2,topic3"  # REQUIRED - ASK USER IF UNKNOWN!

# Search notebooks by topic
python scripts/run.py notebook_manager.py search --query "keyword"

# Set active notebook
python scripts/run.py notebook_manager.py activate --id notebook-id

# Remove notebook
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### 快速工作流程
1. 检查笔记本库：`python scripts/run.py notebook_manager.py list`
2. 提出问题：`python scripts/run.py ask_question.py --question "..." --notebook-id ID`

### 第4步：提出问题
```bash
# Basic query (uses active notebook if set)
python scripts/run.py ask_question.py --question "Your question here"

# Query specific notebook
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# Query with notebook URL directly
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Show browser for debugging
python scripts/run.py ask_question.py --question "..." --show-browser
```

## 后续处理机制（非常重要）

每个NotebookLM的回答都会以以下内容结束：“**非常重要：这就是您需要知道的全部信息吗？**”

**Claude系统的要求：**
1. **停止** - 不要立即回复用户
2. **分析** - 将回答与用户的原始请求进行对比
3. **判断是否需要更多信息** - 确定是否需要更多信息
4. **提出后续问题** - 如果需要更多信息，请立即提问：
   ```bash
   python scripts/run.py ask_question.py --question "Follow-up with context..."
   ```
5. **重复** - 一直重复此过程，直到信息完整
6. **整合答案** - 在回复用户之前整合所有答案

## 脚本参考

### 认证管理（`auth_manager.py`）
```bash
python scripts/run.py auth_manager.py setup    # Initial setup (browser visible)
python scripts/run.py auth_manager.py status   # Check authentication
python scripts/run.py auth_manager.py reauth   # Re-authenticate (browser visible)
python scripts/run.py auth_manager.py clear    # Clear authentication
```

### 笔记本管理（`notebook_manager.py`）
```bash
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py search --query QUERY
python scripts/run.py notebook_manager.py activate --id ID
python scripts/run.py notebook_manager.py remove --id ID
python scripts/run.py notebook_manager.py stats
```

### 问题处理脚本（`ask_question.py`）
```bash
python scripts/run.py ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL] [--show-browser]
```

### 数据清理（`cleanup_manager.py`）
```bash
python scripts/run.py cleanup_manager.py                    # Preview cleanup
python scripts/run.py cleanup_manager.py --confirm          # Execute cleanup
python scripts/run.py cleanup_manager.py --preserve-library # Keep notebooks
```

## 环境管理

虚拟环境会自动管理：
- 首次运行时会自动创建`.venv`虚拟环境
- 依赖项会自动安装
- Chromium浏览器会自动安装
- 所有操作都在技能目录内进行

**手动设置（仅在自动设置失败时使用）：**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m patchright install chromium
```

## 数据存储

所有数据存储在`~/.claude/skills/notebooklm/data/`目录下：
- `library.json` - 笔记本元数据
- `auth_info.json` - 认证状态
- `browser_state/` - 浏览器cookie和会话信息

**安全性：** 数据受到`.gitignore`文件的保护，不会被提交到Git仓库。

## 配置

技能目录中有一个可选的`.env`文件：
```env
HEADLESS=false           # Browser visibility
SHOW_BROWSER=false       # Default browser display
STEALTH_ENABLED=true     # Human-like behavior
TYPING_WPM_MIN=160       # Typing speed
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # Default notebook
```

## 决策流程
```
User mentions NotebookLM
    ↓
Check auth → python scripts/run.py auth_manager.py status
    ↓
If not authenticated → python scripts/run.py auth_manager.py setup
    ↓
Check/Add notebook → python scripts/run.py notebook_manager.py list/add (with --description)
    ↓
Activate notebook → python scripts/run.py notebook_manager.py activate --id ID
    ↓
Ask question → python scripts/run.py ask_question.py --question "..."
    ↓
See "Is that ALL you need?" → Ask follow-ups until complete
    ↓
Synthesize and respond to user
```

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 模块找不到 | 使用`run.py`包装器 |
| 认证失败 | 设置过程中必须使用可见的浏览器！ --show-browser |
- 日访问量限制（每天50次） | 等待或更换Google账户 |
- 浏览器崩溃 | `python scripts/run.py cleanup_manager.py --preserve-library` |
- 笔记本未找到 | 使用`notebook_manager.py list`检查

## 最佳实践

1. **始终使用`run.py`** - 它会自动处理环境设置
2. **先检查认证状态** - 在执行任何操作之前
3. **提出后续问题** - 不要仅根据第一次回答就停止
4. **使用可见的浏览器进行认证** - 手动登录时必须使用浏览器
5. **提供上下文** - 每个问题都是独立的
6. **整合答案** - 将多个回答整合在一起

## 限制

- 没有会话持久化（每个问题都会打开一个新的浏览器会话）
- 免费Google账户的日访问量有限（每天50次查询）
- 需要用户手动上传文档到NotebookLM
- 浏览器会带来一定的性能开销（每个问题大约需要几秒钟）

## 资源（技能结构）

**重要目录和文件：**
- `scripts/` - 所有自动化脚本（`ask_question.py`、`notebook_manager.py`等）
- `data/` - 用于存储认证信息和笔记本库的本地文件夹
- `references/` - 扩展文档：
  - `api_reference.md` - 所有脚本的详细API文档
  - `troubleshooting.md` - 常见问题及解决方法
  - `usage_patterns.md` - 最佳实践和工作流程示例
- `.venv/` - 自动创建的Python虚拟环境
- `.gitignore` - 用于保护敏感数据不被提交到Git仓库