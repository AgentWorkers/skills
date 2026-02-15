---
name: intranet
description: "一个轻量级的本地HTTP文件服务器，支持插件功能。它可以从指定的webroot目录提供静态文件；通过配置文件，可以将插件目录挂载到特定的URL前缀下；同时，它还能以CGI方式执行名为`index.py`的入口脚本。"
summary: "Local HTTP file server with config-based plugins and CGI support."
version: 3.2.3
homepage: https://github.com/odrobnik/intranet-skill
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["python3"]
---

# 内部网（Intranet）

这是一个轻量级的本地HTTP文件服务器，无需使用Apache或Nginx，也不需要root权限。它可以提供静态文件服务，挂载插件目录，并以CGI方式执行`index.py`脚本。

**入口脚本：** `{baseDir}/scripts/intranet.py`

## 设置（Setup）

有关先决条件和设置说明，请参阅[SETUP.md](SETUP.md)。

## 命令（Commands）

```bash
python3 {baseDir}/scripts/intranet.py start                          # Start on default port 8080
python3 {baseDir}/scripts/intranet.py start --port 9000              # Custom port
python3 {baseDir}/scripts/intranet.py start --host 0.0.0.0            # LAN access (requires token + allowed_hosts)
python3 {baseDir}/scripts/intranet.py start --token SECRET            # Enable bearer token auth
python3 {baseDir}/scripts/intranet.py status                         # Check if running
python3 {baseDir}/scripts/intranet.py stop                           # Stop server
```

## 目录结构（Directory Layout）

配置文件位于`{workspace}/intranet/config.json`，网站根目录（webroot）为`{workspace}/intranet/www/`。配置文件永远不会被暴露在HTTP请求中。

## 插件（Plugins）

插件可以通过URL前缀来挂载外部目录。具体配置方法请参见`config.json`：

```json
{
  "plugins": {
    "banker": "/path/to/banker",
    "deliveries": "/path/to/deliveries"
  }
}
```

插件配置支持两种格式：
- **简单格式**：仅支持静态文件。
- **扩展格式**：支持通过CGI处理动态请求（需要使用SHA-256哈希值）。

- **插件路径要求**：
  - 插件文件必须位于`workspace`目录内。
  - 如果启用了CGI功能并且插件文件包含哈希值，那么位于插件根目录下的`index.py`文件将处理该插件下的所有子路径请求（前提是该文件的SHA-256哈希值与配置中的哈希值匹配）。
  - 不包含哈希值的插件仅提供静态文件服务（即使CGI功能全局启用，这些插件也无法通过CGI处理请求）。
  - 生成哈希值的命令：`shasum -a 256 /path/to/index.py`

## CGI执行（CGI Execution）

**默认情况下，CGI功能是关闭的。**可以通过`config.json`中的`"cgi": true`来启用它。

**启用CGI后的规则：**
- **仅`index.py`文件可以被执行为CGI脚本：**
  - **对于网站根目录下的子目录**：该子目录中的`index.py`文件将处理所有请求。
  - **对于插件**：插件根目录下的`index.py`文件将处理该插件下的所有子路径请求。
  - **其他`.py`文件**：都会收到403 Forbidden错误（既不会被提供也不会被执行）。
- **脚本必须具有可执行权限**（使用`chmod +x`命令设置）。

## 安全性（Security）：
- **网站根目录隔离**：配置文件`config.json`位于`www/`目录之外，因此不会被暴露在HTTP请求中。
- **CGI默认关闭**：必须通过`config.json`中的`"cgi": true`明确启用。
- **路径限制**：所有解析后的路径都必须位于其所在目录内。虽然会解析符号链接，但会检查目标路径是否在允许的范围内。
- **插件访问控制**：只有`config.json`中明确列出的目录才会被提供服务；这些目录也必须位于`workspace`目录内。
- **CGI仅限于`index.py`文件**：不允许执行任意脚本；插件通过CGI处理请求时需要提供SHA-256哈希值。
- **所有`.py`文件都被禁止**：只有`index.py`文件可以被执行；其他`.py`文件既不会被提供也不会被执行。
- **主机访问控制**：`allowed_hosts`列表可以限制允许访问的IP地址。
- **令牌认证**：支持通过`--token`参数或`config.json`配置令牌认证。浏览器客户端访问`?token=SECRET`后，系统会设置会话cookie，之后所有请求都会正常生效。API客户端需要使用`Authorization: Bearer <token>`头部进行认证。
- **路径遍历防护**：所有路径在提供服务前都会被解析和验证。
- **默认绑定地址**：`127.0.0.1`（仅限本地访问）。要通过`--host 0.0.0.0`访问外部主机，需要同时满足令牌认证和`allowed_hosts`的限制。

## 其他注意事项（Notes）：
- 所有状态相关文件都位于`workspace`目录内：
  - 配置文件：`{workspace}/intranet/config.json`
  - 进程ID：`{workspace}/intranet/.pid`
  - 运行时信息：`{workspace}/intranet/.conf`
  - 网站根目录：`{workspace}/intranet/www/`
- 任何文件都不能被写入`workspace`目录之外。
- **CGI执行超时**：如果启用了CGI功能，执行时间限制为30秒。