---
name: openrouter-usage
description: '获取 OpenRouter 的实时使用情况统计数据和各型号的历史支出情况。当用户询问使用量、支出明细、成本结构或 OpenRouter 的相关统计数据时，可以使用此功能。该功能不适用于系统健康状况检查或其他与大型语言模型（LLM）无关的指标的查询。'
license: Apache-2.0
compatibility: Requires internet access. Primary path uses python3. Optional fallback uses curl (+ jq if available).
required-env-vars:
  - OPENROUTER_API_KEY
optional-env-vars:
  - OPENROUTER_MGMT_KEY
primary-credential: OPENROUTER_API_KEY
credential-description: OpenRouter API key
metadata:
  author: Arkology Studio
  version: "1.1"
allowed-tools: Bash(python3:*) Bash(curl:*) Bash(jq:*) Read
---

# OpenRouter 使用情况监控

## 该技能的功能
该技能用于获取 OpenRouter 的使用情况和费用数据：
- **实时总计（今日/本周/本月）**：通过 `/auth/key` 端点获取
- **按模型划分的历史数据**：通过 `/activity` 端点获取（仅限已完成的 UTC 日）

---

## 运行方法（推荐）
建议设置环境变量，或创建一个 `credentials.env` 文件：

```bash
export OPENROUTER_API_KEY=your_key_here
export OPENROUTER_MGMT_KEY=your_mgmt_key_here  # optional, enables model breakdown
```

然后执行以下命令：`python3 scripts/stats.py`

或者，您也可以在技能目录下创建 `credentials.env` 文件：

```
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MGMT_KEY=your_mgmt_key_here
```

---

## 备用方法（不使用 Python）
如果无法使用 Python，可以直接查询相关端点：

**实时总计**
```bash
curl -sS -H "Authorization: Bearer $OPENROUTER_API_KEY"
https://openrouter.ai/api/v1/auth/key
```

**按模型划分的最近 7 天活动数据**
```bash
curl -sS -H "Authorization: Bearer $OPENROUTER_MGMT_KEY"
https://openrouter.ai/api/v1/activity
```

---

## 配置要求
- **必需的配置项**：
  - `OPENROUTER_API_KEY`：用于获取实时使用情况和余额信息

**可选的配置项**：
  - `OPENROUTER_MGMT_KEY`：用于通过 `/activity` 端点获取按模型划分的支出数据

凭据可以通过以下方式提供：
1. 环境变量（出于安全考虑，推荐使用此方法）
2. 技能目录中的 `credentials.env` 文件（作为备用方案）

---

## 输出格式
💰 OpenRouter 使用情况
今日：$X.XX | 本周：$X.XX | 本月：$X.XX
余额：$X.XX / $X.XX

最近使用的模型（7 天）：
• 模型名称：$X.XX (N)
...
`*` 表示实时总计数据，可能尚未在按模型划分的统计数据中显示。

---

## 注意事项
- `/activity` 端点仅返回已完成的 UTC 日的数据。
- 今日的支出数据可能会出现在总计中，但按模型划分的数据需要等到下一个 UTC 时间点才会更新。
- 如果提供的密钥无效，将会收到 401/403 错误。
- 如果遇到请求限制（rate limiting），系统会返回 429 错误。
- 如果网络出现故障，需要重新尝试请求或查看错误信息。