---
name: intranet
description: "这是一个轻量级的本地HTTP文件服务器，支持插件功能。它可以从指定的webroot目录提供静态文件；通过配置文件，可以将插件目录挂载到特定的URL前缀下；同时，它还可以通过CGI方式执行名为`index.py`的脚本文件。"
summary: "Local HTTP file server with config-based plugins and CGI support."
version: 3.2.7
homepage: https://github.com/odrobnik/intranet-skill
metadata:
  openclaw:
    emoji: "🌐"
    acceptLicenseTerms: true
    requires:
      bins: ["python3"]
---
# 内部网络（Intranet）

这是一个轻量级的本地HTTP文件服务器，无需使用Apache或Nginx，也不需要root权限。它可以提供静态文件服务、挂载插件目录，并通过CGI方式执行`index.py`脚本。

**入口脚本：** `{baseDir}/scripts/intranet.py`

## 设置（Setup）

有关先决条件和设置步骤，请参阅[SETUP.md](SETUP.md)。

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

配置文件存储在`{workspace}/intranet/config.json`中，网站根目录（webroot）位于`{workspace}/intranet/www/`。配置文件不会通过HTTP暴露给外部访问。

## 插件（Plugins）

插件可以通过URL前缀来挂载外部目录。具体配置方法请参见`config.json`：

```json
{
  "plugins": {
    "banker": "{workspace}/skills/banker/web",
    "deliveries": "{workspace}/skills/deliveries/web"
  }
}
```

插件配置支持两种格式：简单格式（仅提供静态内容）和扩展格式（支持CGI功能）：

```json
{
  "plugins": {
    "static-only": "/path/to/dir",
    "with-cgi": {
      "dir": "/path/to/dir",
      "hash": "sha256:abc123..."
    }
  }
}
```

- 插件路径必须位于工作区（workspace）内。
- 如果启用了CGI功能，并且插件包含`hash`值，那么位于插件根目录下的`index.py`脚本将处理所有子路径的请求——但前提是该脚本的SHA-256哈希值必须与配置文件中的哈希值匹配。
- 不包含`hash`值的插件仅提供静态内容（即使启用了CGI功能，这些插件也无法被执行）。
- 生成哈希值的命令：`shasum -a 256 /path/to/index.py`

## CGI执行（CGI Execution）

默认情况下，CGI功能是关闭的。需要在`config.json`中手动启用：

```json
{
  "cgi": true
}
```

启用CGI功能后，只有名为`index.py`的脚本才能通过CGI方式执行：
- **网站根目录（Webroot）**：位于任意子目录下的`index.py`脚本将处理该子目录的所有请求。
- **插件（Plugins）**：位于插件根目录下的`index.py`脚本将处理该插件的所有子路径的请求。
- **其他`.py`文件**：都会收到403 Forbidden错误（既不会被提供，也不会被执行）。
- 所有`.py`文件都必须具有可执行权限（使用`chmod +x`命令设置）。

## 安全性（Security）

- **网站根目录隔离**：配置文件`config.json`位于网站根目录之外，因此不会被公开访问。
- **CGI功能默认关闭**：必须通过`config.json`中的`"cgi": true`选项明确启用。
- **路径限制**：所有解析后的路径都必须位于其所在目录内。虽然会解析符号链接，但会检查目标路径是否在允许的范围内。
- **插件允许列表**：只有那些在`config.json`中明确列出的目录才会被提供服务；这些目录也必须位于工作区内。
- **CGI功能仅限于`index.py`脚本**：不允许执行任意脚本；插件使用CGI功能时需要`config.json`中的哈希值。网站根目录的CGI请求不需要哈希值（因为网站根目录的文件由你直接控制）。
- **所有`.py`文件都被禁止执行**，只有`index.py`脚本除外（既不会以文本形式提供，也不会被执行）。
- **主机访问限制**：`allowed_hosts`选项可以限制允许访问的主机。
- **令牌认证**：可以通过`--token`参数或`config.json`文件进行令牌认证。浏览器客户端首次访问时需要发送`?token=SECRET`请求，系统会设置会话cookie，之后所有请求都会使用`Authorization: Bearer <token>`头部进行认证。
- **路径遍历防护**：所有路径在提供服务之前都会被解析和验证。
- **默认绑定地址**：`127.0.0.1`（仅限本地访问）。要通过`--host 0.0.0.0`访问服务器，需要同时满足令牌认证和`config.json`中的`allowed_hosts`设置。

## 工作区检测（Workspace Detection）

服务器会从`$PWD`（或脚本执行位置）开始遍历目录，寻找`skills/`目录来自动检测工作区的位置。启动时会显示检测到的工作区路径，以便你进行验证。

如果希望跳过自动检测过程，可以将`INTRANET_WORKSPACE`环境变量设置为工作区的根目录：

```bash
INTRANET_WORKSPACE=/path/to/workspace python3 scripts/intranet.py start
```

## 其他注意事项（Notes）：
- 所有状态相关的文件都存储在工作区内：
  - 配置文件：`{workspace}/intranet/config.json`
  - 进程ID：`{workspace}/intranet/.pid`
  - 运行时信息：`{workspace}/intranet/.conf`
  - 网站根目录：`{workspace}/intranet/www/`
- 任何文件都不允许被写入工作区之外。
- 当CGI功能启用时，CGI执行的超时时间为30秒。