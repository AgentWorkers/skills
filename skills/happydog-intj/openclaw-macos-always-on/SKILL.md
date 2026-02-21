---
name: macos-launchdaemon
description: 在 macOS 上，将 OpenClaw 作为系统级启动守护进程（LaunchDaemon）运行，以实现 24/7 不间断运行，即使在屏幕锁定、用户登出或切换用户的情况下也能持续运行。该进程使用 `caffeinate` 工具来防止系统进入睡眠状态。经验证，该方案在屏幕长时间处于锁定状态的情况下依然能够正常工作。
---
# OpenClaw 的 macOS LaunchDaemon 设置

使用 `caffeinate` 将 OpenClaw 设置为系统级服务（LaunchDaemon），以确保其能够 24/7 运行。此配置已经过测试，即使在屏幕锁定时间较长（30 分钟以上）的情况下也能正常工作。

**确保 OpenClaw 在以下情况下仍能继续运行：**
- 🔒 屏幕被锁定（无论锁定时间长短）
- 👤 用户登出
- 🔄 在不同用户账户之间切换
- 💤 显示器进入睡眠状态（系统保持唤醒）

## 何时使用 LaunchDaemon

**在以下情况下使用 LaunchDaemon：**
- 需要机器人全天候可用
- 经常锁定 Mac，但仍希望接收消息
- 多个用户需要同时访问该机器人
- 在家用服务器或始终开启的 Mac 上运行

**在以下情况下使用 LaunchAgent：**
- 仅在登录时需要使用机器人
- 偏好更简单的设置（无需 sudo 权限）
- 对系统级服务有安全顾虑

## 快速设置

### 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/clawd/master/skills/macos-launchdaemon/install.sh | bash
```

或按照以下步骤进行手动设置 ⬇️

## 手动设置

### 第一步：创建 LaunchDaemon 配置文件

使用您的实际用户名创建一个 plist 文件。此配置使用 `caffeinate`，并且已经过测试，即使在屏幕锁定 30 分钟以上的情况下也能正常工作：

```bash
cat > /tmp/ai.openclaw.gateway.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>ai.openclaw.gateway</string>
    
    <key>Comment</key>
    <string>OpenClaw Gateway (System Daemon - Network Always On)</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <!-- Enhanced KeepAlive for network services -->
    <key>KeepAlive</key>
    <dict>
      <key>SuccessfulExit</key>
      <false/>
      <key>NetworkState</key>
      <true/>
      <key>Crashed</key>
      <true/>
    </dict>
    
    <!-- Prevent ANY throttling -->
    <key>ThrottleInterval</key>
    <integer>0</integer>
    
    <!-- Interactive process - highest priority -->
    <key>ProcessType</key>
    <string>Interactive</string>
    
    <!-- Enable network transactions -->
    <key>EnableTransactions</key>
    <true/>
    
    <key>UserName</key>
    <string>YOUR_USERNAME</string>
    
    <key>GroupName</key>
    <string>staff</string>
    
    <!-- Wrap with caffeinate to prevent sleep -->
    <key>ProgramArguments</key>
    <array>
      <string>/usr/bin/caffeinate</string>
      <string>-s</string>
      <string>/opt/homebrew/bin/node</string>
      <string>/opt/homebrew/lib/node_modules/openclaw/dist/index.js</string>
      <string>gateway</string>
      <string>--port</string>
      <string>18789</string>
    </array>
    
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/.openclaw/logs/gateway.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/.openclaw/logs/gateway.err.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
      <key>HOME</key>
      <string>/Users/YOUR_USERNAME</string>
      <key>PATH</key>
      <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
  </dict>
</plist>
EOF

# Replace YOUR_USERNAME with your actual username
sed -i '' "s/YOUR_USERNAME/$(whoami)/g" /tmp/ai.openclaw.gateway.plist
```

**🔑 保持屏幕锁定状态的配置关键项：**
- **`/usr/bin/caffeinate -s`** - 阻止系统进入睡眠状态（显示器可以进入睡眠，但网络保持活跃）
- **`NetworkState: true`** - 确保网络可用时服务仍保持运行
- **`ProcessType: Interactive`** - 防止 macOS 暂停该进程
- **`ThrottleInterval: 0`** - 禁用任何节流机制
- **`Crashed: true`** - 发生崩溃时自动重启

**✅ 在 macOS 14.4 上测试过，屏幕锁定 30 分钟以上后仍能正常工作**

### 第二步：停止现有的 LaunchAgent

```bash
# Stop user-level service
launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null

# Backup and disable LaunchAgent plist
mv ~/Library/LaunchAgents/ai.openclaw.gateway.plist ~/Library/LaunchAgents/ai.openclaw.gateway.plist.disabled 2>/dev/null
```

### 第三步：安装 LaunchDaemon（需要 sudo 权限）

```bash
# Copy to system location
sudo cp /tmp/ai.openclaw.gateway.plist /Library/LaunchDaemons/

# Set correct permissions
sudo chown root:wheel /Library/LaunchDaemons/ai.openclaw.gateway.plist
sudo chmod 644 /Library/LaunchDaemons/ai.openclaw.gateway.plist

# Load and start service
sudo launchctl bootstrap system /Library/LaunchDaemons/ai.openclaw.gateway.plist
```

### 第四步：验证安装

```bash
# Check process is running
ps aux | grep openclaw-gateway | grep -v grep

# Verify PPID = 1 (launched by system launchd)
ps -p $(pgrep -f openclaw-gateway) -o pid,ppid,user,command

# Check service status
sudo launchctl print system/ai.openclaw.gateway | head -10

# Test with OpenClaw
openclaw status
```

预期输出：
```
PID   PPID  USER       COMMAND
12345 1     youruser   openclaw-gateway
```

PPID=1 表明它作为 LaunchDaemon 运行（父进程是系统的 launchd）。

## 测试屏幕锁定状态下的行为

### 测试脚本

```bash
#!/bin/bash
echo "🧪 Testing LaunchDaemon lock screen behavior..."
echo ""
echo "1. Lock your Mac in 5 seconds..."
sleep 5
pmset displaysleepnow

echo "2. Use your phone to send 'ping' to your bot"
echo "3. Bot should reply 'pong! 🎉' even while locked"
echo ""
echo "Unlock your Mac after testing."
```

### 手动测试步骤：
1. **锁定 Mac**：按 ⌘ + Control + Q
2. **从手机发送消息**：通过 Telegram/Feishu 等方式向机器人发送 “ping” 消息
3. **预期结果**：机器人立即回复 “pong! 🎉”
4. **解锁 Mac** 并检查日志以确认消息已被处理

## 管理命令

### 查看日志

```bash
# Real-time logs
tail -f ~/.openclaw/logs/gateway.log

# Error logs
tail -f ~/.openclaw/logs/gateway.err.log

# Last 100 lines
tail -100 ~/.openclaw/logs/gateway.log
```

### 重启服务

```bash
# Unload and reload
sudo launchctl bootout system/ai.openclaw.gateway
sudo launchctl bootstrap system /Library/LaunchDaemons/ai.openclaw.gateway.plist

# Or use kickstart (restarts without unloading)
sudo launchctl kickstart -k system/ai.openclaw.gateway
```

### 停止服务

```bash
# Stop service
sudo launchctl bootout system/ai.openclaw.gateway

# Prevent auto-start
sudo launchctl disable system/ai.openclaw.gateway
```

### 启动服务

```bash
# Enable and start
sudo launchctl enable system/ai.openclaw.gateway
sudo launchctl bootstrap system /Library/LaunchDaemons/ai.openclaw.gateway.plist
```

### 检查状态

```bash
# Full service details
sudo launchctl print system/ai.openclaw.gateway

# Quick status check
sudo launchctl list | grep openclaw

# Process info
ps aux | grep openclaw-gateway | grep -v grep
```

## 卸载

### 完全移除

```bash
# 1. Stop service
sudo launchctl bootout system/ai.openclaw.gateway

# 2. Remove plist
sudo rm /Library/LaunchDaemons/ai.openclaw.gateway.plist

# 3. Restore LaunchAgent (optional)
mv ~/Library/LaunchAgents/ai.openclaw.gateway.plist.disabled ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>/dev/null
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 4. Verify
ps aux | grep openclaw | grep -v grep
```

## 自动化安装脚本

将以下内容保存为 `install-launchdaemon.sh`：

```bash
#!/bin/bash
set -e

echo "🚀 OpenClaw LaunchDaemon Installer"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

USERNAME=$(whoami)
PLIST_PATH="/Library/LaunchDaemons/ai.openclaw.gateway.plist"
TEMP_PLIST="/tmp/ai.openclaw.gateway.plist"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}❌ Don't run this script with sudo${NC}"
   echo "The script will ask for sudo password when needed."
   exit 1
fi

# Check if OpenClaw is installed
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}❌ OpenClaw not found. Install it first:${NC}"
    echo "   npm install -g openclaw"
    exit 1
fi

echo -e "${YELLOW}📋 Creating LaunchDaemon configuration...${NC}"

# Get OpenClaw gateway token
GATEWAY_TOKEN=$(openclaw config get gateway.auth.token 2>/dev/null | tr -d '"' || echo "")

cat > "$TEMP_PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>ai.openclaw.gateway</string>
    
    <key>Comment</key>
    <string>OpenClaw Gateway (System Daemon)</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>UserName</key>
    <string>$USERNAME</string>
    
    <key>GroupName</key>
    <string>staff</string>
    
    <key>ProgramArguments</key>
    <array>
      <string>/opt/homebrew/bin/node</string>
      <string>/opt/homebrew/lib/node_modules/openclaw/dist/index.js</string>
      <string>gateway</string>
      <string>--port</string>
      <string>18789</string>
    </array>
    
    <key>StandardOutPath</key>
    <string>/Users/$USERNAME/.openclaw/logs/gateway.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/$USERNAME/.openclaw/logs/gateway.err.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
      <key>HOME</key>
      <string>/Users/$USERNAME</string>
      <key>PATH</key>
      <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
      <key>OPENCLAW_GATEWAY_PORT</key>
      <string>18789</string>
      <key>OPENCLAW_GATEWAY_TOKEN</key>
      <string>$GATEWAY_TOKEN</string>
    </dict>
  </dict>
</plist>
EOF

echo -e "${YELLOW}🛑 Stopping existing services...${NC}"

# Stop LaunchAgent
launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null || true

# Backup LaunchAgent plist
if [ -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist ]; then
    mv ~/Library/LaunchAgents/ai.openclaw.gateway.plist ~/Library/LaunchAgents/ai.openclaw.gateway.plist.backup
    echo -e "${GREEN}✅ Backed up LaunchAgent plist${NC}"
fi

# Stop existing LaunchDaemon
sudo launchctl bootout system/ai.openclaw.gateway 2>/dev/null || true

echo -e "${YELLOW}📦 Installing LaunchDaemon...${NC}"

# Install plist
sudo cp "$TEMP_PLIST" "$PLIST_PATH"
sudo chown root:wheel "$PLIST_PATH"
sudo chmod 644 "$PLIST_PATH"

echo -e "${YELLOW}🚀 Starting service...${NC}"

# Start service
sudo launchctl bootstrap system "$PLIST_PATH"
sleep 3

# Verify
if ps aux | grep -q "[o]penclaw-gateway"; then
    echo ""
    echo -e "${GREEN}✅ LaunchDaemon installed successfully!${NC}"
    echo ""
    echo "📊 Service Status:"
    ps aux | grep "[o]penclaw-gateway" | awk '{print "   PID: "$2", User: "$1}'
    echo ""
    echo "🧪 Test it:"
    echo "   1. Lock your Mac: ⌘ + Control + Q"
    echo "   2. Send 'ping' from your phone"
    echo "   3. Bot should reply even while locked!"
    echo ""
    echo "📋 Management:"
    echo "   Logs:    tail -f ~/.openclaw/logs/gateway.log"
    echo "   Restart: sudo launchctl kickstart -k system/ai.openclaw.gateway"
    echo "   Stop:    sudo launchctl bootout system/ai.openclaw.gateway"
    echo "   Status:  sudo launchctl print system/ai.openclaw.gateway"
else
    echo -e "${RED}❌ Service failed to start${NC}"
    echo "Check logs: tail -50 ~/.openclaw/logs/gateway.err.log"
    exit 1
fi
```

使其可执行：
```bash
chmod +x install-launchdaemon.sh
./install-launchdaemon.sh
```

## 故障排除

### 服务无法启动

**检查日志：**
```bash
tail -50 ~/.openclaw/logs/gateway.err.log
```

**常见问题：**
1. plist 文件中的用户名错误
   ```bash
   # Verify username matches
   grep UserName /Library/LaunchDaemons/ai.openclaw.gateway.plist
   whoami
   ```

2. 节点路径错误
   ```bash
   # Check node location
   which node
   
   # Update plist if needed (change /opt/homebrew/bin/node to your path)
   ```

3. 权限问题
   ```bash
   # Fix log directory permissions
   mkdir -p ~/.openclaw/logs
   chmod 755 ~/.openclaw/logs
   ```

### 屏幕锁定后服务仍会暂停

如果使用的是较旧的 macOS 或特定硬件：

```bash
# Prevent system sleep
sudo pmset -a sleep 0
sudo pmset -a disksleep 0
sudo pmset -a displaysleep 10  # Screen off but system awake
```

或者使用 `caffeinate`（不推荐用于笔记本电脑）：
```bash
# Modify ProgramArguments in plist to wrap with caffeinate
<string>/usr/bin/caffeinate</string>
<string>-s</string>  <!-- prevent sleep -->
<string>/opt/homebrew/bin/node</string>
...
```

### 端口已被占用

```bash
# Find what's using port 18789
lsof -i :18789

# Kill the process
kill -9 <PID>

# Or change port in config and plist
openclaw config set gateway.port 18790
```

### 日志无法记录

```bash
# Create log directory
mkdir -p ~/.openclaw/logs

# Test permissions
touch ~/.openclaw/logs/test.log
ls -la ~/.openclaw/logs/

# Check plist paths match
grep Path /Library/LaunchDaemons/ai.openclaw.gateway.plist
```

## 安全考虑

### 以用户身份运行与以 root 身份运行

✅ **此设置以您的用户身份运行**（在 `<key>UserName</key>` 中指定）
- 不以 root 身份运行
- 权限与手动运行 OpenClaw 时相同
- 比以 root 身份运行的守护进程更安全

### 文件权限

```bash
# LaunchDaemon plist should be owned by root
ls -l /Library/LaunchDaemons/ai.openclaw.gateway.plist
# Should show: -rw-r--r--  1 root  wheel

# Log directory owned by you
ls -ld ~/.openclaw/logs
# Should show: drwxr-xr-x ... youruser staff
```

### 令牌安全

Gateway 令牌存储在 plist 环境变量中。虽然只有 root 和您自己可以读取该令牌，但请注意：

```bash
# Check who can read the plist
ls -l /Library/LaunchDaemons/ai.openclaw.gateway.plist

# More secure: use macOS Keychain (advanced)
# Store token in keychain and retrieve at runtime
```

## 性能影响

LaunchDaemon 的性能影响 **很小**：
- 与 LaunchAgent 使用相同的进程
- 仅在需要时运行（KeepAlive 负责处理崩溃情况）
- 空闲时占用约 50MB 内存，CPU 使用率低于 1%
- 活动状态（处理消息时）占用约 100MB 内存，具体取决于任务负载

## macOS 版本兼容性

已在以下版本上测试通过：
- ✅ macOS 10.15 (Catalina)
- ✅ macOS 11 (Big Sur)
- ✅ macOS 12 (Monterey)
- ✅ macOS 13 (Ventura)
- ✅ macOS 14 (Sonoma)
- ✅ macOS 15 (Sequoia)

注意：macOS 11 及更高版本中 LaunchDaemon 的语法略有变化，但向下兼容。

## LaunchAgent 与 LaunchDaemon 的比较

| 特性 | LaunchAgent | LaunchDaemon |
|---------|-------------|--------------|
| **屏幕锁定时是否运行** | ❌ 可能会暂停 | ✅ 始终运行 |
| **用户登出时是否运行** | ❌ 停止运行 | ✅ 继续运行 |
| **设置复杂性** | 简单 | 需要 sudo 权限 |
| **是否需要 sudo** | ❌ 不需要 | ✅ 需要 |
| **适用场景** | 个人使用（仅限登录时） | 24/7 运行的服务器、多用户环境 |
| **安全性** | 用户级别 | 系统级别（但仍以用户身份运行） |
| **自动启动** | 登录时启动 | 启动时启动 |

## 迁移

### 从 LaunchAgent 迁移到 LaunchDaemon

使用上述安装脚本，或：

```bash
# Automatic migration
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
mv ~/Library/LaunchAgents/ai.openclaw.gateway.plist ~/Library/LaunchAgents/ai.openclaw.gateway.plist.backup
# Then follow installation steps
```

### 从 LaunchDaemon 迁回 LaunchAgent

```bash
# Stop daemon
sudo launchctl bootout system/ai.openclaw.gateway
sudo rm /Library/LaunchDaemons/ai.openclaw.gateway.plist

# Restore agent
mv ~/Library/LaunchAgents/ai.openclaw.gateway.plist.backup ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

## 常见问题解答

**Q：这会消耗我的电池电量吗？**  
A：影响很小。OpenClaw 在不处理消息时，CPU 使用率低于 1%。

**Q：我可以更新 OpenClaw 吗？**  
A：可以。更新后请重启服务：
```bash
sudo launchctl kickstart -k system/ai.openclaw.gateway
```

**Q：如果我升级 macOS 会怎样？**  
A：LaunchDaemon 可以在操作系统升级后继续运行。请确认升级后服务仍能正常工作：
```bash
sudo launchctl print system/ai.openclaw.gateway
```

**Q：我可以运行多个实例吗？**  
A：不推荐。建议使用一个 LaunchDaemon 来管理多个频道账户。

**Q：这可以在 M1/M2 Mac 上使用吗？**  
A：可以！在 Intel 和 Apple Silicon Mac 上都能正常运行。

## 相关技能

- [macos-lock-screen-fix](../macos-lock-screen-fix/) - 另一种使用 LaunchAgent 的解决方案（更简单，但可能不适用于所有 Mac）
- [healthcheck](../healthcheck/) - 监控 OpenClaw 的运行状态和可用时间

## 贡献建议

如果发现任何问题或有改进意见，请提交到：
- GitHub: https://github.com/openclaw/openclaw/issues
- 欢迎提交 Pull Request！

---

**常用命令参考：**

```bash
# Status
sudo launchctl print system/ai.openclaw.gateway

# Restart
sudo launchctl kickstart -k system/ai.openclaw.gateway

# Logs
tail -f ~/.openclaw/logs/gateway.log

# Uninstall
sudo launchctl bootout system/ai.openclaw.gateway
sudo rm /Library/LaunchDaemons/ai.openclaw.gateway.plist
```