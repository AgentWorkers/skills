---
name: feishu-md2blocks
description: 将富文本Markdown内容（包括表格）插入到Feishu文档中。当使用`feishu_doc write/append`命令处理表格时遇到问题，或者需要将格式复杂的文本内容（如表格、代码块、嵌套列表）插入到现有文档的特定位置时，可以使用此方法。
---
# 将 Markdown 内容（包括表格）插入 Feishu 文档中

您可以使用 Feishu 的 `block_convert` 和 `descendant` API 将 Markdown 内容（包括表格）插入到 Feishu 文档中。

## 使用场景

- `feishu_doc` 的 `write` 方法用于替换整个文档；如果您希望将内容插入文档的特定位置，可以使用此方法。
- `feishu_doc` 的 `create_table_with_values` 方法在处理大型表格时存在局限性。
- 当您需要向现有文档中插入表格、代码块或复杂的嵌套内容时，可以使用这些 API。

## 使用方法

```bash
# Insert from file (appends to document end)
python3 <skill_dir>/scripts/md2blocks.py <doc_token> content.md

# Insert from stdin
echo "| A | B |\n|---|---|\n| 1 | 2 |" | python3 <skill_dir>/scripts/md2blocks.py <doc_token> -

# Insert after a specific block
python3 <skill_dir>/scripts/md2blocks.py <doc_token> content.md --after <block_id>

# Replace all content
python3 <skill_dir>/scripts/md2blocks.py <doc_token> content.md --replace
```

## 工作原理

1. 调用 `POST /docx/v1/documents/blocks/convert` 将 Markdown 内容转换为 Feishu 文档中的块结构。
2. 从表格块中删除 `merge_info` 字段（该字段为只读字段，可能会导致插入错误）。
3. 调用 `POST /docx/v1/documents/{doc}/blocks/{parent}/descendant` 将转换后的块插入到文档中。

`descendant` API 可以处理嵌套结构（例如包含文本的表格），而较简单的 `/children` API 则无法处理这类结构。

## 位置控制

`--after <block_id>` 选项用于将内容插入到指定块之后。脚本会自动识别该块的索引位置。

**重要提示：** `/descendant` API 的 `index` 参数必须放在请求体中，而不能作为 URL 查询参数传递。如果在 URL 中添加 `?index=N`，该参数会被忽略（内容会直接追加到文档的末尾）。脚本会自动处理这种情况。

## 支持的 Markdown 格式

- 文本
- 标题（h1-h9）
- 列表（无序列表、有序列表）
- 代码块
- 引用
- 表格
- 待办事项
- 分隔符

## 限制事项

- Markdown 中的图片不会自动上传；需要单独进行上传操作。
- 每次插入操作最多支持 1000 个块；如果文档内容过多，可能需要分批处理。
- 使用这些 API 需要具有 `docx:document.block:convert` 的权限。
- 文档的编辑频率限制为：每秒每个文档最多 3 次操作。

## 参考资料

有关完整的块级 API 参考信息，请参阅 `feishu-block-ops` 技能文档，其中包含以下内容：
- 所有的块级 API（创建、读取、更新、删除、批量操作）
- 块类型说明
- 表格操作方法（批量编辑、合并单元格）
- 常见问题及注意事项