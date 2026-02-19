# identity-resolver

**跨消息渠道的统一用户身份解析**

## 描述

该工具能够解析来自多个渠道（Telegram、WhatsApp、Discord、网页等）的用户身份信息，将其统一转换为标准的用户ID，从而避免用户在多个渠道间交互时导致的状态碎片化问题。

**解决的问题：**  
如果没有身份解析机制，用户在Telegram和WhatsApp上的消息记录会被视为两个不同的用户，这会导致内存管理混乱、访问控制问题以及每个用户的状态信息分散在不同系统中。

**解决方案：**  
系统会自动将所有渠道的用户身份映射到一个标准的用户ID上。

## 安装

**先决条件：**  
如果尚未安装`uv`，请先安装它：  
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**安装该工具：**  
```bash
cd /path/to/openclaw/workspace

# Via ClawHub (recommended)
clawhub install identity-resolver

# Or via Git
git clone https://github.com/clawinfra/identity-resolver skills/identity-resolver
```

## 快速入门

### 对于最终用户  

```bash
# Initialize identity map (auto-detects owner from USER.md)
cd /path/to/workspace
uv run python skills/identity-resolver/scripts/identity_cli.py init

# Verify your identity
uv run python skills/identity-resolver/scripts/identity_cli.py resolve \
  --channel telegram --user-id YOUR_TELEGRAM_ID
# Output: your-canonical-id

# List all registered identities
uv run python skills/identity-resolver/scripts/identity_cli.py list
```

### 对于技能开发者  

请将以下代码添加到您的技能的Python代码中：  
```python
import sys
from pathlib import Path

# Import identity resolver
sys.path.insert(0, str(Path.cwd() / "skills" / "identity-resolver" / "scripts"))
from identity import resolve_canonical_id

# Get canonical user ID from session context
import os
channel = os.getenv("OPENCLAW_CHANNEL")  # e.g., "telegram"
user_id = os.getenv("OPENCLAW_USER_ID")   # e.g., "123456789"

canonical_id = resolve_canonical_id(channel, user_id)
# Use canonical_id for all user-specific operations

# Example: User-specific memory file
memory_file = f"data/users/{canonical_id}/memory.json"
```

## 主要功能  

✅ 从`WORKSPACE_USER.md`文件中自动注册用户信息  
✅ 使用`fcntl`锁定机制实现线程安全的身份映射存储  
✅ 提供命令行接口（CLI）和Python API，供用户和开发者使用  
✅ 提供路径遍历保护功能，确保所有标准用户ID的格式正确  
✅ 无依赖项，仅使用Python标准库  
✅ 支持多种渠道：Telegram、WhatsApp、Discord、网页等  

## 使用场景  

### 多用户内存管理系统  
```python
# tiered-memory skill integration
canonical_id = resolve_canonical_id(channel, user_id)
memory_tree = f"memory/users/{canonical_id}/tree.json"
```

### 访问控制  
```python
# agent-access-control skill integration
canonical_id = resolve_canonical_id(channel, user_id)
if is_owner(canonical_id):
    # Full access
else:
    # Limited access
```

### 跨平台用户跟踪  
```python
# Same user across Discord + Telegram
discord_id = resolve_canonical_id("discord", "user#1234")
telegram_id = resolve_canonical_id("telegram", "987654321")
# Both resolve to same canonical ID if registered
```

## API参考  

### 核心函数  

**`resolve_canonical_id(channel, provider_user_id, workspace=None, owner_numbers=None) -> str`**  
将渠道身份解析为标准用户ID。  
- 会自动从`WORKSPACE_USER.md`文件中注册用户信息  
- 返回标准用户ID（例如“alice”），或对于未注册的用户返回“stranger:{channel}:{user_id}”  

**`add_channel(canonical_id, channel, provider_user_id, workspace=None, display_name=None)`**  
将渠道与标准用户ID关联起来（如果用户不存在，则创建新用户）  

**`remove_channel(canonical_id, channel, provider_user_id, workspace=None)`**  
从标准用户ID中删除对应的渠道关联  

**`list_identities workspace=None) -> dict`**  
返回所有用户身份的映射关系  

**`get_channels(canonical_id, workspace=None) -> list`**  
获取某个标准用户的所有使用渠道  

**`is_owner(canonical_id, workspace=None) -> bool`**  
检查该标准用户ID是否属于当前用户  

### 命令行接口（CLI）命令  

```bash
# Initialize
identity init [--force]

# Resolve (auto-detect from env or explicit params)
identity resolve [--channel CH] [--user-id ID]

# Add mapping
identity add --canonical ID --channel CH --user-id ID [--display-name NAME]

# Remove mapping
identity remove --canonical ID --channel CH --user-id ID

# List all
identity list [--json]

# Get channels
identity channels --canonical ID [--json]

# Check owner
identity is-owner --canonical ID [--json]
```

## 身份映射格式  

存储路径：`data/identity-map.json` 或 `memory/identity-map.json`  

```json
{
  "version": "1.0",
  "identities": {
{
  "version": "1.0",
  "identities": {
    "alice": {
      "canonical_id": "alice",
      "is_owner": true,
      "display_name": "Alice Johnson",
      "channels": [
        "telegram:123456789",
        "whatsapp:+1234567890",
        "whatsapp:+9876543210",
        "whatsapp:+5555555555"
      ],
      "created_at": "2026-01-15T10:00:00Z",
      "updated_at": "2026-01-15T10:05:00Z"
    },
    "bob": {
      "canonical_id": "bob",
      "is_owner": false,
      "display_name": "Bob Smith",
      "channels": [
        "discord:bob#1234",
        "telegram:987654321"
      ],
      "created_at": "2026-01-15T10:10:00Z",
      "updated_at": "2026-01-15T10:10:00Z"
    }
  }
}
    }
  }
}
```

## 安全性  

- **路径遍历保护**：确保所有标准用户ID仅包含字母、数字和下划线（`[a-z0-9-_]`）  
- **线程安全操作**：所有读写操作都使用`fcntl`进行文件锁定  
- **输入验证**：所有用户输入都会经过验证和清洗  
- **自动注册用户**：仅将`WORKSPACE_USER.md`文件中的数字信息注册为合法的用户ID  

## 集成示例  

请参阅`docs/TIERED_MEMORY_INTEGRATION_EXAMPLE.md`以获取完整的集成示例。  

## 许可证  

MIT许可证——详见LICENSE文件  

## 作者  

OpenClaw Agent <agent@openclaw.local>  

## 链接  

- GitHub：https://github.com/clawinfra/identity-resolver  
- 问题反馈：https://github.com/clawinfra/identity-resolver/issues  
- ClawHub：https://clawhub.com/skills/identity-resolver