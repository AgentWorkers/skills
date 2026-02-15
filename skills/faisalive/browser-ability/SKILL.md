---
name: browser-ability
description: 该技能使AI代理能够通过JS脚本登录网站并从中获取数据。
---

# 浏览器操作技能

该技能使AI代理能够通过JavaScript脚本登录网站并获取数据（如果用户所需的工具不可用，则只能直接使用浏览器通过CDP连接进行操作）。这包括那些需要用户手动身份验证的数据源。当需要身份验证时，脚本会提供一个登录URL和一个`signin_id`。代理必须将登录过程交给用户，等待用户确认后，再使用提供的`signin_id`继续数据请求。该技能通过API密钥认证来确保访问的安全性，并支持对敏感或受保护数据源进行人工干预的工作流程。

## 设置

```bash
# Navigate to skill directory
cd skills/browser-ability

# Install dependencies
npm install

# Set CDP URL
# This CDP URL are the same with your browser CDP URL
export CDP_URL="http://[ipv6]:port"
```

---

## 可用方法

### 列出可用工具

```
npm run list
```

### 调用工具

```
npm run call -- TOOL_NAME --args='{"foo":"bar"}'
```

### 登录后调用工具

```
npm run call -- TOOL_NAME --args='{"foo":"bar"}' --signinId=YOUR_SIGNIN_ID
```

---

## 手动登录流程

某些工具的调用需要用户手动登录网站（例如电子商务、银行或基于账户的平台）。

代理**不得**自动执行基于浏览器的登录操作。

---

## 逐步工作流程

### 1. 初始API调用

代理正常调用目标工具。

**示例：**

```
npm run call -- amazon_get_purchase_history
```

---

### 2. 需要登录的响应

如果需要登录，脚本会返回一个登录URL和一个`signin_id`。

**示例响应：**

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"url\":\"https://signinurl\",\"message\":\"Continue to sign in in your browser at https://signinurl.\",\"signin_id\":\"YOUR_SIGNIN_ID\",\"system_message\":\"Try open the url https://signinurl in a browser with a tool if available.Give the url to the user so the user can open it manually in their browser.Then call check_signin tool with the signin_id to check if the sign in process is completed. Once it is completed successfully, then call this tool again to proceed with the action.\"}"
    }
  ],
  "structuredContent": {
    "url": "https://signinurl",
    "message": "Continue to sign in in your browser at https://signinurl.",
    "signin_id": "YOUR_SIGNIN_ID",
    "system_message": "Try open the url https://signinurl in a browser with a tool if available.Give the url to the user so the user can open it manually in their browser.Then call check_signin tool with the signin_id to check if the sign in process is completed. Once it is completed successfully, then call this tool again to proceed with the action."
  },
  "isError": false
}
```

---

### 3. 代理的操作（当需要登录时）

当响应中包含`url`和`signin_id`时，代理必须：

1. 告知用户需要手动登录
2. 将登录URL提供给用户
3. 暂停自动化流程
4. 等待用户确认登录完成

---

### 4. 用户操作

用户：

- 在浏览器中打开提供的URL
- 完成手动登录过程
- 登录完成后通知代理

---

### 5. 继续调用工具

用户确认后，代理重新调用**相同的工具**，并将`signin_id`作为查询参数传递。

**示例：**

```
npm run call -- amazon_get_purchase_history --signinId=YOUR_SIGNIN_ID
```

---

### 6. 最终结果

如果身份验证成功，脚本会返回请求的数据（例如购买历史记录）。

---

## 代理行为约束

- 不得自动打开登录URL
- 不得尝试自动化网站登录
- 在继续之前始终等待用户的明确确认
- 登录后重复使用相同的工具端点
- 如果没有可用的工具，则直接打开浏览器并通过CDP进行浏览

---

## 示例用例

**目标：** 获取亚马逊购买历史记录

1. 调用`amazon_get_purchase_history`
2. 接收登录URL和`signin_id`
3. 请求用户打开URL并登录
4. 等待确认
5. 用`signin_id`重新调用API
6. 接收购买历史记录数据

**目标：** 打开亚马逊密码修改页面

1. 尝试通过CDP打开浏览器，进入亚马逊密码修改页面
2. 由于需要登录而无法打开该页面
3. 调用`amazon_signin`
4. 接收登录URL和`signin_id`
5. 请求用户打开URL并登录
6. 等待确认
7. 再次尝试通过CDP打开浏览器
8. 成功打开密码修改页面

---

## 总结

该技能通过以下方式实现安全的网站登录：

- 将敏感的认证步骤委托给用户
- 在身份验证后恢复自动化工作流程
- 确保一致的安全实践得到执行