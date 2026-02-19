---
name: credence
description: 在安装任何 MCP 服务器或 AI 工具之前，请先将其与 Credence 信任注册表进行比对。该注册表会从 0 到 100 的范围内对工具的安全性、来源以及行为风险进行评分。
user-invocable: true
metadata: {"openclaw": {"emoji": "🛡️", "requires": {"bins": ["curl"]}, "os": ["darwin", "linux", "win32"], "tags": ["security", "trust", "mcp"]}}
---
# Credence

在安装MCP服务器和AI工具之前，请先通过Credence信任注册表对其进行验证。

## 适用场景

- 在安装任何MCP服务器之前
- 当用户请求添加MCP服务器或AI工具时
- 当您需要验证某个工具的安全性时
- 当用户请求执行`/credence`命令时

## 工作原理

Credence会扫描MCP服务器和AI工具，检查其是否存在安全问题，验证其来源，并评估其行为风险。每个被扫描的工具都会获得一个0到100分的信任评分以及相应的评估结果：

| 评分 | 评估结果 | 含义 |
|-------|---------|---------|
| 90-100 | 已批准 | 可以安全安装 |
| 70-89 | 条件性批准 | 安装前请查看相关警告信息 |
| 40-69 | 被标记为有问题 | 仅在对风险有充分了解的情况下才能安装 |
| 0-39 | 被拒绝 | 请勿安装 |

## 使用说明

### 按名称或URL检查服务器

1. 获取Credence注册表信息，并查找相应的服务器：
   ```bash
curl -s "https://raw.githubusercontent.com/pestafford/credence-registry/main/registry/index.json"
```

2. 在`servers`数组中根据`server_id`、`server_name`、`canonical_name`或`repo_url`进行搜索。搜索结果不必完全匹配，部分匹配也是可以的。
   **如果找到服务器**：
   ```
Credence: <server_name>
  Score: <trust_score>/100
  Verdict: <thinktank_verdict>
  Scanned: <attested_at>
  Registry: https://credence.securingthesingularity.com/registry.html
```

3. 根据评分给出建议：
   - **已批准（评分90分及以上）**：可以安全安装。
   - **条件性批准（评分70-89分）**：建议用户先查看注册表页面以获取详细信息。
   - **被标记为有问题（评分40-69分）**：警告用户，未经确认请勿安装。
   - **被拒绝（评分0-39分）**：存在严重问题，请勿安装。

### 安装前进行验证

无论您是通过`claude mcp add`命令、编辑`claude_desktop_config.json`文件还是其他方式准备安装或连接MCP服务器，都应先使用Credence进行验证。如果服务器未在注册表中，请告知用户该服务器尚未经过扫描，并询问用户是否仍要继续安装。

### 获取详细信息

如需了解特定服务器的更多信息，可以获取其认证文件。认证文件的路径位于索引条目中（路径格式为：```
https://raw.githubusercontent.com/pestafford/credence-registry/main/registry/
```）。

认证文件包含完整的评分详情（安全性、来源信息、行为风险分析）、扫描元数据以及评估结果。

## 示例

**用户请求：**“添加这个文件系统MCP服务器”
1. 获取注册表索引。
2. 查找`modelcontextprotocol/servers/filesystem`服务器——评分88分，属于“已批准”状态。
3. 报告：“Credence评分：88/100（已批准）。可以安全安装。”
4. 继续安装。

**用户请求：**“安装某个未知服务器”
1. 获取注册表索引。
2. 未找到该服务器。
3. 报告：“该服务器尚未经过Credence的扫描。您可以通过https://credence.securingthesingularity.com/#submit提交相关信息——是否仍要继续安装？”

**用户请求：**`/credence modelcontextprotocol/servers/memory`
1. 获取注册表索引。
2. 找到该服务器——评分98分，属于“已批准”状态。
3. 报告完整的评估结果。

## 注意事项

- Credence注册表是公开的，无需任何认证即可访问。
- 评分基于自动化扫描和人工智能分析得出。
- 如果某个工具未出现在注册表中，并不意味着它存在安全风险，只是尚未被扫描而已。
- 有关完整的评估方法，请参阅：https://credence.securingthesingularity.com/faq.html