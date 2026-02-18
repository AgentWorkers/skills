---
name: clawsec-clawhub-checker
version: 0.0.1
description: ClawHub信誉检查器，适用于ClawSec套件。该工具为受保护的技能安装程序（guarded skill installer）提供了VirusTotal Code Insight的信誉评分以及额外的安全检查功能。
homepage: https://clawsec.prompt.security
clawdis:
  emoji: "🛡️"
  requires:
    bins: [clawhub, curl, jq]
  depends_on: [clawsec-suite]
---
# ClawSec ClawHub 检查器

该工具通过集成 ClawHub 的信誉检查功能，增强了 ClawSec 安全套件的技能安装机制。在允许技能安装之前，它会先验证 VirusTotal Code Insight 的评分以及其他信誉指标，从而提供第二层安全保障。

## 功能概述

1. **拦截技能安装请求**：拦截所有的技能安装请求。
2. **验证 VirusTotal 信誉**：利用 ClawHub 内置的 VirusTotal Code Insight 功能来评估技能的信誉。
3. **双重确认**：对于信誉评分低于预设阈值的可疑技能，会要求用户再次确认是否继续安装。
4. **与安全建议系统集成**：与现有的 ClawSec 安全建议系统协同工作。
5. **提供详细报告**：明确显示技能被标记为可疑的原因。

## 安装说明

此工具必须**在**`clawsec-suite` 安装完成后**再进行安装：

```bash
# First install the suite
npx clawhub@latest install clawsec-suite

# Then install the checker
npx clawhub@latest install clawsec-clawhub-checker

# Run the setup script to integrate with clawsec-suite
node ~/.openclaw/skills/clawsec-clawhub-checker/scripts/setup_reputation_hook.mjs

# Restart OpenClaw gateway for changes to take effect
openclaw gateway restart
```

安装完成后，该检查器会将 `enhanced_guarded_install.mjs` 和 `guarded_skill_install_wrapper.mjs` 文件添加到 `clawsec-suite/scripts` 目录中，并更新相应的安全建议系统配置。原有的 `guarded_skill_install.mjs` 文件不会被替换。

## 工作原理

### 增强型安装流程

安装完成后，可以直接运行 `guarded_skill_install_wrapper.mjs` 或者直接执行增强后的安装脚本：
```bash
# Recommended drop-in wrapper
node scripts/guarded_skill_install_wrapper.mjs --skill some-skill --version 1.0.0

# Or call the enhanced script directly
node scripts/enhanced_guarded_install.mjs --skill some-skill --version 1.0.0
```

增强后的安装流程包括以下步骤：
1. **安全建议检查**：首先检查 ClawSec 的安全建议系统。
2. **信誉评估**：向 ClawHub 查询技能的 VirusTotal 评分。
3. **综合风险判断**：结合安全建议系统和信誉评估结果。
4. **双重确认**：如果评估结果提示风险，系统会要求用户明确确认是否继续安装。

### 检查的信誉指标

- **VirusTotal Code Insight**：检测恶意代码模式、外部依赖项（如 Docker 的使用、网络调用、`eval` 函数的调用、加密密钥等）。
- **技能的更新历史**：新发布的技能与已存在的技能进行对比。
- **作者信誉**：查看同一作者发布的其他技能的信誉情况。
- **下载统计信息**：分析技能的受欢迎程度等指标。

### 返回码

- `0`：安装安全（没有安全建议，信誉良好）。
- `42`：发现与现有安全建议系统中的警告匹配的情况。
- `43`：存在信誉风险（新发现的警告，需要用户确认是否继续安装）。
- `1`：安装过程中出现错误。

## 配置选项

环境变量：
- `CLAWHUB_REPUTATION_THRESHOLD`：最低信誉评分阈值（0-100，默认值：70）。

## 与现有安全系统的集成

该检查器仅对现有安全机制进行增强，不会替代它们：
- **安全建议系统仍然是主要的安全防线**：已知危险的技能仍会被立即阻止。
- **信誉评估作为补充**：对于未知或可疑的技能，会进行额外的审查。
- **双重确认机制保持不变**：无论哪种情况，都需要用户的明确授权才能继续安装。

## 使用示例

```bash
# Try to install a skill
node scripts/guarded_skill_install_wrapper.mjs --skill suspicious-skill --version 1.0.0

# Output might show:
# WARNING: Skill "suspicious-skill" has low reputation score (45/100)
# - Flagged by VirusTotal Code Insight: crypto keys, external APIs, eval usage
# - Author has no other published skills
# - Skill is less than 7 days old
# 
# To install despite reputation warning, run:
# node scripts/guarded_skill_install_wrapper.mjs --skill suspicious-skill --version 1.0.0 --confirm-reputation

# Install with confirmation
node scripts/guarded_skill_install_wrapper.mjs --skill suspicious-skill --version 1.0.0 --confirm-reputation
```

## 安全注意事项

- 该工具属于深度防御措施，不能替代现有的安全建议系统。
- VirusTotal 的评分结果基于启发式分析，可能存在误判。
- **可能存在误报**：某些具有新颖代码结构的合法技能也可能被标记为可疑。
- 在使用 `--confirm-reputation` 选项安装技能之前，请务必仔细审查技能的代码。

## 当前限制

- **缺少 OpenClaw 的内部检查数据**：ClawHub 在技能页面上会显示两个安全评分指标：
  - **VirusTotal Code Insight**：我们的检查器能够捕捉到这些评分信息。
  - **OpenClaw 内部检查**：该信息无法通过 API 获取（仅在 ClawHub 的网站上显示）。
  - 例如，在 `clawsec-suite` 的页面上，VirusTotal 可能显示“无害”，但 OpenClaw 内部检查可能会提示“该软件在内部检查中存在一些问题，建议在安装前进一步核实”。

**我们的检查器无法获取 OpenClaw 的内部检查结果，因为这些信息并未通过 `clawhub` 的 CLI 或 API 提供。**

### 对 ClawHub 的建议

为了实现全面的信誉评估，ClawHub 应该通过以下方式公开内部检查结果：
- 提供 `clawhub inspect --json` 端点来获取内部检查结果。
- 为安全工具提供额外的 API 接口。
- 或者将内部检查结果包含在 `clawhub install` 的警告信息中。

### 解决方案

虽然我们的启发式检查（技能的更新历史、作者信誉、下载量、更新情况等）能够提供类似的风险评估，但可能会遗漏一些关于安全漏洞（如绕过安全机制、缺少签名等问题）的详细信息。因此，请务必查看 ClawHub 的官方网站以获取最全面的安全评估信息。

## 开发说明

如需修改信誉评估逻辑，请编辑以下文件：
- `scripts/enhanced_guarded_install.mjs`：主要的增强型安装脚本。
- `scripts/check_clawhub_reputation.mjs`：负责执行信誉评估的逻辑。
- `hooks/clawsec-advisory-guardian/lib/reputation.mjs`：负责将信誉评估结果与安全建议系统集成。

## 许可证

MIT 许可证——该工具属于 ClawSec 安全套件的一部分。