---
name: pattern-extraction
model: reasoning
description: 从代码库中提取设计系统、架构模式和方法论，并将其转化为可重用的技能和文档。这些资源可用于分析项目以识别其中的模式，从现有代码中创建新的技能，提取设计元素，或记录项目的构建过程。相关操作包括：“提取模式”、“从这个代码库中提取信息”、“分析这个代码库”、“从这个项目中创建技能”以及“提取设计系统”。
---

# 模式提取

从现有代码库中提取可重用的模式、技能和方法论文档。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install extraction
```


---

## 开始前

**必读**：根据您要提取的内容，阅读以下参考文件：

| 提取内容 | 首先阅读 |
|------------|------------|
| 任何类型的提取 | [`methodology-values.md`](references/methodology-values.md) — 优先级顺序及需要关注的内容 |
| 特定类别 | [`extraction-categories.md`](references/extraction-categories.md) — 每个类别的详细模式 |
| 生成技能文档 | [`skill-quality-criteria.md`](references/skill-quality-criteria.md) — 质量检查标准 |

---

## 提取过程

### 第一阶段：发现

分析项目以了解其结构。

**扫描项目结构：**
```
- Root directory layout
- Key config files (package.json, tailwind.config.*, etc.)
- Documentation (README, docs/, etc.)
- Source organization (src/, app/, components/, etc.)
```

**识别技术栈：**
| 指标 | 技术 |
|-----------|------------|
| 包含 React 的 `package.json` | React |
| `tailwind.config.*` | Tailwind CSS |
| `components.json` | shadcn/ui |
| `go.mod` | Go |
| `Dockerfile` | Docker |
| `k8s/` 或 `.yaml` 配置文件 | Kubernetes |
| `turbo.json` | Turborepo |
| `Makefile` | Make 自动化脚本 |

**查找设计系统的线索：**
- 自定义的 Tailwind 配置（非默认设置）
- CSS 变量/自定义属性
- 主题文件
- 设计文档
- 情感板或参考列表

**记录关键发现：**
- 项目使用的技术栈是什么？
- 文件夹结构是怎样的？
- 是否有明确的设计方向？
- 存在哪些工作流程（如 Makefile、脚本）？

---

### 第二阶段：分类

将发现的内容按照优先级归类到相应的提取类别中：

**优先级顺序：**
1. **设计系统** — 颜色代码、排版、间距、动画效果、设计文档
2. **UI 模式** — 组件组织结构、布局、交互方式
3. **架构** — 文件夹结构、数据流、API 模式
4. **工作流程** — 构建、开发、部署、持续集成/持续部署（CI/CD）
5. **特定领域** — 仅适用于该应用程序类型的模式

**对于每个找到的类别，记录以下信息：**
- 存在哪些具体的模式？
- 它们定义在哪些文件中？
- 是否有文档记录？
- 它们是否有价值被提取？（是否在多个地方被使用，设计是否合理？）

**根据价值进行筛选：**
| 是否值得提取 | 是否应跳过 |
|----------------|----------------|
| 在多个组件中使用的模式 | 一次性解决方案 |
| 有明确目的的定制配置 | 默认配置 |
| 有文档记录的设计决策 | 随意的选择 |
| 可重用的基础设施 | 项目特定的技巧 |

---

### 第三阶段：提取

对于每个有价值的模式，生成相应的输出文件。

**设计系统 → 设计系统文档 + 技能文档**

1. 阅读 Tailwind 配置文件、CSS 文件和主题文件
2. 提取实际的代码值（颜色、字体、间距等）
3. 记录设计方向
4. 使用 [`design-system.md`](references/output-templates/design-system.md) 模板创建文档：
   - `docs/extracted/[项目]-design-system.md`
   - 如果模式可重用，还创建 `ai/skills/[项目]-design-system/SKILL.md`

**架构 → 方法论文档**

1. 记录文件夹结构及其设计思路
2. 捕捉数据流模式
3. 记录关键的技术决策
4. 使用 [`project-summary.md`](references/output-templates/project-summary.md) 模板创建文档：
   - `docs/extracted/[项目]-summary.md`

**模式 → 技能文档**

对于每个值得记录为技能的模式：
1. 查看 [`skill-quality-criteria.md`](references/skill-quality-criteria.md)
2. 使用 [`skill-template.md`](references/output-templates/skill-template.md) 模板
3. 遵循质量检查标准：
   - 描述中包含“做什么”（WHAT）、“何时使用”（WHEN）、“关键词”（KEYWORDS）
   - 不要包含 Claude 已知的基础知识
   - 文档长度应少于 300 行
4. 创建 `ai/skills/[项目]-[模式]/SKILL.md`

---

### 第四阶段：验证

在编写输出文件之前，对提取的内容进行验证。

**对于每个技能，验证以下内容：**
- 描述中是否包含“做什么”（WHAT）、“何时使用”（WHEN）和触发条件（KEYWORDS）
- 内容是否包含超过 70% 的专家级知识（不在 Claude 的基础模型中）
- 文档长度是否少于 300 行（最多 500 行）
- 是否有“何时使用”（When to Use）部分，并包含明确的触发条件
- 是否包含代码示例（如适用）
- 是否包含避免使用这些模式的建议（NEVER Do 部分）
- 文档是否具有通用性（不包含具体的项目名称）

**对于文档，验证以下内容：**
- 提取的内容是否为实际值（而非占位符）
- 模板是否填写完整
- 是否记录了设计方向
- 文件路径是否正确

**冲突检测：**
在创建新技能之前，检查是否已经存在类似的技能：

```bash
# Check existing skills in the target repo
ls ai/skills/*/
```

| 情况 | 应采取的行动 |
|-----------|--------|
| 已经存在类似的技能 | 优化现有的技能 |
| 模式重复 | 记录重复内容，可能在后续合并 |
| 独特的模式 | 继续创建新技能 |

---

### 第五阶段：输出

将提取的内容写入目标位置。

**方法论文档：**
```
docs/extracted/
├── [project]-summary.md       # Overall methodology
├── [project]-design-system.md # Design tokens and aesthetic
└── [project]-architecture.md  # Code patterns (if complex)
```

**技能文档：**
```
ai/skills/
└── [project]-[category]/
    ├── SKILL.md
    └── references/  # (if needed for detailed content)
```

**如果 `docs/extracted/` 目录不存在，请创建该目录。**

---

## 提取重点领域

### 设计系统提取（最高优先级）

当项目有明确的设计工作时，应彻底提取相关内容：

**必须捕获的信息：**
- 颜色调色板（主色、辅助色、强调色、语义色）
- 字体排版（字体、字号、粗细）
- 间距设置
- 动画/过渡效果
- 整体的设计风格或美学方向

**查找文件：**
- `tailwind.config.js` / `tailwind.config.ts`
- `globals.css` / `app.css` / 核心 CSS 文件
- `theme.ts` / `theme.js`
- 任何设计文档

**生成内容：**
- 包含实际值的 design 系统文档
- 如果设计风格独特，还生成相应的技能文档

### 工作流程提取

**查找以下内容：**
- Makefile 中的自动化脚本
- `package.json` 中的配置脚本
- Docker 配置文件
- 持续集成/持续部署（CI/CD）工作流程

**提取内容：**
- 开发设置命令
- 构建流程
- 部署模式

---

## 错误处理

| 情况 | 处理方法 |
|-----------|------------|
| 未找到模式 | 仅创建项目摘要，并记录提取失败的原因 |
| 模式过于特定于某个项目 | 跳过该模式或通过省略项目名称来使其通用化 |
| 模式不完整 | 提取现有的内容，并记录缺失的部分 |
- 不符合质量标准 | 修订技能文档或跳过该模式 |
- 已经存在类似的技能 | 更新现有技能而非创建新的技能 |
- 无法找到源文件 | 在提取日志中记录该情况，并跳过该类别 |

**如果提取部分失败：**
1. 完成可以提取的部分
2. 在项目摘要中记录缺失的内容
3. 在输出文件中注明“提取不完整”
4. 建议需要哪些额外的信息

---

**禁止的行为**

- **禁止提取默认配置** — 仅提取自定义的、有明确设计目的的模式
- **禁止为基本概念创建技能文档** — Claude 已经掌握了 React 和 Tailwind 的基础知识
- **禁止跳过设计相关的内容** — 设计哲学是最高优先级
- **禁止生成的技能文档超过 500 行** — 详细内容请参考相关参考资料
- **禁止创建描述不完整的技能文档** — 描述是决定技能是否适用的关键
- **禁止提取一次性解决方案** — 重点提取在多个地方使用的模式
- **禁止跳过验证阶段** — 在编写输出前必须进行质量检查
- **禁止在技能文档中包含项目名称** — 确保模式具有通用性
- **禁止创建重复的技能** — 先检查是否已有类似的技能

---

## 完成前的质量检查

- **设计系统是否被捕获？**
- **方法论摘要是否已创建？**
- **技能文档是否包含完整的描述（包括“做什么”（WHAT）、“何时使用”（WHEN）、“关键词”（KEYWORDS）？**
- **技能文档是否通过了专家级知识的验证？**
- **技能文档中是否记录了避免使用这些模式的建议（ANTI-PATTERNS）？**
- **输出文件是否已正确生成？**

---

## 提取后的步骤：准备进一步优化

如果您打算将提取的内容用于多个项目的整合：

**将结果复制到技能工具包仓库中进行进一步优化：**

```bash
# From this project, copy to the skills repo staging area
cp -r ai/skills/[project]-* /path/to/skills-repo/ai/staging/skills/
cp -r docs/extracted/* /path/to/skills-repo/ai/staging/docs/
```

**优化后的文件夹结构：**
```
ai/staging/
├── skills/           # Extracted skills from multiple projects
│   ├── project-a-design-system/
│   ├── project-b-ui-patterns/
│   └── ...
└── docs/             # Extracted methodology docs
    ├── project-a-summary.md
    ├── project-b-design-system.md
    └── ...
```

**整合多个项目的优化内容后：**
- 标注为“优化后的内容”或“整合后的技能”
- 优化过程将包括：
  - 识别跨项目的共同模式
  - 将这些模式整合为通用的技能文档
  - 更新方法论文档以包含新的见解
  - 将优化后的技能文档推送到正式的使用位置

---

## 相关工具

- **自动化提取工具：** [`ai/agents/extraction/`](../../agents/extraction/) — 自动化提取流程
- **提取命令：** [`/extract-patterns`](../commands/extraction/extract-patterns.md) — 快速提取命令
- **下一步：** [`ai/skills/refinement/`](../refinement/) — 整合提取到的模式
- **质量标准：** [`references/skill-quality-criteria.md`](references/skill-quality-criteria.md)