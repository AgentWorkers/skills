# Memos技能的SKILL.md文档

## 目的

此技能提供了一个简单的接口，用于访问Memos API（https://usememos.com/docs/api）。它允许您在OpenClaw中创建、读取、删除和列出备忘录。

## 工作原理

- 该技能使用Python实现，并依赖于`requests`库。
- 它需要两个环境变量：
  - `MEMOS_URL` – **必需**。您的Memos实例的基URL（例如：`https://demo.usememos.com`）。
  - `MEMOS_TOKEN` – **必需**。用于身份验证的个人访问令牌。
- 如果`MEMOS_URL`或`MEMOS_TOKEN`未设置，该技能将立即终止并显示明确的错误信息。

## 命令

| 命令                         | 描述                                                                                                                                | 使用示例                                      |   |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- | --- |
| `create <内容> [可见性]` | 创建一个新的备忘录。`可见性`默认为`PUBLIC`（可选值：PRIVATE, PROTECTED, PUBLIC）。会自动添加`#openclaw`标签。 | `openclaw skill-run create "Hello world" "PUBLIC"` |
| `get <id>`                      | 根据ID检索备忘录。ID可以是`memos/123`的形式，也可以直接使用`123`。                                                                  | `openclaw skill-run get 123`                       |
| `delete <id> [force]`           | 删除备忘录。可选参数`force`（true/false）表示即使备忘录包含关联数据也会被删除。                                                   | `openclaw skill-run delete 123 true`               |
| `list [pageSize]`               | 分页列出备忘录。`pageSize`默认为20（最大1000）。                                                                          | `openclaw skill-run list 50`                       |

## 直接使用Python

您也可以直接使用Python来执行这些命令：

```bash
# Create a memo
python3 skills/memos/memos.py create "My memo content" "PUBLIC"

# Get a memo by ID
python3 skills/memos/memos.py get j9THXDmYtueosTTeHcC5NA

# Delete a memo
python3 skills/memos/memos.py delete j9THXDmYtueosTTeHcC5NA

# Delete with force
python3 skills/memos/memos.py delete j9THXDmYtueosTTeHcC5NA true

# List memos (default 20)
python3 skills/memos/memos.py list

# List with custom page size
python3 skills/memos/memos.py list 50
```

所有命令在成功时返回JSON格式的结果；在出错时，错误信息会输出到stderr中。

## 在OpenClaw中引用备忘录

当您创建或检索备忘录时，API会返回一个包含`uid`字段的备忘录对象。要在OpenClaw的输出中引用该备忘录，可以将其格式化为Markdown链接：

```markdown
[memo description](https://demo.usememos.com/memos/{uid})
```

**示例：**
如果API返回`{"uid": "ABC123xyz", "name": "memos/ABC123xyz", ...}`，则可以这样引用它：

```markdown
Created [your memo](https://demo.usememos.com/memos/ABC123xyz)
```

链接的格式为：`{MEMOS_URL}/memos/{uid}`，其中`uid`是从响应中提取的。

## 错误处理

该技能具有全面的错误处理机制：
- **API错误**：返回详细的错误信息，包括HTTP状态码和API响应详情。
- **网络错误**：处理超时（默认为30秒）和连接失败。
- **参数验证**：在调用API之前验证参数（例如：可见性选项、`pageSize`的范围）。
- **退出代码**：从命令行运行时，成功返回0，失败返回1。
- **错误输出**：所有错误都会以JSON格式输出到stderr中，便于解析。

错误响应示例：

```json
{
  "error": "Memos API Error",
  "message": "HTTP 404: Not Found - Memo not found",
  "status_code": 404
}
```

## 扩展技能

- 可以按照现有命令的模式添加新的命令。
- 如果Memos API添加了新的端点，您可以创建相应的函数。

---

**注意：**此技能仅供个人使用；切勿公开分享您的`MEMOS_TOKEN`。