---
name: "Skill Finder"
slug: skill-finder
version: "1.1.0"
homepage: https://clawic.com/skills/skill-finder
description: "根据需求，通过高质量过滤和偏好学习功能来查找、评估并推荐适合使用的 ClawHub 技能。"
changelog: "Added categories table, troubleshooting guide, better discovery workflows, setup system"
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["npx"]},"os":["linux","darwin","win32"]}}
---
## 设置（Setup）

如果 `~/skill-finder/` 不存在或为空，请静默读取 `setup.md` 文件，然后按照文件中的指示进行设置。

## 使用场景（When to Use）

当用户需要查找某项技能、了解某项技能的功能，或者对某事物的存在感到疑惑时，可以使用该系统。该系统负责处理搜索、评估技能质量、比较不同选项以及了解用户的需求。

## 架构（Architecture）

技能相关的所有数据都存储在 `~/skill-finder/` 目录下。具体结构请参考 `memory-template.md` 文件。

```
~/skill-finder/
├── memory.md     # Preferences + liked/passed skills
└── searches.md   # Recent search history (optional)
```

## 快速参考（Quick Reference）

| 主题 | 文件名          |
|-------|-----------------|
| 设置       | `setup.md`         |
| 存储模板     | `memory-template.md`     |
| 搜索策略     | `search.md`         |
| 评估标准     | `evaluate.md`         |
| 技能分类     | `categories.md`        |
| 故障排除     | `troubleshooting.md`     |

## 核心规则（Core Rules）

### 1. 根据需求搜索，而非名称
当用户请求帮助时（例如：“需要处理 PDF 文件”），应先思考他们的实际需求：
- 编辑 PDF 文件？ → 使用 `clawhub search "pdf edit"`
- 创建 PDF 文件？ → 使用 `clawhub search "pdf generate"`
- 提取 PDF 文件内容？ → 使用 `clawhub search "pdf parse"`

### 2. 推荐前先进行评估
切勿盲目推荐技能。请根据 `evaluate.md` 中列出的标准进行评估：
- 描述的清晰度
- 下载次数（下载次数越多，说明该技能越受欢迎/维护得越好）
- 最后更新时间（最近更新的技能通常更活跃）
- 开发者的声誉

### 3. 附带理由推荐
不要只是简单地列出技能，要解释为什么每个技能适合用户：
> “找到了 `pdf-editor` 这个技能——它可以处理表格填写和注释功能，已有 2300 次下载，上周进行了更新，符合您编辑合同的需求。”

### 4. 了解用户的偏好
当用户明确表达自己的偏好时，更新 `~/skill-finder/memory.md` 文件：
- “我更喜欢简洁的技能” → 将该偏好添加到用户设置中
- “这个技能很棒” → 说明原因后将其添加到用户喜欢的技能列表中
- “这个技能太复杂了” → 说明原因后将其添加到用户不喜欢的技能列表中

### 5. 先查看技能信息
在推荐技能之前，请先阅读 `memory.md` 文件：
- 跳过与用户不喜欢的技能相似的技能
- 优先考虑用户喜欢的技能所具备的特性
- 优先考虑用户的偏好设置

## 搜索命令（Search Commands）

```bash
# Primary search
npx clawhub search "query"

# Install (with user consent)
clawhub install <slug>

# Get skill details
clawhub inspect <slug>

# See what's installed
clawhub list
```

## 工作流程（Workflow）

1. **理解用户需求**：用户真正需要什么？
2. **进行搜索**：先尝试使用具体的关键词搜索，必要时再扩大搜索范围
3. **评估技能质量**：根据 `evaluate.md` 中的标准对搜索结果进行评估
4. **进行比较**：如果找到多个匹配项，根据适用性和质量对结果进行排序
5. **推荐最佳选项**：推荐排名前 1-3 的技能，并附上明确的推荐理由
6. **记录用户反馈**：将用户的反馈保存到 `memory.md` 文件中

## 常见问题（Common Traps）

- 使用过于泛泛的搜索词会导致结果混乱。请使用具体的关键词（例如：使用 “react testing” 而不是 “testing”）
- 仅根据技能名称进行推荐可能会错过名称不同但功能更好的选项
- 忽略技能的下载次数：下载次数少的技能可能意味着该技能已被弃用
- 不检查技能的更新时间：使用过时的技能可能会导致问题

## 安全性与隐私（Security & Privacy）

**会离开用户设备的数据：**
- 用户的搜索查询会被发送到 ClawHub 注册表（公开搜索）

**保留在用户设备上的数据：**
- 所有的用户偏好设置（存储在 `~/skill-finder/memory.md` 中）
- 搜索历史记录（如果启用了该功能）

**本系统不会：**
- 未经用户同意就安装技能
- 隐秘地跟踪用户行为
- 访问 `~/skill-finder/` 目录之外的文件

## 相关技能（Related Skills）

如果用户同意，可以使用以下命令安装相关技能：
- `clawhub install <slug>`：安装技能
- `skill-manager`：管理已安装的技能，并提示是否需要更新
- `skill-builder`：从头开始创建新的技能
- `skill-update`：更新现有的技能

## 用户反馈（Feedback）

- 如果觉得本系统有用，请使用 `clawhub star skill-finder` 给予评分
- 为了保持系统更新，请使用 `clawhub sync` 命令同步数据