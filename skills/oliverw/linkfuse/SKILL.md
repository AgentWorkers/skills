---
name: Linkfuse
description: >
  **创建 Linkfuse 联盟短链接**  
  可以从任意 URL 创建 Linkfuse 联盟短链接。当用户需要创建 Linkfuse 链接、缩短联盟链接或输入 “/linkfuse” 时，可以触发此功能。该功能需要 `LINKFUSE_TOKEN` 环境变量。
compatibility: Requires Node.js 18+, network access and valid Linkfuse API key
metadata:
  source: https://www.linkfuse.net
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - LINKFUSE_TOKEN
  env:
    - name: LINKFUSE_TOKEN
      required: true
      description: Bearer token from https://app.linkfuse.net/user/external-token
---# Linkfuse 技能

通过 Linkfuse REST API 创建一个联盟链接（affiliate link）——该 API 也被 Chrome 和 Firefox 扩展程序使用。

## 触发条件

当用户执行以下操作时，使用此技能：
- 输入 `/linkfuse [url]`
- 请求为某个 URL “创建一个 Linkfuse 链接”
- 希望通过 Linkfuse 缩短一个联盟链接或 Amazon 链接

## 认证

此技能仅从 `LINKFUSE_TOKEN` 环境变量中读取 Bearer 令牌。如果该变量未设置，需告知用户：
> `LINKFUSE_TOKEN` 未设置。请从 `https://app.linkfuse.net/user/external-token` 获取令牌，并将其添加到您的环境变量中：
> ```
> export LINKFUSE_TOKEN=your_token_here
> ```
> 然后重试。
**没有令牌的情况下，切勿继续执行操作。**

## 工作流程

### 第 1 步：获取 URL

如果用户未提供 URL，请先要求用户提供 URL。

### 第 2 步：创建链接

```bash
node scripts/create-link.js --url "<url>"
```

- **退出状态 0**：stdout 包含 JSON 数据 `{ "url": "...", "title": "..." }` —— 进入第 3 步。
- **退出状态 2（未经授权）**：告知用户他们的 `LINKFUSE_TOKEN` 无效或已过期，需要更新令牌。
- **退出状态 1**：向用户显示 stderr 中的错误信息。

### 第 3 步：显示结果

向用户展示生成的链接：
```
✓ Link created: <short-url>
  Title: <title>
```

**提供将链接复制到剪贴板的选项：**
```bash
echo -n "<short-url>" | xclip -selection clipboard 2>/dev/null || echo -n "<short-url>" | pbcopy 2>/dev/null || true
```

## 注意事项

- 每个请求都会附带 `allowRecycle: true` 参数——如果该 URL 之前已被缩短过，系统会返回现有的链接，而不会创建重复链接。
- `X-API-CLIENT: claude-skill` 标头用于向服务器标识当前客户端。