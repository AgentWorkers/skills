---
name: sip-voice-call-control
description: 使用 Telnyx Call Control API 的语音接口：可通过 AI 答复电话、执行功能调用以及进行自然语言对话。适用于实现免提助手、基于电话的提醒功能或语音控制工具。需要 Node.js 和 Telnyx API 密钥。
metadata: {"openclaw":{"emoji":"📞","requires":{"bins":["node","npm"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# SIP语音通话控制

这是一个使用Telnix Call Control API的OpenClaw语音接口，支持通过SIP协议发起通话，并与您的AI助手进行自然对话。

## 工作原理

```
Your Phone (SIP) → Telnyx Call Control → Webhooks → This Server → Commands back
                         ↓                              ↓
                    STT/TTS/Media              LLM + Tool Execution
```

请注意：这并非基于WebRTC的技术，而是服务器端处理的SIP通话。所有音频处理由Telnix负责；我们仅接收Webhook信号并发送相应的指令。

## 设置步骤

### 1. 安装依赖项

```bash
cd skills/sip-voice-call-control
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑`.env`文件：
```env
TELNYX_API_KEY=KEY_your_api_key_here
```

### 3. 启动服务器

```bash
npm run start
```

服务器启动后，控制台会显示相应的状态信息：
```
🎙️  Assistant Voice Server ready on port 3000
📞 Dial: sip:openclaw@yourconnection.sip.telnyx.com
```

## 代理设置流程

在为用户设置AI助手时，代理需要执行以下步骤：

### 1. 收集配置信息

请求以下信息：

1. **Telnix API密钥**（必填）：
   - 获取地址：https://portal.telnyx.com/#/app/auth/v2
   - 该密钥需要具备“Voice API”和“Inference”权限。

2. **语音合成引擎**（可选）：
   - `Telnyx.NaturalHD.astra` — 女性声音，温暖清晰（默认推荐）
   - `Telnyx.NaturalHD.atlas` — 男性声音，低沉权威
   - `Polly.Amy-Neural` — 英国女性声音
   - `Polly.Brian-Neural` — 英国男性声音
   - `Polly.Joanna-Neural` — 美国女性声音
   - `Polly.Matthew-Neural` — 美国男性声音
   - `Azure.en-US-JennyNeural` — 美国女性声音
   - `Azure.en-GB-RyanNeural` — 英国男性声音
   - 完整列表请参考`.env.example`文件。

3. **语音模型**（可选）：
   - `Qwen/Qwen3-235B-A22B` — 适合执行功能调用（默认选择）
   - `meta-llama/Meta-Llama-3.1-8B-Instruct` — 执行速度最快
   - `meta-llama/Llama-3.3-70B-Instruct` — 性能均衡

代理的个性化设置（如助手名称、用户名、时区）会自动从`IDENTITY.md`和`USER.md`文件中读取。

### 2. 编写`.env`文件

```bash
cat > .env << 'EOF'
TELNYX_API_KEY=<user_api_key>
VOICE_MODEL=Qwen/Qwen3-235B-A22B
TTS_VOICE=Telnyx.NaturalHD.astra
EOF
```

### 3. 在后台持续运行服务器

服务器需要持续运行以接收通话请求。使用`nohup`命令使其在后台持续运行：
```bash
cd /path/to/sip-voice-call-control
nohup npm run start > sip-voice-call-control.log 2>&1 &
```

或者通过代理程序来启动服务器：

```typescript
// Use nohup to keep process alive after session ends
exec({ 
  command: "cd /path/to/sip-voice-call-control && nohup npm run start > sip-voice-call-control.log 2>&1 &",
  background: true 
})
```

**重要提示：** 如果不使用`nohup`，服务器会在父进程结束时自动终止。在生产环境中务必使用`nohup`或进程管理工具。

**检查服务器是否正在运行：**
```bash
ps aux | grep "tsx.*dev" | grep -v grep
```

**停止服务器：**
```bash
pkill -f "tsx.*dev.ts"
```

**查看日志：**
```bash
tail -f /path/to/sip-voice-call-control/sip-voice-call-control.log
```

### 4. 获取SIP通话地址

从服务器日志中提取SIP通话地址，并提供给用户用于拨打电话。

## 环境变量

| 变量            | 是否必填 | 默认值        | 说明                                      |
|------------------|---------|-----------------------------|
| `TELNYX_API_KEY`     | 是       |                          | Telnix API密钥                          |
| `VOICE_MODEL`       | 否       | `Qwen/Qwen3-235B-A22B`            | 用于语音合成的模型                        |
| `TTS_VOICE`       | 否       | `Polly.Amy-Neural`            | 语音合成引擎                          |
| `PORT`          | 否       | `3000`                         | 服务器监听端口                          |
| `ENABLE_TUNNEL`      | 否       | `true`                          | 是否启用Cloudflare隧道                      |
| `WORKSPACE_DIR`     | 否       | `~/clawd`                        | 工作空间目录                          |

## 可用工具

| 工具            | 触发语句                | 功能                                      |
|------------------|------------------|-------------------------------------------|
| `list_cron_jobs`      | "what reminders", "my schedule", "cron jobs" | 列出计划任务                        |
| `add_reminder`      | "remind me", "set a reminder" | 创建新的提醒                        |
| `remove_cron_job`     | "delete", "cancel" + 任务名称       | 删除已安排的任务                        |
| `get_weather`      | "weather", "temperature", "forecast" | 获取当前天气信息                        |
| `search_memory`     | "what have we been working on", "projects" | 搜索工作空间文件                        |

## 主要特性

- **低延迟**：在`enable_thinking: false`模式下，响应时间约为500毫秒至1.5秒。
- **即时插话**：用户可以随时通过语音打断助手的对话。
- **功能调用**：支持使用Qwen模型执行特定功能。
- **自动配置**：会自动创建Cloudflare隧道和Call Control应用程序。
- **个性化设置**：根据`IDENTITY.md`和`USER.md`文件中的信息进行个性化设置。

## 故障排除

- **说话后无响应**：
  - 确认Telnix API密钥具备“Voice API”和“Inference”权限。
  - 检查Webhook地址是否可访问（确保Cloudflare隧道处于激活状态）。

- **响应延迟过长（>3秒）**：
  - 确保使用`function-calling`分支（而非`main`分支）。
  - 检查Telnix账户中对应的语音模型是否可用。

- **工具无法执行命令**：
  - 确保`openclaw`命令行工具已在系统路径中。
  - 检查`WORKSPACE_DIR`是否设置正确。

- **端口已被占用**：
  - 使用`pkill -f "tsx.*dev.ts"`命令终止现有服务器进程。
  - 或者修改`.env`文件中的`PORT`设置。

## 参考资源

- Telnyx Call Control文档：https://developers.telnyx.com/docs/voice/call-control
- Telnyx Inference文档：https://developers.telnyx.com/docs/inference
- 技术细节请参阅[ARCHITECTURE.md](ARCHITECTURE.md)文件。