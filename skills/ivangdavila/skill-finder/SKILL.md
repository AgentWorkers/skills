---
name: "Skill Finder (Find ClawHub skills + Search Skills.sh)"
slug: skill-finder
version: "1.1.5"
homepage: https://clawic.com/skills/skill-finder
description: "当用户需要新的功能、更高效的工作流程、更强大的工具或更安全的解决方案时，可以在 ClawHub 和 Skills.sh 之间查找、比较并安装相应的代理技能（agent skills）。以下是使用这些功能的场景：  
1. 当用户询问如何执行某项操作、如何改进或自动化某个流程，或者需要安装什么工具时；  
2. 当某个技能能够扩展代理的功能、替代现有的手动操作方式，或者填补功能上的空白时；  
3. 当你需要找到最适合用户需求的选择（而不仅仅是提供一个直接的答案）时。"
changelog: "Broader discovery guidance for finding better, safer, and more relevant skills faster."
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["npx"]},"os":["linux","darwin","win32"],"configPaths":["~/skill-finder/"]}}
---
## 使用场景

当用户询问如何完成某项任务、不确定是否存在相应的技能、需要新的功能，或者询问适合某项工作的最佳技能时，可以使用该功能。在手动解决问题之前，如果可以通过安装新的技能来扩展代理程序、替换现有的薄弱技能或提供更安全的替代方案，那么就应该使用该功能。

## 架构

技能相关的数据存储在 `~/skill-finder/` 目录下。如果该目录不存在或为空，请运行 `setup.md` 文件进行初始化。

```
~/skill-finder/
├── memory.md     # Source mode + preferences + liked/passed skills
└── searches.md   # Recent search history (optional)
```

## 迁移

如果从旧版本升级，请参考 `migration.md` 文件了解数据迁移的步骤。在升级过程中，代理程序必须先检查现有的数据结构是否兼容新版本。

## 快速参考

| 主题 | 文件      |
|-------|---------|
| 初始化 | `setup.md`   |
| 数据模板 | `memory-template.md` |
| 搜索策略 | `search.md`   |
| 评估标准 | `evaluate.md`   |
| 技能分类 | `categories.md`   |
| 故障排除 | `troubleshooting.md` |

## 激活条件

当用户提出以下问题时，该功能会被激活：
- “我该如何完成这个任务？”
- “有适合这个任务的技能吗？”
- “你能做得更好吗？”
- “帮我找到一个适合这个任务的技能。”
- “我需要一个更安全或维护更完善的工具。”
- “我应该安装什么技能来完成这个任务？”

此外，当用户反映当前技能存在功能缺失、工作流程重复或对现有技能不满意时，该功能也会被激活。

## 搜索来源

该功能可以搜索两个技能库：
- **ClawHub**：通过 `npx clawhub search "查询"` 进行搜索，并使用 `npx clawhub install <slug>` 进行安装。该库提供经过筛选的技能列表，并包含内置的技能检查功能。
- **Skills.sh**：通过 `npx skills find [查询]` 进行搜索，并使用 `npx skills add <owner/repo@skill>` 进行安装。该库来自一个开放的技能生态系统。

默认情况下，该功能会同时搜索这两个来源，并对比搜索结果。

**可配置的搜索模式：**
- `both`（推荐，默认设置）：同时搜索两个来源。
- `clawhub`：仅搜索 ClawHub。
- `skills.sh`：仅搜索 Skills.sh 库。

当前搜索模式会保存在 `~/skill-finder/memory.md` 文件中。如果用户尚未设置偏好，系统会首次向用户解释这两个搜索来源，并推荐使用 `both` 模式，随后用户可以自行选择。

## 安全注意事项

该功能使用 `npx clawhub` 和 `npx skills` 命令从两个不同的技能库中搜索和安装技能。在安装前，请务必仔细评估候选技能的可靠性；所有安装操作都需要用户的明确同意；同时，系统会记录每个技能的来源信息。

## 数据存储

该功能将用户的偏好设置、已安装的技能信息以及搜索历史记录存储在 `~/skill-finder/` 目录下：
- 用户的偏好设置、喜欢的技能以及已安装的技能信息保存在 `~/skill-finder/` 目录下的本地文件中。
- 用户的最近搜索记录也会保存在 `~/skill-finder/` 目录下的日志文件中。

**首次使用时的操作：**  
执行 `mkdir -p ~/skill-finder` 命令以创建必要的目录结构。

## 核心规则

### 1. 默认情况下同时搜索两个来源

除非用户另有明确要求，否则系统会同时搜索 ClawHub 和 Skills.sh 库，然后对比搜索结果。

**注意：**  
不要假设 Skills.sh 中的技能可以通过 ClawHub 安装，反之亦然。系统会在每个推荐结果中明确标注技能的来源和安装命令。

### 2. 不仅响应用户的明确搜索请求，还要根据功能需求进行推荐

当用户反映功能缺失、希望加快任务完成速度或需要更合适的工具时，系统也会主动提供帮助。

### 3. 根据实际需求进行搜索

用户提出需求时（例如：“如何处理 PDF 文件？”），系统需要判断用户真正需要什么功能：
- 编辑 PDF 文件？ -> 使用 `npx clawhub search "pdf edit"` 和 `npx skills find pdf edit`。
- 创建 PDF 文件？ -> 使用 `npx clawhub search "pdf generate"` 和 `npx skills find pdf generate`。
- 提取 PDF 文件内容？ -> 使用 `npx clawhub search "pdf parse"` 和 `npx skills find pdf parse`。

### 4. 推荐前进行评估

在推荐技能之前，系统会仔细评估候选技能的质量，参考 `evaluate.md` 中规定的评估标准：
- 技能描述的清晰度。
- 下载次数（下载次数越多，通常表示该技能维护得越好）。
- 最后更新时间（更新时间越近，技能通常越活跃）。
- 开发者或仓库的信誉。
- 安装后的使用范围和复杂性。

对于 Skills.sh 库中的技能，系统还会关注 CLI 返回的软件包来源和安装命令信息。

### 5. 提供详细的推荐理由

在展示推荐结果时，系统会解释每个技能的适用场景、适用对象以及推荐原因：
> “最佳推荐：ClawHub 的 `pdf-editor`——支持表格填写和注释功能，下载量 2300 次，上周更新。它比 Skills.sh 中的技能更适合你的需求。”

如果有多个合适的技能，系统会排名前三，并明确指出各自的优缺点。

### 6. 学习并记录用户的偏好设置

当用户明确表达自己的偏好时，系统会更新 `~/skill-finder/memory.md` 文件：
- 如果用户选择“默认同时搜索两个来源”，则将搜索模式设置为 `both`。
- 如果用户指定“仅使用 Skills.sh”，则将搜索模式设置为 `skills.sh`。
- 如果用户有其他特殊要求，系统也会相应地更新设置。

### 7. 首先查看用户之前的设置

在推荐技能之前，系统会读取 `memory.md` 文件中的用户偏好设置：
- 除非用户更改了设置，否则优先使用用户之前的偏好。
- 系统会忽略那些与用户之前选择的技能相似的候选项。
- 优先推荐用户喜欢的技能。
- 如果用户对某个技能有负面评价，系统也会将其记录下来。

### 8. 遵守安装和安全限制

如果系统检测到某个技能存在风险，或者安装路径不明确，系统会先向用户说明原因，并推荐更安全的替代方案。
- 系统不会自动执行强制安装操作。
- 系统不会在用户未明确同意的情况下自动接受安装提示（例如使用 `-y` 参数）。
- 除非用户明确要求，否则不会自动选择全局安装范围。
- 安装操作必须得到用户的明确同意。

### 9. 优雅地处理无合适解决方案的情况

如果找不到合适的技能，系统会：
- 告诉用户搜索的内容和使用的搜索来源。
- 解释为什么没有找到合适的技能。
- 直接提供帮助，或建议用户创建一个专门的技能。

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

1. **检测**：判断用户是否需要安装新的技能或存在功能上的缺失。
2. **读取设置**：读取 `~/skill-finder/memory.md` 文件中的搜索来源和用户偏好设置。
3. **理解需求**：明确用户实际需要什么功能。
4. **搜索**：默认情况下同时搜索两个来源；如果用户有特殊要求，也会按照用户的偏好设置进行搜索。
5. **评估**：根据搜索结果的质量进行评估（参考 `evaluate.md` 文件中的标准）。
6. **对比结果**：综合两个来源的结果，根据适用性和质量进行排序。
7. **推荐**：推荐排名前三的技能，并详细说明推荐理由。
8. **安装或提供替代方案**：只有在用户同意的情况下才进行安装；否则直接提供帮助。
9. **记录用户反馈**：将用户的反馈信息保存在 `memory.md` 文件中。

## 推荐结果的结构

在展示推荐结果时，系统会采用以下结构：

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
- 使用过于泛泛的搜索词可能会导致搜索结果混乱。请使用具体的关键词，例如“react testing”而不是“testing”。
- 如果用户设置了同时搜索两个来源的偏好，却只在一个来源中搜索，可能会错过更好的解决方案。
- 在推荐技能时，如果混合使用 `ClawHub` 和 `Skills.sh` 的命令，可能会导致推荐不准确。
- 忽略技能的下载次数（下载次数少可能意味着该技能已被弃用）。
- 不检查技能的更新时间可能会导致使用过时的技能。

## 安全与隐私

**会传输到外部的数据：**
- 发送到 ClawHub 注册库的搜索请求（公开搜索数据）。
- 通过 `skills` CLI 或 Skills.sh 库发送的搜索请求。

**会保存在本地的数据：**
- 用户的所有偏好设置（`~/skill-finder/memory.md`）。
- 搜索历史记录（如果用户启用了该功能）。

**该功能不会：**
- 未经用户同意就安装技能。
- 使用强制安装选项（`-y` 参数）。
- 在用户未明确同意的情况下自动安装技能。
- 自动切换到全局安装范围。
- 收集用户的隐藏行为数据。
- 访问 `~/skill-finder/` 目录以外的文件。

## 相关技能

如果用户同意，可以使用以下命令安装相关技能：
- `npx clawhub install <slug>`：用于安装和管理已安装的技能。
- `skill-builder`：用于从零开始创建新的技能。
- `skill-update`：用于更新现有的技能。

## 用户反馈

- 如果您觉得该功能有用，请使用 `clawhub star skill-finder` 给予反馈。
- 为了保持功能的更新，请使用 `clawhub sync` 命令同步设置。