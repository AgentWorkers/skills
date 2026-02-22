---
name: clawtime
description: 安装、配置、启动以及排查ClawTime的故障——这是一个专为OpenClaw设计的私有自托管Webchat界面，支持Passkey（Face ID）认证、Piper TTS语音功能以及3D虚拟形象。该服务需要通过Cloudflare隧道来实现HTTPS连接（Passkey认证需要使用真实的域名）。用户可以在新机器上安装ClawTime、配置隧道、注册Passkey、设置TTS功能、启动/停止服务器，或解决相关故障。常见的操作指令包括：“install clawtime”、“set up clawtime”、“start clawtime”、“clawtime isn't working”、“register passkey”以及“device auth issue”。
metadata:
  openclaw:
    requires:
      bins:
        - node
        - git
        - cloudflared
        - npm
      optionalBins:
        - python3
        - ffmpeg
        - piper
    env:
      - PUBLIC_URL
      - GATEWAY_TOKEN
      - SETUP_TOKEN
    files:
      - scripts/install.sh
      - references/device-auth.md
      - references/troubleshooting.md
      - references/launchd.md
    permissions:
      - network (Cloudflare tunnel, git clone, npm install)
      - keychain (store/retrieve GATEWAY_TOKEN and SETUP_TOKEN)
      - filesystem (~/Projects/clawtime, ~/.clawtime, ~/.cloudflared, ~/Library/LaunchAgents)
---
# ClawTime — 使用 Cloudflare Tunnel 进行本地安装

ClawTime 是一个私有的 Webchat 用户界面，它通过 WebSocket 与 OpenClaw 网关连接。  
**功能包括：**  
- 密码验证（Face ID/Touch ID）  
- Piper TTS 语音功能  
- 3D 虚拟形象  

**为什么需要 Cloudflare？**  
WebAuthn（密码验证）需要使用 HTTPS 协议，并且必须部署在真实的域名上。  
`http://localhost` 仅能在同一台机器上使用，无法从网络中的手机访问。  

## 架构  

```
iPhone/Browser → https://portal.yourdomain.com → Cloudflare Tunnel → localhost:3000 (ClawTime) → ws://127.0.0.1:18789 (OpenClaw Gateway)
```  

## 先决条件  
- Node.js v22 或更高版本  
- `cloudflared` 命令行工具：`brew install cloudflared`  
- 在 Cloudflare 上注册一个域名（免费 tier 即可）  
- OpenClaw 已经运行：`openclaw status`  
- （可选）Piper TTS 和 ffmpeg 用于语音功能  

## 安装步骤  

### 1. 克隆并安装相关依赖  
```bash
cd ~/Projects
git clone https://github.com/youngkent/clawtime.git
cd clawtime
npm install --legacy-peer-deps
```  

### 2. 设置 Cloudflare Tunnel  
```bash
# Login to Cloudflare
cloudflared tunnel login

# Create named tunnel
cloudflared tunnel create clawtime

# Configure routing
# Edit ~/.cloudflared/config.yml:
```  

**`~/.cloudflared/config.yml` 文件内容：**  
```yaml
tunnel: clawtime
credentials-file: /Users/YOUR_USER/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: portal.yourdomain.com
    service: http://localhost:3000
  - service: http_status:404
```  

接下来，在 Cloudflare 的 DNS 控制面板中添加一个 CNAME 记录：  
- 名称：`portal`  
- 目标：`<tunnel-id>.cfargotunnel.com`  

### 3. 配置 OpenClaw 网关  
网关必须将 ClawTime 的请求源地址添加到白名单中：  
```bash
openclaw config patch '{"gateway":{"controlUi":{"allowedOrigins":["https://portal.yourdomain.com"]}}}'
openclaw gateway restart
```  

**注意：**  
`PUBLIC_URL` 必须与这个源地址完全匹配，因为它将作为 WebSocket 请求的源地址头用于设备身份验证。  

### 4. 启动 ClawTime 服务器  
**（基础配置，不包含 TTS 功能）：**  
```bash
cd ~/Projects/clawtime
PUBLIC_URL=https://portal.yourdomain.com \
SETUP_TOKEN=<your-setup-token> \
GATEWAY_TOKEN=<gateway-token> \
node server.js
```  

**（包含 TTS 功能的配置：）**  
```bash
cd ~/Projects/clawtime
PUBLIC_URL=https://portal.yourdomain.com \
SETUP_TOKEN=<your-setup-token> \
GATEWAY_TOKEN=<gateway-token> \
BOT_NAME="Beware" \
BOT_EMOJI="🌀" \
TTS_COMMAND='python3 -m piper --data-dir ~/Documents/resources/piper-voices -m en_US-kusal-medium -f /tmp/clawtime-tts-tmp.wav -- {{TEXT}} && ffmpeg -y -loglevel error -i /tmp/clawtime-tts-tmp.wav {{OUTPUT}}' \
node server.js
```  

**TTS 安全提示：**  
`{{TEXT}}` 这个占位符会被替换到 shell 命令中。  
ClawTime 服务器在替换文本之前必须对其进行安全处理，以防止命令注入攻击。  
服务器应删除或转义用户输入中的 shell 特殊字符（`; | & $ \` ( ) { } < >`），然后再将其传递给 TTS 命令。  
如果修改了 TTS 处理流程，请使用 `child_process.execFile()` 并传递参数数组，而不是使用 `child_process.exec()` 和字符串插值。  

### 5. 启动 Cloudflare Tunnel  
```bash
cloudflared tunnel run clawtime
```  

### 6. 注册密码（仅首次使用时需要）  
1. 打开 `https://portal.yourdomain.com/?setup=<your-setup-token>`（使用 Safari 浏览器）  
2. 按照提示完成密码验证（Face ID/Touch ID）  
3. **注意：** 不要使用隐私模式或无痕模式——Safari 在这些模式下不支持密码验证。  
4. **注意：** 在 iOS 设备上请使用 Safari，而非 Chrome。  
注册完成后，可以通过 `https://portal.yourdomain.com` 访问 ClawTime。  

---

## 环境变量  
| 变量 | 是否必需 | 说明 |  
|----------|----------|-------------|  
| `PUBLIC_URL` | 是 | 公开的 HTTPS 网址（必须与网关配置中的 `allowedOrigins` 一致） |  
| `GATEWAY_TOKEN` | 是 | OpenClaw 网关的身份验证令牌 |  
| `SETUP_TOKEN` | 是 | 注册时使用的密码 |  
| `TTS_COMMAND` | 是 | 用于语音功能的 Piper 命令（包含 `{{TEXT}}` 和 `{{OUTPUT}}` 占位符） |  
| `BOT_NAME` | 否 | 机器人显示名称（默认：Beware） |  
| `BOT_EMOJI` | 否 | 虚拟形象的emoji（默认：🌀） |  
| `PORT` | 否 | 服务器端口（默认：3000） |  

### 安全存储令牌（推荐）  
建议不要将令牌以明文形式存储在环境变量或 plist 文件中，而是将其保存在 macOS 的 Keychain 中：  
```bash
# Store tokens in Keychain
security add-generic-password -s "clawtime-gateway-token" -a "$(whoami)" -w "YOUR_GATEWAY_TOKEN"
security add-generic-password -s "clawtime-setup-token" -a "$(whoami)" -w "YOUR_SETUP_TOKEN"
```  

**启动时获取令牌：**  
```bash
GATEWAY_TOKEN=$(security find-generic-password -s "clawtime-gateway-token" -a "$(whoami)" -w) \
SETUP_TOKEN=$(security find-generic-password -s "clawtime-setup-token" -a "$(whoami)" -w) \
PUBLIC_URL=https://portal.yourdomain.com \
node server.js
```  

这样可以避免将敏感信息以明文形式保存在磁盘上。  

---

## 设备身份验证（至关重要）  
ClawTime 使用 Ed25519 密钥对进行身份验证。  
这是许多安装过程中会出问题的环节——详细信息请参阅 `references/device-auth.md`。  

**快速总结：**  
- 第一次运行时，系统会在 `~/.clawtime/device-key.json` 文件中自动生成密钥对。  
- 设备 ID 是 32 字节的 Ed25519 公钥的 SHA-256 哈希值（而非完整的 SPKI 编码密钥）。  
- 签名数据格式：`v2|deviceId|clientId|clientMode|role|scopes|signedAtMs|token|nonce`  
- 如果设备身份验证失败，请删除 `~/.clawtime/device-key.json` 文件并重新启动应用。  

---

## 在启动时自动运行（macOS 的 launchd 服务）  
有关服务器和 Tunnel 的启动配置文件模板，请参阅 `references/launchd.md`。  

---

## 服务管理  
```bash
# Stop server
pkill -f "node server.js"

# Stop tunnel
pkill -f "cloudflared"

# View logs (if backgrounded)
tail -f /tmp/clawtime.log
tail -f /tmp/cloudflared.log

# Restart after code/config changes
pkill -9 -f "node server.js"; sleep 2; # then re-run start command
```  

---

## 获取网关令牌  
```bash
# From macOS Keychain
security find-generic-password -s "openclaw-gateway-token" -a "$(whoami)" -w

# From config file
cat ~/.openclaw/openclaw.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('gateway',{}).get('token',''))"
```  

---

## 密码操作  
```bash
# Reset passkeys (re-register from scratch)
echo '[]' > ~/.clawtime/credentials.json
# Restart server, then visit /?setup=<token>

# Reset device key (new keypair on next restart)
rm ~/.clawtime/device-key.json
```  

---

## 故障排除  
有关常见错误及其解决方法，请参阅 `references/troubleshooting.md`。  
有关网关身份验证的详细信息，请参阅 `references/device-auth.md`。