---
name: frontend-design-extractor
description: "从前端代码库中提取可重用的 UI/UX 设计系统，包括设计元素（design tokens）、全局样式（global styles）、组件（components）、交互模式（interaction patterns）以及页面模板（page templates）。在分析任何前端项目（React/Vue/Angular/Next/Vite 等）时，可以利用这些提取的内容来记录或迁移 UI/UX 设计，以便在其他项目中重复使用。请仅关注 UI/UX 部分，明确忽略业务逻辑和领域工作流程（business logic and domain workflows）。"
---

# 前端设计提取工具

## 概述
该工具通过梳理前端代码库中的UI资源、记录基础设计规范、整理组件信息以及捕捉页面级别的模式和行为，提取出可复用的UI/UX设计文档。该工具不涉及业务逻辑和特定领域的工作流程，且具有框架无关性（能够适应目标代码库中实际使用的技术栈）。

## 快速入门
1. 确定工作模式：新项目（从零开始）或现有项目重构。请注意，业务逻辑不在工具的处理范围内。
2. 如果使用现有代码库，请运行 `scripts/scan_ui_sources.sh` 命令来扫描代码库的根目录。该脚本会使用通用的匹配规则，并默认忽略常见的构建/缓存目录以及提取结果文件夹。
3. 可选参数：`scripts/scan_ui_sources.sh <repo_root> [out_file] [extra_glob ...]` 或 `--root/--out/--ignore`（用于处理非标准的目录结构）。
4. 通过 `scripts/generate_output_skeleton.sh` 命令创建输出文件夹（默认为 `./ui-ux-spec`），并将所有提取结果保存在该文件夹中。
5. 输出内容将遵循预设的结构（详见“输出结构”部分）。

## 工作模式（请选择一种）

### A) 从零开始（新建项目）
目标：创建一个不包含业务逻辑的可复用UI/UX基础框架及初始UI组件。

1. 定义基础设计规范，包括颜色、字体样式、间距、阴影效果、动画效果等设计元素，以及全局样式和布局框架。
2. 创建一组基础组件：按钮（Button）、输入框（Input）、选择框（Select）、卡片（Card）、模态框（Modal）、表格（Table）、列表（List）、标签页（Tabs）、提示框（Toast）和空状态（EmptyState）。
3. 创建页面模板，包括列表（List）、详情页（Detail）、表单（Form）和仪表盘（Dashboard）的骨架结构，并添加占位数据。
4. 提供针对目标框架的实现指南（如CSS架构、主题设置机制和文件结构）。
5. 可选地运行 `scripts/generate_output_skeleton.sh [out_root]` 命令来生成相应的文件夹结构和空模板。默认的输出目录为 `./ui-ux-spec`。

**交付物：**
- 设计规范文档
- 包含组件变体、可用性状态（a11y标准）的组件目录
- 带有布局规则的页面模板
- 工程实现相关约束（如命名规范、CSS使用方式、主题设置）

### B) 项目重构
目标：提取现有项目的UI/UX设计规范，统一设计元素，并制定安全的、逐步的改进计划。

1. 整理前端代码库中的UI资源（通过扫描脚本或手动检查）。
2. 将现有的设计元素进行标准化处理，并将其映射到新的规范中。
3. 确定需要优先改进的高影响组件和设计模式。
4. 制定分阶段的迁移计划，以最小化代码差异（例如使用封装组件、主题适配器等手段逐步替换旧代码）。
5. 记录现有的设计缺陷及可访问性（a11y标准）方面的问题，并计划逐步修复。

**交付物：**
- 提取的设计规范文档（与新建项目相同）
- 分阶段的迁移计划（包含低风险的实施步骤）
- 组件级别的映射信息

## 从设计规范开始的重构流程（固定步骤）
当需要将现有的 `ui-ux-spec/` 应用于目标项目时，请按照以下步骤进行：
1. **了解目标项目**：确认目标项目使用的框架、样式系统、组件库以及开发入口点。
2. **制定重构计划**：对比设计规范与当前项目的差异，按类别列出需要修改的内容：
   - 设计元素和全局样式
   - 组件
   - 设计模式和页面布局
   - 可访问性方面的问题
   **注意**：不要假设设计规范中的文件夹结构与目标项目一致，应根据实际内容进行映射。
3. **分阶段执行重构**：严格按照计划逐步进行修改，避免遗漏任何需要调整的部分。
4. **验证重构结果**：每个阶段完成后，重新检查代码是否符合设计规范，并确保修改后的代码差异最小且可逆。
5. **总结与反馈**：在完成当前阶段后，提供详细的变更列表以及剩余需要改进的地方，并建议下一阶段的改进方向。

## 重构请求模板
使用以下模板之一，以确保请求的清晰性和计划的可执行性：

### 模板A：标准重构
```
Please refactor the existing project based on this UI/UX spec:
- Project path: /path/to/target-project
- Spec path: /path/to/ui-ux-spec
- Goal: UI/UX only (tokens, styles, components, layout), do not change business logic/APIs
- Scope: start with global styles + base components
- Constraints: minimal changes, small-step commits, reversible
- Deliverables: refactor plan + actual code changes + list of impacted files
```

### 模板B：分阶段重构
```
Please refactor UI/UX in phases; only do Phase 1:
- Project path: /path/to/target-project
- Spec path: /path/to/ui-ux-spec
- Phase 1: align tokens + global styles (colors/typography/spacing/radius/shadows)
- Do not change: business logic/routing/APIs
- Deliverables: list of changed files + alignment diff notes
```

### 模板C：组件级重构
```
Please align the following components to the spec while keeping business logic unchanged:
- Project path: /path/to/target-project
- Spec path: /path/to/ui-ux-spec
- Component list: Button, Input, Modal, Table
- Goal: only change styling/structure/interaction details
- Deliverables: alignment notes per component + code changes
```

## 工作流程

### 0) 确定工作范围和约束条件
- 确认代码库的根目录、使用的框架以及任何设计系统相关包。
- 确定所需的输出格式（默认为Markdown格式）。
- 了解需要遵守的约束条件：例如品牌设计规范、目标平台以及可访问性要求。
- 重申：工具不处理业务逻辑和业务规则，也不会修改项目现有的代码结构。

### 1) 整理代码资源（仅针对现有代码库）
- 不要假设代码库有固定的目录结构；扫描结果将帮助确定需要查看的资源位置。
- 运行扫描脚本，并检查以下内容：
   - 设计元素（如颜色、字体样式等）、全局样式、主题设置
   - 使用的组件库及自定义封装组件
   - 项目中的Storybook文档、测试用例或视觉回归测试结果
   - 资源文件和国际化（i18n）相关文件

### 2) 基础设计规范（设计元素和全局样式）
- 记录颜色、字体样式、间距、阴影效果、z轴层次（z-index）以及动画效果等设计元素。
- 确定页面的默认样式（如背景重置、文本默认样式、链接和表单的默认样式、焦点可见性、滚动条的显示规则等）。

### 3) 布局与信息架构
- 记录页面的断点设置、容器布局、网格系统、导航结构以及页面的总体布局框架。

### 4) 组件信息整理
- 对每个组件进行详细记录，包括其用途、组件结构、可用状态、交互方式、可访问性要求、响应式行为、动画效果以及主题设置相关的功能。
- 如果使用了第三方库，重点关注自定义的封装组件及其覆盖的属性。

### 5) 页面模板与组合规则
- 提取页面的骨架结构（如列表页、详情页、表单页、仪表盘等），以及各组件的排列顺序。
- 记录页面在不同状态下的显示效果（如加载中、空白状态、错误状态、只读状态等）。

### 6) 行为与内容规则
- 记录页面的加载和错误处理策略、数据验证规则、撤销操作的功能以及优化的更新逻辑。
- 记录文本描述的编写规范以及国际化格式要求。

### 7) 生成输出文件
- 至少生成以下文件：
   - 设计规范文档
   - 组件目录
   - 页面模板
   - 确保输出文件保存在指定的文件夹中（默认为 `ui-ux-spec/`）。
   **注意**：除非用户有特殊要求，否则输出文件的结构应保持不变。

## 输出结构（推荐格式）
此结构为推荐的文档格式。它不必与目标项目的目录结构完全一致，用户可以根据需要更改文件夹名称或位置（例如：`docs/ui-ux-spec/`）。

## 相关工具
- `scripts/scan_ui_sources.sh`：用于在代码库中查找UI相关资源。
- `scripts/generate_output_skeleton.sh`：用于生成标准的输出文件夹和占位模板。
- `references/design-extraction-checklist.md`：根据README文件生成的详细检查清单。