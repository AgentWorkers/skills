---
name: docuseal
description: 管理 DocuSeal 文档模板和电子签名功能。
license: MIT
metadata:
   version: "1.0.2"
   author: "DocuSeal"
   clawdbot:
      emoji: "📝"
      homepage: "https://docuseal.com"
      credential: DOCUSEAL_MCP_TOKEN
      requires:
         env:
            - DOCUSEAL_URL
            - DOCUSEAL_MCP_TOKEN
---
# DocuSeal 应用技能

通过 DocuSeal 的 MCP （Master Control Panel）端点来管理文档模板和电子签名。

## 设置

1. 在 DocuSeal 的设置中启用 MCP（设置 > MCP）
2. 创建一个 MCP 令牌
3. 设置环境变量：
   ```bash
   export DOCUSEAL_URL="https://your-docuseal-instance.com"
   export DOCUSEAL_MCP_TOKEN="your-mcp-token"
   ```

## 协议

所有请求均使用 JSON-RPC 2.0 协议，通过 HTTP POST 发送到 `$DOCUSEAL_URL/mcp`。

## 与 scripts/cli.js 的配合使用

需要 Node.js 18 及以上版本。无需额外依赖。

```bash
node scripts/cli.js init
node scripts/cli.js tools
node scripts/cli.js search-templates --q="contract" --limit=5
node scripts/cli.js create-template --url="https://example.com/document.pdf" --name="My Template"
node scripts/cli.js send-documents --template-id=1 --emails="signer@example.com,another@example.com"
node scripts/cli.js search-documents --q="john@example.com" --limit=5
```

## 命令参考

### search-templates

按名称搜索文档模板。

| 选项 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `--q` | 字符串 | 是 | 用于按名称过滤模板的搜索查询 |
| `--limit` | 整数 | 否 | 返回的模板数量（默认为 10） |

### create-template

从 PDF URL 创建模板。

| 选项 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `--url` | 字符串 | 是 | 要上传的文档文件的 URL |
| `--name` | 字符串 | 否 | 模板名称（默认为文件名） |

### send-documents

将文档模板发送给指定的提交者进行签名。

| 选项 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `--template-id` | 整数 | 是 | 模板标识符 |
| `--emails` | 字符串 | 是 | 以逗号分隔的提交者电子邮件地址列表 |

### search-documents

按提交者名称、电子邮件、电话或模板名称搜索已签名或待签名的文档。

| 选项 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `--q` | 字符串 | 是 | 按提交者名称、电子邮件、电话或模板名称进行搜索 |
| `--limit` | 整数 | 否 | 返回的结果数量（默认为 10） |

## 注意事项

- 需要 Node.js 18 及以上版本（使用内置的 `fetch` 函数，无需额外依赖）
- 所有响应均遵循 JSON-RPC 2.0 格式
- 必须设置 `DOCUSEAL_URL` 和 `DOCUSEAL_MCP_TOKEN` 环境变量
- 使用前必须在账户设置中启用 MCP
- 令牌仅在创建时显示一次——请妥善保管