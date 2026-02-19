---
name: skill-releaser
description: 通过完整的发布流程将技能发布到 ClawhHub：包括自动搭建开发环境、进行 OPSEC 安全性扫描、双重审核（代理审核 + 用户审核）、强制推送发布以及安全扫描验证。此流程适用于发布技能、准备技能发布、审核技能的发布状态或检查发布准备情况时使用。
version: 1.4.2
triggers:
  - release skill
  - publish skill
  - prepare for clawhub
  - release readiness
  - skill release review
  - publish to clawhub
---
# 技能发布工具

该工具负责协调从内部仓库到ClawhHub的整个技能发布流程。

## 使用场景

- 用户输入“发布{技能名称}”或“将{技能名称}发布到ClawhHub”
- 用户输入“准备发布{技能名称}”或“检查发布准备情况”
- 用户输入“审核{技能名称}以准备发布”
- 在重构流程中，通过Cron触发发布检查

## 前提条件

**OpenClaw与用户在发布过程中的交互方式：**
- 代理程序运行在具有shell访问权限的机器上，用于执行git和CLI操作
- 用户通过消息通道（如Telegram、Discord、Signal等）进行沟通（通常是在手机上）
- 用户直接在浏览器或手机上查看私有的GitHub仓库——仓库本身就是审核的对象，而不是文本摘要
- 用户通过回复代理程序的消息来批准或拒绝发布（使用自然语言，例如：“批准”、“修改：修复readme文件”、“拒绝”）
- 代理程序可以代表用户的已认证账户使用`gh` CLI创建和管理GitHub仓库
- 代理程序在请求用户审核之前，会先将内容推送到私有的测试仓库，以便有内容可供审核
- 未经用户明确批准，代理程序不会公开发布任何内容——这是一个严格的限制
- 仓库在发布前是私有的，用于测试和审核；发布时会通过孤儿分支和强制推送（单次干净的提交）清除历史记录，然后切换为公开状态
- 整个发布过程可能跨越多个会话——私有的测试仓库会保留状态，以便任何代理程序都可以继续执行
- 多个技能可以同时处于发布流程的不同阶段

## 先决条件

- 已使用`gh` CLI进行认证（用于创建仓库和更改可见性）
- 已安装`clawhub` CLI（用于将技能发布到ClawhHub）
- 存在一个至少包含`SKILL.md`文件的技能目录

## 范围与限制

**该工具负责：**完整的发布流程——包括结构搭建、OPSEC扫描、审核和发布。
**该工具不负责：**技能内容的创建或设计。`SKILL.md`文件必须已经描述了技能的功能。其他所有内容（模板文件、结构搭建等）都是该工具的工作范围。

用户只需提供一个完整的`SKILL.md`文件，该工具就可以处理从发布前的所有准备工作。

## 自动化模型

发布流程包含两个完全自动化的阶段，中间有一个人工审核环节。**无论是单个技能还是批量技能的发布，都遵循相同的模型。**

### 单个技能的发布流程
```
Phase 1 (AUTO): Steps 1-7 — scaffold, validate, stage, scan, review, push
     ↓
  GATE: User reviews private repo, replies "approve" / "revise" / "reject"
     ↓
Phase 2 (AUTO): Steps 9-12 — erase history, flip public, publish, verify scan, deliver
```

### 批量技能的发布流程
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
- 绝不串行处理发布请求——为每个技能启动一个子代理程序来执行第一阶段
- 不要因为一个技能的审核未通过而阻塞下一个阶段的开始
- 在批量审核消息中为每个技能分配一个唯一的短ID（A、B、C等）
- 收集所有第一阶段的结果，然后发送一条包含所有短ID的批量审核消息
- 接受批量审核结果：例如“全部批准”/“批准A、C”/“修改B：修复readme文件”
- 审核通过后，同时并行执行所有第二阶段的操作

**设计原则：**
- 用户只需输入“发布这些技能”，代理程序会并行执行所有第一阶段的操作。
- 代理程序发送一条包含所有审核链接和建议的消息，然后等待用户回复。
- 用户回复后，代理程序会并行执行所有第二阶段的操作。
- 代理程序发送一条包含所有结果的最终消息。
- 如果有任何步骤失败，代理程序会自动修复问题并继续执行；只有在无法修复的情况下才会通知用户。
- 速率限制、重试和延迟都会被默默处理（通过延迟和重试来处理，而不会显示提示信息）

**禁止的做法：**
- 不要串行处理发布请求——始终使用子代理程序并行执行
- 不要在开始处理一个技能的审核时阻塞另一个技能的发布
- 不要为每个技能发送单独的审核消息——统一发送批量审核消息
- 不要询问是否需要创建仓库——直接创建仓库
- 不要报告中间步骤的结果——只报告批量审核和最终发布的结果
- 不要询问关于速率限制或临时错误的信息——默默地处理重试

## 流程步骤

### 第1步：结构搭建（自动生成模板文件）
在任何质量检查之前，从现有的`SKILL.md`文件中生成所有缺失的结构文件：

**如果文件缺失，则自动生成：**

| 文件 | 来源 | 生成方法 |
|------|--------|-------------------|
| `skill.yml` | `SKILL.md`文件的前言部分 | 从`SKILL.md`中提取技能名称、描述、版本和触发条件 |
| `README.md` | `SKILL.md`中的描述和使用说明 | 为外部用户准备的GitHub页面内容：技能的功能、安装方法、未来计划。不是给代理程序的指令 |
| `CHANGELOG.md` | `skill.yml`中的版本信息 + git日志 | 格式为`## v{版本} — {日期}`，加上当前状态的总结 |
| `tests/test-triggers.json` | `SKILL.md`中的触发条件 | 从触发条件列表中判断是否应该触发检查，从禁止的触发条件列表中判断是否不应该触发检查 |
| `scripts/` | 创建目录 | 如果不需要脚本，则创建一个空目录或放置一个占位符`README.md` |
| `references/` | 创建目录 | 如果不需要引用资料，则创建一个空目录或放置一个占位符`README.md` |
| `LICENSE` | 默认使用MIT许可证 | 使用标准的MIT许可证文本 |
| `.gitignore` | 使用默认的`.gitignore`规则 | 包括`node_modules/`、`.DS_Store`、`.log`文件 |

**规则：**
- 绝不覆盖现有文件——只生成缺失的部分
- 所有生成的内容都来源于`SKILL.md`——不得添加额外的功能
- 如果`SKILL.md`中的信息不足，无法生成某个文件，则标记为内容缺失（用户需要先修复`SKILL.md`文件）
- 生成的`README.md`文件对于从未见过该技能的外部用户来说必须是可理解的

**搭建完成后进行验证：**
- 运行`scripts/validate-structure.sh`脚本——必须得到8分（满分8分）
- 如果得分低于8分，找出缺失的部分并进行修复

### 第1.5步：版本更新（仅限已有技能）
如果该技能之前已经发布过，在继续之前需要更新版本：

1. **检查当前已发布的版本：**
```bash
clawhub inspect {slug}
```

2. 在`skill.yml`和`SKILL.md`的前言部分更新版本号：
   - 小幅更新（例如1.0.0 → 1.0.1）：修复错误、修正拼写错误、更新文档
   - 中等程度的更新（例如1.0.0 → 1.1.0）：添加新功能、修改结构
   - 大幅更新（例如1.0.0 → 2.0.0）：引入重大变更、彻底重构

3. 在`CHANGELOG.md`中添加新的版本信息

4. 确保`skill.yml`中设置了`display_name`字段——这是显示在ClawhHub上的标题。
   这个字段必须明确设置；不能从slug字段推导出来或猜测。
   如果`display_name`字段缺失，请现在添加：
   ```yaml
   display_name: "Human Readable Title"  # Required — used as ClawhHub listing title
   ```
   规则：
   - 标题使用大写英文，避免使用专业术语
   - 描述技能的功能，而不是实现方式
   - 例如：slug为`autonomous-task-runner`时，`display_name`应为“Autonomous Task Runner”
   - 例如：slug为`skill-releaser`时，`display_name`应为“Skill Releaser”

首次发布时可以跳过此步骤（但仍需验证`display_name`字段是否存在）。

### 第2步：准备发布
验证技能目录是否完整：
- `SKILL.md`文件存在，并包含描述和使用说明
- `skill.yml`文件存在，并包含技能名称、描述和触发条件
- 结构评分达到8分（根据第1步的验证结果）
- 不存在明显的OPSEC违规行为（快速扫描）

如果任何检查失败，报告需要修复的问题。否则继续下一步。

### 第3步：创建私有测试仓库
```bash
# Check if repo already exists
gh repo view your-org/openclaw-skill-{name} 2>/dev/null

# If not, create it — CRITICAL: use the SANITIZED description, not the source skill.yml
# Run OPSEC scan on the description string BEFORE passing to gh repo create
gh repo create your-org/openclaw-skill-{name} --private --description "{sanitized description}"
```

**仓库元数据的OPSEC检查：**在仓库切换为公开状态时，传递给`gh repo create`的描述信息也会被公开。必须对该描述信息进行扫描，检查是否存在与文件内容相关的安全风险（如组织名称、个人信息、内部项目名称等）。这不能通过基于文件的扫描工具来完成——必须手动进行检查。

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

**关键验证步骤——在继续之前必须通过：**
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
- `LICENSE`文件（默认使用MIT许可证）
- `README.md`文件（必须能够作为外部用户的GitHub页面）
- `.gitignore`文件

### 第5步：发布内容验证（严格限制）
```bash
bash scripts/validate-release-content.sh /tmp/skill-release-{name}
```
**这是一个决定性步骤——如果发布目录中包含`USER.md`、`MEMORY.md`、`audits/`等文件，或者文件数量超过50个，或者包含可疑文件类型（如日志文件、图片、PDF文件），则阻止发布。**

必须返回成功的结果（退出代码为0）。如果失败，说明复制了错误的目录。**请修复源目录并重新复制内容。**

### 第6步：深度OPSEC扫描
```bash
bash scripts/opsec-scan.sh /tmp/skill-release-{name}
```
必须返回成功的结果（退出代码为0）。如果发现违规行为，请在发布副本中修复这些问题。不要修改`openclaw-knowledge`中的源代码——保持内部版本的原始状态。

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

将审核文档保存到`openclaw-knowledge/reviews/{name}-release-review.md`文件中

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
对于单个技能，发送审核链接。对于批量发布，收集所有第一阶段的结果并发送一条审核消息。

**单个技能的审核：**
```
RELEASE REVIEW: {skill-name}

{score} | OPSEC: CLEAN
{1-line description}
https://github.com/your-org/openclaw-skill-{name}

Reply: approve / revise:{feedback} / reject
```

**批量审核（为便于审核分配短ID）：**
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
- 链接应单独显示（不要放在表格中——在手机上无法点击）
- 为批量审核分配短ID（A、B、C等）——用户无需输入完整的技能名称
- 仓库本身就是审核的对象。用户需要审核实际的文件，而不是摘要
- 等待用户的回复。未经明确批准不得继续下一步。

### 第10步：清除历史记录并切换为公开状态（用户审核通过后）
清除git历史记录（可能包含之前修订中的OPSEC修复内容），然后将仓库设置为公开状态：
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

执行单次提交，清除历史记录，保持仓库的简洁性。避免使用双仓库结构。

### 第11步：发布到ClawhHub
在运行发布命令之前，从`skill.yml`文件中提取所有必要的参数——切勿猜测或硬编码：
```bash
# Extract publish parameters directly from skill.yml
SLUG=$(grep '^name:' /tmp/skill-release-{name}/skill.yml | awk '{print $2}')
DISPLAY_NAME=$(grep '^display_name:' /tmp/skill-release-{name}/skill.yml | sed 's/display_name: *//' | tr -d '"')
VERSION=$(grep '^version:' /tmp/skill-release-{name}/skill.yml | awk '{print $2}')

echo "slug:         $SLUG"
echo "display_name: $DISPLAY_NAME"
echo "version:      $VERSION"

# Verify all three are non-empty before proceeding
if [ -z "$SLUG" ] || [ -z "$DISPLAY_NAME" ] || [ -z "$VERSION" ]; then
  echo "ERROR: Missing slug, display_name, or version in skill.yml — fix before publishing"
  exit 1
fi
```

如果`skill.yml`文件中缺少`display_name`字段，请现在添加（参见第1.5步）。如果`display_name`字段为空，则不能继续发布。

```bash
clawhub publish /tmp/skill-release-{name} \
  --slug "$SLUG" \
  --name "$DISPLAY_NAME" \
  --version "$VERSION" \
  --changelog "{summary of changes from CHANGELOG.md}"
```

### 第11.5步：发布后的验证
发布完成后，验证实际发布的技能信息是否与`skill.yml`文件中的信息完全一致。
**此步骤用于检查标题错误、版本号不匹配或元数据过时的情况。**

```bash
clawhub inspect "$SLUG" 2>&1
```

比较`skill.yml`文件和发布后的信息：

| 字段 | `skill.yml`中的预期值 | `clawhub`中的实际值 | 是否匹配？ |
|-------|--------------------------|-------------------------------|--------|
| Display name | `display_name`字段的值 | `inspect`工具输出的第一个字段 | ✅ / ❌ |
| Version | `version`字段的值 | `Latest:`字段 | ✅ / ❌ |
| Description | `description`字段的第一句话 | `Summary:`字段 | ✅ / ❌ |
| Owner | 用户在ClawhHub上的用户名 | `Owner:`字段 | ✅ / ❌ |

**如果任何字段不匹配：**
1. 不得继续执行第12步
2. 查明不匹配的原因（可能是`--name`字段错误、`--slug`字段错误或`skill.yml`文件过时）
3. 修复源文件（`skill.yml`或发布命令），更新版本号，然后重新发布
4. 重新执行第11.5步，直到所有字段都匹配
5. 只有当所有字段都匹配时，才能继续执行第12步

**常见的不匹配情况及修复方法：**

| 不匹配原因 | 修复方法 |
|----------|-------|-----|
| `display_name`错误 | `skill.yml`文件中缺少`display_name`字段；名称猜测错误 | 在`skill.yml`文件中添加`display_name`字段，然后重新发布 |
| 版本号错误 | 发布前未更新`skill.yml`文件中的版本号 | 更新`skill.yml`文件中的版本号，然后重新发布 |
| `slug`错误 | `skill.yml`文件中的`name`字段与实际使用的`slug`字段不匹配 | 修复`skill.yml`文件中的`name`字段或使用正确的`--slug`字段 |
| 所有者错误 | 使用错误的账户发布技能 | 检查`clawhub whoami`信息，必要时重新认证 |

### 第12步：验证安全扫描结果（需要浏览器）
ClawhHub会自动使用VirusTotal（Code Insight）和OpenClaw自己的扫描工具对所有发布的技能进行安全扫描。**在扫描结果审核完成之前，发布过程视为未完成。**

**使用浏览器查看扫描结果：**
1. **使用浏览器打开技能详情页面：**
```
browser start (profile=openclaw)
browser navigate → https://clawhub.ai/{username}/{slug}
browser snapshot (refs=aria)
```

2. **找到“Security Scan”部分**：
   - **VirusTotal的判断结果：** 无害 / 可疑 / 恶意 / 待处理
   - **OpenClaw的判断结果：** 无害 / 可疑 / 恶意（附带置信度等级）
   - **详细信息：** 显示被标记的原因（展开“Details”部分可查看详细信息）
   - **VirusTotal的报告链接：** 提供完整分析的直接链接

3. **根据结果采取相应行动：**

| 判断结果 | 含义 | 应采取的行动 |
|---------|---------|--------|
| 无害（两种情况） | 安全，自动批准 | 继续执行第13步 |
| 待处理 | 扫描仍在进行中 | 等待2分钟后重新扫描 |
| 可疑（权限问题） | 技能需要额外的权限，但这些权限未在元数据中声明 | 在`skill.yml`文件中添加`permissions`字段，更新版本号，然后重新发布 |
| 可疑（其他问题） | 报告的权限问题 | 查看详细信息。如果是误报，联系OpenClaw的安全团队；如果是真实问题，修复问题后重新发布 |
| 恶意 | 被阻止下载 | 立即修复问题，更新版本号，然后重新执行第1.5步 |

4. **常见的修复措施——权限问题：**
   如果检测到需要额外权限（如`gh`、`clawhub`、`git`、文件系统的权限），在`skill.yml`文件中添加`permissions`字段：
   ```yaml
   permissions:
     - exec: git, gh CLI (repo creation, visibility changes)
     - exec: clawhub CLI (publishing)
     - filesystem: read/write skill directories
     - browser: verify scan results on ClawhHub
   ```
   然后更新版本号并重新发布。这样可以明确权限要求并解决问题。

5. **如果VirusTotal的扫描结果仍为“待处理”，则继续执行第12步，但在报告中注明这一点。扫描结果是异步完成的。**

### 第13步：交付结果
确认发布成功后，将所有链接和扫描结果发送给用户：
```
RELEASED: {skill-name} v{version}

GitHub: https://github.com/your-org/openclaw-skill-{name}
ClawhHub: https://clawhub.ai/{username}/{slug}
VirusTotal: {verdict} — {report link}
OpenClaw Scan: {verdict} ({confidence})

{1-line description}
```

**流程在此结束**

技能发布工具的功能到第13步（结果交付）为止。发布后的后续工作（如更新`STATUS.json`文件、转换子模块、记录日志等）属于**重构系统的职责**，而非发布流程的职责。详情请参阅`REFACTORY-SYSTEM.md`中的“发布后阶段”部分。

## 错误处理

| 错误类型 | 原因 | 修复方法 |
|-------|-------|-----|
| 准备阶段检查失败 | 评分过低或存在OPSEC问题 | 先完成重构 |
| 发布副本存在安全问题 | 清理不完整 | 修复发布副本中的问题，然后重新扫描 |
| `gh repo create`失败 | 认证问题或仓库名称已被占用 | 检查`gh auth status`，尝试使用其他名称 |
| `clawhub publish`失败 | 未安装`clawhub` CLI或认证失败 | 运行`npm install -g clawhub`并重新认证 |
| 用户拒绝发布 | 收到用户反馈 | 根据反馈进行处理，然后从第4步重新开始 |

## 配置要求

无需持久化的配置。该流程使用环境级别的工具（`gh`、`clawhub`、`git`），这些工具在使用前需要先进行认证。

**所需工具：**

| 工具 | 用途 | 需要检查的内容 |
|------|---------|-------|
| `gh` CLI | 创建GitHub仓库、更改仓库可见性 | 检查`gh auth status` |
| `clawhub` CLI | 将技能发布到ClawhHub注册表 | 检查`clawhub whoami` |
| `git` | 版本控制 | 内置工具 |
| `python3` | OPSEC扫描工具（可选） | 检查`python3 --version` |

**流程中的脚本（位于`scripts/`目录下）：**

| 脚本 | 用途 |
|--------|---------|
| `validate-structure.sh` | 检查技能结构的完整性（8项检查） |
| `validate-release-content.sh` | 删除占位符文本和空文件 |
| `opsec-scan.sh` | 在发布前扫描敏感数据 |

**组织/用户名：** 在流程步骤中，请将`your-org`替换为你的GitHub用户名或组织名称。`clawhub`命令中的`--slug`参数使用`skill.yml`文件中的`name`字段。**

**示例**

**发布特定技能：**
“将`skill-engineer`技能发布到ClawhHub”

**检查发布准备情况（不进行实际发布）：**
“`evidence-based-investigation`技能是否准备好发布？”

**批量技能的发布准备情况检查：**
“哪些技能已经准备好发布？”