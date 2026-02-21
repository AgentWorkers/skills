---
name: fatsecret
description: FatSecret 营养 API 支持以下功能：食物搜索、营养信息查询、条形码扫描、食谱搜索以及食物日记记录。当用户需要获取食物的营养信息、查询食物数据库、扫描产品条形码、查看卡路里/宏量营养素/微量营养素含量、搜索健康食谱，或将餐食记录到 FatSecret 日记中时，可以使用该 API。
metadata:
  credentials:
    required:
      - name: FATSECRET_CONSUMER_KEY
        description: FatSecret API Consumer Key (get from platform.fatsecret.com)
      - name: FATSECRET_CONSUMER_SECRET
        description: FatSecret API Consumer Secret
    optional:
      - name: FATSECRET_PROXY
        description: SOCKS5 proxy URL if FatSecret requires IP whitelisting (e.g., socks5://127.0.0.1:1080)
      - name: FATSECRET_CONFIG_DIR
        description: Custom config directory (default ~/.config/fatsecret). Use for persistent storage in containers.
---
# FatSecret Nutrition API

本API可与FatSecret平台完全集成，用于查询食物信息并记录饮食日记。

## ⚠️ 认证方式

本技能支持**两种认证方式**，以适应不同的使用场景：

| 认证方式 | 使用场景 | 是否需要用户登录 | 功能 |
|--------|----------|---------------------|--------------|
| **OAuth2**（使用客户端凭据） | 仅读访问 | ❌ 不需要 | 食物搜索、条形码查询、食谱查找 |
| **OAuth1**（三重认证） | 全部访问权限 | ✅ 需要（一次性PIN码验证） | 上述所有功能 + 饮食日记记录 |

### 应该如何选择？
- **仅用于搜索食物？** → 选择OAuth2（更简单，无需登录）
- **需要记录到用户饮食日记中？** → 选择OAuth1（需要用户授权）

## 🚀 快速入门

### 1. 获取API凭据
1. 访问 https://platform.fatsecret.com
2. 注册一个应用程序
3. 复制您的**消费者密钥**（Consumer Key）和**消费者秘密**（Consumer Secret）

### 2. 保存凭据
```bash
mkdir -p ~/.config/fatsecret
cat > ~/.config/fatsecret/config.json << EOF
{
  "consumer_key": "YOUR_CONSUMER_KEY",
  "consumer_secret": "YOUR_CONSUMER_SECRET"
}
EOF
```

### 3. 安装依赖项
```bash
cd /path/to/fatsecret-skill
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4a. 仅读访问（OAuth2） - 无需用户登录
```bash
# Search works immediately
./scripts/fatsecret-cli.sh search "chicken breast"
```

### 4b. 记录饮食日记（OAuth1） - 需要一次性用户授权
```bash
# Run authentication flow
./scripts/fatsecret-cli.sh auth

# Follow prompts:
# 1. Visit the authorization URL
# 2. Log in with FatSecret account
# 3. Authorize the app
# 4. Enter the PIN shown

# Now you can log foods
./scripts/fatsecret-cli.sh quick egg 3 Breakfast
```

## 📋 命令行工具（CLI）命令

| 命令 | 是否需要认证 | 描述 |
|---------|---------------|-------------|
| `search <查询>` | OAuth2 | 搜索食物 |
| `barcode <条形码>` | OAuth2 | 查找条形码对应的食物 |
| `recipes <查询>` | OAuth2 | 搜索食谱 |
| `auth` | - | 运行OAuth1认证 |
| `log` | OAuth1 | 将食物添加到饮食日记中（交互式） |
| `quick <食物> [数量] [餐次]` | OAuth1 | 快速记录到饮食日记中 |

## 🤖 代理集成

### 对于OpenClaw代理

```python
from scripts.fatsecret_agent_helper import (
    get_authentication_flow,
    complete_authentication_flow,
    save_user_credentials
)

# Check authentication status
state = get_authentication_flow()

if state["status"] == "need_credentials":
    # Ask user for Consumer Key/Secret
    # Save with: save_user_credentials(key, secret)
    pass

elif state["status"] == "need_authorization":
    # Show authorization URL to user
    url = state["authorization_url"]
    # User visits URL, authorizes, gets PIN
    # Complete with: complete_authentication_flow(pin)
    pass

elif state["status"] == "already_authenticated":
    # Ready to use diary functions
    from scripts.fatsecret_diary_simple import quick_log
    quick_log("egg", quantity=3, meal="Breakfast")
```

### 代理辅助函数

| 函数 | 描述 |
|----------|-------------|
| `get_authentication_flow()` | 检查认证状态，返回下一步操作 |
| `save_user_credentials(key, secret)` | 保存API凭据 |
| `complete_authentication_flow(pin)` | 使用PIN码完成OAuth1认证 |
| `quick_log(food, qty, meal)` | 将食物记录到饮食日记中 |
| `log_food(food_id, serving_id, 克数或毫升, 餐次, 名称)` | 详细记录食物信息 |
| `search_food(query, tokens)` | 搜索食物 |

### ⚠️ 重要说明：`grams_or_ml` 参数的用法

`grams_or_ml` 参数（在FatSecret API中称为 `number_of_units`）表示**实际数量**，而非单位换算系数！

**示例：**
| 需要查询的信息 | 食物单位 | `grams_or_ml` 值 |
|---------------|--------------|-------------------|
| 156克饼干 | “100克”一份 | `156` |
| 200毫升牛奶 | “100毫升”一份 | `200` |
| 3个鸡蛋 | “1个大鸡蛋”一份 | `3` |
| 2片面包 | “1片”一份 | `2` |

## 🔐 凭据存储

所有凭据和令牌均存储在本地：

| 文件 | 内容 | 创建者 |
|------|----------|------------|
| `$CONFIG_DIR/config.json` | 消费者密钥/秘密 | 用户（手动设置） |
| `$CONFIG_DIR/oauth1_access_tokens.json` | OAuth1访问令牌 | `auth` 命令生成 |
| `$CONFIG_DIR/token.json` | OAuth2令牌（自动刷新） | OAuth2客户端使用 |

其中 `$CONFIG_DIR` 的默认值为 `~/.config/fatsecret`，也可通过设置 `FATSECRET_CONFIG_DIR` 来更改。

**撤销访问权限的方法：** 删除 `config` 文件夹，并在FatSecret账户设置中取消该应用程序的访问权限。

### 🐳 容器/Docker环境

在容器化环境（如Docker、OpenClaw沙箱）中，`~/.config/` 目录可能无法在重启后保持其内容。请使用 `FATSECRET_CONFIG_DIR` 指向一个持久化的存储目录：

```bash
# Set env var to persistent directory
export FATSECRET_CONFIG_DIR="/home/node/clawd/config/fatsecret"

# Or prefix commands
FATSECRET_CONFIG_DIR="/persistent/path" ./scripts/fatsecret-cli.sh auth
```

**OpenClaw示例** - 可将相关配置添加到您的shell初始化脚本或 `AGENTS.md` 文件中：
```bash
export FATSECRET_CONFIG_DIR="/home/node/clawd/config/fatsecret"
```

## 🌐 代理配置（可选）

某些FatSecret API计划可能需要IP白名单。如有需要，请设置代理：

```bash
# Environment variable
export FATSECRET_PROXY="socks5://127.0.0.1:1080"

# Or in config.json
{
  "consumer_key": "...",
  "consumer_secret": "...",
  "proxy": "socks5://127.0.0.1:1080"
}
```

**如果不需要代理：** 本技能无需代理即可正常使用。只有在FatSecret限制您的IP地址访问时才需要代理。

## 🌍 Open Food Facts（替代方案）

对于欧洲地区的食品，可以使用免费的Open Food Facts API（无需认证）：

```python
from scripts.openfoodfacts_client import OpenFoodFactsClient

off = OpenFoodFactsClient(country="it")
products = off.search("barilla")
product = off.get_product("8076800105735")  # Barcode
```

## 📁 文件结构

```
fatsecret/
├── SKILL.md                      # This documentation
├── README.md                     # GitHub/ClawHub readme
├── requirements.txt              # Python: requests, requests[socks]
├── scripts/
│   ├── fatsecret-cli.sh          # Main CLI (bash wrapper)
│   ├── fatsecret_auth.py         # OAuth1 3-legged authentication
│   ├── fatsecret_agent_helper.py # Helper functions for agents
│   ├── fatsecret_diary_simple.py # Diary logging (OAuth1)
│   ├── fatsecret_client.py       # OAuth2 client (read-only)
│   └── openfoodfacts_client.py   # Open Food Facts client
└── examples/
    └── agent_usage_example.py    # Agent integration example
```

## ⚠️ 安全注意事项

1. **凭据存储在本地目录 `~/.config/fatsecret/` 中**
2. **OAuth1令牌不会自动过期**，除非您主动撤销它们
3. **OAuth1认证会授予您对FatSecret饮食日记的完整访问权限（读写）**
4. **安全卸载应用程序的方法：** 删除 `~/.config/fatsecret/` 目录，并在FatSecret账户中取消该应用程序的访问权限

## 🔗 参考资料

- FatSecret API文档：https://platform.fatsecret.com/docs
- OAuth1认证指南：https://platform.fatsecret.com/docs/guides/authentication/oauth1/three-legged
- Open Food Facts API：https://wiki.openfoodfacts.org/API

## 更新日志

### v1.0.1（2026-02-20）
- 修复了OAuth2客户端的问题：现在所有操作（食物搜索和日记记录）均使用OAuth1认证
- 统一了认证流程：无论是读写操作都使用相同的OAuth1认证方式
- 移除了有问题的OAuth2实现