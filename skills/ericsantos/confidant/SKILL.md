---
name: Confidant
description: **安全地从人类用户向人工智能传递敏感信息**  
当您需要用户提供敏感数据（如 API 密钥、密码、令牌、凭证等）时，请使用此方法。切勿通过聊天工具请求这些信息——请改用 Confidant 工具进行传输。
---

# Confidant – 安全的秘密传递工具

Confidant 允许在不泄露敏感数据的情况下安全地共享秘密。根据需要发送和接收秘密的用户，它支持多种传递方式。

**核心原则：**  
- 需要接收秘密的用户需要运行 `serve-request` 命令；  
- 需要发送秘密的用户需要使用 `fill` 命令（或浏览器表单）。

## 传递方式  

### 1. 用户到代理（用户向 AI 发送秘密）  
**使用场景：** 需要获取用户的秘密信息（如 API 密钥、密码、令牌等）。  

**工作流程：**  
1. 你（作为代理）运行 `serve-request` 命令生成一个 URL。  
2. 将该 URL 分发给用户。  
3. 用户在浏览器中打开该 URL 并输入秘密信息。  
4. 你将在终端中收到秘密信息。  

**相关命令：**  
```bash
npx @aiconnect/confidant serve-request --label "<description>"
```  

**示例对话：**  
> **AI：** 我需要你的 API 密钥才能继续操作。请创建一个安全链接……  
>  
> *(AI 执行：`npx @aiconnect/confidant serve-request --label "API Key"`)*  
>  
> **AI：** 在浏览器中打开此链接并输入你的 API 密钥：`http://localhost:3000/requests/abc123`  
>  
> *(用户输入密码后，AI 收到秘密信息)*  

---

### 2. 代理到用户（AI 向用户发送秘密）  
**使用场景：** 需要将秘密安全地发送给用户（如生成的密码、API 密钥等）。  

**工作流程：**  
1. 用户运行 `serve-request` 命令生成一个接收秘密的 URL。  
2. 用户将此 URL 分发给你。  
3. 你执行 `fill` 命令发送秘密信息。  
4. 用户会在终端中看到收到的秘密信息。  

**相关命令：**  
```bash
npx @aiconnect/confidant fill "<url>" --secret "<value>"
```  

**示例对话：**  
> **AI：** 我已经为你生成了新密码。要安全地接收它，请运行以下命令：  
>  
> ```
> npx @aiconnect/confidant serve-request --label "New Password"
> ```  
>  
> 将显示的 URL 发送给我：`http://192.168.1.100:3000/requests/abc123`  
>  
> *(AI 执行：`npx @aiconnect/confidant fill "http://..." --secret "...")`*  
> **AI：** 完成！密码已发送到你的终端。  

---

### 3. 代理到代理（自动秘密共享）  
**使用场景：** 系统或代理之间的自动凭证传递。  

**工作流程：**  
1. 代理 A（接收方）运行：`npx @aiconnect/confidant serve-request --label "数据库凭证"`  
2. 代理 A 将生成的 URL 通过 API、调度器等方式发送给代理 B（发送方）。  
3. 代理 B 运行：`npx @aiconnect/confidant fill "<url>" --secret "<value>"`  
4. 代理 A 接收到秘密信息。  

**安全输入提示：**  
为避免秘密信息被记录在 shell 历史记录中，请确保使用安全的方式输入秘密。  
```bash
echo "$SECRET" | npx @aiconnect/confidant fill "<url>" --secret -
```  

## 命令参考  

- **创建请求并等待接收秘密：**  
```bash
npx @aiconnect/confidant serve-request --label "<description>"
```  

- **向现有请求提交秘密：**  
```bash
npx @aiconnect/confidant fill "<url>" --secret "<value>"
```  

**输出选项：**  
- `--quiet`：仅输出 URL 和秘密信息（最小化输出）。  
- `--json`：以 JSON 格式输出，便于解析或自动化处理。  

## 重要规则：  
- **切勿要求用户在聊天中粘贴秘密信息**——始终使用 Confidant 进行传递。  
- **切勿在聊天中透露接收到的秘密**——哪怕是部分内容也不行。  
- 如果 24 小时内未使用，秘密信息会自动过期。  
- 信息仅被读取一次后就会被删除。  
- 如果用户位于远程位置，可能需要使用隧道工具（如 ngrok、Tailscale 等）进行安全连接。  

## 接收/发送后的操作：  
- 确认操作完成：显示“收到秘密！”或“已发送！请查看终端”。  
- 仅将秘密用于指定任务，切勿显示或记录其内容。