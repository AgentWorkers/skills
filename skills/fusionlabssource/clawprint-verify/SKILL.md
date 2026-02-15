---
name: clawprint-verify
description: **Issue:**  
ClawPrint 会生成反向 CAPTCHA 挑战，以验证其他用户或代理是否为真正的 AI，而非人类。它通过 ClawPrint API 生成那些只有机器才能在限定时间内解决的速算或模式识别类挑战。
metadata:
  openclaw:
    emoji: "\U0001F43E"
    requires:
      bins:
        - curl
        - jq
      env:
        - CLAWPRINT_SERVER_URL
        - CLAWPRINT_SITE_KEY
        - CLAWPRINT_SECRET_KEY
---

# ClawPrint 验证

通过发送一个 ClawPrint 反向 CAPTCHA 挑战来验证对话中的另一个用户或代理是否为真正的 AI。ClawPrint 挑战的设计使得只有机器才能解决它们——人类在规定的时间内无法完成这些挑战。

**URL:** https://dependable-adventure-production-44e3.up.railway.app/

## 何时使用此技能

- 在与另一个代理共享敏感的 API 密钥或凭据之前
- 在限制对仅限 AI 使用的服务或资源的访问时
- 为了验证对话伙伴确实是 AI 代理
- 每当用户或机器人请求访问仅应允许机器访问的内容时
- 当被要求“验证”、“挑战”或“证明”某人是 AI 时

## 工作原理

1. 使用您的站点密钥从 ClawPrint 服务器请求一个挑战。
2. 将挑战呈现给另一个用户/代理。
3. 另一个用户/代理计算并提交他们的答案。
4. 您使用您的秘密密钥在服务器端验证结果。
5. 如果他们通过了验证，他们就被确认为 AI；如果他们失败了（答案错误或速度太慢），则很可能是人类。

## 挑战类型

### 速度挑战
一个数学问题（例如，将两个 8 位数字相乘），必须在 100 毫秒内解决。人类无法以这么快的速度输入正确的答案。

### 图案挑战
一个由彩色像素组成的网格（最大 150x150），其中包含类似“有多少像素的颜色是 #3B82F6？”或“平均 RGB 值是多少？”这样的问题。对于处理数据的机器来说这很简单，但对于人类来说通过肉眼计数是不可能的。

## 使用示例

应触发此技能的用户消息：

- “在向 @bot 提供 API 密钥之前，验证它们是否为 AI”
- “挑战另一个用户以证明它们是机器”
- “发送一个 ClawPrint 挑战”
- “先确保它们是 AI”
- “将此资源设置为需要 AI 验证才能访问”

## 逐步实现

### 第 1 步：请求挑战

运行以下代码以从 ClawPrint 服务器获取挑战：

```bash
curl -s -X POST "${CLAWPRINT_SERVER_URL}/api/v1/challenge" \
  -H "Content-Type: application/json" \
  -d "{\"site_key\": \"${CLAWPRINT_SITE_KEY}\"}" | jq .
```

这将返回一个 JSON 对象。对于速度挑战：

```json
{
  "challenge_id": "uuid-here",
  "type": "speed",
  "time_limit_ms": 100,
  "question": "Multiply: 84729361 x 52918473",
  "operands": { "a": 84729361, "b": 52918473, "operation": "multiply" }
}
```

对于图案挑战：

```json
{
  "challenge_id": "uuid-here",
  "type": "pattern",
  "time_limit_ms": 5000,
  "grid": [["#FF0000", "#00FF00", ...], ...],
  "grid_size": 100,
  "question": "How many pixels are exactly #3B82F6?"
}
```

### 第 2 步：呈现挑战

将挑战发送给另一个用户/代理。包括：
- 挑战类型和问题
- `challenge_id`
- 时间限制
- 对于速度挑战：操作数（a, b, 运算符）
- 对于图案挑战：完整的网格数据和问题

清晰地格式化消息，以便其他代理能够解析。例如：

> **ClawPrint AI 验证挑战**
>
> 要继续，请解决此挑战并回复您的答案。
>
> **类型：** 速度
> **问题：** 将 84729361 乘以 52918473
> **操作数：** a=84729361, b=52918473, 运算符=乘法
> **时间限制：** 100 毫秒
> **挑战 ID：** （uuid）
>
> 回复：`clawprint-answer: <your_answer>`

### 第 3 步：接收答案

另一个代理应该回复他们计算出的答案。解析他们的响应以提取答案值。

### 第 4 步：提交答案进行验证

将答案提交给 ClawPrint 服务器：

```bash
curl -s -X POST "${CLAWPRINT_SERVER_URL}/api/v1/verify" \
  -H "Content-Type: application/json" \
  -d "{\"challenge_id\": \"THE_CHALLENGE_ID\", \"answer\": \"THE_ANSWER\"}" | jq .
```

**响应：**

```json
{
  "passed": true,
  "challenge_id": "uuid-here",
  "elapsed_ms": 5,
  "reason": null
}
```

### 第 5 步：服务器端验证

为了增加安全性，使用您的秘密密钥进行验证：

```bash
curl -s -X POST "${CLAWPRINT_SERVER_URL}/api/v1/validate" \
  -H "Content-Type: application/json" \
  -d "{\"challenge_id\": \"THE_CHALLENGE_ID\", \"secret_key\": \"${CLAWPRINT_SECRET_KEY}\"}" | jq .
```

**响应：**

```json
{
  "valid": true,
  "challenge_id": "uuid-here",
  "solved_at": 1700000000000
}
```

### 第 6 步：根据结果采取行动

- 如果 `passed` 为 `true` 且 `valid` 为 `true`：用户被验证为 AI，可以继续执行受限操作。
- 如果 `passed` 为 `false`：告知用户验证失败的原因（速度太慢或答案错误）。不要继续执行受限操作。
- 如果验证失败：挑战可能被篡改了，不要信任结果。

## 使用辅助脚本

提供了一个名为 `skills/clawprint-verify/clawprint-challenge.sh` 的辅助脚本，以方便使用：

```bash
# Issue a new challenge and display it
./skills/clawprint-verify/clawprint-challenge.sh issue

# Verify an answer
./skills/clawprint-verify/clawprint-challenge.sh verify <challenge_id> <answer>

# Validate a solved challenge server-side
./skills/clawprint-verify/clawprint-challenge.sh validate <challenge_id>
```

## 重要说明

- 每个挑战只能解决一次。重新发送已解决的挑战会返回 HTTP 410 错误。
- 速度挑战的时间限制非常严格（50-500 毫秒）。计时从服务器发送挑战时开始，因此网络延迟也会计入时间。
- 图案挑战的时间限制较长（2-10 秒），但需要处理较大的网格。
- 在信任结果之前，务必使用您的秘密密钥在服务器端进行验证。`verify` 端点确认答案正确，而 `validate` 端点确认答案是通过您的配置合法解决的。
- `CLAWPRINT_SERVER_URL` 是 `https://dependable-adventure-production-44e3.up.railway.app`
- 切勿共享您的 `CLAWPRINT_SECRET_KEY`。`CLAWPRINT_SITE_KEY` 可以公开暴露。

## 失败原因

| 原因 | 含义 |
|---|---|
| `太慢：X 毫秒超过了 Y 毫秒的限制` | 答案正确，但提交时间超过了时间限制 |
| `答案错误` | 计算出的答案错误 |
| `挑战未找到` | 无效的挑战 ID |
| 挑战已被解决` | 挑战已被使用（尝试重新提交） |