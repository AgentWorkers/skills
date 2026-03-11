---
name: docker-socket-proxy
description: Manage a remote Docker host via a Tecnativa docker-socket-proxy instance. Unlike raw Docker socket access (which is root-equivalent), docker-socket-proxy acts as a firewall: each API section is individually enabled or disabled via env vars, so the agent only gets access to what you explicitly allow. Requires docker-socket-proxy exposed over TCP. Covers the full Docker REST API surface: container lifecycle (list, start, stop, restart, kill, pause, unpause, rename, exec), inspection (logs, stats, top, changes), images, networks, volumes, Swarm, plugins, system info, and event streaming.
homepage: https://github.com/BP602/docker-socket-proxy
metadata: {"openclaw":{"requires":{"bins":["curl","jq"]}}}
---

# Docker Socket Proxy

该工具通过 `tecnativa/docker-socket-proxy` REST API，利用 `curl` 和 `jq` 来管理 Docker 容器。可用的模式取决于代理实例启用了哪些 API 功能。

## 触发条件

- 用户请求列出、启动、停止、重启、终止、暂停或恢复容器的运行状态。
- 用户需要获取容器的日志、统计信息、正在运行的进程列表或文件系统变更记录。
- 用户对 Docker 镜像、网络、卷、Swarm 服务或相关任务有查询需求。
- 当配置发生变化时，需要重启某个服务。

## 使用方法

```
bash {baseDir}/scripts/run-docker.sh <mode> [args...]
```

不带参数运行即可获取全部功能。代理的 URL 会根据 `$DOCKER_PROXY_URL` 的设置自动解析为 `$DOCKER_HOST`（默认协议为 TCP，端口为 2375，即 `http://localhost:2375`）。

## 可用模式

### 系统相关操作
| 模式          | 描述                          |
|---------------|-------------------------------------------|
| `ping`          | 进行健康检查                        |
| `version`        | 显示 Docker 版本信息                   |
| `info`          | 提供主机概览信息（包括容器、内存等）             |
| `events`        | 显示最近发生的事件（时间范围可自定义）             |
| `system-df`       | 显示镜像/容器/卷的磁盘使用情况             |

### 容器相关操作
| 模式          | 描述                          |
|---------------|-------------------------------------------|
| `list`          | 列出所有正在运行的容器                   |
| `list-all`       | 列出所有容器（包括已停止的容器）                |
| `inspect <name>`     | 查看容器的详细信息                   |
| `top <name> [ps-args]`    | 查看容器内的进程列表                   |
| `logs <name> [tail]`    | 查看容器日志（默认显示最后 100 行）               |
| `stats <name>`     | 获取容器的 CPU、内存、网络和块 I/O 统计信息         |
| `changes <name>`     | 查看容器启动以来的文件系统变更             |
| `start <name>`     | 启动指定的容器                     |
| `stop <name> [timeout]`    | 停止指定的容器                     |
| `restart <name> [timeout]`    | 重启指定的容器                     |
| `kill <name> [signal]`    | 终止指定的容器                     |
| `pause <name>`     | 暂停指定的容器                     |
| `unpause <name>`     | 恢复指定的容器运行                     |
| `rename <name> <new-name>` | 重命名指定的容器                   |
| `exec <name> <cmd> [args...]` | 在容器内执行命令                     |
| `prune-containers`   | 删除已停止的容器                     |

### 镜像相关操作
| 模式          | 描述                          |
|---------------|-------------------------------------------|
| `images`        | 列出所有 Docker 镜像                     |
| `image-inspect <name>` | 查看镜像的详细信息                   |
| `image-history <name>` | 查看镜像的层结构历史                 |
| `prune-images`    | 删除不再使用的镜像                     |

### 网络相关操作
| 模式          | 描述                          |
|---------------|-------------------------------------------|
| `networks`        | 列出所有网络                         |
| `network-inspect <name>` | 查看网络详情及连接的容器                 |
| `prune-networks`    | 删除不再使用的网络                     |

### 卷相关操作
| 模式          | 描述                          |
|---------------|-------------------------------------------|
| `volumes`        | 列出所有卷                         |
| `volume-inspect <name>` | 查看卷的详细信息                   |
| `prune-volumes`    | 删除不再使用的卷                     |

### Swarm 相关操作
| 模式          | 描述                          |
|---------------|-------------------------------------------|
| `swarm`         | 查看 Swarm 的相关信息                   |
| `nodes`        | 列出所有节点                         |
| `node-inspect <name>` | 查看节点的详细信息                   |
| `services`      | 列出所有服务                         |
| `service-inspect <name>` | 查看服务的详细信息                   |
| `service-logs <name> [tail]` | 查看服务的日志                     |
| `tasks`        | 列出所有任务                         |
| `configs`        | 查看配置信息                       |
| `secrets`       | 查看所有加密密钥                         |

### 插件相关操作
| 模式          | 描述                          |
|---------------|-------------------------------------------|
| `plugins`        | 列出所有已安装的插件                     |

## 名称匹配规则

容器名称可以部分匹配——例如 `myapp` 会匹配 `project-myapp-1`。系统会先尝试完全匹配，如果找不到则使用子字符串匹配。如果匹配到的容器数量为 0 或超过 2 个，系统会返回错误信息。

## 注意事项

- 需要使用特定 API 功能的模式（如 `IMAGES`、`NETWORKS`、`VOLUMES`、`SYSTEM`）在代理配置中被禁用时，会返回 HTTP 403 错误。请确保在代理配置中启用相应的环境变量以启用这些功能。
- `exec` 模式需要分两步执行（创建容器和启动容器），并且会合并输出结果流。
- `events` 模式默认使用 1 秒的时间窗口来收集事件信息；可以通过 `--since` 或 `--until` 参数调整时间范围。