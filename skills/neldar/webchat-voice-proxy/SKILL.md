---
name: webchat-voice-proxy
description: >
  OpenClaw WebChat控制界面的语音输入和麦克风按钮功能：  
  - 为聊天界面添加麦克风按钮；  
  - 通过浏览器的`MediaRecorder`模块录制音频；  
  - 使用`faster-whisper`技术进行本地语音转文字处理；  
  - 将转录后的文本实时插入聊天内容中；  
  - 支持HTTPS/WSS反向代理协议，以及TLS证书管理功能，确保数据传输安全；  
  - 全部语音转文字处理过程在本地完成，无需支付任何API费用；  
  - 实时显示语音活动量（通过VU仪表盘显示）；  
  - 支持“按住说话”（Push-to-Talk）和“开关模式”（点击开始/停止）功能，可通过双击切换；  
  - 提供键盘快捷键：`Ctrl+Space`用于开启/关闭语音输入功能，`Ctrl+Shift+M`用于连续录制；  
  - 界面支持多语言本地化（内置英语、德语、中文，可扩展支持更多语言）；  
  关键词：  
  语音输入、麦克风、WebChat、控制界面、语音转文字（Speech-to-Text, STT）、本地转录、`MediaRecorder`、HTTPS代理、语音按钮、按住说话（Push-to-Talk）、键盘快捷键、国际化（i18n）。
requires:
  config_paths:
    - ~/.openclaw/openclaw.json (appends allowedOrigins entry)
  modified_paths:
    - <npm-global>/openclaw/dist/control-ui/index.html (injects script tag)
    - <npm-global>/openclaw/dist/control-ui/assets/voice-input.js (copies asset)
    - ~/.config/systemd/user/openclaw-voice-https.service (creates unit)
    - ~/.openclaw/hooks/voice-input-inject/ (creates startup hook)
    - ~/.openclaw/workspace/voice-input/ (copies runtime files)
    - ~/.openclaw/workspace/voice-input/certs/ (generates self-signed TLS cert)
  env:
    - VOICE_HTTPS_PORT (optional, default: 8443)
    - VOICE_HOST (optional, default: 127.0.0.1 — set to a LAN IP to expose externally)
    - VOICE_ALLOWED_ORIGIN (optional, default: https://<VOICE_HOST>:<VOICE_HTTPS_PORT>)
    - VOICE_LANG (optional, default: auto — prompts interactively if not set)
  persistence:
    - "User systemd service: openclaw-voice-https.service (HTTPS/WSS proxy)"
    - "Gateway startup hook: voice-input-inject (re-injects JS after updates)"
  privileges: user-level only, no root/sudo required
  dependencies:
    - python3 with aiohttp >= 3.9.0 (pip)
    - faster-whisper transcription service on port 18790
    - openssl (for self-signed cert generation)
---
# WebChat语音代理

为OpenClaw WebChat设置一个可重启的安全语音处理栈（包括当前完善的麦克风/停止/计时器UI状态）：
- 在8443端口上提供HTTPS控制UI
- 将`/transcribe`代理请求转发到本地的faster-whisper服务
- 通过WebSocket将请求转发到网关（`ws://127.0.0.1:18789`）
- 将语音按钮的脚本注入到控制UI中
- 实时显示声音强度：按钮的阴影部分和刻度会根据声音强度变化而变化
- **按住麦克风按钮开始录音**：按住按钮进行录音，释放按钮开始发送（默认模式）
- **切换模式**：点击按钮开始/停止录音（双击麦克风按钮可切换模式）
- **键盘快捷键**：`Ctrl+Space`开始/停止按住麦克风录音，`Ctrl+Shift+M`开始/停止连续录音
- **本地化UI**：自动检测浏览器语言（内置英语、德语、中文），支持自定义

## 先决条件（必需）

此功能需要一个本地的faster-whisper HTTP服务。
默认设置如下：
- URL：`http://127.0.0.1:18790/transcribe`
- systemd用户服务：`openclaw-transcribe.service`

在部署前请验证以下内容：
```bash
systemctl --user is-active openclaw-transcribe.service
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18790/transcribe -X POST -H 'Content-Type: application/octet-stream' --data-binary 'x'
```

如果缺少此依赖项，请先安装faster-whisper（包括模型加载和HTTP端点），然后再运行此功能。

相关功能：
- `faster-whisper-local-service`（后端依赖项）
- `webchat-voice-full-stack`（用于部署后端和代理的元安装工具）

## 工作流程

1. 确保转录服务存在并正在运行（`openclaw-transcribe.service`）。
2. 将`voice-input.js`文件部署到控制UI的资源文件夹中，并将其脚本标签注入`index.html`文件。
3. 配置网关允许的请求来源地址。
4. 以持久化用户服务的方式运行HTTPS+WSS代理（`openclaw-voice-https.service`）。
5. 检查并解决配对/令牌/来源地址相关的错误。

## 安全注意事项

- **默认使用localhost**：HTTPS代理仅绑定到`127.0.0.1`。除非您将`VOICE_HOST`设置为局域网IP地址，否则其他设备无法访问该代理。
- **局域网暴露**：将`VOICE_HOST`设置为局域网IP地址会导致代理（以及网关的WebSocket和转录端点）对局域网内的所有设备可见。请仅在可信任的网络环境中使用此设置。
- **持久化设置**：此功能会安装一个在系统启动时自动运行的用户服务`openclaw-voice-https.service`，以及一个在更新后重新注入UI脚本的钩子。使用`uninstall.sh`命令可以完全恢复原始状态。
- **自签名TLS证书**：自动生成的证书可能不被浏览器信任。首次访问时可能会出现证书警告。

## 部署

仅在本地运行（默认设置，最安全）：
```bash
bash scripts/deploy.sh
```

或者将其暴露在局域网中（以便其他设备访问）：
```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 VOICE_LANG=de bash scripts/deploy.sh
```

如果在运行时未设置`VOICE_LANG`参数，脚本会要求您选择UI语言（`auto`、`en`、`de`、`zh`）。设置`VOICE_LANG=auto`可跳过语言选择提示。

此脚本是幂等的（多次运行不会产生不同结果）。

## 快速验证

运行以下命令：
```bash
bash scripts/status.sh
```

预期结果：
- 两个服务均处于活跃状态
- 脚本注入成功
- 返回HTTP状态码200

## 常见问题解决方法

- **404 /chat?...**：可能是HTTPS代理中的单页面应用（SPA）回退问题。
- **请求来源不被允许**：请确保使用了正确的`VOICE_HOST`设置，并在`gateway.controlUi.allowedOrigins`中添加了相应的HTTPS来源地址。
- **令牌缺失**：尝试访问`?token=...`的URL。
- **需要配对**：通过`openclaw devices approve <requestId> --token <gateway-token>`命令批准待配对的设备。
- 重启后麦克风无法使用：请确保证书路径是持久化的（不要使用`/tmp`临时文件夹）。
- 无转录结果：请先检查本地的faster-whisper服务。

有关详细命令，请参阅`references/troubleshooting.md`。

## 该功能修改的内容

在安装之前，请注意`deploy.sh`命令会对系统进行的更改：

| 修改内容 | 修改路径 | 修改操作 |
|---|---|---|
| 控制UI HTML | `<npm-global>/openclaw/dist/control-ui/index.html` | 添加`<script>`标签以引入voice-input.js脚本 |
| 控制UI资源文件 | `<npm-global>/openclaw/dist/control-ui/assets/voice-input.js` | 复制麦克风按钮相关的JavaScript文件 |
| 网关配置 | `~/.openclaw/openclaw.json` | 在`gateway.controlUi.allowedOrigins`中添加HTTPS来源地址 |
| systemd服务 | `~/.config/systemd/user/openclaw-voice-https.service` | 创建并启用持久的HTTPS代理服务 |
| 网关钩子 | `~/.openclaw/hooks/voice-input-inject/` | 安装启动钩子，在更新后重新注入JavaScript脚本 |
| 工作区文件 | `~/.openclaw/workspace/voice-input/` | 复制`voice-input.js`和`https-server.py`文件 |
| TLS证书 | `~/.openclaw/workspace/voice-input/certs/` | 首次运行时生成自签名证书 |

注入的JavaScript文件`voice-input.js`会在控制UI中运行，并与聊天输入功能进行交互。在部署前请仔细审查其源代码。

## 麦克风按钮控制

| 操作 | 功能 |
|---|---|
| **按住**（按住麦克风按钮） | 按住按钮时开始录音，释放按钮时开始转录 |
| **点击**（切换模式） | 开始/停止录音并开始转录 |
| **双击** | 在按住模式和切换模式之间切换 |
| **右键点击** | 打开/关闭提示音 |
| **Ctrl+Space**（按住键盘） | 通过键盘开始按住麦克风录音 |
| **Ctrl+Shift+M** | 开始/停止录音（停止录音时开始转录） |
| **Ctrl+Shift+B** | 开始/停止实时转录（测试版）——文本会实时显示，2秒后自动发送，静默5秒或输入“Stop Hugo”后停止 |

按钮上的提示文本会显示当前的录音模式和可用操作。

## 语言设置 / 国际化（i18n）

UI会自动检测浏览器语言，并以相应语言显示提示信息、通知和占位文本。

**内置语言**：英语（`en`）、德语（`de`）、中文（`zh`）

### 修改语言设置

在浏览器控制台中设置语言：
```js
localStorage.setItem('oc-voice-lang', 'de');  // force German
localStorage.setItem('oc-voice-lang', 'zh');  // force Chinese
localStorage.removeItem('oc-voice-lang');      // back to auto-detect
```

然后重新加载页面。

### 添加自定义语言

编辑`voice-input.js`文件，并在`I18N`对象中添加新的语言条目。可以使用`assets/i18n.json`作为模板，其中包含所有翻译键和对应的翻译内容。

例如，添加法语语言：
```js
const I18N = {
  // ... existing entries ...
  fr: {
    tooltip_ptt: "Maintenir pour parler",
    tooltip_toggle: "Cliquer pour démarrer/arrêter",
    tooltip_next_toggle: "Mode clic",
    tooltip_next_ptt: "Push-to-Talk",
    tooltip_beep_off: "Désactiver le bip",
    tooltip_beep_on: "Activer le bip",
    tooltip_dblclick: "Double-clic",
    tooltip_rightclick: "Clic droit",
    toast_ptt: "Push-to-Talk",
    toast_toggle: "Mode clic",
    toast_beep_on: "Bip activé",
    toast_beep_off: "Bip désactivé",
    placeholder_suffix: " — Voix : (Ctrl+Espace Push-To-Talk, Ctrl+Shift+M enregistrement continu)"
  }
};
```

编辑完成后，使用`bash scripts/deploy.sh`命令重新部署，将更新后的JavaScript文件复制到控制UI中。

## CORS策略

`/transcribe`代理端点使用可配置的`Access-Control-Allow-Origin`头部。
可以通过设置`VOICE_ALLOWED-Origin`环境变量来限制访问来源。默认值：`https://<VOICE_HOST>:<VOICE_HTTPS_PORT>`。

## 卸载

要完全恢复系统到初始状态，请执行以下操作：
```bash
bash scripts/uninstall.sh
```

这将：
1. 停止并删除`openclaw-voice-https.service`服务
2. 删除网关的启动钩子
3. 从控制UI中删除`voice-input.js`文件，并撤销对`index.html`的修改
4. 从网关配置中删除HTTPS来源地址
5. 重新启动网关
6. 删除TLS证书
7. 删除工作区中的相关文件（`voice-input.js`、`https-server.py`、`i18n.json`）

请注意，卸载操作不会影响faster-whisper后端服务——如果需要卸载该服务，请单独使用`faster-whisper-local-service`命令。