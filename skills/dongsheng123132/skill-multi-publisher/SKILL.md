---
name: skill-multi-publisher
version: 2.0.0
description: >
  **一键发布 Claude Code 技能到所有主要市场平台：**  
  GitHub（使用 `npx skills` 命令）、ClawHub，以及社区市场平台（如 composiohq/awesome-claude-skills、anthropics/skills、daymade/claude-code-skills、obra/superpowers-marketplace）。  
  该流程会验证 `SKILL.md` 文件的内容，自动生成缺失的文件，创建相应的仓库，完成技能的发布，并将相关更改提交到相应的社区目录中。
tags: ["skill", "publish", "github", "clawhub", "marketplace", "automation"]
metadata: {"openclaw":{"emoji":"🚀"}}
---
# 多平台技能发布工具

通过一个命令，即可将技能发布到所有主要的市场平台。

## 使用场景

当用户执行以下操作时：
- “发布这个技能”
- “将技能推送到所有平台”
- “在所有地方发布这个技能”
- “提交到awesome-claude-skills”

## 先决条件

- 已安装并登录 `gh` CLI（`gh auth status`）
- 已安装并登录 `clawhub` CLI（`clawhub whoami`）
- 技能目录中包含有效的 `SKILL.md` 文件，该文件应包含 YAML 格式的元数据（技能名称和描述）

## 支持的平台

| 平台 | 星级 | 发布方法 | 安装命令 |
|----------|-------|--------|-----------------|
| GitHub (npx skills) | - | `gh repo create` + `push` | `npx skills add user/repo` |
| ClawHub | - | `clawhub publish` | `clawhub install slug` |
| composiohq/awesome-claude-skills | 41K+ | 分支提交（Fork）+ 提交 Pull Request (PR) | `/plugin install` |
| anthropics/skills | 86K+ | 分支提交（Fork）+ 提交 Pull Request (PR) | `/plugin install` |
| daymade/claude-code-skills | 600+ | 分支提交（Fork）+ 提交 Pull Request (PR) | `/plugin install` |
| obra/superpowers-marketplace | 595 | 分支提交（Fork）+ 提交 Pull Request (PR) | `/plugin install` |
| anthropics/claude-plugins-official | 9.3K | 通过官方表单提交 | `/plugin install` |
| trailofbits/skills-curated | 252 | 分支提交（Fork）+ 提交 Pull Request (PR) | `/plugin install` |
| MadAppGang/claude-code | 242 | 分支提交（Fork）+ 提交 Pull Request (PR) | `/plugin install` |

## 发布流程

### 第一阶段：直接发布（自动化）

#### 第一步：验证格式

```bash
head -10 SKILL.md
```

所需格式：
```yaml
---
name: my-skill-name
version: 1.0.0
description: |
  What this skill does. At least 50 characters.
tags: ["tag1", "tag2"]
---
```

#### 第二步：自动生成缺失的文件

如果缺少以下文件，请生成：
- `LICENSE`（许可证文件，格式为 MIT，包含当前年份和 Git 用户名称）
- `README.md`（内容来自 `SKILL.md`，如果用户使用中文，则提供中文和英文版本）

#### 第三步：发布到 GitHub

```bash
cd <skill_dir>
git init
git add -A
git commit -m "Release: <skill-name> v<version>"
gh repo create <user>/<skill-name> --public --description "<desc>" --source . --push
```

#### 第四步：发布到 ClawHub

```bash
clawhub publish <skill_dir> \
  --slug <skill-name> \
  --name "<Display Name>" \
  --version <version> \
  --tags "<comma-separated-tags>" \
  --changelog "<changelog text>"
```

### 第二阶段：社区市场平台（提交 Pull Request）

#### 第五步：提交到 composiohq/awesome-claude-skills（41K 星级）

这是最大的技能发布平台，需通过 Pull Request 发布：

```bash
# Fork the repo
gh repo fork composiohq/awesome-claude-skills --clone=false

# Clone your fork
gh repo clone <user>/awesome-claude-skills /tmp/awesome-claude-skills
cd /tmp/awesome-claude-skills

# Create branch
git checkout -b add-<skill-name>

# Copy skill folder (only SKILL.md needed)
mkdir <skill-name>
cp <skill_dir>/SKILL.md <skill-name>/SKILL.md

# Commit and push
git add -A
git commit -m "Add <skill-name>: <short description>"
git push origin add-<skill-name>

# Create PR
gh pr create \
  --repo composiohq/awesome-claude-skills \
  --title "Add <skill-name>" \
  --body "$(cat <<'EOF'
## New Skill: <skill-name>

<description>

### What it does
<bullet points>

### Install
- npx skills add <user>/<skill-name>
- clawhub install <skill-name>

### Tested on
- Claude Code CLI
- OpenClaw
EOF
)"
```

#### 第六步：提交到 anthropics/skills（86K 星级）

这是 Anthropic 官方技能仓库：

```bash
gh repo fork anthropics/skills --clone=false
gh repo clone <user>/skills /tmp/anthropics-skills
cd /tmp/anthropics-skills

git checkout -b add-<skill-name>
mkdir -p skills/<skill-name>
cp <skill_dir>/SKILL.md skills/<skill-name>/SKILL.md
# Copy scripts if any
cp -r <skill_dir>/tools skills/<skill-name>/tools 2>/dev/null || true
cp -r <skill_dir>/scripts skills/<skill-name>/scripts 2>/dev/null || true

git add -A
git commit -m "Add <skill-name> skill"
git push origin add-<skill-name>

gh pr create \
  --repo anthropics/skills \
  --title "Add <skill-name> skill" \
  --body "$(cat <<'EOF'
## Summary
<description>

## Skill Structure
- SKILL.md with frontmatter (name, description, tags)
- tools/ or scripts/ directory

## Testing
Tested in Claude Code CLI.
EOF
)"
```

#### 第七步：提交到 daymade/claude-code-skills（623 星级，中文社区）

```bash
gh repo fork daymade/claude-code-skills --clone=false
gh repo clone <user>/claude-code-skills /tmp/daymade-skills
cd /tmp/daymade-skills

git checkout -b add-<skill-name>
mkdir <skill-name>
cp <skill_dir>/SKILL.md <skill-name>/SKILL.md
cp -r <skill_dir>/scripts <skill-name>/scripts 2>/dev/null || true
cp -r <skill_dir>/tools <skill-name>/tools 2>/dev/null || true
cp -r <skill_dir>/references <skill-name>/references 2>/dev/null || true

git add -A
git commit -m "Add <skill-name>"
git push origin add-<skill-name>

gh pr create \
  --repo daymade/claude-code-skills \
  --title "Add <skill-name>" \
  --body "$(cat <<'EOF'
## New Skill: <skill-name>

<description>

### Structure
- SKILL.md (with YAML frontmatter)
- tools/ or scripts/

### Also available at
- npx skills add <user>/<skill-name>
- clawhub install <skill-name>
EOF
)"
```

#### 第八步：提交到 obra/superpowers-marketplace（595 星级）

```bash
gh repo fork obra/superpowers-marketplace --clone=false
gh repo clone <user>/superpowers-marketplace /tmp/superpowers
cd /tmp/superpowers

git checkout -b add-<skill-name>
mkdir -p plugins/<skill-name>/skills/<skill-name>
cp <skill_dir>/SKILL.md plugins/<skill-name>/skills/<skill-name>/SKILL.md

# Create plugin.json
cat > plugins/<skill-name>/.claude-plugin/plugin.json <<PJSON
{
  "name": "<skill-name>",
  "description": "<description>",
  "version": "<version>"
}
PJSON

git add -A
git commit -m "Add <skill-name> plugin"
git push origin add-<skill-name>

gh pr create \
  --repo obra/superpowers-marketplace \
  --title "Add <skill-name>" \
  --body "<description>"
```

#### 第九步（可选）：提交到 anthropics/claude-plugins-official

仅适用于高质量的插件。请通过官方表单提交：
- 提交地址：https://clau.de/plugin-directory-submission
- 需要 Anthropic 团队审核
- 适用于成熟、经过充分测试的插件

### 第三阶段：报告发布结果

所有提交完成后，显示发布总结：

```
Published <skill-name> v<version>:

Direct publish:
  ✅ GitHub:   https://github.com/<user>/<skill-name>
  ✅ ClawHub:  clawhub install <skill-name>
  ✅ Install:  npx skills add <user>/<skill-name>

PR submitted:
  🔄 composiohq/awesome-claude-skills (41K stars) - PR #xxx
  🔄 anthropics/skills (86K stars) - PR #xxx
  🔄 daymade/claude-code-skills (623 stars) - PR #xxx
  🔄 obra/superpowers-marketplace (595 stars) - PR #xxx

Manual:
  📋 anthropics/claude-plugins-official - submit at clau.de/plugin-directory-submission
```

## 更新流程

对于已发布的技能：

```bash
# GitHub: commit + push
cd <skill_dir> && git add -A && git commit -m "Update: <changelog>" && git push

# ClawHub: re-publish with bumped version
clawhub publish <skill_dir> --slug <name> --version <new_version> --changelog "<text>"

# Community PRs: update existing PR or create new one
```

## 发布检查清单

- [ ] `SKILL.md` 文件包含 YAML 格式的元数据（技能名称、版本、描述）
- [ ] 描述内容至少 50 个字符
- [ ] 目录中不存在敏感信息（如 `.env` 文件或凭证）
- [ ] 存在包含安装说明的 `README.md` 文件
- [ ] 存在 `LICENSE` 文件
- [ ] 所有脚本均可执行（使用 `chmod +x` 命令使其可执行）

## 示例命令：
- “将这个技能发布到所有平台”
- “将技能推送到所有市场”
- “提交到 awesome-claude-skills”
- “在所有地方发布 v2.0.0 版本”