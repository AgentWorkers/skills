---
name: webchat-voice-proxy
deprecated: true
description: ⚠️ 已弃用 — 为了提高代码的模块化程度，该技能已被拆分为两个独立的技能：**webchat-https-proxy**（HTTPS/WSS 反向代理）和 **webchat-voice-gui**（麦克风按钮、语音指标显示、国际化支持）。请安装这两个技能。如需一次性部署所有组件，请使用 **webchat-voice-full-stack**。关键词：语音输入、麦克风、WebChat、控制界面、语音转文本（STT）、本地转录、MediaRecorder、HTTPS 代理、语音按钮、按键通话（PTT）、键盘快捷键、国际化（i18n）。
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

为OpenClaw WebChat设置一个重启后仍可使用的语音功能（包括当前优化过的麦克风/停止/计时器UI状态）：

- 在8443端口上提供HTTPS控制UI
- 将`/transcribe`代理请求转发到本地的`faster-whisper`服务
- 通过WebSocket将请求转发到网关（`ws://127.0.0.1:18789`）
- 将语音按钮的脚本注入到控制UI中
- 实时显示语音强度：按钮的阴影部分和刻度会根据语音强度变化而变化
- **按住说话**：按住麦克风按钮开始录音，松开按钮开始发送（默认模式）
- **切换模式**：点击按钮开始/停止录音（通过双击麦克风按钮切换）
- **键盘快捷键**：`Ctrl+Space`开始/停止按住说话，`Ctrl+Shift+M`开始/停止连续录音
- **本地化UI**：自动检测浏览器语言（内置英语、德语、中文），支持自定义

## 先决条件（必需）

此功能需要一个本地的`faster-whisper HTTP服务**。
默认设置如下：
- URL：`http://127.0.0.1:18790/transcribe`
- systemd用户服务：`openclaw-transcribe.service`

在部署前请进行验证：
```bash
systemctl --user is-active openclaw-transcribe.service
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18790/transcribe -X POST -H 'Content-Type: application/octet-stream' --data-binary 'x'
```

如果缺少此依赖项，请先设置`faster-whisper`（包括模型加载和HTTP端点），然后再运行此功能。

相关功能：
- `faster-whisper-local-service`（后端依赖项）
- `webchat-voice-full-stack`（用于部署后端和代理的元安装工具）

## 工作流程

1. 确保转录服务存在并正在运行（`openclaw-transcribe.service`）。
2. 将`voice-input.js`文件部署到控制UI的资源文件夹中，并将脚本标签注入到`index.html`文件中。
3. 配置网关允许的外部HTTPS请求来源。
4. 以持久化用户服务的方式运行HTTPS+WSS代理（`openclaw-voice-https.service`）。
5. 检查配对/令牌/来源相关的错误，并按顺序解决这些问题。

## 安全注意事项

- **默认使用本地主机**：HTTPS代理仅绑定到`127.0.0.1`。除非你将`VOICE_HOST`设置为局域网IP地址，否则其他设备无法访问该代理。
- **局域网暴露**：将`VOICE_HOST`设置为局域网IP地址会暴露代理（以及网关的WebSocket和转录端点）给该网络中的所有设备。仅在可信任的网络环境中使用此设置。
- **持久性**：此功能会安装一个在系统启动时自动运行的用户服务`openclaw-voice-https.service`，以及一个在更新后重新注入UI脚本的钩子。使用`uninstall.sh`命令可完全恢复原始状态。
- **自签名TLS证书**：自动生成的证书可能不被浏览器信任。首次访问时会出现证书警告。

## 部署

仅在本地主机上运行（默认设置，最安全）：
```bash
bash scripts/deploy.sh
```

或者将其暴露在局域网中（以便其他设备可以访问）：
```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 VOICE_LANG=de bash scripts/deploy.sh
```

如果未设置`VOICE_LANG`参数，则在交互式运行时脚本会要求您选择UI语言（`auto`、`en`、`de`、`zh`）。设置`VOICE_LANG=auto`可跳过此提示。

此脚本是幂等的（多次运行不会产生不同结果）。

## 快速验证

运行以下命令：
```bash
bash scripts/status.sh
```

预期结果：
- 两个服务均处于活动状态
- 脚本已成功注入
- 返回状态码`https:200`

## 常见问题解决方法

- **404 /chat?...**：可能是HTTPS代理中的单页面应用程序（SPA）回退问题。
- **“origin not allowed”**：确保在部署时使用了正确的`VOICE_HOST`，并在`gateway.controlUi.allowedOrigins`中添加了相应的HTTPS来源。
- **令牌缺失**：尝试访问`?token=...`的URL。
- **需要配对**：通过`openclaw devices approve <requestId> --token <gateway-token>`批准待配对的设备。
- 重启后麦克风无法使用：确保证书路径是持久化的（不要使用`/tmp`目录）。
- 无转录结果：请先检查本地的`faster-whisper`服务。

有关详细命令，请参阅`references/troubleshooting.md`。

## 该功能会修改的内容

在安装之前，请注意`deploy.sh`命令会对系统进行的以下更改：

| 修改内容 | 修改路径 | 修改操作 |
|---|---|---|
| 控制UI HTML | `<npm-global>/openclaw/dist/control-ui/index.html` | 添加用于语音输入的`<script>`标签 |
| 控制UI资源文件 | `<npm-global>/openclaw/dist/control-ui/assets/voice-input.js` | 复制麦克风按钮的JavaScript代码 |
| 网关配置 | `~/.openclaw/openclaw.json` | 在`gateway.controlUi.allowedOrigins`中添加HTTPS来源 |
| systemd服务 | `~/.config/systemd/user/openclaw-voice-https.service` | 创建并启用持久的HTTPS代理 |
| 网关钩子 | `~/.openclaw/hooks/voice-input-inject/` | 安装启动钩子，以便在更新后重新注入JavaScript代码 |
| 工作区文件 | `~/.openclaw/workspace/voice-input/` | 复制`voice-input.js`和`https-server.py`文件 |
| TLS证书 | `~/.openclaw/workspace/voice-input/certs/` | 首次运行时生成自签名证书 |

注入的JavaScript代码（`voice-input.js`）会在控制UI中运行，并与聊天输入功能交互。在部署前请仔细审查代码。

## 麦克风按钮控制

| 操作 | 功能 |
|---|---|
| **按住**（按住说话模式） | 按住按钮时开始录音，松开按钮时开始转录 |
| **点击**（切换模式） | 开始/停止录音和转录 |
| **双击** | 在按住说话模式和切换模式之间切换 |
| **右键点击** | 开/关提示音 |
| **Ctrl+Space**（按住） | 通过键盘开始按住说话（即使文本框处于焦点状态也能生效） |
| **Ctrl+Shift+M** | 开始/停止录音（停止时开始转录） |
| **Ctrl+Shift+B** | 开始/停止实时转录（测试版）——文本会实时显示，2秒后自动发送，静默5秒或输入“Stop Hugo”后停止 |

当前模式和可用操作会在鼠标悬停在按钮上时显示在提示框中。

## 语言/国际化（i18n）

UI会自动检测浏览器语言，并以相应语言显示提示框、提示信息和占位文本。

**内置语言**：英语（`en`）、德语（`de`）、中文（`zh`）

### 更改语言

在浏览器控制台中设置语言：
```js
localStorage.setItem('oc-voice-lang', 'de');  // force German
localStorage.setItem('oc-voice-lang', 'zh');  // force Chinese
localStorage.removeItem('oc-voice-lang');      // back to auto-detect
```

然后重新加载页面。

### 添加自定义语言

编辑`voice-input.js`文件，并在`I18N`对象中添加新的语言条目。可以使用`assets/i18n.json`作为模板，其中包含所有翻译键和默认翻译内容。

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

编辑完成后，使用`bash scripts/deploy.sh`重新部署，将更新后的JavaScript代码复制到控制UI中。

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
3. 从控制UI中删除`voice-input.js`文件，并取消对`index.html`的修改
4. 从网关配置中删除HTTPS来源设置
5. 重启网关
6. 删除TLS证书
7. 删除工作区的运行时文件（`voice-input.js`、`https-server.py`、`i18n.json`）

`faster-whisper`后端不会被卸载程序影响——如果需要，需通过`faster-whisper-local-service`单独卸载它。