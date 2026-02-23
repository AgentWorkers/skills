---
name: nori-health
description: Query your personal health data and get coaching from Nori, your AI health coach. Use when the user asks about sleep, workouts, nutrition, weight, heart rate, HRV, or wants health insights. NOT for: medical diagnosis, prescriptions, or emergency health situations.
homepage: https://nori.health
metadata: {"openclaw":{"emoji":"🌿","requires":{"env":["NORI_API_KEY"],"bins":["curl","jq"]},"primaryEnv":"NORI_API_KEY"}}
---

# Nori 健康教练

您可以将健康相关的问题发送给 Nori，Nori 会分析来自可穿戴设备（如 Apple Watch、Oura、Garmin、Whoop 等）、饮食记录、锻炼数据、体重信息以及实验室检测结果等数据。

## 设置

1. 安装 Nori 的 iOS 应用程序，并将您的可穿戴设备连接到该应用。
2. 在 Nori 应用中，进入“设置”>“集成”>“OpenClaw”。
3. 生成一个 API 密钥（以 `nori_` 开头）。
4. 设置环境变量：
   ```bash
   export NORI_API_KEY="nori_您的密钥_here"
   ```
   或将其添加到 `~/.openclaw/openclaw.json` 文件中：
   ```json
   {
     "skills": {
       "entries": {
         "nori-health": {
           "apiKey": "nori_您的密钥_here"
         }
       }
     }
   }
   ```

## 使用场景

- “我想比较锻炼日和休息日的睡眠情况。”
- “我今天应该吃什么来达到蛋白质摄入目标？”
- “请显示我这个月的静息心率趋势。”
- “昨天跑步后我的恢复情况如何？”
- “我早餐吃了两个鸡蛋和配鳄梨的吐司。”
- “我进行了 30 分钟的力量训练。”
- “您能看出我的睡眠和心率变异性（HRV）之间有什么规律吗？”

## 使用方法

通过聊天接口将用户的问题发送给 Nori。请务必原样转发用户的文字内容。

使用 `jq -n` 将用户的信息安全地转换为有效的 JSON 格式，并捕获 HTTP 状态码以处理可能的错误：

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://api.nori.health/api/v1/openclaw/chat" \
  -H "Authorization: Bearer $NORI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg msg "用户的问题_here" '{message: $msg}')")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "$BODY" | jq -r '.reply'
elif [ "$HTTP_CODE" -eq 401 ]; then
  echo "您的 Nori API 密钥无效。请在 Nori 应用的“设置”>“集成”>“OpenClaw”中重新生成密钥。”
elif [ "$HTTP_CODE" -eq 429 ]; then
  echo “请求次数过多，请稍后再试。”
else
  echo “连接到 Nori 时出现了问题（HTTP 状态码：$HTTP_CODE）。”
fi
```

## 响应处理

- 如果请求成功（状态码为 200）：直接将 `.reply` 字段以纯文本形式返回给用户。不要添加 Markdown 格式、项目符号或其他装饰内容。
- 如果状态码为 401：告知用户他们的 Nori API 密钥无效，需在 Nori 应用中重新生成密钥。
- 如果状态码为 429：告知用户稍后再试。
- 对于其他错误：告知用户连接 Nori 时出现了问题，并显示相应的 HTTP 状态码。

## 重要提示

- 请原样转发用户的消息，不要重新表述、总结或添加任何背景信息。
- 也请原样返回 Nori 的回复，不要进行格式调整或添加任何评论。
- Nori 负责所有的健康数据分析、日志记录和健康指导工作；您的任务仅仅是传递信息。
- Nori 并非医疗服务。如果用户需要医疗诊断或紧急帮助，请引导他们联系医生或紧急服务部门。