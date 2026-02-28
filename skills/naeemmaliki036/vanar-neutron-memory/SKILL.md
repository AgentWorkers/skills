---
name: vanar-neutron-memory
description: 通过语义搜索来保存和检索代理内存。这种上下文信息会在每次会话中保持一致。
user-invocable: true
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": ["API_KEY"]}, "primaryEnv": "API_KEY"}}
---
# Neutron Memory

您的代理所做的每一次对话、偏好设置和决策都可以在会话之间持续保留。系统会保存重要的信息，当您需要时，语义搜索会根据内容的含义而非关键词来找到相关的上下文。每个新会话都是在前一个会话的基础上构建的。

## 工作原理

**手动方式** — 使用简单的命令进行保存和搜索：
1. `./scripts/neutron-memory.sh save "用户偏好暗模式" "偏好设置"` — 保存上下文
2. `./scripts/neutron-memory.sh search "用户喜欢什么主题"` — 根据含义进行搜索

**自动方式**（需手动启用） — 通过钩子自动捕获和调用信息：
- **自动捕获**：在每次AI轮次结束后保存对话内容
- **自动调用**：在每次AI轮次开始前查找相关的记忆内容，并将其作为上下文信息提供

## 快速入门

请参阅 **[SETUP.md](SETUP.md)** 以获取完整的设置指南。简而言之：
1. 在 **https://openclaw.vanarchain.com/** 获取免费的API密钥（免费提供20美元的信用额度，无需信用卡）
2. `export API_KEY=nk_your_key`
3. `./scripts/neutron-memory.sh test`

## 命令

### 保存
```bash
./scripts/neutron-memory.sh save "Content to remember" "Title"
```

### 搜索
```bash
./scripts/neutron-memory.sh search "what do I know about X" 10 0.5
```

参数：`QUERY` `LIMIT` `THRESHOLD(0-1)`

### 诊断
```bash
./scripts/neutron-memory.sh diagnose
```

系统会检查所有先决条件：curl、jq、API密钥、网络连接以及身份验证是否正常。

## 钩子（自动捕获与自动调用）

- `hooks/pre-tool-use.sh` — **自动调用**：在AI轮次开始前查询记忆内容，并将其作为上下文信息提供
- `hooks/post-tool-use.sh` — **自动捕获**：在AI轮次结束后保存对话内容

这两个功能默认是关闭的（需要手动启用）。要启用它们，请执行以下操作：
```bash
export VANAR_AUTO_RECALL=true
export VANAR_AUTO_CAPTURE=true
```

## API接口

- `POST /memory/save` — 保存文本（使用multipart/form-data格式）
- `POST /memory/search` — 进行语义搜索（请求体为JSON格式）

**身份验证**：`Authorization: Bearer $API_KEY` — 仅需要此身份验证信息，无需其他凭证。

## 安全性与隐私

**除非您执行了相关命令或明确启用了自动捕获/自动调用功能，否则不会发送任何数据。** 这两个钩子默认都是关闭的。

该功能仅会将您手动保存的数据（或通过自动捕获的对话内容）发送到Neutron API。具体发送的数据如下：

| 操作 | 发送的内容 | 发送的目标地址 |
|--------|------------|-------|
| **保存** | 您传递给 `save` 的文本或自动捕获的对话内容 | `POST /memory/save`（通过HTTPS） |
| **搜索** | 您的搜索查询文本 | `POST /memory/search`（通过HTTPS） |
| **自动调用** | 用户的最新消息（作为搜索查询） | `POST /memory/search`（通过HTTPS） |
| **自动捕获** | `用户：{message}\n助手：{response}` | `POST /memory/save`（通过HTTPS） |

**不会发送的内容：**
- 不会读取或上传任何本地文件
- 不会发送任何环境变量（除了用于身份验证的API密钥）
- 不会发送系统信息、文件路径或目录内容
- 不会发送来自其他工具或功能的数据

所有通信都通过HTTPS传输到 `api-neutron.vanarchain.com`。源代码完整保存在 `scripts/` 和 `hooks/` 目录中，仅包含三个简单的bash脚本，没有编译后的二进制文件。