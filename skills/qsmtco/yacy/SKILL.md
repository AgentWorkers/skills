# YaCy 技能

用于控制和管理本地的 YaCy 搜索引擎实例。

## 描述

该技能提供了一个与开源分布式搜索引擎 YaCy 交互的接口，该引擎运行在本地主机上。您可以使用该接口来启动/停止服务、检查状态，并将搜索功能集成到您的 OpenClaw 工作流程中。

## 先决条件

- 已安装并运行 Docker
- 本地主机上的端口 8090 和 8443 可用

## 安装

YaCy 容器运行时，其数据会存储在 Docker 卷（`yacy_search_server_data`）中。安装步骤如下：

```bash
docker run -d --name yacy_search_server -p 8090:8090 -p 8443:8443 -v yacy_search_server_data:/opt/yacy_search_server/DATA --restart unless-stopped --log-opt max-size=200m --log-opt max-file=2 yacy/yacy_search_server:latest
```

访问 Web 界面：http://localhost:8090

默认凭据：admin / yacy（首次登录后可以更改）

## 功能

- [x] 启动 YaCy 容器/守护进程
- [x] 停止 YaCy 容器/守护进程
- [x] 检查 YaCy 的状态
- [x] 执行网页搜索（通过 RSS API）
- [ ] 管理索引（未来版本支持）

## 工具

该技能提供了以下命令：
- `yacy_start` - 启动 YaCy 服务
- `yacy_stop` - 停止 YaCy 服务
- `yacy_status` - 检查 YaCy 是否正在运行并查看日志
- `yacy_search` - 执行搜索查询（如果配置为默认搜索引擎，则会替代 Brave 搜索）

## 配置

配置方式如下：
- 在 OpenClaw 配置文件中设置，或通过环境变量进行设置：
  - `yacy_dir` - YaCy 安装路径（默认：`/home/q/.openclaw/workspace/yacy_search_server`)
  - `port` - HTTP 端口（默认：`8090`）

## 替换 Brave 搜索引擎

要将 YaCy 设置为默认的网页搜索引擎，请按照以下步骤操作：
1. 安装并启动 YaCy。
2. 在 OpenClaw 配置文件中设置：`tools.defaultSearch = "yacy_search"`。
3. 如果之前设置了 `BRAVE_API_KEY` 环境变量，请将其删除。

现在，所有“搜索 X”之类的请求都将使用本地的 YaCy 实例，而不是 Brave。

## 注意事项

YaCy 完全在本地运行，可作为注重隐私的搜索解决方案使用。默认情况下，它会参与全球的 YaCy 对等网络，但您可以在设置中禁用此功能。

## 许可证

GPL 2.0+（与 YaCy 的许可证相同）

---
创建日期：2026-02-11
技能版本：0.1.0
支持的 OpenClaw 版本：2026.2.9+