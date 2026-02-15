---
name: feishu-doc-reader
description: 使用 Feishu（Lark）的官方 Open API 读取并提取文档内容
metadata: {"moltbot":{"emoji":"📄","requires":{"bins":["python3","curl"]}}}
---

# Feishu 文档阅读器

该技能允许使用 Feishu 官方 Open API 读取和提取 Feishu（Lark）文档中的内容。

## 配置

### 设置技能

1. 在 `./reference/feishu_config.json` 文件中创建配置文件，并填写您的 Feishu 应用程序凭据：

```json
{
  "app_id": "your_feishu_app_id_here",
  "app_secret": "your_feishu_app_secret_here"
}
```

2. 确保脚本可执行：
```bash
chmod +x scripts/read_doc.sh
chmod +x scripts/get_blocks.sh
```

**安全提示**：配置文件应妥善保管，切勿提交到版本控制系统中。建议使用适当的文件权限设置（例如：`chmod 600 ./reference/feishu_config.json`）。

## 使用方法

### 基本文档阅读

要读取 Feishu 文档，您需要文档令牌（该令牌位于以下 URL 中：`https://example.feishu.cn/docx/DOC_TOKEN`）。

**推荐使用 shell 脚本：**
```bash
# Make sure environment variables are set first
./scripts/read_doc.sh "your_doc_token_here"

# Or specify document type explicitly
./scripts/read_doc.sh "docx_token" "doc"
./scripts/read_doc.sh "sheet_token" "sheet"
```

### 获取详细的文档块（新功能）

要获取包含所有块的完整文档结构，请使用专门的块处理脚本：

```bash
# Get full document blocks structure
./scripts/get_blocks.sh "docx_AbCdEfGhIjKlMnOpQrStUv"

# Get specific block by ID
./scripts/get_blocks.sh "docx_token" "block_id"

# Get blocks with children
./scripts/get_blocks.sh "docx_token" "" "true"
```

**直接使用 Python 处理文档块：**
```bash
python scripts/get_feishu_doc_blocks.py --doc-token "your_doc_token_here"
python scripts/get_feishu_doc_blocks.py --doc-token "docx_token" --block-id "block_id"
python scripts/get_feishu_doc_blocks.py --doc-token "docx_token" --include-children
```

### 支持的文档类型

- **Docx 文档**（新版本的 Feishu 文档）：可提取完整内容（包括块、元数据和结构）
- **Doc 文档**（旧版本）：仅可提取基本元数据
- **Sheets（电子表格）**：可提取完整的电子表格数据并支持页面导航
- **Slides（幻灯片）**：仅可提取基本元数据（提取内容需要额外权限）

## 功能特点

### 增强的内容提取功能
- **结构化输出**：输出格式为清晰的 JSON，包含文档元数据、内容块及层次结构
- **完整块访问**：可访问所有文档块（包括文本、表格、图片、标题、列表等）
- **块层次结构**：准确反映块之间的父子关系
- **文本提取**：能够从复杂的块结构中自动提取文本
- **表格支持**：正确解析表格的行和列结构
- **图片处理**：提取图片的 URL 和元数据
- **链接解析**：解析内部和外部链接

### 支持的块类型
- **text**：纯文本和富文本内容
- **heading1/2/3**：具有正确层次结构的文档标题
- **bullet/ordered**：支持嵌套的列表项
- **table**：包含单元格和格式的完整表格结构
- **image**：包含图片 URL 和元数据的图片块
- **quote**：带引号的文本块
- **code**：带有语言检测功能的代码块
- **equation**：数学公式
- **divider**：水平分隔符
- **page**：多页文档中的分页信息

### 错误处理与诊断
- **详细的错误信息**：针对常见问题提供清晰的解释
- **权限验证**：在发起请求前检查所需的权限
- **令牌验证**：在处理前验证文档令牌的有效性
- **重试机制**：针对短暂的网络故障自动重试
- **速率限制**：优雅地处理 API 的速率限制

### 安全特性
- **安全的凭据存储**：支持使用环境变量或安全文件存储方式
- **禁止记录凭据**：凭据不会出现在日志或输出中
- **最小权限使用**：仅请求应用程序所需的 API 权限
- **访问令牌缓存**：高效地重用令牌以减少 API 调用次数

## 命令行选项

### 主要文档阅读器
```bash
# Python script options
python scripts/read_feishu_doc.py --help

# Shell script usage
./scripts/read_doc.sh <doc_token> [doc|sheet|slide]
```

### 块阅读器（新功能）
```bash
# Get full document blocks
./scripts/get_blocks.sh <doc_token>

# Get specific block
./scripts/get_blocks.sh <doc_token> <block_id>

# Include children blocks
./scripts/get_blocks.sh <doc_token> "" true

# Python options
python scripts/get_feishu_doc_blocks.py --help
```

## 所需的 API 权限

您的 Feishu 应用程序需要以下权限：
- `docx:document:readonly` - 读取文档内容
- `doc:document:readonly` - 读取旧版本文档内容
- `sheets:spreadsheet:readonly` - 读取电子表格内容

## 错误处理

常见错误及解决方法：
- **403 Forbidden**：检查应用程序权限和文档共享设置
- **404 Not Found**：确认文档令牌正确且文档存在
- **令牌过期**：访问令牌的有效期为 2 小时，必要时请刷新令牌
- **App ID/Secret 无效**：在 Feishu Open Platform 中重新核对您的凭据
- **权限不足**：确保应用程序具有所需的 API 权限
- **99991663**：应用程序无权限访问该文档
- **99991664**：文档不存在或已被删除
- **99991668**：令牌过期，需要刷新令牌

## 示例

### 提取包含完整结构的文档
```bash
# Read document
./scripts/read_doc.sh "docx_AbCdEfGhIjKlMnOpQrStUv"
```

### 获取完整的文档块（新功能）
```bash
# Get all blocks with full structure
./scripts/get_blocks.sh "docx_AbCdEfGhIjKlMnOpQrStUv"

# Get specific block details
./scripts/get_blocks.sh "docx_AbCdEfGhIjKlMnOpQrStUv" "blk_xxxxxxxxxxxxxx"
```

### 处理电子表格数据
```bash
./scripts/read_doc.sh "sheet_XyZ123AbCdEfGhIj" "sheet"
```

### 仅提取文本内容（Python 脚本）
```bash
python scripts/read_feishu_doc.py --doc-token "docx_token" --extract-text-only
```

## 安全提示

- **切勿提交凭据**：不要将应用程序的敏感信息提交到版本控制系统中
- **使用最小权限**：仅请求应用程序实际需要的权限
- **设置安全的文件权限**：为敏感文件设置适当的权限（例如：`chmod 600`）
- **环境隔离**：在开发和生产环境中使用不同的应用程序
- **审计访问权限**：定期审查应用程序可以访问的文档

## 故障排除

### 认证问题
1. 在 Feishu Open Platform 中核对您的 App ID 和 App Secret
2. 确保应用程序已发布并具有所需的权限
3. 检查环境变量或配置文件是否设置正确
4. 使用 `test_auth.py` 脚本测试凭据是否有效

### 文档访问问题
1. 确保文档已与您的应用程序共享或位于可访问的位置
2. 核对文档令牌的格式（应以 `docx_`、`doc_` 或 `sheet_` 开头）
3. 检查文档是否需要额外的共享权限

### 网络问题
1. 确保您的服务器能够访问 `open.feishu.cn`
2. 在受限环境中运行时，请检查防火墙规则
3. 脚本包含针对短暂网络故障的重试机制

### 特定块相关问题
1. **空块响应**：文档可能为空或没有可访问的块
2. **缺少某些块类型**：某些块类型可能需要额外的权限
3 **层次结构不完整**：使用 `--include-children` 标志以获取完整的块树结构

## 参考资料

- [Feishu Open API 文档](https://open.feishu.cn/document)
- [文档 API 参考](https://open.feishu.cn/document/server-docs/docs/docx-v1/document)
- [块 API 参考](https://open.feishu.cn/document/server-docs/docs/docx-v1/block)
- [认证指南](https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token_internal)
- [电子表格 API 参考](https://open.feishu.cn/document/server-docs/sheets-v3/introduction)