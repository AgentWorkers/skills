---
name: clawtime
description: **设置并使用 ClawTime：OpenClaw 的 Webchat 接口**  
ClawTime 是一个专为 OpenClaw 设计的 Webchat 工具，支持密码认证（passkey auth）、3D 虚拟形象（3D avatars）以及语音通话功能。  

**主要特性：**  
1. **密码认证（Passkey Auth）**：用户可以通过输入密码来安全地登录系统。  
2. **3D 虚拟形象（3D Avatars）**：用户可以自定义自己的 3D 虚拟形象，增加聊天时的个性化元素。  
3. **语音通话（Voice Mode）**：支持实时语音交流，提升聊天体验。  

**安装与配置步骤：**  
1. **安装 OpenClaw 和 ClawTime**：首先确保您已安装 OpenClaw，然后从官方网站下载并安装 ClawTime。  
2. **配置 ClawTime**：根据官方文档配置 ClawTime，设置服务器地址、端口等参数。  
3. **集成到 OpenClaw**：在 OpenClaw 中启用 ClawTime 功能，将其作为默认的 Webchat 插件。  

**使用方法：**  
1. **访问 ClawTime 网站**：使用浏览器访问 ClawTime 的官方网站，使用用户名和密码登录。  
2. **加入聊天室**：选择感兴趣的聊天室，点击“加入”按钮。  
3. **开始聊天**：与室内的其他用户进行文字或语音交流。  

**注意事项：**  
- 请确保您的网络环境稳定，以确保语音通话的顺畅进行。  
- 如果遇到技术问题，请查阅 ClawTime 的官方文档或联系技术支持。  

**更多信息：**  
- [ClawTime 官方网站](https://clawhub.com/)  
- [OpenClaw 官方文档](https://openclaw.org/)  

希望这能帮助您快速上手并享受 ClawTime 带来的便捷聊天体验！
---

# ClawTime 技能

## 设置指南

### 1. 安装

```bash
cd ~/.openclaw/workspace
git clone https://github.com/youngkent/clawtime.git
cd clawtime
npm install
```

首次运行时，系统会创建 `~/.clawtime/` 目录，并使用默认配置。

### 1b. Whisper STT 设置（语音模式必需）

ClawTime 使用 [whisper.cpp](https://github.com/ggerganov/whisper.cpp) 来实现服务器端的语音转文本功能。

**检查是否已安装：**
```bash
which whisper-transcribe && echo "✅ Whisper ready" || echo "❌ Need to install"
```

**如果未安装：**
```bash
# Clone and build whisper.cpp
cd /tmp
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make

# Download a model (base.en is fast and good for English)
bash ./models/download-ggml-model.sh base.en

# Create wrapper script
sudo tee /usr/local/bin/whisper-transcribe << 'EOF'
#!/bin/bash
/tmp/whisper.cpp/main -m /tmp/whisper.cpp/models/ggml-base.en.bin -f "$1" --no-timestamps -otxt 2>/dev/null
cat "${1}.txt"
rm -f "${1}.txt"
EOF
sudo chmod +x /usr/local/bin/whisper-transcribe

# Test it works
echo "Test" | whisper-transcribe /dev/stdin 2>/dev/null && echo "✅ Working"
```

**为了支持多种语言，请使用 `base` 模型，而不是 `base.en`：**
```bash
bash ./models/download-ggml-model.sh base
# Update the wrapper script to use ggml-base.bin
```

**自定义二进制路径：** 如果 Whisper 安装在其他位置，请在 `~/.clawtime/.env` 中设置 `WHISPER_BIN`。

**备用方案：** 如果 Whisper 无法使用或出现故障，ClawTime 会切换到基于浏览器的 SpeechRecognition API（准确性较低，且大多数浏览器仅支持英语）。

### 2. 询问用户关于他们的 AI 助手的信息

在配置之前，请询问用户：

> “您希望您的 AI 助手具有什么样的外观？请描述一下它的头像、性格以及颜色偏好。”

根据用户的回答：
- **选择名称** — 助手的显示名称
- **选择表情符号** — 代表助手的表情符号（例如：🤖、🦊、🔥、🦉）

**注意：** 主题颜色会自动从头像生成。如果您创建了自定义头像，请在 `AVATAR_META` 中设置颜色，它将自动应用于整个用户界面。

### 3. 配置（必需）

**⚠️ 您必须设置网关令牌，否则 ClawTime 会显示“需要设备身份验证”的错误。**

**步骤 1：** 获取网关令牌：
```bash
# Option A: Check existing config
grep -o '"token":"[^"]*"' ~/.openclaw/openclaw.json | head -1

# Option B: Generate new token if needed
openssl rand -hex 24
```

**步骤 2：** 使用令牌创建 `~/.clawtime/.env` 文件：
```bash
cat > ~/.clawtime/.env << 'EOF'
GATEWAY_TOKEN=<paste_token_here>
BOT_NAME=AgentName
BOT_EMOJI=🤖
EOF
```

**步骤 3：** 在继续之前进行验证：
```bash
# Must show a valid token (not empty, not "your_openclaw_gateway_token")
grep GATEWAY_TOKEN ~/.clawtime/.env
```

如果令牌缺失或无效，ClawTime 无法连接到 OpenClaw 网关。

### 4. 创建自定义 3D 头像（推荐）

ClawTime 使用 **Three.js 体素头像** — 这些 3D 角色由简单的形状组成，并根据状态（空闲、思考、说话等）进行动画展示。可以参考 `public/avatars/lobster.js` 作为实现示例。

**步骤 1：** 在 `~/.clawtime/avatars/<name>.js` 文件中创建头像文件：

```javascript
/* AVATAR_META {"name":"MyAgent","emoji":"🤖","description":"Custom 3D avatar","color":"4f46e5"} */
(function() {
  'use strict';
  
  var scene, camera, renderer, character;
  var head, leftEye, rightEye, mouth;
  var clock = new THREE.Clock();
  var currentState = 'idle';
  var isInitialized = false;

  // ─── Required: Initialize the 3D scene ───
  window.initAvatarScene = function() {
    if (isInitialized) return;
    
    var container = document.getElementById('avatarCanvas');
    if (!container) return;
    
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f1318);
    
    var w = container.clientWidth, h = container.clientHeight;
    camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 100);
    camera.position.set(0, 2, 8);
    camera.lookAt(0, 0, 0);
    
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);
    
    // Lighting
    scene.add(new THREE.AmbientLight(0x606080, 1.5));
    var light = new THREE.DirectionalLight(0xffffff, 2.0);
    light.position.set(4, 10, 6);
    scene.add(light);
    
    // Build your character here
    character = new THREE.Group();
    buildCharacter();
    scene.add(character);
    
    isInitialized = true;
    animate();
  };
  
  function buildCharacter() {
    // Body (main color from AVATAR_META)
    var bodyMat = new THREE.MeshLambertMaterial({ color: 0x4f46e5 });
    var body = new THREE.Mesh(new THREE.BoxGeometry(1.5, 2, 1), bodyMat);
    body.position.y = 0;
    character.add(body);
    
    // Head
    var headMat = new THREE.MeshLambertMaterial({ color: 0x4f46e5 });
    head = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1), headMat);
    head.position.y = 1.8;
    character.add(head);
    
    // Eyes (white with black pupils)
    var eyeMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    var pupilMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
    
    leftEye = new THREE.Mesh(new THREE.SphereGeometry(0.15), eyeMat);
    leftEye.position.set(-0.25, 1.9, 0.5);
    character.add(leftEye);
    
    rightEye = new THREE.Mesh(new THREE.SphereGeometry(0.15), eyeMat);
    rightEye.position.set(0.25, 1.9, 0.5);
    character.add(rightEye);
    
    // Mouth
    mouth = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.1, 0.1), pupilMat);
    mouth.position.set(0, 1.5, 0.5);
    character.add(mouth);
  }
  
  function animate() {
    requestAnimationFrame(animate);
    var t = clock.getElapsedTime();
    
    // Idle breathing animation
    if (character) {
      character.position.y = Math.sin(t * 2) * 0.05;
    }
    
    // State-specific animations
    if (currentState === 'thinking') {
      head.rotation.z = Math.sin(t * 3) * 0.1;
    } else if (currentState === 'talking') {
      mouth.scale.y = 1 + Math.sin(t * 15) * 0.5;
    } else {
      head.rotation.z = 0;
      mouth.scale.y = 1;
    }
    
    renderer.render(scene, camera);
  }
  
  // ─── Required: Handle state changes ───
  window.setAvatarState = function(state) {
    currentState = state;
    // Add visual feedback per state (colors, animations, etc.)
  };
  
  // ─── Required: Handle connection state ───
  window.setConnectionState = function(state) {
    // state: 'online', 'connecting', 'offline'
    // Update visual indicator (glow, color, etc.)
  };
  
  // ─── Required: Handle resize ───
  window.adjustAvatarCamera = function() {
    if (!renderer) return;
    var container = document.getElementById('avatarCanvas');
    var w = container.clientWidth, h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  };
})();
```

**步骤 2：** 设置为默认头像 — 创建或更新 `~/.clawtime/config.json` 文件：

```json
{
  "selectedAvatar": "<name>"
}
```

其中 `<name>` 应与文件名（不包括 `.js` 扩展名）相匹配（例如，对于 `myagent.js`，则使用 `"selectedAvatar": "myagent"`）。

**头像设计提示：**
- 参考 `public/avatars/lobster.js` 中的完整示例，了解所有状态的表现方式
- 使用体素风格（立方体、球体）—— 以匹配 ClawTime 的设计风格
- 实现所有状态：空闲、思考、工作、说话、倾听、快乐、错误、睡眠
- 添加连接状态指示器（颜色会变化的环或光效）
- 在桌面和移动设备布局上测试头像
- 保持多边形数量适中，以优化移动设备的性能

### 5. 启动服务

**⚠️ 在启动服务之前，请完成步骤 3-4。服务器仅在启动时读取 `.env` 文件。**

```bash
# Verify config is ready
cat ~/.clawtime/.env  # Must show GATEWAY_TOKEN, BOT_NAME
cat ~/.clawtime/config.json  # Must show selectedAvatar (if custom avatar created)

# Create and start ClawTime server
cat > ~/.config/systemd/user/clawtime.service << 'EOF'
[Unit]
Description=ClawTime Server
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.openclaw/workspace/clawtime
EnvironmentFile=%h/.clawtime/.env
ExecStart=/usr/bin/node server.js
KillSignal=SIGTERM
TimeoutStopSec=120
Restart=always
EOF

systemctl --user daemon-reload
systemctl --user enable --now clawtime

# If you change .env later, restart to apply:
# systemctl --user restart clawtime
```

### 6. 设置隧道

```bash
chmod +x scripts/tunnel.sh
cp scripts/clawtime-tunnel.service ~/.config/systemd/user/
sed -i "s|%h|$HOME|g" ~/.config/systemd/user/clawtime-tunnel.service
systemctl --user daemon-reload
systemctl --user enable --now clawtime-tunnel

# Get your URL and setup token
journalctl --user -u clawtime-tunnel | grep "Setup URL"
```

**注意：** 免费的 Cloudflare 隧道会分配随机 URL，该 URL 在重启后会发生变化。此时需要重新注册 Passkey。**

**告知用户：** “免费隧道会提供一个随机 URL，该 URL 在服务器重启后会改变。如果您希望获得永久 URL（无需重新设置），可以尝试付费选项，如 [ngrok Pro](https://ngrok.com)（每月 8 美元）或 [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)，它们提供带有自定义域名的稳定 URL。”

### 7. 将设置链接发送给用户

设置完成后，将一次性设置链接发送给用户：

> “您的 ClawTime 已经准备好了！🎉
>
> **设置链接：`https://YOUR-URL.trycloudflare.com?setup=YOUR_TOKEN`
>
> **在手机上将其保存为应用程序：**
>
> **iPhone/iPad：**
> 1. 在 Safari 中打开链接
> 2. 点击分享按钮（带有箭头的方形图标）
> 3. 向下滚动并点击“添加到主屏幕”
> 4. 点击“添加”
>
> **Android：**
> 1. 在 Chrome 中打开链接
> 2. 点击三点菜单
> 3. 点击“添加到主屏幕”
> 4. 点击“添加”
>
> 注册 Passkey 后，您就可以从主屏幕随时访问 ClawTime 了——就像使用普通应用程序一样！**

## 操作

```bash
# Status & logs
systemctl --user status clawtime
journalctl --user -u clawtime -f

# Restart after config changes  
systemctl --user restart clawtime

# Get current tunnel URL
journalctl --user -u clawtime-tunnel | grep trycloudflare | tail -1
```

## 语音模式

- 点击头像开始语音对话
- **语音转文本 (STT)：** 默认使用服务器端的 Whisper 功能（更准确，支持多种语言）
- **文本转语音 (TTS)：** 使用 edge-tts（无需 API 密钥）
- **插话：** 在机器人说话时插话
- **视觉反馈：** 在聊天界面显示 “🎤 正在录制...” → “⏳ 正在转录...” 的提示
- **静音检测：** 在发送音频前会等待 2 秒的静默时间
- 配置语音：在 `~/.clawtime/.env` 中设置 `TTS_VOICE=en-US-AndrewNeural`

### 语音模式功能
| 功能 | 描述 |
|---------|-------------|
| Whisper STT | 服务器端的语音转文本功能（默认）。如果 Whisper 不可用，则切换到浏览器端。 |
| 插话 | 在机器人正在说话时插话 |
| 噪音过滤 | 噪音检测阈值设置为 0.07 RMS，以平衡响应速度和噪音抑制 |
| 2 秒静默：** 停止说话后等待 2 秒再发送音频 |
| 噪音过滤：** 过滤掉 Whisper 输出中的噪音（如吸鼻声、[音乐] 等）
| 视觉状态提示 | 显示 “🎤 正在录制 → ⏳ 正在转录 → 机器人正在思考 → 机器人正在说话” |
| 自动同步 | 在 WebSocket 重新连接后，语音模式状态会自动同步 |

## 关键文件

| 路径 | 用途 |
|------|---------|
| `~/.clawtime/.env` | 保密信息和配置设置 |
| `~/.clawtime/config.json` | 头像选择和偏好设置 |
| `~/.clawtime/credentials.json` | Passkey 数据 |
| `~/.clawtime/avatars/` | 自定义头像文件 |

## 故障排除

### “需要设备身份验证” 错误
**原因：** `~/.clawtime/.env` 文件中缺少或无效的 `GATEWAY_TOKEN`

**解决方法：**
```bash
# 1. Get token from OpenClaw config
TOKEN=$(grep -o '"token":"[^"]*"' ~/.openclaw/openclaw.json | cut -d'"' -f4 | head -1)

# 2. Set it in ClawTime config
echo "GATEWAY_TOKEN=$TOKEN" >> ~/.clawtime/.env

# 3. Restart
systemctl --user restart clawtime
```

### 头像未显示或显示错误头像
**原因：** 创建了自定义头像但未设置为默认头像

**解决方法：**
```bash
# Set your avatar as default (replace "myavatar" with your filename without .js)
echo '{"selectedAvatar":"myavatar"}' > ~/.clawtime/config.json
systemctl --user restart clawtime
```

### 连接频繁中断
**原因：** 隧道 URL 发生变化（免费 Cloudflare 隧道的限制）

**解决方法：** 检查新的 URL 并重新注册 Passkey：
```bash
journalctl --user -u clawtime-tunnel | grep trycloudflare | tail -1
```