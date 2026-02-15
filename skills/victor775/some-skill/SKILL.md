---
name: blueclaw1
description: 通过 OpenClaw (8004scan.io) API 搜索和发现 AI 代理。当用户提到 OpenClaw、需要查找代理、搜索代理或浏览代理注册表时，可以使用该功能。首次使用时，系统会提示用户输入 API 密钥，并将其安全存储起来。
---

# OpenClaw

这是一项用于与 OpenClaw 代理注册表（地址：8004scan.io）交互的技能。

## 设置（首次使用）

**每次调用时**，都需要检查 API 密钥文件是否存在：

```bash
cat ~/.openclaw/api_key 2>/dev/null
```

- **如果文件存在且非空**——从文件中读取密钥并继续执行后续操作。
- **如果文件缺失或为空**——运行设置流程：

### 设置流程

1. 请求用户提供他们的 OpenClaw API 密钥（可以通过对话方式或使用 `AskQuestion` 功能获取）。
2. 保存该密钥：

```bash
mkdir -p ~/.openclaw && chmod 700 ~/.openclaw
echo "USER_PROVIDED_KEY" > ~/.openclaw/api_key
chmod 600 ~/.openclaw/api_key
```

3. 向用户确认密钥已保存到 `~/.openclaw/api_key` 文件中。

> **安全提示**：该目录和文件的权限仅限当前操作系统用户访问。切勿将 API 密钥提交到版本控制系统或记录在任何地方。

---

## 查找代理

当用户请求查找、搜索或发现代理时：

1. 从用户的请求中提取搜索关键词。
2. 发起 API 调用（请替换 `KEYWORDS` 和 `API_KEY`）：

```bash
curl -s -H "X-API-Key: API_KEY" \
  "https://www.8004scan.io/api/v1/agents?search=KEYWORDS&limit=10"
```

3. 解析 JSON 响应，并以清晰、易读的格式展示结果：
   - 代理名称
   - 简要描述
   - API 返回的其他有用信息

如果请求失败（返回 401/403 状态码），请告知用户他们的 API 密钥可能无效，并建议他们重新输入密钥（删除 `~/.openclaw/api_key` 文件后重新运行设置流程）。

---

## 错误处理

| 错误情况 | 处理方式 |
|----------|--------|
| 网络错误 | 通知用户并建议重试 |
| 401/403 | API 密钥无效——建议通过设置流程重新设置密钥 |
| 没有找到匹配结果 | 告知用户没有找到匹配项，并建议使用更宽泛的关键词 |
| 达到请求速率限制（429） | 通知用户并建议稍后重试 |