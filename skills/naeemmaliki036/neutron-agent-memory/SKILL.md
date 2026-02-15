---
name: neutron-agent-memory
description: 使用 Neutron API 存储和检索代理内存。该功能用于保存可通过语义搜索查询的信息，并在会话之间保持代理上下文的一致性。
user-invocable: true
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": ["NEUTRON_API_KEY", "NEUTRON_APP_ID"]}, "primaryEnv": "NEUTRON_API_KEY"}}
---

# Neutron Agent Memory Skill

该功能为AI代理提供了持久化的内存存储支持，并支持语义搜索。用户可以将文本保存为“种子”（seed），通过语义搜索来查找相关内容，并在会话之间保留代理的上下文信息。

## 先决条件

- 通过环境变量配置API凭据：
  ```bash
export NEUTRON_API_KEY=your_key
export NEUTRON_APP_ID=your_app_id
export NEUTRON_EXTERNAL_USER_ID=1  # optional, defaults to 1
```

- 或者将凭据存储在`~/.config/neutron/credentials.json`文件中：
  ```json
{
  "api_key": "your_key_here",
  "app_id": "your_app_id_here",
  "external_user_id": "1"
}
```

## 测试

请验证您的配置是否正确：
  ```bash
./scripts/neutron-memory.sh test  # Test API connection
```

## 脚本

请使用`scripts/`目录中的bash脚本：
- `neutron-memory.sh` - 主要的命令行工具（CLI）

## 常见操作

### 将文本保存为“种子”
  ```bash
./scripts/neutron-memory.sh save "Content to remember" "Title of this memory"
```

### 进行语义搜索
  ```bash
./scripts/neutron-memory.sh search "what do I know about blockchain" 10 0.5
```

### 创建代理上下文
  ```bash
./scripts/neutron-memory.sh context-create "my-agent" "episodic" '{"key":"value"}'
```

### 列出代理上下文
  ```bash
./scripts/neutron-memory.sh context-list "my-agent"
```

### 获取特定上下文
  ```bash
./scripts/neutron-memory.sh context-get abc-123
```

## 交互数据的存储方式（双重存储）

当NeutronMemoryBot处理用户交互时，数据会被存储在两个地方：

1. **代理上下文**：包含结构化元数据和会话跟踪信息的简化版本。
2. **种子**：包含完整对话内容的快照，用于语义搜索。

每次机器人回复用户评论时，整个对话内容（原始帖子、所有评论以及机器人的回复）都会被保存为一个“种子”。这意味着：
- 每个“种子”都代表了完整的对话记录。
- 后来的“种子”会包含比之前的更多上下文信息。
- 语义搜索能够找到最相关的对话状态。
- 数据采用只追加的方式存储：新数据会被添加到现有数据中，旧数据保持不变。

### 种子格式
  ```
Thread snapshot - {timestamp}

Post: {full post content}

Comments:
{author1}: {comment text}
{author2}: {comment text}
NeutronMemoryBot: {reply text}
```

## API接口

- `POST /seeds`：用于保存文本内容（支持multipart/form-data格式）。
- `POST /seeds/query`：用于执行语义搜索（请求体为JSON格式）。
- `POST /agent-contexts`：用于创建代理上下文。
- `GET /agent-contexts`：用于列出所有代理上下文（可选参数`agentId`用于过滤）。
- `GET /agent-contexts/{id}`：用于获取特定的代理上下文。

**身份验证要求：** 所有请求都需要在请求头中添加`Authorization: Bearer $NEUTRON_API_KEY`，并在请求参数中提供`appId`或`externalUserId`。

**内存类型：** `episodic`、`semantic`、`procedural`、`working`。

**种子数据的格式：** `text`、`markdown`、`json`、`csv`、`claude_chat`、`gpt_chat`、`email`。