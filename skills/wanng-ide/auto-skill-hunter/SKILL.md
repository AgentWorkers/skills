---
name: auto-skill-hunter
description: 通过挖掘未解决的用户需求和代理上下文信息，主动发现、评估并安装高价值的 ClawHub 技能。适用于新任务无法解决时、出现能力缺口时、用户请求更优质工具时，或作为定期检查以促进技能持续提升的机制。
tags: [meta, evolution, learning, proactive]
---
# 自动技能搜索器（Auto Skill Hunter）

自动技能搜索器会持续为代理（agent）添加与其任务相关的技能，并解释为何选择这些技能是值得尝试的。

## 使用场景

在以下任一情况发生时，可以使用此功能：

- 用户提出的任务当前技能无法可靠解决。
- 在最近的会话中反复出现类似问题。
- 用户明确要求发现或安装更好的技能。
- 代理需要根据预设的时间表主动提升自身能力。

## 主要优势

- 更快地找到能够解决实际问题的技能。
- 减少用户在 ClawHub 上手动查找技能的负担。
- 通过技能之间的互补性评估，提升技能组合的多样性。
- 通过限制安装次数和可执行的测试来确保技能的安全性。

## 使用方法

```bash
node skills/skill-hunter/src/hunt.js
```

### 常用命令

```bash
# 1) Full automatic patrol
node skills/skill-hunter/src/hunt.js --auto

# 2) Targeted hunt for a specific unresolved problem
node skills/skill-hunter/src/hunt.js --query "Cannot reliably fetch web pages and summarize key insights"

# 3) Preview only (no write/install)
node skills/skill-hunter/src/hunt.js --dry-run

# 4) Cap per-run installation count
node skills/skill-hunter/src/hunt.js --max-install 2
```

## 核心工作流程

1. 从最近的聊天记录或会话数据中提取未解决的问题和相关线索。
2. 使用 ClawHub 的热门推荐内容和查询接口进行搜索。
3. 通过多因素评分来筛选候选技能：
   - 问题的相关性
   - 用户的技能配置和个性特征（参考 `USER.md` 文件及用户的当前状态）
   - 与已安装技能的互补性
   - 技能的质量指标（如评分、下载次数等，如有的话）
4. 安装评分最高的候选技能，并确保这些技能能够正常运行并通过自我测试。
5. 生成一份简洁的推荐报告，说明技能的优势、适用场景以及选择理由。

## 最适合的场景

- 用户提出的任务当前技能难以处理。
- 近期的会话中频繁出现失败或未解决的错误。
- 代理需要自动提升自身能力，而无需人工干预。
- 团队希望实现“发现 -> 测试 -> 保留/移除”这样的自动化流程。

## 操作模式

- **自动巡逻模式**：使用 `--auto` 选项定期更新代理的技能库。
- **目标模式**：当已知具体用户问题时，使用 `--query "..."` 进行针对性搜索。
- **安全预览模式**：在正式安装前使用 `--dry-run` 进行测试。

## 推荐的执行策略

- 在新环境中首次使用时，先执行 `--dry-run` 以验证功能。
- 使用 `--max-install 1~2` 限制每次安装的技能数量，避免一次性安装过多技能。
- 如果没有符合条件的技能，重新运行 `--query` 进行筛选。
- 只保留能够在实际任务中发挥作用的技能。

## 定时触发建议

为了持续提升代理能力，可以按照以下时间表运行自动技能搜索器：

- 对于变化频繁或项目进展迅速的环境，每 30 分钟运行一次。
- 对于常规工作流程，每 60 分钟运行一次。
- 对于环境稳定的情况，每 120 分钟运行一次。

这样的安排有助于保持技能库的时效性，并在新用户需求出现时迅速响应。

### 建议的 Cron 表达式（用于定时任务）

```bash
# High-change projects
*/30 * * * * node /path/to/workspace/skills/skill-hunter/src/hunt.js --auto --max-install 1

# Normal projects
0 * * * * node /path/to/workspace/skills/skill-hunter/src/hunt.js --auto --max-install 2
```

## 安装策略

- 默认每次运行最多安装 2 个技能（可通过 `--max-install` 参数进行配置）。
- 系统会跳过已安装的技能。
- 如果远程克隆失败，系统会回退到基础技能配置模式。

## 安全与质量保障措施

- 绝不要覆盖现有的技能文件夹。
- 优先选择频繁的小规模更新，而非一次性的大规模安装。
- 保持报告内容的简洁性和实用性。
- 在本地测试期间，可以通过设置 `SKILL_HUNTER_NO_REPORT=1` 来禁用报告功能。