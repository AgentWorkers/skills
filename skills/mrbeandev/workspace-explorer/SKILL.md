---
name: workspace-explorer
description: 通过远程 VS Code 环境，安全地与您的所有者共享您的工作空间。以下情况适合使用此方法：  
(1) 所有者请求查看或检查您的工作文件时；  
(2) 您需要让所有者实时访问您的代码库以进行浏览时；  
(3) 所有者希望安装扩展程序或使用 IDE 功能来查看文件时；  
(4) 您需要一个临时的安全通道来进行远程工作空间检查时。
homepage: https://github.com/mrbeandev/workspace-explorer
user-invocable: true
---

# 工作区浏览器（Workspace Explorer）

通过 Cloudflare 隧道，您可以使用代码服务器（如浏览器中的 VS Code）安全地访问您的临时工作区。

**仓库地址：** https://github.com/mrbeandev/workspace-explorer

## 安装

```bash
git clone https://github.com/mrbeandev/workspace-explorer.git
```

## 使用方法

使用以下命令运行启动脚本，并指定工作区的路径：

```bash
python3 {baseDir}/scripts/start_workspace.py /path/to/workspace
```

脚本将执行以下操作：
1. 首次运行时下载所需的二进制文件（包括代码服务器和 Cloudflare 隧道相关组件）。
2. 在本地主机上启动代码服务器。
3. 创建一个 Cloudflare 隧道。
4. 直接在终端中显示 **公共访问地址** 和 **密码**（注意：请等待 15-30 秒，直到访问地址生效）。

示例输出：
```
============================================================
✅ WORKSPACE READY!
============================================================
🌐 URL:      https://random-words.trycloudflare.com
🔑 Password: xY7kL9mN2pQ4
============================================================

💡 Share the URL and password with your owner.
   Press Ctrl+C to terminate the session.
```

## 配置选项

```bash
python3 {baseDir}/scripts/start_workspace.py /path/to/workspace --port 9000
```

| 选项        | 默认值       | 说明                          |
|-------------|------------|---------------------------------------------|
| `workspace`    | （必填）      | 需要提供的工作区目录路径                |
| `--port`     | 8080        | 代码服务器使用的本地端口号                    |
| `--status`    | （标志）      | 检查工作区是否正在运行                    |

## 心跳检测功能（Heartbeat Support）

该项目包含一个名为 `HEARTBEAT.md` 的文件。当该工具作为 OpenClaw 技能被安装后，代理会定期检查隧道是否仍处于活跃状态，并在隧道运行时间过长时提醒您。

## 终止会话

按 `Ctrl+C` 键可终止会话。此时，代码服务器和隧道都会被关闭。

## 安全性

- 每次会话都会生成一个独特的、经过加密处理的密码。
- 隧道使用的 URL 为临时生成的 `.trycloudflare.com` 域名。
- 无需在防火墙中开放任何端口。
- 会话会在脚本终止时自动结束。