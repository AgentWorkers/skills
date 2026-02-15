---
name: Follow
description: 通过智能过滤、分层警报以及可搜索的存档功能，监控来自不同平台的人、主题和来源的内容。
---

## 工作区

```
~/follow/
├── sources/           # One file per followed entity
│   ├── people/        # @naval.md, @dhh.md
│   ├── topics/        # ai-safety.md, rust.md
│   └── feeds/         # techcrunch.md, hn-frontpage.md
├── archive/           # Captured content by date
│   └── YYYY-MM/
├── alerts.md          # Alert configuration
└── index.md           # Quick status: what's being followed
```

---

## 快速参考

| 任务 | 所需文件 |
|------|------|
| 添加/配置信息源 | `sources.md` |
| 设置过滤规则 | `filtering.md` |
| 配置警报等级 | `alerts.md` |
| 查询存档内容 | `querying.md` |
| 平台特定设置 | `platforms.md` |

---

## 核心流程

1. **添加信息源**：用户名称 → 人名/主题/信息源 → 创建跟踪文件
2. **监控**：按计划（通过 cron 任务）或按需检查信息源
3. **过滤**：应用相关性规则，排除无关内容
4. **存储**：仅存储重要的内容（摘要，而非完整数据）
5. **警报**：根据警报等级（立即/每日/每周/被动）发送通知
6. **查询**：从存档中检索“X 对 Y 说了什么？”

---

## 常见操作模式

| 用户操作 | 代理执行 |
|-----------|------------|
| “关注 @naval 的 Twitter 账号” | 创建 `sources/people/naval.md` 文件，并配置 Twitter 监控 |
| “跟踪关于 AI 安全的讨论” | 创建跨多个信息源的关键词跟踪器 |
| “竞争对手 X 本周发布了什么？” | 查询存档并生成摘要 |
| “当 Y 发生时立即通知我” | 将该事件添加到 `alerts.md` 的高优先级警报中 |
| “每周提供一次汇总” | 在警报设置中配置每周摘要 |
| “停止关注 X” | 将该用户的信息源存档并标记为“不活跃” |

---

## 数据捕获原则

- **使用摘要而非完整内容** — 节省空间，确保合规性
- **始终添加链接和时间戳** — 便于日后检索
- **提供内容的重要性背景** — 不仅仅是“X 发布了什么”
- **跨信息源去重** — 来自多个来源的相同内容只记录一次