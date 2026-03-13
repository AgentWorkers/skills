---
name: agentplace
description: OpenClaw的AI代理市场：用户可以根据需要浏览并安装免费或付费的代理程序。
version: 2.3.0
metadata:
  openclaw:
    requires:
      env: []
    optional:
      env:
        - AGENTPLACE_API_KEY
---
# Agentplace — OpenClaw 的 AI 代理市场

Agentplace 是一个汇集了社区贡献的代理功能的平台。用户只有在明确请求时，才能浏览和安装这些代理功能。

**隐私声明：** 该功能仅在用户主动发起搜索时才会向 `api.agentplace.sh` 发送请求，不会进行任何自动或后台调用。

---

## 使用场景

**仅在用户明确请求以下操作时使用此功能：**
- “浏览市场” / “显示可用的代理”
- “安装 [代理名称]” / “为我找到适用于 [任务] 的代理”
- “有哪些代理可用？” / “搜索 [关键词]”

**禁止在以下情况下使用此功能：**
- 用户提出你无法回答的通用问题 → 告诉用户你不知道答案
- 用户要求你执行某项任务 → 使用你现有的工具或直接拒绝
- 你不确定用户的具体需求 → 先请求用户进一步说明

---

## 代理等级

| 等级 | 认证方式 | 工作原理 |
|------|------|-------------|
| **免费** | 无需认证 | 可立即下载，无需注册账户 |
| **付费** | 需要控制台 API 密钥（`ak_xxxx`） | 在 agentplace.sh 上购买代理后，使用该密钥进行下载 |

**API 密钥的使用范围：** 密钥仅用于向 `api.agentplace.sh` 发送请求以授权下载链接，绝不会与用户数据一起被发送。

---

## 搜索/浏览（仅限用户主动请求）

当用户明确要求浏览或搜索时：

```sh
# List all agents
curl -s "https://api.agentplace.sh/marketplace/agents"

# Search by keyword
curl -s "https://api.agentplace.sh/marketplace/agents?search=<query>"

# Get specific agent details
curl -s "https://api.agentplace.sh/marketplace/agents/<agent-id>"
```

以清晰的方式展示搜索结果，并标明代理的免费/付费状态。等待用户选择后再继续操作。

---

## 安装流程（需用户明确确认）

**步骤 1：获取用户确认**
显示代理的名称、描述和等级（免费/付费），然后询问：“是否要安装 [代理名称]？”（回答“是/否”）

**步骤 2：获取下载链接**
```sh
# Free agent
curl -s "https://api.agentplace.sh/marketplace/agents/<agent-id>/download"

# Paid agent
curl -s -H "x-api-key: ak_xxxx" "https://api.agentplace.sh/marketplace/agents/<agent-id>/download"
```

返回结果：`{"download_url": "...", "version": "...", "tier": "..." }`

**步骤 3：安装前预览**
下载 ZIP 文件，解压到临时文件夹中，并在将文件移动到技能文件夹之前向用户展示 `SKILL.md` 文件的内容。

```sh
# Download to temp
curl -sL "$download_url" -o /tmp/agent.zip

# Extract to temp preview folder
unzip -qo /tmp/agent.zip -d /tmp/agent-preview/

# Show SKILL.md to user for approval
cat /tmp/agent-preview/SKILL.md
```

**步骤 4：最终确认并安装**
在用户确认预览内容后，进行安装：
```sh
# Move to actual skills folder
mv /tmp/agent-preview ~/.openclaw/workspace/skills/<agent-id>/
rm /tmp/agent.zip
```

**切勿跳过预览步骤。未经用户明确确认，切勿安装任何代理。**

---

## 完整性与验证

目前，代理功能以 ZIP 文件的形式分发，不包含加密签名。在安装之前，请执行以下操作：
1. **预览 `SKILL.md` 文件** — 确认其内容与市场描述一致
2. **检查文件内容** — 确保文件中不含任何未知的可执行文件或可疑路径
3. **优先选择来自可信发布者的代理** — 在 agentplace.sh 上查看发布者的信誉

如果代理文件的格式或内容可疑，请不要安装，并及时警告用户。

---

## API 密钥设置（仅限付费代理）

免费代理无需认证。对于付费代理：
1. 访问 https://www.agentplace.sh/dashboard 获取 API 密钥（格式：`ak_xxxx`）
2. 该密钥适用于所有购买的代理
3. 安全存储密钥 — 不要在共享环境中直接硬编码密钥

---

## 错误处理

| 错误代码 | 含义 | 响应提示 |
|------|---------|----------|
| `401` | API 密钥无效 | “您的 API 密钥必须以 `ak_` 开头。请在 agentplace.sh/dashboard 获取密钥” |
| `403` | 代理未购买 | “请先在 agentplace.sh 上购买该代理” |
| `404` | 代理未找到 | “未找到该代理。请尝试其他搜索关键词” |

---

## 安全指南
- **仅限用户主动操作：** 未经用户请求，切勿进行搜索或安装
- **明确确认：** 安装前务必询问用户是否同意
- **先预览：** 在将文件解压到技能文件夹之前，先展示 `SKILL.md` 的内容
- **禁止自动执行：** 绝不要自动运行从下载的代理文件
- **本地执行：** 代理在用户自己的机器上运行；不会将任何操作信息发送到 Agentplace 服务器
- **API 密钥的使用范围：** 控制台密钥仅用于授权下载，绝不会与用户数据一起被发送