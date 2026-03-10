---
name: skill-publisher
description: 端到端的工作流程，用于将技能发布到 GitHub、ClawdHub 以及 skills.sh。该流程包括仓库创建、主题标签设置、在 ClawdHub 上发布技能、向 skills.sh 提交索引请求以及安装验证等步骤。适用场景包括：“发布技能”（publish skill）、“将技能上架”（upload skill to ClawdHub）等操作。
version: 1.0.0
metadata:
  openclaw:
    emoji: "rocket"
    homepage: https://github.com/bryant24hao/skill-publisher
    os:
      - macos
      - linux
---
# 技能发布工具

这是一个用于代理技能的端到端发布工作流程，支持 GitHub、ClawdHub 和 skills.sh — 从预发布检查到安装验证的全过程。

## 语言

系统会使用用户调用该工具时所使用的语言进行响应；如果未检测到语言信息，则默认使用英语。

## 先决条件

```bash
command -v gh >/dev/null || echo "CRITICAL: gh (GitHub CLI) not found — install with: brew install gh"
command -v git >/dev/null || echo "CRITICAL: git not found"
```

（针对 ClawdHub 发布的额外要求：）
```bash
npx clawhub --help >/dev/null 2>&1 || echo "INFO: clawhub CLI not installed — needed for ClawdHub publishing"
```

## 工作流程概述

整个发布流程包含 6 个阶段：

```
1. Pre-flight Check    → Validate skill structure and content
2. GitHub Publish      → Create repo, push, add topics
3. ClawdHub Publish    → Publish to ClawdHub registry
4. skills.sh Submit    → Submit index request via GitHub issue
5. Install Verify      → Test all installation methods
6. Post-publish        → Summary with all links and install commands
```

请按顺序执行这些阶段。如果用户仅需要执行某个特定阶段（例如“仅提交到 skills.sh”），可以直接跳转到该阶段。

## 第 1 阶段：预发布检查

在发布之前，验证技能目录的内容。需要检查以下所有内容：

### 1.1 必需文件

```bash
SKILL_DIR="<path-to-skill>"  # Ask user or infer from context

# Required
[ -f "$SKILL_DIR/SKILL.md" ] || echo "FAIL: SKILL.md missing"
[ -f "$SKILL_DIR/LICENSE" ]  || echo "FAIL: LICENSE missing"
[ -f "$SKILL_DIR/README.md" ] || echo "FAIL: README.md missing"
```

### 1.2 SKILL.md 文件的元数据

读取 SKILL.md 文件，并确认其 YAML 元数据中包含以下内容：
- `name` — 必需字段，应使用驼峰式命名法（kebab-case）。
- `description` — 必需字段，需提供描述性信息（用于搜索引擎和技能发现）。
- `version` — 必需字段，必须是有效的半版本号（semver 格式）。

**可选但推荐的内容：**
- `metadata.openclaw.emoji`
- `metadata.openclaw.homepage`
- `metadata.openclaw.os`
- `metadata.openclaw.requires.bins`（所需 CLI 工具的列表）

### 1.3 README 文件的质量检查

检查 README.md 文件：
1. **徽章** — 至少需要包含许可证徽章；建议同时添加平台徽章。
2. **描述** — 用一句话清晰地说明该技能的功能。
3. **安装部分** — 应包含占位符形式的安装命令（发布后会被替换为实际命令）。
4. **无失效链接** — 检查链接是否指向不存在的仓库或占位符组织。
5. **无硬编码的用户路径** — 检查文件中是否包含 `/Users/xxx/` 或 `/home/xxx/` 等路径。
6. **保密信息** — 确保没有以明文形式存放 API 密钥、令牌或密码。

### 1.4 双语言 README 文件（可选）

如果该技能同时面向中文和英文用户，请检查：
- 是否存在 `README.zh-CN.md` 文件。
- 两个 README 文件的顶部是否都有语言切换链接。
- 两个文件的内容是否一致（包括章节和安装命令）。

### 1.5 检查结果报告

生成检查结果的报告：

```
# Pre-flight Report

## Required Files
- [x] SKILL.md
- [x] LICENSE (MIT)
- [x] README.md
- [ ] README.zh-CN.md (optional, not found)

## SKILL.md Frontmatter
- name: my-skill
- version: 1.0.0
- description: OK (127 chars)

## Issues Found
- WARNING: README contains placeholder org "nicepkg" — update before publishing
- INFO: No .gitignore found (optional but recommended)

## Ready to publish? YES / NO (with blockers listed)
```

## 第 2 阶段：在 GitHub 上发布

### 2.1 初始化 Git 仓库

```bash
cd "$SKILL_DIR"
git init
git add -A
git status  # Review staged files
```

**在提交之前**，检查暂存文件中是否包含以下内容：
- 保密信息（API 密钥、令牌、密码）
- 用户特定的绝对路径（如 `/Users/xxx/`）
- 大型二进制文件（大于 1MB）

```bash
git commit -m "Initial release: <skill-name> v<version>"
```

### 2.2 确定仓库名称

询问用户希望使用的 GitHub 仓库名称。默认名称为 SKILL.md 文件中 `name` 字段的值。

**重要提示**：在创建 GitHub 仓库之前，请先检查该名称是否已被 ClawdHub 占用，以确保名称的一致性：

```bash
npx clawhub inspect <proposed-name> 2>&1
```

如果名称已被占用，请建议其他可用名称，并让用户选择一个在两个平台上都适用的名字。

### 2.3 创建 GitHub 仓库

```bash
gh repo create <owner>/<repo-name> \
  --public \
  --description "<skill description from SKILL.md>" \
  --source . \
  --push
```

### 2.4 添加 GitHub 主题标签

为 skills.sh 的索引和技能的可见性添加相关主题标签：

```bash
gh repo edit <owner>/<repo-name> --add-topic agent-skill,claude-code-skill
```

根据技能内容，可以推荐以下主题标签：
- 类别标签：`productivity`（生产力）、`devtools`（开发工具）、`security`（安全）、`health-check`（健康检查）等。
- 平台标签：`macos`（MacOS）、`linux`（Linux）、`openclaw`（OpenClaw）。
- 技术标签：`eventkit`（事件处理框架）、`calendar`（日历）等。

### 2.5 更新相关文件中的引用

仓库创建完成后，需要更新所有引用该仓库的文件：
- `README.md` — 徽章链接、安装命令、Git 克隆地址。
- `README.zh-CN.md` — 同上。
- `SKILL.md` — `metadata.openclaw.homepage`（仓库主页链接）。
- `docs/` 目录下的用户指南或文档文件（如果有的话）。
- `LICENSE` 文件 — 显示版权持有者信息。

```bash
# Verify no stale references remain
grep -r "placeholder-org\|nicepkg\|example-user" "$SKILL_DIR" --include="*.md"
```

提交并推送更新内容。

## 第 3 阶段：在 ClawdHub 上发布

### 3.1 登录 ClawdHub

```bash
npx clawhub whoami 2>&1 || npx clawhub login
```

### 3.2 检查仓库名称的唯一性

```bash
npx clawhub inspect <slug> 2>&1
```

如果仓库名称已被占用，请根据技能名称推荐其他可用名称。

### 3.3 发布技能

```bash
npx clawhub publish "$SKILL_DIR" \
  --slug <slug> \
  --name "<display-name>" \
  --version <version> \
  --changelog "<changelog text>"
```

**已知问题（截至 clawhub CLI v0.7.0）**：服务器要求在发布请求中包含 `acceptLicenseTerms: true` 参数，但 CLI 当前不支持该参数。如果遇到此问题：

```
Error: Publish payload: acceptLicenseTerms: invalid value
```

请通过修补本地 CLI 来解决这个问题：

```bash
# Find the publish.js file
PUBLISH_JS="$(find ~/.npm/_npx -name 'publish.js' -path '*/clawhub/dist/cli/commands/*' 2>/dev/null | head -1)"

# Add acceptLicenseTerms to the payload
# In the JSON.stringify block, add: acceptLicenseTerms: true,
```

修复问题后，重新尝试发布操作。

### 3.4 验证发布结果

```bash
npx clawhub inspect <slug>
```

## 第 4 阶段：向 skills.sh 提交索引请求

skills.sh 并不会自动为技能创建索引。用户需要通过 GitHub 提交索引请求。

### 4.1 提交索引请求

```bash
gh issue create --repo vercel-labs/skills \
  --title "Request to index skill: <owner>/<repo>" \
  --body "$(cat <<'ISSUE_EOF'
## Skill Information

- **Repository:** https://github.com/<owner>/<repo>
- **Skill name:** <skill-name>
- **Install:** \`npx skills add <owner>/<repo>\`
- **License:** MIT

## Description

<2-3 sentence description of what the skill does and its key features>
ISSUE_EOF
)"
```

### 4.2 用户须知

向用户说明：
- 索引请求将由 vercel-labs/skills 团队审核。
- 处理时间可能较长。
- `npx skills add <owner>/<repo>` 命令可以立即执行（直接从 GitHub 克隆仓库）。
- 只有 `npx skills search` 或 `npx skills find` 命令需要索引功能。

## 第 5 阶段：安装验证

依次测试三种安装方法。在开始安装之前，请先备份现有的安装配置。

### 5.1 使用 skills.sh 安装技能

```bash
npx skills add <owner>/<repo> -g -y
# Verify: check installation path and file completeness
ls ~/.agents/skills/<skill-name>/ || ls ~/.claude/skills/<skill-name>/
# Cleanup
npx skills remove <skill-name> -g -y
```

### 5.2 使用 ClawdHub 安装技能

```bash
npx clawhub install <slug>
# Verify
ls ~/clawd/skills/<slug>/
# Cleanup
npx clawhub uninstall <slug> --yes
```

### 5.3 手动通过 Git 克隆仓库并安装技能

```bash
git clone https://github.com/<owner>/<repo>.git /tmp/test-skill-install
# Verify
ls /tmp/test-skill-install/
# Cleanup
rm -rf /tmp/test-skill-install
```

### 5.4 提交安装结果报告

```
# Installation Verification

| Method | Command | Result |
|--------|---------|--------|
| skills.sh | npx skills add <owner>/<repo> -g -y | OK / FAIL |
| ClawdHub | clawhub install <slug> | OK / FAIL |
| Manual | git clone ... | OK / FAIL |
```

## 第 6 阶段：发布后的总结

提供包含所有链接和安装命令的最终总结：

```
# Published: <skill-name> v<version>

## Links
- GitHub: https://github.com/<owner>/<repo>
- ClawdHub: https://clawhub.ai/<owner>/<slug> (if published)
- skills.sh: pending indexing (issue #NNN)

## Install Commands
# skills.sh (recommended)
npx skills add <owner>/<repo> -g -y

# ClawdHub
clawhub install <slug>

# Manual
git clone https://github.com/<owner>/<repo>.git ~/.claude/skills/<skill-name>

## Next Steps
- [ ] Wait for skills.sh indexing (issue #NNN)
- [ ] Share the GitHub link
- [ ] Consider creating a GitHub Release with tag v<version>
```

## 重要注意事项

- **仓库名称的一致性**：尽量在 GitHub 和 ClawdHub 上使用相同的仓库名称。如果 ClawdHub 上的名称已被占用，请重新命名 GitHub 仓库以保持一致性。
- **README 文件中的安装命令**：在确定最终的仓库名称和 ClawdHub 仓库名称后，请及时更新所有 README 文件中的安装命令。
- **双语文档**：如果技能有相关文档（如用户指南），请创建双语版本，并添加语言切换链接。英文文档应使用国际通用的示例平台（如 Telegram，而非 Feishu）。
- **提交前的隐私检查**：在每次推送代码之前，检查文件中是否包含真实的 IP 地址、API 密钥、WiFi 凭据、用户特定路径等敏感信息。
- **ClawdHub CLI 的已知问题**：从 CLI v0.7.0 开始，服务器要求在发布请求中包含 `acceptLicenseTerms: true` 参数。在应用补丁之前，请确认新版本是否解决了此问题。