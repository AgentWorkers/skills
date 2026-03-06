---
name: buildwright
description: >
  **具有多代理架构的自主开发工作流程**  
  - **单代理模式**：适用于处理简单功能；  
  - **多代理模式**：可将跨域任务分解为专门的代理模块（如 UI、API、DB 等）。  
  - **支持的功能**：测试驱动开发（TDD）、安全扫描、代码审查以及质量控制流程（Quality Gates）。  
  - **兼容的工具**：Claude Code、OpenCode、OpenClaw 和 Cursor。
license: MIT
compatibility: Requires git and gh (GitHub CLI). GITHUB_TOKEN with repo scope needed for push/PR. Optional tools for security scans (semgrep, gitleaks, trufflehog). Works with Claude Code, OpenCode, OpenClaw, and Cursor.
metadata:
  homepage: https://github.com/raunakkathuria/buildwright
  version: "0.0.3"
  author: raunakkathuria
  tags:
    - development
    - workflow
    - tdd
    - security
    - code-review
    - autonomous
    - multi-agent
    - claw-architecture
  openclaw:
    requires:
      bins:
        - git
        - gh
      env:
        - GITHUB_TOKEN
    primaryEnv: GITHUB_TOKEN
---
# Buildwright

这是一个基于规范的自动化开发工具。人类负责审批开发计划，而代理则负责处理其余的所有工作。

## Buildwright 的功能

当 Buildwright 被激活后，它会指导代理执行以下操作：

1. 读取你的代码库和开发指导文档。
2. 编写一个单页的开发规范文档（文件路径：`docs/specs/[feature]/spec.md`）。
3. 请求人类审批——除非设置了 `BUILDWRIGHT_AUTO_APPROVE` 为 `true`。
4. 使用测试驱动开发（TDD）来实现该功能。
5. 运行代码质量检查（类型检查、代码格式检查、测试、构建）。
6. （如果安装了 `semgrep`、`gitleaks` 或 `trufflehog`，则）运行安全扫描。
7. 进行基于提示的代码审查（由“Staff Engineer”角色执行）。
8. 通过 `gh` 提交代码更改、推送代码，并创建 Pull Request（PR）。

## 所需条件

### 凭据（必需）

| 凭据 | 用途 | 权限范围 | 提供方式 |
|------------|---------|-------|----------------|
| `GITHUB_TOKEN` | 通过 `gh` 提交代码更改和创建 PR | `repo` 权限范围（读写） | 使用 `export GITHUB_TOKEN=ghp_...` 命令设置，或在 OpenClaw 的配置文件 `skills.entries.buildwright.apiKey` 中配置 |

该令牌必须具有 `repo` 权限范围，才能推送分支和创建 Pull Request。为了最小化权限需求，可以使用仅针对单个仓库的细粒度个人访问令牌，其权限设置为“读取和写入仓库内容”以及“读取和写入 Pull Request”。

**注意：** 即使你使用 SSH 进行 Git 推送，`GITHUB_TOKEN` 仍然是创建 PR 所必需的。你可以使用 `gh auth login` 命令单独登录 GitHub CLI。

### 必需的 binaries

| Binary | 用途 |
|--------|---------|
| `git` | 用于提交和推送代码 |
| `gh` | 用于通过 GitHub CLI 创建 PR |

### 可选工具

| Binary | 用途 |
|--------|---------|
| `semgrep` | 用于安全扫描（SAST） |
| `gitleaks` / `trufflehog` | 用于检测代码中的敏感信息 |

## 代理角色（基于提示，无需安装 binaries）

**Staff Engineer** 和 **Security Engineer** 是两个基于提示的角色，它们的指令存储在工作区的 `.buildwright/agents/` 文件中。这些角色不是外部工具或 binaries。代理会根据这些指令和预设的审查标准来审查开发规范和代码。这些文件仅包含提示指令和审查清单，不包含任何敏感信息或凭据。

## 配置选项

### BUILDWRIGHT_AUTO_APPROVE（可选，非凭据）

这是一个布尔值标志，用于控制代理在编写开发规范阶段是否需要等待人类审批。这个配置项**不是**敏感信息，也不会在 `requires.env` 文件中声明，因为它的存在并不是运行该工具的必要条件。

| 值 | 行为 |
|-------|---------|
| 未设置 | **交互式**（默认）——在构建之前会暂停并等待人类审批 |
| `false` | 交互式——与默认行为相同 |
| `true` | **自动化**——直接将开发规范提交到 Git（保留审计记录），然后继续执行后续步骤 |

**首次使用建议：** 在你熟悉工作流程之前，建议将 `BUILDWRIGHT_AUTO_APPROVE` 保持未设置的状态。可以先在沙箱仓库中以交互式模式使用该工具，观察其运行情况，然后再启用自动化提交和创建 PR 的功能。

## 命令

### /bw-new-feature \<description\>

用于新功能的完整开发流程。系统会自动识别项目是全新的（greenfield）还是已存在的（existing）。

**工作流程：**  
- 识别项目类型 → 进行需求分析 → 编写开发规范 → 由 Staff Engineer 验证 → 人类审批 → 使用 TDD 进行代码开发 → 进行质量检查 → 安全扫描 → 代码审查 → 提交 PR

**生成的文件：**  
- `docs/specs/[feature]/research.md`：代理在代码库中发现的详细信息  
- `docs/specs/[feature]/spec.md`：包含实现方案的开发规范文档

---

### /bw-claw \<feature\>

这是一个多代理协同工作的流程，采用 Claw 架构。架构师会将功能分解为具体的任务（如 UI、API、数据库相关任务），定义接口契约，并协调各个任务的执行。

**工作流程：**  
- 架构师进行分析 → 将功能分解为具体的任务 → 定义接口契约 → 各个任务分别执行（使用 TDD） → 架构师进行集成 → Buildwright 进行质量检查 → 提交 PR

**适用场景：** 适用于涉及多个开发领域的功能（例如需要数据库架构、API 接口和用户界面组件的功能）。

**生成的文件：**  
- `docs/specs/[feature]/claw-plan.md`：任务分解计划及接口契约  
- `docs/specs/[feature]/claw-[domain].md`：各任务的执行报告

---

### /bw-quick \<task\>

适用于快速修复 bug 或完成简单任务（耗时小于 2 小时）的快捷流程。该流程不需要编写开发规范或等待人类审批。

---

### /bw-ship \[message\]

适用于现有代码的标准化流程：包括质量检查、安全扫描和代码审查，最后提交 PR。

---

### /bw-verify

仅执行基本的代码检查：类型检查、代码格式检查、测试和构建。

---

### /bw-analyse

用于分析现有的代码库，并在 `.buildwright/codebase/` 目录下生成结构化的文档。该命令会在所有项目中首次执行，以便后续操作有清晰的背景信息。

**生成的文件：**  
- `STACK.md`、`ARCHITECTURE.md`、`CONVENTIONS.md`、`CONCERNS.md`，均存储在 `.buildwright/codebase/` 目录下。

---

### /bw-help

用于显示所有可用的命令。

---

## 失败处理机制

如果某个检查步骤在重试后仍然失败，代理会提交已完成的代码更改，然后推送代码并创建一个包含失败原因的 PR。该工具不会留下未处理的分支或隐藏失败信息。

## 重试策略

| 检查步骤 | 重试次数 | 失败原因 |
|------|---------|-----------|
| 类型检查、代码格式检查、测试、构建 | 2 次 | 问题可由代理自行解决 |
| 安全扫描 | 不进行重试 | 需要人类判断 |
| 代码审查 | 不进行重试 | 需要人类参与决策 |

## 安全注意事项

该工具会自动执行代码修改、提交更改和创建 Pull Request。在将此工具应用于包含敏感代码或生产环境的仓库之前，请确保你了解其工作原理。

**该工具会访问的内容：**  
- 你的仓库源代码  
- `.buildwright/agents/` 目录下的角色配置文件（仅包含提示指令，不含敏感信息）  
- `.buildwright/steering/` 目录下的配置文件  

**该工具会修改的内容：**  
- 位于 `docs/specs/` 目录下的开发规范文件  
- 代码库中的源代码更改  
- 通过 `gh` 提交的 Pull Request  

**该工具不会执行以下操作：**  
- 修改 `.env` 文件  
- 访问敏感信息存储  
- 执行破坏性的 Git 操作（如强制推送、重置仓库）  
- 合并未经审批的 PR  

**首次使用的推荐设置：**  
1. 从分支仓库或沙箱环境开始使用，避免在生产环境中直接应用该工具。  
2. 将 `BUILDWRIGHT_AUTO_APPROVE` 保持未设置的状态（交互式模式），以便在构建前先审查开发规范。  
3. 使用仅针对单个仓库的细粒度 GitHub 令牌，并确保权限最小化。  
4. 定期更换令牌，并在不再需要时及时撤销。  
5. 在合并代码之前，请务必审查所有生成的 PR——虽然该工具会创建 PR，但不会自动合并它们。  

## 更多信息

完整的文档、源代码和配置指南：https://github.com/raunakkathuria/buildwright