---
name: dokku
description: 安装、升级并使用 Dokku 来创建应用程序、部署任务、运行一次性任务或后台任务，以及清理容器。当用户需要安装或升级 Dokku、将应用程序部署到 Dokku、在后台运行某些任务，或清理 Dokku 及其容器时，请使用这些功能。相关术语：dokku、安装 Dokku、升级 Dokku、迁移指南、部署、清理、删除冗余资源（prune）、容器（containers）。
metadata: {"openclaw":{"requires":{"bins":["dokku"]}}}
---

# Dokku

Dokku 是一个 PaaS（平台即服务）解决方案；所有命令都在 Dokku 主机上执行（可以通过 SSH 或本地方式连接）。建议将耗时较长的操作（如部署、构建等）放在 **后台** 进行——可以使用 `exec` 命令并设置 `background: true`，或者在工具支持的情况下使用 `yieldMs` 参数来实现后台执行。

## 部分索引

详细的命令语法和示例分别存储在各个对应的部分文件中。执行特定类型操作时，请阅读相应的文件。

| 部分                        | 文件                                      | 命令 / 主题                                      |
| -------------------------- | ------------------------------------------ | ------------------------------------------------------------- |
| 应用                          | [apps/commands.md](apps/commands.md)       | 创建、删除、列出、重命名、克隆、锁定、解锁、报告                    |
| 配置                          | [config/commands.md](config/commands.md)   | 获取、设置、取消设置、导出配置                          |
| 域名                          | [domains/commands.md](domains/commands.md)   | 添加、设置、删除、全局设置、报告域名                        |
| Git / 部署                        | [git/commands.md](git/commands.md)         | 从镜像部署、设置部署分支、推送代码到 Dokku                    |
| 运行（一次性/后台执行）                | [run/commands.md](run/commands.md)         | 直接运行命令；以分离模式运行命令                          |
| 日志                          | [logs/commands.md](logs/commands.md)       | 查看日志；设置日志记录方式                          |
| 进程管理                        | [ps/commands.md](ps/commands.md)           | 调整进程数量、重新构建、重启、停止进程                        |
| 插件                          | [plugin/commands.md](plugin/commands.md)   | 列出插件、安装插件、更新插件、卸载插件                        |
| 证书                          | [certs/commands.md](certs/commands.md)     | 添加证书、删除证书、生成新证书                          |
| Nginx                          | [nginx/commands.md](nginx/commands.md)     | 配置 Nginx 服务器；查看配置信息                        |
| 存储                          | [storage/commands.md](storage/commands.md)     | 挂载存储设备、列出存储资源                          |
| 网络                          | [network/commands.md](network/commands.md)     | 报告网络状态；绑定所有网络接口                        |
| **安装**                        | [install/commands.md](install/commands.md)       | 安装 Dokku；安装后的配置与优化                        |
| **升级**                        | [upgrade/commands.md](upgrade/commands.md)       | 升级 Dokku；升级前请查看迁移指南                        |
| **清理**                        | [cleanup/commands.md](cleanup/commands.md)       | 清理 Dokku 及其相关容器（包括构建工具和应用程序）            |

## 快速参考

- **创建应用：** `dokku apps:create <应用名称>`
- **通过 Git 部署：** 先将应用添加到远程仓库（格式：`dokku@<主机>:<应用名称>`），然后执行 `git push dokku <分支>:master`
- **通过镜像部署：** `dokku git:from-image <应用> <Docker 镜像名称>`
- **在后台运行应用：** `dokku run:detached <应用> <命令>` 或 `dokku run --detach <应用> <命令>`
- **在代理端后台执行：** 对于耗时的部署或安装操作，可以使用 `exec` 命令并设置 `background: true`；根据需要查看日志。

如需查看完整的命令详情和选项，请参阅上述各部分文件。