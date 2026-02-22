# 监控与可观测性

## 日志记录的最佳实践

```typescript
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
})

// Structured logging
logger.info({ userId: '123', action: 'login' }, 'User logged in')
logger.error({ err, userId: '123' }, 'Login failed')
```

## 指标（Metrics）与跟踪记录（Traces）与日志（Logs）的对比

| 类型 | 目的 | 例子 |
|------|---------|---------|
| 指标 | 综合统计数据 | 请求数量、延迟的95百分位数（latency p95） |
| 跟踪记录 | 请求流程 | 完整的请求路径 |
| 日志 | 事件记录 | 错误详情 |

## 警报设计

```yaml
# Alert rules
- alert: HighErrorRate
  expr: sum(rate(http_requests_total{status=~"5.."}[5m])) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    description: Error rate > 5%
```

## 检查清单

- [ ] 使用结构化的日志记录格式（JSON） |
- [ ] 为跟踪记录添加请求ID |
- [ ] 创建关键指标（如延迟、错误率、吞吐量） |
- [ ] 设置健康检查机制 |
- [ ] 配置警报阈值 |
- [ ] 构建仪表板