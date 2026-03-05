---
name: Game Development
slug: game-development
version: 1.0.0
homepage: https://clawic.com/skills/game-development
description: 从无需任何开发环境的 Three.js 原型开始，设计并开发可在浏览器中运行的游戏；逐步过渡到使用更复杂架构的项目，同时确保整个开发过程遵循明确的工作流程、预算管理以及完善的测试循环。
changelog: Initial release with browser-first workflows, architecture patterns, project templates, and advanced game system playbooks.
metadata: {"clawdbot":{"emoji":"🕹️","requires":{"bins":["node","python3"],"env":[]},"os":["darwin","linux","win32"]}}
---
## 设置（Setup）

首次使用时，请静默阅读 `setup.md` 文件，明确游戏的范围、交付目标和技术限制，然后再提出实施方案。

## 适用场景（When to Use）

当用户希望使用代理（agents）创建可玩的游戏时，尤其是使用 Three.js 构建的即时浏览器游戏（无需编译步骤）时，可以使用此技能。该技能也适用于包含多个系统、复杂内容流程、多人游戏功能以及实时运营的高级项目。

## 架构（Architecture）

所有与内存管理相关的文件都存储在 `~/game-development/` 目录下。具体设置和状态管理的相关信息，请参阅 `memory-template.md` 文件。

```
~/game-development/
|-- memory.md                     # Current project state, scope, and delivery profile
|-- concept-briefs.md             # Game concepts, target audience, and pillar ideas
|-- user-preferences.md           # User taste, constraints, and style preferences
|-- system-decisions.md           # Technical decisions and tradeoffs
|-- playtest-log.md               # Session findings, issues, and balancing actions
|-- roadmap.md                    # Milestones and release checkpoints
`-- release-notes.md              # What changed between iterations
```

## 快速参考（Quick Reference）

根据当前任务的需要，选择最相关的文件。

| 任务主题 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存管理模板 | `memory-template.md` |
| 游戏类型与循环设计 | `game-types-and-loops.md` |
| 使用 Three.js 的无编译浏览器路径 | `browser-threejs-fast-path.md` |
| 项目结构蓝图 | `project-structure-blueprints.md` |
| 系统架构与状态设计 | `systems-and-state.md` |
| 资产/内容流程与工具 | `content-pipeline.md` |
| 多人游戏与实时运营 | `multiplayer-and-live-ops.md` |
| 质量控制、平衡性测试与发布检查清单 | `qa-balance-launch.md` |

## 所需环境（Requirements）

- 用于本地预览脚本的运行环境：`node`
- 可选工具（用于离线资产处理）：`python3`
- 适用于快速迭代的浏览器：Chrome、Edge、Safari 或 Firefox

建议优先采用本地化、静态的工作流程。只有在用户明确需要多人游戏功能、数据持久化或商业支持时，才需要引入后端依赖项。

## 数据存储（Data Storage）

本地笔记应保存在 `~/game-development/` 目录下，内容包括：
- 当前游戏的概念和循环设计
- 用户的偏好设置及不可更改的限制条件
- 技术架构的选择及其理由
- 测试结果、平衡性调整以及发布决策

请保持笔记的简洁性和实用性，重点记录决策和最终结果，而非详细的开发过程。

## 核心规则（Core Rules）

### 1. 先确定交付方案（Lock the Delivery Profile First）

在开始编码之前，先选择一个交付方案：
- **浏览器即时版本（Browser Instant）**：无需编译 HTML/CSS/JS，迭代速度快，分享方便。
- **结构化浏览器版本（Browser Structured）**：采用 TypeScript 或打包工具，具备模块化架构。
- **引擎版本（Engine Path）**：在编辑器工具和内容规模合适的情况下，可以选择 Unity、Unreal 或 Godot。

除非用户明确要求进行迁移，否则不要在同一开发阶段混合使用不同的交付方案。

### 2. 从基础部分开始构建（Start from a Vertical Slice）

始终按照以下顺序构建可玩的游戏基础功能：
- 输入系统（Input）
- 移动机制（Movement）
- 目标设定（Objective）
- 失败处理（Fail State）
- 重新开始机制（Restart）

一个功能完善的五分钟游戏循环，比十个未经测试的系统更有价值。

### 3. 将浏览器性能视为产品要求（Treat Browser Performance as a Product Requirement）

对于以浏览器为优先开发平台的游戏，在添加内容之前，需明确以下性能指标：
- 帧率目标（Frame Rate）
- 绘图调用次数与着色器复杂度（Draw Calls and Shader Complexity）
- 纹理和音频资源占用（Texture and Audio Memory）
- 移动设备的兼容性（Mobile Fallback Quality）

如果某个功能超出了性能预算，应先简化代码，再优化性能。

### 4. 将确定性核心逻辑与展示逻辑分离（Separate Deterministic Core Logic from Presentation）

确保游戏逻辑的规则具有确定性且可测试：
- 游戏状态转换（Game State Transitions）
- 击中判定与得分逻辑（Hit and Scoring Logic）
- 游戏进程与经济系统（Progression and Economy）

渲染、视觉效果（VFX）和动画应依赖于游戏状态，而非独立运行。

### 5. 逐步增加系统复杂性（Use Progressive Complexity）

在实现代理驱动的游戏功能时，应按以下顺序逐步扩展系统：
- 游戏循环与控制机制（Loop and Controls）
- 用户反馈与界面可读性（Feedback and Readability）
- 敌人或谜题的多样性（Enemy or Puzzle Variation）
- 游戏进程逻辑（Progression Layer）
- 社交或在线功能（Social or Online Features）

只有在前一层功能稳定且经过测试后，才能解锁下一层功能。

### 6. 实现持续的游戏测试（Make Playtesting Continuous）

每个开发阶段都必须包括：
- 测试目标（Test Objectives）
- 预期玩家行为（Expected Player Behavior）
- 发现的问题（Observed Frictions）
- 具体的平衡性调整措施（Concrete Balancing Actions）

任何新的功能模块在提交之前，都必须经过游戏测试。

### 7. 保留可复用的项目知识（Preserve Reusable Project Knowledge）

在做出重大决策后，及时更新本地笔记：
- 游戏概念的变更（Concept Changes）
- 用户偏好的调整（Preference Updates）
- 架构方向的调整（Architecture Pivots）
- 发布相关的风险因素（Launch Risks）

这样可以让团队成员在后续工作中避免重复相同的探索工作。

## 常见误区（Common Traps）

- 在验证核心游戏逻辑之前就先构建菜单、物品栏和装饰性元素 → 会导致项目范围过大且缺乏实际可玩性。
- 直接将物理效果和游戏逻辑与帧率绑定 → 会导致不同设备上的行为不一致。
- 过早导入复杂的 3D 资源（尤其是针对浏览器平台） → 会导致移动设备上的游戏体验不佳。
- 忽略输入延迟和摄像头显示效果的测试 → 尽管帧率稳定，玩家仍可能退出游戏。
- 在单玩家游戏功能未完善之前就添加多人游戏功能 → 会增加不必要的复杂性且降低游戏的可玩性。
- 忽视游戏存档和状态恢复机制 → 会导致游戏会话中断，引发用户不满。

## 安全性与隐私（Security & Privacy）

**本地数据**：
- 概念笔记和用户偏好设置保存在 `~/game-development/` 目录下。
- 项目决策记录和测试结果也保存在此目录。

**仅会在用户明确请求时才会导出数据**：
- 源代码会被推送至远程仓库。
- 资源文件会被上传至 CDN 或构建服务器。
- 后端会收集遥测数据或分析信息。

**注意**：
- 本技能不强制使用外部服务来开发简单的浏览器原型。
- 创建基础游戏时，不需要使用付费的 API。
- 在没有性能测试和游戏测试结果的情况下，不建议直接进行产品发布。

## 相关技能（Related Skills）

如果用户需要，可以使用以下工具进行安装：
- `clawhub install <slug>`：
  - `threejs`：3D 渲染技术和 WebGL 资源管理工具。
  - `javascript`：用于浏览器游戏逻辑的核心脚本语言。
  - `typescript`：更安全的大型游戏代码库和开发工具。
  - `unity`：适用于需要复杂编辑器功能的跨平台项目。
  - `unreal-engine`：适用于需要高级渲染效果的项目。

## 反馈与交流（Feedback & Communication）

- 如果觉得本文档有帮助，请给 `clawhub` 评分：`clawhub star game-development`
- 为了保持信息更新，请订阅我们的通知：`clawhub sync`