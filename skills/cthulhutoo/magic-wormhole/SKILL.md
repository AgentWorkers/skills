---
name: magic-wormhole
description: 使用 magic-wormhole 协议为 OpenClaw 实现安全的秘密共享功能
homepage: https://github.com/magic-wormhole/magic-wormhole
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🔐"
    requires:
      env: []
    primaryEnv: null
    files: ["install.sh", "docs/*", "examples/*"]
  author:
    name: Stateless Collective
    url: https://stateless.id
  attribution:
    - "Created by Stateless Collective AI Committee (https://stateless.id)"
    - "Based on magic-wormhole by Brian Warner and contributors (https://github.com/magic-wormhole/magic-wormhole)"
    - "License: MIT (matches magic-wormhole)"
tags: security, secrets, encryption, privacy, tools, ssh, api-keys, credentials
---
# Magic Wormhole 技能 - 安全秘密共享

## 描述

该技能使 OpenClaw 代理能够安全地与人类用户共享秘密（如 SSH 密钥、API 令牌、密码、证书等敏感数据），同时避免这些秘密被记录在聊天历史或日志中。

Magic Wormhole 是一个基于 Python 的安全文件和文本传输工具，它使用了 PAKE（密码认证密钥交换，Password-Authenticated Key Exchange）协议。秘密通过人类可读的代码（例如 `7-blue-rabbit`）进行传输，从而实现端到端加密通信，无需预先共享密钥或证书。

### 主要特点

- **零泄露**：秘密永远不会出现在聊天日志或代理的响应中。
- **简单的工作流程**：只需分享简短的代码即可，无需分享完整的秘密。
- **代理到人类用户及人类用户到代理**：支持双向传输。
- **可脚本化且易于自动化**：易于集成到代理的工作流程中。
- **可自托管**：可以运行自己的服务器以保障生产环境的安全性。
- **跨平台**：支持 Linux、macOS、Windows 和移动设备。

---

## 使用场景

### 何时使用此技能

✅ **适用于以下场景：**
- **SSH 密钥分发**：安全地生成并发送 SSH 密钥。
- **API 令牌传输**：在不暴露密钥的情况下分享 API 令牌。
- **密码轮换**：在密码轮换时分发新的凭证。
- **证书共享**：传输 SSL/TLS 证书或密钥。
- **秘密文件传输**：发送包含敏感数据的配置文件。
- **团队凭证分发**：与团队成员共享临时凭证。
- **隔离环境**：在无法直接访问的情况下传输秘密。
- **审计追踪需求**：通过将秘密排除在日志之外来维护安全性。

❌ **不适用以下场景：**
- **大文件传输（超过 100MB）**：请使用专用的文件传输工具。
- **非敏感的公共数据**。
- **需要持续共享通道的情况**（因为 Wormhole 代码是一次性使用的）。

### 示例场景

1. **部署设置**：代理生成服务器访问所需的 SSH 密钥，并通过 Wormhole 发送。
2. **API 集成**：人类用户向代理分享 API 令牌以进行配置。
3. **事件响应**：与安全团队共享临时凭证。
4. **新员工入职**：新员工通过安全传输方式接收访问权限。
5. **秘密轮换**：自动进行密码轮换并安全分发新凭证。

---

## 先决条件

### 所需工具

- **wormhole CLI**：基于 Python 的安全传输工具。
- **bash** 或兼容的 shell：用于运行安装和示例脚本。
- **OpenClaw 代理**：具备执行 shell 命令的功能（`exec` 工具）。

### 平台支持

| 平台 | 安装方法 | 测试情况 |
|----------|---------------------|--------|
| Linux (Debian/Ubuntu) | `apt`, `snap`, `pip` | ✅ |
| Linux (Fedora) | `dnf`, `pip` | ✅ |
| Linux (openSUSE) | `zypper`, `pip` | ✅ |
| macOS | Homebrew, `pip` | ✅ |
| Windows | `pip` | ⚠️ 有限支持 |

### 网络要求

- **出站 HTTPS**：需要连接到默认的会合服务器（`relay.magic-wormhole.io`）。
- **WebSocket 支持**：用于中继通信。
- **可选**：如果网络环境允许，可以使用直接 P2P 连接。

---

## 安装

### 方法 1：自动脚本（推荐）

运行随此技能提供的安装脚本：

```bash
cd /data/.openclaw/workspace/skills/magic-wormhole
./install.sh
```

脚本将：
1. 检测您的包管理器（apt、dnf、zypper、brew、pip）。
2. 如果没有安装 `magic-wormhole`，则进行安装。
3. 验证安装是否成功。
4. 显示包含版本信息的成功消息。

### 方法 2：手动安装

#### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install magic-wormhole
```

#### Linux (Fedora)

```bash
sudo dnf install magic-wormhole
```

#### 其他 Linux 发行版

```bash
pip install --user magic-wormhole
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### macOS

```bash
brew install magic-wormhole
```

### 验证安装是否成功

```bash
wormhole --version
# Should output: magic-wormhole X.X.X
```

### 自托管（可选）

为了生产环境的安全性，您可以自己托管会合服务器：

```bash
pip install magic-wormhole-server
wormhole-server start --rendezvous-relay=ws://0.0.0.0:4000/v1 \
  --transit-relay=tcp:0.0.0.0:4001
```

然后使用 `--server` 标志使用该工具：

```bash
wormhole send --server=ws://your-server:4000/v1 filename
```

---

## 使用方法

### 基本模式：代理向人类用户发送秘密

**工作流程：**
1. 代理生成秘密（SSH 密钥、API 令牌、密码）。
2. 代理通过 `wormhole send --text "$SECRET"` 发送秘密。
3. 代理从输出中提取代码。
4. 代理仅将代码返回给人类用户。
5. 人类用户运行 `wormhole receive` 并输入提取到的代码。

**示例脚本：**

```bash
#!/bin/bash
# Generate SSH key and send securely

# 1. Generate key
ssh-keygen -t ed25519 -f /tmp/key -N ""

# 2. Send via wormhole
CODE=$(wormhole send --text "$(cat /tmp/key)" 2>&1 | grep "Wormhole code is:" | cut -d' ' -f4)

# 3. Return only the code (NOT the secret!)
echo "I've generated a new SSH key. Receive it with: wormhole receive"
echo "Code: $CODE"

# 4. Cleanup
rm -f /tmp/key /tmp/key.pub
```

**人类用户接收到的内容：**
```bash
wormhole receive
# Enter: 7-blue-rabbit
# Save the key
```

### 基本模式：人类用户向代理发送秘密

**工作流程：**
1. 人类用户发起请求：`wormhole send --text "my-secret"`。
2. 人类用户将代码分享给代理。
3. 代理运行 `wormhole receive <<< "$CODE"`。
4. 代理安全地存储接收到的秘密。

**示例脚本：**

```bash
#!/bin/bash
# Receive secret from human and store

# 1. Receive secret
wormhole receive <<< "$CODE" > /tmp/secret

# 2. Store securely (example: password manager)
pass insert -m api/production-key < /tmp/secret

# 3. Cleanup
rm -f /tmp/secret
echo "Secret stored securely."
```

### 核心命令

#### 发送秘密

```bash
# Send text/secret
wormhole send --text "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5..."

# Send file
wormhole send ~/.ssh/id_rsa

# Send directory
wormhole send ~/.ssh/

# Send from clipboard (Linux)
xclip -o | wormhole send --text "$(cat)"

# Send from clipboard (macOS)
pbpaste | wormhole send --text "$(cat)"
```

#### 接收秘密

```bash
# Interactive
wormhole receive
# Enter code when prompted

# Non-interactive
echo "7-blue-rabbit" | wormhole receive

# From argument
wormhole receive 7-blue-rabbit > output.txt
```

#### 程序化提取代码

```bash
# Extract code from output
CODE=$(wormhole send --text "$SECRET" 2>&1 | grep "Wormhole code is:" | cut -d' ' -f4)

# Verify extraction
if [ -z "$CODE" ]; then
    echo "ERROR: Failed to extract code"
    exit 1
fi
echo "Code: $CODE"
```

#### 批量分发

```bash
#!/bin/bash
# Send multiple secrets to team

# Send username
USER_CODE=$(wormhole send --text "$DB_USER" 2>&1 | grep "Wormhole code is:" | cut -d' ' -f4)

# Send password
PASS_CODE=$(wormhole send --text "$DB_PASS" 2>&1 | grep "Wormhole code is:" | cut -d' ' -f4)

# Report codes
echo "Database credentials ready:"
echo "Username: wormhole receive → Code: $USER_CODE"
echo "Password: wormhole receive → Code: $PASS_CODE"
```

---

## 集成

### 与 OpenClaw 的集成

此技能可以无缝集成到 OpenClaw 的代理功能中：

#### 模式 1：内联 Shell 执行

代理直接执行 Shell 命令：

```bash
# Agent command
ssh-keygen -t ed25519 -f /tmp/key -N ""
wormhole send --text "$(cat /tmp/key)"
```

#### 模式 2：脚本模板

代理即时生成并执行脚本：

```bash
# Create temporary script
cat > /tmp/send-key.sh << 'EOF'
#!/bin/bash
SECRET="$1"
CODE=$(wormhole send --text "$SECRET" 2>&1 | grep "Wormhole code is:" | cut -d' ' -f4)
echo "Code: $CODE"
EOF

chmod +x /tmp/send-key.sh
/tmp/send-key.sh "$MY_SECRET"
```

#### 模式 3：工作流程集成

作为更大自动化工作流程的一部分使用：

```bash
#!/bin/bash
# Deployment workflow with secure credential distribution

# 1. Generate deployment credentials
USER="deploy-$(date +%s)"
PASS=$(openssl rand -base64 24)

# 2. Configure server
ssh root@server "useradd $USER && echo '$PASS' | passwd $USER --stdin"

# 3. Send credentials to team via wormhole
USER_CODE=$(wormhole send --text "$USER" 2>&1 | grep "Wormhole code is:" | cut -d' ' -f4)
PASS_CODE=$(wormhole send --text "$PASS" 2>&1 | grep "Wormhole code is:" | cut -d' ' -f4)

# 4. Notify team (via message tool or other channel)
echo "Deployment credentials ready:"
echo "User: $USER_CODE"
echo "Pass: $PASS_CODE"
```

### 集成时的安全最佳实践

#### 应该做的：
- **仅返回代码**：切勿在代理的响应中返回秘密。
- **使用临时文件**：将秘密写入 `/tmp/` 目录，并在程序退出时清理文件。
- **设置正确的权限**：对敏感文件设置 `chmod 600` 权限。
- **验证代码提取**：在继续操作前确认代码提取是否成功。
- **使用安全存储**：将接收到的秘密存储在密码管理器或密钥库中。
- **在生产环境中自托管**：对于敏感操作，使用自己的会合服务器。
- **分开发送代码**：使用电话、视频聊天或安全消息应用来传递代码。

#### 不应该做的：
- **不要记录秘密**：避免在调试输出中记录秘密内容。
- **重复使用代码**：代码是一次性使用的，每次传输都应生成新的代码。
- **在同一聊天频道中发送代码和讨论秘密**：不要在同一频道中同时发送代码和讨论秘密。
- **忽略错误**：出现“拥挤”或“警告”错误可能表示存在攻击。
- **不要保留临时文件**：传输完成后清理 `/tmp/` 目录。
- **使用短代码**：对于敏感秘密，使用 `--code-length 3` 选项设置代码长度。

### 消息工具集成示例

```python
# Pseudocode: Send secure notification with code
import subprocess

def send_secret_notification(secret, channel):
    # 1. Send secret via wormhole
    result = subprocess.run(
        ["wormhole", "send", "--text", secret],
        capture_output=True,
        text=True
    )

    # 2. Extract code
    if "Wormhole code is:" in result.stderr:
        code = result.stderr.split("Wormhole code is:")[1].strip().split()[0]
    else:
        return {"error": "Failed to send secret"}

    # 3. Send notification via message tool
    message.send(
        action="send",
        channel=channel,
        message=f"I'm sending a secure secret. Receive with: wormhole receive\nCode: {code}"
    )

    return {"success": True, "code": code}
```

---

## 故障排除

### 常见问题

#### “连接被拒绝”或“超时”

**原因**：防火墙或 NAT 阻止了连接。

**解决方法：**
```bash
# Check firewall
sudo ufw allow 4000:4001/tcp

# Use custom transit relay
wormhole send --transit-relay=tcp://public-relay.magic-wormhole.io:4001 filename

# Test connectivity
ping -c 3 relay.magic-wormhole.io
nc -zv transit.magic-wormhole.io 4001
```

#### “代码未找到”

**原因**：代码已过期（一次性使用）或服务器地址错误。

**解决方法：**
```bash
# Generate new code
wormhole send --text "$SECRET"

# Check server
wormhole send --server=ws://relay.magic-wormhole.io:4000/v1 filename
```

#### “权限被拒绝”

**原因**：当前目录没有写入权限。

**解决方法：**
```bash
cd ~/Downloads
wormhole receive
```

#### 传输速度慢

**原因**：中继服务器拥堵或网络速度慢。

**解决方法：**
```bash
# Use compression
wormhole send --zstd large-file.tar

# Use custom transit relay
wormhole send --transit-relay=tcp://fast-relay.example.com:4001 filename
```

### 调试模式

启用详细输出：

```bash
# Full debug logs
wormhole send --debug filename

# Save logs to file
wormhole send --debug filename 2>&1 | tee wormhole-debug.log
```

### 版本兼容性

**检查版本：**
```bash
wormhole --version
```

**更新：**
```bash
pip install --upgrade magic-wormhole
# or
sudo apt update && sudo apt upgrade magic-wormhole
```

### Python 依赖问题

```bash
# Install missing dependencies
pip install --upgrade attrs automat spake2 twisted

# Check Python version (requires 3.10+)
python3 --version
```

### 测试安装

```bash
# Test with dummy secret
echo "test" | wormhole send --text "$(cat)"
# Should output: "Wormhole code is: X-word-word"
```

---

## 安全注意事项

### Magic Wormhole 的工作原理

1. **连接建立**：双方连接到会合服务器。
2. **密钥协商（PAKE）**：使用 SPAKE2 协议通过代码生成 256 位的共享秘密。
3. **数据传输**：所有数据均使用 NaCl/libsodium 进行端到端加密。

### 安全特性

| 威胁 | 保护措施 |
|--------|------------|
| 中间人攻击**：PAKE 协议可防止未经授权的访问。
| 服务器被攻破**：服务器只能看到加密后的数据或元数据。
- **暴力攻击**：代码是一次性使用的，且使用 256 位派生密钥。
- **流量分析**：所有数据都经过端到端加密。
- **重放攻击**：代码是一次性使用的，传输后会立即失效。

### 服务器相关知识

- **会合服务器**：知道代码、IP 地址和连接时间（但不知道加密密钥或明文内容）。
- **中继服务器**：只知道加密后的数据块（不知道加密密钥或明文内容）。

### 建议

- 对于高度敏感的秘密（约 400 万种组合），使用 `--code-length 3` 选项设置代码长度。
- 在生产环境或受监管的环境中，建议自托管服务器。
- 通过非加密通道（如电话、视频聊天或 Signal）传输代码。
- 在传输前后验证代码的真实性。
- 如有需要，可以使用 Tor 保护匿名性：`wormhole send --tor filename`。

---

## 示例

详细的使用示例请参阅 `examples/` 目录：
- **ssh-key-sharing.md**：生成和分发 SSH 密钥。
- **api-token-sharing.md**：安全的 API 令牌传输方法。
- **agent-to-human.md**：完整的代理到人类用户的秘密共享流程。

---

## 其他文档

- **docs/advanced-usage.md**：高级功能和自定义选项。

---

## 资源

### 官方链接

- **GitHub**：https://github.com/magic-wormhole/magic-wormhole
- **文档**：https://magic-wormhole.readthedocs.io/
- **协议规范**：https://github.com/magic-wormhole/magic-wormhole-protocols

### 默认服务器

- **会合服务器**：`relay.magic-wormhole.io:4000`
- **中继服务器**：`transit.magic-wormhole.io:4001`

### 社区

- **IRC**：`#magic-wormhole`（Libera.chat）
- **邮件列表**：magic-wormhole@lists.sourceforge.net

---

## 许可证

本技能文档仅供与 OpenClaw 配合使用。

Magic Wormhole 本身遵循 MIT 许可证：https://github.com/magic-wormhole/magic-wormhole/blob/main/LICENSE