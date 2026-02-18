---
name: browser-auth
description: 启动一个安全的远程浏览器隧道，用于手动用户身份验证（解决验证码、双因素认证（2FA）问题以及登录操作），并捕获会话数据。当代理需要访问需要手动登录或具有机器人防护机制的网站时，可以使用此功能。
---
# 浏览器认证

该功能允许代理程序请求用户在网站上手动登录，然后捕获会话cookie以用于后续的自动化操作。

## 🚨 安全警告：远程代码执行（RCE）风险

如果浏览器访问了恶意网站，运行远程浏览器会话可能会导致**远程代码执行（Remote Code Execution, RCE）**风险。为降低此风险，请采取以下措施：
1. **启用沙箱**：该功能默认以启用沙箱的模式运行Chromium浏览器。
2. **避免访问不安全的网站**：切勿使用此通道访问不可信或未知的URL。
3. **本地绑定**：默认绑定到`127.0.0.1`地址。在没有安全通道（如VPN、SSH或Cloudflare Tunnel）的情况下，切勿将其暴露在公共互联网上。
4. **敏感数据**：生成的`session.json`文件包含明文的会话cookie，请将其视为机密信息。任务完成后请立即删除该文件。

## 环境变量

- `AUTH_HOST`：服务器绑定的IP地址（默认值：`127.0.0.1`）。
- `AUTH_TOKEN`：用于访问该通道的秘密令牌（默认值：随机生成的十六进制字符串）。
- `BROWSER_NO_SANDBOX`：设置为`true`以禁用Chromium的沙箱功能（不推荐）。
- `BROWSER_PROXY`：浏览器的SOCKS5/HTTP代理地址（例如：`socks5://127.0.0.1:40000`）。

## 工作流程

1. **请求认证**：使用`scripts/auth_server.js`启动安全交互式浏览器通道。该脚本会生成一个唯一的访问链接。
2. **提供链接**：将包含令牌的链接提供给用户。
3. **等待用户登录**：等待用户完成登录并点击“完成”按钮。
4. **验证会话**：使用`scripts/verify_session.js`验证会话是否有效。
5. **使用cookie**：在其他浏览器工具中利用捕获到的`session.json`文件。
6. **清理**：任务完成后删除`session.json`文件。

## 工具

### 启动认证服务器
用于启动安全的交互式浏览器通道。
```bash
AUTH_HOST=127.0.0.1 AUTH_TOKEN=secret123 node scripts/auth_server.js <port> <output_session_file>
```
默认端口：`19191`。默认主机：`127.0.0.1`。

### 验证会话
用于检查捕获到的cookie是否能够成功登录用户。
```bash
node scripts/verify_session.js <session_file> <target_url> <expected_string_in_page>
```

## 运行时要求

需要安装以下Node.js包：`express`、`socket.io`和`playwright-core`。