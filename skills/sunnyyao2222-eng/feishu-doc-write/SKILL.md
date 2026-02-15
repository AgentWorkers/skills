---
name: feishu-doc-writer
description: Feishu（Lark）文档API编写规范：  
该规范用于将Markdown格式的内容转换为Feishu的区块结构，并将其写入云端文档。同时支持并发处理和有序执行操作。适用于同步文章、创建文档区块，或向Feishu文档中编写长篇内容等场景。
---

# Feishu 文档编写器

本文档提供了通过 Docx API 将内容写入 Feishu（Lark）云文档的参考规范。Feishu 文档采用 **块树模型**，因此不支持原始的 Markdown 格式。

### 首选方法：使用转换 API

Feishu 提供了一个官方的 **Markdown -> 块** 转换接口，可以自动将 Markdown 内容转换为 Feishu 支持的块结构：

**优点**：无需手动构建块 JSON 数据；支持大部分标准的 Markdown 格式。  
**限制**：不支持 Feishu 特有的块类型（如 Callout 等），这些类型需要手动创建。

## 块类型参考

| 块类型 | 名称 | JSON 键 | 说明 |
|---------|------|---------|--------|
| 1       | Page    | `page`   | 文档根节点 |
| 2       | Text    | `text`   | 段落     |
| 3-11     | Heading1-9 | `heading1`-`heading9` | 标题     |
| 12       | Bullet   | `bullet`  | 无序列表   |
| 13       | Ordered | `ordered` | 有序列表   |
| 14       | Code    | `code`   | 代码块     |
| 15       | Quote    | `quote`   | 引用      |
| 17       | Todo    | `todo`   | 待办事项   |
| 19       | Callout   | `callout` | 高亮框     |
| 22       | Divider   | `divider` | 水平分隔线   |
| 27       | Image    | `image`   | 两步上传图片  |
| 31       | Table    | `table`   | 表格      |
| 34       | QuoteContainer | `quote_container` | 引用容器   |

## 创建块的 API

调用以下 API 来创建新的块：

```json
{
  "block_id": "parent_block_id",  // 父块 ID（通常是文档 ID）
  "index":     // 插入位置（0 表示开头，-1 表示末尾）
}
```

### 块的 JSON 示例

- **文本块**：
```json
{
  "type": "Text",
  "text": "这是示例文本"
}
```

- **标题块**：
```json
{
  "type": "Heading1",
  "text": "这是一个标题"
}
```

- **无序列表**：
```json
{
  "type": "Bullet",
  "items": ["项目1", "项目2", "项目3"]
}
```

- **有序列表**：
```json
{
  "type": "Ordered",
  "items": ["项目1", "项目2", "项目3"]
}
```

- **代码块**：
```json
{
  "type": "Code",
  "language": "JavaScript",
  "code": "console.log("Hello, world!")
}
```

### Feishu 特有的 Callout 高亮框

Callout 是一个 **容器块**，需要先创建容器，然后再添加子块：

```json
{
  "type": "Callout",
  "content": "这是一个高亮框",
  "color": "red"
}
```

### 颜色设置

- `color`: 可选颜色（红色、橙色、黄色、绿色、蓝色、紫色、灰色）

### 分隔线：
```json
{
  "type": "Divider",
  "style": "solid"
}
```

### 图片上传（两步操作）

- 首先创建图片占位符，然后上传图片文件。

### 文本样式

可以通过 `text_element_style` 属性来设置文本样式：

| 属性      | 类型      | 效果       |
|-----------|---------|-----------|
| bold       | bool      | 加粗        |
| italic     | bool      | 斜体        |
| strikethrough | bool      | 下划线      |
| underline    | bool      | 下划线      |
| inline_code   | bool      | 内联代码     |
| text_color   | int       | 文本颜色     |
| background_color | int       | 背景颜色     |
| link.url    | string     | 超链接      |

在一个块中可以包含多个 `text_run` 元素，从而实现混合样式。

### Markdown 与块结构的对应关系

| Markdown 格式 | Feishu 块类型 | JSON 键       |
|------------|-------------|--------------|
| #H1       | 3           | `heading1`      |
| ##H2       | 4           | `heading2`      |
| ###H3       | 5           | `heading3`      |
| Paragraph    | 2           | `text`        |
| -item       | 12          | `bullet`       |
| 1. item     | 13          | `ordered`       |
| Code       | 14          | `code`        |
| >quote      | 15          | `quote`        |
| [-[ ]todo     | 17          | `todo`       |
| ---        | 22          | `divider`       |
| ![](url)     | 27          | `image`        |
| **bold**     | ```text_element_style.bold: true`` | **加粗**     |
| *italic*     | ```text_element_style.italic: true`` | **斜体**     |
| ```code` ``   | ```text_element_style.inline_code: true`` | **内联代码**   |
| ~~strike~~    | ```text_element_style.strikethrough: true`` | **删除线**     |
| `[text](url)`   | ```text_element_style.link.url`` | **超链接**     |
| （无对应 Markdown 标签）| 19          | `callout`      | **高亮框**     |

### 并发与顺序问题

**问题**：同时调用创建块的 API 会导致块顺序混乱。

**解决方案 A**：**批量请求**（推荐）：将所有块放入一个数组中，然后一次性发送 API 请求。

**解决方案 B**：**按顺序发送请求**：对于较长的内容，使用明确的 `index` 值逐个发送请求。

**解决方案 C**：**先收集数据再写入**：避免使用并发 API 请求同时写入一个段落。

## 完整的写入流程

1. **创建文档**：发送 POST 请求到 `/open-apis/docx/v1/documents`，参数为 `{ "folder_token": "<token>", "title": "文档标题" }`，返回 `document_id`。
2. **构建块数组**：将所有内容转换为 JSON 格式的块数据。
3. **批量写入**：发送 POST 请求到 `.../documents/{doc_id}/blocks/{doc_id}/children?documentrevision_id=-1`，传入所有块的 JSON 数据。
4. **特殊块类型**（如 Callout）：从步骤 3 的响应中获取对应的 `block_id`，然后添加子块。

### 自定义 Callout 标记语法

由于 Markdown 中没有直接对应的 Callout 标签，可以使用以下自定义标记：

```markdown
<callout color="yellow" emoji="bulb" border="red">
  这是一个自定义的高亮框。
</callout>
```

### 注意事项

- 每个列表项都必须是一个独立的块。
- 在编写文档时，不要尝试在列表中嵌套代码块，因为 Feishu 的架构对此有严格限制。
- 使用自定义标记时，请遵循上述语法和参数。

## 其他注意事项

- 每批最多建议创建 50 个块。
- 长篇文章应按照 H2/H3 标题分段发送，每批请求之间间隔 200-500 毫秒。
- 始终使用 `documentrevision_id=-1` 以获取最新版本的文档。
- 令牌的有效期为约 2 小时，过期前请刷新令牌。

## 认证机制

Feishu 文档编写器需要用户认证。

## 常见问题与注意事项

- **注意事项**：
  - 不支持在文档中插入 Markdown 表格，应使用无序列表代替。
  - 不允许在列表中嵌套代码块，Feishu 对嵌套深度有严格要求。
  - Callout 是一个容器块，必须先创建容器再添加子块。
  - 每个列表项都必须是一个独立的块。

### 参考链接

- 创建块的 API：[https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/document-docx/docx-v1/document-block-children/create](...)
- 块数据结构：[https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/document-docx/docx-v1/data-structure/block](...)
- 转换 API：[https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/document-docx-v1/document/convert](...)
- 更详细的 API 参考：请查看工作区根目录下的 `FEISHU_API_HANDBOOK.md` 文件。