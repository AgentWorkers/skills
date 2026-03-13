---
name: modelshow
version: 1.0.1
description: >
  **盲法多模型比较：具备架构级去匿名化保障**  
  可通过 `mdls` 或 `modelshow` 命令触发该功能，实现对 AI 模型响应的双盲评估（即评估过程中评估者和被评估者均不知晓彼此的模型信息）。
metadata: {"openclaw": {"homepage": "https://github.com/schbz/modelshow", "emoji": "🕶️"}}
---
# ModelShow — 专业多模型评估工具

ModelShow 是一个先进的框架，用于通过双盲评估来比较人工智能模型的输出。该系统可以并行查询多个模型，对它们的输出进行匿名处理，并使用独立的评估模型仅根据模型表现对其进行排名。

## 主要特性

- **架构级去匿名化保证**：评估子代理在返回结果之前会自动进行去匿名化处理——协调者永远看不到占位符标签。
- **加密随机化**：使用 `secrets.SystemRandom()` 方法以加密安全的随机顺序向评估者展示模型输出。
- **全面评估**：评估者不仅会为每个模型提供排名，还会提供分析模型间差异的“总体评估”。
- **智能监控**：自动监控进度，提供无内容的状态更新，并能即时检测任务完成情况。
- **专业格式的输出**：输出结果包含分数、评估者的评论以及有用的见解。

## 检测规则

**触发条件**：消息以 `mdls` 或 `modelshow` 开头（不区分大小写）。通过移除触发词来提取实际问题。

**示例**：`mdls explain quantum entanglement` → 提取后的问题为 `explain quantum entanglement`。

## 工作流程

```plaintext
步骤 1 → 确认并加载配置
步骤 2 → 启动并行模型代理
步骤 3 → 使用智能监控收集模型输出
步骤 4 → 通过加密随机化进行匿名处理
步骤 5 → 启动评估子代理
步骤 6 → 解析去匿名化后的结果
步骤 7 → 生成格式化输出
步骤 8 → 保存结果（可选：通过 `update_modelshow_index.py` 更新网页索引）
```

### 步骤 1：确认并加载配置

**即时反馈**：
```plaintext
🔄 ModelShow 正在启动——并行查询模型。
评估完成后，结果将自动显示。
```

**加载配置**：读取 `{baseDir}/config.json` 文件以获取模型列表、评估模型、超时设置等配置信息。

### 步骤 2：启动并行模型代理

对于 `config.models` 中的每个模型：
- **模型别名**：例如 `pro`、`grok`、`kimi`
- **唯一标识符**：`mdls-{model}-{timestamp}`
- **超时时间**：`config.timeoutSeconds`（默认值：360 秒）
- **任务内容**：
  ```plaintext
  {config.systemPrompt}
  {提取的用户问题}
  ```
- **并行执行**：如果 `config.parallel` 为 `true`，则同时启动所有代理。
- **上下文处理**：如果问题中提到了外部内容（URL、文件等），则获取这些内容并将其添加到任务中。

### 步骤 3：使用智能监控收集模型输出

- **监控频率**：每 20 秒检查一次模型响应。
- **超时处理**：所有代理完成后立即停止监控。
- **最低成功要求**：至少需要收到 `config.minSuccessful` 个有效模型响应才继续执行。
- **状态更新**：
  ```plaintext
  ⏳ 模型正在响应中... {已完成的数量}/{总数量}。已花费 {elapsed} 秒。
  ✅ 所有 {N} 个模型均已响应。正在发送给评估者...
  ```
- **输出收集**：
  ```python
  collected_responses = {
    "model_name": {
      "status": "completed" | "failed" | "timeout",
      "text": "模型输出内容或空字符串",
      "duration_seconds": duration
    }
  }
  ```
- **失败处理**：如果有效响应数量少于 `config.minSuccessful`，则终止任务并显示错误信息。

### 步骤 4：通过加密随机化进行匿名处理

执行匿名化流程：
```bash
echo '{
  "action": "anonymize",
  "responses": {model: response_dict},
  "label_style": "alphabetic",
  "shuffle": true
}' | python3 {baseDir}/judge_pipeline.py
```

**关键点**：
- `shuffle: true` 确保模型输出顺序的随机性。
- 生成的标签格式为 “Response A”、“Response B” 等。
- `anonymization_map` 用于记录标签与模型之间的对应关系，以便后续去匿名化。

### 步骤 5：启动评估子代理

评估子代理在同一操作中完成评估和去匿名化工作：

**评估者任务结构**：
```plaintext
您是一名公正的评估者，同时也是数据处理器。

您的任务分为两部分，请同时完成这两部分后再返回任何结果。

══════════════════════════════════════════════════════════════
第一部分：评估模型输出
════════════════════════════════════════════════════════════
[带有占位符标签的匿名模型输出]

════════════════════════════════════════════════════════════
第二部分：完成评估
══════════════════════════════════════════════════════════

1. 对每个模型输出进行评分（1-10 分）。
2. 提供分析模型间差异的“总体评估”。
完成评估后，请执行以下命令：
```plaintext
echo '{
  "action": "finalize",
  "judge_output": "[您的评估内容]",
  "anonymization_map": {anonymization_map}
}' | python3 {baseDir}/judge_pipeline.py
```

**评估模型**：使用 `config.judgeModel`（例如 `sonnet`、`gemini31or`）。

### 步骤 6：解析去匿名化后的结果

评估子代理返回以下内容：
- `deanonymized_judge_output`：包含真实模型名称的完整评估结果。
- `ranked_models_deanonymized`：结构化的排名数据。
- `deanonymization_complete`：表示匿名化操作是否完成。

**架构保证**：协调者只能看到去匿名化后的结果，永远不会看到原始的占位符标签。

### 步骤 7：生成格式化输出

生成专业的结果展示格式：
```plaintext
🕶️ 双盲评估结果：

🏆 模型名称（得分：X.X/10）
[模型完整输出]
评估者的评价：[评价内容]

🥈 第二名（得分：X.X/10）
[模型完整输出]
评估者的评价：[评价内容]

📊 总体评估：
[评估者对模型间差异的全面分析]
```

> ⚠️ **警告：步骤 8 是必须执行的。**
> 将结果发送给用户并不意味着任务结束。
> 在发送结果后，必须立即执行步骤 8（`save_results`）。
> 任务只有在 `save_results.py` 返回 `{"success": true}` 时才算完成。
> 任何情况下都不得跳过、延迟或省略步骤 8。

### 步骤 8：保存结果

> 🚨 **此步骤必不可少。请务必执行。**
> 每次运行 ModelShow 后，都必须使用 `save_results.py` 保存结果。
> 如果未保存结果，后续将无法使用这些数据。

**保存位置**：`config.outputDir`（默认路径：`~/.openclaw/workspace/modelshow-results`）：
- **JSON 格式**：`{config.outputDir}/{slug}-{timestamp}.json`
- **Markdown 格式**：`{config.outputDir}/{slug}-{timestamp}.md`

**需要传递给 `save_results.py` 的 JSON 数据格式**：
```json
{
  "prompt": "<原始用户问题>",
  "timestamp": "<ISO 8601 格式的时间戳，例如 2026-03-08T01:00:00Z>",
  "models": ["model1", "model2", "model3"],
  "judge_model": "<config.judgeModel>",
  "output_dir": "<config.outputDir>",
  "ranked_results": [
    {
      "rank": 1,
      "model": "model_alias",
      "score": 9.5,
      "judge_notes": "评估者的具体评价",
      "response_text": "模型的完整输出内容"
    },
    {
      "rank": 2,
      "model": "model_alias",
      "score": 8.0,
      "judge_notes": "评估者的具体评价",
      "response_text": "模型的完整输出内容"
    },
  ],
  "deanonymized_judge_output": "<包含真实模型名称的完整评估结果>",
  "anonymization_map": {
    "Response A": "model_alias_1",
    "Response B": "model_alias_2"
  },
  "metadata": {
    "total_duration_ms": 45000,
    "successful_models": 4,
    "failed_models": 0,
    "timed_out_models": ["deepseek"]
  }
}
```

**执行保存命令**：
```bash
echo '<上述 JSON 数据>' | python3 {baseDir}/save_results.py
```

**验证成功**：脚本必须返回 `{"success": true, ...}`。如果出现错误，请修复后重试。未成功保存的结果将无法保存。

**可选操作**：`update_modelshow_index.py` 用于构建结果文件的本地索引（例如用于自定义仪表板或静态网站），或用于更新 rexuvia.com 的网页展示。这不是必须的工作流程部分。

> ✅ **只有当 `save_results.py` 返回成功结果后，ModelShow 任务才算完成。**

## 配置文件（`config.json`）

| 参数 | 说明 | 默认值 |
|-----|-------------|---------|
| `keyword` | 主要触发词 | `"mdls"` |
| `alternativeKeywords` | 其他触发词 | `["modelshow"]` |
| `models` | 需要比较的模型别名列表 | `["pro", "sonnet", "deepseek", "gpt4", "grok", "kimi"]` |
| `judgeModel` | 用于双盲评估的模型 | `"sonnet"` |
| `outputDir` | 结果文件的保存路径 | `"~/.openclaw/workspace/modelshow-results"` |
| `timeoutSeconds` | 每个模型的最大等待时间 | `360` 秒 |
| `minSuccessful` | 至少需要成功响应的模型数量 | `2` |
| `parallel` | 是否并行运行模型 | `true` |
| `showTopN` | 显示的顶级结果数量 | `10` |
| `includeResponseText` | 是否在输出中包含模型输出 | `true` |
| `blindJudging` | 是否启用匿名化 | `true` |
| `blindJudgingLabels` | 匿名化标签的显示格式 | `"alphabetic"` |
| `shuffleBlindOrder` | 是否随机化模型输出顺序 | `true` |

## 文件结构

```plaintext
modelshow/
├── SKILL.md              # 本文档
├── config.json           | 配置设置
├── judge_pipeline.py     | 匿名化与去匿名化处理脚本
├── save_results.py       | 保存结果及提取评估内容
├── update_modelshow_index.py | 可选：构建结果索引
├── blind_judge_manager.py    | 旧版匿名化辅助工具
└── README.md             | 用户使用说明
└── .gitignore            | Git 忽略文件
```

## 相关脚本

- **judge_pipeline.py**：负责模型输出的匿名化和去匿名化处理。
- **save_results.py**：以 JSON 和 Markdown 格式保存结果，并提取评估者的“总体评估”内容。
- **update_modelshow_index.py**：可选脚本，用于构建结果文件的本地索引或更新网页索引。

## 使用示例

- **基本比较**：
```plaintext
mdls explain the difference between TCP and UDP
```

- **创造性任务**：
```plaintext
mdls write a short poem about working late at night
```

- **技术分析**：
```plaintext
mdls pros and cons of event sourcing vs traditional CRUD
```

- **代码审查**：
```plaintext
mdls review this Python function for potential issues: [代码]
```

## 最佳实践

- **问题设计**：提供清晰、具体的问题以进行有意义的模型比较。
- **模型选择**：根据任务类型选择具有互补优势的模型。
- **上下文包含**：在适当的情况下引用相关背景信息。
- **结果解读**：同时考虑模型得分和评估者的综合评价。
- **配置调整**：根据实际可用的模型更新 `config.json` 文件。
- **集成方式**：可选地使用 `update_modelshow_index.py` 来发布结果。

## 集成方式

- **本地存储**：结果以 JSON 和 Markdown 格式保存在 `config.outputDir` 中，便于后续使用或脚本处理。
- **网页展示**：使用 `update_modelshow_index.py` 将结果发布到网站上。
- **定时任务**：可以设置定时任务进行定期比较分析。
- **API 接口**：JSON 格式的结果支持程序化分析。

ModelShow 是人工智能模型评估领域的先进工具，它结合了严谨的方法论和实用的用户体验，适用于日常探索和专业评估。