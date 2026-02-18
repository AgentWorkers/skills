---
name: skill-releaser
description: 通过完整的发布流程将技能发布到 ClawhHub：包括自动代码生成、OPSEC 安全性扫描、双重审核（代理审核 + 用户审核）、强制推送发布以及安全性扫描验证。该流程适用于发布技能、准备技能发布、审核技能的发布状态或检查技能是否具备发布条件时使用。
version: 1.4.0
triggers:
  - release skill
  - publish skill
  - prepare for clawhub
  - release readiness
  - skill release review
  - publish to clawhub
---
# 技能发布流程

该流程负责将技能从内部仓库协调发布到 ClawhHub。

## 使用场景

- 用户输入 “release {skill}” 或 “publish {skill} to clawhub”
- 用户输入 “prepare {skill} for release” 或 “check release readiness”
- 用户输入 “review {skill} for publication”
- 在重构流程中通过 Cron 任务触发发布检查

## 前提条件

**OpenClaw 与用户之间的交互流程：**
- 代理程序运行在具有 Shell 访问权限的机器上，用于执行 Git 和 CLI 操作
- 用户通过消息通道（如 Telegram、Discord、Signal 等）进行沟通（通常使用手机）
- 用户直接在浏览器或手机上查看私有的 GitHub 仓库——仓库本身即为审核对象，而非文本摘要
- 用户通过回复代理程序的消息来批准或拒绝发布（支持自然语言指令，例如 “approve”、“revise: fix the readme”、“reject”）
- 代理程序可以代表用户的已认证账户使用 `gh` CLI 创建和管理 GitHub 仓库
- 代理程序会在请求用户审核之前将代码推送到私有的测试仓库中，确保有内容可供审核
- 未经用户明确批准，代理程序不会公开发布任何内容——这是一个严格的限制
- 仓库在测试和审核阶段为私有状态；发布时，会通过删除分支并执行强制推送（一次干净的提交）来清除历史记录，之后再切换为公开状态
- 完整的发布过程可能跨越多个阶段——私有测试仓库会保留所有状态，以便任何代理程序都可以继续执行后续操作
- 多个技能可以同时处于发布流程的不同阶段

## 必备条件

- 已通过 `gh` CLI 进行认证（用于创建仓库和修改仓库可见性）
- 已安装 `clawhub` CLI（用于将技能发布到 ClawhHub）
- 存在一个至少包含 `SKILL.md` 文件的技能目录

## 范围与限制

- 该流程负责整个发布流程：结构搭建、安全扫描、审核和发布。
- 该流程不负责技能内容的创建或设计。`SKILL.md` 文件必须已经详细描述了技能的功能。其他所有工作（模板文件、结构搭建等）均由该流程完成。

用户只需提供完整的 `SKILL.md` 文件，该流程会处理后续的所有步骤，包括生成所有缺失的文件。

## 自动化模型

发布流程包含两个完全自动化的阶段，中间有一个人工审核环节：

**设计原则：**
- 用户只需输入一次 “release {skill}”，代理程序会不间断地执行整个第一阶段。
- 代理程序发送一条消息：包含审核链接和推荐意见，然后等待用户回复。
- 用户回复一个单词后，代理程序会不间断地执行整个第二阶段。
- 如果任何步骤失败，代理程序会自动修复问题并继续执行；只有在无法修复的情况下才会通知用户。
- 速率限制、重试和延迟操作都会在后台默默处理（通过延迟和重试来实现，而不会显示提示信息）。

**禁止的做法：**
- 不要询问 “是否需要创建仓库？”——直接创建仓库
- 不要询问 “是否需要执行安全扫描？”——直接执行扫描
- 不要报告中间步骤——只报告最终的审核请求和发布结果
- 不要询问关于速率限制或临时错误的问题——默默地重试
- 不要在一个阶段内发送多条消息——将所有操作批量处理成一条消息

## 流程步骤

### 第一步：构建结构（自动生成模板文件）
在进行任何质量检查之前，根据现有的 `SKILL.md` 文件生成所有缺失的结构文件：

**如果文件缺失，则自动生成：**
| 文件 | 来源 | 生成方法 |
|------|--------|-------------------|
| `skill.yml` | `SKILL.md` 的前言部分 | 从 `SKILL.md` 中提取名称、描述、版本和触发条件 |
| `README.md` | `SKILL.md` 中的描述和使用说明 | 生成适用于 GitHub 页面的内容，包括功能介绍、使用场景和示例命令 |
| `CHANGELOG.md` | `skill.yml` 中的版本信息 + Git 日志 | 格式为 `## v{version} — {date}`，并附上当前状态的总结 |
| `tests/test-triggers.json` | `SKILL.md` 中的触发条件 | 从触发条件列表中筛选 `shouldTrigger`，并从禁止的操作中筛选 `shouldNotTrigger` |
| `scripts/` | 创建目录 | 如果没有脚本需求，则创建空目录或放置占位符 `README.md` |
| `references/` | 创建目录 | 如果没有参考资料需求，则创建空目录或放置占位符 `README.md` |
| `LICENSE` | 默认使用 MIT 许可证 | 使用标准的 MIT 许可证文本 |
| `.gitignore` | 标准配置 | 包含 `node_modules/`、`.DS_Store` 和 `.log` 文件 |

**规则：**
- 从不覆盖现有文件——仅生成缺失的部分
- 所有生成的内容都来源于 `SKILL.md`——不会添加额外的功能
- 如果 `SKILL.md` 中的信息不足，应标记为内容缺失（用户需要先修改 `SKILL.md`）
- 生成的 `README.md` 对从未使用过该技能的用户来说也是易于理解的

**构建结构后的验证：**
- 运行 `scripts/validate-structure.sh` 脚本——评分必须达到 8/8 分
- 如果评分未达到 8/8，则需要找出缺失的部分并进行修复

### 第 1.5 步：版本更新（仅限已有技能）
如果该技能之前已经发布过，在继续发布前需要更新版本：

1. **检查当前发布的版本：**
```bash
clawhub search {name}
```

2. 在 `skill.yml` 和 `SKILL.md` 的前言部分更新版本号：
   - 小幅更新（1.0.0 → 1.0.1）：修复漏洞、修正拼写错误、更新文档
   - 中等更新（1.0.0 → 1.1.0）：添加新功能、修改结构
   - 大幅更新（1.0.0 → 2.0.0）：引入重大变更、彻底重构

3. 在 `CHANGELOG.md` 中添加新的版本信息，说明具体变更内容

首次发布时可以跳过此步骤。

### 第二步：准备发布内容
验证技能目录是否完整：
- `SKILL.md` 是否存在，其中包含描述和使用说明
- `skill.yml` 是否包含名称、描述和触发条件
- 结构评分是否达到 8/8 分（根据第一步的结果）
- 不存在明显的安全违规问题（快速扫描）

如果任何检查失败，需要修复相关问题后再继续。

### 第三步：创建私有测试仓库
```bash
# Check if repo already exists
gh repo view your-org/openclaw-skill-{name} 2>/dev/null

# If not, create it
gh repo create your-org/openclaw-skill-{name} --private --description "{skill description from skill.yml}"
```

### 第四步：准备发布内容
将处理过的技能内容复制到一个干净的目录中：
```bash
mkdir -p /tmp/skill-release-{name}
cp -r skills/{name}/* /tmp/skill-release-{name}/

# Remove internal-only files
rm -f /tmp/skill-release-{name}/WORKSPACE.md
rm -f /tmp/skill-release-{name}/.gitignore
rm -rf /tmp/skill-release-{name}/_meta.json
```

如果缺少以下文件，请添加：
- `LICENSE`（默认使用 MIT 许可证）
- `README.md`（必须能够作为适合陌生用户的 GitHub 页面）
- `.gitignore` 文件

### 第五步：安全深度扫描
```bash
bash scripts/opsec-scan.sh /tmp/skill-release-{name}
```
扫描结果必须为 “CLEAN”（返回代码 0）。如果发现安全问题，请在发布的副本中进行修复。不要修改 `openclaw-knowledge` 仓库中的源代码——保持内部版本的原始状态。

### 第六步：代理审核
生成审核文档：
```markdown
# Release Review: {skill-name}

## Checklist
- [ ] SKILL.md clear and useful to a stranger
- [ ] README.md works as GitHub landing page
- [ ] skill.yml triggers accurate and complete
- [ ] Scripts work without hardcoded dependencies
- [ ] Tests present and described
- [ ] CHANGELOG.md current
- [ ] LICENSE present
- [ ] No references to internal repos, infrastructure, or personal info
- [ ] OPSEC scan: CLEAN
- [ ] Competitive position: {novel|ahead}

## OPSEC Scan Output
{paste scan output}

## Competitive Summary
{from audits/{name}-competitive.md}

## Recommendation
APPROVE / REVISE: {reasons}
```

将文档保存到 `openclaw-knowledge/reviews/{name}-release-review.md` 文件中。

### 第七步：将内容推送到私有测试仓库
将处理过的内容推送到私有测试仓库，以便用户可以在任何设备（手机、笔记本电脑等）上查看仓库：
```bash
cd /tmp/skill-release-{name}
git init
git config user.email "agent@localhost"
git config user.name "SkillEngineer"
git add .
git commit -m "v{version}: Initial release of {name}"
git remote add origin https://github.com/your-org/openclaw-skill-{name}.git
git branch -M main
git push -u origin main
```

### 第八步：用户审核
通过 Telegram 将仓库链接和简要说明发送给用户：
```
RELEASE REVIEW: {skill-name}

Score: {X}/24 | OPSEC: CLEAN | Position: {novel/ahead}
Review here: https://github.com/your-org/openclaw-skill-{name}

{1-2 sentence summary of what the skill does}

Agent recommendation: {APPROVE/REVISE}

Reply: approve / revise:{feedback} / reject
```

仓库本身即为审核对象。用户需要查看实际的文件内容，而不是文本摘要。
等待用户的回复。未经明确批准不得继续下一步。

### 第九步：删除历史记录并切换为公开状态（用户批准后）
删除 Git 的历史记录（可能包含之前版本中的安全修复内容），然后将仓库设置为公开状态：
```bash
cd /tmp/skill-release-{name}
# Orphan branch erases all history
git checkout --orphan clean
git add -A
git commit -m "v{version}: {name}"
git branch -D main
git branch -m main
git push -f origin main

# Flip visibility
gh repo edit your-org/openclaw-skill-{name} --visibility public
```

通过一次提交清除历史记录，保持仓库的简洁性。避免使用双重仓库结构。

### 第十步：将技能发布到 ClawhHub
```bash
clawhub publish /tmp/skill-release-{name} \
  --slug {name} \
  --name "{Display Name}" \
  --version {version} \
  --changelog "{summary of changes}"
```

### 第十一步：验证安全扫描结果（需要使用浏览器）
ClawhHub 会自动使用 VirusTotal（Code Insight）和 OpenClaw 自带的扫描工具对所有发布的技能进行安全扫描。**在扫描结果审核完毕之前，发布过程视为未完成。**

**使用浏览器工具查看扫描结果：**
1. **使用浏览器打开技能详情页面：**
```
browser start (profile=openclaw)
browser navigate → https://clawhub.ai/{username}/{slug}
browser snapshot (refs=aria)
```

2. **找到 “Security Scan” 部分**：
   - **VirusTotal 的扫描结果：** 无害 / 可疑 / 恶意 / 待定
   - **OpenClaw 的扫描结果：** 无害 / 可疑 / 恶意（附带置信度等级）
   - **详细信息：** 显示被标记问题的具体原因（展开 “Details” 可查看更多细节）
   - **VirusTotal 的报告链接：** 提供完整分析的直接链接

3. **根据扫描结果采取相应措施：**

| 扫描结果 | 含义 | 应采取的行动 |
|---------|---------|--------|
| 无害（两者均显示为无害） | 可以继续下一步 |
| 待定 | 扫描结果仍在处理中 | 等待 2 分钟后重新扫描 |
| 可疑（存在未声明的权限需求） | 技能需要额外的权限（例如访问 `gh`、`clawhub`、`git`、文件系统） | 在 `skill.yml` 中添加相应的权限设置，更新版本号，然后重新发布 |
| 可疑（其他问题） | 需要进一步检查 | 查看详细信息。如果是误报，请联系 OpenClaw 的安全团队；如果是真实问题，请修复后重新发布 |
| 恶意 | 被阻止下载 | 立即修复问题，更新版本号，然后从第一步开始重新执行整个流程 |

4. **常见问题——未声明的权限需求：**
   如果检测到需要特殊权限（如访问 `gh`、`clawhub`、`git`、文件系统的权限），在 `skill.yml` 中添加 `permissions` 字段：
   ```yaml
   permissions:
     - exec: git, gh CLI (repo creation, visibility changes)
     - exec: clawhub CLI (publishing)
     - filesystem: read/write skill directories
     - browser: verify scan results on ClawhHub
   ```
   然后更新版本号并重新发布。这样可以明确权限需求并解决扫描问题。

5. **如果 VirusTotal 的扫描结果仍显示为 “待定”，请继续执行第十二步，但在提交时需注明这一点。扫描结果是异步完成的。**

### 第十二步：完成发布
确认发布成功后，将所有链接和扫描结果发送给用户：

```
RELEASED: {skill-name} v{version}

GitHub: https://github.com/your-org/openclaw-skill-{name}
ClawhHub: https://clawhub.ai/{username}/{slug}
VirusTotal: {verdict} — {report link}
OpenClaw Scan: {verdict} ({confidence})

{1-line description}
```

**更新跟踪信息**——记录在内存或 `STATUS.json` 文件中：
- GitHub 的公开链接
- ClawhHub 的链接和版本号
- 发布日期和版本信息
- 安全扫描结果（VirusTotal 和 OpenClaw 的扫描结果）
- 审核日期（代理程序和用户的审核时间）

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|-----|
| 准备阶段失败 | 评分过低或存在安全问题 | 先完成重构 |
| 安全扫描发现发布副本中的问题 | 清理不完整 | 修复发布副本中的问题后重新扫描 |
| 创建 GitHub 仓库失败 | 认证问题或仓库名称已被占用 | 检查 `gh` 的认证状态，尝试使用其他名称 |
| 将技能发布到 ClawhHub 失败 | 未安装 `clawhub` 或认证失败 | 运行 `npm install -g clawhub` 并完成认证 |
| 用户拒绝发布 | 收到用户反馈 | 根据反馈重新开始发布流程 |

## 示例

- **发布特定技能：**
  “将 skill-engineer 发布到 ClawhHub”

- **在不发布技能的情况下检查准备情况：**
  “Is evidence-based-investigation 准备好了吗？”

- **批量检查准备情况：**
  “哪些技能已经准备好发布？”