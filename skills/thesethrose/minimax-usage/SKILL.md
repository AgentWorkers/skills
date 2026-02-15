---
name: minimax-usage
description: 监控 Minimax Coding Plan 的使用情况，确保其使用量在 API 的限制范围内。该工具会获取当前的使用统计数据，并在超出限制时发出状态警报。
metadata: {"clawdbot":{"emoji":"📊"}}
---

# Minimax 使用技巧

监控 Minimax 编码计划的使用情况，以确保使用量在规定的范围内。

## 设置

在脚本所在的目录中创建一个 `.env` 文件：

```bash
MINIMAX_CODING_API_KEY=your_api_key_here
MINIMAX_GROUP_ID=your_group_id_here
```

从以下链接获取您的 GroupId：https://platform.minimax.io/user-center/basic-information（在“基本信息”部分）

## 使用方法

```bash
./minimax-usage.sh
```

## 输出示例

```
🔍 Checking Minimax Coding Plan usage...
✅ Usage retrieved successfully:

📊 Coding Plan Status (MiniMax-M2):
   Used:      255 / 1500 prompts (17%)
   Remaining: 1245 prompts
   Resets in: 3h 17m

💚 GREEN: 17% used. Plenty of buffer.
```

## API 详情

**端点：**
```
GET https://platform.minimax.io/v1/api/openplatform/coding_plan/remains?GroupId={GROUP_ID}
```

**必需的请求头：**
```
accept: application/json, text/plain, */*
authorization: Bearer {MINIMAX_CODING_API_KEY}
referer: https://platform.minimax.io/user-center/payment/coding-plan
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
```

## 使用限制

| 指标 | 值 |
|--------|-------|
| 重置窗口 | 5 小时（动态调整） |
| 最大使用量 | 60% |
| 每条提示信息大约对应 | 15 次模型调用 |

## 注意事项

- 编码计划 API 密钥是专为此计划设计的（不能与标准 API 密钥互换） |
- 5 小时之前的使用量会自动从统计中清除。