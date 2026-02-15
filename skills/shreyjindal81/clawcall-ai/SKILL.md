---
name: clawcall-ai
description: 使用 Telnyx 和 Deepgram Voice Agent 运行由 AI 驱动的出站电话呼叫。当用户需要进行真实的电话联系（跟进、确认、提醒、回电）时，该工具能够根据配置提供个性化的沟通方式、任务背景信息、语音模型以及通话内容。
metadata: {"openclaw": {"emoji": "📞", "requires": {"bins": ["node", "npm"], "env": ["TELNYX_API_KEY", "TELNYX_CONNECTION_ID", "TELNYX_PHONE_NUMBER", "DEEPGRAM_API_KEY"]}, "primaryEnv": "TELNYX_API_KEY", "os": ["darwin", "linux"]}}
---

# ClawCall AI - 外拨电话

通过自然流畅的对话流程，实现真实的人工智能电话通话。

## 重要提示：提供上下文信息

在使用此功能时，必须提供丰富、详细的上下文信息。语音助手不会自行假设任何信息，它仅使用您明确提供的内容。

### 需要收集的信息：
1. **电话号码**（E.164 格式：+15551234567）
2. **角色设定** – 代理应扮演什么角色？请具体说明：
   - 不佳示例： “一个接待员”
   - 佳例： “Emma，她是 Pawsitive Care 动物医院的热心接待员，已经在那里工作了五年，能叫出所有兽医的名字”
3. **通话目的** – 通话的具体内容是什么？请包含所有相关细节：
   - 不佳示例： “关于他们宠物的后续事宜”
   - 佳例： “与 Henderson 家人联系，询问 Max（一只金毛寻回犬）的情况：Max 上周接受了膝盖手术，需要术后复查，并且每天需要服用两次 Rimadyl 药。同时提醒他们还有 325 美元的未付费用。可选择的通话时间有：周三下午 2 点或周四上午 10 点/下午 4 点。”

### 上下文信息检查清单：
- [ ] 姓名（来电者姓名、企业名称、联系人姓名）
- [ ] 日期和时间（请具体说明，例如：“1 月 15 日星期二下午 3 点”）
- [ ] 相关细节（预约类型、订单编号、服务详情）
- [ ] 如有需要，提供备用选项（重新安排时间、其他处理方式）
- [ ] 代理可能需要的任何参考编号或 ID

## 先决条件

请一次性安装 JavaScript 依赖项：
```bash
npm --prefix {baseDir} install
```

如果使用 `--ngrok`，必须配置 `NGROK_AUTH_TOKEN` 并验证 ngrok 账户。
如果不使用 `--ngrok`，请将 `PUBLIC_WS_URL` 设置为一个可访问的 `wss://.../telnyx` 端点。

## 命令

### 基本通话：
```bash
node {baseDir}/telnyx_voice_agent.js --to "+15551234567" --ngrok \
  --personality "<detailed personality>" \
  --task "<detailed task with all context>"
```

### 完整示例（多主题的复杂通话）：
```bash
node {baseDir}/telnyx_voice_agent.js \
  --to "+15551234567" \
  --ngrok \
  --personality "Emma, a warm and experienced veterinary receptionist at Pawsitive Care Animal Hospital. You've worked there for 5 years and genuinely love animals. You know all the vets by name - Dr. Chen specializes in surgery, Dr. Patel handles general wellness, and Dr. Morrison is the exotic animals expert. You're organized but personable." \
  --task "Call to follow up with the Hendersons about their pets. They have three animals at your clinic: 1) Max, a 7-year-old golden retriever who had knee surgery last week - need to schedule his two-week post-op checkup and confirm he's been taking his pain medication (Rimadyl, twice daily with food). 2) Whiskers, a 12-year-old tabby cat due for her senior blood panel and dental cleaning - Dr. Patel recommended this at her last visit in October. 3) Pickles, their bearded dragon who needs his annual wellness exam. Also remind them that Max's surgery bill of eight hundred fifty dollars has a remaining balance of three hundred twenty-five dollars after insurance. Payment plans are available if needed. If they want to schedule, available slots this week: Wednesday 2pm, Thursday 10am or 4pm, Friday 9am." \
  --greeting "Hi there! This is Emma calling from Pawsitive Care Animal Hospital. Is this the Henderson household?"
```

### 带有通话记录的回拨：

在之前的对话结束后进行回拨时，请将完整的通话记录包含在任务信息中，以保持对话的连贯性。代理会理解之前的对话内容，并从上次停下的地方继续对话。

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

以下情况适用此功能：
- 代理承诺会回电提供更多信息
- 需要对之前的对话进行跟进
- 继续进行多部分的交互

## 语音选择

除非用户另有指定，否则始终使用 ElevenLabs 提供的语音：
- `elevenlabs/rachel` – 女性声音（默认）
- `elevenlabs/adam` – 男性声音
- `elevenlabs/josh` – 男性声音（音色较深）

## 模型选择

默认模型：`gpt-4o-mini`

## 输出

通话记录将会被返回，其中包含完整的对话内容。您可以使用这些记录来：
- 确认任务是否完成
- 提取通话中收集的信息
- 向用户报告通话结果

通话结束后，系统会返回完整的通话记录给用户。

通话结束后，系统还会生成以下日志：
- 录音文件的 URL
- 录音文件会被保存到本地磁盘（默认路径为 `./recordings`）
- 成功保存后，录音文件会从 Telnyx 门户删除

## 注意事项：
- 代理绝不会自行假设未提供的信息
- 如果遇到未知问题，它会建议挂断电话并重新拨打
- ngrok 隧道会自动管理
- 环境变量需要在 OpenClaw 设置中配置
- 如果通话过程中没有音频信号，请先检查 `DEEPGRAM_API_KEY` 的有效性/权限
- 录音功能默认是开启的，并会保存在本地