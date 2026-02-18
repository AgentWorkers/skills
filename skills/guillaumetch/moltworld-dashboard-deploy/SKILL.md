---
name: moltworld-dashboard-deploy
description: 为真实用户安装、配置并可靠地运行 MoltWorld 控制面板。当需要设置本地运行环境时（包括 README 文件、package.json 文件、.env 文件以及 .gitignore 文件），请使用该控制面板；同时，它还可以用于生成 Docker/Compose/systemd 部署文件，并验证端口 8787 的可用性。此外，该控制面板还能帮助排查系统运行时间或连接性问题。
---
# MoltWorld 仪表盘部署

标准化此工作流程，以便更轻松地运行和安全管理 `moltworld-dashboard`。

## 运行时要求

必需的二进制文件：
- npm
- docker
- docker-compose

可选（仅限需要特权访问的持久化路径）：
- systemd
- sudo

## 安全措施（强制要求）

1. 在项目依赖项经过审核之前，将其视为不可信的。
2. 安装包之前，检查 `package.json` 和 `lockfile` 中是否存在可疑的脚本或依赖项。
3. 在执行任何需要特权或持久化操作的命令（如 `sudo`、`systemctl enable`、在 `/etc/systemd/system` 下写入文件）之前，必须获得明确批准。
4. 首先选择非特权运行方式（本地运行或使用 Docker Compose，无需安装主机级服务）。
5. 绝不要使用 `curl | bash` 或类似的远程脚本执行方式。

## 工作流程

1. 确认基础项目文件存在（`server.mjs`、`public/`）。
2. 如果缺少以下文件，请添加或共享这些文件：
   - `package.json`（启动脚本）
   - `.env.example`
   - `.nvmrc`
   - `.gitignore`
   - `README.md`
3. 如果需要，添加部署文件：
   - `Dockerfile`
   - `docker-compose.yml`
   - `moltworld-dashboard.service`（仅在使用 `systemd` 时需要，并且必须获得明确批准）
4. 验证应用程序是否能够正常启动，并确认 `http://localhost:8787/` 返回 HTTP 200 状态码。
5. 验证应用程序的重启行为及其长期运行的稳定性。
6. 通过 `localhost` 或主机 IP 地址确认应用程序的可访问性。
7. 为操作人员编写运行手册。

## 文件规范要求

- 将运行时状态相关的文件（如 `data/state.json`、日志文件、进程 ID 文件）放在 Git 仓库之外。
- 将敏感信息（如配置文件中的密钥）放在 Git 仓库之外。
- 默认运行时端口为 `8787`。
- `README.md` 必须包含以下内容：
  - 本地快速启动方法
  - 使用 Docker 运行应用程序的步骤
  - 使用 Docker Compose 运行应用程序的步骤
  - 关于使用 `systemd` 安装/启用服务的说明（标明是否需要特权或是否可选）

## 运行时稳定性检查

当服务无法访问时，请执行以下检查：

```bash
ss -ltnp | grep ':8787' || true
curl -I --max-time 5 http://localhost:8787/
```

如果应用程序进程崩溃，请使用监督进程（如 Docker Compose 或已获批准的 systemd 服务）来重启应用程序，而不是手动在前台重新启动它。

## 故障排除快速检查方法

- 服务无法访问：检查 `:8787` 端口的监听器是否正常工作。
- 请求超时：增加 API 请求的超时时间，并在 `postJson` 函数中添加重试机制。
- 如果进程在执行会话后崩溃，请使用监督进程重新启动应用程序。

## 参考资料

- 部署/运行手册中的命令示例：`references/commands.md`