---
name: open-wallet
description: 使用 `https://tx.steer.fun`，可以通过一个可共享的 URL 让用户使用自己的钱包执行某些操作（例如发送交易或签署消息）。当代理需要用户批准/执行 JSON-RPC 请求（如 `eth_sendTransaction`、`personal_sign`、`eth_signTypedData_v4`、`wallet_sendCalls`）并将结果（交易哈希或签名）返回给代理时，可以选择通过 `redirect_url` 来完成这一过程。
---

# 打开钱包（tx.steer.fun）

系统会生成一个链接，用户可以在浏览器中打开该链接。页面会显示请求信息，提示用户连接他们的钱包，切换到指定的链ID（chainId），然后执行相应的JSON-RPC请求。

## 构建链接

基础URL：

`https://tx.steer.fun/`

查询参数：

- `method`：JSON-RPC方法的名称。
- `chainId`：要执行的链ID（应用程序会在执行前切换链）。
- `params`：经过URL编码的JSON数据（可以是对象或数组）。
- `redirect_url`（可选）：请求成功或失败后的重定向地址。

**`redirect_url`的几种模式：**

- **默认模式**：应用程序会在`redirect_url`后面添加`resultType`/`result`（或`error`）作为查询参数。
- **模板模式**：如果`redirect_url`中包含`{{...}}`，应用程序会替换这些占位符，而不会添加额外的查询参数。

**注意事项：**

- 如果`params`是一个JSON数组，它将被直接作为JSON-RPC请求的参数传递。
- 如果`params`是一个JSON对象，应用程序会尝试将其转换为常见的请求格式（例如，从用户连接的钱包中获取`from`字段）。
- 避免双重编码：`params`只需要被编码一次（例如，使用`encodeURIComponent(JSON.stringify(params)`）。如果在URL中看到`%2522`，说明它被编码了两次。

## 常见操作流程

### 签署消息（personal_sign）

使用一个JSON对象：

```text
https://tx.steer.fun/?method=personal_sign&chainId=1&params=%7B%22message%22%3A%22hello%22%7D
```

**预期结果**：签名字符串。

### 发送交易（eth_sendTransaction）

使用一个JSON对象（如果未提供`from`字段，应用程序会从用户连接的钱包中获取该字段）：

```text
https://tx.steer.fun/?method=eth_sendTransaction&chainId=1&params=%7B%22to%22%3A%220x4c5Ce72478D6Ce160cb31Dd25fe6a15DC269592D%22%2C%22data%22%3A%220xd09de08a%22%7D
```

**预期结果**：交易哈希值（tx hash）。

### 类型化数据签名（eth_signTypedData_v4）

提供`{ address, typedData }`：

```text
https://tx.steer.fun/?method=eth_signTypedData_v4&chainId=1&params=%7B%22address%22%3A%220xYourAddress%22%2C%22typedData%22%3A%7B%22types%22%3A%7B%7D%2C%22domain%22%3A%7B%7D%2C%22primaryType%22%3A%22%22%2C%22message%22%3A%7B%7D%7D%7D
```

**预期结果**：签名字符串。

### 批量调用（wallet_sendCalls）

提供`{ calls: [{ to, data }, ...] }`（可选`from`字段）：

```text
https://tx.steer.fun/?method=wallet_sendCalls&chainId=1&params=%7B%22calls%22%3A%5B%7B%22to%22%3A%220x0000000000000000000000000000000000000000%22%2C%22data%22%3A%220x%22%7D%5D%7D
```

**预期结果**：取决于钱包的具体类型，通常是一个ID或交易哈希值。

## 获取结果

### 选项A：不使用`redirect_url`（手动复制结果）

如果省略`redirect_url`，执行完成后页面会显示可复制的响应内容（或错误信息）。

在给用户的消息中，请他们复制以下内容：

- 交易哈希值或签名字符串；
- 如果返回了JSON对象，那么复制整个JSON响应内容。

### 选项B：使用`redirect_url`（自动重定向）

如果包含了`redirect_url`，请求成功或失败后应用程序会自动进行重定向。

**`redirect_url`的参数格式：**

- **成功时：**
  - `resultType=string` 且 `result=<value>`
  - 或 `resultType=json` 且 `result=<JSON.stringify(value)>`
- **失败时：**
  - `error=<message>`

**模板模式（适用于消息应用）：**

- 如果`redirect_url`中包含`{{...}}`，占位符会被替换，不会添加额外的查询参数。
- 可用的占位符：
  - `{{result}}`：经过URL编码的结果字符串（或`JSON.stringify(result)`的结果）。
  - `{{result_raw}}`：未编码的结果字符串（或`JSON.stringify(result)`的结果）。
  - `{{resultType}}`：`string`或`json`类型。
  - `{{error}}`：经过URL编码的错误信息。
  - `{{error_raw}}`：未编码的错误信息。

**对代理程序的实现建议：**

- 可以考虑在用户聊天界面中生成一个“草稿链接”，并将其作为`redirect_url`。这样，在用户批准后，他们会被重定向到一个预先填充好的消息页面，其中包含执行结果。

**示例（用于Telegram分享）：**

**注意：**在使用Telegram分享功能时，建议同时设置`url=`和`text=`。如果省略`url=`，系统可能会直接重定向到`telegram.org`，而不会显示分享界面。

```text
https://tx.steer.fun/?method=personal_sign&chainId=1&params=%7B%22message%22%3A%22hello%22%7D&redirect_url=https%3A%2F%2Ft.me%2Fshare%2Furl%3Furl%3Dhttps%253A%252F%252Ftx.steer.fun%252F%26text%3DSignature%253A%2520%7B%7Bresult%7D%7D
```

## 安全性检查**

- 在请求用户点击链接之前，务必用通俗易懂的语言向用户说明该请求的具体用途（例如：调用的是哪个合约、执行的是哪个函数、在哪个链上操作、以及会修改什么数据）。
- 尽量使用权限最小的请求方式；避免请求不必要的权限。