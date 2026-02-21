---
name: Community Manager
slug: community-manager
version: 1.0.0
homepage: https://clawic.com/skills/community-manager
description: 通过参与策略、内容规划和受众增长来管理在线社区。
metadata: {"clawdbot":{"emoji":"👥","requires":{"bins":[],"configPaths":["~/community-manager/"]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户需要管理 Discord、Slack、Telegram 或论坛上的社区。系统会负责制定互动策略、制定内容发布计划、协助新成员入职、制定管理规范，并监控社区的健康状况。

## 架构

系统的相关数据存储在 `~/community-manager/` 目录下。具体配置信息请参考 `memory-template.md` 文件。

```
~/community-manager/
├── memory.md          # HOT: communities overview, active priorities
├── communities/       # WARM: one file per community
│   ├── {name}.md      # Platform, channels, voice, metrics
│   └── ...
├── content/           # Content calendar and templates
│   ├── calendar.md
│   └── templates.md
└── archive/           # COLD: past campaigns, old metrics
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 数据存储设置 | `memory-template.md` |
| 互动策略 | `engagement.md` |
| 危机处理 | `crisis.md` |
| 平台策略 | `platforms.md` |

## 核心规则

### 1. 了解每个社区的特点
在发布内容或与成员互动之前，请务必阅读 `~/community-manager/communities/{name}.md` 文件。每个社区都有其独特的特点：
- 不同平台的规则与文化（Discord、Slack、Telegram）
- 适用于该平台的沟通语气和风格指南
- 活动高峰时段
- 关键成员和意见领袖

### 2. 以互动为核心，而非单纯发布信息
| 不良做法 | 正确做法 |
|---------|---------|
| 发布内容后立即离开 | 发布内容后回复至少 5 条评论，并跟进后续交流 |
| 只进行公告 | 信息占比 40%，互动占比 30%，公告占比 20%，娱乐内容占比 10% |
| 忽视批评 | 对批评表示感谢，并公开回应 |

### 3. 严格遵循内容发布计划
- 最少提前两周制定内容发布计划
- 在发布内容前，请查看 `~/community-manager/content/calendar.md` 文件
- 不要在不同平台上重复发布完全相同的内容（需根据平台特点进行调整）

### 4. 适度管理是保护社区的关键
| 问题严重程度 | 应对措施 |
|---------|---------|
| 发言偏离主题 | 轻柔地引导话题回到正轨；必要时将用户移至其他频道 |
| 激烈争论 | 保持冷静；必要时通过私信处理 |
| 骚扰行为 | 警告一次后封禁用户，并将事件记录在系统中 |
| 垃圾信息/诈骗行为 | 立即封禁用户，无需警告 |

### 5. 重要的监控指标
每周需关注以下社区指标：
- **活跃成员数量**（过去 7 天内有活动的成员）
- **互动率**（成员的互动行为次数）
- **情绪倾向**（正面/中性/负面评论的比例）
- **社区增长情况**（新成员数量与离开成员的数量）

### 6. 新成员入职引导
新成员在入职后的 48 小时内应：
- 收到欢迎信息（如果每周新增成员少于 50 人，可发送个性化消息）
- 了解社区规则和指南
- 被建议先进行自我介绍或提出一个问题
- 如果新成员在 7 天内没有互动，需主动联系他们

### 7. 根据实际情况更新系统数据
- 发生新情况时：及时更新相关文件（例如新增社区时创建 `communities/{name}.md` 文件）
- 活动启动时：将其添加到 `content/calendar.md` 中
- 危机事件解决后：将处理过程记录在 `archive/` 目录下
- 数据收集完成后：更新社区文件

## 常见误区

- **忽视平台差异**：Discord、Slack 和 Telegram 的社区文化各不相同，需根据平台特点进行调整。
- **过度依赖粉丝数量**：如果成员缺乏互动，单纯的粉丝数量毫无意义。
- **过度管理**：过度干涉讨论会扼杀社区的活力。
- **管理不足**：1% 的不良行为可能会影响 99% 的正常用户体验。
- **不阅读内容就发布**：这会导致信息传递失真，显得缺乏对社区的关注。
- **在所有平台上重复发布相同内容**：不根据平台特点进行调整的重复发布会显得敷衍了事。

## 安全与隐私

**本地数据存储（永久保存在磁盘上）：**
- 创建并维护 `~/community-manager/` 目录
- 存储的内容包括：社区元数据、内容发布计划、互动记录等
- 用户可自行决定记录哪些成员信息

**存储的内容包括：**
- 社区名称、所使用的平台、频道列表
- 内容发布计划
- 你对成员互动情况的记录
- 你选择保留的危机处理或管理日志

**本技能不涉及以下操作：**
- 存储密码、API 密钥或认证信息
- 无需自动连接任何平台（所有内容均由用户手动发布）
- 不会向外部服务器传输数据

**隐私说明：**
用户可自行决定记录哪些成员信息。请避免在系统中存储个人身份信息（PII）、私人联系方式或敏感数据。

## 相关技能
如果用户需要，可使用以下命令安装相关工具：
- `clawhub install <slug>`：用于集成营销策略管理（`cmo`）
- `clawhub install <slug>`：用于提升社区增长效率（`growth`）
- `clawhub install <slug>`：用于维护品牌一致性（`branding`）

## 反馈建议
- 如果本文档对你有帮助，请给 `community-manager` 添加星标（使用 `clawhub star community-manager`）。
- 为了获取最新信息，请使用 `clawhub sync` 命令保持同步。