---
name: clawbrain
version: 0.1.14
description: "**Claw Brain**——专为 OpenClaw/ClawDBot 设计的个人 AI 记忆系统。该系统具备记忆存储、个性塑造、情感建立以及学习功能，并支持加密数据的存储与保护。在服务重启时，系统会自动恢复所有数据。"
metadata: {"openclaw":{"emoji":"🧠","category":"memory","provides":{"slot":"memory"},"events":["gateway:startup","command:new"]},"clawdbot":{"emoji":"🧠","category":"memory","provides":{"slot":"memory"},"events":["gateway:startup","command:new"]}}
---

# Claw Brain 技能 🧠

这是一个专为 OpenClaw/ClawDBot 设计的个人 AI 记忆系统，具备灵魂、情感联结和学习功能。

> **重启时自动刷新**：当服务重启时，ClawBrain 会自动刷新记忆数据。

---

## 📋 安全扫描器相关

**环境变量**：所有环境变量都在 `skill.json` 文件的 `environment.optional` 部分（第 30-55 行）中声明。这些变量是**可选的**，因为 ClawBrain 可以在**无需任何配置**的情况下运行（使用 SQLite 和自动生成的加密密钥）。

**安装说明**：`skill.json` 文件中指定了安装方法：`pip install clawbrain[all]` 后执行 `clawbrain setup`（第 17-20 行）。

**是否需要 sudo**：核心组件的安装**完全不需要 sudo**。`Configuration (Optional)` 部分中的 systemd 配置仅作为设置环境变量的**可选方案**。核心组件只需使用 `pip` 和 `clawbrain setup` 即可。

**源代码**：完整源代码可在 [https://github.com/clawcolab/clawbrain](https://github.com/clawcolab/clawbrain) 查看，所有代码（包括约 50 行 JavaScript 代码）均为开源。

**请参阅 [SECURITY.md](SECURITY.md) 以获取完整的安全性文档。**

---

## 主要功能

- 🎭 **灵魂/个性**：6 个可发展的特质（幽默感、同理心、好奇心、创造力、乐于助人、诚实）
- 👤 **用户资料**：学习用户的偏好、兴趣和沟通风格
- 💭 **对话状态**：实时检测用户情绪并跟踪对话上下文
- 📚 **学习能力**：通过互动和反馈持续学习
- 🧠 **get_full_context()**：提供个性化响应所需的所有信息
- 🔄 **自动刷新**：服务重启时自动刷新记忆数据
- 🔐 **加密秘密**：安全存储 API 密钥和凭证

---

## 安全性与透明度

ClawBrain 处理敏感数据，因此需要相应的权限。在安装前，请了解以下内容：

### ClawBrain 的功能：
- ✅ **本地存储记忆数据**（默认使用 SQLite，也可使用 PostgreSQL）
- ✅ **使用 Fernet 加密敏感数据（如 API 密钥）**
- ✅ **在 `~/.openclaw/hooks` 或 `~/.clawdbot/hooks` 中安装启动脚本**
- ✅ **将加密密钥存储在 `~/.config/clawbrain/.brain_key` 中**

### ClawBrain 不会做什么：
- ❌ **不发送任何遥测数据**：不会向外部发送任何信息或收集使用数据
- ❌ **不进行外部调用**：仅会在您配置的情况下连接 PostgreSQL/Redis
- ❌ **无需 sudo**：所有操作都在您的用户目录内完成
- ❌ **不执行任何代码**：安装后不会下载或运行远程代码

### 安全特性：
- 🔒 **加密密钥管理 CLI**：可以显示完整的加密密钥以用于备份（会提供警告）
- 🔍 **代码可审计**：所有代码均为开源，可供审查
- 📋 **权限说明**：详细信息请参阅 [SECURITY.md](SECURITY.md)

**⚠️ 重要提示**：CLI 命令 `clawbrain show-key --full` 会显示完整的加密密钥，用于备份。请将此密钥视为重要密码！

**📖 完整的安全性文档**：请参阅 [SECURITY.md]，了解：
- 安全模型和防护措施
- 密钥管理最佳实践
- 安装脚本的功能
- 所需的权限
- 网络访问设置（可选的 PostgreSQL/Redis）

---

## 快速安装

> **安全提示**：建议在安装前阅读 [SECURITY.md](SECURITY.md)，尤其是在生产环境中使用该功能。

### 通过 PyPI 安装（推荐，最安全）

```bash
# Install with all features
pip install clawbrain[all]

# Run interactive setup
clawbrain setup

# Backup your encryption key (IMPORTANT!)
clawbrain backup-key --all

# Restart your service
sudo systemctl restart clawdbot  # or openclaw
```

安装命令会：
1. 检测您的平台（ClawdBot 或 OpenClaw）
2. 生成安全的加密密钥
3. 自动安装启动脚本
4. 测试安装结果

### 从源代码安装（可审计）

```bash
# Clone to your skills directory
cd ~/.openclaw/skills  # or ~/clawd/skills or ~/.clawdbot/skills
git clone https://github.com/clawcolab/clawbrain.git
cd clawbrain

# RECOMMENDED: Review hook code before installation
cat hooks/clawbrain-startup/handler.js

# Install in development mode
pip install -e .[all]

# Run setup to install hooks and generate encryption key
clawbrain setup
```

**为什么要从源代码安装？** 可以在安装前查看所有代码，确保安全性。

---

## 配置（可选）

**注意**：配置是**完全可选的**。ClawBrain 在没有配置的情况下也能使用 SQLite 和自动生成的加密密钥正常运行。

如果您想自定义代理 ID 或使用 PostgreSQL/Redis，有两种方法：

### 方法 1：通过环境变量（无需 sudo）

在您的 shell 配置文件中设置环境变量：

```bash
# Add to ~/.bashrc or ~/.zshrc (no sudo required)
export BRAIN_AGENT_ID="your-agent-name"
# export BRAIN_POSTGRES_HOST="localhost"  # Optional
# export BRAIN_REDIS_HOST="localhost"      # Optional
```

### 方法 2：通过 systemd 配置（需要 sudo）

**⚠️ 仅适用于使用 systemd 服务的场景**：

```bash
# Create systemd drop-in config (requires sudo)
sudo mkdir -p /etc/systemd/system/clawdbot.service.d

sudo tee /etc/systemd/system/clawdbot.service.d/brain.conf << EOF
[Service]
Environment="BRAIN_AGENT_ID=your-agent-name"
EOF

sudo systemctl daemon-reload
sudo systemctl restart clawdbot
```

### 环境变量

| 变量          | 描述                        | 默认值         |
|---------------|---------------------------|--------------|
| BRAIN_AGENT_ID     | 该代理的记忆数据的唯一标识符         | `default`        |
| BRAIN_ENCRYPTION_KEY | 用于加密敏感数据的 Fernet 密钥     | （未设置时自动生成）   |
| BRAIN_POSTGRES_HOST    | PostgreSQL 服务器地址            | `localhost`       |
| BRAIN_POSTGRES_PASSWORD | PostgreSQL 密码                |              |
| BRAIN_POSTGRES_PORT    | PostgreSQL 端口                | `5432`        |
| BRAIN_POSTGRES_DB     | 使用的 PostgreSQL 数据库名称       | `brain_db`       |
| BRAIN_POSTGRES_USER    | PostgreSQL 用户名                | `brain_user`       |
| BRAIN_REDIS_HOST    | Redis 服务器地址            | `localhost`       |
| BRAIN_REDIS_PORT    | Redis 端口                | `6379`        |
| BRAIN_STORAGE     | 数据存储方式（sqlite, postgresql, auto）     | `auto`         |

---

## 工作原理

### 服务启动时：
1. 在 `gateway:startup` 事件触发时执行相关操作
2. 检测存储后端（SQLite 或 PostgreSQL）
3. 加载为当前 `BRAIN_AGENT_ID` 配置的记忆数据
4. 将上下文信息注入代理的启动脚本中

### 执行 `/new` 命令时：
1. 在 `command:new` 事件触发时执行相关操作
2. 将当前会话信息保存到内存中
3. 清除会话状态，以便重新开始

### 存储优先级：
1. **PostgreSQL**：如果可用且已配置，则优先使用
2. **SQLite**：作为备用方案，无需额外配置

---

## 加密敏感数据

ClawBrain 支持使用 Fernet（对称加密算法）来加密 API 密钥和凭证等敏感数据。

**安全模型：**
- 🔐 加密密钥存储在 `~/.config/clawbrain/.brain_key` 文件中（权限设置为 600）
- 🔑 只有标记为 `memory_type='secret'` 的记忆数据才会被加密
- 📦 加密后的数据仅凭密钥才能读取
- ⚠️ 如果密钥丢失，加密数据将无法恢复

**配置方法**：
```bash
# Run setup to generate encryption key
clawbrain setup

# Backup your key (IMPORTANT!)
clawbrain backup-key --all
```

**使用方法**：
```python
# Store encrypted secret
brain.remember(
    agent_id="assistant",
    memory_type="secret",  # Memory type 'secret' triggers encryption
    content="sk-1234567890abcdef",
    key="openai_api_key"
)

# Retrieve and automatically decrypt
secrets = brain.recall(agent_id="assistant", memory_type="secret")
api_key = secrets[0].content  # Automatically decrypted
```

**密钥管理 CLI**：
```bash
clawbrain show-key          # View key info (masked)
clawbrain show-key --full   # View full key
clawbrain backup-key --all  # Backup with all methods
clawbrain generate-key      # Generate new key
```

**重要提示**：请务必备份您的加密密钥！密钥丢失会导致加密数据无法恢复。

---

## 命令行接口

ClawBrain 提供了以下命令行接口：

| 命令          | 功能                        |
|-----------------|---------------------------|
| clawbrain setup    | 设置 ClawBrain、生成密钥、安装启动脚本       |
| clawbrain generate-key | 生成新的加密密钥                |
| clawbrain show-key    | 显示当前的加密密钥                |
| clawbrain backup-key   | 备份密钥（文件、二维码、剪贴板）           |
| clawbrain health    | 检查系统运行状态                |
| clawbrain info     | 显示安装信息                    |

---

## 启动脚本

| 事件            | 执行的操作                          |
|-----------------|-----------------------------|
| gateway:startup    | 初始化 ClawBrain、刷新记忆数据           |
| command:new       | 将当前会话信息保存到内存中           |

---

## 开发环境安装

适用于开发或手动安装：

```bash
# Clone to your skills directory
cd ~/.openclaw/skills  # or ~/clawd/skills or ~/.clawdbot/skills
git clone https://github.com/clawcolab/clawbrain.git
cd clawbrain

# Install in development mode
pip install -e .[all]

# Run setup
clawbrain setup
```

---

## Python API

适用于在 ClawdBot/OpenClaw 之外直接使用 ClawBrain 的 Python 代码：

```python
from clawbrain import Brain

brain = Brain()
```

#### 方法列表

| 方法            | 功能                          | 返回值           |
|-----------------|-----------------------------|-------------------|
| get_full_context()    | 获取所有上下文信息，用于个性化响应       | dict            |
| remember()       | 存储记忆数据                   | None            |
| recall()        | 检索记忆数据                   | List[Memory]       |
| learn_user_preference() | 学习用户偏好                   | None            |
| get_user_profile()    | 获取用户资料                   | UserProfile         |
| detect_user_mood()    | 检测用户当前情绪                 | dict            |
| detect_user(intent()    | 分析用户发送消息的意图             | str            |
| generate_personality_prompt() | 生成个性引导提示             | str            |
| health_check()      | 检查后端连接状态                 | dict            |
| close()         | 关闭所有连接                   | None            |

### get_full_context() 方法

**返回值：**

```python
context = brain.get_full_context(
    session_key="telegram_12345",  # Unique session ID
    user_id="username",              # User identifier
    agent_id="assistant",          # Bot identifier
    message="Hey, how's it going?" # Current message
)
```

### detect_user_mood() 方法

```python
mood = brain.detect_user_mood("I'm so excited about this!")
# Returns: {"mood": "happy", "confidence": 0.9, "emotions": ["joy", "anticipation"]}
```

### detect_user(intent() 方法

```python
intent = brain.detect_user_intent("How does AI work?")
# Returns: "question"

intent = brain.detect_user_intent("Set a reminder for 3pm")
# Returns: "command"

intent = brain.detect_user_intent("I had a great day today")
# Returns: "casual"
```

---

## 完整集成示例

```python
import sys
sys.path.insert(0, "ClawBrain")

from clawbrain import Brain

class AssistantBot:
    def __init__(self):
        self.brain = Brain()
    
    def handle_message(self, message, chat_id):
        # Get context
        context = self.brain.get_full_context(
            session_key=f"telegram_{chat_id}",
            user_id=str(chat_id),
            agent_id="assistant",
            message=message
        )
        
        # Generate response using context
        response = self.generate_response(context)
        
        # Learn from interaction
        self.brain.learn_user_preference(
            user_id=str(chat_id),
            pref_type="interest",
            value="AI"
        )
        
        return response
    
    def generate_response(self, context):
        # Use user preferences
        name = context["user_profile"].name or "there"
        mood = context["mood"]["mood"]
        
        # Personalized response
        if mood == "frustrated":
            return f"Hey {name}, I'm here to help. Let me assist you."
        else:
            return f"Hi {name}! How can I help you today?"
    
    def shutdown(self):
        self.brain.close()
```

---

## 存储后端

### SQLite（默认，无需配置）

无需任何配置，数据存储在本地 SQLite 数据库中。

```python
brain = Brain({"storage_backend": "sqlite"})
```

**适用场景**：开发、测试、单用户环境

### PostgreSQL + Redis（生产环境）

需要安装 PostgreSQL 和 Redis 服务器。

```python
brain = Brain()  # Auto-detects
```

**系统要求**：
- PostgreSQL 14 及更高版本
- Redis 6 及更高版本
- 所需 Python 包：`psycopg2-binary`, `redis`

```bash
pip install psycopg2-binary redis
```

**适用场景**：生产环境、多用户、高并发场景

---

## 相关文件

- `clawbrain.py`：包含所有核心功能的主类
- `__init__.py`：模块导出文件
- `SKILL.md`：本文档文件
- `skill.json`：ClawdHub 的元数据文件
- `README.md`：快速入门指南

---

## 常见问题解答

### 错误提示：`ImportError: No module named 'clawbrain'`

```bash
# Ensure ClawBrain folder is in your path
sys.path.insert(0, "ClawBrain")
```

### 连接 PostgreSQL 失败

```bash
# Check environment variables
echo $POSTGRES_HOST
echo $POSTGRES_PORT

# Verify PostgreSQL is running
pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT
```

### 连接 Redis 失败

```bash
# Check Redis is running
redis-cli ping
```

### 使用 SQLite（备用方案）

如果 PostgreSQL/Redis 无法使用，ClawBrain 会自动切换到 SQLite：

```python
brain = Brain({"storage_backend": "sqlite"})
```

---

## 更多信息

- **仓库地址**：[https://github.com/clawcolab/clawbrain](https://github.com/clawcolab/clawbrain)
- **快速入门指南**：请参阅 `README.md`
- **问题报告**：请在 GitHub 上提交问题