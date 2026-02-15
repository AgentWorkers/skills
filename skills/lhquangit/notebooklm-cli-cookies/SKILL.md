---
name: notebooklm-cli
description: 使用 nlm CLI 在已上传到 NotebookLM 的文档中搜索并回答问题。当用户需要查找信息、总结资料内容或查询特定的 NotebookLM 笔记本时，可以使用该工具。
metadata: {"openclaw":{"requires":{"bins":["nlm"],"env":["NOTEBOOKLM_MCP_CLI_PATH"]}}}
user-invocable: true
---

# NotebookLM CLI

## 使用目的

当用户希望搜索或查询 NotebookLM 中已存在的内容时，可以使用此技能。

此技能的前提条件包括：
- `nlm` 已安装（通过 `notebooklm-mcp-cli` 包安装）。
- 无头运行时（headless runtime）的认证已经完成。
- `NOTEBOOKLM_MCP_CLI_PATH` 指向认证存储目录。

## 必须遵守的规则（避免错误使用工具）

当用户提到以下内容时，应视为明确要求查询 NotebookLM：
- “NotebookLM”、“notebooklm”
- “notebook alias”（笔记本别名）
- 已知的别名（例如：`tai_lieu_dien`、`nlm_tai_lieu_dien`）

在这些情况下：
- 必须通过 `Exec` 命令来执行 `nlm`，切勿直接从内存中获取答案。
- 除非用户明确要求使用网络搜索，否则不要切换到网络搜索方式。
- 如果查询结果不在 NotebookLM 中，应如实告知用户（根据 `nlm` 的返回结果）。

**命令格式说明：**
- 如果用户通过 Telegram 中的 `/nlm ...` 调用此技能，应将 `/nlm` 后面的文本视为 `nlm` 的参数。
- 必须通过 `Exec` 命令执行 `nlm <args>`，并返回相关的标准输出（stdout）。

## 运行时检查

在执行查询之前，需要完成以下检查：
1. 验证认证路径是否配置正确：
```bash
echo "$NOTEBOOKLM_MCP_CLI_PATH"
```
2. 验证用户的登录状态：
```bash
nlm login --check
```

如果认证检查失败，应停止操作并要求用户重新进行认证（切勿在 AWS 运行时中使用浏览器登录）。

## 查询流程
1. 列出所有笔记本：
```bash
nlm notebook list --json
```
2. 选择笔记本：
  - 如果用户提供了笔记本 ID，直接使用该 ID。
  - 如果用户提供了笔记本标题，从列表中解析出对应的 `notebook_id`（不要将原始标题直接传递给 `nlm notebook get/source list/query` 命令）。
  - 如果用户提供了别名，使用该别名。
  - 如果别名不明确，要求用户选择具体的笔记本。
3. 执行查询：
```bash
nlm notebook query "<notebook_id_or_alias>" "<user_question>"
```
4. 返回查询结果，并说明查询的是哪个笔记本。

**注意事项：**
- `nlm notebook list` 命令返回的是笔记本的标题，但许多其他命令需要笔记本的 ID（UUID）或别名。直接传递标题（如 “tài liệu điện”）可能会导致返回空结果。
- 如果用户经常需要查询同一个笔记本，建议为其创建一个别名并统一使用（例如：`tai_lieu_dien`）。

## Telegram 提示模板（可复制/粘贴）

以下两种格式均可用于可靠地触发此技能：
1) 强制使用 CLI 查询：
```text
Chạy lệnh: nlm notebook query tai_lieu_dien "giá của A9N61500 là bao nhiêu? Nếu notebook không có thông tin giá thì trả lời: không thấy trong NotebookLM."
```

2) 以自然语言表达，但需明确说明查询需求：
```text
Trong NotebookLM notebook alias tai_lieu_dien: trả lời câu hỏi "giá của A9N61500 là bao nhiêu?". Bắt buộc dùng nlm để truy vấn, không tìm web, không đọc file local.
```

## 输出规范
- 明确指出查询的笔记本信息（如果有的话，包括标题和 ID）。
- 如果查询结果为空或不明确，建议用户提供更具体的查询条件。
- 回答应简洁且基于 NotebookLM 的实际返回内容。

## 常见错误及解决方法：
- **认证过期** / **401** / **403** 错误：
  - 检查 `NOTEBOOKLM_MCP_CLI_PATH` 的配置是否正确。
  - 确保 `profiles/default/cookies.json` 和 `profiles/default/metadata.json` 文件存在。
  - 在非 AWS 环境中刷新浏览器缓存，然后重新设置密钥。
- **`nlm: command not found` 错误**：
  - 安装 `notebooklm-mcp-cli` 包（推荐使用 `pipx install notebooklm-mcp-cli`），或使用 `uv tool install notebooklm-mcp-cli` 进行安装。

## 命令参考
```bash
# List notebooks
nlm notebook list --json

# Query notebook by id or alias
nlm notebook query "<notebook_id_or_alias>" "<question>"

# Check auth status
nlm login --check
```