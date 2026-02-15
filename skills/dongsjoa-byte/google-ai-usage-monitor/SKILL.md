---
name: google-ai-usage-monitor
version: 1.0.0
description: 监控 Google AI Studio（Gemini API）的使用情况、速率限制以及配额消耗情况，并通过自动化警报进行提醒。
author: xiaoyaner
---

# Google AI 使用监控技能

监控 Google AI Studio 的使用情况，以防止配额耗尽并优化 API 的使用。

## 支持的指标

| 指标 | 描述 | 警报阈值 |
|--------|-------------|-----------------|
| RPM | 每分钟请求数（峰值） | 超过限制的 80% |
| TPM | 每分钟令牌数（峰值） | 超过限制的 80% |
| RPD | 每天请求数 | 超过限制的 80% |

## 不同等级的速率限制

| 等级 | 典型限制 |
|------|---------------|
| 免费 | 2 RPM, 32K TPM, 50 RPD |
| 按使用量付费 | 10-15 RPM, 100K+ TPM, 500+ RPD |
| 支付等级 1 | 20 RPM, 100K TPM, 250 RPD（因模型而异） |

注意：实际限制因模型而异，可在使用情况仪表板上查看。

## 使用情况仪表板

### URL
```
https://aistudio.google.com/usage?project={PROJECT_ID}&timeRange=last-28-days&tab=rate-limit
```

### 需要提取的关键信息
- **项目名称**：对应的 GCP 项目
- **等级**：免费 / 按使用量付费 / 支付等级 X
- **模型表格**：每行包含模型名称、类别、RPM、TPM、RPD
- **时间范围**：默认为 28 天

## 浏览器自动化

### 打开使用情况页面
```javascript
// Using OpenClaw browser tool
browser action=open targetUrl="https://aistudio.google.com/usage?project=YOUR_PROJECT_ID&timeRange=last-28-days&tab=rate-limit" profile=openclaw
```

### 等待数据加载
页面会异步加载数据。请等待以下情况：
1. 项目下拉菜单显示项目名称（而不是“Loading...”）
2. 速率限制表格中有数据行

### 解析表格数据
查找符合以下模式的表格行：
```
Model Name | Category | X / Y | X / Y | X / Y | View in charts
```

其中 `X / Y` 分别代表“已使用量”和“限制量”。

## 报告格式

### Discord 消息模板
```markdown
## 📊 Google AI Studio 用量报告

**项目**: {project_name}
**付费等级**: {tier}
**统计周期**: 过去 28 天

---

### {Model Name}
| 指标 | 用量 | 限额 | 使用率 |
|------|------|------|--------|
| RPM | {rpm_used} | {rpm_limit} | {rpm_pct}% |
| TPM | {tpm_used} | {tpm_limit} | {tpm_pct}% |
| RPD | {rpd_used} | {rpd_limit} | {rpd_pct}% |

---

{status_emoji} **状态**: {status_text}

*检查时间: {timestamp}*
```

## 状态等级

| 使用量百分比 | 状态 | 表情符号 | 措施 |
|---------|--------|-------|--------|
| < 50% | 正常 | ✅ | 继续正常使用 |
| 50-80% | 需要关注 | ⚠️ | 加密监控使用情况 |
| > 80% | 风险预警 | 🚨 | 向用户发送警报，并考虑实施速率限制 |

## 警报规则

### 何时向用户发送警报
1. **任何指标超过 80%**：立即通过 @mention 发送警报
2. **任何指标超过 50%**：在报告中包含警告信息
3. **API 错误（429）**：记录速率限制的触发情况

### 警报消息模板
```markdown
🚨 **Google AI 配额预警**

<@USER_ID> 以下指标接近限额：

- **{model}** {metric}: {used}/{limit} ({pct}%)

建议：
- 减少 API 调用频率
- 考虑升级付费等级
- 检查是否有异常调用
```

## Cron 作业设置

### 建议每天检查一次
```json
{
  "name": "Google AI 用量检查",
  "schedule": {
    "kind": "cron",
    "expr": "0 20 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "检查 Google AI Studio 用量并发送报告到指定 Discord 频道"
  },
  "delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "CHANNEL_ID"
  }
}
```

## 与 OpenClaw 的集成

### 配置
将相关配置添加到 `TOOLS.md` 文件中：
```markdown
## Google AI Studio

- **Project ID**: gen-lang-client-XXXXXXXXXX
- **Dashboard**: https://aistudio.google.com/usage
- **Discord Channel**: #google-ai (CHANNEL_ID)
- **Check Schedule**: Daily 20:00
```

### 与 Heartbeat 的集成
将相关配置添加到 `HEARTBEAT.md` 文件中：
```markdown
## Google AI Monitoring
- Check usage if last check > 24 hours
- Alert if any metric > 80%
```

## 故障排除

### 页面无法加载
1. 确认是否使用正确的 Google 账户登录
2. 验证项目 ID 是否正确
3. 等待更长时间（5-10 秒）以完成异步数据加载

### 数据显示“Loading...”状态
项目下拉菜单可能需要一些时间才能显示完整内容。请稍后重新尝试。

### 指标未更新
Google 提示：“使用数据可能需要最多 15 分钟才能更新。”

## 参考资料
- [Google AI Studio 使用情况仪表板](https://aistudio.google.com/usage)
- [Gemini API 速率限制](https://ai.google.dev/gemini-api/docs/rate-limits)
- [计费文档](https://ai.google.dev/gemini-api/docs/billing)
- [Gemini 的云监控功能](https://firebase.google.com/docs/ai-logic/monitoring)