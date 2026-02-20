---
name: webchat-voice-proxy
description: >
  **OpenClaw WebChat 控制界面的语音输入与麦克风功能**  
  该功能为 OpenClaw WebChat 控制界面添加了麦克风按钮，允许用户通过浏览器内置的 `MediaRecorder` 模块录制音频，并使用 `faster-whisper` 工具进行实时转录。转录后的文本会直接插入聊天对话中。系统支持 HTTPS/WSS 反向代理和 TLS 证书管理，以确保数据传输的安全性。整个语音转文字过程完全在本地完成，无需支付任何 API 使用费用。实时语音活动显示在界面上的 VU（Voice Activity）仪表盘中。用户可通过长按按钮开启“按住说话”（Push-to-Talk）模式，或通过双击切换“开始/停止”状态。支持键盘快捷键：`Ctrl+Space` 用于开启/关闭 PTT（Push-to-Talk）功能，`Ctrl+Shift+M` 用于连续录制音频。界面提供多语言支持（内置英语、德语、中文，可扩展其他语言）。  
  **关键词**：  
  语音输入、麦克风、WebChat、控制界面、语音转文字（Speech-to-Text, STT）、本地转录、`MediaRecorder`、HTTPS 代理、语音按钮、按住说话（Push-to-Talk）、键盘快捷键、国际化（i18n）。
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
    - VOICE_HOST (optional, auto-detected from hostname -I)
    - VOICE_ALLOWED_ORIGIN (optional, default: https://<VOICE_HOST>:<VOICE_HTTPS_PORT>)
    - VOICE_LANG (optional, default: auto — prompts interactively if not set)
  persistence:
    - "User systemd service: openclaw-voice-https.service (HTTPS/WSS proxy)"
    - "Gateway startup hook: voice-input-inject (re-injects JS after updates)"
  privileges: user-level only, no root/sudo required
  dependencies:
    - python3 with aiohttp (pip)
    - faster-whisper transcription service on port 18790
    - openssl (for self-signed cert generation)
---
# WebChat语音代理

为OpenClaw WebChat设置一个可在重启后仍保持正常运行的语音功能（包括当前完善的麦克风控制、停止以及时间显示界面）：

- 在8443端口上提供HTTPS控制界面
- 将`/transcribe`请求代理到本地的faster-whisper服务
- 通过WebSocket将语音数据传输到网关（`ws://127.0.0.1:18789`）
- 将语音控制脚本注入到控制界面中
- 实时显示语音音量：麦克风按钮的阴影部分和刻度会随着音量变化而变化
- **按住麦克风按钮开始录音**：松开按钮即可发送录音
- **切换模式**：点击按钮开始/停止录音（双击麦克风按钮可切换模式）
- **键盘快捷键**：`Ctrl+Space`用于按住麦克风开始录音，`Ctrl+Shift+M`用于开始/停止连续录音
- **支持多语言界面**：自动检测浏览器语言（内置英语、德语、中文），并可自定义

## 先决条件（必需）

此功能需要一个本地的faster-whisper HTTP服务。  
默认配置：
- URL：`http://127.0.0.1:18790/transcribe`
- systemd用户服务：`openclaw-transcribe.service`

在部署前请先验证这些依赖项是否已正确设置：
```bash
systemctl --user is-active openclaw-transcribe.service
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18790/transcribe -X POST -H 'Content-Type: application/octet-stream' --data-binary 'x'
```

如果缺少该依赖项，请先安装faster-whisper服务（包括模型加载和HTTP端点配置），然后再部署此功能。

**相关功能：**
- `faster-whisper-local-service`（后端依赖项）
- `webchat-voice-full-stack`（用于部署后端和代理服务的元安装工具）

## 工作流程：

1. 确保转录服务（`openclaw-transcribe.service`）已启动并运行。
2. 将`voice-input.js`文件部署到控制界面的资源目录中，并将其脚本标签注入到`index.html`文件中。
3. 配置网关以允许外部HTTPS请求的来源地址。
4. 以持久化用户服务的形式运行HTTPS+WSS代理（`openclaw-voice-https.service`）。
5. 检查并解决配对、令牌以及来源地址相关的错误。

## 部署

**自动检测主机IP并运行脚本：**
```bash
bash scripts/deploy.sh
```

**或手动指定主机、端口和语言：**
```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 VOICE_LANG=de bash scripts/deploy.sh
```

如果未指定`VOICE_LANG`参数，脚本会提示您选择界面语言（`auto`、`en`、`de`、`zh`）。设置`VOICE_LANG=auto`可跳过此提示。

此脚本具有幂等性（多次运行不会产生不同结果）。

## 快速验证

运行以下命令进行验证：
```bash
bash scripts/status.sh
```

预期结果：
- 两个服务均处于活跃状态
- 脚本已成功注入控制界面
- 响应状态码为`https:200`

## 常见问题解决方法：

- **404 /chat?...**：可能是HTTPS代理中的单页面应用（SPA）回退问题。
- **“origin not allowed”**：请确保使用了正确的`VOICE_HOST`地址，并在`gateway.controlUi.allowedOrigins`配置中添加了相应的HTTPS来源地址。
- **令牌缺失**：尝试访问`?token=...`的URL。
- **需要配对设备**：使用`openclaw devices approve <requestId> --token <gateway-token>`命令批准设备。
- 重启后麦克风功能失效：请确保证书路径是持久化的（不要使用`/tmp`目录）。
- 无转录结果：请先检查本地的faster-whisper服务。

具体操作命令请参考`references/troubleshooting.md`。

## 该功能会修改的系统文件：

在安装此功能之前，请注意`deploy.sh`脚本会对系统进行的以下更改：

| 修改内容 | 修改路径 | 修改操作 |
|---|---|---|
| 控制界面HTML | `<npm-global>/openclaw/dist/control-ui/index.html` | 添加`<script>`标签以引入voice-input.js脚本 |
| 控制界面资源文件 | `<npm-global>/openclaw/dist/control-ui/assets/voice-input.js` | 复制麦克风控制按钮的JavaScript代码 |
| 网关配置文件 | `~/.openclaw/openclaw.json` | 在`gateway.controlUi.allowedOrigins`中添加HTTPS来源地址 |
| systemd服务配置 | `~/.config/systemd/user/openclaw-voice-https.service` | 创建并启用持久的HTTPS代理服务 |
| 网关启动脚本 | `~/.openclaw/hooks/voice-input-inject/` | 安装启动时重新注入脚本的钩子 |
| 工作区文件 | `~/.openclaw/workspace/voice-input/` | 复制`voice-input.js`和`https-server.py`文件 |
| TLS证书 | `~/.openclaw/workspace/voice-input/certs/` | 首次运行时自动生成自签名证书 |

注入的`voice-input.js`脚本会在控制界面中运行，并与聊天输入功能进行交互。在部署前请仔细审查该脚本的源代码。

## 麦克风按钮的控制方式：

| 操作 | 功能 |
|---|---|
| **按住按钮**（PTT模式） | 按住按钮时开始录音，松开按钮时开始转录 |
| **点击按钮**（切换模式） | 开始/停止录音并转录 |
| **双击按钮** | 在PTT模式和切换模式之间切换 |
| **右键点击** | 开/关提示音 |
| **Ctrl+Space**（按住按钮） | 通过键盘控制开始录音（即使文本框处于焦点状态也可使用） |
| **Ctrl+Shift+M** | 开始/停止连续录音 |

当前模式及可用功能会在鼠标悬停在按钮上时显示在提示框中。

## 语言支持

界面会自动检测浏览器语言，并以相应语言显示提示信息、提示框内容和占位文本。

**内置语言：** 英语（`en`）、德语（`de`）、中文（`zh`）

### 更改语言设置

在浏览器控制台中设置语言偏好：
```js
localStorage.setItem('oc-voice-lang', 'de');  // force German
localStorage.setItem('oc-voice-lang', 'zh');  // force Chinese
localStorage.removeItem('oc-voice-lang');      // back to auto-detect
```

然后重新加载页面。

### 添加自定义语言

编辑`voice-input.js`文件，在`I18N`对象中添加新的语言条目。可以使用`assets/i18n.json`作为模板，其中包含所有翻译键及对应的翻译内容。

**添加法语语言的示例：**
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

编辑完成后，使用`bash scripts/deploy.sh`重新部署，将更新后的JavaScript文件复制到控制界面。

## CORS策略

`/transcribe`代理端点支持配置`Access-Control-Allow-Origin`头部。  
可以通过设置`VOICE_ALLOWED_ORIGIN`环境变量来限制允许的来源地址。默认值为`https://<VOICE_HOST>:<VOICE_HTTPS_PORT>`。

## 卸载

要完全恢复系统到初始状态，请执行以下操作：
```bash
bash scripts/uninstall.sh
```

操作步骤包括：
1. 停止并删除`openclaw-voice-https.service`服务
2. 删除网关的启动脚本
3. 从控制界面中移除`voice-input.js`文件，并取消对`index.html`文件的修改
4. 从网关配置中删除相关的HTTPS来源地址
5. 重启网关

工作区文件（`voice-input/`）和TLS证书默认会被保留。如需删除这些文件，可执行相应的命令：
```bash
rm -rf ~/.openclaw/workspace/voice-input
```

请注意：卸载此功能不会影响faster-whisper服务——如果需要卸载faster-whisper服务，请单独执行`faster-whisper-local-service`命令。