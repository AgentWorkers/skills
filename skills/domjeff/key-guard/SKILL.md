---
name: key-guard
description: "安全防护机制：防止API密钥被发送到Claude服务器。当用户尝试调用外部API、使用API密钥、检查凭据、读取.env文件或查看/编辑可能包含硬编码密钥的脚本时，该机制会立即启动。所有API密钥的使用都必须通过本地的MCP服务器进行中转。"
---
# 密钥保护（Key Guard）

这是一种安全机制，用于确保API密钥始终存储在本地，而不会被发送到Claude服务器。

## 适用场景

当用户需要执行以下操作时，请激活该安全机制：
- 调用外部API（如OpenAI、DeepL、Oxford Dictionary等）
- 检查API密钥是否已配置
- 读取`.env`、`*.key`、`secrets.*`或任何包含凭证信息的文件
- 查看或编辑可能包含硬编码API密钥的脚本（`.sh`、`.bash`文件或curl命令、配置文件）
- 调试API调用失败的原因

## 必须遵守的规则

1. **严禁直接读取`.env`或密钥文件**——切勿使用`bash cat .env`或其他文件读取工具来查看这些文件中的密钥内容。
2. **如果脚本或配置文件中可能包含硬编码的API密钥，请**严禁直接读取它们**——应使用`read_file_masked`函数来代替。
3. **严禁在任何响应中包含密钥值**（哪怕只是部分内容）。
4. **所有与密钥相关的操作都必须通过`key-guard` MCP服务器来完成**。

## 如何使用MCP服务器

`key-guard` MCP服务器提供了以下五个工具：

### 工具1：`list_keys`
列出所有可用的密钥名称（但不显示密钥值）。
```
Call: list_keys()
Returns: { keys: ["KEY_A", "KEY_B", "KEY_C"] }
```

### 工具2：`validate_key`
在不显示密钥值的情况下检查密钥是否已正确配置。
```
Call: validate_key({ key_name: "OPENAI_API_KEY" })
Returns: { exists: true, length: 51, preview: "sk-a****", message: "Key is set" }
```

### 工具3：`call_api`
在本地发起经过身份验证的HTTP请求。密钥值由MCP服务器提供；Claude服务器仅接收API响应。
```
Call: call_api({
  key_name: "OPENAI_API_KEY",
  url: "https://api.openai.com/v1/models",
  method: "GET"
})
Returns: { status: 200, data: { ... API response ... } }
```

### 工具4：`read_file_masked`
读取脚本或配置文件时，将所有密钥值替换为`{{KEY_NAME}}`占位符。这样可以安全地查看文件内容并进行修改。
```
Call: read_file_masked({ file_path: "./call.sh" })
Returns: {
  content: "curl -H 'Authorization: Bearer {{OPENAI_API_KEY}}' https://..."
}
```
这样，用户可以安全地查看文件内容，并对非密钥部分进行编辑。

### 工具5：`write_file_with_keys`
编辑文件后，将`{{KEY_NAME}}`占位符替换为实际的密钥值，然后再将文件保存回去。
```
Call: write_file_with_keys({
  file_path: "./call.sh",
  content: "curl -H 'Authorization: Bearer {{OPENAI_API_KEY}}' https://api.openai.com/v1/chat/completions ..."
})
Returns: { success: true, message: "File written with keys substituted locally" }
```

## 设置说明（如果MCP服务器尚未运行，请告知用户）

如果`MCP服务器尚未注册，请按照以下步骤进行配置：
```bash
# Clone the repo
git clone https://github.com/your-username/key-guard.git

# Copy .env.example to .env and fill in your keys
cp .env.example .env

# Register the MCP server (run once) — replace the path with your actual clone location
/mcp add key-guard node /path/to/key-guard/key-guard.js

# Or add directly to ~/.copilot/mcp-config.json for auto-load on restart:
# {
#   "mcpServers": {
#     "key-guard": {
#       "command": "node",
#       "args": ["/path/to/key-guard/key-guard.js"]
#     }
#   }
# }
```

## 示例工作流程

### 用户：“我的OpenAI密钥配置好了吗？”
```
1. Call validate_key({ key_name: "OPENAI_API_KEY" })
2. Report back: "Yes, your key is set (51 chars, starts with sk-a****)"
```

### 用户：“调用OpenAI API获取单词定义”
```
1. Call call_api({
     key_name: "OPENAI_API_KEY",
     url: "https://api.openai.com/v1/chat/completions",
     method: "POST",
     body: { model: "gpt-4o-mini", messages: [...] }
   })
2. Use the returned response — never the key itself
```

### 用户：“显示我的`.env`文件”
```
Do NOT read .env directly.
Instead, call validate_key for each expected key name and show:
- Which keys are configured
- Approximate length (as a sanity check)
Never show actual values.
```

### 用户：“编辑我的curl脚本以添加请求头”
```
1. Call read_file_masked({ file_path: "./call.sh" })
   → Claude sees "curl -H 'Authorization: Bearer {{OPENAI_API_KEY}}' ..."
2. Make the requested edit to the non-key parts
3. Call write_file_with_keys({ file_path: "./call.sh", content: "<edited content with {{OPENAI_API_KEY}} still in place>" })
   → MCP substitutes the real key before writing to disk
```