---
name: incident-response-plan
description: 为AI代理的部署和SaaS运营生成一份定制的 incident response plan（事件响应计划）。该计划涵盖了检测、分类、控制、恢复以及事后分析等环节。适用于将代理部署到生产环境、准备SOC2审计或提升运营韧性时使用。由AfrexAI开发。
metadata:
  version: 1.0.0
  author: AfrexAI
  tags: [incident-response, security, operations, devops, enterprise]
---
# 事件响应计划生成器

本工具可为您生成一份适用于生产环境的事件响应计划，专门针对您的 AI 代理部署场景进行定制。

## 使用场景
- 首次将 AI 代理部署到生产环境时
- 准备 SOC2 或 ISO 27001 审计时
- 客户询问“出现问题时该怎么办？”
- 为托管的 AI 服务制定操作手册时
- 事件发生后的预防措施（防止类似问题再次发生）

## 输入数据
```
Service: [Name of AI agent/service]
Environment: [cloud provider, region, architecture]
Data Sensitivity: [low/medium/high/critical]
Team Size: [number of responders]
SLA: [uptime target, e.g., 99.9%]
Integrations: [list of connected systems]
```

## 计划结构

### 1. 事件严重程度分类
| 严重程度 | 描述 | 响应时间 | 例子 |
|---------|--------|---------|-------|
| SEV1（严重） | 服务中断、数据泄露、财务损失 | 15 分钟 | 代理向客户发送错误数据、API 密钥被泄露 |
| SEV2（较高） | 服务性能下降、部分功能中断 | 1 小时 | 代理响应缓慢、某个集成组件出现故障 |
| SEV3（中等） | 非关键问题，有解决方法 | 4 小时 | 精确度略有下降、出现外观性错误 |
| SEV4（较低） | 需进行优化，但没有立即影响 | 下一个工作日 | 功能请求、性能优化 |

### 2. 检测与警报机制
- 健康检查（每 60 秒执行一次）
- 错误率阈值（>1% = SEV3，>5% = SEV2，>25% = SEV1）
- 响应时间监控（p99 值超过基线值的 2 倍时触发警报）
- 成本异常检测（每日平均值超过 150%）
- 输出质量抽样（随机检查代理的响应结果）
- 运行时间监控（使用 UptimeRobot、Pingdom 或自定义工具）

### 3. 事件分类与处理流程
```markdown
□ Confirm the alert is real (not false positive)
□ Classify severity (SEV1-4)
□ Identify affected scope (which agents, which clients)
□ Check recent changes (deploys, config changes, upstream)
□ Assign incident commander
□ Open incident channel/thread
□ Notify affected stakeholders per SLA
```

### 4. 根据事件类型采取的应对措施

**代理异常行为：**
- 暂停代理的运行（紧急停止机制）
- 恢复到上次正常运行的配置
- 启用人工干预模式
- 将相关消息放入队列以供人工审核

**基础设施故障：**
- 切换到备用区域/实例
- 如果容量不足，进行横向扩展
- 检查上游依赖服务（如 API 提供商、数据库）
- 启用故障保护机制（circuit breakers）

**安全事件：**
- 立即更换所有凭据
- 隔离受影响的系统
- 保留日志和证据
- 如果发生数据泄露，立即联系安全团队或法律部门

**数据质量问题：**
- 停止自动化输出
- 确定数据污染的时间范围
- 及时通知受影响的客户
- 准备数据修复方案

### 5. 通信模板

**客户通知（SEV1/2）：**
```
Subject: [Service Name] — Incident Update

We've identified an issue affecting [description].
- Impact: [what's affected]
- Status: [investigating/identified/monitoring/resolved]
- ETA: [estimated resolution time]
- Workaround: [if available]

We'll provide updates every [30 min / 1 hour].
```

**内部升级流程：**
```
🚨 SEV[X] — [Service]: [Brief description]
Impact: [scope]
Started: [time]
Commander: [name]
Channel: [link]
Action needed: [specific ask]
```

### 6. 恢复与验证
```markdown
□ Root cause identified and documented
□ Fix deployed and verified
□ All affected data corrected/reconciled
□ Client communication sent (resolution)
□ Monitoring confirms stable for 30+ min
□ Incident timeline documented
```

### 7. 事件事后分析模板
```markdown
# Incident Post-Mortem: [Title]
**Date:** YYYY-MM-DD
**Severity:** SEV[X]
**Duration:** [start] — [end] ([total time])
**Commander:** [name]

## Summary
[2-3 sentence description]

## Timeline
- HH:MM — [event]
- HH:MM — [event]

## Root Cause
[Technical root cause]

## Impact
- Users affected: [number]
- Duration: [time]
- Data impact: [description]
- Financial impact: [if applicable]

## What Went Well
- [item]

## What Went Wrong
- [item]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [item] | [name] | [date] | Open |

## Lessons Learned
- [lesson]
```

## 最佳实践
- 每季度测试一次事件响应计划（通过桌面演练）
- 将操作手册与相关代码放在同一位置
- 实现自动化检测机制——人工发现问题的速度较慢
- 在事件发生期间保持充分沟通——沉默只会加剧恐慌
- 在事后分析中避免指责个人，重点关注系统问题
- 将平均恢复时间（MTTR）作为核心评估指标

---

*如果您希望从第一天起就为 AI 运维流程集成事件响应机制，AfrexAI 可为您提供具备监控、警报和响应计划功能的生产级 AI 代理服务。欢迎预约咨询：[calendly.com/cbeckford-afrexai/30min](https://calendly.com/cbeckford-afrexai/30min)*