---
name: diataxis-writing
description: Diataxis文档框架实践指南。为四种类型的文档（教程/操作指南/参考手册/解释性文档）提供了诊断、分类、模板以及质量评估方法。
---
# Diátaxis 文档框架实践

## 快速入门

在创建或重构文档时，请遵循以下步骤：

### 编写前的问题（必须询问）

**在开始之前，请询问用户：**

1. **语言偏好**：“这份文档应该用哪种语言编写？”
   - 英语 / 中文 / 其他语言

2. **输出方式**： “完成后，您希望如何输出这份文档？”
   - 聊天消息（默认）
   - Feishu 文档（通过 MCP/mcporter）
   - 本地 Markdown 文件
   - GitHub 仓库
   - 其他平台

### 工具可用性检查（用户选择输出方式后）

**用户选择输出方式后，自动检查工具是否可用：**

```bash
# Run auto-detection (script is in ./scripts/ relative to this skill)
python3 scripts/output-handler.py --detect
```

**检查结果：**
- ✅ 工具可用 → 继续使用选定的输出方式
- ⚠️ 工具不可用 → 通知用户并推荐替代方案

**对于通过 MCP 输出到 Feishu 的情况：**
- 检查是否安装了 mcporter
- 检查 MCP Feishu 服务器是否已配置（通常位于 `/root/config/mcporter.json` 或 `~/.mcporter/mcporter.json`）
- 测试与 Feishu MCP 服务器的连接

**如果工具不可用：**
1. 通知用户：“选定的输出方式 [X] 不可用”
2. 推荐替代方案：“可用选项：[列表]”
3. 请用户确认替代方案或配置相应的工具

### 编写工作流程

在确认语言、输出方式和工具可用性后，请按照以下步骤进行：
1. **确定用户需求** - 使用 [Diataxis Compass](references/compass.md) 来确定文档类型
2. **选择模板** - 从 [templates/](templates/) 中选择相应的模板
3. **使用检查表** - 在编写过程中使用相应的 [检查表](references/)
4. **质量评估** - 使用 [质量框架](references/quality-framework.md) 来评估最终草稿
5. **执行输出** - 使用用户选择的方式和语言输出文档

## 四种文档类型

Diátaxis 区分了四种根本不同的文档类型，每种类型对应不同的用户需求：

| 类型 | 用户需求 | 文档目的 | 关键特征 |
|------|-----------|------------------|---------------------|
| **教程** | 获取技能（学习） | 提供学习体验 | 以实践为导向，减少解释，提供具体步骤 |
| **操作指南** | 应用技能（工作） | 帮助完成任务 | 以目标为导向，假设用户具备相关技能，处理实际场景 |
| **参考资料** | 应用技能（工作） | 描述技术事实 | 中立描述，准确完整，结构清晰 |
| **解释性文档** | 获取技能（学习） | 提供理解背景 | 采用论述式写作，允许表达个人观点，提供相关背景信息 |

### 类型详情

- **教程**：[references/four-types.md#Tutorial](references/four-types.md)
- **操作指南**：[references/four-types.md#How-to Guide](references/four-types.md)
- **参考资料**：[references/four-types.md#Reference](references/four-types.md)
- **解释性文档**：[references/four-types.md#Explanation](references/four-types.md)

## 使用 Diátaxis Compass

当不确定文档类型时，请使用 [compass.md](references/compass.md) 这个工具：

提出两个问题：
1. **内容类型**：是提供操作指导（action）还是认知知识（cognition）？
2. **用户状态**：用户是在获取技能（acquisition/study）还是在应用技能（application/work）？

## 常见用例

### 用例 1：故障排除记录 → 操作指南或解释性文档

故障排除记录通常属于以下类型：
- **操作指南**：如果提供“如何解决 X 问题”的逐步指导
- **解释性文档**：如果是对“X 问题发生的原因”的原理分析

**模板**：[templates/template-troubleshooting.md](templates/template-troubleshooting.md)

### 用例 2：经验总结 → 操作指南或解释性文档

- **最佳实践**：操作指南（提供正确操作的方法）
- **经验教训**：解释性文档（解释某些方法为何错误）

**模板**：[templates/template-best-practices.md](templates/template-best-practices.md)

### 用例 3：学习笔记 → 教程或解释性文档

- **学习笔记**：如果是包含实际操作步骤的笔记，则属于教程
- **理论总结**：如果是概念性解释，则属于解释性文档

**模板**：[templates/template-learning-notes.md](templates/template-learning-notes.md)

### 用例 4：探索性分享 → 解释性文档

技术探索、实验记录和比较分析通常属于解释性文档。

**模板**：[templates/template-exploration.md](templates/template-exploration.md)

## 检查表

在编写过程中和编写完成后，请使用以下检查表：
- 教程：[checklist/checklist-tutorial.md](checklist/checklist-tutorial.md)
- 操作指南：[checklist/checklist-how-to.md](checklist/checklist-how-to.md)
- 参考资料：[checklist/checklist-reference.md](checklist/checklist-reference.md)
- 解释性文档：[checklist/checklist-explanation.md](checklist/checklist-explanation.md)

## 质量评估

使用功能质量和深度质量框架进行评估：[references/quality-framework.md]

### 功能质量
- 准确性、完整性、一致性、可用性、精确性

### 深度质量
- 文章结构是否流畅、是否符合用户需求、外观是否美观、是否能够预见用户需求

## 常见错误

避免以下错误：
[references/common-mistakes.md](references/common-mistakes.md)

1. **类型混淆** - 将参考资料的内容混入教程中
2. **位置错误** - 将解释性文档写成教程
3. **界限模糊** - 在操作指南中加入过多解释性内容
4. **结构不一致** - 参考资料未能反映产品架构

## 语言风格

四种文档类型使用不同的语言风格：
[references/writing-language.md](references/writing-language.md)

- **教程**：使用“我们将...”、“请注意...”、“现在执行 X...”等语句
- **操作指南**：使用“如果您需要 X，请执行 Y”、“请参考 X 文档以获取完整信息”等语句
- **参考资料**：使用“X 继承了 Y”、“子命令：a, b, c”、“必须使用 X”等语句
- **解释性文档**：使用“X 的原因是...”、“W 比 Z 更好，因为...”等语句

## 输出方式

完成文档后，使用用户选择的方式输出：

### 可用的输出方式

1. **聊天消息** - 直接在聊天中显示（默认）
2. **Feishu 文档** - 通过 **MCP/mcporter** 创建/更新 Feishu 文档（需要 MCP Feishu 服务器）
3. **本地 Markdown** - 保存为 .md 文件（内置支持）
4. **GitHub 仓库** - 提交到代码仓库（需要 MCP github 或 git）
5. **其他平台** - 用户提供平台信息，MCP 提供相应的支持

**重要提示：** 对于 Feishu 输出，始终使用 MCP/mcporter 方法，不要使用其他渠道工具。

### 检测可用工具

使用 [scripts/output-handler.py](scripts/output-handler.py) 自动检测可用工具（该脚本位于 `./scripts/` 目录下）：

```bash
python3 scripts/output-handler.py --detect
```

**工具可用性检查**

**用户选择输出方式后，检查工具是否可用：**

1. 运行 `output-handler.py --detect`
2. 检查所选工具是否已配置且可用
3. 如果工具不可用：
   - 通知用户：“选定的输出方式 [X] 不可用”
   - 从可用工具列表中推荐替代方案
   - 请用户确认替代方案

### 选择输出方式

**必须询问用户：**“文档编写完成，您希望如何输出？”

根据用户的选择：
- **聊天** → 直接回复
- **Feishu (MCP)** → 使用 mcporter 调用 Feishu MCP 服务器
  ```bash
  node /path/to/mcporter/dist/cli.js call feishu doc.create '{"title":"...", "content":"..."}'
  # Note: mcporter path varies by installation, common paths:
  # - ~/.npm/_npx/*/node_modules/mcporter/dist/cli.js
  # - Or use: npx mcporter call feishu doc.create ...
  ```
- **本地** → 调用 `write` 工具或 `output-handler.py --output local`
- **GitHub** → 调用 `output-handler.py --output github`
- **其他** → 请用户提供 MCP 服务器的相关信息

### 语言考虑

根据用户的选择输出文档：
- 如果选择中文，则输出中文
- 如果选择其他语言，请确认系统是否支持翻译

### 输出平台详情

完整的平台列表及配置方法：[references/output-platforms.md](references/output-platforms.md)

| 平台 | 所需工具 | 配置难度 | 适用场景 |
|----------|---------------|-------------------------|----------|
| 聊天 | 无需额外工具 | - | 快速回复 |
| Feishu (MCP) | MCP Feishu 服务器 | 中等难度 | 团队协作 |
| 本地 Markdown | 内置支持 | 低难度 | 个人使用 |
| GitHub | MCP github/git | 中等难度 | 技术博客 |
| Notion | MCP notion | 中等难度 | 知识库 |
| Google Docs | MCP google | 高难度 | Google 生态系统 |

## 理论框架

Diátaxis 的完整理论体系包括：
- **映射模型**：[references/map.md](references/map.md)
- **理论基础**：[references/four-types.md](references/four-types.md)
- **质量框架**：[references/quality-framework.md](references/quality-framework.md)

## 使用脚本（可选）

使用诊断脚本自动识别文档类型（脚本位于 `./scripts/` 目录下）：

```bash
python3 scripts/diagnose.py <document content or file path>
```

---

**技能版本**：1.0  
**理论来源**：https://diataxis.fr  
**作者**：Zhua Zhua（为 Master 版本创建）