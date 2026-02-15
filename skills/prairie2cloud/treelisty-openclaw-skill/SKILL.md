---
name: treelisty
description: **分层项目分解与规划**  
适用于分解复杂项目、构建信息结构、规划多步骤工作流程或组织任何嵌套层次结构。支持21种专业模式（如WBS、GTD、哲学分析、销售流程、电影制作流程等），并可将结果导出为JSON、Markdown或Mermaid图表格式。
license: Apache-2.0
metadata:
  author: prairie2cloud
  version: "1.0.0"
  openclaw:
    requires:
      bins: ["node"]
---

# TreeListy 技能

TreeListy 是一个用于层次化内容分解的工具。当你需要将一个复杂主题进行拆分、规划项目或以树状结构组织信息时，可以使用 TreeListy。

## 何时使用此技能

在以下情况下使用 TreeListy：
- **分解复杂任务**：将一个大目标拆分为多个阶段、子任务和可执行的操作。
- **项目规划**：创建具有适当层次结构的工作分解结构（WBS）、路线图或战略计划。
- **结构化分析**：组织论点、对话或知识库。
- **内容组织**：规划书籍、课程、论文或活动安排。
- **可视化文档**：为任何层次结构生成 Mermaid 图表。

## 快速入门

```bash
# List available patterns
node scripts/treelisty-cli.js patterns

# Create a structured decomposition
node scripts/treelisty-cli.js decompose --pattern wbs --input "Build a mobile app"

# Export to Mermaid diagram
node scripts/treelisty-cli.js export --input tree.json --format mermaid
```

## 21 种常用模板

| 模板 | 图标 | 适用场景 |
|---------|------|----------|
| `generic` | 📋 | 通用项目，默认结构 |
| `sales` | 💼 | 销售流程，季度交易 |
| `thesis` | 🎓 | 学术论文，学位论文 |
| `roadmap` | 🚀 | 产品路线图，功能规划 |
| `book` | 📚 | 书籍，小说，剧本结构 |
| `event` | 🎉 | 活动策划，会议 |
| `fitness` | 💪 | 训练计划，锻炼方案 |
| `strategy` | 📊 | 业务策略，关键绩效指标（OKRs） |
| `course` | 📖 | 课程大纲，教学计划 |
| `film` | 🎬 | AI 视频制作（Sora, Veo） |
| `veo3` | 🎥 | Google Veo 3 工作流程 |
| `sora2` | 🎬 | OpenAI Sora 2 工作流程 |
| `philosophy` | 🤔 | 哲学论点，对话 |
| `prompting` | 🧠 | 提示工程库 |
| `familytree` | 👨‍👩‍👧‍👦 | 家谱，家族史 |
| `dialogue` | 💬 | 辩论分析，修辞学 |
| `filesystem` | 💾 | 文件/文件夹管理 |
| `gmail` | 📧 | 电子邮件工作流程 |
| `knowledge-base` | 📚 | 文献语料库，问答系统（RAG）准备 |
| `capex` | 💰 | 资本支出，投资者演示 |
| `freespeech` | 🎙️ | 语音捕捉模式分析 |
| `lifetree` | 🌳 | 人生时间线 |
| `custom` | ✏️ | 定义自定义的层级名称 |

## 命令

### `patterns` — 查找可用的模板

```bash
# List all patterns
node scripts/treelisty-cli.js patterns

# Get details for a specific pattern
node scripts/treelisty-cli.js patterns --name philosophy

# Get full JSON schema
node scripts/treelisty-cli.js patterns --name philosophy --detail
```

### `decompose` — 创建结构化的树状结构

接受文本输入（主题、大纲或结构化文本），并应用相应的模板。

**选项：**
- `--pattern <key>` — 要应用的模板（默认：generic）
- `--input <text|file>` — 主题文本、文件路径或标准输入（stdin）
- `--name <name>` — 覆盖根节点名称
- `--depth <1-4>` — 树的最大深度
- `--format <fmt>` — 输出格式：json、markdown、mermaid

### `export` — 将树状结构转换为其他格式

**支持的格式：** json、markdown、mermaid、csv、checklist、html

### `validate` — 检查树的结构质量

**返回结果：**
- 质量评分（0-100）
- 结构分析（节点数量、深度、平衡性）
- 问题（错误、警告、建议）
- 模板合规性检查

### `push` — 将树状结构发送到在线 TreeListy（可选）

如果用户在浏览器中打开了支持 MCP 桥接的 TreeListy 应用程序：

```bash
node scripts/treelisty-cli.js push \
  --input tree.json \
  --port 3456
```

树状结构将在 TreeListy 的可视化界面中显示，便于交互式探索。

## 树状数据模型

树的结构如下：

```json
{
  "id": "n_abc12345",
  "treeId": "tree_xyz78901",
  "name": "Project Name",
  "type": "root",
  "pattern": "roadmap",
  "icon": "🚀",
  "description": "Optional description",
  "expanded": true,
  "children": [
    {
      "name": "Phase 1",
      "type": "phase",
      "items": [
        {
          "name": "Feature A",
          "type": "item",
          "patternType": "Core Feature",
          "subtasks": [
            {
              "name": "Implement login",
              "type": "subtask"
            }
          ]
        }
      ]
    }
  ]
}
```

**层次结构：** 根节点 → 阶段 → 子任务 → 子子任务

每个模板都会添加自定义字段。例如，`roadmap` 模板会添加 `storyPoints`、`userImpact`、`technicalRisk` 等字段。

## 工作流程示例

1. **代理从用户处接收复杂任务**。
2. **使用合适的模板进行分解：**
   ```bash
   node scripts/treelisty-cli.js decompose \
     --pattern wbs \
     --input "Build an e-commerce platform with user auth, product catalog, shopping cart, and checkout" \
     --format json > project.json
   ```

3. **验证结构：**
   ```bash
   node scripts/treelisty-cli.js validate --input project.json
   ```

4. **导出结果供用户使用：**
   ```bash
   node scripts/treelisty-cli.js export --input project.json --format mermaid
   ```

5. **将生成的 Mermaid 图表分享给用户。**

## 无需使用 AI 令牌

TreeListy 的所有操作都是基于本地模板进行的转换，不涉及任何 API 调用，也不会产生任何费用。该工具使用 21 种经过验证的层次化模板来组织内容。

## 更多信息

- 完整的模板参考：`references/PATTERNS.md`
- TreeListy 可视化应用：https://treelisty.com
- 源代码：https://github.com/prairie2cloud/treelisty