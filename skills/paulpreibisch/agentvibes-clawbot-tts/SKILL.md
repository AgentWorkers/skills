# AgentVibes Clawdbot 技能 - 本地 TTS 集成

**版本：** 1.0.0  
**作者：** Paul Preibisch  
**仓库：** https://github.com/paulpreibisch/AgentVibes  
**许可证：** Apache-2.0  

## 概述  

该技能可自动将 AgentVibes 与 Clawdbot 集成，通过 SSH 在远程设备（Android/Termux、Linux、macOS）上实现本地 TTS 生成。  

### 功能亮点：  
- ✅ **自动 TTS**：Clawdbot 的所有回复均通过 AgentVibes 生成并播放。  
- ✅ **远程生成**：文本发送到远程设备后，音频在本地生成。  
- ✅ **完整功能**：支持语音效果、混响效果及背景音乐。  
- ✅ **低带宽需求**：仅通过 SSH 传输文本（约 1-5 KB）。  
- ✅ **安全性**：采用 SSH 密钥认证及 Tailscale VPN 保障安全。  

## 先决条件  

### 服务器端（Clawdbot）  
- Clawdbot 已安装并运行。  
- 具备访问远程设备的 SSH 连接权限。  
- 需要一个工作目录（例如：`~/clawd`）。  

### 远程设备（Android/Linux/macOS）  
- 远程设备上运行 SSH 服务器（`sshd`）。  
- 安装了 Node.js（用于自动安装 AgentVibes）。  
- 推荐使用 Tailscale（可选）。  

**注意：** 在设置过程中，AgentVibes 会自动在服务器和远程设备上安装。  

## 安装步骤  

### 先决条件：SSH 设置 ⚠️  
在运行安装脚本之前，请务必完成以下 SSH 设置：  
1. **生成 SSH 密钥**（如果尚未生成）：  
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ''
```  
2. **将密钥复制到远程设备**：  
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@remote-ip
```  
3. **测试 SSH 连接**（无需密码）：  
```bash
ssh android "echo Connected"
# Should print: Connected
```  
4. **将密钥添加到 `~/.ssh/config` 文件中**（可选，但推荐）：  
```
Host android
    HostName your-device-ip
    User your-username
    Port 22
```  
确认 SSH 连接正常后，即可继续安装。  

### 快速安装  
运行安装脚本：  
```bash
npx agentvibes install-clawdbot-skill
```  

### 手动安装  
1. 运行安装脚本（AgentVibes 会自动在服务器和远程设备上安装）：  
```bash
cd ~/.npm-global/lib/node_modules/agentvibes

# Set your Clawdbot workspace
export CLAWDBOT_WORKSPACE=~/clawd

# Set SSH remote host (optional, defaults to 'android')
export AGENTVIBES_SSH_HOST=android

# Run setup - AgentVibes will be auto-installed if needed
bash skills/clawdbot/setup.sh
```  
安装脚本将完成以下操作：  
- ✅ 在服务器上安装 AgentVibes（如果尚未安装）。  
- ✅ 创建 TTS 相关脚本和钩子。  
- ✅ 通过 SSH 连接到远程设备并自动安装 AgentVibes。  
- ✅ 配置所有必要的文件和权限。  

## 安装内容  

### 1. TTS 脚本（`<workspace>/.claude/hooks/play-tts.sh`）  
Clawdbot 会在每次生成 TTS 内容时自动调用此脚本：  
```bash
#!/usr/bin/env bash
# AgentVibes Clawdbot TTS Hook
TEXT="${1:-}"
VOICE="${2:-en_US-kristin-medium}"
[[ -z "$TEXT" ]] && exit 0
bash "$WORKSPACE/local-gen-tts.sh" "$TEXT" "$VOICE" &
exit 0
```  

### 2. 本地生成脚本（`<workspace>/local-gen-tts.sh`）  
该脚本负责将文本发送到远程设备以生成音频：  
```bash
#!/usr/bin/env bash
# AgentVibes local-gen-tts
ANDROID_HOST="android"
TEXT="${1:-}"
VOICE="${2:-en_US-kristin-medium}"

ssh "$ANDROID_HOST" "bash ~/.termux/agentvibes-play.sh '$TEXT' '$VOICE'" &
```  

### 3. 远程接收脚本（`~/.termux/agentvibes-play.sh`）  
该脚本安装在远程设备（Android/Linux/macOS）上：  
```bash
#!/usr/bin/env bash
# AgentVibes SSH Receiver
TEXT="$1"
VOICE="${2:-en_US-ryan-high}"
export AGENTVIBES_NO_REMINDERS=1
export AGENTVIBES_RDP_MODE=false

AGENTVIBES_ROOT="/data/data/com.termux/files/usr/lib/node_modules/agentvibes"
bash "$AGENTVIBES_ROOT/.claude/hooks/play-tts.sh" "$TEXT" "$VOICE"
```  

### 配置文件（`<workspace>/.claude/`）  
- `tts-provider.txt`：指定 TTS 服务（例如：`piper`）。  
- `tts-voice.txt`：选择语音类型（例如：`en_US-kristin-medium`）。  
- `ssh-remote-host.txt`：指定远程设备的 SSH 主机名（例如：`android`）。  

## 配置选项  

### 语音选项  
**女性语音：**  
- `en_US-kristin-medium`：专业、中性音色（推荐）  
- `en_US-lessac-medium`：温暖、富有表现力  
- `en_US-amy-medium`：亲切、适合对话  
- `en_US-libritts-high`：清晰、音质较高  

**男性语音：**  
- `en_US-ryan-high`：充满活力、音质清晰（推荐）  
- `en_US-joe-medium`：风格自然  
- `en_US-bryce-medium`：专业音质  

### 音效设置（可选）  
在远程设备上进行配置：  
```bash
# On Android/remote
nano ~/.local/share/agentvibes/.claude/config/audio-effects.cfg
```  
如需添加更多音效，请参考相关文档。  

### SSH 设置  
将以下内容添加到 `~/.ssh/config` 文件中：  
```
Host android
    HostName 100.115.27.58  # Tailscale IP
    User u0_a484
    Port 52847
    IdentityFile ~/.ssh/android_key
```  

## 使用方法  
安装完成后，整个流程完全自动化，无需手动操作！  

## 架构说明  
```
┌─────────────────────────────────────┐
│ Clawdbot (Server)                   │
│ ├─ Generates text response          │
│ ├─ Calls .claude/hooks/play-tts.sh │
│ ├─ Calls local-gen-tts.sh          │
│ └─ Sends TEXT via SSH              │
└─────────────────────────────────────┘
              ↓ SSH/Tailscale
┌─────────────────────────────────────┐
│ Android/Remote Device               │
│ ├─ Receives text                    │
│ ├─ AgentVibes (Piper TTS)          │
│ ├─ Generates audio locally          │
│ ├─ Applies reverb + music           │
│ └─ Plays on speakers                │
└─────────────────────────────────────┘
```  

### 多个 Clawdbot 实例  
如果同时使用多个 Clawdbot 实例（例如 Orian 和 Samuel），每个实例均可：  
- 使用不同的语音  
- 设置不同的背景音乐  
- 自定义不同的音效设置。  

## 常见问题及解决方法：  
- **远程设备无音频输出？**  
- **TTS 未自动触发？**  
- **播放的语音错误？**  
请参考相关文档进行排查。  

## 卸载方法  
```bash
# Remove TTS integration
rm -rf $CLAWDBOT_WORKSPACE/.claude/hooks
rm $CLAWDBOT_WORKSPACE/.claude/tts-provider.txt
rm $CLAWDBOT_WORKSPACE/.claude/tts-voice.txt
rm $CLAWDBOT_WORKSPACE/local-gen-tts.sh

# On remote device
ssh android "rm ~/.termux/agentvibes-play.sh"
```  

## 安全性措施：  
- **仅使用 SSH 密钥认证（无需密码）**  
- **仅传输文本数据（无可执行代码）**  
- **推荐使用 Tailscale VPN**  
- **可配置 SSH 端口（使用非标准端口）**  

## 性能参数：  
- **延迟：** 约 5-8 秒（文本 → 音频 → 播放）。  
- **带宽消耗：** 每条消息约 1-5 KB（仅传输文本）。  
- **音质：** 支持高保真神经网络 TTS 效果。  
- **可靠性：** 在后台运行，无阻塞现象。  

## 示例：  
- **基本配置（Orian）**  
```bash
# 1. Install on server
cd ~/.npm-global/lib/node_modules/agentvibes
CLAWDBOT_WORKSPACE=~/clawd AGENTVIBES_SSH_HOST=android bash skills/clawdbot/setup.sh

# 2. Install receiver on Android
ssh android "curl -sSL https://raw.githubusercontent.com/paulpreibisch/AgentVibes/main/scripts/install-ssh-receiver.sh | bash"

# 3. Done! Send a message to Clawdbot
```  
- **高级配置（多个实例及不同背景音乐）**  
```bash
# Orian - Kristin + Flamenco
CLAWDBOT_WORKSPACE=~/clawd \
AGENTVIBES_VOICE=en_US-kristin-medium \
AGENTVIBES_MUSIC=agentvibes_soft_flamenco_loop.mp3 \
bash skills/clawdbot/setup.sh

# Samuel - Ryan + Bachata
CLAWDBOT_WORKSPACE=~/clawd2 \
AGENTVIBES_VOICE=en_US-ryan-high \
AGENTVIBES_MUSIC=agent_vibes_bachata_v1_loop.mp3 \
bash skills/clawdbot/setup.sh
```  

## 支持项目  
如果您喜欢 AgentVibes，请为该仓库点赞以支持开发者：  
👉 https://github.com/paulpreibisch/AgentVibes  
您的支持将帮助更多人发现并使用这个项目！  

## 贡献方式  
发现漏洞或有建议？请提交 issue：  
https://github.com/paulpreibisch/AgentVibes/issues  

## 许可证信息  
Apache-2.0 许可证，请参阅 LICENSE 文件。  

**致谢：**  
- **AgentVibes**：Paul Preibisch  
- **Clawdbot 集成**：与 Claude AI 共同开发。  
- **TTS 服务（piper）**：基于 Rhasspy/Home Assistant 实现。  

---

**版本：** 1.0.0  
**最后更新时间：** 2026-01-30  
**状态：** 已准备好投入生产使用 ✅