---
name: "Skill Finder - Search Skills"
slug: skill-finder
version: "1.1.2"
homepage: https://clawic.com/skills/skill-finder
description: "根据需求，通过高质量过滤和偏好学习功能来查找、评估并推荐适合使用的 ClawHub 技能。"
changelog: "Updated the title to make the skill purpose clearer."
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["npx"]},"os":["linux","darwin","win32"]}}
---
## 设置（Setup）

如果 `~/skill-finder/` 不存在或为空，请告知用户您正在初始化本地存储文件，然后按照 `setup.md` 的说明进行操作。

## 使用场景（When to Use）

当用户需要查找某项技能、了解其功能，或对某事物的存在产生疑问时，该功能可帮助用户进行搜索、评估技能质量、比较不同选项，并了解用户的偏好。

## 架构（Architecture）

所有技能相关的信息都存储在 `~/skill-finder/` 目录下。具体结构请参考 `memory-template.md`。

```
~/skill-finder/
├── memory.md     # Preferences + liked/passed skills
└── searches.md   # Recent search history (optional)
```

## 快速参考（Quick Reference）

| 主题 | 文件          |
|-------|-------------|
| 设置     | `setup.md`       |
| 存储模板   | `memory-template.md`   |
| 搜索策略 | `search.md`       |
| 评估标准   | `evaluate.md`      |
| 技能分类   | `categories.md`     |
| 故障排除 | `troubleshooting.md`   |

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
- 作者的信誉

### 3. 附带理由进行推荐
不要只是简单地列出技能列表，要解释为什么每个技能适合用户：
> “找到了 `pdf-editor`——该工具支持表格填写和注释功能，已下载 2300 次，上周进行了更新，符合您编辑合同的需求。”

### 4. 了解用户的偏好
当用户明确表达自己的偏好时，请更新 `~/skill-finder/memory.md` 文件：
- “我更喜欢简洁的技能” → 将该偏好添加到用户设置中
- “这个工具很棒” → 说明原因后将其添加到“喜欢”的列表中
- “这个工具太复杂了” → 说明原因后将其添加到“不推荐”的列表中
切勿仅根据用户的行为来推断其隐藏的偏好。

### 5. 先查看存储的信息
在推荐技能之前，请先阅读 `memory.md` 文件：
- 跳过与用户已选中的技能相似的选项
- 优先考虑用户“喜欢”的技能所具备的特质
- 优先考虑用户明确表示的偏好

### 6. 绝不忽视安全警告
如果系统检测到某个技能存在风险，请务必：
- 向用户解释警告原因并仔细检查相关细节
- 优先推荐更安全的替代方案
- 未经用户明确同意，切勿强制安装该技能

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

1. **了解用户需求**：用户真正需要什么？
2. **进行搜索**：先尝试使用具体的关键词，必要时再扩大搜索范围
3. **评估技能质量**：参考 `evaluate.md` 中列出的标准
4. **比较多个选项**：根据适用性和质量对结果进行排序
5. **推荐最佳方案**：推荐排名前 1-3 的技能，并提供清晰的推荐理由
6. **记录用户反馈**：将用户的反馈信息保存到本地存储中

## 常见错误（Common Traps）

- 使用过于泛泛的搜索词会导致结果混乱。请使用具体的关键词（例如：使用 “react testing” 而不是 “testing”）
- 仅根据名称进行推荐可能会错过名称不同但功能更好的技能
- 忽视下载次数：下载次数少的技能可能意味着该技能已被弃用
- 不检查技能的更新时间：过时的技能可能会引发问题

## 安全性与隐私（Security & Privacy）

**会离开用户设备的数据**：
- 用户的搜索查询会被发送到 ClawHub 注册表（公开搜索）

**保留在用户设备上的数据**：
- 所有用户设置（存储在 `~/skill-finder/memory.md` 中）
- 搜索历史记录（如果启用）

**本系统不会执行以下操作：**
- 未经用户同意就安装技能
- 使用强制安装选项绕过安全警告
- 收集用户的隐藏行为数据
- 访问 `~/skill-finder/` 目录以外的文件

## 相关工具（Related Tools）

如果用户同意，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：用于安装技能
- `skill-manager`：用于管理已安装的技能并提示更新
- `skill-builder`：用于从头开始创建新技能
- `skill-update`：用于更新现有技能

## 用户反馈（Feedback）

- 如果您觉得本工具有用，请使用 `clawhub star skill-finder` 给予评价
- 要保持工具的最新状态，请使用 `clawhub sync` 命令同步数据