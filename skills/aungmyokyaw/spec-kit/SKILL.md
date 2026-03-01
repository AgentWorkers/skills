---
name: spec-kit
description: 使用 GitHub Spec Kit 进行规范驱动的开发（Spec-Driven Development）。通过 `/speckit.*` 命令来初始化项目、创建规范以及构建软件。该工具支持 Claude Code、GitHub Copilot、Gemini CLI 和 Codebuddy 等工具。
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "requires": { "bins": ["uv", "python3", "git"] },
      },
  }
---
# Spec Kit — 基于规范的驱动开发（Spec-Driven Development）

使用**基于规范的驱动开发**（Spec-Driven Development, SDD）更快地构建高质量软件。规范不再是单纯的文档，而是可以执行的代码，能够直接生成可运行的实现。

**官方网站：** https://github.github.com/spec-kit/  
**GitHub 仓库：** https://github.com/github/spec-kit

---

## 什么是基于规范的驱动开发？

SDD 打破了传统的软件开发模式：

| 传统开发 | 基于规范的开发 |
|-------------|-------------|
| 规范仅作为框架使用 → 最后被丢弃 | 规范是可执行的代码 → 直接生成代码 |
| 代码至高无上 | 设计意图至高无上 |
| 一次性输入需求 | 多步骤逐步细化 |
| 关注“如何实现” | 关注“要实现什么”以及“为什么实现” |

**核心理念：**
- 以设计意图为导向的开发方式
- 详细的规范，并配备相应的约束机制
- 重度依赖人工智能模型的能力
- 与具体技术无关的开发流程

---

## 先决条件

- **操作系统：** Linux、macOS、Windows（支持 PowerShell）
- **AI 辅助工具：** Claude Code、GitHub Copilot、Gemini CLI 或 Codebuddy CLI
- **包管理器：** [uv](https://docs.astral.sh/uv/)
- **Python：** 3.11 及以上版本
- **Git：** 任意最新版本

---

## 安装与设置

### 初始化新项目

```bash
# Create new project directory
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>

# Initialize in current directory
uvx --from git+https://github.com/github/spec-kit.git specify init .
uvx --from git+https://github.com/github/spec-kit.git specify init --here
```

### 指定 AI 辅助工具

```bash
# Proactively set AI agent during init
uvx --from git+https://github.com/github/spec-kit.git specify init <project> --ai claude
uvx --from git+https://github.com/github/spec-kit.git specify init <project> --ai gemini
uvx --from git+https://github.com/github/spec-kit.git specify init <project> --ai copilot
uvx --from git+https://github.com/github/spec-kit.git specify init <project> --ai codebuddy
```

### 脚本类型（Shell 或 PowerShell）

由操作系统自动选择，或手动指定：

```bash
# Force PowerShell (Windows)
uvx --from git+https://github.com/github/spec-kit.git specify init <project> --script ps

# Force POSIX shell (Linux/macOS)
uvx --from git+https://github.com/github/spec-kit.git specify init <project> --script sh
```

### 跳过工具检查

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <project> --ai claude --ignore-agent-tools
```

---

## 六步基于规范的驱动开发流程

### 第一步：初始化

运行 `specify init` 以创建项目结构及模板。

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init my-app --ai claude
```

**创建内容：**
- 包含配置的 `.speckit/` 目录
- 与辅助工具相关的模板
- Git 仓库结构

---

### 第二步：定义项目规范

为项目建立核心规则和原则。

**命令：**
```
/speckit.constitution This project follows a "Library-First" approach. 
All features must be implemented as standalone libraries first. 
We use TDD strictly. We prefer functional programming patterns.
```

**目的：** 设定所有规范必须遵循的约束机制和组织原则。

---

### 第三步：创建规范

描述你要开发的功能或系统，而不是具体的实现方式。

**命令：**
```
/speckit.specify Build an application that can help me organize my photos 
in separate photo albums. Albums are grouped by date and can be re-organized 
by dragging and dropping on the main page. Albums are never in other nested 
albums. Within each album, photos are previewed in a tile-like interface.
```

**最佳实践：**
- 专注于用户场景和行为
- 避免详细说明技术栈（由 AI 选择合适的技术）
- 用简单的语言描述用户界面/用户体验（UI/UX）
- 包括约束条件和业务规则

---

### 第四步：细化规范

识别并解决规范中的模糊之处。

**命令：**
```
/speckit.clarify Focus on security implications and edge cases
```

**功能：**
- 检测模糊或不明确的需求
- 提出澄清问题
- 建议具体的实现方案
- 根据澄清结果更新规范

---

### 第五步：制定实施计划

根据规范生成详细的实施计划。

**命令：**
```
/speckit.plan
```

**输出内容：**
- 系统架构决策
- 文件结构
- 实现步骤
- 测试策略
- 需要安装的依赖库

---

### 第六步：构建代码

执行实施计划。

**命令：**
```
/speckit.build
```

**特点：**
- 根据规范和计划生成代码
- 分阶段构建文件
- 按照计划执行测试
- 将开发进度提交到 Git

---

## 上下文感知：基于 Git 分支

Spec Kit 会根据你当前使用的 Git 分支自动识别正在开发的功能。

**命名规范：**
```
001-feature-name
002-user-authentication
003-photo-album-grid
```

**切换规范：**
```bash
git checkout 001-feature-name    # Work on feature 1
git checkout 002-user-auth       # Work on feature 2
```

**运行 Spec Kit 命令时，系统会自动加载相应的规范上下文。**

---

## 开发阶段

### 第一阶段：从零开始（Greenfield 阶段）
**重点：** 从零开始构建
- 从高层次需求出发
- 生成规范
- 制定实施计划
- 构建可投入生产的应用程序

### 第二阶段：创造性探索（Creative Exploration 阶段）
**重点：** 多样化实现方案
- 探索不同的技术栈
- 实验不同的用户界面/用户体验（UX）模式
- 比较不同的实现方法

### 第三阶段：迭代优化（Brownfield 阶段）
**重点：** 系统现代化
- 逐步添加新功能
- 优化现有系统
- 使用规范进行代码重构

---

## 所有命令参考

| 命令 | 功能 | 使用场景 |
|---------|---------|-------------|
| `/speckit.constitution` | 定义项目原则 | 项目开始时 |
| `/speckit.specify` | 创建新的规范 | 为每个新功能创建规范 |
| `/speckit.clarify` | 解决规范中的模糊之处 | 规范不明确时 |
| `/speckit.plan` | 制定实施计划 | 编码前 |
| `/speckit.build` | 执行实施 | 计划完成后 |

---

## 企业级应用特性

### 组织约束

- **云服务提供商：** 针对特定平台（如 AWS、Azure、GCP）
- **技术栈要求：** 使用批准的技术栈
- **系统设计：** 集成企业级 UI 库
- **合规性：** 遵守安全/监管要求

### 技术独立性

Spec Kit 支持：
- 任何编程语言
- 任何框架
- 任何架构模式
- 任何部署目标

---

## 本地开发（贡献者指南）

### 克隆并设置环境

```bash
git clone https://github.com/github/spec-kit.git
cd spec-kit
```

### 直接运行 CLI

```bash
# Fastest feedback - no install needed
python -m src.specify_cli --help
python -m src.specify_cli init demo-project --ai claude --script sh
```

### 可编辑的安装方式

```bash
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
uv pip install -e .
specify --help
```

### 从分支中执行测试

```bash
# Push branch first
git push origin your-feature-branch

# Test via uvx
uvx --from git+https://github.com/github/spec-kit.git@your-feature-branch \
  specify init demo-branch-test --script ps
```

---

## 最佳实践

### 规范编写指南

✅ **应该做：**
- 描述用户场景
- 包括业务规则
- 使用简单的语言
- 专注于功能行为，而非实现细节

❌ **不应该做：**
- 明确指定技术栈（让 AI 自动选择）
- 写实现细节
- 使用无上下文的行业术语
- 做出未明确说明的假设

### 规范编写示例（优秀/糟糕的例子）

```
/speckit.specify Build a task management app where:
- Users can create projects with color-coded labels
- Tasks have priorities (High/Medium/Low) with visual indicators
- Drag-and-drop to reorder tasks within a project
- Tasks can be assigned to multiple users
- Due dates trigger notifications 24h before
- Completed tasks archive automatically after 7 days
- Mobile-responsive with touch-friendly interactions
```  
```
/speckit.specify Build a React app with Redux for state management.
Use Material-UI for components. Store data in PostgreSQL.
```  

---

## 常见问题及解决方法

### 命令找不到

**问题：** AI 辅助工具无法识别 `/speckit.*` 命令  
**解决方法：** 在项目目录中重新运行 `specify init` 命令

### 加载了错误的规范上下文

**问题：** 使用了错误的规范  
**解决方法：** 使用 `git branch` 查看当前分支，并切换到正确的分支：`git checkout <branch>`

### 脚本类型冲突

**问题：** 在 macOS 上使用 PowerShell 脚本，或在 PowerShell 上使用错误的脚本类型  
**解决方法：** 明确指定脚本类型：`--script sh` 或 `--script ps`

### 缺少辅助工具

**问题：** Spec Kit 报告缺少必要的辅助工具  
**解决方法：** 在初始化时使用 `--ignore-agent-tools` 标志

---

## 工作流程示例

### 新功能开发流程

```bash
# 1. Create feature branch
git checkout -b 004-dark-mode

# 2. In AI agent chat:
/speckit.specify Add dark mode toggle to the application. 
System should detect OS preference but allow manual override. 
Store preference in localStorage.

# 3. Clarify ambiguities:
/speckit.clarify Focus on accessibility (WCAG contrast)

# 4. Generate plan:
/speckit.plan

# 5. Build:
/speckit.build

# 6. Commit and PR
git add .
git commit -m "feat: add dark mode toggle"
```

### 系统优化流程

```bash
# 1. Switch to existing feature
git checkout 002-user-auth

# 2. Enhance spec:
/speckit.specify Add OAuth2 login with Google and GitHub providers

# 3. Plan the enhancement:
/speckit.plan

# 4. Build iteratively:
/speckit.build
```

---

## 资源链接

- **官方文档：** https://github.github.com/spec-kit/
- **GitHub 仓库：** https://github.com/github/spec-kit
- **贡献指南：** https://github.com/github/spec-kit/blob/main/CONTRIBUTING.md
- **支持信息：** https://github.com/github/spec-kit/blob/main/SUPPORT.md

---

## 关键原则总结

1. **以设计意图为核心** — 专注于要实现的功能，而非实现方式
2. **规范是核心产出物** — 规范应被视为最重要的交付成果
3. **多步骤迭代** — 通过定义 → 制定规范 → 澄清需求 → 制定计划 → 构建代码的流程
4. **上下文感知** — 使用 Git 分支来管理开发内容的上下文
5. **技术无关性** — 该工具适用于任何技术栈和开发环境

---

**最后更新时间：2026-02-28**