---
name: skill-releaser
description: 通过完整的发布流程将技能发布到 ClawhHub：包括自动代码生成（auto-scaffolding）、OPSEC 安全性扫描、双重审核（代理审核 + 用户审核）、强制推送发布（force-push release）以及安全扫描验证。该流程适用于发布技能、准备技能发布、审核技能的发布状态或检查发布是否准备就绪等场景。
version: 1.5.0
triggers:
  - release skill
  - publish skill
  - prepare for clawhub
  - release readiness
  - skill release review
  - publish to clawhub
---
# 技能发布工具

该工具负责协调从内部仓库到ClawhHub的完整技能发布流程。

## 使用场景

- 用户输入“发布{技能名称}”或“将{技能名称}发布到ClawhHub”
- 用户输入“准备发布{技能名称}”或“检查发布准备情况”
- 用户输入“审核{技能名称}以准备发布”
- 在重构流程中，通过Cron触发发布检查

## 前提条件

**OpenClaw与用户在发布过程中的交互方式：**
- 代理程序运行在具有shell访问权限的机器上（可执行git和CLI命令）
- 用户通过消息通道（如Telegram、Discord、Signal等）进行沟通——通常是在手机上
- 用户直接在浏览器或手机上查看私有的GitHub仓库——仓库本身就是审核的对象，而不是文本摘要
- 用户通过回复代理程序的消息来批准或拒绝发布（使用自然语言，例如：“批准”、“修改：修复readme文件”、“拒绝”）
- 代理程序可以代表用户的已认证账户通过`gh` CLI创建和管理GitHub仓库
- 代理程序在请求用户审核之前，会先将内容推送到私有的测试仓库，以便有内容可供审核
- 未经用户明确批准，代理程序不会公开发布任何内容——这是一个严格的限制
- 仓库在测试和审核阶段是私有的。发布时，会通过创建孤儿分支并强制推送（单次干净的提交）来清除历史记录，然后切换为公开状态
- 完整的发布过程可能跨越多个会话——私有的测试仓库会保留状态，以便任何代理程序都可以继续执行
- 多个技能可以同时处于发布流程的不同阶段

## 先决条件

- 已通过`gh` CLI认证（用于创建仓库和更改可见性）
- 已安装`clawhub` CLI（用于向ClawhHub发布）
- 存在一个至少包含`SKILL.md`文件的技能目录

## 范围与限制

**该工具负责：**完整的发布流程——包括结构搭建、OPSEC扫描、审核和发布。
**该工具不负责：**技能内容的创建或设计。`SKILL.md`文件必须已经描述了技能的功能。其他所有内容（模板文件、结构搭建等）都是该工具的工作范围。

拥有已完成`SKILL.md`文件的用户应该能够输入“发布这个技能”，该工具会处理从这一步开始的所有流程——包括生成所有缺失的结构文件。

## 自动化模型

发布流程包含两个完全自动化的阶段，中间有一个人工审核环节。**无论是单个技能还是批量发布，都遵循相同的模型。**

### 单个技能发布
```
Phase 1 (AUTO): Steps 1-7 — scaffold, validate, stage, scan, review, push
     ↓
  GATE: User reviews private repo, replies "approve" / "revise" / "reject"
     ↓
Phase 2 (AUTO): Steps 9-12 — erase history, flip public, publish, verify scan, deliver
```

### 批量发布（多个技能）
```
Phase 1 (PARALLEL): Spawn subagents — one per skill, all run Phase 1 simultaneously
     ↓
  GATE: ONE batch review message with all repo links
        User replies: "approve all" / "approve A,C; revise B: fix readme"
     ↓
Phase 2 (PARALLEL): Spawn subagents for approved skills, all publish simultaneously
     ↓
  DELIVERY: ONE batch summary with all links and scan results
```

**批量发布规则：**
- 绝不串行处理发布请求——为每个技能创建一个子代理程序来执行第一阶段
- 在开始下一阶段之前，不会因为某个技能的审批而阻塞
- 在批量审核消息中为每个技能分配一个唯一的短ID（A、B、C...）
- 收集所有第一阶段的结果，然后发送一条包含这些短ID的批量审核消息
- 接受批量审批：`批准全部` / `批准A,C` / `修改B：修复readme文件`
- 审批通过后，同时执行所有第二阶段的操作

**设计原则：**
- 用户输入“发布这些技能”一次。代理程序会并行执行所有第一阶段的操作。
- 代理程序发送一条消息：包含所有审核链接和建议。然后等待用户回复。
- 用户回复一次。代理程序会并行执行所有第二阶段的操作。
- 代理程序发送一条包含所有结果的最终消息。
- 如果有任何步骤失败，代理程序会自动修复并继续执行。只有在无法修复的情况下才会向用户报告。
- 对于速率限制、重试和延迟的处理都是自动进行的（通过睡眠和重试来处理，而不会显示提示信息，例如“达到速率限制了，我应该再试一次吗？”）

**避免的做法：**
- 不要串行处理发布请求——始终使用子代理程序并行处理
- 在开始B技能的第一阶段之前，不要因为A技能的审批而阻塞
- 不要为每个技能发送单独的审核消息——将它们批量处理
- 不要询问“我应该创建仓库吗？”——直接创建仓库
- 不要报告中间步骤——只报告批量审核和最终发布的结果
- 不要询问关于速率限制或临时错误的问题——自动进行重试

## 流程

### 第1步：结构搭建（自动生成模板文件）
在任何质量检查之前，从现有的`SKILL.md`文件生成所有缺失的结构文件：

**如果缺失则自动生成：**

| 文件 | 来源 | 生成方法 |
|------|--------|-------------------|
| `skill.yml` | `SKILL.md`的前言部分 + 触发条件 | 从`SKILL.md`中提取名称、描述、版本和触发条件 |
| `README.md` | `SKILL.md`中的描述和使用说明 | 为外部用户准备的GitHub页面内容：技能的功能、安装方法、未来计划。不是给代理程序的指令。 |
| `CHANGELOG.md` | `skill.yml`中的版本信息 + git日志 | `## v{版本} — {日期}` + 当前状态的总结 |
| `tests/test-triggers.json` | `SKILL.md`中的触发条件 | 从触发条件列表中判断是否应该触发检查，从避免错误的条件列表中判断不应该触发检查 |
| `scripts/` | 创建目录 | 如果不需要脚本，则创建空目录或放置占位符`README.md` |
| `references/` | 创建目录 | 如果不需要引用资料，则创建空目录或放置占位符`README.md` |
| `LICENSE` | 默认的MIT许可证 | 标准的MIT许可证文本 |
| `.gitignore` | 标准配置 | `node_modules/`, `.DS_Store`, `*.log` |

**规则：**
- 绝不要覆盖现有文件——只生成缺失的部分
- 所有生成的内容都来源于`SKILL.md`——不要添加额外的功能
- 如果`SKILL.md`中的信息不足以生成某个文件，就将其标记为内容缺失（用户需要先修复`SKILL.md`）
- 生成的`README.md`对于从未见过该技能的外部用户来说必须是可理解的

**搭建后的验证：**
- 运行`scripts/validate-structure.sh`——必须得到8分（满分8分）
- 如果得分不是8分，找出缺失的部分并进行修复

### 第1.5步：版本升级（仅限需要升级的情况）
如果该技能之前已经发布过，在继续之前需要升级版本：

1. **检查当前已发布的版本：**
```bash
clawhub inspect {slug}
```

2. 在`skill.yml`和`SKILL.md`的前言部分中升级版本：
   - 小幅升级（1.0.0 → 1.0.1）：修复错误、拼写错误、文档更新
   - 中度升级（1.0.0 → 1.1.0）：新增功能、添加新章节、结构调整
   - 大幅升级（1.0.0 → 2.0.0）：重大修改、全面重写

3. 使用新的版本信息更新`CHANGELOG.md`

4. 确认`skill.yml`中设置了`display_name`——这是显示在ClawhHub上的标题。
   必须明确设置；不能从slug字段推导出来或猜测。
   如果缺失，请现在添加：
   ```yaml
   display_name: "Human Readable Title"  # Required — used as ClawhHub listing title
   ```
   规则：
   - 标题使用大写英文，避免使用专业术语
   - 描述技能的功能，而不是实现方式
   - 例如：slug `autonomous-task-runner` → `display_name: "自主任务运行器"`
   - 例如：slug `skill-releaser` → `display_name: "技能发布工具"`

首次发布时可以跳过此步骤（但仍需确认`display_name`是否存在）。

### 第2步：准备发布
验证技能目录是否完整：
- `SKILL.md`存在，并包含描述和使用说明
- `skill.yml`存在，并包含名称、描述和触发条件
- 结构评分达到8分（来自第1步）
- 没有明显的OPSEC违规（快速扫描）

如果任何检查失败，请报告需要修复的问题。不要继续下一步。

### 第3步：创建私有测试仓库
```bash
# Check if repo already exists
gh repo view your-org/openclaw-skill-{name} 2>/dev/null

# If not, create it — CRITICAL: use the SANITIZED description, not the source skill.yml
# Run OPSEC scan on the description string BEFORE passing to gh repo create
gh repo create your-org/openclaw-skill-{name} --private --description "{sanitized description}"
```

**关于仓库元数据的OPSEC注意事项：**在仓库切换为公开状态时，传递给`gh repo create`的描述信息也会公开。必须对其进行检查，确保没有包含敏感信息（如组织名称、个人信息、内部项目名称）。这不能通过基于文件的扫描工具来完成——必须手动检查。

### 第4步：复制发布内容
仅将技能目录的内容复制到一个干净的测试区域：
```bash
mkdir -p /tmp/skill-release-{name}
cp -r skills/{name}/* /tmp/skill-release-{name}/

# Remove internal-only files
rm -f /tmp/skill-release-{name}/WORKSPACE.md
rm -f /tmp/skill-release-{name}/.gitignore
rm -rf /tmp/skill-release-{name}/_meta.json
rm -rf /tmp/skill-release-{name}/.clawhub
```

**关键验证——在继续之前必须通过：**
```bash
# The release directory must contain ONLY skill files.
# If you see ANY of these, you copied from the wrong directory — STOP and fix:
#   - USER.md, MEMORY.md, AGENTS.md, SOUL.md (workspace/repo root files)
#   - audits/, shared/, scripts/ (repo directories)
#   - memory/, slides/, projects/ (personal data)
#   - .gitmodules (repo root)
ls /tmp/skill-release-{name}/
# Expected: SKILL.md, skill.yml, README.md, CHANGELOG.md, LICENSE, tests/, references/, scripts/
# If file count exceeds ~15 files, something is wrong. Verify source path.
```

如果缺少以下文件，请添加：
- `LICENSE`（默认使用MIT许可证）
- `README.md`（必须能够作为外部用户的GitHub页面）
- `.gitignore`

### 第5步：发布内容验证（严格检查）
```bash
bash scripts/validate-release-content.sh /tmp/skill-release-{name}
```
**这是一个确定性脚本，如果发布目录中包含仓库级别的文件（如USER.md、MEMORY.md、audit/等），或者文件数量过多（超过50个），或者包含可疑文件类型（如日志、图片、PDF等），则会阻止发布。**

必须返回成功的结果（退出代码0）。如果被阻止，说明复制的内容来自错误的目录。**请修复源目录并重新复制。**

### 第6步：深入进行OPSEC扫描
```bash
bash scripts/opsec-scan.sh /tmp/skill-release-{name}
```
必须返回成功的结果（退出代码0）。如果发现违规，请在发布副本中修复这些问题。不要修改`openclaw-knowledge`中的源代码——保持内部版本的原始状态。

### 第7步：代理程序审核
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

将文档保存到`openclaw-knowledge/reviews/{name}-release-review.md`

### 第8步：将内容推送到私有测试仓库
将清理后的内容推送到私有测试仓库，以便用户可以在任何设备（手机、笔记本电脑）上查看仓库：
```bash
cd /tmp/skill-release-{name}
git init
git config user.email "agent@localhost"
git config user.name "SkillEngineer"

# Install OPSEC pre-commit hook — prevents sensitive data from entering git history
cp /tmp/openclaw-knowledge/scripts/opsec-precommit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

git add .
git commit -m "v{version}: Initial release of {name}"
git remote add origin https://github.com/your-org/openclaw-skill-{name}.git
git branch -M main
git push -u origin main
```

### 第9步：用户审核
对于单个技能，发送审核链接。对于批量发布，收集所有第一阶段的结果并发送一条消息。

**单个技能：**
```
RELEASE REVIEW: {skill-name}

{score} | OPSEC: CLEAN
{1-line description}
https://github.com/your-org/openclaw-skill-{name}

Reply: approve / revise:{feedback} / reject
```

**批量审核（分配短ID以便于审批）：**
```
BATCH RELEASE REVIEW — {N} skills

A. {skill-name} — {score} | CLEAN | {1-line description}
https://github.com/your-org/openclaw-skill-{name}

B. {skill-name} — {score} | CLEAN | {1-line description}
https://github.com/your-org/openclaw-skill-{name}

C. {skill-name} — {score} | CLEAN | {1-line description}
https://github.com/your-org/openclaw-skill-{name}

Reply: approve all / approve A,C / revise B:{feedback}
```

**规则：**
- 链接单独显示（不要放在表格中——在手机上无法点击）
- 使用短ID（A、B、C）进行批量审批——用户无需输入完整的技能名称
- 仓库本身就是审核的对象。用户审核的是实际文件，而不是摘要。
- 等待用户的回复。未经明确批准不得继续下一步。

### 第10步：清除历史记录并切换为公开状态（用户批准后）
清除git历史记录（可能包含之前修订中的OPSEC修复内容），然后将仓库切换为公开状态：
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

# Verify repo metadata is OPSEC-clean (description, topics are now public)
gh repo view your-org/openclaw-skill-{name} --json description,repositoryTopics -q '.description + " " + (.repositoryTopics | join(" "))'
# Manually check output for org names, personal info, internal project names
# If dirty: gh repo edit your-org/openclaw-skill-{name} --description "{clean description}"
```

执行一次提交，清除历史记录，保持仓库的简洁性。避免使用双仓库结构。

### 第11步：准备发布包并请求批准
**向ClawhHub发布是一个不可逆的外部操作。在执行之前需要用户通过D-## ID进行明确批准。**

提取发布参数并记录批准请求——此时不要运行`clawhub publish`：

```bash
# Extract publish parameters directly from skill.yml
SLUG=$(grep '^name:' /tmp/skill-release-{name}/skill.yml | awk '{print $2}')
DISPLAY_NAME=$(grep '^display_name:' /tmp/skill-release-{name}/skill.yml | sed 's/display_name: *//' | tr -d '"')
VERSION=$(grep '^version:' /tmp/skill-release-{name}/skill.yml | awk '{print $2}')

echo "slug:         $SLUG"
echo "display_name: $DISPLAY_NAME"
echo "version:      $VERSION"

if [ -z "$SLUG" ] || [ -z "$DISPLAY_NAME" ] || [ -z "$VERSION" ]; then
  echo "ERROR: Missing slug, display_name, or version in skill.yml — fix before proceeding"
  exit 1
fi
```

如果`skill.yml`中缺少`display_name`，请现在添加（参见第1.5步）。

**然后在`ESCALATIONS.md`中添加一个待发布的条目：**
```
D-##: Publish {display_name} v{version} (slug: {slug}) to ClawhHub? — yes/no
```

**在此之前请等待My Lord回复“D-## 是”后再继续执行第11.5步。**

只有在My Lord明确批准了当前发布的技能后，才能继续执行第11.5步。

### 第11.5步：执行发布并验证（必须获得批准）
**只有在收到My Lord的明确批准后才能执行此步骤。**

```bash
clawhub publish /tmp/skill-release-{name} \
  --slug "$SLUG" \
  --name "$DISPLAY_NAME" \
  --version "$VERSION" \
  --changelog "{summary of changes from CHANGELOG.md}"
```

**发布后的验证——确认实际列表与`skill.yml`完全匹配：**

发布后，验证实际列表是否与`skill.yml`中的内容完全一致。
**此步骤用于检查标题错误、版本不匹配或元数据过时的问题。**

```bash
clawhub inspect "$SLUG" 2>&1
```

比较输出内容与`skill.yml`中的信息：

| 字段 | `skill.yml`中的预期值 | `clawhub inspect`中的实际值 | 是否匹配？ |
|-------|--------------------------|-------------------------------|--------|
| Display name | `display_name`的值 | `inspect`输出的第一行 | ✅ / ❌ |
| Version | `version`的值 | `Latest:`字段 | ✅ / ❌ |
| Description | `description`的第一句话 | `Summary:`字段（可能被截断） | ✅ / ❌ |
| Owner | 用户的ClawhHub用户名 | `Owner:`字段 | ✅ / ❌ |

**如果任何字段不匹配：**
1. 不要继续执行第12步
2. 查明不匹配的原因（可能是`--name`错误、`--slug`错误或`skill.yml`过时）
3. 修复源代码（`skill.yml`或发布命令），升级版本，然后重新发布
4. 重新执行第11.5步，直到所有字段都匹配
5. 只有当所有行的结果显示为✅时，才能继续执行第12步

**常见的不匹配情况及其解决方法：**

| 不匹配原因 | 解决方法 |
|----------|-------|-----|
| 显示名称错误 | `skill.yml`中缺少`display_name`；名称猜测错误 | 在`skill.yml`中添加`display_name`，然后重新发布 |
| 版本错误 | 发布前未更新`skill.yml`中的版本 | 在`skill.yml`中升级版本，然后重新发布 |
| Slug错误 | `skill.yml`中的`name`字段与预期的slug不符 | 修复`skill.yml`中的`name`字段或使用正确的`--slug` |
| 所有者错误 | 以错误的账户发布了技能 | 检查`clawhub whoami`，必要时重新认证 |

### 第12步：验证安全扫描（需要使用浏览器）
ClawhHub会自动使用VirusTotal（Code Insight）和OpenClaw自己的扫描工具来扫描所有发布的技能。**在扫描结果审核完成之前，发布过程视为未完成。**

**使用浏览器工具检查扫描结果——ClawhHub页面需要JS渲染：**

1. **使用浏览器打开技能详情页面：**
```
browser start (profile=openclaw)
browser navigate → https://clawhub.ai/{username}/{slug}
browser snapshot (refs=aria)
```

2. **找到“Security Scan”部分**：
   - **VirusTotal的判断结果：**良性 / 可疑 / 恶意 / 待处理
   - **OpenClaw的判断结果：**良性 / 可疑 / 恶意及置信度
   - **详细信息：**解释被标记的原因（展开“Details”查看详细信息）
   - **VirusTotal的报告链接：**直接链接到完整分析报告

3. **根据结果采取相应行动：**

| 判断结果 | 含义 | 应采取的措施 |
|---------|---------|--------|
| 良性（两者都为良性） | 清洁，自动批准 | 继续执行第13步 |
| 待处理 | 正在处理中 | 等待2分钟，重新生成快照 |
| 可疑（权限未声明） | 技能需要权限，但元数据中未声明 | 在`skill.yml`中添加`permissions`字段，升级版本，然后重新发布 |
| 可疑（其他原因） | 标记为可疑的行为 | 查看详细信息。如果是误报，请联系OpenClaw的安全团队。如果是真实问题，修复后重新发布 |
| 恶意 | 被阻止下载 | 立即修复，升级版本，然后重新执行第1.5步 |

4. **常见的修复措施——权限未声明：**
   如果检测到需要特权访问权限（如gh、clawhub、git、文件系统），在`skill.yml`中添加`permissions`字段：
   ```yaml
   permissions:
     - exec: git, gh CLI (repo creation, visibility changes)
     - exec: clawhub CLI (publishing)
     - filesystem: read/write skill directories
     - browser: verify scan results on ClawhHub
   ```
   然后升级版本并重新发布。这样可以明确权限需求并解决问题。

5. **如果VirusTotal的判断结果仍为待处理**，则继续执行第12步，但需要在报告中注明这一点。扫描结果是异步完成的。

### 第13步：交付
确认发布成功，并将所有链接和扫描结果发送给用户：
```
RELEASED: {skill-name} v{version}

GitHub: https://github.com/your-org/openclaw-skill-{name}
ClawhHub: https://clawhub.ai/{username}/{slug}
VirusTotal: {verdict} — {report link}
OpenClaw Scan: {verdict} ({confidence})

{1-line description}
```

**流程到此结束**

技能发布工具的功能到第13步（交付）为止。发布后的后续工作（如更新`STATUS.json`、转换子模块、记录日志等）属于**重构系统的职责**，不属于发布流程的职责。详情请参阅REFACTORY-SYSTEM.md中的“发布后阶段”。

## 错误处理

| 错误类型 | 原因 | 解决方法 |
|-------|-------|-----|
| 准备就绪检查失败 | 评分过低或存在OPSEC问题 | 先完成重构 |
| 发布副本中发现OPSEC违规 | 清理不完整 | 修复发布副本中的问题，重新扫描 |
| `gh repo create`失败 | 认证问题或仓库名称已被占用 | 检查`gh auth status`，尝试使用其他名称 |
| `clawhub publish`失败 | 未安装`clawhub` CLI或认证失败 | 运行`npm install -g clawhub`，重新认证 |
| 用户拒绝 | 收到用户反馈 | 根据反馈进行处理，从第4步重新开始 |

## 配置
无需持久化配置。该流程使用环境级别的工具（`gh`、`clawhub`、`git`），在使用前需要先进行认证。

**所需工具：**

| 工具 | 用途 | 检查内容 |
|------|---------|-------|
| `gh` CLI | 创建GitHub仓库、更改仓库可见性 | `gh auth status` |
| `clawhub` CLI | 向ClawhHub注册库发布 | `clawhub whoami` |
| `git` | 版本控制 | 内置工具 |
| `python3` | OPSEC扫描工具（可选） | `python3 --version` |

**流程脚本（位于`scripts/`目录中）：**

| 脚本 | 用途 |
|--------|---------|
| `validate-structure.sh` | 检查技能结构的完整性（8项检查） |
| `validate-release-content.sh` | 删除占位符文本和空文件 |
| `opsec-scan.sh` | 在公开发布前扫描敏感数据 |

**组织/用户名：**在流程步骤中，将`your-org`替换为你的GitHub用户名或组织名称。`clawhub`的`--slug`参数使用`skill.yml`中的`name`字段。**

**示例**

**发布特定技能：**
“将skill-engineer发布到ClawhHub”

**检查准备情况（无需立即发布）：**
“基于证据的调查功能是否准备好发布？”

**批量检查准备情况：**
“哪些技能已经准备好发布？”