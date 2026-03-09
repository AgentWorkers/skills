---
name: "Skill Finder (Find ClawHub skills + Search Skills.sh)"
slug: skill-finder
version: "1.1.4"
homepage: https://clawic.com/skills/skill-finder
description: "当用户需要新的功能或更好的选项时，可以在 Skills.sh 和 ClawHub 之间查找、比较并安装相应的代理技能（agent skills）。"
changelog: "Added support for a second skill ecosystem, clearer install guidance, and saved source preferences."
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["npx"]},"os":["linux","darwin","win32"],"configPaths":["~/skill-finder/"]}}
---
## 使用场景

当用户询问如何完成某项任务、不确定是否存在相应的技能、需要新的功能，或者询问最适合当前任务的技能时，可以使用该技能。在手动解决问题之前，如果可以通过安装新的技能来扩展代理的功能、替换现有的薄弱技能或提供更安全的替代方案，那么就应该使用该技能。

## 架构

技能相关的数据存储在 `~/skill-finder/` 目录下。如果该目录不存在或为空，请先运行 `setup.md` 脚本进行初始化。

```
~/skill-finder/
├── memory.md     # Source mode + preferences + liked/passed skills
└── searches.md   # Recent search history (optional)
```

## 迁移

如果要从旧版本升级，请参考 `migration.md` 文件中的数据迁移步骤。在升级过程中，代理必须先检查现有的数据结构是否兼容新版本。

## 快速参考

| 主题 | 文件 |
|-------|------|
| 设置 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 搜索策略 | `search.md` |
| 评估标准 | `evaluate.md` |
| 技能分类 | `categories.md` |
| 故障排除 | `troubleshooting.md` |

## 激活条件

当用户提出以下问题时，该技能会被激活：
- “我该如何完成这个任务？”
- “有适合这个任务的技能吗？”
- “你能做得更好吗？”
- “帮我找到一个适合这个任务的技能”
- “我需要一个更安全或维护更完善的工具”
- “我应该安装什么来完成这个任务？”

此外，当用户提到功能缺失、工作流程重复或对现有技能不满意时，该技能也会被激活。

## 搜索来源

该技能可以搜索两个技能库：
- **ClawHub**：通过 `npx clawhub search "查询"` 进行搜索，并使用 `npx clawhub install <slug>` 进行安装。ClawHub 提供经过筛选的技能库和内置的质量检查功能。
- **Skills.sh**：通过 `npx skills find [查询]` 进行搜索，并使用 `npx skills add <owner/repo@skill>` 进行安装。Skills.sh 是一个开放的技能库，提供了更广泛的搜索范围。

默认情况下，该技能会同时搜索这两个来源，并将结果进行比较。

**可配置的搜索模式：**
- `both`（推荐，默认设置）：同时搜索两个来源。
- `clawhub`：仅搜索 ClawHub。
- `skills.sh`：仅搜索 Skills.sh。

当前搜索模式会保存在 `~/skill-finder/memory.md` 文件中。如果用户尚未设置偏好，系统会首次向用户解释这两个搜索来源，并推荐使用 `both` 模式，之后用户可以自行选择。

## 安全提示

该技能使用 `npx clawhub` 和 `npx skills` 来搜索和安装技能。在安装前，请务必仔细检查候选技能的信息，并确保用户明确同意安装。同时，系统会记录每个技能的来源信息。

## 数据存储

该技能将用户的偏好设置、已安装的技能信息等数据存储在 `~/skill-finder/` 目录下：
- 用户的搜索来源偏好、喜欢的技能以及已安装的技能信息都保存在 `~/skill-finder/` 目录下的本地文件中。
- 用户的搜索历史记录也会保存在 `~/skill-finder/` 目录下的日志文件中。

**首次使用时的操作：**  
运行 `mkdir -p ~/skill-finder` 以创建必要的目录结构。

## 核心规则

### 1. 默认情况下同时搜索两个来源

除非用户另有指定，否则系统会同时搜索 ClawHub 和 Skills.sh 中与用户需求匹配的技能，并将结果进行比较。

**注意：**  
不要假设 Skills.sh 中的技能可以通过 ClawHub 安装，反之亦然。系统会在每个推荐结果中明确标注技能的来源和安装命令。

### 2. 不仅响应用户的明确搜索请求，还要根据功能需求进行推荐

当用户提到功能缺失、希望加快任务完成速度或需要更好的工具时，系统也会主动推荐合适的技能。

### 3. 根据实际需求进行搜索

用户提出需求时（例如：“如何处理 PDF 文件？”），系统会根据需求判断应使用哪个技能库进行搜索：
- 如果需要编辑 PDF 文件，使用 `npx clawhub search "pdf edit"` 和 `npx skills find pdf edit`。
- 如果需要生成 PDF 文件，使用 `npx clawhub search "pdf generate"` 和 `npx skills find pdf generate`。
- 如果需要解析 PDF 文件，使用 `npx clawhub search "pdf parse"` 和 `npx skills find pdf parse`。

### 4. 推荐前进行评估

在推荐技能之前，系统会仔细评估候选技能的质量，参考 `evaluate.md` 中列出的评估标准：
- 技能描述的清晰度
- 下载次数（下载次数越多，说明该技能越受欢迎、维护得越好）
- 最后更新时间（更新时间越近，说明该技能越活跃）
- 开发者或仓库的信誉
- 安装后的使用范围和操作难度

对于 Skills.sh 中的技能，系统还会关注 CLI 返回的软件包来源和安装命令信息。

### 5. 提供明确的推荐理由

在展示推荐结果时，系统会解释每个技能的适用场景、适用人群以及推荐理由：
> “最佳推荐：来自 ClawHub 的 `pdf-editor`——支持表格填写和注释功能，下载量 2300 次，上周更新。它比 Skills.sh 中的技能更适合你的需求。”

如果有多个合适的技能，系统会排名前三并明确说明各自的优缺点。

### 6. 学习并记录用户的偏好设置

当用户明确表达自己的偏好时，系统会更新 `~/skill-finder/memory.md` 文件：
- 如果用户选择“默认同时搜索两个来源”，则将搜索模式设置为 `both`。
- 如果用户指定“仅使用 Skills.sh”，则将搜索模式设置为 `skills.sh`。
- 如果用户有其他特殊要求，系统会相应地更新设置。

### 7. 首先查看用户之前的设置

在推荐技能之前，系统会读取 `memory.md` 文件中的用户设置：
- 除非用户更改了设置，否则优先使用用户之前选择的搜索来源。
- 系统会忽略用户已经安装过的技能。
- 优先推荐用户喜欢的技能。
- 系统会记录用户的偏好设置。

### 8. 遵守安装和安全限制

如果系统检测到某个技能存在风险或安装路径不明确，系统会先向用户说明风险，并推荐更安全的替代方案。
- 系统不会自动执行强制安装操作。
- 系统不会在用户未明确同意的情况下自动安装技能。
- 系统不会默认选择全局安装范围。
- 安装技能时必须获得用户的明确同意。

### 9. 优雅地处理无合适技能的情况

如果找不到合适的技能，系统会：
- 告诉用户搜索的内容和使用的搜索来源。
- 解释为什么没有找到合适的技能。
- 直接帮助用户解决问题，或建议用户创建一个专门的技能。

## 搜索命令

```bash
# ClawHub search and inspect
npx clawhub search "query"
npx clawhub inspect <slug>
npx clawhub install <slug>
npx clawhub list

# Skills.sh ecosystem
npx skills find [query]
npx skills add <owner/repo@skill>
npx skills list
npx skills check
npx skills update

# Example install string returned by `npx skills find`
npx skills add vercel-labs/agent-skills@vercel-react-best-practices
```

## 工作流程

1. **检测**：判断用户是否提到了功能缺失或需要安装新技能。
2. **读取设置**：读取 `~/skill-finder/memory.md` 文件中的搜索来源设置和用户偏好。
3. **理解需求**：明确用户实际需要什么功能。
4. **搜索**：默认情况下同时搜索两个来源；如果用户有特定偏好，则使用用户指定的来源。
5. **评估**：根据质量标准（参考 `evaluate.md`）对搜索结果进行评估。
6. **比较**：综合两个来源的结果，根据适用性和质量进行排序。
7. **推荐**：推荐排名前三的技能，并给出明确的推荐理由。
8. **安装或提供替代方案**：只有在用户同意的情况下才进行安装；否则直接提供帮助。
9. **记录用户反馈**：将用户的反馈信息保存在 `memory.md` 文件中。

## 推荐结果格式

在展示推荐结果时，系统会使用以下格式：

```text
Best fit: <slug or owner/repo@skill>
Source: <ClawHub or Skills.sh>
Why it wins: <1-2 lines>
Install: <exact command>
Tradeoffs: <what it does not cover or where alternative is stronger>
Alternatives: <slug>, <slug>
Next step: Install now or continue without installing
```

## 常见问题

- 仅等待用户输入“find a skill”这样的关键词，可能会错过主动发现合适技能的机会。
- 使用过于泛化的搜索词（例如“testing”）会导致搜索结果不准确。请使用具体的任务描述（例如“react testing”）。
- 如果用户设置了同时搜索两个来源的偏好，却只在一个来源中搜索，可能会导致错过更好的替代方案。
- 在不同的技能库之间混合使用安装命令（例如同时使用 `npx clawhub search` 和 `npx skills find`），可能会导致推荐结果不准确。
- 忽略技能的下载次数（下载次数少的技能可能意味着该技能已被弃用）。
- 不检查技能的更新时间，可能会导致使用过时的技能。

## 安全与隐私

**会发送到外部的数据：**
- 发送到 ClawHub 注册库的搜索请求（公开搜索数据）。
- 通过 `skills` CLI 或 Skills.sh 进行的搜索请求。

**保留在本地的数据：**
- 用户的所有偏好设置（`~/skill-finder/memory.md`）。
- 用户的搜索历史记录（如果启用了该功能）。

**该技能不会：**
- 未经用户同意就安装技能。
- 使用强制安装选项（`-y`）来忽略系统警告。
- 自动确认安装操作。
- 在用户未明确同意的情况下自动切换到全局安装范围。
- 收集用户的隐藏行为数据。
- 访问 `~/skill-finder/` 之外的文件。

## 相关技能

如果用户同意，可以使用以下命令安装相关技能：
- `npx clawhub install <slug>`：用于安装和管理已安装的技能。
- `skill-builder`：用于从头开始创建新的技能。
- `skill-update`：用于更新已安装的技能。

## 用户反馈

- 如果觉得该技能有用，请使用 `clawhub star skill-finder` 给予评分。
- 为了保持功能更新，请使用 `clawhub sync` 命令同步设置。