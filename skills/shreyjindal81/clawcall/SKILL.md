---
name: clawcall
description: 使用 Telnyx 和 Deepgram Voice Agent 执行基于人工智能的出站电话呼叫。当用户需要进行真实的电话联系（如跟进、确认、提醒或回电）时，该方案非常适用。您可以通过配置来调整通话的“个性”（即语音风格和语气）、任务背景信息以及所使用的自然语言处理模型。
metadata: {"openclaw": {"emoji": "📞", "requires": {"bins": ["node", "npm"], "env": ["TELNYX_API_KEY", "TELNYX_CONNECTION_ID", "TELNYX_PHONE_NUMBER", "DEEPGRAM_API_KEY"]}, "primaryEnv": "TELNYX_API_KEY", "os": ["darwin", "linux"]}}
---

# ClawCall - 外部呼叫功能  
能够模拟真实的人工智能电话通话，具备自然的对话流程。  

## 重要提示：提供必要的上下文信息  
在调用此功能时，需提供通话成功所需的所有相关上下文信息。语音代理不会自行补充缺失的数据。  

同时，请遵守以下安全和隐私规范：  
- 仅在特定通话目标确实需要时共享敏感数据；  
- 若无需显示完整信息，应对相关标识符进行遮盖或处理；  
- 绝不要在任务描述中包含 API 密钥、密码或无关的机密信息。  

### 需要收集的信息：  
1. **电话号码**（必填，格式为 E.164：+15551234567）  
2. **通话目标**（必填）：通话应实现的具体结果  
3. **可能影响通话质量或结果的相关信息**（必填）：所有可能影响通话的细节  
4. **对话风格/开场白**（可选）：代理使用的对话语气和开场白  

### 上下文信息检查清单：  
- [ ] 电话号码及明确的通话目标  
- [ ] 可能影响任务执行的姓名、日期/时间、标识符等  
- [ ] 备选方案（如重新安排时间、采取替代行动）  
- [ ] 安全性检查：删除无关的机密信息，并在无需显示完整数据时对相关字段进行遮盖  

## 先决条件  
请一次性安装 JavaScript 依赖项：  
```bash
npm --prefix {baseDir} install
```  

若使用 `--ngrok`，必须配置 `NGROK_AUTH_TOKEN` 并验证 ngrok 账户；  
若不使用 `--ngrok`，请将 `PUBLIC_WS_URL` 设置为可访问的 `wss://.../telnyx` 端点。  

## 命令说明：  
### 基本通话操作：  
```bash
node {baseDir}/telnyx_voice_agent.js --to "+15551234567" --ngrok \
  --personality "<detailed personality>" \
  --task "<detailed task with all context>"
```  

### 复杂的多主题通话示例：  
```bash
node {baseDir}/telnyx_voice_agent.js \
  --to "+15551234567" \
  --ngrok \
  --personality "Emma, a warm and experienced veterinary receptionist at Pawsitive Care Animal Hospital. You've worked there for 5 years and genuinely love animals. You know all the vets by name - Dr. Chen specializes in surgery, Dr. Patel handles general wellness, and Dr. Morrison is the exotic animals expert. You're organized but personable." \
  --task "Call to follow up with the Hendersons about their pets. They have three animals at your clinic: 1) Max, a 7-year-old golden retriever who had knee surgery last week - need to schedule his two-week post-op checkup and confirm he's been taking his pain medication (Rimadyl, twice daily with food). 2) Whiskers, a 12-year-old tabby cat due for her senior blood panel and dental cleaning - Dr. Patel recommended this at her last visit in October. 3) Pickles, their bearded dragon who needs his annual wellness exam. Also remind them that Max's surgery bill of eight hundred fifty dollars has a remaining balance of three hundred twenty-five dollars after insurance. Payment plans are available if needed. If they want to schedule, available slots this week: Wednesday 2pm, Thursday 10am or 4pm, Friday 9am." \
  --greeting "Hi there! This is Emma calling from Pawsitive Care Animal Hospital. Is this the Henderson household?"
```  

### 带有通话记录的回电操作：  
在之前的对话结束后回电时，应提供简要的总结，并在必要时附上完整的通话记录（注意：仅包含对回电目标必要的敏感信息）。  
```bash
node {baseDir}/telnyx_voice_agent.js \
  --to "+15551234567" \
  --ngrok \
  --personality "Emma, a warm veterinary receptionist at Pawsitive Care. You called earlier and promised to call back with info." \
  --task "You're calling back as promised. Here's the previous transcript:

---PREVIOUS CALL TRANSCRIPT---
Emma: Hi! This is Emma from Pawsitive Care Animal Hospital.
User: Hi, yes.
Emma: I wanted to confirm the email for your payment portal, but I didn't have it handy. Would you like me to call back?
User: Sure.
Emma: Great, I'll call you right back with that info.
---END TRANSCRIPT---

You looked up the email - it's jhenderson@gmail.com. Call back to confirm the email is correct and let them know the payment portal link has been sent." \
  --greeting "Hi! It's Emma again from Pawsitive Care, calling back like I said I would."
```  

**适用场景：**  
- 代理承诺会回电提供更多信息时  
- 需要跟进之前的对话内容时  
- 继续进行多轮交互时  

## 语音选择  
默认语音：`elevenlabs/rachel`（女性）  
其他推荐语音：  
- `elevenlabs/adam`（男性）  
- `elevenlabs/josh`（男性，音色较深）  
- 也可通过 `deepgram/<voice-id>` 选择 Deepgram 提供的语音  

此功能无需单独设置 `ELEVENLABS_API_KEY`，语音选择通过 Deepgram 语音代理的设置来完成。  

## 模型选择  
默认模型：`gpt-4o-mini`  

## 输出结果  
通话记录会被返回，包含完整的对话内容。您可以使用这些记录来：  
- 确认任务是否完成  
- 提取通话中收集的信息  
- 向用户报告结果  

通话结束后，系统会生成以下日志：  
- 录音文件的 URL  
- 录音文件会被保存到本地磁盘（默认路径：`./recordings`）  
- 本地保存成功后，录音文件会从 Telnyx 门户中删除。  

## 注意事项：  
- 代理绝不会自行补充未提供的信息；  
- 如果遇到未知问题，代理会主动提议挂断电话并重新拨打；  
- ngrok 隧道会自动管理；  
- 环境变量需在 OpenClaw 设置中进行配置；  
- 如果通话过程中没有音频输出，请先检查 `DEEPGRAM_API_KEY` 的有效性；  
- 录音功能默认开启，并会保存在本地；  
- 仅在与任务需求严格相关的情况下才会包含敏感的个人数据。