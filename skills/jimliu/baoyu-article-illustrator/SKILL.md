---
name: baoyu-article-illustrator
description: 分析文章的结构，确定需要使用视觉辅助工具的部分，并采用“Type × Style”二维设计方法生成相应的插图。适用于用户请求“为文章添加插图”、“为文章生成图片”或“为文章配图”的场景。
version: 1.56.1
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator
---
# 文章插图生成工具

该工具用于分析文章内容，确定插图的位置，并生成符合特定类型和风格的图像。

## 两种维度

| 维度 | 控制选项 | 示例 |
|-----------|----------|----------|
| **类型** | 信息结构 | 信息图、场景图、流程图、对比图、框架图、时间线图 |
| **风格** | 视觉效果 | 温暖风格、极简风格、蓝图风格、水彩风格、优雅风格 |

可以自由组合使用：`--type infographic --style blueprint`  
或者使用预设样式：`--preset tech-explainer`（同时指定类型和风格）。详细信息请参见 [样式预设](references/style-presets.md)。

## 图片类型

| 类型 | 适用场景 |
|------|----------|
| `infographic` | 数据展示、指标分析、技术说明 |
| `scene` | 故事叙述、情感表达 |
| `flowchart` | 流程说明、工作流程 |
| `comparison` | 对比分析 |
| `framework` | 模型展示、架构图 |
| `timeline` | 历史发展过程 |

## 图片风格

详细信息请参见 [styles.md](references/styles.md)，其中包含核心风格、完整风格库以及类型与风格的兼容性说明。

## 工作流程

### 第一步：预检查

**1.5 加载用户偏好设置（EXTEND.md）⛔**  
（此步骤为必填，用于确保工具根据用户设置进行操作。）

### 第二步：分析文章内容

| 分析内容 | 输出结果 |
|----------|--------|
| 文章类型 | 技术类/教程类/方法论类/叙述类 |
| 文章目的 | 信息传递/可视化展示/创意表达 |
| 核心观点 | 2-5个主要论点 |
| 插图适用位置 | 插图能够提升文章效果的位置 |

**注意**：使用隐喻时，应将其可视化，而非直接绘制成图片。  
完整步骤请参见 [references/workflow.md](references/workflow.md#step-2-setup--analyze)。

### 第三步：确认设置 ⚠️

**请用户回答以下问题（最多4个问题，其中Q1和Q2为必答项；Q3仅在未选择预设样式时需要回答）：**

| 问题 | 选项 |
|---|---------|
| **Q1：使用预设样式还是自定义类型？** | 推荐的预设样式、备用预设样式，或手动选择：信息图、场景图、流程图、对比图、框架图、时间线图、混合样式 |
| **Q2：插图密度？** | 极简风格（1-2张/页）、平衡风格（3-5张/页）、每节一张（推荐）、密集风格（6张以上） |
| **Q3：选择哪种风格？** | 推荐风格、极简扁平风格、科幻风格、手绘风格、编辑风格、海报风格、其他风格（如已选择预设样式则可跳过此步骤） |
| **Q4：语言设置？** | 文章语言与 EXTEND.md 中设置的语言是否一致 |

完整步骤请参见 [references/workflow.md](references/workflow.md#step-3-confirm-settings)。

### 第四步：生成大纲

创建一个 `outline.md` 文件，其中包含以下内容：
- 文章类型
- 插图密度
- 选择的风格
- 需要生成的图片数量

完整模板请参见 [references/workflow.md](references/workflow.md#step-4-generate-outline)。

### 第五步：生成图片

**注意**：在生成任何图片之前，必须先保存所有相关的提示文件。  
**执行策略**：当有多个插图需要生成时，建议使用 `baoyu-image-gen` 批量处理模式（`build-batch.ts` 和 `--batchfile` 参数），以避免重复操作。只有在每张图片都需要单独处理或需要创意调整时，才使用子代理任务。  
具体步骤如下：
1. 根据 [references/prompt-construction.md](references/prompt-construction.md) 为每个插图创建提示文件。
2. 将提示文件保存到 `prompts/NN-{type}-{slug}.md` 目录中，并使用 YAML 格式编写文件内容。
3. 提示文件必须包含类型相关的结构化信息（区域划分、标签、颜色、风格、元素等）。
4. 标签中必须包含文章中的具体数据（如数字、术语、指标、引文等）。
5. **禁止** 直接将临时生成的提示内容传递给 `--prompt` 命令，必须先保存提示文件。
6. 选择合适的生成方式（`direct`、`style` 或 `palette`）。
7. 如果启用了 EXTEND.md 功能，请添加水印。
8. 从保存的提示文件中生成图片；如果生成失败，请重试一次。

完整步骤请参见 [references/workflow.md](references/workflow.md#step-5-generate-images)。

### 第六步：最终处理

在文章段落后插入生成的图片文件（格式：`![描述](path/NN-{type}-{slug}.png)`。

## 输出目录

输出文件的路径格式为 `NN-{type}-{slug}.png`，其中 `NN` 为数字或字母组合，`slug` 为2-4个单词的短字符串（使用连字符连接）；文件名中可添加 `-YYYYMMDD-HHMMSS` 作为时间戳。

## 文章修改流程

| 操作 | 所需步骤 |
|--------|-------|
| 修改内容 | 更新提示文件 → 重新生成图片 → 更新相关参考文件 |
| 添加新插图 | 确定插图位置 → 创建提示文件 → 生成图片 → 更新大纲 → 插入图片 |
| 删除插图 | 删除相关文件 → 移除引用信息 → 更新大纲 |

## 参考资料

| 文件 | 详细内容 |
|------|---------|
| [references/workflow.md](references/workflow.md) | 完整的工作流程说明 |
| [references/usage.md](references/usage.md) | 命令使用说明 |
| [references/styles.md](references/styles.md) | 图片风格库 |
| [references/style-presets.md](references/style-presets.md) | 预设样式快捷方式 |
| [references/prompt-construction.md](references/prompt-construction.md) | 提示文件模板 |
| [references/config/first-time-setup.md](references/config/first-time-setup.md) | 首次使用指南 |