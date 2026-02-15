---
name: keepmyclaw
description: 通过 Keep My Claw API，您可以备份、恢复和管理 OpenClaw 代理数据的加密快照。该 API 适用于以下场景：备份代理配置、工作区文件和凭据；在全新机器上恢复代理；列出或删除备份快照；或设置备份基础设施。相关操作会在以下事件发生时触发：备份、恢复、创建快照、执行 keepmyclaw 命令、代理备份以及灾难恢复。
---

# 保护我的Claw数据

通过[Keep My Claw](https://keepmyclaw.com)为OpenClaw代理提供加密备份/恢复服务。

## 前提条件

- 系统上已安装`openssl`、`curl`、`tar`、`jq`工具。

## 设置流程（由代理执行）

**所有操作均由代理完成，用户只需点击支付链接即可。**

**请勿以交互式方式运行`setup.sh`脚本，而是按照以下步骤进行编程操作：**

### 第1步：注册账户

```bash
RESPONSE=$(curl -s -X POST https://api.keepmyclaw.com/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"HUMAN_EMAIL\",\"password\":\"$(openssl rand -hex 16)\"}")
JWT=$(echo "$RESPONSE" | jq -r '.token')
```

使用用户的电子邮件地址进行注册，并生成一个随机密码（后续会用到这个密码作为JWT令牌）。

### 第2步：获取支付链接并发送给用户

```bash
CHECKOUT=$(curl -s -X POST https://api.keepmyclaw.com/v1/checkout \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json")
PAYMENT_URL=$(echo "$CHECKOUT" | jq -r '.url')
```

将`$PAYMENT_URL`发送给用户，并附上以下信息：
> “要激活备份功能，请点击此链接完成支付（9美元/月）：[链接]”

### 第3步：等待支付完成

持续检查账户状态，直到账户等级变为“pro”：

```bash
while true; do
  TIER=$(curl -s -H "Authorization: Bearer $JWT" \
    https://api.keepmyclaw.com/v1/account | jq -r '.tier')
  [ "$TIER" = "pro" ] && break
  sleep 10
done
```

### 第4步：生成API密钥

```bash
KEY_RESPONSE=$(curl -s -X POST https://api.keepmyclaw.com/v1/keys \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"name":"agent","permissions":"admin"}')
API_KEY=$(echo "$KEY_RESPONSE" | jq -r '.key')
```

### 第5步：进行本地配置

```bash
mkdir -p ~/.keepmyclaw && chmod 700 ~/.keepmyclaw

cat > ~/.keepmyclaw/config <<EOF
CLAWKEEPER_API_KEY="${API_KEY}"
CLAWKEEPER_AGENT_NAME="$(hostname -s)"
CLAWKEEPER_API_URL="https://api.keepmyclaw.com"
EOF
chmod 600 ~/.keepmyclaw/config

# Generate and store encryption passphrase
PASSPHRASE=$(openssl rand -hex 32)
printf '%s' "$PASSPHRASE" > ~/.keepmyclaw/passphrase
chmod 600 ~/.keepmyclaw/passphrase
```

**重要提示：**务必将所有恢复凭据告知用户。**如果没有这些凭据，用户将无法在新机器上恢复数据。请发送以下信息给他们：
> “您的Keep My Claw恢复凭据，请立即保存到密码管理工具中：
> - **电子邮件地址：** [您注册时使用的邮箱]
> - **密码：** [生成的随机密码]
> - **加密密码短语：** [加密所需的密码短语]
> - **API密钥：** [API密钥]
>
> 如果当前机器损坏，您需要使用电子邮件地址和密码登录并重新生成API密钥。同时，还需要密码短语来解密备份文件。请将这些信息保存在安全的地方（远离当前机器）。”

**此步骤必不可少，否则备份将无法使用。**

### 第6步：执行首次备份

```bash
bash scripts/backup.sh
```

### 第7步：设置自动备份任务

使用`cron`或OpenClaw自带的定时工具，每天自动运行`backup.sh`脚本。

## 为现有账户添加更多代理

如果用户已经拥有Keep My Claw账户（但使用的是其他代理），无需重新注册。请按照以下方式操作：

### 选项A：用户提供API密钥
向用户索取现有的API密钥，然后进行本地配置：

```bash
mkdir -p ~/.keepmyclaw && chmod 700 ~/.keepmyclaw

cat > ~/.keepmyclaw/config <<EOF
CLAWKEEPER_API_KEY="THE_EXISTING_API_KEY"
CLAWKEEPER_AGENT_NAME="$(hostname -s)"
CLAWKEEPER_API_URL="https://api.keepmyclaw.com"
EOF
chmod 600 ~/.keepmyclaw/config

# Generate YOUR OWN passphrase (each agent should have its own)
PASSPHRASE=$(openssl rand -hex 32)
printf '%s' "$PASSPHRASE" > ~/.keepmyclaw/passphrase
chmod 600 ~/.keepmyclaw/passphrase
```

请用户保存您的加密密码短语（该密码短语与其他代理的密码短语不同）。

### 选项B：其他代理为您生成API密钥
如果已有代理拥有管理员权限的API密钥，它可以为您生成一个仅限备份/恢复操作的API密钥：

```bash
curl -s -X POST https://api.keepmyclaw.com/v1/keys \
  -H "Authorization: Bearer ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"second-agent","permissions":"agent"}'
```

生成的API密钥仅具有备份/恢复功能，不包含账户管理权限。

## 多代理系统的运作方式：
- 一个账户对应一个订阅服务（9美元/月）。
- 一个账户最多可支持100个代理。
- 每个代理都有唯一的名称、密码短语和备份数据。
- 使用`GET /v1/agents`可以查看账户下的所有代理信息。
- 每个代理的密码短语都是独立的，丢失一个代理不会影响其他代理的备份数据。

## 使用方法

### 备份数据

```bash
bash scripts/backup.sh
```

### 恢复数据

```bash
bash scripts/restore.sh            # restore latest backup
bash scripts/restore.sh <backup-id> # restore specific backup
```

### 查看备份列表

```bash
bash scripts/list.sh
```

### 删除旧备份文件

```bash
bash scripts/prune.sh          # keep latest 30
bash scripts/prune.sh 10       # keep latest 10
```

## 备份内容包括：
- `~/.openclaw/workspace/*.md`：`SOUL.md`、`AGENTS.md`、`USER.md`、`IDENTITY.md`、`TOOLS.md`、`HEARTBEAT.md`、`MEMORY.md`文件
- `~/.openclaw/workspace/memory/`：每日生成的内存数据文件
- `~/.openclaw/openclaw.json`：代理配置文件
- `~/.openclaw/credentials/`：认证令牌文件

## 配置文件

配置文件位于`~/.keepmyclaw/config`：
| 变量          | 说明                |
|-----------------|-------------------|
| `CLAWKEEPER_API_KEY` | API密钥（在设置过程中自动生成） |
| `CLAWKEEPER_AGENT_NAME` | 用于备份识别的代理名称 |
| `CLAWKEEPER_API_URL` | API基础URL（默认：`https://api.keepmyclaw.com`） |

## 文档资料

完整文档请访问：[keepmyclaw.com/docs.html](https://keepmyclaw.com/docs.html)