---
name: claw-trace
license: MIT
description: >
  **功能描述：**  
  跟踪并可视化 OpenClaw 代理的工作流程。记录工具调用的输入参数、输出结果、执行耗时以及状态，并以易于阅读的格式呈现这些信息。  
  **重要提示：**  
  当配置 `enable = true` 时，该功能将在每次工具调用后自动显示追踪结果，无需用户手动触发“显示追踪”命令。  
  **适用范围：**  
  仅适用于 OpenClaw 平台。
---
# Claw Trace - 工作流程可视化

该功能用于记录并显示AI代理的工作流程。

## 可配置的功能模块

用户可以通过命令“enable XX feature”或“use simple mode”来切换不同的功能模块。

### 模块1：调用记录（默认启用）

| 步骤 | 工具 | 输入 | 结果 | 所需时间 |
|------|------|-------|--------|----------|
| 1 | web_search | 查询内容：xxx | ❌ 失败 | 0ms |
| 2 | web_fetch | 网址：xxx | ✅ 成功 | 230ms |

### 模块2：流程图（默认启用）

[用户请求]
    ↓
1. web_search → ❌
    ↓
2. web_fetch → ✅
    ↓
[回复用户]

### 模块3：统计信息（可选）

```
📊 Work Statistics
⏱️ Total Time: 8.5s
🔧 Tool Calls: 15 times
✅ Success Rate: 87% (13/15)

📈 Tool Usage Ranking:
  1. web_fetch  - 10 times (67%)
  2. exec       - 3 times (20%)
```

### 模块4：详细日志（可选）

记录每次调用的完整输入/输出内容（敏感信息除外）。

### 模块5：保存到文件（可选）

生成Markdown格式的报告并保存到工作区。

### 模块6：过滤器（可选）

根据多种条件过滤工具调用：

| 过滤类型 | 命令 | 例子 |
|-------------|---------|---------|
| 按工具名称过滤 | "filter: tool_name" | "filter: web_search" |
| 按结果过滤 | "filter: success" / "filter: failed" | "filter: failed" |
| 按时间过滤 | "filter: last N calls" | "filter: last 5 calls" |
| 按关键词过滤 | "filter: keyword in output" | "filter: error" |
| 可以组合多个过滤条件：| "filter: web_search and failed" |

### 模块7：导出格式（可选）

可以选择导出格式：
- Markdown（默认）
- JSON
- HTML（带语法高亮）

## 使用方法

### 配置文件

该功能有一个名为`config.json`的配置文件，其中包含以下配置选项：

```json
{
  "enable": false,        // Whether to enable by default (default: false, on-demand)
  "mode": "simple",       // Mode: simple / full
  "enabledModules": {
    "table": true,        // Call table
    "flowchart": true,   // Flowchart
    "statistics": false,  // Statistics
    "detailedLog": false,// Detailed log
    "saveToFile": false  // Save to file
  },
  "language": "auto"       // Language: auto / zh / en
}
```

### 用户命令

用户可以通过对话来修改配置：

| 命令 | 功能 |
|---------|--------|
| "enable trace" | 启用跟踪功能 |
| "disable trace" | 关闭跟踪功能 |
| "use simple mode" | 使用简单模式 |
| "use full mode" | 使用完整模式 |
| "enable statistics" | 启用统计信息 |
| "enable filters" | 启用过滤器 |
| "filter: tool_name" | 按工具名称过滤 |
| "filter: success/failed" | 按结果过滤 |
| "filter: last N calls" | 按调用次数过滤 |
| "output in English" | 输出语言设置为英语 |
| "output in Chinese" | 输出语言设置为中文 |

### 工作流程

1. **每次调用该功能时**：首先读取`config.json`以获取当前配置。
2. **根据配置**：
   - 如果`enable`设置为`false`，则不显示跟踪信息（除非用户明确要求）。
   - 如果`enable`设置为`true`，则**每次工具调用后**必须自动显示跟踪结果，无需用户另行请求。
3. **当用户修改配置时**：更新`config.json`文件并保存。

### ⚠️ 重要规则

**当`enable`设置为`true`时，每次工具调用后必须自动在回复中包含跟踪结果，无需用户另行请求！**

### 语言自动检测

- 输出语言会根据用户的语言设置自动调整：
  - 如果用户使用中文，则输出中文；
  - 如果用户使用英语，则输出英文。

## 注意事项

- 敏感信息（如API密钥、密码）不应被记录。
- 对过长的输出内容进行截断（例如使用“[...]”）。
- 明确显示调用失败的原因。
- 保持输出简洁，避免过度详细。

## ⚠️ 安全指南

### 敏感数据的处理（强制要求）

在显示任何工具调用的输入/输出内容之前，必须对以下信息进行隐藏：

**必须隐藏的内容**：
- API密钥、令牌、密码（格式：`key=`, `token=`, `password=`, `Authorization:`）
- 可能包含机密信息的文件内容
- 用户凭证或私人数据

**隐藏方法**：
- 用`[REDACTED]`或`[HIDDEN]`替换这些内容。
- 保持原有的结构，但隐藏具体值。
- 例如：`{"api_key": "sk-xxx"}` → `{"api_key": "[REDACTED]"}`

### 安全默认设置

默认配置如下：
- `enable: false`（默认关闭，用户需要手动启用）
- `detailedLog: false`（不记录完整的输入/输出内容）
- `saveToFile: false`（不将数据保存到磁盘）

### 最佳实践

1. **启用前先进行测试**——先在安全环境中启用该功能。
2. **检查输出内容**——确保跟踪记录中不包含任何敏感信息。
3. **在生产环境中使用简单模式**——避免进行详细日志记录。
4. **使用完毕后立即关闭**——不再需要时立即关闭该功能。