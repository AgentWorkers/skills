# Analytix402

实时监控、控制并优化您的人工智能代理的API使用情况以及大语言模型（LLM）相关费用。

## 产品描述

Analytix402为您的OpenClaw代理提供了财务透明度和费用管理功能。它可以追踪代理发起的所有API调用、LLM请求以及相关的费用支出。您可以通过该工具设置预算限制，检测重复购买行为，并在费用失控前收到警报。

**主要功能：**
- 自动追踪所有出站API调用和费用支出
- 监控OpenAI、Anthropic等提供商的LLM令牌使用情况及其费用
- 强制执行每日预算限制和单次调用费用上限
- 检测重复的API购买行为，防止资源浪费
- 发送“心跳信号”以确保代理正常运行
- 提供实时监控界面（网址：analytix402.com）

## 配置

```yaml
# Required
ANALYTIX402_API_KEY: ax_live_your_key_here

# Optional
ANALYTIX402_AGENT_ID: my-openclaw-agent
ANALYTIX402_BASE_URL: https://analytix402.com
ANALYTIX402_DAILY_BUDGET: 50.00
ANALYTIX402_PER_CALL_LIMIT: 5.00
ANALYTIX402_TRACK_LLM: true
```

## 工具

### analytix402_spend_report
获取代理的费用汇总信息：总费用、按API和LLM提供商划分的详细费用情况以及效率评分。

### analytix402_set_budget
为当前代理会话设置或更新每日预算限制。

### analytix402_check_budget
在进行高成本的API调用前检查剩余预算。

### analytix402_flag_purchase
标记可能存在的重复或不必要的购买行为以供审核。

## 关键标签
监控、分析、预算、费用管理、可观测性、成本追踪