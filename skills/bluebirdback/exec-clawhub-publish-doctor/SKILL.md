---
name: exec-clawhub-publish-doctor
description: "诊断并解决与 ClawHub 发布及 GitHub CLI 查询相关的工具故障（包括身份验证问题、浏览器登录错误、依赖项缺失、安全扫描结果未显示、配置文件/技能 URL 错误，以及 JSON 字段不匹配的问题，如“未知 JSON 字段”）。当使用 GitHub CLI 发布技能到 ClawHub 时遇到故障，或者需要检查报告中的临时错误时，或者由于字段结构差异导致 GitHub CLI 搜索命令失败时，可以使用此方法进行排查。"
---
# 执行 ClawHub 发布流程

通过预检、安全的发布命令以及发布后的验证机制来确保 ClawHub 的发布过程更加稳定，这些机制能够容忍注册表状态的临时变化。

## 快速工作流程

1. 运行预检：
   - `scripts/clawhub_preflight.sh`
2. 如果出现登录或浏览器相关的问题，请参考 `references/error-map.md`。
3. 使用具有重试功能的验证机制进行发布：
   - `scripts/clawhub_publish_safe.sh <skill_path> <slug> <name> <version> [changelog]`
4. 如果在 GitHub 搜索过程中遇到“未知 JSON 字段”等错误，请使用以下命令：
   - `scripts/gh_search_repos_safe.sh "<query>" [limit]`
5. 如果错误仍然存在，请先根据 `references/error-map.md` 进行分类，然后再寻求进一步帮助。

## 标准命令

### 预检
```bash
bash scripts/clawhub_preflight.sh
```

### 登录（基于令牌，无头模式，安全可靠）
```bash
clawhub login --token <clh_token>
clawhub whoami
```

### 安全发布
```bash
bash scripts/clawhub_publish_safe.sh ./my-skill my-skill "My Skill" 1.0.0 "Initial release"
```

### 手动检查
```bash
clawhub inspect my-skill --json
```

### 安全的 GitHub 仓库搜索（支持数据结构验证）
```bash
bash scripts/gh_search_repos_safe.sh "safe-exec skill" 15
```

## 规则

- 在服务器或无头环境中，建议使用令牌进行登录。
- 发布后出现的 `inspect` 错误可能属于暂时性问题，请在几分钟内继续观察。
- 通过 CLI (`clawhub inspect`) 和网页 URL (`/skills/<slug>` 进行双重验证。
- 对于 `gh search repos --json` 命令的失败情况，优先使用 `fullName` 而不是不支持的别名（如 `nameWithOwner`），或者使用 `scripts/gh_search_repos_safe.sh`。
- 使用规范的 URL 格式：
  - 技能页面：`https://clawhub.ai/skills/<slug>`
  - 所有者/技能名称页面：`https://clawhub.ai/<handle>/<slug>`
  - 用户个人资料页面（如果可用）：`https://clawhub.ai/users/<handle>`

## 资源

- `references/error-map.md`：用于快速诊断常见错误的原因。
- `scripts/clawhub_preflight.sh`：用于检查依赖项和环境配置。
- `scripts/clawhub_publish_safe.sh`：用于执行发布操作并包含重试机制的验证功能。
- `scripts/gh_search_repos_safe.sh`：用于执行 GitHub 仓库搜索的备用脚本，能够处理 JSON 字段不匹配的情况。