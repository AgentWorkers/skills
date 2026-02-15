---
name: phone-calls
description: 通过 Bland AI 进行人工智能驱动的电话通话——预订餐厅、预约服务、查询相关信息。AI 会代表您拨打电话，并在通话结束后提供通话记录（文字记录）。
metadata: {"clawdbot":{"emoji":"📞","requires":{"env":["BLAND_API_KEY"]}}}
---

# 电话通话功能

代表用户发起由 AI 驱动的电话通话——预订餐厅、预约服务、咨询信息等。

## 提供商：Bland AI

**选择 Bland AI 的原因：**
- 所有选项中 API 最简单（Vapi 和 Retell 的使用更为复杂）
- 只需要提供 `phone_number` 和 `task` 即可发起通话
- 响应延迟低，语音自然
- 按分钟计费，无平台费用
- 可自行托管（数据安全）

## 所需设置

### 1. 创建 Bland AI 账户
1. 访问 https://app.bland.ai
2. 使用电子邮件注册
3. 添加支付方式（或使用免费试用积分）

### 2. 获取 API 密钥
1. 访问 https://app.bland.ai/dashboard
2. 点击个人资料 → API 密钥
3. 复制 API 密钥

### 3. 配置 Clawdbot
将 API 密钥添加到您的环境变量或 `.env` 文件中：
```bash
BLAND_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

或者将其存储在 `~/.clawd/secrets.json` 文件中：
```json
{
  "bland_api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
}
```

## 使用方法

### 基本通话
```bash
./phone-call.sh "+447123456789" "Call the restaurant and book a table for 2 at 7pm tonight under the name John"
```

### 使用自定义语音
```bash
./phone-call.sh "+447123456789" "Ask about their opening hours" --voice maya
```

### 查看通话状态
```bash
./check-call.sh <call_id>
```

## 工作原理

1. 您提供电话号码和通话任务/目标
2. Bland AI 会通过 AI 代理拨打电话
3. AI 会按照您的指令自然地与对方交流
4. 通话结束后，您会收到通话记录和总结信息

## 示例任务

**预订餐厅：**
```
Call this restaurant and book a table for 4 people on Saturday at 8pm. 
The booking should be under the name "Smith". If they ask for a phone 
number, give them +447123456789.
```

**查询预约信息：**
```
Call this dental office and ask what appointments are available next 
week for a routine checkup. Get at least 3 options if possible.
```

**咨询服务详情：**
```
Call this plumber and ask if they can come out tomorrow to fix a 
leaking tap. Get a quote for the callout fee.
```

## 价格（Bland AI）

- **呼出电话：** 约 0.09 美元/分钟（美国）
- **价格因国家/地区而异** — 请访问 https://app.bland.ai 查看当前费率
- 首次通话可能享受免费试用积分

## 语音选项

内置语音：
- `josh` — 男性，专业风格
- `maya` — 女性，友好风格（默认）
- `florian` — 男性，欧洲口音
- `derek` — 男性，随意风格
- `june` — 女性，专业风格
- `nat` — 男性，自然风格
- `paige` — 女性，积极向上

## 高级功能

### 语音邮件处理
AI 可以识别语音邮件，并选择挂断、留言或忽略。

### 通话录音
将 `record: true` 设置为 `true` 可以获取通话录音的 URL。

### Webhook
通过设置 webhook URL，在通话完成后接收通知。

### 通话流程管理
对于复杂的通话流程（如 IVR 菜单、多步骤操作），可以在 Bland AI 的控制台中创建相应的流程路径。

## 限制

- 无法拨打紧急电话（如 999、911 等）
- 部分电话号码可能被屏蔽（DNC 列表）
- 每 10 秒内只能拨打同一号码一次
- 默认通话时长为 30 分钟（可配置）

## 故障排除

**“电话号码无效”**
- 请添加国家代码：英国使用 `+44`，美国使用 `+1`
- 请删除电话号码中的空格和括号

**“余额不足”**
- 请在 https://app.bland.ai/dashboard/billing 添加积分

**“超出通话限制”**
- 请等待几秒后再尝试拨打同一号码

## 相关文件

- `phone-call.sh` — 发起电话通话的脚本
- `check-call.sh` — 查看通话状态/记录的脚本
- `bland.sh` — 低级 API 封装层