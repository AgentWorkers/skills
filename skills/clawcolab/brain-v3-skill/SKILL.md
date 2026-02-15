---
name: clawbrain
version: 0.1.10
description: "**Claw Brain** – 专为 OpenClaw/ClawDBot 设计的个人 AI 记忆系统  
该系统具备存储数据、塑造机器人“个性”、促进机器人与用户之间的互动以及支持加密数据存储的功能。在服务重启时，系统会自动更新其内部数据。"
metadata: {"openclaw":{"emoji":"🧠","category":"memory","provides":{"slot":"memory"},"events":["gateway:startup","command:new"]},"clawdbot":{"emoji":"🧠","category":"memory","provides":{"slot":"memory"},"events":["gateway:startup","command:new"]}}
---

# Claw Brain 技能 🧠

这是一个专为 OpenClaw/ClawDBot 设计的个性化 AI 记忆系统，具备灵魂、情感联结和学习功能。

> **重启时自动刷新**：当服务重启时，ClawBrain 会自动刷新记忆数据。

## 主要特性

- 🎭 **灵魂/个性**：6 个可发展的特质（幽默感、同理心、好奇心、创造力、乐于助人、诚实）
- 👤 **用户资料**：学习用户的偏好、兴趣和沟通风格
- 💭 **对话状态**：实时检测用户情绪并跟踪对话上下文
- 📚 **学习能力**：通过互动和反馈持续学习
- 🧠 **get_full_context()**：提供个性化响应所需的所有信息
- 🔄 **自动刷新**：服务重启时自动更新记忆数据
- 🔐 **加密保护**：安全存储 API 密钥和凭证

---

## 快速安装

### 通过 PyPI 安装（推荐）

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
1. 识别您的平台（ClawdBot 或 OpenClaw）
2. 生成一个安全的加密密钥
3. 自动安装启动钩子
4. 测试安装是否成功

### 或者：从源代码安装

```bash
# Clone to your skills directory
cd ~/.openclaw/skills  # or ~/clawd/skills or ~/.clawdbot/skills
git clone https://github.com/clawcolab/clawbrain.git
cd clawbrain
pip install -e .[all]
clawbrain setup
```

---

## 配置

安装完成后，您可以选择配置代理 ID：

```bash
# Create systemd drop-in config
sudo mkdir -p /etc/systemd/system/clawdbot.service.d  # or openclaw.service.d

sudo tee /etc/systemd/system/clawdbot.service.d/brain.conf << EOF
[Service]
Environment="BRAIN_AGENT_ID=your-agent-name"
# Optional: PostgreSQL (for production)
# Environment="BRAIN_POSTGRES_HOST=localhost"
# Environment="BRAIN_POSTGRES_PASSWORD=your-password"
# Optional: Redis (for caching)
# Environment="BRAIN_REDIS_HOST=localhost"
EOF

sudo systemctl daemon-reload
sudo systemctl restart clawdbot  # or openclaw
```

### 环境变量

| 变量          | 描述                                      | 默认值        |
|-----------------|-----------------------------------------|-------------|
| BRAIN_AGENT_ID     | 该代理的记忆的唯一标识符                         | `default`       |
| BRAIN_ENCRYPTION_KEY | 用于加密敏感数据的 Fernet 密钥（未设置时自动生成）       | -            |
| BRAIN_POSTGRES_HOST   | PostgreSQL 服务器地址                          | `localhost`     |
| BRAIN_POSTGRES_PASSWORD | PostgreSQL 密码                             | -            |
| BRAIN_POSTGRES_PORT    | PostgreSQL 端口                          | `5432`       |
| BRAIN_POSTGRES_DB     | 使用的 PostgreSQL 数据库名称                     | `brain_db`     |
| BRAIN_POSTGRES_USER   | PostgreSQL 用户名                          | `brain_user`     |
| BRAIN_REDIS_HOST   | Redis 服务器地址                          | `localhost`     |
| BRAIN_REDIS_PORT    | Redis 端口                          | `6379`       |
| BRAIN_STORAGE     | 数据存储方式（可选：sqlite、postgresql、auto）           | `auto`        |

---

## 工作原理

### 服务启动时
1. 在 `gateway:startup` 事件触发时初始化 ClawBrain
2. 检测配置的存储后端（SQLite 或 PostgreSQL）
3. 加载与 `BRAIN_AGENT_ID` 相关的记忆数据
4. 将对话上下文信息注入代理的启动流程中

### 执行 `/new` 命令时
1. 在 `command:new` 事件触发时将当前会话信息保存到内存中
2. 清除会话状态以便重新开始对话

### 数据存储优先级
1. **PostgreSQL**：如果可用且已配置，则优先使用
2. **SQLite**：作为备用方案，无需额外配置

---

## 加密保护

ClawBrain 支持加密 API 密钥和凭证等敏感数据。

**设置方法：**
```bash
# Run setup to generate encryption key
clawbrain setup

# Backup your key (IMPORTANT!)
clawbrain backup-key --all
```

**使用方法：**
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

**密钥管理命令行工具：**
```bash
clawbrain show-key          # View key info (masked)
clawbrain show-key --full   # View full key
clawbrain backup-key --all  # Backup with all methods
clawbrain generate-key      # Generate new key
```

**重要提示：** 请务必备份您的加密密钥！密钥丢失会导致加密数据丢失。

---

## 命令行接口

ClawBrain 提供了以下命令行接口：

| 命令        | 功能                                        |
|-------------|---------------------------------------------|
| `clawbrain setup` | 设置 ClawBrain、生成密钥并安装启动钩子                |
| `clawbrain generate-key` | 生成新的加密密钥                        |
| `clawbrain show-key` | 显示当前的加密密钥                        |
| `clawbrain backup-key` | 备份密钥（文件、二维码或剪贴板）                      |
| `clawbrain health` | 检查系统运行状态                        |
| `clawbrain info` | 显示安装信息                            |

---

## 启动钩子

| 事件          | 执行的操作                                      |
|--------------|---------------------------------------------|
| `gateway:startup` | 初始化 ClawBrain 并刷新记忆数据                        |
| `command:new`    | 将当前会话信息保存到内存中                        |

---

## 开发环境安装

适用于开发或手动安装场景：

```bash
# Clone to your skills directory
cd ~/.openclaw/skills  # or ~/clawd/skills or ~/.clawdbot/skills
git clone https://github.com/clawcolab/clawbrain.git
cd clawbrain
./install.sh
```

---

## Python API

支持在 ClawdBot/OpenClaw 之外直接使用 ClawBrain 的 Python API：

```python
from clawbrain import Brain

brain = Brain()
```

#### 方法列表

| 方法            | 功能                                        | 返回值         |
|-----------------|---------------------------------------------|-------------------|
| `get_full_context()` | 获取所有用于个性化响应的上下文信息                | dict            |
| `remember()`      | 存储新的记忆数据                              | None            |
| `recall()`       | 检索已存储的记忆数据                              | List[Memory]       |
| `learn_user_preference()` | 学习用户的偏好设置                              | None            |
| `get_user_profile()` | 获取用户资料                              | UserProfile       |
| `detect_user_mood()` | 检测用户的当前情绪                        | dict            |
| `detect_user(intent()` | 分析用户的意图                              | str            |
| `generate_personality_prompt()` | 生成个性化的引导语                         | str            |
| `health_check()`     | 检查与后端的连接状态                        | dict            |
| `close()`        | 关闭所有连接                                  | None            |

### `get_full_context()`

**返回值：**
```python
{
    "user_profile": {...},        # User preferences, interests
    "mood": {"mood": "happy", ...},  # Current mood
    "intent": "question",         # Detected intent
    "memories": [...],            # Relevant memories
    "personality": "...",         # Personality guidance
    "suggested_responses": [...]  # Response suggestions
}
```

### `detect_user_mood()`

### `detect_user(intent()`

### `detect_user(intent()`

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

## 数据存储方式

### SQLite（默认配置，无需额外设置）

数据存储在本地 SQLite 数据库中。

**适用场景：** 开发、测试及单用户环境

### PostgreSQL + Redis（生产环境推荐）

需要安装 PostgreSQL 和 Redis 服务器。

```python
brain = Brain()  # Auto-detects
```

**系统要求：**
- PostgreSQL 14 及以上版本
- Redis 6 及以上版本
- 必需的 Python 包：`psycopg2-binary`、`redis`

**适用场景：** 生产环境、多用户场景及高并发需求

---

## 相关文件

- `clawbrain.py`：包含所有核心功能的 Python 类文件
- `__init__.py`：模块导出文件
- `SKILL.md`：本文档文件
- `skill.json`：ClawdHub 的元数据文件
- `README.md`：快速入门指南

---

## 常见问题解答

### 错误提示：`ImportError: No module named 'clawbrain'`

**解决方法：** 确保已正确安装 ClawBrain 相关模块。

### PostgreSQL 连接失败

**解决方法：** 检查 PostgreSQL 服务器是否正常运行，并检查连接配置。

### Redis 连接失败

**解决方法：** 检查 Redis 服务器是否正常运行，并检查连接配置。

### 使用 SQLite（备用方案）

如果 PostgreSQL 或 Redis 无法使用，ClawBrain 会自动切换到 SQLite 数据存储模式。

---


## 更多信息

- **项目仓库：** https://github.com/clawcolab/clawbrain
- **快速入门指南：** 查看 `README.md`
- **问题报告：** 在 GitHub 的 Issues 中提交问题反馈。