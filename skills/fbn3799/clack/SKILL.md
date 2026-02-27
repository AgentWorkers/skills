---
name: clack
version: 1.5.3
description: 部署并管理 Clack——这是一个专为 OpenClaw 设计的语音中继服务器。它通过 Speech-to-Text (STT) 将语音输入（WebSocket）传输到 OpenClaw 代理，再由代理将文本转换为语音（TTS），从而实现与代理的实时语音对话。Clack 支持 ElevenLabs、OpenAI 和 Deepgram 作为 STT/TTS 服务提供商。用户可以在应用程序设置中独立选择每次会话的 STT 和 TTS 服务提供商（包括设备内置的提供商）。Clack 支持加密连接（通过 Domain SSL 或 Tailscale），并提供了本地语音模式：在这种模式下，STT/TTS 操作在设备上完成，只有大型语言模型 (LLM) 的调用才会通过服务器进行。当用户需要设置语音聊天、语音中继、语音界面，或通过语音与代理交流时，Clack 是一个理想的选择。
metadata:
  openclaw:
    requires:
      env:
        - OPENCLAW_GATEWAY_TOKEN
        - RELAY_AUTH_TOKEN
      bins:
        - python3
        - systemctl
    primaryEnv: OPENCLAW_GATEWAY_TOKEN
    os:
      - linux
    emoji: "🎙️"
    homepage: https://github.com/fbn3799/clack-skill
---
# Clack

这是一个WebSocket中继服务器，支持与OpenClaw代理进行实时语音对话。

**工作流程：** 客户端音频（PCM格式，16kHz/16位/单声道） → 音频转文本（STT） → OpenClaw网关 → 语音转文本（TTS） → 将文本转换回PCM格式的音频发送给客户端。

**会话中的提供者选择：** 客户端可以在每次通话中独立选择STT和TTS提供者——可以是设备内置的（Apple语音框架）或服务器端的提供者（ElevenLabs、OpenAI、Deepgram）。服务器会根据配置的API密钥自动检测所有可用的提供者，并通过`/info`接口展示这些提供者。

## 先决条件

- Python 3.10及以上版本
- 至少一个提供者（ElevenLabs、OpenAI或Deepgram）的API密钥（本地语音模式不需要）
- 已启用`chatCompletions`端点的OpenClaw网关
- 具有root或sudo权限（用于systemd管理）
- **安全连接**：建议使用带有SSL的域名或Tailscale进行加密连接

## 设置

运行设置脚本。该脚本会创建一个虚拟环境（venv），安装依赖项，提示输入API密钥，配置systemd服务，并可选地设置SSL连接。

### 选项

| 标志 | 默认值 | 描述 |
|------|---------|-------------|
| `--port` | `9878` | 中继服务器端口 |
| `--domain` | *(无)* | 用于SSL设置的域名（启用WSS） |

### 连接模式

所有连接都是加密的。该应用支持两种连接模式：

**使用SSL的域名（推荐）：**  
需要一个DNS A记录将域名指向服务器IP地址。设置脚本会通过Caddy自动配置SSL。你可以使用[DuckDNS](https://www.duckdns.org)提供的免费域名，或者使用自己的域名。

**Tailscale：**  
不需要设置域名或SSL。Tailscale会在网络层对所有流量进行加密。在服务器和手机上安装Tailscale，然后在应用中使用服务器的Tailscale IP地址。

**安全提示：** 应将端口9878设置为防火墙的禁止访问端口。仅允许通过localhost（用于Caddy反向代理）和Tailscale进行访问。该应用不支持未加密的公共网络连接。

### 启用OpenClaw网关的`chatCompletions`端点

必须启用网关的`chatCompletions`功能。请应用以下配置更改：

## 管理

## 客户端应用

**iOS版** — 可在[App Store](https://clack-app.com)购买（或从[github.com/fbn3799/clack-app](https://github.com/fbn3799/clack-app)源代码编译）
**Android版** — 即将推出！

## 安全性

### 认证

除了`GET /health`和`POST /pair`之外的所有接口都需要有效的认证令牌（`RELAY_AUTH_TOKEN`）。令牌通过恒定时间HMAC验证来防止时间攻击。

### 配对系统

- 配对码为6位字母数字组合（约21亿种可能）
- 配对码在5分钟后过期，且只能使用一次
- 每个IP每5分钟最多尝试5次配对请求，失败后会返回HTTP 429错误
- 失败的尝试会有2秒的延迟，以减缓暴力破解尝试
- 生成配对码需要管理员认证令牌（`GET /pair`）
- 兑换配对码是公开的，但也需要进行速率限制（`POST /pair`）

### 加密连接

- **使用域名模式：** 通过Caddy使用WSS（WebSocket安全）并自动配置SSL证书
- **使用Tailscale模式：** 在网络层使用WireGuard加密
- 应用强制使用加密连接，不允许未加密的公共访问
- 端口9878应设置为防火墙的禁止访问端口；仅允许通过localhost和Tailscale访问

### 输入清洗

所有用户输入的文本在处理前都会进行清洗：
- **语音转录内容：** 最长300个字符（`CLACK_MAX_INPUT_CHARS`），通过回声检测过滤掉无意义的文本
- **用户上下文：** 仅保留自然语言字符（字母、数字、常见标点符号和空格）。控制字符、转义序列和不可打印字符会被删除。上下文长度最多为1000个字符。在注入系统提示之前，上下文会被用明确的分隔符包裹起来。
- **禁止执行shell命令：** 所有外部通信都通过结构化的HTTP/WebSocket接口进行。用户输入不会被传递给shell。

### 数据隐私

- 不会进行数据分析、跟踪或遥测
- 语音音频只会发送到你的服务器以及你选择的提供者
- iOS应用仅将设置信息存储在本地（服务器地址、令牌、偏好设置）
- 第三方API的使用取决于你选择的提供者（ElevenLabs、OpenAI、Deepgram）

## 会话路由

每次语音通话都会在OpenClaw中创建一个`clack:<uuid>`会话。这些会话是独立的，每个通话都会创建一个新的会话，因此语音对话不会干扰主代理的上下文。

### 会话选择器

iOS应用中的会话选择器仅用于**上下文注入**。当你选择一个会话ID时，它会被作为文本上下文添加到LLM的提示中，但不会改变路由方式。所有语音通话仍然会创建自己的`clack:<uuid>`会话。

## 用户上下文

用户可以提供持久化的上下文，这些上下文会在每次语音通话时被注入到系统中。这可以让AI了解用户的偏好、备注或任何背景信息。

### 设置上下文的方法

- **应用文本字段：** 在Clack应用的“设置”→“上下文”中输入文本
- **会话选择器：** 选择一个OpenClaw会话，将其内容作为上下文注入
- **WebSocket消息：** 在语音通话期间发送`{"type": "set_context", "text": "..."}`消息
- **HTTP API：** 使用`PUT /context?token=...&text=...`或`POST /context`，其中`{"text": "..."`为JSON格式

上下文在保存前会进行清洗——只保留自然语言字符。IP地址和域名会被删除。服务器会在响应中返回清洗后的文本，以便应用能够准确地显示将要发送的上下文内容。

上下文会在通话之间和服务器重启后保持不变。可以通过`DELETE /context`或发送空的`set_context`消息来清除上下文。

## 对话历史记录

中继服务器会在通话之间维护一个共享的历史记录文件，以确保对话的连续性。历史记录以JSON格式存储在`CLACK_HISTORY_DIR`目录中（默认路径：`/var/lib/clack/history`）。
- **最大记录条数：** 50条（可通过`CLACK_MAX_HISTORY`配置）
- 历史记录会在通话之间和服务器重启后保持不变
- 可通过`GET /history`查看，通过`DELETE /history`清除

## 回声测试模式

为了在不使用LLM信用的情况下测试音频传输，可以设置以下环境变量：

- **全局模式：** 设置`CLACK_ECHO_MODE=true`
- **会话模式：** 客户端发送`{"type":"start","config":{"echo":true}`消息

在回声模式下，转录的文本会通过TTS回放，而不会发送给LLM。音频会进行峰值归一化处理，以确保播放音量一致。

## 提供者选择

每次会话都可以独立配置STT和TTS提供者。服务器在启动时会根据设置的API密钥（`ELEVENLABS_API_KEY`、`OPENAI_API_KEY`、`DEEPGRAM_API_KEY`）自动检测所有可用的提供者。

### 可用的模式（STT / TTS）：

- **设备内置（本地）：** 使用Apple内置的语音框架。无需支付API费用。
- **服务器端提供者：** ElevenLabs、OpenAI或Deepgram——取决于配置的密钥。

### 工作原理：
1. 应用通过`GET /info`请求来发现可用的提供者
2. 用户在“设置”→“语音”选项中独立选择STT和TTS提供者
3. 通话开始时，应用会在会话配置中发送`sttProvider`和`ttsProvider`
4. 服务器会根据会话创建相应的提供者实例

### 示例组合：

| STT提供者 | TTS提供者 | 使用场景 |
|---------|---------|----------|
| ElevenLabs | ElevenLabs | 使用完整的云服务——获得最佳音质 |
| 设备内置 | ElevenLabs | 节省STT费用，同时使用高级语音服务 |
| 设备内置 | 设备内置 | 完全本地处理——无需API费用，支持离线使用 |
| OpenAI | Deepgram | 自由组合不同的提供者 |

**成本优化：** 可以使用免费的设备内置STT服务（无费用）和高级云语音服务，从而获得高质量的音频输出，同时完全免除转录费用。或者完全使用设备内置服务，实现零API费用。

### 文本输入模式

当STT设置为设备内置时，客户端会发送转录的文本，而不是音频：

当TTS设置为设备内置时，服务器只会返回`response_text`，而不会进行音频合成。

## AI响应规则

- AI的响应被限制在1-3句话以内，以保持自然的语音对话效果
- 服务器端的最大响应长度为150个字符，以防止响应过长
- 服务器端的最大输入长度为300个字符（`CLACK_MAX_INPUT_CHARS`），超过这个长度的文本会被截断

## HTTP接口

| 接口 | 方法 | 认证要求 | 描述 |
|---------|--------|------|-------------|
| `GET /health` | GET | 无 | 健康检查——返回服务状态 |
| `POST /pair` | POST | 无 | 兑换配对码以获取认证令牌（有限制） |
| `GET /pair` | GET | 是 | 生成一次性配对码 |
| `GET /info` | GET | 是 | 服务器信息：代理名称、可用的STT/TTS提供者 |
| `GET /voices` | GET | 是 | 可用的TTS语音列表 |
| `GET /sessions` | GET | 是 | 活动会话列表 |
| `GET /history` | GET | 是 | 查看对话历史记录 |
| `DELETE /history` | DELETE | 是 | 清除对话历史记录 |
| `GET /context` | GET | 是 | 获取当前用户上下文 |
| `PUT /context` | PUT | 是 | 设置用户上下文（查询参数`text`） |
| `POST /context` | POST | 是 | 设置用户上下文（JSON格式的`{"text": "..."}`） |
| `DELETE /context` | DELETE | 是 | 清除用户上下文 |
| `WebSocket /voice` | WS | 是 | 声音中继连接 |

## WebSocket协议

**接口地址：** `ws://<host>:<port>/voice?token=<RELAY_AUTH_TOKEN>`

### 客户端 → 服务器

| 消息 | 格式 | 描述 |
|---------|--------|-------------|
| `{"type":"start","config":{...}}` | JSON | 启动会话。配置参数包括`voice`、`systemPrompt`、`echo`、`sttProvider`、`ttsProvider` |
| 二进制数据帧 | 字节 | 原始PCM音频（16kHz，16位，单声道） |
| `{"type":"text_input","text":"..."}` | JSON | 本地语音模式——直接发送文本 |
| `{"type":"end_speech"}` | JSON | 表示语音结束，触发处理 |
| `{"type":"interrupt"}` | JSON | 中断当前的TTS播放 |
| `{"type":"ping"}` | JSON | 保持连接活跃 |
| `{"type":"set_context","text":"..."}` | JSON | 设置用户上下文（发送前会进行清洗） |
| `{"type":"auth","token":"..."}` | JSON | 进行认证（作为查询参数的替代方式） |

### 服务器 → 客户端

| 消息 | 格式 | 描述 |
|---------|--------|-------------|
| `{"type":"ready"}` | JSON | 会话准备就绪 |
| `{"type":"auth_ok"}` / `{"type":"auth_failed"}` | JSON | 认证结果 |
| `{"type":"processing","stage":"..."}` | JSON | 处理阶段：`transcribing`、`thinking`、`speaking`、`filtered` |
| `{"type":"transcript","text":"...","final":true}` | JSON | STT处理结果 |
| `{"type":"response_text","text":"..."}` | JSON | AI的文本响应 |
| `{"type":"response_start","format":"pcm_16000"}` | JSON | 开始播放音频流 |
| 二进制数据帧 | 字节 | TTS音频（PCM格式，16kHz，16位，单声道） |
| `{"type":"response_end"}` | JSON | 音频流结束 |
| `{"type":"tts_cancelled"}` | JSON | TTS播放被中断 |
| `{"type":"context_updated","text":"..."}` | JSON | 上下文已保存——`text`字段包含清洗后的上下文 |
| `{"type":"context_cleared"}` | JSON | 上下文已被清除 |

## 功能特性

- **多提供者STT/TTS**：支持ElevenLabs、OpenAI和Deepgram
- **独立的语音输入/输出配置**：可以分别选择STT和TTS提供者，完全控制语音的转录方式和AI的播放方式
- **设备内置语音**：使用Apple的语音框架进行STT和/或TTS处理——无需支付API费用，可以自由组合不同的云服务
- **成本优化**：可以使用免费的设备内置转录服务搭配高级云语音服务，或者完全使用本地服务以实现零费用
- **语音响应规则**：AI的响应被限制在1-3句话以内
- **输入长度限制**：可配置的最大转录长度（默认为300个字符）
- **置信度过滤**：丢弃置信度较低的STT结果
- **回声检测**：防止语音反馈循环（TTS → 麦克风 → STT）
- **回声测试模式**：可以在全局或会话级别测试音频传输流程
- **音频归一化**：在回声模式下对音频进行峰值归一化处理
- **音频分块**：长录音会自动分割以便于准确转录
- **异常检测**：过滤重复或无意义的STT输出
- **中断/TTS取消**：可以中断正在进行的TTS播放
- **配对系统**：使用一次性代码进行安全的设备配对
- **会话隔离**：每次通话都会创建独立的`clack:<uuid>`会话
- **对话历史记录**：会话之间的历史记录会共享，最多保存50条记录
- **令牌认证**：使用恒定时间HMAC进行验证
- **保持连接活跃**：在AI响应较长时防止客户端超时
- **静音检测**：默认阈值220，可配置范围为20–1000
- **自动重启**：在系统崩溃时自动重启

## 语音配置

提供20种内置的ElevenLabs语音。默认语音为`Will`。你可以在会话配置中指定语音的名称或ID：

### 可用的语音名称：

will, aria, roger, sarah, laura, charlie, george, callum, river, liam, charlotte, alice, matilda, jessica, eric, chris, brian, daniel, lily, bill

## 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `RELAY_AUTH_TOKEN` | — | **必需**。客户端认证令牌（32个字符） |
| `OPENCLAW_GATEWAY_URL` | `http://127.0.0.1:18789` | OpenClaw网关地址 |
| `OPENCLAW_GATEWAY_TOKEN` | — | 网关令牌 |
| `STT_PROVIDER` | `elevenlabs` | STT提供者（可选值：`elevenlabs`、`openai`、`deepgram`） |
| `TTS_PROVIDER` | `elevenlabs` | TTS提供者（可选值：`elevenlabs`、`openai`、`deepgram`） |
| `TTS_VOICE` | `Will` | 默认语音（名称或ID） |
| `VOICE_RELAY_PORT` | `9878` | 服务器端口 |
| `CLACK_ECHO_MODE` | `false` | 全局启用回声测试模式 |
| `CLACK_MAX_INPUT_CHARS` | `300` | 最大转录长度（字符数） |
| `CLACK_HISTORY_DIR` | `/var/lib/clack/history` | 历史记录文件存储目录 |
| `CLACK_MAX_HISTORY` | `50` | 最大对话历史记录条数 |
| `CLACK_AGENT_NAME` | `Storm` | iOS应用中显示的代理名称 |

提供者的API密钥（`ELEVENLABS_API_KEY`、`OPENAI_API_KEY`、`DEEPGRAM_API_KEY`）存储在`config.json`文件中，文件权限受到限制，不会作为环境变量传递。设置脚本会交互式地管理这些密钥。