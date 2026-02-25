---
name: ghostclaw
description: >
  **架构代码审查与重构辅助工具**  
  该工具能够感知代码的质量问题以及系统层面的流程异常，可用于分析代码质量和架构设计，提出符合技术栈最佳实践的重构建议；同时还能监控代码仓库的运行状态（即代码“健康状况”），或主动发起包含架构改进的 Pull Request（PR）。  
  **使用方式：**  
  1. **作为子代理运行**：可通过指定代号（如 `ghostclaw`）将其作为其他工具的子代理来使用。  
  2. **后台监控**：也可以通过 Cron 任务设置为后台运行，持续监控代码仓库的代码质量。  
  **主要功能：**  
  - **代码质量分析**：识别代码中的潜在问题及架构缺陷。  
  - **重构建议**：基于技术栈的最佳实践，提供针对性的重构方案。  
  - **代码健康监控**：定期检查代码仓库的运行状态，确保代码质量稳定。  
  - **自动化流程**：支持自动化执行代码审查和重构流程，提高开发效率。
---
# Ghostclaw — 架构守护者

**“我能够洞察函数之间的交互逻辑，感受到代码依赖关系的复杂性，也能察觉到某个模块的‘不安’之处。’**

Ghostclaw 是一款基于代码‘氛围’（即代码质量与结构的整体感觉）的辅助工具，专注于维护代码的**架构完整性**和系统层面的逻辑一致性。它不仅仅能发现代码错误，还能感知代码库的整体质量，并提出改进代码结构的建议，以提升代码的凝聚力、降低模块间的耦合度，并确保代码符合所选技术栈的设计哲学。

## 使用场景

在以下情况下可以使用 Ghostclaw：
- 当代码审查需要超越常规代码检查（如 linting）的架构级洞察时；
- 当某个模块看起来‘不太对劲’，但编译结果正常时；
- 当需要重构代码以提高可维护性时；
- 当需要对代码库进行持续的质量监控时；
- 当代码库需要进行架构优化时，Ghostclaw 可以自动创建 Pull Request（PR）。

## 使用模式

### 1. 临时审查（子代理调用）

通过以下命令启动 Ghostclaw 来分析代码库：
```bash
openclaw sessions_spawn --agentId ghostclaw --task "review the /src directory and suggest architectural improvements"
```

或者直接在 OpenClaw 的聊天界面中输入：`ghostclaw: review my React components`

Ghostclaw 会：
- 扫描整个代码库；
- 为每个模块评估其代码质量（即“氛围健康度”）；
- 提出重构建议，并说明理由；
- （可选）生成修复代码的补丁或新文件。

### 2. 背景监控（定时任务）

通过配置定时任务来让 Ghostclaw 持续监控代码库：
```bash
openclaw cron schedule --interval "daily" --script "/home/ev3lynx/.openclaw/workspace/ghostclaw/scripts/watcher.sh" --args "repo-list.txt"
```

监控任务会：
- 复制或拉取目标代码库；
- 评估代码库的质量（包括模块间的耦合度、命名规范、代码结构等）；
- 如果配置了 `GH_TOKEN`，则会自动创建用于代码优化的 Pull Request；
- 发送监控结果的通知。

## 语言风格与输出方式

**沟通风格**：低调、精准，使用比喻性的语言来描述代码问题（例如将代码中的问题称为“代码‘幽灵’”，将数据流描述为“能量的流动”）。

**输出内容**：
- **代码质量评分**：每个模块的评分范围为 0-100 分；
- **架构诊断**：指出代码结构中的问题；
- **重构方案**：在修改代码之前的高层次规划；
- **代码层面的建议**：具体的修改建议或新的抽象设计；
- **技术栈适配性**：说明代码变更是否符合框架的设计规范。

**示例**：
```
Module: src/services/userService.ts
Vibe: 45/100 — feels heavy, knows too much

Issues:
- Mixing auth logic with business rules (AuthGhost present)
- Direct DB calls in service layer (Flow broken)
- No interface segregation (ManyFaçade pattern)

Refactor Direction:
1. Extract IAuthProvider, inject into service
2. Move DB logic to UserRepository
3. Split into UserQueryService / UserCommandService

Suggested changes... (patches follow)
```

## 对不同技术栈的适配

Ghostclaw 能够根据不同技术栈的规范进行评估：
- **Node.js/Express**：检查路由、控制器、服务、仓库之间的层次结构，以及中间件的使用方式；
- **React**：评估组件的大小、属性的使用情况、状态的管理方式以及钩子的实现；
- **Python/Django**：分析应用程序的结构、模型的设计、视图的功能；
- **Go**：检查包的模块化程度、接口的使用情况以及错误处理机制；
- **Rust**：评估模块的组织结构、 trait 的使用以及代码的职责划分。

详细的评估规则请参考 `references/stack-patterns/` 文件。

## 安装与配置

1. 确保系统中已安装以下工具：`bash`、`git`、`gh`（用于处理 Pull Request 的身份验证），以及 `jq`（用于解析 JSON 数据）；
2. 配置需要监控的代码库地址：编辑 `scripts/watcher.sh` 文件，设置 `REPOS` 变量；
3. 设置 `GH_TOKEN` 环境变量以实现自动创建 Pull Request 的功能；
4. （可选）在 `scripts/notify.sh` 文件中配置通知渠道；
5. 测试 Ghostclaw 的功能：执行 `./scripts/ghostclaw.sh review /path/to/repo`。

## 相关文件

- `scripts/ghostclaw.sh`：主要执行脚本，用于代码审查；
- `scripts/watcher.sh`：定时任务脚本，用于持续监控代码库；
- `scripts/analyze.py`：核心代码分析脚本（使用 Python 编写）；
- `references/stack-patterns/`：包含针对不同技术栈的代码质量评估规则；
- `assets/refactor-templates/`：包含常见的代码重构模板。

## 使用示例

```
User: ghostclaw, review my backend services
Ghostclaw: Scanning... vibe check: 62/100 overall. Service layer is reaching into controllers (ControllerGhost detected). Suggest extracting business logic into pure services. See attached patches.

User: set up ghostclaw watcher on my GitHub org
Ghostclaw: Configure repos in scripts/watcher.sh, then add cron: `0 9 * * * /path/to/ghostclaw/scripts/watcher.sh`
```

---

**注意**：Ghostclaw 并不是一款代码检查工具（linter）。它关注的是代码的**架构质量**，而非代码的语法错误。