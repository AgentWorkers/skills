---
name: token-efficiency-guide
version: 1.1.0
description: "将每周的限额从周二改为周日。总共需要10个步骤，每个步骤需要一个下午的时间来完成。"
metadata:
  openclaw:
    owner: kn7623hrcwt6rg73a67xw3wyx580asdw
    category: optimization
    tags:
      - tokens
      - efficiency
      - claude-max
      - cost-reduction
      - maintenance
    license: MIT
---
# 令牌使用效率指南

让您的 Claude Max 订阅服务持续整周使用。只需在一天下午完成以下 10 个步骤，就能减少 80-90% 的令牌消耗。

## 您将获得什么

以下是按影响程度排序的 10 个优化建议，大多数步骤的修改时间都在几分钟以内：

| 步骤 | 节省的令牌数量 | 所需时间 |
|------|-------------|---------|
| 1. 将心跳请求（Heartbeat）改为俳句（Haiku） | 约 25% | 1 分钟 |
| 2. 压缩会话数据（Session compaction） | 约 20% | 10 分钟 |
| 3. 将简单的定时任务（Simple crons）替换为 bash 脚本 | 约 15% | 1-2 小时 |
| 4. 将 Cron 任务（Cron jobs）优化为更高效的 Sonnet 脚本 | 约 10% | 5 分钟 |
| 5. 分离大型输出文件（Isolate large outputs） | 约 10% | 10 分钟 |
| 6. 降低 Cron 任务的执行频率 | 约 8% | 5 分钟 |
| 7. 清理工作区文件（Workspace file cleanup） | 约 7% | 30 分钟 |
| 8. 启用缓存功能（Enable cache retention） | 约 3% | 1 分钟 |
| 9. 协调多个代理的使用（Coordinate multi-agent usage） | 约 2% | 需要团队协作 |
| 10. 自动化维护任务（Automated maintenance crons） | 约 5% | 1-2 小时 |

仅执行步骤 1 就可以让您的订阅服务多使用一天；步骤 1-3 的优化效果合计可达 60%。

## 适用人群

- 使用 Claude Max 的 OpenClaw 用户，尤其是那些经常遇到“令牌已用尽”的情况的人  
- 在多个代理上共享同一订阅服务的团队  
- 希望将令牌用于工作而非重复发送心跳请求的用户  

## 包含内容

- 详细的操作步骤及配置示例  
- 可直接使用的维护脚本  
- 根据任务类型推荐的模型路由方案  

*您可以克隆、修改或根据自身需求进行调整。*  

👉 探索完整项目：[github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)